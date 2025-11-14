"""
Unit tests for Arabic text normalization.
"""

import pytest
from app.core.normalization import (
    remove_diacritics,
    normalize_hamza,
    normalize_alef,
    remove_tatweel,
    normalize_whitespace,
    normalize_arabic_text,
    has_diacritics,
)


class TestRemoveDiacritics:
    """Test removal of all Arabic diacritical marks."""

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

    def test_removes_all_diacritics(self):
        text = "إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ"
        result = remove_diacritics(text)
        assert not has_diacritics(result)

    def test_preserves_arabic_letters(self):
        text = "الشعر العربي"
        assert remove_diacritics(text) == text

    def test_empty_string(self):
        assert remove_diacritics("") == ""


class TestNormalizeHamza:
    """Test normalization of all hamza variants."""

    def test_normalizes_hamza_on_alef(self):
        assert normalize_hamza("أحمد") == "احمد"
        assert normalize_hamza("إبراهيم") == "ابراهيم"
        assert normalize_hamza("آمن") == "امن"

    def test_normalizes_hamza_on_waw(self):
        assert normalize_hamza("مؤمن") == "مومن"

    def test_normalizes_hamza_on_ya(self):
        assert normalize_hamza("شيئ") == "شيي"

    def test_normalizes_multiple_hamzas(self):
        text = "أأنت إنسان"
        result = normalize_hamza(text)
        assert "أ" not in result
        assert "إ" not in result

    def test_preserves_non_hamza_text(self):
        text = "محمد علي"
        assert normalize_hamza(text) == text


class TestNormalizeAlef:
    """Test normalization of alef variants."""

    def test_normalizes_alef_maksura(self):
        assert normalize_alef("على") == "علي"
        assert normalize_alef("موسى") == "موسي"

    def test_normalizes_alef_variants(self):
        assert normalize_alef("أحمد") == "احمد"
        assert normalize_alef("إبراهيم") == "ابراهيم"
        assert normalize_alef("آمن") == "امن"

    def test_normalizes_mixed_alef_variants(self):
        text = "على إبراهيم موسى"
        result = normalize_alef(text)
        assert "ى" not in result
        assert "أ" not in result
        assert "إ" not in result
        assert "آ" not in result

    def test_preserves_regular_ya(self):
        text = "يوم جميل"
        assert normalize_alef(text) == text


class TestRemoveTatweel:
    """Test removal of tatweel (kashida) character."""

    def test_removes_tatweel(self):
        assert remove_tatweel("مـــرحـــبـــا") == "مرحبا"

    def test_handles_no_tatweel(self):
        text = "مرحبا"
        assert remove_tatweel(text) == text

    def test_removes_multiple_tatweels(self):
        text = "الـــسلام عــلــيـــكـم"
        result = remove_tatweel(text)
        assert "\u0640" not in result

    def test_empty_string(self):
        assert remove_tatweel("") == ""


class TestNormalizeWhitespace:
    """Test whitespace normalization."""

    def test_replaces_multiple_spaces(self):
        assert normalize_whitespace("مرحبا    بك") == "مرحبا بك"

    def test_strips_leading_whitespace(self):
        assert normalize_whitespace("   مرحبا") == "مرحبا"

    def test_strips_trailing_whitespace(self):
        assert normalize_whitespace("مرحبا   ") == "مرحبا"

    def test_replaces_tabs_and_newlines(self):
        result = normalize_whitespace("مرحبا\t\nبك\n\nأهلا")
        assert result == "مرحبا بك أهلا"

    def test_handles_already_normalized(self):
        text = "مرحبا بك"
        assert normalize_whitespace(text) == text


class TestNormalizeArabicText:
    """Test main normalization function."""

    def test_basic_normalization(self):
        result = normalize_arabic_text("إِذَا غَامَرْتَ")
        assert "ا" in result  # Hamza normalized

    def test_with_tashkeel_removal(self):
        result = normalize_arabic_text("مَرْحَبًا", remove_tashkeel=True)
        assert not has_diacritics(result)
        assert result == "مرحبا"

    def test_preserves_tashkeel_by_default(self):
        text = "مَرْحَبًا"
        result = normalize_arabic_text(text, remove_tashkeel=False)
        assert has_diacritics(result)

    def test_raises_on_empty_text(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            normalize_arabic_text("")

    def test_raises_on_whitespace_only(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            normalize_arabic_text("   \n\t  ")

    def test_raises_on_non_arabic(self):
        with pytest.raises(ValueError, match="must contain Arabic"):
            normalize_arabic_text("Hello World")

    def test_normalizes_whitespace(self):
        result = normalize_arabic_text("مرحبا    بك   \n  أهلا")
        assert "  " not in result
        assert result.count(" ") == 2

    def test_removes_tatweel(self):
        result = normalize_arabic_text("مـــرحـــبـــا")
        assert "\u0640" not in result

    def test_normalizes_hamza_by_default(self):
        result = normalize_arabic_text("أحمد", normalize_hamzas=True)
        assert "أ" not in result
        assert "ا" in result

    def test_skip_hamza_normalization(self):
        # When normalize_hamzas=False, hamza should be preserved
        # But note: normalize_alef also affects hamza on alef, so we need to skip both
        result = normalize_arabic_text("أحمد", normalize_hamzas=False, normalize_alefs=False)
        assert "أ" in result

    def test_normalizes_alef_by_default(self):
        result = normalize_arabic_text("على", normalize_alefs=True)
        assert "ى" not in result
        assert "ي" in result

    def test_skip_alef_normalization(self):
        result = normalize_arabic_text("على", normalize_alefs=False)
        assert "ى" in result

    def test_complete_normalization(self):
        text = "إِذَا   غَامَرْتَ  فِي شَـــرَفٍ مَرُومِ"
        result = normalize_arabic_text(
            text,
            remove_tashkeel=True,
            normalize_hamzas=True,
            normalize_alefs=True
        )
        # Should have no diacritics, normalized hamza/alef, no tatweel, normalized whitespace
        assert not has_diacritics(result)
        assert "  " not in result
        assert "\u0640" not in result
        assert "إ" not in result

    def test_mixed_arabic_and_numbers(self):
        # Should work - contains Arabic characters
        result = normalize_arabic_text("الفصل 123")
        assert "الفصل" in result
        assert "123" in result

    def test_already_normalized_text(self):
        text = "الشعر العربي"
        result = normalize_arabic_text(text)
        assert result == text


class TestHasDiacritics:
    """Test diacritical marks detection."""

    def test_detects_fatha(self):
        assert has_diacritics("مَرحبا") == True

    def test_detects_damma(self):
        assert has_diacritics("مُحمد") == True

    def test_detects_kasra(self):
        assert has_diacritics("بِسم") == True

    def test_detects_shadda(self):
        assert has_diacritics("مُحَمَّد") == True

    def test_detects_sukun(self):
        assert has_diacritics("مَرْحبا") == True

    def test_detects_tanween(self):
        assert has_diacritics("شُكْرًا") == True

    def test_no_diacritics(self):
        assert has_diacritics("مرحبا") == False

    def test_empty_string(self):
        assert has_diacritics("") == False

    def test_mixed_text(self):
        assert has_diacritics("مَرحبا بك") == True


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_normalize_none_as_text(self):
        # Passing None should raise ValueError with specific message
        with pytest.raises(ValueError, match="cannot be None"):
            normalize_arabic_text(None)

    def test_very_long_text(self):
        # Test with long text
        long_text = "الشعر العربي " * 1000
        result = normalize_arabic_text(long_text)
        assert len(result) > 0

    def test_special_arabic_characters(self):
        # Test with special Arabic punctuation
        text = "مرحبا، كيف حالك؟"
        result = normalize_arabic_text(text)
        assert "،" in result
        assert "؟" in result

    def test_mixed_rtl_ltr(self):
        # Arabic with English - contains Arabic so should pass
        # The validation only checks if there's at least one Arabic character
        result = normalize_arabic_text("مرحبا Hello")
        assert "مرحبا" in result
        assert "Hello" in result

    def test_only_numbers(self):
        # Only numbers - should fail
        with pytest.raises(ValueError, match="must contain Arabic"):
            normalize_arabic_text("123456")

    def test_only_punctuation(self):
        # Only punctuation - should fail
        with pytest.raises(ValueError, match="must contain Arabic"):
            normalize_arabic_text(".,!?")
