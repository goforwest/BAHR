"""
Bahr (meter) detection for Arabic poetry.

This module provides functionality to detect which classical Arabic meter (bahr)
a verse follows by comparing its tafa'il pattern to known bahr templates.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from difflib import SequenceMatcher
from app.core.taqti3 import perform_taqti3


@dataclass
class BahrInfo:
    """
    Information about a detected bahr (meter).

    Attributes:
        id: Unique identifier for the bahr
        name_ar: Arabic name of the bahr (e.g., "الطويل")
        name_en: English transliteration (e.g., "at-Tawil")
        pattern: Tafa'il pattern string (e.g., "فعولن مفاعيلن فعولن مفاعيلن")
        confidence: Similarity score between 0.0 and 1.0

    Example:
        >>> bahr = BahrInfo(1, "الطويل", "at-Tawil", "فعولن مفاعيلن فعولن مفاعيلن", 0.95)
        >>> bahr.to_dict()
        {'id': 1, 'name_ar': 'الطويل', 'name_en': 'at-Tawil', ...}
    """
    id: int
    name_ar: str
    name_en: str
    pattern: str
    confidence: float  # 0.0 to 1.0

    def to_dict(self) -> Dict:
        """
        Convert BahrInfo to dictionary.

        Returns:
            Dictionary representation with rounded confidence

        Example:
            >>> bahr.to_dict()
            {'id': 1, 'name_ar': 'الطويل', 'name_en': 'at-Tawil',
             'pattern': 'فعولن مفاعيلن فعولن مفاعيلن', 'confidence': 0.95}
        """
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "pattern": self.pattern,
            "confidence": round(self.confidence, 2)
        }


# Hardcoded bahrs for initial implementation (TODO: load from database)
BAHRS_DATA = [
    {
        "id": 1,
        "name_ar": "الطويل",
        "name_en": "at-Tawil",
        "pattern": "فعولن مفاعيلن فعولن مفاعيلن"
    },
    {
        "id": 2,
        "name_ar": "الكامل",
        "name_en": "al-Kamil",
        "pattern": "متفاعلن متفاعلن متفاعلن"
    },
    {
        "id": 3,
        "name_ar": "الوافر",
        "name_en": "al-Wafir",
        "pattern": "مفاعلتن مفاعلتن فعولن"
    },
    {
        "id": 4,
        "name_ar": "الرمل",
        "name_en": "ar-Ramal",
        "pattern": "فاعلاتن فاعلاتن فاعلاتن"
    },
    # TODO: Add remaining 12 bahrs when expanding the system
]


class BahrDetector:
    """
    Detects bahr (meter) from verse tafa'il pattern.

    This class compares analyzed verse patterns against known classical Arabic
    meters using fuzzy matching to account for minor variations (zihafat).

    Example:
        >>> detector = BahrDetector()
        >>> result = detector.analyze_verse("إذا غامَرتَ في شَرَفٍ مَرومِ")
        >>> result.name_ar
        "الطويل"
        >>> result.confidence
        0.95
    """

    def __init__(self):
        """
        Initialize the detector with bahr data.

        Loads the hardcoded BAHRS_DATA list containing the 4 primary bahrs.
        In future versions, this will load from the database.
        """
        self.bahrs = BAHRS_DATA

    def calculate_similarity(self, tafail1: str, tafail2: str) -> float:
        """
        Calculate similarity between two tafa'il patterns.

        Uses Python's difflib.SequenceMatcher for fuzzy string matching,
        which allows for minor variations (zihafat) in the prosodic pattern.

        Args:
            tafail1: First tafa'il pattern string
            tafail2: Second tafa'il pattern string

        Returns:
            Similarity score between 0.0 (completely different) and 1.0 (identical)

        Example:
            >>> detector = BahrDetector()
            >>> detector.calculate_similarity(
            ...     "فعولن مفاعيلن فعولن مفاعيلن",
            ...     "فعولن مفاعيلن فعولن مفاعيلن"
            ... )
            1.0
            >>> detector.calculate_similarity(
            ...     "فعولن مفاعيلن فعولن",
            ...     "فعولن مفاعيلن فعولن مفاعيلن"
            ... )
            0.85  # Approximate
        """
        return SequenceMatcher(None, tafail1, tafail2).ratio()

    def detect_bahr(self, tafail_pattern: str) -> Optional[BahrInfo]:
        """
        Detect bahr from tafa'il pattern.

        Compares the input tafa'il pattern against all known bahr patterns
        and returns the best match if confidence is >= 0.7 (70% threshold).

        Args:
            tafail_pattern: Tafa'il string (e.g., "فعولن مفاعيلن فعولن مفاعيلن")

        Returns:
            BahrInfo object with best match and confidence score, or None
            if no match exceeds the 0.7 confidence threshold

        Example:
            >>> detector = BahrDetector()
            >>> result = detector.detect_bahr("فعولن مفاعيلن فعولن مفاعيلن")
            >>> result.name_ar
            "الطويل"
            >>> result.confidence >= 0.7
            True
            >>> detector.detect_bahr("")  # Empty pattern
            None
        """
        if not tafail_pattern:
            return None

        best_match = None
        best_similarity = 0.0

        # Compare against all known bahrs
        for bahr in self.bahrs:
            similarity = self.calculate_similarity(
                tafail_pattern,
                bahr["pattern"]
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = bahr

        # Only return if confidence meets minimum threshold
        if best_match and best_similarity >= 0.7:
            return BahrInfo(
                id=best_match["id"],
                name_ar=best_match["name_ar"],
                name_en=best_match["name_en"],
                pattern=best_match["pattern"],
                confidence=best_similarity
            )

        return None

    def analyze_verse(self, verse: str) -> Optional[BahrInfo]:
        """
        Complete end-to-end analysis: taqti3 + bahr detection.

        This is the main convenience function that performs the full pipeline:
        1. Normalizes the verse text
        2. Converts to phonetic pattern
        3. Extracts tafa'il pattern
        4. Detects the matching bahr

        Args:
            verse: Arabic verse text (with or without diacritics)

        Returns:
            BahrInfo object with detected bahr and confidence, or None if
            no bahr matches or if taqti3 fails

        Raises:
            ValueError: If verse is empty or contains no Arabic text
                (raised by underlying normalization/taqti3 functions)

        Example:
            >>> detector = BahrDetector()
            >>> result = detector.analyze_verse("إذا غامَرتَ في شَرَفٍ مَرومِ")
            >>> result.name_ar
            "الطويل"
            >>> result.name_en
            "at-Tawil"
            >>> result.confidence
            0.95
        """
        # Perform taqti3 (prosodic scansion)
        tafail = perform_taqti3(verse)

        # Detect bahr from the tafa'il pattern
        return self.detect_bahr(tafail)
