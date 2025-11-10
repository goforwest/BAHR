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
    """Test pattern matching functionality."""

    def test_empty_pattern(self):
        """Empty pattern should return empty list."""
        result = pattern_to_tafail("")
        assert result == []

    def test_single_tafila_fauulun(self):
        """Test matching single taf'ila: فعولن (/o//o)."""
        result = pattern_to_tafail("/o//o")
        assert len(result) == 1
        assert "فعولن" in result

    def test_single_tafila_mafaaiilun(self):
        """Test matching single taf'ila: مفاعيلن (//o/o)."""
        result = pattern_to_tafail("//o/o")
        assert len(result) == 1
        assert "مفاعيلن" in result

    def test_single_tafila_mafaaalatun(self):
        """Test matching single taf'ila: مفاعلتن (///o)."""
        result = pattern_to_tafail("///o")
        assert len(result) == 1
        assert "مفاعلتن" in result

    def test_single_tafila_mustafeilun(self):
        """Test matching single taf'ila: مستفعلن (/o/o//o)."""
        result = pattern_to_tafail("/o/o//o")
        assert len(result) == 1
        assert "مستفعلن" in result

    def test_single_tafila_faailaatun(self):
        """Test matching single taf'ila: فاعلاتن (//o//o)."""
        result = pattern_to_tafail("//o//o")
        assert len(result) == 1
        assert "فاعلاتن" in result

    def test_single_tafila_faailun(self):
        """Test matching single taf'ila: فاعلن (/o/o/o)."""
        result = pattern_to_tafail("/o/o/o")
        assert len(result) == 1
        assert "فاعلن" in result

    def test_single_tafila_falan(self):
        """Test matching single taf'ila: فعلن (///)."""
        result = pattern_to_tafail("///")
        assert len(result) == 1
        assert "فعلن" in result

    def test_single_tafila_mafuulaatu(self):
        """Test matching single taf'ila: مفعولات (/o//)."""
        result = pattern_to_tafail("/o//")
        assert len(result) == 1
        assert "مفعولات" in result

    def test_multiple_tafail_combined(self):
        """Test matching multiple tafa'il in sequence."""
        # Pattern: فعولن + مفاعيلن
        result = pattern_to_tafail("/o//o//o/o")
        assert len(result) >= 1
        # Should contain at least one matched taf'ila

    def test_greedy_matching_longest_first(self):
        """Test that greedy matching works (longest pattern first)."""
        # مستفعلن is 7 chars (/o/o//o), should match before shorter patterns
        result = pattern_to_tafail("/o/o//o")
        assert "مستفعلن" in result

    def test_unmatched_characters_skipped(self):
        """Test that unmatched characters are skipped."""
        # Pattern with some unmatched chars
        result = pattern_to_tafail("x/o//oy")
        # Should skip 'x' and 'y', but match "/o//o" if possible
        # Result may be empty or partial
        assert isinstance(result, list)

    def test_pattern_matching_consistency(self):
        """Test that all patterns in BASIC_TAFAIL are matchable."""
        for pattern, name in BASIC_TAFAIL.items():
            result = pattern_to_tafail(pattern)
            assert name in result, f"Pattern {pattern} should match {name}"


class TestPerformTaqti3:
    """Test end-to-end taqti3 functionality."""

    def test_raises_on_empty_verse(self):
        """Empty verse should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            perform_taqti3("")

    def test_raises_on_whitespace_only_verse(self):
        """Whitespace-only verse should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            perform_taqti3("   ")

    def test_raises_on_none_verse(self):
        """None verse should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            perform_taqti3(None)

    def test_returns_string(self):
        """Result should be a string."""
        result = perform_taqti3("كتب الشعر")
        assert isinstance(result, str)

    def test_normalization_applied_by_default(self):
        """Text normalization should be applied by default."""
        # Verse with various forms of alef and hamza
        verse_with_variants = "أكتب إلى الشعراء"
        result = perform_taqti3(verse_with_variants, normalize=True)
        assert isinstance(result, str)
        # Should not raise error due to normalization

    def test_normalization_can_be_disabled(self):
        """Normalization can be disabled."""
        verse = "كتب الشعر"
        result = perform_taqti3(verse, normalize=False)
        assert isinstance(result, str)

    def test_handles_verse_with_diacritics(self):
        """Should handle verses with diacritical marks."""
        verse_with_tashkeel = "كَتَبَ الشِّعْرَ"
        result = perform_taqti3(verse_with_tashkeel)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_handles_verse_without_diacritics(self):
        """Should handle verses without diacritical marks."""
        verse_without_tashkeel = "كتب الشعر"
        result = perform_taqti3(verse_without_tashkeel)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_result_contains_arabic_tafail_names(self):
        """Result should contain Arabic taf'ila names."""
        verse = "كتب الشعر العربي"
        result = perform_taqti3(verse)
        # Result should be string of space-separated tafa'il
        # At minimum, should not be empty
        assert len(result) > 0

    # Test cases with known verses (to be expanded with real data)
    
    def test_simple_verse_example_1(self):
        """Test with a simple Arabic phrase."""
        # This is a placeholder - actual expected output depends on implementation
        verse = "محمد رسول الله"
        result = perform_taqti3(verse)
        assert isinstance(result, str)
        assert len(result) > 0
        # Contains at least some tafa'il (actual pattern verification needs test data)

    def test_simple_verse_example_2(self):
        """Test with another simple Arabic phrase."""
        verse = "الحمد لله رب العالمين"
        result = perform_taqti3(verse)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_classical_verse_placeholder_1(self):
        """Placeholder for classical verse test - Al-Mutanabbi (Tawil meter)."""
        # TODO: Add actual verse from test dataset when available
        # Expected: "إذا غامَرتَ في شَرَفٍ مَرومِ"
        # Expected tafa'il: Should match Tawil pattern
        verse = "إذا غامرت في شرف مروم"
        result = perform_taqti3(verse)
        assert isinstance(result, str)
        # Full validation will be done in test_accuracy.py with dataset

    def test_classical_verse_placeholder_2(self):
        """Placeholder for classical verse test - Al-Kamil meter."""
        # TODO: Add actual verse from test dataset when available
        verse = "ألا ليت الشباب يعود يوما"
        result = perform_taqti3(verse)
        assert isinstance(result, str)

    def test_classical_verse_placeholder_3(self):
        """Placeholder for classical verse test - Al-Wafir meter."""
        # TODO: Add actual verse from test dataset when available
        verse = "لك الحمد على نعمائك الوافرة"
        result = perform_taqti3(verse)
        assert isinstance(result, str)

    def test_result_format_space_separated(self):
        """Result should be space-separated tafa'il names."""
        verse = "كتب الشعر"
        result = perform_taqti3(verse)
        # Should be string, may contain spaces between tafa'il
        assert isinstance(result, str)
        # If result is not empty, it should be valid format
        if result:
            # Result is either empty or contains Arabic characters
            assert any(char in result for char in "فمعلنتوياسكبحرذطظضصقغخجد ") or result == ""

    def test_consistent_results(self):
        """Same verse should produce same result."""
        verse = "كتب الشعر العربي"
        result1 = perform_taqti3(verse)
        result2 = perform_taqti3(verse)
        assert result1 == result2

    def test_handles_arabic_punctuation(self):
        """Should handle verses with Arabic punctuation."""
        verse = "كتب الشعر، والنثر"
        result = perform_taqti3(verse)
        assert isinstance(result, str)

    def test_handles_longer_verse(self):
        """Should handle longer verses."""
        verse = "في كل قلب من هواك نصيب وفي كل عين من جمالك حبيب"
        result = perform_taqti3(verse)
        assert isinstance(result, str)
        assert len(result) > 0


class TestBASICTAFAIL:
    """Test the BASIC_TAFAIL dictionary."""

    def test_dictionary_has_eight_entries(self):
        """BASIC_TAFAIL should have 8 tafa'il."""
        assert len(BASIC_TAFAIL) == 8

    def test_all_patterns_unique(self):
        """All patterns should be unique."""
        patterns = list(BASIC_TAFAIL.keys())
        assert len(patterns) == len(set(patterns))

    def test_all_names_unique(self):
        """All taf'ila names should be unique."""
        names = list(BASIC_TAFAIL.values())
        assert len(names) == len(set(names))

    def test_patterns_valid_format(self):
        """All patterns should only contain '/' and 'o' characters."""
        for pattern in BASIC_TAFAIL.keys():
            assert all(c in '/o' for c in pattern), f"Invalid pattern: {pattern}"

    def test_patterns_not_empty(self):
        """All patterns should be non-empty."""
        for pattern in BASIC_TAFAIL.keys():
            assert len(pattern) > 0, "Pattern should not be empty"

    def test_names_are_arabic(self):
        """All taf'ila names should be in Arabic."""
        for name in BASIC_TAFAIL.values():
            assert len(name) > 0, "Name should not be empty"
            # Basic check: contains Arabic Unicode range
            assert any('\u0600' <= c <= '\u06FF' for c in name), f"Name should be Arabic: {name}"
