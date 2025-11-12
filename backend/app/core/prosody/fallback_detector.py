"""
Fallback meter detection for undiacritized text.

When primary detection fails, this module attempts alternative strategies
to detect the meter, including pattern relaxation and statistical matching.
"""

from typing import List, Optional, Tuple
from difflib import SequenceMatcher
from .detector_v2 import BahrDetectorV2, DetectionResult, MatchQuality
from .meters import Meter
import logging

logger = logging.getLogger(__name__)


class FallbackDetector:
    """
    Provides fallback detection strategies when primary detection fails.

    Strategies:
    1. Relaxed similarity matching (lower threshold)
    2. Length-based meter prediction
    3. Pattern normalization and retry
    """

    def __init__(self, primary_detector: BahrDetectorV2):
        """Initialize with primary detector instance."""
        self.primary_detector = primary_detector

    def detect_with_fallback(
        self,
        phonetic_pattern: str,
        confidence_threshold: float = 0.75
    ) -> Optional[DetectionResult]:
        """
        Try multiple detection strategies in order of reliability.

        Args:
            phonetic_pattern: Input phonetic pattern
            confidence_threshold: Minimum confidence for primary detection

        Returns:
            Best detection result or None
        """
        # Try primary detection first
        primary_results = self.primary_detector.detect(phonetic_pattern, top_k=3)

        if primary_results and primary_results[0].confidence >= confidence_threshold:
            logger.info(f"[Fallback] Primary detection succeeded: {primary_results[0].meter_name_ar}")
            return primary_results[0]

        logger.info(f"[Fallback] Primary detection weak (confidence={primary_results[0].confidence:.2%} if primary_results else 0), trying fallback strategies...")

        # Strategy 1: Ultra-relaxed similarity matching (70% threshold)
        result = self._relaxed_similarity_match(phonetic_pattern)
        if result:
            logger.info(f"[Fallback] Relaxed similarity matched: {result.meter_name_ar}")
            return result

        # Strategy 2: Length-based prediction
        result = self._length_based_prediction(phonetic_pattern)
        if result:
            logger.info(f"[Fallback] Length-based prediction: {result.meter_name_ar}")
            return result

        logger.warning("[Fallback] All strategies failed")
        return primary_results[0] if primary_results else None

    def _relaxed_similarity_match(
        self,
        phonetic_pattern: str,
        threshold: float = 0.70
    ) -> Optional[DetectionResult]:
        """
        Find best match with very relaxed similarity threshold.

        This is useful for undiacritized text where the pattern might
        be significantly off but the meter is still identifiable.

        Uses frequency-based tie-breaking to prefer common meters when
        similarities are close (within 5% of each other).
        """
        # Collect all matches above threshold with meter frequency info
        candidates: List[Tuple[float, Meter, str, int, int]] = []

        # Check all meters
        for meter_id, meter in self.primary_detector.meters.items():
            valid_patterns = self.primary_detector.pattern_cache[meter_id]
            best_sim_for_meter = 0.0
            best_pat_for_meter = None

            for cached_pattern in valid_patterns:
                similarity = SequenceMatcher(
                    None,
                    phonetic_pattern,
                    cached_pattern
                ).ratio()

                if similarity > best_sim_for_meter:
                    best_sim_for_meter = similarity
                    best_pat_for_meter = cached_pattern

            if best_sim_for_meter >= threshold:
                candidates.append((
                    best_sim_for_meter,
                    meter,
                    best_pat_for_meter,
                    meter.tier.value,  # Lower is better (Tier 1 = most common)
                    meter.frequency_rank  # Lower is better (rank 1 = most frequent)
                ))

        if not candidates:
            return None

        # Sort by: 1) similarity (desc), 2) tier (asc), 3) frequency_rank (asc)
        # This ensures that if similarities are close, we prefer الطويل and other common meters
        candidates.sort(key=lambda x: (-x[0], x[3], x[4]))

        # Get best match
        best_similarity, best_meter, best_cached_pattern, _, _ = candidates[0]

        if best_similarity >= threshold and best_meter:
            # Calculate adjusted confidence
            # Penalize for using fallback but still give reasonable confidence
            confidence = best_similarity * 0.85  # 15% penalty for fallback

            # Create result
            generator = self.primary_detector.generators[best_meter.id]
            tracked_patterns = generator.generate_with_tracking()

            transformations = []
            for pat, trans in tracked_patterns:
                if pat == best_cached_pattern:
                    transformations = trans
                    break

            match_quality = MatchQuality.MODERATE if best_similarity >= 0.80 else MatchQuality.WEAK

            explanation_ar = f"مطابقة تقريبية ({best_similarity:.0%}) - قد يكون النص يحتاج إلى تشكيل"
            explanation_en = f"Approximate match ({best_similarity:.0%}) - text may need diacritics"

            return DetectionResult(
                meter_id=best_meter.id,
                meter_name_ar=best_meter.name_ar,
                meter_name_en=best_meter.name_en,
                confidence=confidence,
                match_quality=match_quality,
                matched_pattern=best_cached_pattern,
                input_pattern=phonetic_pattern,
                transformations=transformations,
                explanation=f"{explanation_ar} | {explanation_en}"
            )

        return None

    def _length_based_prediction(
        self,
        phonetic_pattern: str
    ) -> Optional[DetectionResult]:
        """
        Predict meter based on pattern length and characteristics.

        This is a last resort for heavily corrupted patterns.
        Uses statistical knowledge about typical pattern lengths.
        """
        pattern_len = len(phonetic_pattern)
        harakat_count = phonetic_pattern.count('/')
        sukun_count = phonetic_pattern.count('o')

        # Typical pattern lengths for common meters (single hemistich)
        # Based on statistical analysis of the golden set
        METER_LENGTH_PROFILES = {
            1: (20, 25, "الطويل"),      # at-Tawil: 20-25 chars
            2: (16, 21, "الكامل"),      # al-Kamil: 16-21 chars
            6: (16, 20, "المتقارب"),    # al-Mutaqarib: 16-20 chars
            4: (18, 22, "الرمل"),       # ar-Ramal: 18-22 chars
            3: (18, 22, "الوافر"),      # al-Wafir: 18-22 chars
        }

        candidates = []

        for meter_id, (min_len, max_len, meter_name) in METER_LENGTH_PROFILES.items():
            if min_len <= pattern_len <= max_len:
                # Calculate simple confidence based on length match
                center = (min_len + max_len) / 2
                deviation = abs(pattern_len - center)
                max_deviation = (max_len - min_len) / 2
                length_score = 1.0 - (deviation / max_deviation) if max_deviation > 0 else 1.0

                meter = self.primary_detector.meters[meter_id]
                candidates.append((meter, length_score * 0.60))  # Max 60% confidence

        if candidates:
            # Sort by confidence
            candidates.sort(key=lambda x: x[1], reverse=True)
            best_meter, confidence = candidates[0]

            explanation_ar = "تخمين بناءً على طول النمط - يُنصح بإضافة التشكيل"
            explanation_en = "Prediction based on pattern length - diacritics recommended"

            return DetectionResult(
                meter_id=best_meter.id,
                meter_name_ar=best_meter.name_ar,
                meter_name_en=best_meter.name_en,
                confidence=confidence,
                match_quality=MatchQuality.WEAK,
                matched_pattern="",
                input_pattern=phonetic_pattern,
                transformations=["predicted"],
                explanation=f"{explanation_ar} | {explanation_en}"
            )

        return None


def detect_with_all_strategies(
    detector: BahrDetectorV2,
    phonetic_pattern: str
) -> Optional[DetectionResult]:
    """
    Convenience function to run all detection strategies.

    Args:
        detector: BahrDetectorV2 instance
        phonetic_pattern: Input phonetic pattern

    Returns:
        Best detection result or None
    """
    fallback = FallbackDetector(detector)
    return fallback.detect_with_fallback(phonetic_pattern)
