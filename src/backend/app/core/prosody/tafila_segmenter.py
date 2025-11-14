"""
Tafila-Aware Segmentation for Arabic Meter Detection

This module implements Option B: a prosodic segmenter that identifies
tafail patterns in Arabic text and determines the meter through
probabilistic matching.

Key innovation: Works FORWARD from text → tafail → meter
Instead of: text → pattern → cache match → meter
"""

import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Handle imports for both module use and standalone testing
try:
    from ..phonetics import Phoneme, extract_phonemes
    from .meters import METERS_REGISTRY, Meter, get_meter_by_name
    from .tafila import Tafila, get_tafila
except ImportError:
    # Standalone mode
    sys.path.insert(0, "/home/user/BAHR/backend")
    from app.core.phonetics import Phoneme, extract_phonemes
    from app.core.prosody.meters import METERS_REGISTRY, Meter, get_meter_by_name
    from app.core.prosody.tafila import Tafila, get_tafila


@dataclass
class TafilaMatch:
    """Represents a matched tafila in text."""

    tafila: Tafila
    phonemes: List[Phoneme]
    start_idx: int
    end_idx: int
    confidence: float
    variations_applied: List[str]  # e.g., ['خبن', 'base']

    def __repr__(self):
        return f"TafilaMatch({self.tafila.name}, conf={self.confidence:.2f})"


@dataclass
class MeterMatch:
    """Represents a complete meter match for a verse."""

    meter: Meter
    tafail_sequence: List[TafilaMatch]
    overall_confidence: float
    match_quality: str  # 'exact', 'strong', 'moderate', 'weak'

    def __repr__(self):
        return f"MeterMatch({self.meter.name_ar}, conf={self.overall_confidence:.2f})"


class TafilaSegmenter:
    """
    Segments Arabic verse text into tafail and identifies the meter.

    This approach matches how classical Arabic prosody actually works:
    1. Extract phonemes from text
    2. Try to segment into known tafail patterns
    3. Check which meter's tafail sequence matches
    4. Return best meter match with confidence
    """

    def __init__(self):
        """Initialize segmenter with meter definitions."""
        self.meters = METERS_REGISTRY

        # Build tafila library with variations
        self.tafila_library = self._build_tafila_library()

    def _build_tafila_library(self) -> Dict[str, List[Tuple[Tafila, str]]]:
        """
        Build library of all tafail with their variations.

        Returns:
            Dict mapping phonetic pattern → [(tafila, variation_name)]
        """
        library = defaultdict(list)

        # For each meter, get all tafail with variations
        for meter_id, meter in self.meters.items():
            for position in range(1, meter.tafail_count + 1):
                base_tafila = meter.get_tafila_at_position(position)

                # Add base form
                library[base_tafila.phonetic].append((base_tafila, "base"))

                # Add variations from zihafat
                allowed_zihafat = meter.get_allowed_zihafat(position)
                for zahaf in allowed_zihafat:
                    try:
                        modified = zahaf.apply(base_tafila)
                        library[modified.phonetic].append((modified, zahaf.name))
                    except:
                        pass

                # Add ilal for final positions
                if meter.is_final_position(position):
                    allowed_ilal = meter.get_allowed_ilal(position)
                    for ilah in allowed_ilal:
                        try:
                            modified = ilah.apply(base_tafila)
                            library[modified.phonetic].append((modified, ilah.name))
                        except:
                            pass

        return library

    def phonemes_to_pattern_segment(
        self, phonemes: List[Phoneme], start: int, length: int
    ) -> str:
        """
        Convert a segment of phonemes to prosodic pattern.

        Uses letter-based notation:
        - Short vowel → '/'
        - Sukun → 'o'
        - Long vowel → '/o'
        """
        pattern = ""
        for i in range(start, min(start + length, len(phonemes))):
            phoneme = phonemes[i]

            if phoneme.has_shadda:
                pattern += "o"  # First (sakin)

            if phoneme.is_long_vowel():
                pattern += "/o"
            elif phoneme.is_sukun():
                pattern += "o"
            elif phoneme.vowel in ["a", "u", "i"]:
                pattern += "/"
            elif phoneme.vowel in ["an", "un", "in"]:
                pattern += "/o"

        return pattern

    def find_tafila_matches(
        self, phonemes: List[Phoneme], start_idx: int
    ) -> List[TafilaMatch]:
        """
        Find all possible tafail starting at the given phoneme index.

        Args:
            phonemes: Full phoneme list
            start_idx: Starting position

        Returns:
            List of possible TafilaMatch objects
        """
        matches = []

        # Try different lengths (tafail are typically 3-6 phonemes)
        for length in range(3, 8):
            if start_idx + length > len(phonemes):
                break

            # Convert this segment to pattern
            segment_pattern = self.phonemes_to_pattern_segment(
                phonemes, start_idx, length
            )

            # Check if this pattern matches any known tafila
            if segment_pattern in self.tafila_library:
                for tafila, variation in self.tafila_library[segment_pattern]:
                    # Calculate confidence based on variation
                    if variation == "base":
                        confidence = 1.0
                    elif "common" in variation.lower():
                        confidence = 0.95
                    else:
                        confidence = 0.85

                    matches.append(
                        TafilaMatch(
                            tafila=tafila,
                            phonemes=phonemes[start_idx : start_idx + length],
                            start_idx=start_idx,
                            end_idx=start_idx + length,
                            confidence=confidence,
                            variations_applied=[variation],
                        )
                    )

        return matches

    def segment_verse(self, phonemes: List[Phoneme]) -> List[List[TafilaMatch]]:
        """
        Segment verse into possible tafila sequences.

        Uses dynamic programming to find all valid segmentations.

        Args:
            phonemes: Verse phonemes

        Returns:
            List of possible tafila sequences (each sequence is a valid segmentation)
        """
        n = len(phonemes)

        # DP table: dp[i] = list of segmentations ending at position i
        dp = [[] for _ in range(n + 1)]
        dp[0] = [[]]  # Empty segmentation at start

        for i in range(n):
            if not dp[i]:
                continue

            # Find all tafail starting at position i
            tafila_matches = self.find_tafila_matches(phonemes, i)

            for match in tafila_matches:
                # For each segmentation ending at i, extend it
                for segmentation in dp[i]:
                    new_segmentation = segmentation + [match]
                    dp[match.end_idx].append(new_segmentation)

        # Return all complete segmentations
        return dp[n]

    def match_meter(
        self, tafila_sequence: List[TafilaMatch], meter: Meter
    ) -> Optional[float]:
        """
        Check if a tafila sequence matches a meter's structure.

        Args:
            tafila_sequence: Sequence of matched tafail
            meter: Meter to check against

        Returns:
            Confidence score if match, None otherwise
        """
        # Check if length matches
        if len(tafila_sequence) != meter.tafail_count:
            return None

        # Check if each tafila matches the expected base tafila
        confidence_scores = []
        for i, matched_tafila in enumerate(tafila_sequence):
            expected_tafila = meter.get_tafila_at_position(i + 1)

            # Check if base tafila matches
            if matched_tafila.tafila.name == expected_tafila.name:
                confidence_scores.append(matched_tafila.confidence)
            else:
                # Check if it's a valid variation
                # (This would need more sophisticated logic in full implementation)
                return None

        # Calculate overall confidence
        if confidence_scores:
            return sum(confidence_scores) / len(confidence_scores)
        return None

    def detect_meter(
        self, text: str, has_tashkeel: bool = True
    ) -> Optional[MeterMatch]:
        """
        Detect meter from Arabic text using tafila segmentation.

        Args:
            text: Arabic verse text (preferably with diacritics)
            has_tashkeel: Whether text has diacritical marks

        Returns:
            Best MeterMatch or None if no match found

        Example:
            >>> segmenter = TafilaSegmenter()
            >>> match = segmenter.detect_meter("قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ")
            >>> print(match.meter.name_ar)
            الطويل
        """
        # Extract phonemes
        phonemes = extract_phonemes(text, has_tashkeel=has_tashkeel)

        if not phonemes:
            return None

        # Segment into possible tafila sequences
        all_segmentations = self.segment_verse(phonemes)

        if not all_segmentations:
            return None

        # For each segmentation, check which meter it matches
        best_match = None
        best_confidence = 0.0

        for segmentation in all_segmentations:
            # Try each meter
            for meter_id, meter in self.meters.items():
                confidence = self.match_meter(segmentation, meter)

                if confidence and confidence > best_confidence:
                    best_confidence = confidence
                    best_match = MeterMatch(
                        meter=meter,
                        tafail_sequence=segmentation,
                        overall_confidence=confidence,
                        match_quality=self._assess_quality(confidence),
                    )

        return best_match

    def _assess_quality(self, confidence: float) -> str:
        """Assess match quality from confidence score."""
        if confidence >= 0.95:
            return "exact"
        elif confidence >= 0.85:
            return "strong"
        elif confidence >= 0.75:
            return "moderate"
        else:
            return "weak"


def detect_meter_v3(text: str, has_tashkeel: Optional[bool] = None) -> Optional[Dict]:
    """
    Convenience function for meter detection using tafila segmentation.

    This is the Option B implementation - tafila-aware meter detection.

    Args:
        text: Arabic verse text
        has_tashkeel: Whether text has diacritics (auto-detects if None)

    Returns:
        Detection result dict or None

    Example:
        >>> result = detect_meter_v3("قِفا نَبْكِ مِن ذِكرى")
        >>> print(result['meter_name_ar'])
        الطويل
    """
    try:
        from ..normalization import has_diacritics
    except ImportError:
        from app.core.normalization import has_diacritics

    if has_tashkeel is None:
        has_tashkeel = has_diacritics(text)

    segmenter = TafilaSegmenter()
    match = segmenter.detect_meter(text, has_tashkeel)

    if not match:
        return None

    return {
        "meter_id": match.meter.id,
        "meter_name_ar": match.meter.name_ar,
        "meter_name_en": match.meter.name_en,
        "confidence": match.overall_confidence,
        "match_quality": match.match_quality,
        "tafail_count": len(match.tafail_sequence),
        "tafail_names": [t.tafila.name for t in match.tafail_sequence],
        "method": "tafila_segmentation",
    }


if __name__ == "__main__":
    # Demo
    import sys

    sys.path.insert(0, "/home/user/BAHR/backend")

    print("=" * 80)
    print("TAFILA SEGMENTATION DEMO (Option B)")
    print("=" * 80)
    print()

    segmenter = TafilaSegmenter()

    print(
        f"Tafila library size: {sum(len(v) for v in segmenter.tafila_library.values())} patterns"
    )
    print()

    # Test verses
    test_verses = [
        ("قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ", "الطويل"),
        ("يا لَيلَةَ الصَّبِّ مَتى غَدُكِ", "الرمل"),
    ]

    for text, expected in test_verses:
        print(f"Verse: {text}")
        print(f"Expected: {expected}")

        match = segmenter.detect_meter(text, has_tashkeel=True)

        if match:
            print(f"✅ Detected: {match.meter.name_ar}")
            print(f"   Confidence: {match.overall_confidence:.2%}")
            print(f"   Quality: {match.match_quality}")
            print(
                f"   Tafail: {' + '.join(t.tafila.name for t in match.tafail_sequence)}"
            )
            print(f"   Match: {'✅' if match.meter.name_ar == expected else '❌'}")
        else:
            print(f"❌ No detection")

        print()
