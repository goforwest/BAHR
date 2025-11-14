"""
Unit tests for quality assessment module.
"""

import pytest
from app.core.quality import (
    QualityAnalyzer,
    QualityScore,
    ProsodyError,
    ErrorSeverity,
    analyze_verse_quality
)


class TestQualityScore:
    """Test QualityScore dataclass."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        score = QualityScore(
            overall=95.5,
            meter_accuracy=98.0,
            pattern_consistency=92.0,
            length_score=95.0,
            completeness=100.0
        )
        
        result = score.to_dict()
        
        assert result["overall"] == 95.5
        assert result["breakdown"]["meter_accuracy"] == 98.0
        assert result["breakdown"]["pattern_consistency"] == 92.0
        assert result["breakdown"]["length_appropriateness"] == 95.0
        assert result["breakdown"]["completeness"] == 100.0


class TestProsodyError:
    """Test ProsodyError dataclass."""
    
    def test_to_dict_with_suggestion(self):
        """Test conversion to dictionary with suggestion."""
        error = ProsodyError(
            type="low_confidence",
            severity=ErrorSeverity.MAJOR,
            position=5,
            message_ar="رسالة بالعربية",
            message_en="English message",
            suggestion_ar="اقتراح بالعربية",
            suggestion_en="English suggestion"
        )
        
        result = error.to_dict()
        
        assert result["type"] == "low_confidence"
        assert result["severity"] == "major"
        assert result["position"] == 5
        assert result["message"]["ar"] == "رسالة بالعربية"
        assert result["message"]["en"] == "English message"
        assert result["suggestion"]["ar"] == "اقتراح بالعربية"
        assert result["suggestion"]["en"] == "English suggestion"
    
    def test_to_dict_without_suggestion(self):
        """Test conversion to dictionary without suggestion."""
        error = ProsodyError(
            type="no_meter",
            severity=ErrorSeverity.CRITICAL,
            position=None,
            message_ar="لا بحر",
            message_en="No meter"
        )
        
        result = error.to_dict()
        
        assert result["suggestion"] is None


class TestQualityAnalyzer:
    """Test QualityAnalyzer class."""
    
    @pytest.fixture
    def analyzer(self):
        """Create QualityAnalyzer instance."""
        return QualityAnalyzer()
    
    def test_calculate_quality_score_perfect(self, analyzer):
        """Test quality score calculation for perfect verse."""
        score = analyzer.calculate_quality_score(
            verse_text="إذا غامرت في شرف مروم فلا تقنع بما دون النجوم",
            taqti3_result="فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن",
            bahr_id=1,  # الطويل
            meter_confidence=0.98,
            detected_pattern="/o//o//o/o/o//o/o",
            expected_pattern="/o//o//o/o/o//o/o"
        )
        
        assert score.overall >= 90.0
        assert score.meter_accuracy >= 95.0
        assert score.pattern_consistency >= 95.0
    
    def test_calculate_quality_score_no_meter(self, analyzer):
        """Test quality score when no meter detected."""
        score = analyzer.calculate_quality_score(
            verse_text="نص عشوائي بدون وزن",
            taqti3_result="غير محدد",
            bahr_id=None,
            meter_confidence=0.0,
            detected_pattern="///o/o",
            expected_pattern=""
        )
        
        assert score.meter_accuracy == 0.0
        assert score.overall < 50.0
    
    def test_calculate_pattern_consistency_identical(self, analyzer):
        """Test pattern consistency with identical patterns."""
        consistency = analyzer._calculate_pattern_consistency(
            detected_pattern="/o//o/o//o",
            expected_pattern="/o//o/o//o"
        )
        
        assert consistency == 100.0
    
    def test_calculate_pattern_consistency_similar(self, analyzer):
        """Test pattern consistency with similar patterns."""
        consistency = analyzer._calculate_pattern_consistency(
            detected_pattern="/o//o/o//o",
            expected_pattern="/o//o/o/o"
        )
        
        assert 70.0 <= consistency < 100.0
    
    def test_calculate_pattern_consistency_different(self, analyzer):
        """Test pattern consistency with different patterns."""
        consistency = analyzer._calculate_pattern_consistency(
            detected_pattern="/o//o",
            expected_pattern="///o//o///o"
        )
        
        assert consistency < 70.0
    
    def test_calculate_length_score_exact_match(self, analyzer):
        """Test length score with exact tafila count."""
        score = analyzer._calculate_length_score(
            verse_text="إذا غامرت في شرف مروم فلا تقنع بما دون النجوم",
            taqti3_result="فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن",
            bahr_id=1  # الطويل expects 8 tafa'il
        )
        
        assert score == 100.0
    
    def test_calculate_length_score_missing_tafila(self, analyzer):
        """Test length score with missing tafila."""
        score = analyzer._calculate_length_score(
            verse_text="إذا غامرت في شرف مروم",
            taqti3_result="فعولن مفاعيلن فعولن",  # Only 3 tafa'il
            bahr_id=1  # الطويل expects 8
        )
        
        assert score < 100.0
        assert score >= 0.0
    
    def test_calculate_completeness_score_ideal(self, analyzer):
        """Test completeness score for ideal verse length."""
        score = analyzer._calculate_completeness_score(
            "إذا غامرت في شرف مروم فلا تقنع بما دون النجوم"
        )
        
        assert score == 100.0
    
    def test_calculate_completeness_score_short(self, analyzer):
        """Test completeness score for short verse."""
        score = analyzer._calculate_completeness_score("كلمة واحدة")
        
        assert score < 100.0
    
    def test_calculate_completeness_score_long(self, analyzer):
        """Test completeness score for very long verse."""
        long_verse = " ".join(["كلمة"] * 30)
        score = analyzer._calculate_completeness_score(long_verse)
        
        assert score < 100.0
    
    def test_detect_errors_perfect_verse(self, analyzer):
        """Test error detection for perfect verse."""
        errors = analyzer.detect_errors(
            verse_text="إذا غامرت في شرف مروم فلا تقنع بما دون النجوم",
            taqti3_result="فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن",
            bahr_id=1,
            meter_confidence=0.98,
            phonetic_pattern="/o//o//o/o"
        )
        
        # Should have no critical or major errors
        critical_errors = [e for e in errors if e.severity == ErrorSeverity.CRITICAL]
        assert len(critical_errors) == 0
    
    def test_detect_errors_no_meter(self, analyzer):
        """Test error detection when no meter detected."""
        errors = analyzer.detect_errors(
            verse_text="نص عشوائي",
            taqti3_result="غير محدد",
            bahr_id=None,
            meter_confidence=0.0,
            phonetic_pattern="//o"
        )
        
        # Should detect "no_meter" error
        error_types = [e.type for e in errors]
        assert "no_meter" in error_types
        
        # Should be critical severity
        no_meter_error = next(e for e in errors if e.type == "no_meter")
        assert no_meter_error.severity == ErrorSeverity.CRITICAL
    
    def test_detect_errors_low_confidence(self, analyzer):
        """Test error detection for low confidence meter."""
        errors = analyzer.detect_errors(
            verse_text="إذا غامرت في شرف مروم",
            taqti3_result="فعولن مفاعيلن فعولن مفاعيلن",
            bahr_id=1,
            meter_confidence=0.65,  # Low confidence
            phonetic_pattern="/o//o"
        )
        
        # Should detect low_confidence error
        error_types = [e.type for e in errors]
        assert "low_confidence" in error_types
    
    def test_detect_errors_incomplete_verse(self, analyzer):
        """Test error detection for incomplete verse (too short)."""
        errors = analyzer.detect_errors(
            verse_text="كلمة قصيرة",  # Only 2 words
            taqti3_result="فعولن",
            bahr_id=1,
            meter_confidence=0.8,
            phonetic_pattern="/o//o"
        )
        
        # Should detect incomplete_verse error
        error_types = [e.type for e in errors]
        assert "incomplete_verse" in error_types
    
    def test_detect_errors_verse_too_long(self, analyzer):
        """Test error detection for verse that's too long."""
        long_verse = " ".join(["كلمة"] * 30)
        errors = analyzer.detect_errors(
            verse_text=long_verse,
            taqti3_result="فعولن " * 15,
            bahr_id=1,
            meter_confidence=0.8,
            phonetic_pattern="/o//o"
        )
        
        # Should detect verse_too_long error
        error_types = [e.type for e in errors]
        assert "verse_too_long" in error_types
    
    def test_detect_errors_missing_tafila(self, analyzer):
        """Test error detection for missing tafa'il."""
        errors = analyzer.detect_errors(
            verse_text="إذا غامرت في شرف مروم",
            taqti3_result="فعولن مفاعيلن",  # Only 2 tafa'il (expects 8 for الطويل)
            bahr_id=1,
            meter_confidence=0.8,
            phonetic_pattern="/o//o"
        )
        
        # Should detect missing_tafila error
        error_types = [e.type for e in errors]
        assert "missing_tafila" in error_types
    
    def test_detect_errors_extra_tafila(self, analyzer):
        """Test error detection for extra tafa'il."""
        errors = analyzer.detect_errors(
            verse_text="بيت طويل جداً",
            taqti3_result="فعولن مفاعيلن " * 6,  # 12 tafa'il (expects 8 for الطويل)
            bahr_id=1,
            meter_confidence=0.8,
            phonetic_pattern="/o//o"
        )
        
        # Should detect extra_tafila error
        error_types = [e.type for e in errors]
        assert "extra_tafila" in error_types
    
    def test_detect_errors_taqti3_failed(self, analyzer):
        """Test error detection when taqti3 fails."""
        errors = analyzer.detect_errors(
            verse_text="نص",
            taqti3_result="",  # Empty taqti3 result
            bahr_id=None,
            meter_confidence=0.0,
            phonetic_pattern=""
        )
        
        # Should detect taqti3_failed error
        error_types = [e.type for e in errors]
        assert "taqti3_failed" in error_types
        
        # Should be critical severity
        taqti3_error = next(e for e in errors if e.type == "taqti3_failed")
        assert taqti3_error.severity == ErrorSeverity.CRITICAL
    
    def test_generate_suggestions_excellent(self, analyzer):
        """Test suggestion generation for excellent verse."""
        score = QualityScore(
            overall=96.0,
            meter_accuracy=98.0,
            pattern_consistency=95.0,
            length_score=100.0,
            completeness=100.0
        )
        
        suggestions = analyzer.generate_suggestions(
            verse_text="إذا غامرت في شرف مروم فلا تقنع بما دون النجوم",
            quality_score=score,
            errors=[],
            meter_confidence=0.98,
            bahr_name_ar="الطويل"
        )
        
        assert len(suggestions) > 0
        assert any("ممتاز" in s for s in suggestions)
        assert any("الطويل" in s for s in suggestions)
    
    def test_generate_suggestions_good(self, analyzer):
        """Test suggestion generation for good verse."""
        score = QualityScore(
            overall=88.0,
            meter_accuracy=90.0,
            pattern_consistency=85.0,
            length_score=90.0,
            completeness=100.0
        )
        
        suggestions = analyzer.generate_suggestions(
            verse_text="بيت شعر جيد",
            quality_score=score,
            errors=[],
            meter_confidence=0.90,
            bahr_name_ar="الكامل"
        )
        
        assert len(suggestions) > 0
        assert any("جيد" in s for s in suggestions)
    
    def test_generate_suggestions_needs_improvement(self, analyzer):
        """Test suggestion generation for verse needing improvement."""
        score = QualityScore(
            overall=60.0,
            meter_accuracy=65.0,
            pattern_consistency=55.0,
            length_score=60.0,
            completeness=60.0
        )
        
        suggestions = analyzer.generate_suggestions(
            verse_text="بيت يحتاج تحسين",
            quality_score=score,
            errors=[],
            meter_confidence=0.65,
            bahr_name_ar="الرمل"
        )
        
        assert len(suggestions) > 0
        assert any("مراجعة" in s or "اتساق" in s for s in suggestions)
    
    def test_generate_suggestions_with_errors(self, analyzer):
        """Test suggestion generation with errors present."""
        score = QualityScore(
            overall=45.0,
            meter_accuracy=50.0,
            pattern_consistency=40.0,
            length_score=45.0,
            completeness=40.0
        )
        
        error = ProsodyError(
            type="low_confidence",
            severity=ErrorSeverity.CRITICAL,
            position=None,
            message_ar="خطأ حرج",
            message_en="Critical error",
            suggestion_ar="إصلاح فوري",
            suggestion_en="Immediate fix"
        )
        
        suggestions = analyzer.generate_suggestions(
            verse_text="بيت به أخطاء",
            quality_score=score,
            errors=[error],
            meter_confidence=0.50,
            bahr_name_ar=None
        )
        
        assert len(suggestions) > 0
        assert any("إصلاح" in s for s in suggestions)
    
    def test_generate_suggestions_max_five(self, analyzer):
        """Test that suggestions are limited to 5."""
        score = QualityScore(
            overall=30.0,
            meter_accuracy=20.0,
            pattern_consistency=30.0,
            length_score=40.0,
            completeness=30.0
        )
        
        # Create multiple errors
        errors = [
            ProsodyError(
                type=f"error_{i}",
                severity=ErrorSeverity.CRITICAL,
                position=None,
                message_ar=f"خطأ {i}",
                message_en=f"Error {i}",
                suggestion_ar=f"اقتراح {i}",
                suggestion_en=f"Suggestion {i}"
            )
            for i in range(10)
        ]
        
        suggestions = analyzer.generate_suggestions(
            verse_text="بيت",
            quality_score=score,
            errors=errors,
            meter_confidence=0.20,
            bahr_name_ar=None
        )
        
        assert len(suggestions) <= 5


class TestAnalyzeVerseQuality:
    """Test the convenience function analyze_verse_quality."""
    
    def test_analyze_verse_quality_complete(self):
        """Test complete verse quality analysis."""
        score, errors, suggestions = analyze_verse_quality(
            verse_text="إذا غامرت في شرف مروم فلا تقنع بما دون النجوم",
            taqti3_result="فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن فعولن مفاعيلن",
            bahr_id=1,
            bahr_name_ar="الطويل",
            meter_confidence=0.98,
            detected_pattern="/o//o//o/o",
            expected_pattern="/o//o//o/o"
        )
        
        # Check score
        assert isinstance(score, QualityScore)
        assert score.overall >= 90.0
        
        # Check errors
        assert isinstance(errors, list)
        # Should have minimal errors for good verse
        critical_errors = [e for e in errors if e.severity == ErrorSeverity.CRITICAL]
        assert len(critical_errors) == 0
        
        # Check suggestions
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert any("الطويل" in s for s in suggestions)
    
    def test_analyze_verse_quality_poor(self):
        """Test verse quality analysis for poor verse."""
        score, errors, suggestions = analyze_verse_quality(
            verse_text="نص قصير",
            taqti3_result="فعولن",
            bahr_id=None,
            bahr_name_ar=None,
            meter_confidence=0.0,
            detected_pattern="/o",
            expected_pattern=""
        )
        
        # Check score
        assert score.overall < 50.0
        
        # Check errors
        assert len(errors) > 0
        error_types = [e.type for e in errors]
        assert "no_meter" in error_types or "incomplete_verse" in error_types
        
        # Check suggestions
        assert len(suggestions) > 0
        assert any("مراجعة" in s or "تحسين" in s for s in suggestions)
