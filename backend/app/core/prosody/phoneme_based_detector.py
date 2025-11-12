"""
Phoneme-based meter detection using fitness matching.

This detector matches phoneme structures from actual text to cached patterns
using fitness scoring, similar to how the golden set was preprocessed.
This approach handles the mismatch between actual syllable scansion and
theoretical tafila patterns.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass

from app.core.phonetics import Phoneme, extract_phonemes
from .detector_v2 import BahrDetectorV2, DetectionResult, MatchQuality
from .meters import METERS_REGISTRY


def calculate_pattern_fitness(
    phonemes: List[Phoneme],
    pattern: str
) -> float:
    """
    Calculate how well a cached pattern "fits" a phoneme sequence.

    This uses heuristics based on:
    - Pattern length vs phoneme count
    - Ratio of / to o symbols (harakat vs sukunat)
    - Structural similarity (harakat/sakin ratios and distribution)
    - Penalty for large count mismatches

    Args:
        phonemes: List of phonemes extracted from text
        pattern: Cached pattern to test fitness against

    Returns:
        Fitness score (0.0-1.0), where 1.0 is perfect fit
    """
    if not phonemes or not pattern:
        return 0.0

    # Count phoneme types
    n_harakas = sum(1 for p in phonemes if p.vowel in ['a', 'u', 'i'])
    n_sakins = sum(1 for p in phonemes if p.is_sukun())
    n_long = sum(1 for p in phonemes if p.is_long_vowel())
    n_tanween = sum(1 for p in phonemes if p.vowel in ['an', 'un', 'in'])

    # Count pattern symbols
    n_haraka_in_pattern = pattern.count('/')
    n_sakin_in_pattern = pattern.count('o')

    # Use the original fitness function from precompute_golden_patterns.py
    # This function gives high scores to patterns with similar counts,
    # which works when combined with tier-based tie-breaking

    total_sakins = n_sakins + n_long + n_tanween

    # 1. Harakat count ratio
    if max(n_harakas, n_haraka_in_pattern) > 0:
        haraka_ratio = min(n_harakas, n_haraka_in_pattern) / max(n_harakas, n_haraka_in_pattern)
    else:
        haraka_ratio = 0.0

    # 2. Sakin count ratio
    if max(total_sakins, n_sakin_in_pattern) > 0:
        sakin_ratio = min(total_sakins, n_sakin_in_pattern) / max(total_sakins, n_sakin_in_pattern)
    else:
        sakin_ratio = 0.0

    # 3. Length ratio
    expected_length = n_harakas + total_sakins
    pattern_len = len(pattern)
    if max(pattern_len, expected_length) > 0:
        length_ratio = min(pattern_len, expected_length) / max(pattern_len, expected_length)
    else:
        length_ratio = 0.0

    # Overall fitness (weighted average - same as golden set preprocessing)
    fitness = (haraka_ratio * 0.4 + sakin_ratio * 0.4 + length_ratio * 0.2)

    return fitness


def detect_with_phoneme_fitness(
    text: str,
    has_tashkeel: bool,
    detector: BahrDetectorV2,
    top_k: int = 3,
    use_hybrid_scoring: bool = True
) -> List[Tuple[int, str, float, str]]:
    """
    Detect meter using phoneme-based fitness matching.

    Instead of comparing extracted patterns directly, this method:
    1. Extracts phonemes from text
    2. Tests fitness of all cached patterns for each meter
    3. Optionally combines fitness with pattern similarity (hybrid scoring)
    4. Returns meters with best scores

    Args:
        text: Arabic text (normalized)
        has_tashkeel: Whether text has diacritical marks
        detector: Initialized BahrDetectorV2 instance
        top_k: Number of top results to return
        use_hybrid_scoring: If True, combines fitness and pattern similarity

    Returns:
        List of (meter_id, meter_name_ar, score, best_pattern) tuples
    """
    from app.core.phonetics import text_to_phonetic_pattern
    from difflib import SequenceMatcher

    # Extract phonemes
    try:
        phonemes = extract_phonemes(text, has_tashkeel=has_tashkeel)
    except Exception:
        return []

    if not phonemes:
        return []

    # Also extract pattern if using hybrid scoring
    extracted_pattern = None
    if use_hybrid_scoring:
        try:
            extracted_pattern = text_to_phonetic_pattern(text, has_tashkeel=has_tashkeel)
        except Exception:
            pass

    # Test fitness for each meter
    meter_scores = []

    for meter_id, cached_patterns in detector.pattern_cache.items():
        if not cached_patterns:
            continue

        # Find best-fitting pattern for this meter
        best_fitness = 0.0
        best_similarity = 0.0
        best_pattern = None

        for pattern in cached_patterns:
            # Calculate fitness (phoneme-based)
            fitness = calculate_pattern_fitness(phonemes, pattern)

            # Calculate similarity (pattern-based) if available
            similarity = 0.0
            if extracted_pattern:
                similarity = SequenceMatcher(None, extracted_pattern, pattern).ratio()

            # Hybrid score: weighted combination of fitness and similarity
            if use_hybrid_scoring and extracted_pattern:
                # Give more weight to similarity for diacritized text (more accurate patterns)
                # Give more weight to fitness for undiacritized text (patterns less reliable)
                if has_tashkeel:
                    score = (similarity * 0.65) + (fitness * 0.35)
                else:
                    score = (similarity * 0.50) + (fitness * 0.50)
            else:
                score = fitness

            if score > best_fitness or (score == best_fitness and similarity > best_similarity):
                best_fitness = score
                best_similarity = similarity
                best_pattern = pattern

        if best_fitness > 0.0 and best_pattern:
            meter = METERS_REGISTRY.get(meter_id)
            if meter:
                meter_scores.append((
                    meter_id,
                    meter.name_ar,
                    best_fitness,
                    best_pattern,
                    best_similarity
                ))

    # CRITICAL: Smart frequency-based tie-breaking
    # Only apply frequency boost when scores are close (competitive range)
    # This prevents over-boosting while helping الطويل when appropriate

    if not meter_scores:
        return []

    # Find the highest score
    max_score = max(score for _, _, score, _, _ in meter_scores)

    # Competitive threshold: meters within 10% of the top score are "competing"
    competitive_threshold = max_score - 0.10

    meter_scores_with_ranking = []
    for meter_id, meter_name, score, pattern, similarity in meter_scores:
        meter = METERS_REGISTRY.get(meter_id)
        tier_value = meter.tier.value if meter else 999
        freq_rank = meter.frequency_rank if meter else 999

        # Only apply frequency boost if meter is competitive (within 10% of top score)
        if score >= competitive_threshold:
            # Calculate frequency boost for competitive meters only
            # الطويل (rank 1) is by far the most common meter in classical Arabic poetry
            if freq_rank == 1:
                freq_boost = 0.08  # +8% for الطويل when competitive
            elif freq_rank == 2:
                freq_boost = 0.06  # +6% for الكامل when competitive
            elif freq_rank <= 5:
                freq_boost = 0.03  # +3% for ranks 3-5 when competitive
            elif freq_rank <= 10:
                freq_boost = 0.01  # +1% for ranks 6-10 when competitive
            else:
                freq_boost = 0.0
        else:
            # Not competitive - no boost
            freq_boost = 0.0

        # Apply frequency boost to score
        boosted_score = min(1.0, score + freq_boost)

        meter_scores_with_ranking.append((
            meter_id, meter_name, boosted_score, pattern,
            tier_value, freq_rank, similarity, score  # Keep original score for reference
        ))

    # Sort by: boosted_score (desc), tier (asc), freq_rank (asc)
    meter_scores_with_ranking.sort(key=lambda x: (-x[2], x[4], x[5]))

    # Remove ranking info from results, return boosted score
    meter_scores = [(mid, name, boosted, pat) for mid, name, boosted, pat, _, _, _, _ in meter_scores_with_ranking]

    # Return top K
    return meter_scores[:top_k]


def detect_meter_from_text(
    text: str,
    has_tashkeel: bool,
    detector: BahrDetectorV2,
    min_score: float = 0.50,
    use_hybrid: bool = True
) -> Optional[DetectionResult]:
    """
    Detect meter from Arabic text using hybrid scoring (fitness + similarity).

    This is the main entry point for enhanced phoneme-based detection.
    It combines phoneme fitness with pattern similarity for better accuracy.

    Args:
        text: Arabic text (normalized)
        has_tashkeel: Whether text has diacritical marks
        detector: Initialized BahrDetectorV2 instance
        min_score: Minimum score threshold (default: 0.50 = 50%)
        use_hybrid: Whether to use hybrid scoring (default: True)

    Returns:
        DetectionResult for best match, or None if no good match
    """
    results = detect_with_phoneme_fitness(
        text, has_tashkeel, detector,
        top_k=1,
        use_hybrid_scoring=use_hybrid
    )

    if not results:
        return None

    meter_id, meter_name_ar, score, best_pattern = results[0]

    # Check if score meets minimum threshold
    if score < min_score:
        return None

    # Get meter details
    meter = METERS_REGISTRY.get(meter_id)
    if not meter:
        return None

    # Convert score to confidence
    confidence = score

    # Determine match quality based on score
    if score >= 0.85:
        match_quality = MatchQuality.EXACT
        explanation_ar = "تطابق ممتاز (مزيج من التشابه الهيكلي والصوتي)"
        explanation_en = "Excellent match (hybrid structural + phonetic)"
    elif score >= 0.70:
        match_quality = MatchQuality.STRONG
        explanation_ar = "تطابق قوي"
        explanation_en = "Strong match"
    elif score >= 0.55:
        match_quality = MatchQuality.MODERATE
        explanation_ar = "تطابق جيد"
        explanation_en = "Moderate match"
    else:
        match_quality = MatchQuality.WEAK
        explanation_ar = "تطابق ضعيف - يُنصح بإضافة التشكيل"
        explanation_en = "Weak match - diacritics recommended"

    # Create detection result
    return DetectionResult(
        meter_id=meter_id,
        meter_name_ar=meter_name_ar,
        meter_name_en=meter.name_en,
        confidence=confidence,
        match_quality=match_quality,
        matched_pattern=best_pattern,
        input_pattern="<hybrid-scoring>",  # Using combined fitness + similarity
        transformations=[],
        explanation=f"{explanation_ar} | {explanation_en}"
    )
