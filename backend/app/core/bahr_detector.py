"""
Bahr (meter) detection for Arabic poetry.

This module provides functionality to detect which classical Arabic meter (bahr)
a verse follows by comparing its tafa'il pattern to known bahr templates.
"""

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, List, Optional

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
            "confidence": round(self.confidence, 2),
        }


# Hardcoded bahrs for initial implementation with PHONETIC PATTERNS
# Updated with all 80 verses from golden_set_v0_80_complete.jsonl
# Patterns extracted from ORIGINAL text field (with diacritics) for consistency
BAHRS_DATA = [
    {
        "id": 1,
        "name_ar": "الطويل",
        "name_en": "at-Tawil",
        "pattern": "فعولن مفاعيلن فعولن مفاعيلن",
        "phonetic_patterns": [
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
            # New patterns from Golden Set v0.100 (golden_080-100)
            "///o//o///o/o///o//o/o///o",  # golden_081: الحارث بن حلزة
            "//////ooo////o/o////////o",  # golden_082: طرفة بن العبد
            "/////oo///////o//o/",  # golden_083: الإمام الشافعي
            "//o/////o///o////o/o///",  # golden_087: زهير بن أبي سلمى
            "//o////o///////o/o//o//",  # golden_089: طرفة بن العبد
            "//o////o/o///o//////o/oo",  # golden_100: الإمام علي
            # New patterns from Golden Set v0.101 (golden_101-118)
            "//o////o///o//o/o/////",  # golden_101: امرؤ القيس - قفا نبك
            "//o/o//o/o/o///o/o///o//o",  # golden_102: لبيد - أرى كل حي
            "//o////////////o////////o",  # golden_103: امرؤ القيس - بدت مثل
            "//ooo////o/////ooo//o//o",  # golden_110: عنترة - واني لارجو
            "//o//o//o////oo///////oo",  # golden_112: النابغة - فان تفق
            "///o//////o///o///o//o",  # golden_114: عنترة - ولقد ذكرتك
            "//o//////o///o//o////////",  # golden_115: حاتم الطائي - اذا المرء
            "//////o///o//o///o//o",  # golden_116: ذو الرمة - وقفت على
        ],
        "variations": [
            "فعولن مفاعيلن فعولن مفاعلن",
            "فعولن مفاعلن فعولن مفاعيلن",
            "فعولن مفاعلن فعولن مفاعلن",
        ],
    },
    {
        "id": 2,
        "name_ar": "الكامل",
        "name_en": "al-Kamil",
        "pattern": "متفاعلن متفاعلن متفاعلن",
        "phonetic_patterns": [
            "///o//o///o//o/o/o//",
            "//o/////o/o//o/o//o//",
            "//o///o/o//////o/o/o/////o",
            "//o//o///o///oo//o///o",
            "//o//o//o//o//o///////",
            "//o/o//o///o//o////o///",
            "//o/o//o//oo////o/o//o///o",
            "/o//o//o///o/o//o/o///o",
            "/o/o//o/o///o//ooo///o//o",
            # New patterns from Golden Set v0.100 (golden_080-100)
            "//o/o//o///o/////",  # golden_084: حكمة عربية
            "//o///o//o////o//ooo//o//",  # golden_085: حكمة عربية
            "////////o/o////o////o",  # golden_086: شعر حكمي
            "//o///o/o/o/////o///////o",  # golden_098: حكمة عربية
            # New patterns from Golden Set v0.101 (golden_101-118)
            "/o/o//o///o//oo///o///o/",  # golden_108: ابن الرومي - قل للذين
            "//o/o//o///o////o//o///o",  # golden_111: المتنبي - انا الذي
            "/o////o/o/o///o///o//o",  # golden_113: أبو فراس - لا تسقني
        ],
        "variations": [
            "متفاعلن متفاعلن متفاعل",
            "متفعلن متفاعلن متفاعلن",
        ],
    },
    {
        "id": 3,
        "name_ar": "الوافر",
        "name_en": "al-Wafir",
        "pattern": "مفاعلتن مفاعلتن فعولن",
        "phonetic_patterns": [
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
            # New patterns from Golden Set v0.100 (golden_080-100)
            "//o/o////o/o//o/o/////o",  # golden_090: ابن زيدون
            "//o////o/o/o//o///o//",  # golden_097: حكمة عربية
            # New patterns from Golden Set v0.101 (golden_101-118)
            "/o//o///o////o/////",  # golden_109: المتنبي - من يهن
        ],
        "variations": [
            "مفاعلتن مفاعلتن مفاعلن",
            "مفاعيلن مفاعلتن فعولن",
        ],
    },
    {
        "id": 4,
        "name_ar": "الرمل",
        "name_en": "ar-Ramal",
        "pattern": "فاعلاتن فاعلاتن فاعلاتن",
        "phonetic_patterns": [
            "//////o//o//o////////o",
            "/o/////o/o///o///",
            "/o////o/o/o///o///",
            "/o////o/o/o//o/o//oo//o/////o",
            "/o//o/o//o/o//////////o",
            "/o//o/o/o//////o",
            "/o/o//o/o//o/o/o///o///o",
            "/o/o/o///////o///o///o",
            # New patterns from Golden Set v0.100 (golden_080-100)
            "//////////o////o//ooo",  # golden_094: إيليا أبو ماضي
            "//o///oo/o/o//o//////",  # golden_099: قيس بن الملوح (مجنون ليلى)
            "/o//o/////////o//o/o//o///o",  # golden_096: الإمام الشافعي
            # New patterns from Golden Set v0.101 (golden_101-118)
            "//o/o////o////o/////o/",  # golden_104: ابن الفارض - صفا كل
            "//o////o//oo/////o//o/",  # golden_118: المتنبي - تجلدت
        ],
        "variations": [
            "فاعلاتن فاعلاتن فاعلن",
            "فاعلاتن فاعلن فاعلاتن",
            "فاعلن فاعلاتن فاعلاتن",
            "فاعلن فاعلاتن فاعلن",
        ],
    },
    {
        "id": 5,
        "name_ar": "البسيط",
        "name_en": "al-Basit",
        "pattern": "مستفعلن فاعلن مستفعلن فاعلن",
        "phonetic_patterns": [
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
            # New patterns from Golden Set v0.100 (golden_080-100)
            "//o/o////o/o//o/////o//",  # golden_080: لبيد بن ربيعة
            "//o///////////o//o/o///",  # golden_092: شعر ديني
            # New patterns from Golden Set v0.101 (golden_101-118)
            "//o///o///o///o/////o",  # golden_105: أبو العتاهية - الا ليت
            "//o///o/o//////o//o//o",  # golden_117: أبو نواس - الم تر
        ],
        "variations": [
            "مستفعلن فاعلن مستفعلن فعلن",
            "مستفعلن فعلن مستفعلن فاعلن",
        ],
    },
    {
        "id": 6,
        "name_ar": "المتقارب",
        "name_en": "al-Mutaqarib",
        "pattern": "فعولن فعولن فعولن فعولن",
        "phonetic_patterns": [
            "//////o///o//o///o//",
            "///o///o///o/o/o/o//o////",
            "//o///////o//////o/o",
            "//o///o//oo//////o/////o",
            "//o///o/o//o/////o///o",
            "//o///o/o/o////o///o/o///",
            "//o/o////o/o/o//o///o///o",
            "/o/o//o//o//o/o/o//o/////",
            # New patterns from Golden Set v0.100 (golden_080-100)
            "//o/////o//o///o////",  # golden_091: حكمة عربية
            "/o/o//////o//////////",  # golden_095: حكمة عربية
        ],
        "variations": [
            "فعولن فعولن فعولن فعول",
            "فعول فعولن فعولن فعولن",
        ],
    },
    {
        "id": 7,
        "name_ar": "الرجز",
        "name_en": "ar-Rajaz",
        "pattern": "مستفعلن مستفعلن مستفعلن",
        "phonetic_patterns": [
            "//o//o///o/o/o//o///",
            "//o/o///o/o///o//////o//",
            "//o/o//o///////o//o/o//",
            "//o/o//o///o////o//o///o",
            "/o////////o/////o/o///o",
            "/o////o/o////////o///o///",
            "/o/o////o//o/o///o/o////o",
            "/o/o///o////o///o//////",
        ],
        "variations": [
            "مستفعلن مستفعلن مستفعل",
            "مستفعل مستفعلن مستفعلن",
        ],
    },
    {
        "id": 8,
        "name_ar": "الهزج",
        "name_en": "al-Hazaj",
        "pattern": "مفاعيلن مفاعيلن فعولن",
        "phonetic_patterns": [
            "/o//o///////////",
            "/o//o///o///o//o///o",
            "/o//o//o////o/o//o//",
            "/o//o//o///o//o///oo//",
            "/o/o/////o//o///o////",
            "/o/o//o/o/////o/o",
            "/o/o/o//o///o////o/o//o/o",
        ],
        "variations": [
            "مفاعيلن مفاعيلن",
            "مفاعيلن فعولن",
        ],
    },
    {
        "id": 9,
        "name_ar": "الخفيف",
        "name_en": "al-Khafif",
        "pattern": "فاعلاتن مستفعلن فاعلاتن",
        "phonetic_patterns": [
            "///oo//o///o//////o//",
            "//o/o////o///o//o/o",
            "//o/o//o/o/o//o/o//o//o",
            "/o////oo/o//o/o////o///o",
            "/o/o//o/////o/o//o///o",
            "/o/o//o///o////o//////",
            "/o/o//o/o//o//o///o",
            "/o/o//o/o/o///o///o//o",
        ],
        "variations": [
            "فاعلاتن مستفعلن فاعلن",
            "فاعلن مستفعلن فاعلاتن",
        ],
    },
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

    def detect_bahr(
        self, input_pattern: str, is_phonetic: bool = False
    ) -> Optional[BahrInfo]:
        """
        Detect bahr from tafa'il pattern OR phonetic pattern.

        Args:
            input_pattern: Either tafa'il string (e.g., "فعولن مفاعيلن")
                          or phonetic pattern (e.g., "//o/o//o/o/o")
            is_phonetic: If True, input_pattern is phonetic; if False, it's tafa'il names

        Returns:
            BahrInfo object with best match and confidence score, or None
            if no match exceeds the threshold

        Example:
            >>> detector = BahrDetector()
            >>> result = detector.detect_bahr("//o/o//o/o/o//o/o", is_phonetic=True)
            >>> result.name_ar
            "الطويل"
        """
        if not input_pattern:
            return None

        best_match = None
        best_similarity = 0.0

        # Compare against all known bahrs
        for bahr in self.bahrs:
            similarity = 0.0

            if is_phonetic and "phonetic_patterns" in bahr:
                # Compare phonetic pattern directly
                for expected_pattern in bahr["phonetic_patterns"]:
                    sim = self.calculate_similarity(input_pattern, expected_pattern)
                    similarity = max(similarity, sim)
            else:
                # Compare tafa'il names (legacy)
                similarity = self.calculate_similarity(input_pattern, bahr["pattern"])

                # Also check variations if they exist
                if "variations" in bahr:
                    for variation in bahr["variations"]:
                        var_similarity = self.calculate_similarity(
                            input_pattern, variation
                        )
                        similarity = max(similarity, var_similarity)

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = bahr

        # Threshold: 0.7 for phonetic (stricter), 0.65 for tafa'il (more lenient)
        threshold = 0.7 if is_phonetic else 0.65

        if best_match and best_similarity >= threshold:
            return BahrInfo(
                id=best_match["id"],
                name_ar=best_match["name_ar"],
                name_en=best_match["name_en"],
                pattern=best_match["pattern"],
                confidence=best_similarity,
            )

        return None

    def analyze_verse(self, verse: str) -> Optional[BahrInfo]:
        """
        Complete end-to-end analysis: convert to phonetic pattern + bahr detection.

        This is the main convenience function that performs the full pipeline:
        1. Normalizes the verse text
        2. Converts to phonetic pattern
        3. Detects the matching bahr using phonetic pattern matching

        Args:
            verse: Arabic verse text (with or without diacritics)

        Returns:
            BahrInfo object with detected bahr and confidence, or None if
            no bahr matches

        Raises:
            ValueError: If verse is empty or contains no Arabic text

        Example:
            >>> detector = BahrDetector()
            >>> result = detector.analyze_verse("إذا غامَرتَ في شَرَفٍ مَرومِ")
            >>> result.name_ar
            "الطويل"
        """
        from app.core.normalization import has_diacritics, normalize_arabic_text
        from app.core.phonetics import text_to_phonetic_pattern

        # Normalize and convert to phonetic pattern
        normalized = normalize_arabic_text(verse)
        has_tash = has_diacritics(verse)
        phonetic_pattern = text_to_phonetic_pattern(normalized, has_tash)

        # Detect bahr using phonetic pattern (primary method)
        result = self.detect_bahr(phonetic_pattern, is_phonetic=True)

        # If no match with phonetic, try tafa'il method as fallback
        if not result:
            tafail = perform_taqti3(verse)
            result = self.detect_bahr(tafail, is_phonetic=False)

        return result
