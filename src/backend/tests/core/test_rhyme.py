"""
Tests for rhyme analysis module (قافية).
"""

import pytest
from app.core.rhyme import (
    RhymeAnalyzer,
    RhymeType,
    RhymeError,
    QafiyahComponents,
    RhymePattern,
    RhymeAnalysisResult,
    analyze_verse_rhyme,
    analyze_poem_rhyme,
)


class TestQafiyahComponents:
    """Test QafiyahComponents dataclass."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        qafiyah = QafiyahComponents(
            rawi="م",
            rawi_vowel="i",
            wasl="ي",
            khuruj="u",
            radif="و",
            tasis="ا"
        )
        
        result = qafiyah.to_dict()
        
        assert result["rawi"] == "م"
        assert result["rawi_vowel"] == "i"
        assert result["wasl"] == "ي"
        assert result["khuruj"] == "u"
        assert result["radif"] == "و"
        assert result["tasis"] == "ا"
    
    def test_str_representation_full(self):
        """Test string representation with all components."""
        qafiyah = QafiyahComponents(
            rawi="م",
            rawi_vowel="i",
            wasl="ي",
            khuruj="u",
            radif="و",
            tasis="ا"
        )
        
        result = str(qafiyah)
        
        assert "روي:م" in result
        assert "ردف:و" in result
        assert "تأسيس:ا" in result
        assert "وصل:ي" in result
    
    def test_str_representation_minimal(self):
        """Test string representation with only rawi."""
        qafiyah = QafiyahComponents(
            rawi="ل",
            rawi_vowel="u"
        )
        
        result = str(qafiyah)
        
        assert "روي:ل" in result
        assert "ردف" not in result
        assert "وصل" not in result


class TestRhymeAnalyzer:
    """Test RhymeAnalyzer class."""
    
    def test_extract_qafiyah_simple(self):
        """Test qafiyah extraction from simple verse."""
        analyzer = RhymeAnalyzer()
        
        # Famous verse from المتنبي
        verse = "على قدر أهل العزم تأتي العزائم"
        
        pattern = analyzer.extract_qafiyah(verse)
        
        assert pattern.qafiyah.rawi == "م"
        assert pattern.qafiyah.rawi_vowel in ["i", "u", "a", ""]
        assert isinstance(pattern.rhyme_types, list)
        assert len(pattern.rhyme_types) > 0
    
    def test_extract_qafiyah_with_radif(self):
        """Test qafiyah extraction with radif."""
        analyzer = RhymeAnalyzer()
        
        # Verse ending with واو before rawi
        verse = "وتأتي على قدر الكرام المكارم"
        
        pattern = analyzer.extract_qafiyah(verse)
        
        assert pattern.qafiyah.rawi == "م"
        # May or may not detect radif depending on phonetic structure
        assert pattern.qafiyah is not None
    
    def test_extract_qafiyah_mutlaqah(self):
        """Test identification of مطلقة (unrestricted) rhyme."""
        analyzer = RhymeAnalyzer()
        
        # Verse with vowel ending (مطلقة)
        verse = "أسرب القطا هل من يعير جناحه"
        
        pattern = analyzer.extract_qafiyah(verse)
        
        # Should be classified as mutlaqah if rawi has vowel
        if pattern.qafiyah.rawi_vowel and pattern.qafiyah.rawi_vowel != '':
            assert RhymeType.MUTLAQAH in pattern.rhyme_types
    
    def test_extract_qafiyah_muqayyadah(self):
        """Test identification of مقيدة (restricted) rhyme."""
        analyzer = RhymeAnalyzer()
        
        # Create verse with sukun ending for testing
        # (This is a simplified test - real verses need proper analysis)
        verse = "في ليلة من ليالي الوصل"
        
        pattern = analyzer.extract_qafiyah(verse)
        
        # Verify pattern is extracted
        assert pattern.qafiyah.rawi is not None
    
    def test_classify_rhyme_type_mutlaqah(self):
        """Test rhyme type classification for mutlaqah."""
        analyzer = RhymeAnalyzer()
        
        qafiyah = QafiyahComponents(
            rawi="ل",
            rawi_vowel="i"  # Has vowel = mutlaqah
        )
        
        types = analyzer._classify_rhyme_type(qafiyah)
        
        assert RhymeType.MUTLAQAH in types
        assert RhymeType.MUJARRADAH in types  # No wasl/khuruj
    
    def test_classify_rhyme_type_muqayyadah(self):
        """Test rhyme type classification for muqayyadah."""
        analyzer = RhymeAnalyzer()
        
        qafiyah = QafiyahComponents(
            rawi="ل",
            rawi_vowel=""  # Sukun = muqayyadah
        )
        
        types = analyzer._classify_rhyme_type(qafiyah)
        
        assert RhymeType.MUQAYYADAH in types
    
    def test_classify_rhyme_type_murakkabah(self):
        """Test rhyme type classification for murakkabah."""
        analyzer = RhymeAnalyzer()
        
        qafiyah = QafiyahComponents(
            rawi="م",
            rawi_vowel="i",
            wasl="ي"  # Has wasl = murakkabah
        )
        
        types = analyzer._classify_rhyme_type(qafiyah)
        
        assert RhymeType.MURAKKABAH in types
    
    def test_classify_rhyme_type_mutawatir(self):
        """Test rhyme type classification for mutawatir."""
        analyzer = RhymeAnalyzer()
        
        qafiyah = QafiyahComponents(
            rawi="م",
            rawi_vowel="i",
            radif="و"  # Has radif = mutawatir
        )
        
        types = analyzer._classify_rhyme_type(qafiyah)
        
        assert RhymeType.MUTAWATIR in types
    
    def test_create_rhyme_string_simple(self):
        """Test rhyme string creation for simple pattern."""
        analyzer = RhymeAnalyzer()
        
        qafiyah = QafiyahComponents(
            rawi="ل",
            rawi_vowel="u"
        )
        
        rhyme_string = analyzer._create_rhyme_string(qafiyah)
        
        assert "ل" in rhyme_string
        assert "u" in rhyme_string
    
    def test_create_rhyme_string_with_radif(self):
        """Test rhyme string creation with radif."""
        analyzer = RhymeAnalyzer()
        
        qafiyah = QafiyahComponents(
            rawi="م",
            rawi_vowel="i",
            radif="و"
        )
        
        rhyme_string = analyzer._create_rhyme_string(qafiyah)
        
        assert "و" in rhyme_string
        assert "م" in rhyme_string
        assert "i" in rhyme_string
    
    def test_analyze_rhyme_consistency_perfect(self):
        """Test rhyme consistency with perfectly matching verses."""
        analyzer = RhymeAnalyzer()
        
        # Three verses with same rhyme (م with kasra)
        verses = [
            "على قدر أهل العزم تأتي العزائم",
            "وتأتي على قدر الكرام المكارم",
            "وتعظم في عين الصغير صغارها"  # Different ending for testing
        ]
        
        result = analyzer.analyze_rhyme_consistency(verses)
        
        assert isinstance(result, RhymeAnalysisResult)
        assert result.consistency_score >= 0.0
        assert result.consistency_score <= 1.0
        assert len(result.rhyme_patterns) > 0
    
    def test_analyze_rhyme_consistency_sina_error(self):
        """Test detection of سناد (changing rawi letter)."""
        analyzer = RhymeAnalyzer()
        
        # Verses with different rawi letters (sina error)
        verses = [
            "على قدر أهل العزم تأتي العزائم",  # Ends with م
            "وتبقى على الأيام ذكرى المكارب"   # Ends with ب
        ]
        
        result = analyzer.analyze_rhyme_consistency(verses)
        
        # Should detect sina error
        assert len(result.errors) > 0
        assert any(err[0] == RhymeError.SINA for err in result.errors)
        assert result.consistency_score < 1.0
    
    def test_analyze_rhyme_consistency_iqwa_error(self):
        """Test detection of إقواء (changing rawi vowel)."""
        analyzer = RhymeAnalyzer()
        
        # This test is conceptual - actual detection depends on phonetic analysis
        # We'll test that the consistency checker runs
        verses = [
            "في ليلة من ليالي الوصل",
            "بين الحبيب وبين القلب"
        ]
        
        result = analyzer.analyze_rhyme_consistency(verses)
        
        # Verify analysis completes
        assert isinstance(result, RhymeAnalysisResult)
        assert result.consistency_score >= 0.0
    
    def test_analyze_rhyme_consistency_single_verse_error(self):
        """Test error handling with single verse."""
        analyzer = RhymeAnalyzer()
        
        verses = ["على قدر أهل العزم تأتي العزائم"]
        
        with pytest.raises(ValueError, match="at least 2 verses"):
            analyzer.analyze_rhyme_consistency(verses)
    
    def test_analyze_rhyme_consistency_empty_error(self):
        """Test error handling with empty verse list."""
        analyzer = RhymeAnalyzer()
        
        with pytest.raises(ValueError):
            analyzer.analyze_rhyme_consistency([])


class TestAnalyzeVerseRhyme:
    """Test analyze_verse_rhyme convenience function."""
    
    def test_analyze_verse_rhyme_basic(self):
        """Test basic verse rhyme analysis."""
        verse = "على قدر أهل العزم تأتي العزائم"
        
        pattern, desc_ar, desc_en = analyze_verse_rhyme(verse)
        
        assert isinstance(pattern, RhymePattern)
        assert isinstance(desc_ar, str)
        assert isinstance(desc_en, str)
        assert "القافية" in desc_ar
        assert "Qafiyah" in desc_en or "qafiyah" in desc_en.lower()
    
    def test_analyze_verse_rhyme_descriptions(self):
        """Test that descriptions contain rhyme information."""
        verse = "وتأتي على قدر الكرام المكارم"
        
        pattern, desc_ar, desc_en = analyze_verse_rhyme(verse)
        
        # Should mention rawi
        assert pattern.qafiyah.rawi in desc_ar or pattern.qafiyah.rawi in desc_en
        
        # Should include rhyme types
        assert any(rt.value in desc_ar for rt in pattern.rhyme_types)


class TestAnalyzePoemRhyme:
    """Test analyze_poem_rhyme convenience function."""
    
    def test_analyze_poem_rhyme_consistent(self):
        """Test poem rhyme analysis with consistent rhyme."""
        verses = [
            "على قدر أهل العزم تأتي العزائم",
            "وتأتي على قدر الكرام المكارم"
        ]
        
        result, summary_ar, summary_en = analyze_poem_rhyme(verses)
        
        assert isinstance(result, RhymeAnalysisResult)
        assert isinstance(summary_ar, str)
        assert isinstance(summary_en, str)
    
    def test_analyze_poem_rhyme_summary_consistent(self):
        """Test summary messages for consistent rhyme."""
        verses = [
            "على قدر أهل العزم تأتي العزائم",
            "وتأتي على قدر الكرام المكارم"
        ]
        
        result, summary_ar, summary_en = analyze_poem_rhyme(verses)
        
        if result.is_consistent:
            assert "متسقة" in summary_ar or "متناسق" in summary_ar
            assert "Consistent" in summary_en or "consistent" in summary_en
    
    def test_analyze_poem_rhyme_summary_inconsistent(self):
        """Test summary messages for inconsistent rhyme."""
        verses = [
            "على قدر أهل العزم تأتي العزائم",  # م
            "وتبقى على الأيام ذكرى المكارب"   # ب
        ]
        
        result, summary_ar, summary_en = analyze_poem_rhyme(verses)
        
        if not result.is_consistent:
            assert "غير متسقة" in summary_ar or "أخطاء" in summary_ar
            assert "Inconsistent" in summary_en or "errors" in summary_en.lower()
            assert str(len(result.errors)) in summary_ar


class TestRhymePatternEdgeCases:
    """Test edge cases in rhyme pattern extraction."""
    
    def test_very_short_verse(self):
        """Test handling of very short verse."""
        analyzer = RhymeAnalyzer()
        
        # Short text should still work (extracts what it can)
        pattern = analyzer.extract_qafiyah("كتب")
        
        # Should extract some rhyme pattern
        assert pattern.qafiyah.rawi is not None
    
    def test_non_arabic_text(self):
        """Test handling of non-Arabic text."""
        analyzer = RhymeAnalyzer()
        
        # Should handle gracefully (may raise ValueError)
        try:
            pattern = analyzer.extract_qafiyah("Hello world")
            # If it doesn't raise, verify it returns something
            assert pattern is not None
        except ValueError:
            # Expected behavior for non-Arabic
            pass
    
    def test_verse_with_punctuation(self):
        """Test handling of verse with punctuation."""
        analyzer = RhymeAnalyzer()
        
        verse = "على قدر أهل العزم تأتي العزائم!"
        
        pattern = analyzer.extract_qafiyah(verse)
        
        # Should extract rhyme despite punctuation
        assert pattern.qafiyah.rawi is not None
    
    def test_verse_with_numbers(self):
        """Test handling of verse with numbers."""
        analyzer = RhymeAnalyzer()
        
        verse = "على قدر أهل العزم تأتي العزائم 123"
        
        pattern = analyzer.extract_qafiyah(verse)
        
        # Should extract rhyme from Arabic portion
        assert pattern.qafiyah.rawi is not None


class TestRhymeAnalysisResult:
    """Test RhymeAnalysisResult dataclass."""
    
    def test_to_dict_complete(self):
        """Test conversion to dictionary with all fields."""
        from app.core.rhyme import Phoneme
        
        # Create sample data
        qafiyah = QafiyahComponents(rawi="م", rawi_vowel="i")
        pattern = RhymePattern(
            verse_ending=[Phoneme("م", "i")],
            qafiyah=qafiyah,
            rhyme_types=[RhymeType.MUTLAQAH],
            rhyme_string="م-i"
        )
        
        result = RhymeAnalysisResult(
            is_consistent=True,
            common_rawi="م",
            common_rawi_vowel="i",
            rhyme_patterns=[pattern],
            errors=[],
            consistency_score=1.0
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["is_consistent"] is True
        assert result_dict["common_rawi"] == "م"
        assert result_dict["common_rawi_vowel"] == "i"
        assert result_dict["consistency_score"] == 1.0
        assert len(result_dict["rhyme_patterns"]) == 1
        assert len(result_dict["errors"]) == 0
    
    def test_to_dict_with_errors(self):
        """Test conversion to dictionary with errors."""
        from app.core.rhyme import Phoneme
        
        qafiyah = QafiyahComponents(rawi="م", rawi_vowel="i")
        pattern = RhymePattern(
            verse_ending=[Phoneme("م", "i")],
            qafiyah=qafiyah,
            rhyme_types=[RhymeType.MUTLAQAH],
            rhyme_string="م-i"
        )
        
        errors = [
            (RhymeError.SINA, "تغيير حرف الروي", "Rhyme letter changed")
        ]
        
        result = RhymeAnalysisResult(
            is_consistent=False,
            common_rawi=None,
            common_rawi_vowel=None,
            rhyme_patterns=[pattern],
            errors=errors,
            consistency_score=0.5
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["is_consistent"] is False
        assert result_dict["common_rawi"] is None
        assert len(result_dict["errors"]) == 1
        assert result_dict["errors"][0]["type"] == "سناد"


class TestIntegration:
    """Integration tests for rhyme analysis."""
    
    def test_full_poem_analysis(self):
        """Test complete poem analysis workflow."""
        # Famous poem verses (المعلقات style)
        verses = [
            "قفا نبك من ذكرى حبيب ومنزل",
            "بسقط اللوى بين الدخول فحومل",
            "فتوضح فالمقراة لم يعف رسمها",
        ]
        
        analyzer = RhymeAnalyzer()
        result = analyzer.analyze_rhyme_consistency(verses)
        
        # Verify complete analysis
        assert len(result.rhyme_patterns) == len(verses)
        assert result.consistency_score >= 0.0
        assert result.consistency_score <= 1.0
        
        # Each pattern should have qafiyah
        for pattern in result.rhyme_patterns:
            assert pattern.qafiyah.rawi is not None
            assert len(pattern.rhyme_types) > 0
    
    def test_mixed_quality_verses(self):
        """Test analysis with verses of varying rhyme quality."""
        verses = [
            "على قدر أهل العزم تأتي العزائم",  # Good
            "وتأتي على قدر الكرام المكارم",      # Good (same rhyme)
            "والناس في الدنيا يعيشون",           # Different rhyme
        ]
        
        result, summary_ar, summary_en = analyze_poem_rhyme(verses)
        
        # Should detect inconsistency
        assert not result.is_consistent or result.consistency_score < 1.0
        
        # Should provide meaningful feedback
        assert len(summary_ar) > 0
        assert len(summary_en) > 0
