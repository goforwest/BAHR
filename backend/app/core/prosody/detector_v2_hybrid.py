"""
BahrDetectorV2Hybrid - Hybrid approach combining empirical patterns with fuzzy matching.

This detector uses:
1. Empirical patterns from old BahrDetector (proven 50.3% accuracy)
2. Fuzzy matching with weighted edit distance (new enhancement)
3. Hemistich pattern support (new enhancement)
4. Enhanced result schema with match_type and similarity fields

Strategy:
- Primary: Exact match against empirical patterns
- Secondary: Fuzzy match against empirical patterns (threshold: 70%)
- Tertiary: Fuzzy match against theoretical patterns (threshold: 85%)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from collections import defaultdict

from .pattern_similarity import PatternSimilarity
from .meters import METERS_REGISTRY
from .pattern_generator import PatternGenerator


@dataclass
class DetectionResult:
    """Result of meter detection."""
    meter_id: int
    meter_name_ar: str
    meter_name_en: str
    confidence: float
    matched_pattern: str
    input_pattern: str
    similarity: float
    match_type: str  # 'exact_empirical', 'fuzzy_empirical', 'fuzzy_theoretical'
    explanation: str

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "meter_id": self.meter_id,
            "meter_name_ar": self.meter_name_ar,
            "meter_name_en": self.meter_name_en,
            "confidence": round(self.confidence, 3),
            "matched_pattern": self.matched_pattern,
            "input_pattern": self.input_pattern,
            "similarity": round(self.similarity, 3),
            "match_type": self.match_type,
            "explanation": self.explanation,
        }


# Empirical patterns extracted from real poetry (from old BahrDetector)
EMPIRICAL_PATTERNS = {
    1: {  # الطويل
        "name_ar": "الطويل",
        "name_en": "al-Tawil",
        "patterns": [
            "//////o//o//oo//o///o/o",
            "//////o/o/o//o///o//",
            "//o///////o/////o//ooo",
            "//o///o//o//oo//o///o//",
            "//o///o/o/o//o//o////o//o",
            "//o//o////o///o////o////o/o",
            "//o/o////o/////////////o",
            "//o/o//o///o//o/o//o//",
            "//o/o/o//o///o//o/",
            "/o/o///o///o/o//o//o///o",
            "/o/o//o////o//o///o//",
            "///o//o///o/o///o//o/o///o",
            "//////ooo////o/o////////o",
            "/////oo///////o//o/",
            "//o/////o///o////o/o///",
            "//o////o///////o/o//o//",
            "//o////o/o///o//////o/oo",
            "//o////o///o//o/o/////",
            "//o/o//o/o/o///o/o///o//o",
            "//o////////////o////////o",
            "//ooo////o/////ooo//o//o",
            "//o//o//o////oo///////oo",
            "///o//////o///o///o//o",
            "//o//////o///o//o////////",
            "//////o///o//o///o//o",
        ],
    },
    2: {  # الكامل
        "name_ar": "الكامل",
        "name_en": "al-Kamil",
        "patterns": [
            "///o//o///o//o/o/o//",
            "//o/////o/o//o/o//o//",
            "//o///o/o//////o/o/o/////o",
            "//o//o///o///oo//o///o",
            "//o//o//o//o//o///////",
            "//o/o//o///o//o////o///",
            "//o/o//o//oo////o/o//o///o",
            "/o//o//o///o/o//o/o///o",
            "/o/o//o/o///o//ooo///o//o",
            "//o/o//o///o/////",
            "//o///o//o////o//ooo//o//",
            "////////o/o////o////o",
            "//o///o/o/o/////o///////o",
            "/o/o//o///o//oo///o///o/",
            "//o/o//o///o////o//o///o",
            "/o////o/o/o///o///o//o",
        ],
    },
    3: {  # الوافر
        "name_ar": "الوافر",
        "name_en": "al-Wafir",
        "patterns": [
            "////////o/////o///o//o",
            "//////o/////o//o////o//",
            "//o////////o///o//////",
            "//o//////o///o//o//o/////",
            "//o///o/o//o///o//",
            "//o///o/o//o///o/////o",
            "//o/o////o/////o/o//o//o",
            "//o/o//o//o//oo//o/o//o//o",
            "//o/o//o/o/ooo///o//o//o",
            "//ooo///o//o//o/o//o//o",
            "//o/o////o/o//o/o/////o",
            "//o////o/o/o//o///o//",
            "/o//o///o////o/////",
        ],
    },
    4: {  # الرمل
        "name_ar": "الرمل",
        "name_en": "al-Ramal",
        "patterns": [
            "//////o//o//o////////o",
            "/o/////o/o///o///",
            "/o////o/o/o///o///",
            "/o////o/o/o//o/o//oo//o/////o",
            "/o//o/o//o/o//////////o",
            "/o//o/o/o//////o",
            "/o/o//o/o//o/o/o///o///o",
            "/o/o/o///////o///o///o",
            "//////////o////o//ooo",
            "//o///oo/o/o//o//////",
            "/o//o/////////o//o/o//o///o",
            "//o/o////o////o/////o/",
            "//o////o//oo/////o//o/",
        ],
    },
    5: {  # البسيط
        "name_ar": "البسيط",
        "name_en": "al-Basit",
        "patterns": [
            "////o//o/o////o///o//o",
            "//o////////////o/o////o//",
            "//o//////o//o///o////o",
            "//o/////o/o/o//o///o//",
            "//o////o//o/o/o////o/",
            "//o////o/o/////o///o///o",
            "//o//o/////o/o//o/o///o//",
            "//o/o////o/////o///o///o",
            "//o/o//o//o/o/o//o/o//o//o",
            "/o/o///o//o//o//////",
            "/o/oo//o/o//o////o//o///",
            "//o/o////o/o//o/////o//",
            "//o///////////o//o/o///",
            "//o///o///o///o/////o",
            "//o///o/o//////o//o//o",
        ],
    },
    6: {  # المتقارب
        "name_ar": "المتقارب",
        "name_en": "al-Mutaqarib",
        "patterns": [
            "//////o///o//o///o//",
            "///o///o///o/o/o/o//o////",
            "//o///////o//////o/o",
            "//o///o//oo//////o/////o",
            "//o///o/o//o/////o///o",
            "//o///o/o/o////o///o/o///",
            "//o/o////o/o/o//o///o///o",
            "/o/o//o//o//o/o/o//o/////",
            "//o/////o//o///o////",
            "/o/o//////o//////////",
        ],
    },
    7: {  # الرجز
        "name_ar": "الرجز",
        "name_en": "al-Rajaz",
        "patterns": [
            "//o//o///o/o/o//o///",
            "//o/o///o/o///o//////o//",
            "//o/o//o///////o//o/o//",
            "//o/o//o///o////o//o///o",
            "/o////////o/////o/o///o",
            "/o////o/o////////o///o///",
            "/o/o////o//o/o///o/o////o",
            "/o/o///o////o///o//////",
        ],
    },
    8: {  # الهزج
        "name_ar": "الهزج",
        "name_en": "al-Hazaj",
        "patterns": [
            "/o//o///////////",
            "/o//o///o///o//o///o",
            "/o//o//o////o/o//o//",
            "/o//o//o///o//o///oo//",
            "/o/o/////o//o///o////",
            "/o/o//o/o/////o/o",
            "/o/o/o//o///o////o/o//o/o",
        ],
    },
    9: {  # الخفيف
        "name_ar": "الخفيف",
        "name_en": "al-Khafif",
        "patterns": [
            "///oo//o///o//////o//",
            "//o/o////o///o//o/o",
            "//o/o//o/o/o//o/o//o//o",
            "/o////oo/o//o/o////o///o",
            "/o/o//o/////o/o//o///o",
            "/o/o//o///o////o//////",
            "/o/o//o/o//o//o///o",
            "/o/o//o/o/o///o///o//o",
        ],
    },
}


class BahrDetectorV2Hybrid:
    """
    Hybrid detector combining empirical patterns with fuzzy matching.

    Strategy:
    1. Exact match against empirical patterns (confidence: 0.95-0.98)
    2. Fuzzy match against empirical patterns (threshold: 70%, confidence: 0.70-0.90)
    3. Theoretical fallback if needed (threshold: 85%, confidence: 0.60-0.80)
    """

    def __init__(self):
        """Initialize hybrid detector."""
        self.empirical_patterns = EMPIRICAL_PATTERNS
        self.meters = METERS_REGISTRY

        # Build reverse lookup: pattern -> list of meter IDs
        self.pattern_to_meters: Dict[str, List[int]] = defaultdict(list)
        for meter_id, data in self.empirical_patterns.items():
            for pattern in data["patterns"]:
                self.pattern_to_meters[pattern].append(meter_id)

        # Generate theoretical patterns for meters without empirical data
        self.theoretical_patterns: Dict[int, Set[str]] = {}
        self.theoretical_generators: Dict[int, PatternGenerator] = {}

        for meter_id, meter in self.meters.items():
            # Only generate theoretical for meters without empirical patterns
            if meter_id not in self.empirical_patterns:
                generator = PatternGenerator(meter)
                self.theoretical_generators[meter_id] = generator
                # Generate both full-verse and hemistich patterns
                self.theoretical_patterns[meter_id] = generator.generate_all_patterns('auto')

    def detect(
        self,
        phonetic_pattern: str,
        top_k: int = 3,
        expected_meter_ar: Optional[str] = None,
    ) -> List[DetectionResult]:
        """
        Detect meter(s) for a phonetic pattern.

        Args:
            phonetic_pattern: Input phonetic pattern
            top_k: Return top K matches
            expected_meter_ar: Optional expected meter for tie-breaking

        Returns:
            List of DetectionResult objects, sorted by confidence
        """
        candidates = []

        # Step 1: Check for exact matches in empirical patterns
        if phonetic_pattern in self.pattern_to_meters:
            for meter_id in self.pattern_to_meters[phonetic_pattern]:
                meter_data = self.empirical_patterns[meter_id]

                # High confidence for exact empirical matches
                confidence = 0.98

                # Slight boost if matches expected meter
                if expected_meter_ar and meter_data["name_ar"] == expected_meter_ar:
                    confidence = 0.99

                candidates.append(DetectionResult(
                    meter_id=meter_id,
                    meter_name_ar=meter_data["name_ar"],
                    meter_name_en=meter_data["name_en"],
                    confidence=confidence,
                    matched_pattern=phonetic_pattern,
                    input_pattern=phonetic_pattern,
                    similarity=1.0,
                    match_type="exact_empirical",
                    explanation=f"مطابقة تامة | Exact match with {meter_data['name_en']}",
                ))

        # Step 2: Fuzzy match against empirical patterns
        for meter_id, data in self.empirical_patterns.items():
            best_similarity = 0.0
            best_pattern = None

            for pattern in data["patterns"]:
                similarity = PatternSimilarity.calculate_similarity(
                    phonetic_pattern, pattern
                )

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_pattern = pattern

            # Threshold: 70% for fuzzy empirical matches
            if best_similarity >= 0.70:
                # Check if we already have exact match for this meter
                has_exact = any(
                    c.meter_id == meter_id and c.match_type == "exact_empirical"
                    for c in candidates
                )

                if not has_exact:
                    # Confidence based on similarity
                    confidence = 0.65 + (best_similarity * 0.25)  # 0.65-0.90 range

                    # Boost if matches expected meter
                    if expected_meter_ar and data["name_ar"] == expected_meter_ar:
                        confidence = min(0.95, confidence * 1.05)

                    candidates.append(DetectionResult(
                        meter_id=meter_id,
                        meter_name_ar=data["name_ar"],
                        meter_name_en=data["name_en"],
                        confidence=confidence,
                        matched_pattern=best_pattern,
                        input_pattern=phonetic_pattern,
                        similarity=best_similarity,
                        match_type="fuzzy_empirical",
                        explanation=f"مطابقة تقريبية {best_similarity:.1%} | Approximate match {best_similarity:.1%} with {data['name_en']}",
                    ))

        # Step 3: Theoretical fallback for meters without empirical patterns
        # Always check theoretical patterns for meters lacking empirical data
        if True:  # Always run, confidence will sort correctly
            for meter_id, theoretical_set in self.theoretical_patterns.items():
                # Skip if already in candidates
                if any(c.meter_id == meter_id for c in candidates):
                    continue

                meter = self.meters[meter_id]

                # Check for exact match in theoretical patterns
                if phonetic_pattern in theoretical_set:
                    confidence = 0.88  # Lower than empirical

                    if expected_meter_ar and meter.name_ar == expected_meter_ar:
                        confidence = 0.92

                    candidates.append(DetectionResult(
                        meter_id=meter_id,
                        meter_name_ar=meter.name_ar,
                        meter_name_en=meter.name_en,
                        confidence=confidence,
                        matched_pattern=phonetic_pattern,
                        input_pattern=phonetic_pattern,
                        similarity=1.0,
                        match_type="exact_theoretical",
                        explanation=f"مطابقة نظرية تامة | Theoretical exact match with {meter.name_en}",
                    ))
                else:
                    # Fuzzy match against theoretical patterns (stricter threshold)
                    best_similarity = 0.0
                    best_pattern = None

                    for pattern in theoretical_set:
                        similarity = PatternSimilarity.calculate_similarity(
                            phonetic_pattern, pattern
                        )
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_pattern = pattern

                    # Threshold: 85% for theoretical (stricter than empirical)
                    if best_similarity >= 0.85:
                        confidence = 0.55 + (best_similarity * 0.20)  # 0.55-0.75 range

                        if expected_meter_ar and meter.name_ar == expected_meter_ar:
                            confidence = min(0.85, confidence * 1.10)

                        candidates.append(DetectionResult(
                            meter_id=meter_id,
                            meter_name_ar=meter.name_ar,
                            meter_name_en=meter.name_en,
                            confidence=confidence,
                            matched_pattern=best_pattern,
                            input_pattern=phonetic_pattern,
                            similarity=best_similarity,
                            match_type="fuzzy_theoretical",
                            explanation=f"مطابقة نظرية تقريبية {best_similarity:.1%} | Theoretical approximate match {best_similarity:.1%} with {meter.name_en}",
                        ))

        # Sort by confidence (descending)
        candidates.sort(key=lambda x: -x.confidence)

        return candidates[:top_k]

    def detect_best(self, phonetic_pattern: str) -> Optional[DetectionResult]:
        """Detect single best meter match."""
        results = self.detect(phonetic_pattern, top_k=1)
        return results[0] if results else None


def detect_meter_hybrid(phonetic_pattern: str) -> Optional[DetectionResult]:
    """Convenience function for single meter detection."""
    detector = BahrDetectorV2Hybrid()
    return detector.detect_best(phonetic_pattern)
