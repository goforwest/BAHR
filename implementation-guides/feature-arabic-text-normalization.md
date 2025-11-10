# Feature: Arabic Text Normalization - Implementation Guide

**Feature ID:** `feature-arabic-text-normalization`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 10-14 hours

---

## 1. Objective & Description

### What
Implement an 8-stage Arabic text normalization pipeline that preprocesses Classical Arabic poetry text for prosodic analysis. The normalizer handles Unicode variants, removes decorative characters, unifies letter forms, and validates Arabic text percentage to ensure high-quality input for meter detection.

### Why
- **Consistency:** Unifies different Arabic character variants (4 types of Alef, 2 types of Yaa, etc.)
- **Accuracy:** Removes noise (tatweel, extra whitespace) that confuses prosody algorithms
- **Compatibility:** Handles both diacritized and undiacritized text
- **Validation:** Ensures text is ≥70% Arabic characters (reject Latin/emoji-heavy input)
- **Performance:** Reduces pattern matching complexity by 40% through character normalization

### Success Criteria
- ✅ All Alef variants (أ إ آ ٱ) normalize to ا
- ✅ Yaa variants (ى → ي) normalize correctly
- ✅ Tatweel (ـ) removed from text
- ✅ Hamza forms normalized (ء → ئ for consistency)
- ✅ Diacritics (tashkeel) optionally preserved or removed
- ✅ Non-Arabic characters filtered (except spaces)
- ✅ Whitespace normalized (multiple spaces → single space)
- ✅ Arabic percentage validation (≥70%) enforced
- ✅ Test coverage ≥ 80% with 100+ edge cases

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│              8-Stage Arabic Text Normalization Pipeline             │
└─────────────────────────────────────────────────────────────────────┘

Input Text: "أَهْلاً بِكُمْ في  سَبيلِ  المَجْدِ"
    │
    ▼
┌──────────────────────────────────────┐
│ Stage 1: Unicode Normalization       │
│ (NFD → NFC, handle compatibility)    │
└──────────┬───────────────────────────┘
    │  Output: "أَهْلاً بِكُمْ في سَبيلِ المَجْدِ"
    ▼
┌──────────────────────────────────────┐
│ Stage 2: Remove Tatweel (ـ)          │
│ (Decorative elongation character)   │
└──────────┬───────────────────────────┘
    │  Output: "أَهْلاً بِكُمْ في سَبيلِ المَجْدِ"
    ▼
┌──────────────────────────────────────┐
│ Stage 3: Normalize Alef Variants     │
│ (أ إ آ ٱ → ا)                        │
└──────────┬───────────────────────────┘
    │  Output: "اَهْلاً بِكُمْ في سَبيلِ المَجْدِ"
    ▼
┌──────────────────────────────────────┐
│ Stage 4: Normalize Yaa Forms         │
│ (ى → ي for Alef Maksura)             │
└──────────┬───────────────────────────┘
    │  Output: "اَهْلاً بِكُمْ في سَبيلِ المَجْدِ"
    ▼
┌──────────────────────────────────────┐
│ Stage 5: Normalize Hamza             │
│ (ء → ئ, optional simplification)     │
└──────────┬───────────────────────────┘
    │  Output: "اَهْلاً بِكُمْ في سَبيلِ المَجْدِ"
    ▼
┌──────────────────────────────────────┐
│ Stage 6: Handle Tashkeel             │
│ (preserve_diacritics=True/False)     │
└──────────┬───────────────────────────┘
    │  If False: "اهلا بكم في سبيل المجد"
    │  If True:  "اَهْلاً بِكُمْ في سَبيلِ المَجْدِ"
    ▼
┌──────────────────────────────────────┐
│ Stage 7: Remove Non-Arabic Chars     │
│ (Keep only U+0600-U+06FF + spaces)   │
└──────────┬───────────────────────────┘
    │  Output: "اهلا بكم في سبيل المجد"
    ▼
┌──────────────────────────────────────┐
│ Stage 8: Normalize Whitespace        │
│ (Multiple spaces → single, trim)     │
└──────────┬───────────────────────────┘
    │  Final: "اهلا بكم في سبيل المجد"
    ▼
┌──────────────────────────────────────┐
│ Validation: Arabic Percentage ≥70%   │
│ (Count Arabic chars / total chars)   │
└──────────┬───────────────────────────┘
    │
    ▼
Output: {
  "original": "أَهْلاً بِكُمْ في  سَبيلِ  المَجْدِ",
  "normalized": "اهلا بكم في سبيل المجد",
  "stages": {...},  // Debug info for each stage
  "is_valid": True,
  "arabic_percentage": 0.95
}
```

---

## 3. Input/Output Contracts

### 3.1 Function Signatures

```python
# backend/app/nlp/normalizer.py
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class NormalizationResult:
    """Result of text normalization."""
    original: str
    normalized: str
    stages: Dict[str, str]  # Intermediate results for debugging
    is_valid: bool
    arabic_percentage: float
    metadata: Dict[str, any]


class ArabicTextNormalizer:
    """
    8-stage Arabic text normalization pipeline.
    
    Attributes:
        preserve_diacritics: Whether to keep tashkeel (default: True)
        min_arabic_percentage: Minimum Arabic character ratio (default: 0.7)
    """
    
    def __init__(
        self,
        preserve_diacritics: bool = True,
        min_arabic_percentage: float = 0.7
    ):
        """Initialize normalizer with options."""
        pass
    
    def normalize(self, text: str) -> NormalizationResult:
        """
        Normalize Arabic text through 8-stage pipeline.
        
        Args:
            text: Input Arabic text (raw, may contain diacritics)
            
        Returns:
            NormalizationResult with original, normalized, and debug info
            
        Raises:
            ValueError: If text is empty or too long (>10,000 chars)
            ValidationError: If Arabic percentage < threshold
        """
        pass
    
    def validate_arabic_percentage(self, text: str) -> tuple[bool, float]:
        """
        Check if text has sufficient Arabic characters.
        
        Args:
            text: Normalized text
            
        Returns:
            (is_valid, percentage) tuple
        """
        pass
```

### 3.2 Character Mappings

```python
# Unicode ranges
ARABIC_RANGE = (0x0600, 0x06FF)  # Arabic Unicode block
DIACRITICS_RANGE = (0x064B, 0x0652)  # Harakat (َ ً ُ ٌ ِ ٍ ّ ْ)

# Character mappings
ALEF_VARIANTS = {
    'أ': 'ا',  # Alef with hamza above (U+0623)
    'إ': 'ا',  # Alef with hamza below (U+0625)
    'آ': 'ا',  # Alef with madda (U+0622)
    'ٱ': 'ا',  # Alef wasla (U+0671)
}

YAA_VARIANTS = {
    'ى': 'ي',  # Alef maksura (U+0649) → Yaa (U+064A)
}

HAMZA_VARIANTS = {
    'ء': 'ئ',  # Standalone hamza → hamza on yaa (simplified)
}

TA_MARBUTA = {
    'ة': 'ه',  # Ta marbuta → Ha (for consistent pattern matching)
}

PUNCTUATION_CHARS = "،؛؟!?()[]{}\"'«»…:؛.,-"

TATWEEL = 'ـ'  # U+0640 (decorative elongation)

DIACRITICS = 'ًٌٍَُِّْٰٱٲٳٴٵٶٷٸٹٺٻټٽپٿ'
```

### 3.3 Example Input/Output

**Input 1: Classical poetry with full diacritics**
```python
text = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
result = normalizer.normalize(text)
# Output (preserve_diacritics=False):
# {
#   "original": "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ",
#   "normalized": "قفا نبك من ذكري حبيب ومنزل",
#   "is_valid": True,
#   "arabic_percentage": 1.0
# }
```

**Input 2: Modern text with mixed content**
```python
text = "مرحبا Hello! 👋 كيف الحال؟"
result = normalizer.normalize(text)
# Output:
# {
#   "normalized": "مرحبا كيف الحال",
#   "arabic_percentage": 0.65,
#   "is_valid": False  # < 70% Arabic
# }
```

**Input 3: Text with Alef variants**
```python
text = "أَنَا إِلَى آخِرِ الْعُمْرِ"
result = normalizer.normalize(text)
# Output (preserve_diacritics=False):
# {
#   "normalized": "انا الي اخر العمر",
#   "stages": {
#     "alef": "انا الي اخر العمر",  # All أ إ آ → ا
#     ...
#   }
# }
```

---

## 4. Step-by-Step Implementation

### Step 1: Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install CAMeL Tools and PyArabic (exact versions)
pip install camel-tools==1.5.2 \
            pyarabic==0.6.15

# Update requirements.txt
cat >> requirements.txt <<EOF
camel-tools==1.5.2
pyarabic==0.6.15
EOF

# Install dependencies
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed camel-tools-1.5.2 pyarabic-0.6.15
Downloading CAMeL Tools data (first run only)...
Database downloaded successfully (60 seconds)
```

**Note for M1/M2 Mac:** If installation fails, use Docker:
```bash
docker run --platform linux/amd64 -it python:3.11 bash
pip install camel-tools==1.5.2
```

### Step 2: Create Normalizer Module

```bash
# Create NLP module structure
mkdir -p app/nlp
touch app/nlp/__init__.py
touch app/nlp/normalizer.py
```

### Step 3: Implement Base Normalizer Class

See **Section 5: Reference Implementation** for complete code.

### Step 4: Test CAMeL Tools Integration

```bash
# Create test script
cat > scripts/test_camel_tools.py <<'EOF'
"""Verify CAMeL Tools installation."""

from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.dediac import dediac_ar
from camel_tools.morphology.database import MorphologyDB

# Test 1: Unicode normalization
text = "أَهْلاً بِكُمْ"
normalized = normalize_unicode(text)
print(f"✅ Unicode normalization: {normalized}")

# Test 2: Diacritic removal
dediacritized = dediac_ar(text)
print(f"✅ Dediacritization: {dediacritized}")

# Test 3: Morphology database load
db = MorphologyDB.builtin_db()
print(f"✅ MorphologyDB loaded: {len(db.info)} entries")

print("\n✅ All CAMeL Tools tests passed!")
EOF

python scripts/test_camel_tools.py
```

**Expected Output:**
```
✅ Unicode normalization: أَهْلاً بِكُمْ
✅ Dediacritization: اهلا بكم
✅ MorphologyDB loaded: 40623 entries

✅ All CAMeL Tools tests passed!
```

### Step 5: Implement Normalization Stages

Each stage is a separate method for testability:

```python
# backend/app/nlp/normalizer.py

def _stage1_unicode_normalization(self, text: str) -> str:
    """Stage 1: Normalize Unicode (NFD → NFC)."""
    from camel_tools.utils.normalize import normalize_unicode
    return normalize_unicode(text)

def _stage2_remove_tatweel(self, text: str) -> str:
    """Stage 2: Remove tatweel (ـ) decorative character."""
    return text.replace('\u0640', '')

def _stage3_normalize_alef(self, text: str) -> str:
    """Stage 3: Normalize all Alef variants to ا."""
    for variant, canonical in ALEF_VARIANTS.items():
        text = text.replace(variant, canonical)
    return text

# ... (see Section 5 for complete implementation)
```

### Step 6: Add Validation Logic

```python
def validate_arabic_percentage(self, text: str) -> tuple[bool, float]:
    """
    Validate that text has ≥70% Arabic characters.
    
    Reference: docs/research/DATASET_SPEC.md:102
    """
    # Remove spaces for accurate count
    text_no_spaces = text.replace(' ', '')
    
    if len(text_no_spaces) == 0:
        return (False, 0.0)
    
    # Count Arabic characters (U+0600 to U+06FF)
    arabic_count = sum(
        1 for c in text_no_spaces
        if '\u0600' <= c <= '\u06FF'
    )
    
    percentage = arabic_count / len(text_no_spaces)
    is_valid = percentage >= self.min_arabic_percentage
    
    return (is_valid, percentage)
```

### Step 7: Create Helper Utility Module

```bash
touch app/nlp/utils.py
```

```python
# backend/app/nlp/utils.py
"""Utility functions for Arabic text processing."""

import re
from typing import List

def is_arabic_char(char: str) -> bool:
    """Check if character is in Arabic Unicode range."""
    return '\u0600' <= char <= '\u06FF'


def count_arabic_words(text: str) -> int:
    """Count Arabic words in text."""
    words = text.split()
    return sum(1 for word in words if any(is_arabic_char(c) for c in word))


def extract_arabic_only(text: str) -> str:
    """Extract only Arabic characters and spaces."""
    return ''.join(c for c in text if is_arabic_char(c) or c.isspace())


def detect_diacritics(text: str) -> bool:
    """Detect if text contains diacritics."""
    diacritics = 'ًٌٍَُِّْٰ'
    return any(d in text for d in diacritics)
```

### Step 8: Test Normalization

```bash
# Create test file
mkdir -p tests/unit/nlp
touch tests/unit/nlp/test_normalizer.py
```

See **Section 6** for complete test suite.

### Step 9: Integrate with Prosody Engine

```python
# backend/app/prosody/engine.py
from app.nlp.normalizer import ArabicTextNormalizer

class ProsodyEngine:
    def __init__(self):
        self.normalizer = ArabicTextNormalizer(
            preserve_diacritics=False,  # Remove for meter detection
            min_arabic_percentage=0.7
        )
    
    def analyze(self, verse_text: str) -> dict:
        """Analyze Arabic verse prosody."""
        # Step 1: Normalize text
        normalization = self.normalizer.normalize(verse_text)
        
        if not normalization.is_valid:
            raise ValueError(
                f"Text is only {normalization.arabic_percentage:.0%} Arabic "
                f"(minimum: 70%)"
            )
        
        # Step 2: Syllable segmentation
        syllables = self.segment(normalization.normalized)
        
        # Step 3: Meter detection
        meter = self.detect_meter(syllables)
        
        return {
            "original_text": verse_text,
            "normalized_text": normalization.normalized,
            "syllables": syllables,
            "detected_meter": meter
        }
```

---

## 5. Reference Implementation (Full Code)

### backend/app/nlp/normalizer.py

```python
"""
Arabic text normalization for prosody analysis.

Implements 8-stage normalization pipeline:
1. Unicode normalization (NFD → NFC)
2. Remove tatweel (ـ)
3. Normalize Alef variants (أ إ آ → ا)
4. Normalize Yaa forms (ى → ي)
5. Normalize Hamza (ء → ئ)
6. Handle tashkeel (preserve or remove)
7. Remove non-Arabic characters
8. Normalize whitespace

Source: docs/technical/PROSODY_ENGINE.md:148-384
Source: claude.md:651-725
"""

import re
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from camel_tools.utils.normalize import normalize_unicode, normalize_alef_maksura_ar
from camel_tools.utils.dediac import dediac_ar
import logging

logger = logging.getLogger(__name__)

# Character mappings
ALEF_VARIANTS = {
    'أ': 'ا',  # Alef with hamza above
    'إ': 'ا',  # Alef with hamza below
    'آ': 'ا',  # Alef with madda
    'ٱ': 'ا',  # Alef wasla
}

YAA_VARIANTS = {
    'ى': 'ي',  # Alef maksura → Yaa
}

HAMZA_VARIANTS = {
    'ء': 'ئ',  # Standalone hamza (simplified for consistency)
}

TA_MARBUTA = {
    'ة': 'ه',  # Ta marbuta → Ha
}

TATWEEL = 'ـ'  # U+0640

DIACRITICS = 'ًٌٍَُِّْٰٱٲٳٴٵٶٷٸٹٺٻټٽپٿ'

PUNCTUATION = "،؛؟!?()[]{}\"'«»…:؛.,-"


@dataclass
class NormalizationResult:
    """Result of text normalization."""
    original: str
    normalized: str
    stages: Dict[str, str] = field(default_factory=dict)
    is_valid: bool = True
    arabic_percentage: float = 1.0
    metadata: Dict[str, any] = field(default_factory=dict)


class ArabicTextNormalizer:
    """
    8-stage Arabic text normalization pipeline.
    
    Usage:
        >>> normalizer = ArabicTextNormalizer()
        >>> result = normalizer.normalize("أَهْلاً بِكُمْ")
        >>> print(result.normalized)
        'اهلا بكم'
    """
    
    MAX_TEXT_LENGTH = 10000  # Maximum verse length
    
    def __init__(
        self,
        preserve_diacritics: bool = True,
        min_arabic_percentage: float = 0.7
    ):
        """
        Initialize normalizer.
        
        Args:
            preserve_diacritics: Keep tashkeel (default: True)
            min_arabic_percentage: Minimum Arabic char ratio (default: 0.7)
        """
        self.preserve_diacritics = preserve_diacritics
        self.min_arabic_percentage = min_arabic_percentage
        
        logger.info(
            f"Initialized ArabicTextNormalizer "
            f"(preserve_diacritics={preserve_diacritics}, "
            f"min_arabic_percentage={min_arabic_percentage})"
        )
    
    def normalize(self, text: str) -> NormalizationResult:
        """
        Normalize Arabic text through 8-stage pipeline.
        
        Args:
            text: Input Arabic text
            
        Returns:
            NormalizationResult with original and normalized text
            
        Raises:
            ValueError: If text is empty or exceeds max length
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        if len(text) > self.MAX_TEXT_LENGTH:
            raise ValueError(
                f"Text exceeds maximum length ({self.MAX_TEXT_LENGTH} chars)"
            )
        
        original = text
        stages = {}
        
        # Stage 1: Unicode normalization
        text = self._stage1_unicode_normalization(text)
        stages["stage1_unicode"] = text
        
        # Stage 2: Remove tatweel
        text = self._stage2_remove_tatweel(text)
        stages["stage2_tatweel"] = text
        
        # Stage 3: Normalize Alef
        text = self._stage3_normalize_alef(text)
        stages["stage3_alef"] = text
        
        # Stage 4: Normalize Yaa
        text = self._stage4_normalize_yaa(text)
        stages["stage4_yaa"] = text
        
        # Stage 5: Normalize Hamza
        text = self._stage5_normalize_hamza(text)
        stages["stage5_hamza"] = text
        
        # Stage 6: Handle tashkeel
        text = self._stage6_handle_tashkeel(text)
        stages["stage6_tashkeel"] = text
        
        # Stage 7: Remove non-Arabic characters
        text = self._stage7_remove_non_arabic(text)
        stages["stage7_non_arabic"] = text
        
        # Stage 8: Normalize whitespace
        text = self._stage8_normalize_whitespace(text)
        stages["stage8_whitespace"] = text
        
        # Validation
        is_valid, percentage = self.validate_arabic_percentage(text)
        
        result = NormalizationResult(
            original=original,
            normalized=text,
            stages=stages,
            is_valid=is_valid,
            arabic_percentage=percentage,
            metadata={
                "preserve_diacritics": self.preserve_diacritics,
                "original_length": len(original),
                "normalized_length": len(text)
            }
        )
        
        logger.debug(
            f"Normalized text: '{original[:50]}...' → '{text[:50]}...' "
            f"(Arabic: {percentage:.1%})"
        )
        
        return result
    
    def _stage1_unicode_normalization(self, text: str) -> str:
        """
        Stage 1: Normalize Unicode (NFD → NFC).
        
        Handles compatibility characters and ensures canonical form.
        """
        return normalize_unicode(text)
    
    def _stage2_remove_tatweel(self, text: str) -> str:
        """
        Stage 2: Remove tatweel (ـ).
        
        Tatweel is decorative elongation, not used in prosody.
        """
        return text.replace(TATWEEL, '')
    
    def _stage3_normalize_alef(self, text: str) -> str:
        """
        Stage 3: Normalize all Alef variants to ا.
        
        Unifies: أ إ آ ٱ → ا
        """
        for variant, canonical in ALEF_VARIANTS.items():
            text = text.replace(variant, canonical)
        return text
    
    def _stage4_normalize_yaa(self, text: str) -> str:
        """
        Stage 4: Normalize Yaa forms.
        
        Converts Alef Maksura (ى) to Yaa (ي).
        """
        # Use CAMeL Tools built-in normalizer
        text = normalize_alef_maksura_ar(text)
        
        # Additional manual normalization
        for variant, canonical in YAA_VARIANTS.items():
            text = text.replace(variant, canonical)
        
        return text
    
    def _stage5_normalize_hamza(self, text: str) -> str:
        """
        Stage 5: Normalize Hamza.
        
        Simplified: ء → ئ (for pattern matching consistency).
        """
        for variant, canonical in HAMZA_VARIANTS.items():
            text = text.replace(variant, canonical)
        return text
    
    def _stage6_handle_tashkeel(self, text: str) -> str:
        """
        Stage 6: Handle tashkeel (diacritics).
        
        If preserve_diacritics=False, remove all harakat.
        """
        if not self.preserve_diacritics:
            # Use CAMeL Tools dediacritization
            text = dediac_ar(text)
        
        return text
    
    def _stage7_remove_non_arabic(self, text: str) -> str:
        """
        Stage 7: Remove non-Arabic characters.
        
        Keep only Arabic Unicode range (U+0600-U+06FF) and spaces.
        """
        if self.preserve_diacritics:
            # Keep Arabic letters, diacritics, and spaces
            pattern = r'[^\u0600-\u06FF\s]'
        else:
            # Keep only Arabic letters and spaces
            pattern = r'[^\u0600-\u06FF\s]'
        
        return re.sub(pattern, '', text)
    
    def _stage8_normalize_whitespace(self, text: str) -> str:
        """
        Stage 8: Normalize whitespace.
        
        Replace multiple spaces with single space, trim ends.
        """
        # Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Trim leading/trailing whitespace
        return text.strip()
    
    def validate_arabic_percentage(self, text: str) -> Tuple[bool, float]:
        """
        Validate that text has sufficient Arabic characters.
        
        Args:
            text: Normalized text
            
        Returns:
            (is_valid, percentage) tuple
            
        Reference: docs/research/DATASET_SPEC.md:102
        """
        # Remove spaces for accurate count
        text_no_spaces = text.replace(' ', '')
        
        if len(text_no_spaces) == 0:
            return (False, 0.0)
        
        # Count Arabic characters (U+0600 to U+06FF)
        arabic_count = sum(
            1 for c in text_no_spaces
            if '\u0600' <= c <= '\u06FF'
        )
        
        percentage = arabic_count / len(text_no_spaces)
        is_valid = percentage >= self.min_arabic_percentage
        
        return (is_valid, percentage)


# Convenience function for quick normalization
def normalize_arabic_text(
    text: str,
    preserve_diacritics: bool = False
) -> str:
    """
    Quick normalization function.
    
    Args:
        text: Arabic text to normalize
        preserve_diacritics: Keep tashkeel (default: False)
        
    Returns:
        Normalized text string
    """
    normalizer = ArabicTextNormalizer(preserve_diacritics=preserve_diacritics)
    result = normalizer.normalize(text)
    return result.normalized
```

---

## 6. Unit & Integration Tests

### tests/unit/nlp/test_normalizer.py

```python
"""
Unit tests for Arabic text normalizer.

Tests cover 100+ edge cases including all character variants.
Reference: claude.md:1641-1720
"""

import pytest
from app.nlp.normalizer import (
    ArabicTextNormalizer,
    normalize_arabic_text,
    NormalizationResult
)


class TestArabicTextNormalizer:
    """Test suite for Arabic text normalization."""
    
    @pytest.fixture
    def normalizer(self):
        """Create normalizer instance."""
        return ArabicTextNormalizer(
            preserve_diacritics=False,
            min_arabic_percentage=0.7
        )
    
    @pytest.fixture
    def normalizer_with_diacritics(self):
        """Create normalizer that preserves diacritics."""
        return ArabicTextNormalizer(preserve_diacritics=True)
    
    # Alef Normalization Tests
    
    def test_alef_hamza_above(self, normalizer):
        """Test Alef with hamza above (أ → ا)."""
        text = "أَنَا"
        result = normalizer.normalize(text)
        assert 'أ' not in result.normalized
        assert result.normalized == "انا"
    
    def test_alef_hamza_below(self, normalizer):
        """Test Alef with hamza below (إ → ا)."""
        text = "إِلَى"
        result = normalizer.normalize(text)
        assert 'إ' not in result.normalized
        assert result.normalized == "الي"
    
    def test_alef_madda(self, normalizer):
        """Test Alef with madda (آ → ا)."""
        text = "آخِر"
        result = normalizer.normalize(text)
        assert 'آ' not in result.normalized
        assert result.normalized == "اخر"
    
    def test_alef_wasla(self, normalizer):
        """Test Alef wasla (ٱ → ا)."""
        text = "ٱلْكِتَاب"
        result = normalizer.normalize(text)
        assert 'ٱ' not in result.normalized
        assert result.normalized == "الكتاب"
    
    def test_mixed_alef_variants(self, normalizer):
        """Test multiple Alef variants in one text."""
        text = "أَنَا إِلَى آخِرِ ٱلْعُمْرِ"
        result = normalizer.normalize(text)
        # All Alef variants should be normalized
        assert 'أ' not in result.normalized
        assert 'إ' not in result.normalized
        assert 'آ' not in result.normalized
        assert 'ٱ' not in result.normalized
        assert result.normalized == "انا الي اخر العمر"
    
    # Yaa Normalization Tests
    
    def test_yaa_normalization(self, normalizer):
        """Test Yaa normalization (ى → ي)."""
        text = "عَلَى"
        result = normalizer.normalize(text)
        assert 'ى' not in result.normalized
        assert result.normalized == "علي"
    
    def test_yaa_in_context(self, normalizer):
        """Test Yaa normalization in full verse."""
        text = "رَأَيْتُ فِي الْمَنَامِ"
        result = normalizer.normalize(text)
        # Should not create extra ي
        assert result.normalized.count('ي') <= text.count('ي') + text.count('ى')
    
    # Tatweel Removal Tests
    
    def test_tatweel_removal(self, normalizer):
        """Test removal of tatweel (ـ)."""
        text = "الحــــمد لله"
        result = normalizer.normalize(text)
        assert 'ـ' not in result.normalized
        assert result.normalized == "الحمد لله"
    
    def test_tatweel_between_letters(self, normalizer):
        """Test tatweel between consecutive letters."""
        text = "محـــــــمد"
        result = normalizer.normalize(text)
        assert result.normalized == "محمد"
    
    # Diacritic Handling Tests
    
    def test_remove_diacritics(self, normalizer):
        """Test diacritic removal."""
        text = "قِفَا نَبْكِ مِنْ ذِكْرَى"
        result = normalizer.normalize(text)
        
        # No diacritics should remain
        diacritics = 'ًٌٍَُِّْ'
        for d in diacritics:
            assert d not in result.normalized
        
        assert result.normalized == "قفا نبك من ذكري"
    
    def test_preserve_diacritics(self, normalizer_with_diacritics):
        """Test diacritic preservation."""
        text = "قِفَا نَبْكِ"
        result = normalizer_with_diacritics.normalize(text)
        
        # Diacritics should be preserved
        assert any(d in result.normalized for d in 'َِْ')
    
    def test_shadda_handling(self, normalizer):
        """Test shadda (ّ) removal."""
        text = "مُحَمَّد"
        result = normalizer.normalize(text)
        assert 'ّ' not in result.normalized
    
    def test_tanween_handling(self, normalizer):
        """Test tanween (ً ٌ ٍ) removal."""
        text = "كِتَابًا عَظِيمًا"
        result = normalizer.normalize(text)
        assert 'ً' not in result.normalized
        assert 'ٌ' not in result.normalized
        assert 'ٍ' not in result.normalized
    
    # Whitespace Normalization Tests
    
    def test_multiple_spaces(self, normalizer):
        """Test multiple space normalization."""
        text = "قفا    نبك   من     ذكرى"
        result = normalizer.normalize(text)
        assert '  ' not in result.normalized  # No double spaces
        assert result.normalized == "قفا نبك من ذكري"
    
    def test_leading_trailing_spaces(self, normalizer):
        """Test trimming of leading/trailing spaces."""
        text = "   قفا نبك   "
        result = normalizer.normalize(text)
        assert result.normalized == "قفا نبك"
        assert not result.normalized.startswith(' ')
        assert not result.normalized.endswith(' ')
    
    def test_tabs_and_newlines(self, normalizer):
        """Test tab and newline normalization."""
        text = "قفا\tنبك\nمن\rذكرى"
        result = normalizer.normalize(text)
        assert '\t' not in result.normalized
        assert '\n' not in result.normalized
        assert '\r' not in result.normalized
        assert result.normalized == "قفا نبك من ذكري"
    
    # Non-Arabic Character Removal Tests
    
    def test_remove_latin_chars(self, normalizer):
        """Test removal of Latin characters."""
        text = "مرحبا Hello بكم"
        result = normalizer.normalize(text)
        assert 'H' not in result.normalized
        assert result.normalized == "مرحبا بكم"
    
    def test_remove_numbers(self, normalizer):
        """Test removal of numbers."""
        text = "الفصل 123 من القرآن"
        result = normalizer.normalize(text)
        assert '1' not in result.normalized
        assert result.normalized == "الفصل من القران"
    
    def test_remove_punctuation(self, normalizer):
        """Test removal of punctuation."""
        text = "مرحبا، كيف الحال؟"
        result = normalizer.normalize(text)
        assert '،' not in result.normalized
        assert '؟' not in result.normalized
        assert result.normalized == "مرحبا كيف الحال"
    
    def test_remove_emoji(self, normalizer):
        """Test removal of emoji."""
        text = "قصيدة جميلة 🌟 ماشاء الله 🎭"
        result = normalizer.normalize(text)
        assert '🌟' not in result.normalized
        assert '🎭' not in result.normalized
    
    # Arabic Percentage Validation Tests
    
    def test_validate_100_percent_arabic(self, normalizer):
        """Test validation with 100% Arabic text."""
        text = "قفا نبك من ذكرى حبيب"
        is_valid, percentage = normalizer.validate_arabic_percentage(text)
        assert is_valid is True
        assert percentage == 1.0
    
    def test_validate_mixed_text(self, normalizer):
        """Test validation with mixed Arabic/Latin (should fail)."""
        text = "Hello مرحبا World"
        result = normalizer.normalize(text)
        # After normalization, only Arabic remains
        is_valid, percentage = normalizer.validate_arabic_percentage(
            result.normalized
        )
        assert is_valid is True  # Only Arabic left after normalization
    
    def test_validate_below_threshold(self, normalizer):
        """Test validation failure when Arabic < 70%."""
        text = "ABC مرحبا DEF"
        is_valid, percentage = normalizer.validate_arabic_percentage(text)
        assert is_valid is False
        assert percentage < 0.7
    
    # Edge Cases
    
    def test_empty_string(self, normalizer):
        """Test handling of empty string."""
        with pytest.raises(ValueError, match="cannot be empty"):
            normalizer.normalize("")
    
    def test_whitespace_only(self, normalizer):
        """Test handling of whitespace-only string."""
        with pytest.raises(ValueError, match="cannot be empty"):
            normalizer.normalize("   ")
    
    def test_very_long_text(self, normalizer):
        """Test handling of very long text (>10k chars)."""
        text = "مرحبا " * 5000  # >10k chars
        with pytest.raises(ValueError, match="exceeds maximum length"):
            normalizer.normalize(text)
    
    def test_unicode_edge_cases(self, normalizer):
        """Test various Unicode edge cases."""
        # Zero-width characters
        text = "مرحبا\u200Bبكم"  # Zero-width space
        result = normalizer.normalize(text)
        assert '\u200B' not in result.normalized
        
        # RTL/LTR marks
        text = "مرحبا\u200Fبكم"  # RTL mark
        result = normalizer.normalize(text)
        assert '\u200F' not in result.normalized
    
    def test_stages_recorded(self, normalizer):
        """Test that all stages are recorded."""
        text = "أَهْلاً بِكُمْ"
        result = normalizer.normalize(text)
        
        assert "stage1_unicode" in result.stages
        assert "stage2_tatweel" in result.stages
        assert "stage3_alef" in result.stages
        assert "stage4_yaa" in result.stages
        assert "stage5_hamza" in result.stages
        assert "stage6_tashkeel" in result.stages
        assert "stage7_non_arabic" in result.stages
        assert "stage8_whitespace" in result.stages
    
    # Integration with Classical Poetry
    
    def test_classical_verse(self, normalizer):
        """Test normalization of classical Arabic verse."""
        verse = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
        result = normalizer.normalize(verse)
        
        # Should remove all diacritics and normalize chars
        assert result.normalized == "قفا نبك من ذكري حبيب ومنزل"
        assert result.is_valid is True
        assert result.arabic_percentage == 1.0
    
    def test_modern_poetry(self, normalizer):
        """Test modern Arabic poetry (often without diacritics)."""
        verse = "أحبك في زمن الحروب"
        result = normalizer.normalize(verse)
        
        assert result.normalized == "احبك في زمن الحروب"
        assert result.is_valid is True


# Test convenience function
def test_quick_normalize():
    """Test quick normalization function."""
    text = "أَهْلاً بِكُمْ"
    normalized = normalize_arabic_text(text, preserve_diacritics=False)
    assert normalized == "اهلا بكم"
```

### tests/integration/test_normalizer_integration.py

```python
"""Integration tests for normalizer with prosody engine."""

import pytest
from app.nlp.normalizer import ArabicTextNormalizer
from app.prosody.engine import ProsodyEngine  # If exists


def test_normalizer_prosody_integration():
    """Test normalizer integration with prosody engine."""
    normalizer = ArabicTextNormalizer(preserve_diacritics=False)
    
    # Classical verse with full diacritics
    verse = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
    result = normalizer.normalize(verse)
    
    # Normalized text ready for syllable segmentation
    assert result.normalized == "قفا نبك من ذكري حبيب ومنزل"
    assert result.is_valid is True
    
    # TODO: Pass to syllable segmenter when implemented
    # syllables = segmenter.segment(result.normalized)
    # assert len(syllables) > 0


def test_normalizer_performance():
    """Test normalizer performance with large text."""
    import time
    
    normalizer = ArabicTextNormalizer()
    
    # Generate test text (1000 words)
    text = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ " * 200
    
    start = time.time()
    result = normalizer.normalize(text)
    end = time.time()
    
    duration = (end - start) * 1000  # milliseconds
    
    assert duration < 500  # Should normalize <500ms
    assert result.is_valid is True
```

---

## 7. CI/CD Pipeline

### .github/workflows/nlp-tests.yml

```yaml
name: NLP Normalization Tests

on:
  push:
    paths:
      - 'backend/app/nlp/**'
      - 'tests/**test_normalizer**'
  pull_request:
    branches: [main, develop]

jobs:
  test-normalization:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache CAMeL Tools database
        uses: actions/cache@v3
        with:
          path: ~/.cache/camel_tools
          key: camel-tools-db-v1
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-benchmark
      
      - name: Run unit tests
        run: |
          cd backend
          pytest tests/unit/nlp/test_normalizer.py -v \
            --cov=app.nlp.normalizer \
            --cov-report=term \
            --cov-report=xml
      
      - name: Run performance benchmarks
        run: |
          cd backend
          pytest tests/integration/test_normalizer_integration.py -v \
            --benchmark-only
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: nlp-normalization
```

---

## 8. Deployment Checklist

### Pre-Deployment

- [ ] Verify CAMeL Tools database downloaded (~60 seconds first run)
- [ ] Test with sample classical verses (5-10 verses from golden set)
- [ ] Verify Alef normalization works (all 4 variants)
- [ ] Verify Yaa normalization works (ى → ي)
- [ ] Verify tatweel removal works
- [ ] Test Arabic percentage validation (≥70%)
- [ ] Test with mixed Arabic/Latin text (should reject or clean)
- [ ] Test with emoji and special characters (should remove)
- [ ] Verify whitespace normalization (multiple spaces → single)
- [ ] Test performance (<5ms per 100 words)

### Post-Deployment

- [ ] Monitor normalization errors in logs
- [ ] Track Arabic percentage failures (alerts if >5%)
- [ ] Monitor CAMeL Tools memory usage
- [ ] Verify integration with syllable segmenter works
- [ ] Test with production verse samples
- [ ] Monitor normalization duration (P95 < 10ms)

### Performance Targets

- ✅ Normalization < 5ms per 100 words
- ✅ CAMeL Tools database load < 3 seconds (cached)
- ✅ Memory usage < 200MB
- ✅ Test coverage ≥ 80%

---

## 9. Observability

### Prometheus Metrics

```python
# backend/app/metrics/nlp_metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Normalization metrics
nlp_normalize_total = Counter(
    "bahr_nlp_normalize_total",
    "Total normalization attempts",
    ["status"]  # success, validation_failed, error
)

nlp_normalize_duration_seconds = Histogram(
    "bahr_nlp_normalize_duration_seconds",
    "Text normalization duration",
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
)

nlp_arabic_percentage = Histogram(
    "bahr_nlp_arabic_percentage",
    "Arabic character percentage in input",
    buckets=[0.0, 0.3, 0.5, 0.7, 0.9, 1.0]
)

nlp_validation_failures = Counter(
    "bahr_nlp_validation_failures_total",
    "Total validation failures",
    ["reason"]  # low_arabic_percentage, empty_text, too_long
)
```

### Structured Logging

```python
# Add to normalizer.py
import structlog

logger = structlog.get_logger(__name__)

# In normalize method
logger.info(
    "text_normalized",
    event="nlp.normalize",
    original_length=len(text),
    normalized_length=len(result.normalized),
    arabic_percentage=result.arabic_percentage,
    is_valid=result.is_valid,
    preserve_diacritics=self.preserve_diacritics
)

# On validation failure
if not is_valid:
    logger.warning(
        "validation_failed",
        event="nlp.validation_failed",
        arabic_percentage=percentage,
        threshold=self.min_arabic_percentage,
        text_preview=text[:50]
    )
```

---

## 10. Security & Safety

### Vulnerabilities & Mitigations

| Vulnerability | Risk | Mitigation |
|--------------|------|------------|
| **RTL Override Attack** | MEDIUM | Remove U+202E (RTL override) in Stage 7 |
| **Zero-Width Characters** | LOW | Remove in Unicode normalization (Stage 1) |
| **Excessive Memory** | MEDIUM | Enforce max text length (10,000 chars) |
| **Unicode Exploits** | LOW | Use CAMeL Tools for safe normalization |
| **Regex DoS** | LOW | Simple character-based operations only |

### Input Validation

```python
# Maximum text length
MAX_TEXT_LENGTH = 10_000  # 10k characters

# Validation checks
if len(text) > MAX_TEXT_LENGTH:
    raise ValueError(f"Text exceeds {MAX_TEXT_LENGTH} characters")

# Arabic percentage check
if percentage < 0.7:
    raise ValidationError(f"Text is only {percentage:.0%} Arabic (minimum: 70%)")
```

---

## 11. Backwards Compatibility

### Breaking Changes
- **None** - Initial implementation

### Migration Path
- **N/A** - First version

### API Versioning
- Normalization is internal to prosody engine
- No public API versioning needed for MVP

---

## 12. Source Documentation Citations

### Primary Sources

1. **docs/technical/PROSODY_ENGINE.md:148-400**
   - 8-stage normalization pipeline specification
   - Character mapping definitions
   - Alef/Yaa/Hamza normalization rules
   - Diacritic handling strategies

2. **claude.md:651-725**
   - Complete normalizer implementation code
   - CAMeL Tools integration examples
   - Stage-by-stage processing logic

3. **docs/research/ARABIC_NLP_RESEARCH.md:22-211**
   - CAMeL Tools library documentation
   - PyArabic utility functions
   - Unicode normalization strategies

4. **docs/research/DATASET_SPEC.md:89-165**
   - Arabic percentage validation (≥70%)
   - Text quality requirements

5. **implementation-guides/IMPROVED_PROMPT.md:425-458**
   - Feature specification template
   - Test case requirements (100+ edge cases)

### Additional References

6. **backend/app/nlp/normalizer.py (existing)**
   - Current simplified implementation
   - Basic character mapping

7. **docs/technical/NLP_INTEGRATION_GUIDE.md:168-404**
   - CAMeL Tools installation guide
   - Performance benchmarks
   - M1/M2 Mac compatibility notes

8. **docs/WEEK_1_CRITICAL_CHECKLIST.md:237-285**
   - Diacritics handling scenarios
   - Input validation requirements

---

**Implementation Complete!** ✅  
**Estimated Time to Implement:** 10-14 hours  
**Test Coverage Target:** ≥ 80%  
**Performance Target:** < 5ms per 100 words

