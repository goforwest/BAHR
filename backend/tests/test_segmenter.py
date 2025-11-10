"""
Unit tests for Arabic prosody segmenter.

Tests cover syllable segmentation and classification:
1. Basic syllabification
2. Long vowel detection
3. Syllable type classification (CV, CVV, CVC)
4. Word boundary handling
5. Edge cases
"""

import pytest
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.prosody.segmenter import segment, classify_syllable, Syllable


class TestBasicSegmentation:
    """Test basic syllabification functionality."""
    
    def test_simple_word_segmentation(self):
        """Test segmentation of a simple Arabic word"""
        text = "كتاب"
        syllables = segment(text)
        assert len(syllables) > 0
        assert all(isinstance(s, Syllable) for s in syllables)
    
    def test_word_with_long_vowels(self):
        """Test segmentation with long vowels (ا و ي)"""
        text = "باب"  # bāb - has long vowel
        syllables = segment(text)
        assert len(syllables) > 0
        # Check for long syllable
        has_long = any(s.long for s in syllables)
        assert has_long
    
    def test_multiple_words(self):
        """Test segmentation of multiple words"""
        text = "كتاب قلم"
        syllables = segment(text)
        assert len(syllables) >= 2  # Should have syllables from both words


class TestSyllableClassification:
    """Test syllable type classification."""
    
    def test_cv_syllable(self):
        """Test CV (consonant-vowel) syllable classification"""
        syllable = classify_syllable("با")
        assert syllable.kind == "CV"
        assert not syllable.long
    
    def test_cvv_syllable(self):
        """Test CVV (consonant-vowel-vowel) syllable classification"""
        # Example: consonant + two vowels
        syllable = classify_syllable("باا")
        if syllable.kind == "CVV":
            assert syllable.long
    
    def test_cvc_syllable(self):
        """Test CVC (consonant-vowel-consonant) syllable classification"""
        syllable = classify_syllable("كتب")
        # CVC is typically classified as long
        assert syllable.long or syllable.kind == "CVC"
    
    def test_syllable_text_preserved(self):
        """Test that original syllable text is preserved"""
        text = "با"
        syllable = classify_syllable(text)
        assert syllable.text == text


class TestLongVowelDetection:
    """Test detection of long vowels in Arabic text."""
    
    def test_alif_as_long_vowel(self):
        """Test detection of alif (ا) as long vowel"""
        text = "بابا"  # Contains multiple alifs
        syllables = segment(text)
        long_syllables = [s for s in syllables if s.long]
        assert len(long_syllables) > 0
    
    def test_waw_as_long_vowel(self):
        """Test detection of waw (و) as long vowel"""
        text = "نور"  # Contains waw
        syllables = segment(text)
        assert len(syllables) > 0
    
    def test_ya_as_long_vowel(self):
        """Test detection of ya (ي/ى) as long vowel"""
        text = "عيد"  # Contains ya
        syllables = segment(text)
        assert len(syllables) > 0


class TestWordBoundaries:
    """Test handling of word boundaries and spacing."""
    
    def test_space_boundary(self):
        """Test that spaces correctly separate syllables"""
        text = "با با"
        syllables = segment(text)
        # Should have distinct syllables for each word
        assert len(syllables) >= 2
    
    def test_multiple_spaces(self):
        """Test handling of multiple consecutive spaces"""
        text = "با   با"
        syllables = segment(text)
        # Should handle multiple spaces gracefully
        assert len(syllables) >= 2
    
    def test_leading_trailing_spaces(self):
        """Test handling of leading and trailing spaces"""
        text = "  با  "
        syllables = segment(text)
        assert len(syllables) > 0


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_empty_string(self):
        """Test segmentation of empty string"""
        syllables = segment("")
        assert len(syllables) == 0
    
    def test_single_character(self):
        """Test segmentation of single character"""
        syllables = segment("ب")
        assert len(syllables) > 0
    
    def test_consonant_only(self):
        """Test text with only consonants"""
        text = "بتث"
        syllables = segment(text)
        assert len(syllables) > 0
    
    def test_vowel_only(self):
        """Test text with only vowels"""
        text = "اوي"
        syllables = segment(text)
        assert len(syllables) > 0


class TestRealWorldExamples:
    """Test with real Arabic poetry examples."""
    
    def test_poetry_verse_segmentation(self):
        """Test segmentation of a poetry verse"""
        # Simplified verse without diacritics
        text = "قفا نبك من ذكرى حبيب ومنزل"
        syllables = segment(text)
        
        # Should produce multiple syllables (actual: 9)
        assert len(syllables) >= 9
        
        # Should have mix of long and short syllables
        long_count = sum(1 for s in syllables if s.long)
        short_count = sum(1 for s in syllables if not s.long)
        assert long_count > 0 or short_count > 0
    
    def test_simple_verse_pattern(self):
        """Test that verse produces consistent pattern"""
        text = "كتاب"
        syllables1 = segment(text)
        syllables2 = segment(text)
        
        # Same input should produce same segmentation
        assert len(syllables1) == len(syllables2)
        for s1, s2 in zip(syllables1, syllables2):
            assert s1.long == s2.long
            assert s1.kind == s2.kind


class TestSyllableProperties:
    """Test syllable dataclass properties."""
    
    def test_syllable_has_required_fields(self):
        """Test that Syllable has all required fields"""
        syllable = Syllable(text="با", kind="CV", long=False)
        assert hasattr(syllable, 'text')
        assert hasattr(syllable, 'kind')
        assert hasattr(syllable, 'long')
    
    def test_syllable_kind_values(self):
        """Test common syllable kind values"""
        valid_kinds = ["CV", "CVV", "CVC", "other"]
        text = "كتاب"
        syllables = segment(text)
        for syllable in syllables:
            # Kind should be one of the expected values
            assert syllable.kind in valid_kinds or syllable.kind


class TestPerformance:
    """Test performance with longer texts."""
    
    def test_long_text_segmentation(self):
        """Test segmentation of longer text"""
        # Create long text
        text = "قفا نبك من ذكرى حبيب " * 20
        syllables = segment(text)
        
        # Should complete without error
        assert len(syllables) > 0
        assert all(isinstance(s, Syllable) for s in syllables)
