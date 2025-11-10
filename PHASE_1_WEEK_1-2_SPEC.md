# Phase 1, Week 1-2: Prosody Engine Core
## Detailed Implementation Specification for Codex

---

## Overview

**Duration:** 2 weeks
**Goal:** Build the core Arabic prosody analysis engine
**Deliverable:** Working taqti3 (تقطيع) analyzer that detects bahr (بحر) with 90%+ accuracy

---

## Task 1: Text Normalization Module

### File: `backend/app/core/normalization.py`

**Purpose:** Clean and standardize Arabic text for prosodic analysis

**Requirements:**
1. Remove optional diacritics (tashkeel)
2. Normalize hamza variants
3. Normalize alef variants
4. Remove tatweel (ـ)
5. Normalize tanween
6. Preserve or restore essential vowels based on mode

**Implementation:**

```python
"""
Arabic text normalization for prosodic analysis.
"""

import re
from typing import Optional
import unicodedata


# Unicode ranges for Arabic
ARABIC_DIACRITICS = [
    '\u064B',  # Tanween Fath
    '\u064C',  # Tanween Damm
    '\u064D',  # Tanween Kasr
    '\u064E',  # Fatha
    '\u064F',  # Damma
    '\u0650',  # Kasra
    '\u0651',  # Shadda
    '\u0652',  # Sukun
    '\u0653',  # Maddah
    '\u0654',  # Hamza above
    '\u0655',  # Hamza below
    '\u0656',  # Subscript Alef
    '\u0657',  # Inverted Damma
    '\u0658',  # Mark Noon Ghunna
]


def remove_diacritics(text: str) -> str:
    """
    Remove all Arabic diacritical marks (tashkeel).

    Args:
        text: Arabic text with diacritics

    Returns:
        Text without diacritics

    Example:
        >>> remove_diacritics("مَرْحَبًا")
        "مرحبا"
    """
    for diacritic in ARABIC_DIACRITICS:
        text = text.replace(diacritic, '')
    return text


def normalize_hamza(text: str) -> str:
    """
    Normalize all hamza variants to base form.

    Converts: أ، إ، آ، ء، ؤ، ئ → ا or ء

    Args:
        text: Arabic text with hamza variants

    Returns:
        Text with normalized hamza
    """
    # Hamza on alef variants → alef
    text = text.replace('أ', 'ا')
    text = text.replace('إ', 'ا')
    text = text.replace('آ', 'ا')

    # Hamza on waw → waw
    text = text.replace('ؤ', 'و')

    # Hamza on ya → ya
    text = text.replace('ئ', 'ي')

    return text


def normalize_alef(text: str) -> str:
    """
    Normalize alef variants.

    Converts: ى، أ، إ، آ → ا

    Args:
        text: Arabic text with alef variants

    Returns:
        Text with normalized alef
    """
    text = text.replace('ى', 'ي')  # Alef maksura → ya
    text = text.replace('أ', 'ا')
    text = text.replace('إ', 'ا')
    text = text.replace('آ', 'ا')

    return text


def remove_tatweel(text: str) -> str:
    """
    Remove Arabic tatweel (kashida) character.

    Args:
        text: Arabic text possibly containing tatweel

    Returns:
        Text without tatweel

    Example:
        >>> remove_tatweel("مـــرحبا")
        "مرحبا"
    """
    return text.replace('\u0640', '')


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace to single spaces.

    Args:
        text: Text with irregular whitespace

    Returns:
        Text with normalized whitespace
    """
    # Replace multiple spaces/tabs/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def normalize_arabic_text(
    text: str,
    remove_tashkeel: bool = False,
    normalize_hamzas: bool = True,
    normalize_alefs: bool = True
) -> str:
    """
    Main normalization function for Arabic text.

    Args:
        text: Raw Arabic text
        remove_tashkeel: Whether to remove diacritics (default: False)
        normalize_hamzas: Normalize hamza variants (default: True)
        normalize_alefs: Normalize alef variants (default: True)

    Returns:
        Normalized Arabic text

    Raises:
        ValueError: If text is empty or contains no Arabic

    Example:
        >>> normalize_arabic_text("إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ")
        "إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ"  # (preserves tashkeel by default)
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    # Check if text contains Arabic
    if not any('\u0600' <= c <= '\u06FF' for c in text):
        raise ValueError("Text must contain Arabic characters")

    # Normalize whitespace
    text = normalize_whitespace(text)

    # Remove tatweel
    text = remove_tatweel(text)

    # Normalize hamza
    if normalize_hamzas:
        text = normalize_hamza(text)

    # Normalize alef
    if normalize_alefs:
        text = normalize_alef(text)

    # Remove diacritics if requested
    if remove_tashkeel:
        text = remove_diacritics(text)

    return text


def has_diacritics(text: str) -> bool:
    """
    Check if text contains any diacritical marks.

    Args:
        text: Arabic text

    Returns:
        True if text has diacritics, False otherwise
    """
    return any(diacritic in text for diacritic in ARABIC_DIACRITICS)
```

**Tests: `backend/tests/core/test_normalization.py`**

```python
"""
Unit tests for Arabic text normalization.
"""

import pytest
from app.core.normalization import (
    remove_diacritics,
    normalize_hamza,
    normalize_alef,
    remove_tatweel,
    normalize_arabic_text,
    has_diacritics,
)


class TestRemoveDiacritics:
    def test_removes_fatha(self):
        assert remove_diacritics("مَرحبا") == "مرحبا"

    def test_removes_damma(self):
        assert remove_diacritics("مُحَمَّد") == "محمد"

    def test_removes_kasra(self):
        assert remove_diacritics("بِسْمِ") == "بسم"

    def test_removes_shadda(self):
        assert remove_diacritics("مُحَمَّد") == "محمد"

    def test_removes_sukun(self):
        assert remove_diacritics("مَرْحَبًا") == "مرحبا"

    def test_removes_tanween(self):
        assert remove_diacritics("شُكْرًا") == "شكرا"

    def test_preserves_arabic_letters(self):
        text = "الشعر العربي"
        assert remove_diacritics(text) == text


class TestNormalizeHamza:
    def test_normalizes_hamza_on_alef(self):
        assert normalize_hamza("أحمد") == "احمد"
        assert normalize_hamza("إبراهيم") == "ابراهيم"
        assert normalize_hamza("آمن") == "امن"

    def test_normalizes_hamza_on_waw(self):
        assert normalize_hamza("مؤمن") == "مومن"

    def test_normalizes_hamza_on_ya(self):
        assert normalize_hamza("شيئ") == "شيي"


class TestNormalizeAlef:
    def test_normalizes_alef_maksura(self):
        assert normalize_alef("على") == "علي"
        assert normalize_alef("موسى") == "موسي"

    def test_normalizes_alef_variants(self):
        assert normalize_alef("أحمد") == "احمد"
        assert normalize_alef("إبراهيم") == "ابراهيم"
        assert normalize_alef("آمن") == "امن"


class TestRemoveTatweel:
    def test_removes_tatweel(self):
        assert remove_tatweel("مـــرحـــبـــا") == "مرحبا"

    def test_handles_no_tatweel(self):
        text = "مرحبا"
        assert remove_tatweel(text) == text


class TestNormalizeArabicText:
    def test_basic_normalization(self):
        result = normalize_arabic_text("إِذَا غَامَرْتَ")
        assert "ا" in result  # Hamza normalized

    def test_with_tashkeel_removal(self):
        result = normalize_arabic_text("مَرْحَبًا", remove_tashkeel=True)
        assert not has_diacritics(result)

    def test_preserves_tashkeel_by_default(self):
        text = "مَرْحَبًا"
        result = normalize_arabic_text(text, remove_tashkeel=False)
        assert has_diacritics(result)

    def test_raises_on_empty_text(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            normalize_arabic_text("")

    def test_raises_on_non_arabic(self):
        with pytest.raises(ValueError, match="must contain Arabic"):
            normalize_arabic_text("Hello World")

    def test_normalizes_whitespace(self):
        result = normalize_arabic_text("مرحبا    بك   \n  أهلا")
        assert "  " not in result


class TestHasDiacritics:
    def test_detects_diacritics(self):
        assert has_diacritics("مَرْحَبًا") == True

    def test_no_diacritics(self):
        assert has_diacritics("مرحبا") == False
```

---

## Task 2: Phonetic Analysis Module

### File: `backend/app/core/phonetics.py`

**Purpose:** Convert Arabic text to phonetic representation for prosodic analysis

**Requirements:**
1. Handle shadda (gemination)
2. Identify short vowels (fatha, damma, kasra)
3. Identify long vowels (madd letters: alef, waw, yaa)
4. Mark sukun (no vowel)
5. Infer vowels if diacritics missing (heuristic-based)

**Implementation:**

```python
"""
Arabic phonetic analysis for prosody.
"""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Phoneme:
    """Represents a phonetic unit."""
    consonant: str
    vowel: str  # 'a', 'u', 'i', 'aa', 'uu', 'ii', '' (sukun)
    has_shadda: bool = False

    def __str__(self):
        shadda_mark = "ّ" if self.has_shadda else ""
        return f"{self.consonant}{shadda_mark}{self.vowel}"

    def is_long_vowel(self) -> bool:
        """Check if phoneme has long vowel (madd)."""
        return self.vowel in ['aa', 'uu', 'ii']

    def is_sukun(self) -> bool:
        """Check if phoneme has sukun (no vowel)."""
        return self.vowel == ''


def extract_phonemes(text: str, has_tashkeel: bool = False) -> List[Phoneme]:
    """
    Extract phonemes from Arabic text.

    Args:
        text: Arabic text (normalized)
        has_tashkeel: Whether text has diacritics

    Returns:
        List of Phoneme objects

    Example:
        >>> extract_phonemes("كَتَبَ", has_tashkeel=True)
        [Phoneme('ك', 'a'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
    """
    phonemes = []

    # Diacritic mappings
    VOWEL_MAP = {
        '\u064E': 'a',   # Fatha
        '\u064F': 'u',   # Damma
        '\u0650': 'i',   # Kasra
        '\u0652': '',    # Sukun
        '\u064B': 'an',  # Tanween Fath
        '\u064C': 'un',  # Tanween Damm
        '\u064D': 'in',  # Tanween Kasr
    }

    LONG_VOWEL_MAP = {
        'ا': 'aa',  # Alef (after fatha)
        'و': 'uu',  # Waw (after damma)
        'ي': 'ii',  # Ya (after kasra)
    }

    i = 0
    while i < len(text):
        char = text[i]

        # Skip whitespace
        if char.isspace():
            i += 1
            continue

        # Check if Arabic letter
        if '\u0621' <= char <= '\u064A':
            consonant = char
            vowel = ''
            has_shadda = False

            # Look ahead for diacritics
            j = i + 1
            while j < len(text) and text[j] in VOWEL_MAP.keys() or text[j] == '\u0651':
                if text[j] == '\u0651':  # Shadda
                    has_shadda = True
                else:
                    vowel = VOWEL_MAP[text[j]]
                j += 1

            # Check for long vowel (madd letter after short vowel)
            if j < len(text) and text[j] in LONG_VOWEL_MAP:
                if vowel in ['a', 'u', 'i']:
                    vowel = LONG_VOWEL_MAP[text[j]]
                    j += 1

            # If no tashkeel, infer vowel (heuristic: assume 'a')
            if not has_tashkeel and vowel == '':
                # Simple heuristic: assume fatha unless it's end of word
                if i < len(text) - 1 and text[i+1] not in [' ', '.', '،']:
                    vowel = 'a'

            phonemes.append(Phoneme(consonant, vowel, has_shadda))
            i = j
        else:
            i += 1

    return phonemes


def phonemes_to_pattern(phonemes: List[Phoneme]) -> str:
    """
    Convert phonemes to prosodic pattern string.

    Pattern symbols:
    - / = haraka (moving, CV)
    - o = sukun (still, CVC or CVV)

    Args:
        phonemes: List of Phoneme objects

    Returns:
        Pattern string like "/o//o/o"

    Example:
        >>> phonemes = [Phoneme('k', 'a'), Phoneme('t', 'a'), Phoneme('b', '')]
        >>> phonemes_to_pattern(phonemes)
        "//o"
    """
    pattern = ""

    for phoneme in phonemes:
        if phoneme.is_sukun():
            pattern += "o"
        elif phoneme.is_long_vowel():
            pattern += "/o"  # Long vowel = haraka + sukun
        else:
            pattern += "/"   # Short vowel = haraka

    return pattern


def text_to_phonetic_pattern(text: str, has_tashkeel: bool = None) -> str:
    """
    Convert Arabic text directly to phonetic pattern.

    Args:
        text: Normalized Arabic text
        has_tashkeel: Auto-detect if None

    Returns:
        Phonetic pattern string

    Example:
        >>> text_to_phonetic_pattern("كَتَبَ")
        "///"
    """
    from app.core.normalization import has_diacritics

    if has_tashkeel is None:
        has_tashkeel = has_diacritics(text)

    phonemes = extract_phonemes(text, has_tashkeel)
    return phonemes_to_pattern(phonemes)
```

**Tests: `backend/tests/core/test_phonetics.py`**

```python
"""
Unit tests for phonetic analysis.
"""

import pytest
from app.core.phonetics import (
    Phoneme,
    extract_phonemes,
    phonemes_to_pattern,
    text_to_phonetic_pattern,
)


class TestPhoneme:
    def test_long_vowel_detection(self):
        p = Phoneme('ك', 'aa')
        assert p.is_long_vowel() == True

        p = Phoneme('ك', 'a')
        assert p.is_long_vowel() == False

    def test_sukun_detection(self):
        p = Phoneme('ك', '')
        assert p.is_sukun() == True

        p = Phoneme('ك', 'a')
        assert p.is_sukun() == False


class TestExtractPhonemes:
    def test_simple_word_with_tashkeel(self):
        phonemes = extract_phonemes("كَتَبَ", has_tashkeel=True)
        assert len(phonemes) == 3
        assert all(p.vowel == 'a' for p in phonemes)

    def test_word_with_sukun(self):
        phonemes = extract_phonemes("كَتْبَ", has_tashkeel=True)
        assert len(phonemes) == 3
        assert phonemes[0].vowel == 'a'
        assert phonemes[1].vowel == ''  # sukun
        assert phonemes[2].vowel == 'a'

    def test_word_with_shadda(self):
        phonemes = extract_phonemes("مُحَمَّد", has_tashkeel=True)
        # Find the shadda phoneme
        shadda_phonemes = [p for p in phonemes if p.has_shadda]
        assert len(shadda_phonemes) >= 1

    def test_word_with_long_vowel(self):
        # "كتاب" with tashkeel: "كِتَاب"
        phonemes = extract_phonemes("كِتَاب", has_tashkeel=True)
        # Should detect 'aa' in تا
        long_vowels = [p for p in phonemes if p.is_long_vowel()]
        assert len(long_vowels) >= 1


class TestPhonemesToPattern:
    def test_all_short_vowels(self):
        phonemes = [Phoneme('ك', 'a'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "///"

    def test_with_sukun(self):
        phonemes = [Phoneme('ك', 'a'), Phoneme('ت', ''), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "/o/"

    def test_with_long_vowel(self):
        phonemes = [Phoneme('ك', 'aa'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "/o//"


class TestTextToPhoneticPattern:
    def test_simple_verse(self):
        # Simple test (exact pattern depends on implementation details)
        pattern = text_to_phonetic_pattern("كَتَبَ")
        assert '/' in pattern
        assert len(pattern) >= 3

    def test_handles_no_tashkeel(self):
        # Should infer vowels
        pattern = text_to_phonetic_pattern("كتب", has_tashkeel=False)
        assert pattern != ""
```

---

## Task 3: Taqti' Algorithm Implementation

### File: `backend/app/core/taqti3.py`

**Purpose:** Perform prosodic scansion on Arabic verse

**Requirements:**
1. Convert verse to phonetic pattern
2. Map pattern to tafa'il (prosodic feet)
3. Return tafa'il sequence string

**Implementation:**

```python
"""
Taqti3 (تقطيع) - Prosodic scansion for Arabic poetry.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from app.core.normalization import normalize_arabic_text, has_diacritics
from app.core.phonetics import text_to_phonetic_pattern


@dataclass
class Taf3ila:
    """Represents a taf'ila (prosodic foot)."""
    name: str
    pattern: str  # e.g., "/o//o" for فعولن

    def __str__(self):
        return self.name


# The 8 basic tafa'il
BASIC_TAFAIL = {
    "/o//o": "فعولن",      # fa'uulun
    "//o/o": "مفاعيلن",    # mafaa'iilun
    "///o": "مفاعلتن",     # mafaa'alatun
    "/o/o//o": "مستفعلن",  # mustaf'ilun
    "//o//o": "فاعلاتن",   # faa'ilaatun
    "/o/o/o": "فاعلن",     # faa'ilun
    "///": "فعلن",         # fa'lan
    "/o//": "مفعولات",     # maf'uulaatu
}


def pattern_to_tafail(pattern: str) -> List[str]:
    """
    Convert phonetic pattern to list of tafa'il.

    Uses greedy matching (longest match first).

    Args:
        pattern: Phonetic pattern string (e.g., "/o//o/o//o")

    Returns:
        List of taf'ila names

    Example:
        >>> pattern_to_tafail("/o//o/o//o")
        ["فعولن", "مفاعيلن"]  # (simplified)
    """
    tafail = []
    i = 0

    while i < len(pattern):
        matched = False

        # Try to match longest pattern first (greedy)
        for length in range(min(8, len(pattern) - i), 0, -1):
            substring = pattern[i:i+length]

            if substring in BASIC_TAFAIL:
                tafail.append(BASIC_TAFAIL[substring])
                i += length
                matched = True
                break

        if not matched:
            # No match found, skip one character
            i += 1

    return tafail


def perform_taqti3(verse: str, normalize: bool = True) -> str:
    """
    Perform taqti3 (prosodic scansion) on Arabic verse.

    Args:
        verse: Arabic verse text
        normalize: Whether to normalize text first

    Returns:
        Tafa'il pattern string (e.g., "فعولن مفاعيلن فعولن مفاعيلن")

    Raises:
        ValueError: If verse is invalid

    Example:
        >>> perform_taqti3("إذا غامَرتَ في شَرَفٍ مَرومِ")
        "فعولن مفاعيلن فعولن مفاعيلن"
    """
    if not verse or not verse.strip():
        raise ValueError("Verse cannot be empty")

    # Normalize text
    if normalize:
        verse = normalize_arabic_text(verse)

    # Convert to phonetic pattern
    has_tash = has_diacritics(verse)
    pattern = text_to_phonetic_pattern(verse, has_tash)

    # Convert pattern to tafa'il
    tafail = pattern_to_tafail(pattern)

    # Join with spaces
    return " ".join(tafail)
```

**Tests: `backend/tests/core/test_taqti3.py`**

```python
"""
Unit tests for taqti3 (prosodic scansion).
"""

import pytest
from app.core.taqti3 import (
    pattern_to_tafail,
    perform_taqti3,
    BASIC_TAFAIL,
)


class TestPatternToTafail:
    def test_simple_pattern(self):
        # Test known pattern
        result = pattern_to_tafail("/o//o")
        assert "فعولن" in result or len(result) > 0

    def test_empty_pattern(self):
        result = pattern_to_tafail("")
        assert result == []


class TestPerformTaqti3:
    def test_raises_on_empty_verse(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            perform_taqti3("")

    def test_returns_string(self):
        result = perform_taqti3("كتب الشعر")
        assert isinstance(result, str)

    # TODO: Add tests with known verses from each bahr
    # These require accurate test data with expected outputs
```

---

## Task 4: Bahr Detection

### File: `backend/app/core/bahr_detector.py`

**Purpose:** Detect which bahr (meter) a verse follows

**Requirements:**
1. Load 16 bahr patterns from database
2. Compare verse tafa'il to bahr templates
3. Calculate confidence score
4. Return best match

**Implementation:**

```python
"""
Bahr (meter) detection for Arabic poetry.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from difflib import SequenceMatcher
from app.core.taqti3 import perform_taqti3


@dataclass
class BahrInfo:
    """Information about a detected bahr."""
    id: int
    name_ar: str
    name_en: str
    pattern: str
    confidence: float  # 0.0 to 1.0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "pattern": self.pattern,
            "confidence": round(self.confidence, 2)
        }


# Hardcoded bahrs for now (TODO: load from database)
BAHRS_DATA = [
    {"id": 1, "name_ar": "الطويل", "name_en": "at-Tawil",
     "pattern": "فعولن مفاعيلن فعولن مفاعيلن"},

    {"id": 2, "name_ar": "الكامل", "name_en": "al-Kamil",
     "pattern": "متفاعلن متفاعلن متفاعلن"},

    {"id": 3, "name_ar": "الوافر", "name_en": "al-Wafir",
     "pattern": "مفاعلتن مفاعلتن فعولن"},

    {"id": 4, "name_ar": "الرمل", "name_en": "ar-Ramal",
     "pattern": "فاعلاتن فاعلاتن فاعلاتن"},

    # TODO: Add remaining 12 bahrs
]


class BahrDetector:
    """Detects bahr (meter) from verse tafa'il pattern."""

    def __init__(self):
        """Initialize with bahr data."""
        self.bahrs = BAHRS_DATA

    def calculate_similarity(self, tafail1: str, tafail2: str) -> float:
        """
        Calculate similarity between two tafa'il patterns.

        Uses fuzzy matching to allow for minor variations (zihafat).

        Args:
            tafail1: First tafa'il pattern
            tafail2: Second tafa'il pattern

        Returns:
            Similarity score (0.0 to 1.0)
        """
        return SequenceMatcher(None, tafail1, tafail2).ratio()

    def detect_bahr(self, tafail_pattern: str) -> Optional[BahrInfo]:
        """
        Detect bahr from tafa'il pattern.

        Args:
            tafail_pattern: Tafa'il string (e.g., "فعولن مفاعيلن...")

        Returns:
            BahrInfo object with best match, or None if no match

        Example:
            >>> detector = BahrDetector()
            >>> result = detector.detect_bahr("فعولن مفاعيلن فعولن مفاعيلن")
            >>> result.name_ar
            "الطويل"
        """
        if not tafail_pattern:
            return None

        best_match = None
        best_similarity = 0.0

        for bahr in self.bahrs:
            similarity = self.calculate_similarity(
                tafail_pattern,
                bahr["pattern"]
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = bahr

        # Only return if confidence above threshold
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
        Complete analysis: taqti3 + bahr detection.

        Args:
            verse: Arabic verse text

        Returns:
            BahrInfo or None

        Example:
            >>> detector = BahrDetector()
            >>> result = detector.analyze_verse("إذا غامَرتَ في شَرَفٍ مَرومِ")
            >>> result.name_ar
            "الطويل"
        """
        # Perform taqti3
        tafail = perform_taqti3(verse)

        # Detect bahr
        return self.detect_bahr(tafail)
```

**Tests: `backend/tests/core/test_bahr_detector.py`**

```python
"""
Unit tests for bahr detection.
"""

import pytest
from app.core.bahr_detector import BahrDetector, BahrInfo


class TestBahrDetector:
    def setup_method(self):
        self.detector = BahrDetector()

    def test_initialization(self):
        assert len(self.detector.bahrs) >= 4

    def test_calculate_similarity_exact_match(self):
        pattern = "فعولن مفاعيلن"
        similarity = self.detector.calculate_similarity(pattern, pattern)
        assert similarity == 1.0

    def test_calculate_similarity_different(self):
        pattern1 = "فعولن مفاعيلن"
        pattern2 = "متفاعلن متفاعلن"
        similarity = self.detector.calculate_similarity(pattern1, pattern2)
        assert 0.0 <= similarity < 1.0

    def test_detect_bahr_returns_bahrinfo(self):
        # Use known pattern
        result = self.detector.detect_bahr("فعولن مفاعيلن فعولن مفاعيلن")
        assert result is not None
        assert isinstance(result, BahrInfo)

    def test_detect_bahr_returns_none_for_invalid(self):
        result = self.detector.detect_bahr("invalid pattern xyz")
        # May return None or low confidence match
        assert result is None or result.confidence < 0.7

    # TODO: Add tests with real verses from each bahr
    # Requires test dataset
```

---

## Task 5: Complete Test Dataset

### File: `backend/tests/fixtures/test_verses.json`

**Purpose:** Reference verses for testing accuracy

**Format:**

```json
{
  "verses": [
    {
      "text": "إِذا غامَرتَ في شَرَفٍ مَرومِ",
      "poet": "أبو الطيب المتنبي",
      "bahr": "الطويل",
      "expected_tafail": "فعولن مفاعيلن فعولن مفاعيلن",
      "notes": "Famous verse, standard at-Tawil"
    },
    {
      "text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً",
      "poet": "أبو العتاهية",
      "bahr": "الكامل",
      "expected_tafail": "متفاعلن متفاعلن متفاعلن",
      "notes": "Standard al-Kamil"
    }
    // Add 50-100 verses covering all 16 bahrs
  ]
}
```

### File: `backend/tests/core/test_accuracy.py`

**Purpose:** Integration test for end-to-end accuracy

```python
"""
Accuracy tests using real poetry dataset.
"""

import json
import pytest
from pathlib import Path
from app.core.bahr_detector import BahrDetector


@pytest.fixture
def test_verses():
    """Load test verses from JSON file."""
    fixture_path = Path(__file__).parent.parent / "fixtures" / "test_verses.json"
    with open(fixture_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['verses']


class TestAccuracy:
    def setup_method(self):
        self.detector = BahrDetector()

    def test_overall_accuracy(self, test_verses):
        """Test accuracy across all test verses."""
        correct = 0
        total = len(test_verses)

        for verse_data in test_verses:
            result = self.detector.analyze_verse(verse_data['text'])

            if result and result.name_ar == verse_data['bahr']:
                correct += 1

        accuracy = correct / total
        print(f"\nAccuracy: {accuracy*100:.1f}% ({correct}/{total})")

        # Assertion: Must achieve 90%+ accuracy
        assert accuracy >= 0.90, f"Accuracy {accuracy*100:.1f}% below target 90%"

    def test_accuracy_by_bahr(self, test_verses):
        """Test accuracy for each bahr individually."""
        from collections import defaultdict

        results_by_bahr = defaultdict(lambda: {"correct": 0, "total": 0})

        for verse_data in test_verses:
            bahr = verse_data['bahr']
            results_by_bahr[bahr]["total"] += 1

            result = self.detector.analyze_verse(verse_data['text'])
            if result and result.name_ar == bahr:
                results_by_bahr[bahr]["correct"] += 1

        # Print results
        print("\n\nAccuracy by Bahr:")
        for bahr, stats in results_by_bahr.items():
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
            print(f"  {bahr}: {accuracy*100:.1f}% ({stats['correct']}/{stats['total']})")

            # Each bahr should have >80% accuracy
            assert accuracy >= 0.80, f"{bahr} accuracy {accuracy*100:.1f}% below 80%"
```

---

## Task 6: Setup & Documentation

### File: `backend/app/core/__init__.py`

```python
"""
Core prosody analysis engine for BAHR platform.
"""

from .normalization import normalize_arabic_text, has_diacritics
from .phonetics import text_to_phonetic_pattern, extract_phonemes
from .taqti3 import perform_taqti3
from .bahr_detector import BahrDetector, BahrInfo

__all__ = [
    'normalize_arabic_text',
    'has_diacritics',
    'text_to_phonetic_pattern',
    'extract_phonemes',
    'perform_taqti3',
    'BahrDetector',
    'BahrInfo',
]
```

### File: `backend/README_PROSODY_ENGINE.md`

```markdown
# Prosody Engine

Arabic poetry prosody analysis engine.

## Features

- Text normalization (hamza, alef, diacritics)
- Phonetic analysis
- Taqti3 (prosodic scansion)
- Bahr (meter) detection
- 90%+ accuracy on classical poetry

## Usage

```python
from app.core import BahrDetector

detector = BahrDetector()
result = detector.analyze_verse("إذا غامَرتَ في شَرَفٍ مَرومِ")

print(result.name_ar)      # الطويل
print(result.confidence)   # 0.98
```

## Testing

```bash
pytest backend/tests/core/ -v
```

## Accuracy

Target: 90%+ on test dataset

Run accuracy test:
```bash
pytest backend/tests/core/test_accuracy.py -v -s
```
```

---

## Acceptance Criteria Checklist

- [ ] `normalization.py` implemented with all functions
- [ ] `phonetics.py` implemented with phoneme extraction
- [ ] `taqti3.py` implemented with pattern matching
- [ ] `bahr_detector.py` implemented with 4+ bahrs
- [ ] All unit tests pass (80%+ code coverage)
- [ ] Test dataset created (50+ verses, all 4 bahrs)
- [ ] Accuracy test achieves 90%+ on test dataset
- [ ] Code documented with docstrings
- [ ] README written

---

## Next Steps (Week 3-4)

After completing this spec:
1. Create database schema for bahrs table
2. Implement FastAPI endpoint `/analyze`
3. Add Redis caching layer
4. Generate API documentation

---

## Notes for Codex

- **Start with normalization.py** - it's the foundation
- **Test each module independently** before integration
- **Use real Arabic text** in tests, not transliteration
- **Accuracy is critical** - 90% target must be met
- **If accuracy low**, revisit phonetics and pattern matching logic

## Questions?

If any part is unclear, ask for:
- More examples of specific tafa'il patterns
- Clarification on zihafat (prosodic variations)
- Additional test cases
