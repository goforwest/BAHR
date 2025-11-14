"""Prosody engine MVP: pattern building and naive meter detection.

IMPLEMENTATION SCOPE (Week 1-2 MVP):
This is a lightweight, rule-based placeholder for basic testing and development.
The full fuzzy matching algorithm with Levenshtein distance and confidence
calibration will be implemented in Week 3-5.

Current implementation:
- Simple character-by-character pattern matching
- Basic similarity scoring
- Minimal meter templates

TODO (Week 3-5): Implement full meter detection algorithm
- Levenshtein distance calculation
- Fuzzy matching with ±10% threshold
- Tafaeel decomposition
- Zihafat (prosodic variations) handling
- Confidence calibration (raw → calibrated)
- Quality assessment
- See: docs/implementation-guides/feature-meter-detection.md

"""

from dataclasses import dataclass
from typing import Dict, List

from .segmenter import Syllable


@dataclass
class ProsodyPattern:
    """
    Prosodic pattern representation.

    TODO (Week 3): Extend with:
    - tafail: List[Tafila]
    - confidence_factors: Dict[str, float]
    - quality_breakdown: Dict[str, float]
    """

    taqti3: str
    pattern: str  # '-' for long, 'u' for short
    syllable_count: int
    stress_pattern: str | None = None


def build_pattern(syllables: List[Syllable]) -> ProsodyPattern:
    """
    Build prosodic pattern from syllables.

    Args:
        syllables: List of syllable objects

    Returns:
        ProsodyPattern object

    TODO (Week 3): Enhance with:
    - Syllable weight calculation
    - Stress pattern detection
    - Tafaeel boundary detection
    """
    # Map long to '-' and short to 'u'
    patt = "".join("-" if s.long else "u" for s in syllables)

    # naive grouping with vertical bars every 4 units
    grouped = " | ".join([patt[i : i + 4] for i in range(0, len(patt), 4)])

    # a placeholder taqti3 string mirroring grouping
    taqti3 = grouped.replace("-", "ـ").replace("u", "◌")

    return ProsodyPattern(taqti3=taqti3, pattern=patt, syllable_count=len(syllables))


# Minimal meter templates by rough pattern length and signature
# TODO (Week 3): Expand to full 16 meters with all zihafat variations
METER_SIGNATURES: Dict[str, List[str]] = {
    "الطويل": ["-u--u---", "-u--u--"],
    "الكامل": ["-u-u- -u-u- -u-u-".replace(" ", "")],
    "الرجز": ["--u--u--u"],
    "الرمل": ["-u-u- -u-u- -u-u-".replace(" ", "")],
    "المتقارب": ["- - - - - - - -".replace(" ", "")],
    # TODO: Add remaining 11 meters
}


def detect_meter(pattern: str) -> tuple[str | None, float, list[dict]]:
    """
    Detect meter from prosodic pattern (naive implementation).

    Args:
        pattern: Syllable pattern string ('-' and 'u')

    Returns:
        (best_meter_name, confidence, alternatives)

    CURRENT LIMITATIONS:
    - Simple character matching (not Levenshtein distance)
    - No zihafat handling
    - No confidence calibration
    - Only 5 meters supported

    TODO (Week 3-5): Replace with full implementation
    - Use Levenshtein distance for fuzzy matching
    - Handle all 16 classical meters
    - Support zihafat variations
    - Implement confidence calibration
    - Add tafaeel decomposition
    - See: docs/implementation-guides/feature-meter-detection.md
    """
    best_name = None
    best_score = 0.0
    alts: list[tuple[str, float]] = []

    for name, sigs in METER_SIGNATURES.items():
        score = max(similarity(pattern, s) for s in sigs)
        alts.append((name, score))
        if score > best_score:
            best_score, best_name = score, name

    # Sort alternatives by score
    alts.sort(key=lambda x: x[1], reverse=True)

    # Format alternatives (skip best, return top 3)
    alternatives = [
        {"name": n, "confidence": round(s, 2), "reason": None} for n, s in alts[1:4]
    ]

    return best_name, round(best_score, 2), alternatives


def similarity(a: str, b: str) -> float:
    """
    Calculate simple similarity between two patterns.

    CURRENT: Character-by-character matching
    TODO (Week 3): Replace with Levenshtein distance

    Args:
        a: First pattern string
        b: Second pattern string

    Returns:
        Similarity score (0.0 - 1.0)
    """
    if not a or not b:
        return 0.0

    L = min(len(a), len(b))
    matches = sum(1 for i in range(L) if a[i] == b[i])
    return matches / max(len(a), len(b))


# TODO (Week 4): Add functions for:
# - calculate_edit_distance(pattern1, pattern2) -> int
# - decompose_tafail(pattern) -> List[Tafila]
# - detect_zihafat(pattern, meter) -> List[str]
# - calibrate_confidence(raw_score, factors) -> float
# - assess_quality(analysis_result) -> QualityScore
