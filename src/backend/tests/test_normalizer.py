"""
Unit tests for Arabic text normalizer.

Tests cover Week 1-2 MVP normalization pipeline:
1. Diacritics removal
2. Character mapping (Alif variants, ta marbuta)
3. Punctuation removal
4. Whitespace normalization
"""

import pytest
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.nlp.normalizer import ArabicNormalizer, basic_normalize


class TestDiacriticsRemoval:
    """Test diacritics (tashkeel) removal functionality."""
    
    def test_remove_fatha_damma_kasra(self):
        """Test removal of basic diacritics"""
        normalizer = ArabicNormalizer(remove_diacritics=True)
        input_text = "مَرْحَبًا بِكُمْ"
        expected = "مرحبا بكم"
        assert normalizer.normalize(input_text) == expected
    
    def test_remove_shadda(self):
        """Test removal of shadda (doubling mark)"""
        normalizer = ArabicNormalizer(remove_diacritics=True)
        input_text = "الشَّعْر"
        expected = "الشعر"
        assert normalizer.normalize(input_text) == expected
    
    def test_remove_tanween(self):
        """Test removal of tanween (nunation)"""
        normalizer = ArabicNormalizer(remove_diacritics=True)
        input_text = "شِعْرٌ جَمِيلٌ"
        expected = "شعر جميل"
        assert normalizer.normalize(input_text) == expected
    
    def test_keep_diacritics_when_disabled(self):
        """Test that diacritics are kept when remove_diacritics=False"""
        normalizer = ArabicNormalizer(remove_diacritics=False)
        input_text = "مَرْحَبًا"
        # Should still normalize whitespace and punctuation but keep diacritics
        result = normalizer.normalize(input_text)
        assert "َ" in result or "ْ" in result or "ً" in result


class TestCharacterMapping:
    """Test character normalization (Alif variants, etc.)."""
    
    def test_alif_hamza_above(self):
        """Test normalization of Alif with hamza above (أ)"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("أحمد") == "احمد"
    
    def test_alif_hamza_below(self):
        """Test normalization of Alif with hamza below (إ)"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("إنسان") == "انسان"
    
    def test_alif_madda(self):
        """Test normalization of Alif with madda (آ)"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("آمن") == "امن"
    
    def test_ta_marbuta_to_ha(self):
        """Test conversion of ta marbuta (ة) to ha (ه)"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("مدرسة") == "مدرسه"
    
    def test_mixed_alif_variants(self):
        """Test text with multiple Alif variants"""
        normalizer = ArabicNormalizer()
        input_text = "أإآابب"
        expected = "اااابب"  # آ is a single character mapped to single ا
        assert normalizer.normalize(input_text) == expected


class TestPunctuationRemoval:
    """Test punctuation and special character removal."""
    
    def test_arabic_comma(self):
        """Test removal of Arabic comma (،)"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("كتاب، قلم") == "كتاب قلم"
    
    def test_arabic_question_mark(self):
        """Test removal of Arabic question mark (؟)"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("كيف حالك؟") == "كيف حالك"
    
    def test_mixed_punctuation(self):
        """Test removal of mixed Arabic and English punctuation"""
        normalizer = ArabicNormalizer()
        input_text = "نص: (مثال)، \"اقتباس\"... !؟"
        result = normalizer.normalize(input_text)
        # Should remove all punctuation
        for punct in ":()\",\"...!؟":
            assert punct not in result
    
    def test_brackets_and_quotes(self):
        """Test removal of brackets and quotation marks"""
        normalizer = ArabicNormalizer()
        input_text = "[نص] {آخر} «مقتبس»"
        result = normalizer.normalize(input_text)
        assert "[" not in result and "{" not in result and "«" not in result


class TestWhitespaceNormalization:
    """Test whitespace normalization."""
    
    def test_multiple_spaces(self):
        """Test collapsing multiple spaces to single space"""
        normalizer = ArabicNormalizer()
        # Hamza on alif (أ) and ta marbuta (ة) are normalized
        assert normalizer.normalize("كلمة     أخرى") == "كلمه اخرى"
    
    def test_leading_trailing_spaces(self):
        """Test removal of leading and trailing spaces"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("  نص  ") == "نص"
    
    def test_newlines_and_tabs(self):
        """Test conversion of newlines and tabs to spaces"""
        normalizer = ArabicNormalizer()
        input_text = "سطر\nأول\tثاني"
        result = normalizer.normalize(input_text)
        assert "\n" not in result and "\t" not in result
        # Hamza on alif (أ) is normalized to plain alif (ا)
        assert result == "سطر اول ثاني"


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_empty_string(self):
        """Test normalization of empty string"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("") == ""
    
    def test_whitespace_only(self):
        """Test normalization of whitespace-only string"""
        normalizer = ArabicNormalizer()
        assert normalizer.normalize("   \n\t  ") == ""
    
    def test_numbers_preserved(self):
        """Test that numbers are preserved"""
        normalizer = ArabicNormalizer()
        result = normalizer.normalize("123 ٤٥٦")
        assert "123" in result
        # Arabic digits might be kept or need normalization - verify current behavior
    
    def test_mixed_arabic_english(self):
        """Test mixed Arabic and English text"""
        normalizer = ArabicNormalizer()
        input_text = "Hello مرحبا World عالم"
        result = normalizer.normalize(input_text)
        assert "Hello" in result and "مرحبا" in result


class TestBasicNormalizeFunction:
    """Test the convenience function basic_normalize()."""
    
    def test_basic_normalize_with_diacritics(self):
        """Test basic_normalize with default remove_diacritics=True"""
        result = basic_normalize("مَرْحَبًا")
        assert result == "مرحبا"
    
    def test_basic_normalize_keep_diacritics(self):
        """Test basic_normalize with remove_diacritics=False"""
        result = basic_normalize("مَرْحَبًا", remove_diacritics=False)
        # Should keep some diacritics
        assert len(result) > len("مرحبا")
    
    def test_basic_normalize_comprehensive(self):
        """Test basic_normalize with complex input"""
        input_text = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
        result = basic_normalize(input_text)
        # Should remove diacritics and normalize
        assert "ِ" not in result and "َ" not in result and "ْ" not in result


class TestIntegration:
    """Integration tests with real poetry examples."""
    
    def test_poetry_verse_normalization(self):
        """Test normalization of a classical poetry verse"""
        # Imru' al-Qais verse (with diacritics)
        input_verse = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
        normalizer = ArabicNormalizer()
        result = normalizer.normalize(input_verse)
        
        # Verify:
        # 1. No diacritics
        assert "ِ" not in result and "َ" not in result
        # 2. Whitespace normalized
        assert "  " not in result
        # 3. Has expected words
        assert "قفا" in result and "نبك" in result
    
    def test_normalization_preserves_meaning(self):
        """Test that normalization preserves essential characters"""
        input_text = "الشِّعْرُ العَرَبِيُّ"
        normalizer = ArabicNormalizer()
        result = normalizer.normalize(input_text)
        
        # Should have essential consonants
        assert "ش" in result and "ع" in result and "ر" in result


# Performance and stress tests
class TestPerformance:
    """Test performance with larger texts."""
    
    def test_long_text_normalization(self):
        """Test normalization of longer text"""
        # Create a long text by repeating a verse
        verse = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ "
        long_text = verse * 100
        
        normalizer = ArabicNormalizer()
        result = normalizer.normalize(long_text)
        
        # Should complete without error
        assert len(result) > 0
        assert "ِ" not in result  # No diacritics
