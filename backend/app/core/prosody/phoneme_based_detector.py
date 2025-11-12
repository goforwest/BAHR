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
    top_k: int = 3
) -> List[Tuple[int, str, float, str]]:
    """
    Detect meter using phoneme-based fitness matching.

    Instead of comparing extracted patterns directly, this method:
    1. Extracts phonemes from text
    2. Tests fitness of all cached patterns for each meter
    3. Returns meters with best-fitting patterns

    Args:
        text: Arabic text (normalized)
        has_tashkeel: Whether text has diacritical marks
        detector: Initialized BahrDetectorV2 instance
        top_k: Number of top results to return

    Returns:
        List of (meter_id, meter_name_ar, fitness_score, best_pattern) tuples
    """
    # Extract phonemes
    try:
        phonemes = extract_phonemes(text, has_tashkeel=has_tashkeel)
    except Exception:
        return []

    if not phonemes:
        return []

    # Test fitness for each meter
    meter_scores = []

    for meter_id, cached_patterns in detector.pattern_cache.items():
        if not cached_patterns:
            continue

        # Find best-fitting pattern for this meter
        best_fitness = 0.0
        best_pattern = None

        for pattern in cached_patterns:
            fitness = calculate_pattern_fitness(phonemes, pattern)

            if fitness > best_fitness:
                best_fitness = fitness
                best_pattern = pattern

        if best_fitness > 0.0 and best_pattern:
            meter = METERS_REGISTRY.get(meter_id)
            if meter:
                meter_scores.append((
                    meter_id,
                    meter.name_ar,
                    best_fitness,
                    best_pattern
                ))

    # Sort by fitness score (descending), then by meter tier (prefer common meters for ties)
    # This is critical for breaking ties when multiple meters have similar fitness
    meter_scores_with_tier = []
    for meter_id, meter_name, fitness, pattern in meter_scores:
        meter = METERS_REGISTRY.get(meter_id)
        tier_value = meter.tier.value if meter else 999  # Lower tier value = more common
        meter_scores_with_tier.append((meter_id, meter_name, fitness, pattern, tier_value))

    # Sort by: 1) fitness (descending), 2) tier (ascending - prefer common meters)
    meter_scores_with_tier.sort(key=lambda x: (-x[2], x[4]))

    # Remove tier from results
    meter_scores = [(mid, name, fit, pat) for mid, name, fit, pat, _ in meter_scores_with_tier]

    # Return top K
    return meter_scores[:top_k]


def detect_meter_from_text(
    text: str,
    has_tashkeel: bool,
    detector: BahrDetectorV2,
    min_fitness: float = 0.50
) -> Optional[DetectionResult]:
    """
    Detect meter from Arabic text using phoneme fitness.

    This is the main entry point for phoneme-based detection.
    It provides a DetectionResult compatible with the standard API.

    Args:
        text: Arabic text (normalized)
        has_tashkeel: Whether text has diacritical marks
        detector: Initialized BahrDetectorV2 instance
        min_fitness: Minimum fitness threshold (default: 0.50 = 50%)

    Returns:
        DetectionResult for best match, or None if no good match
    """
    results = detect_with_phoneme_fitness(text, has_tashkeel, detector, top_k=1)

    if not results:
        return None

    meter_id, meter_name_ar, fitness, best_pattern = results[0]

    # Check if fitness meets minimum threshold
    if fitness < min_fitness:
        return None

    # Get meter details
    meter = METERS_REGISTRY.get(meter_id)
    if not meter:
        return None

    # Convert fitness to confidence (fitness already in 0-1 range)
    confidence = fitness

    # Determine match quality based on fitness
    if fitness >= 0.90:
        match_quality = MatchQuality.EXACT
        explanation_ar = "تطابق ممتاز"
        explanation_en = "Excellent match"
    elif fitness >= 0.75:
        match_quality = MatchQuality.STRONG
        explanation_ar = "تطابق قوي"
        explanation_en = "Strong match"
    elif fitness >= 0.60:
        match_quality = MatchQuality.MODERATE
        explanation_ar = "تطابق جيد"
        explanation_en = "Moderate match"
    else:
        match_quality = MatchQuality.WEAK
        explanation_ar = "تطابق ضعيف"
        explanation_en = "Weak match"

    # Create detection result
    return DetectionResult(
        meter_id=meter_id,
        meter_name_ar=meter_name_ar,
        meter_name_en=meter.name_en,
        confidence=confidence,
        match_quality=match_quality,
        matched_pattern=best_pattern,
        input_pattern="<phoneme-based>",  # Not using direct pattern matching
        transformations=[],
        explanation=f"{explanation_ar} | {explanation_en}"
    )
