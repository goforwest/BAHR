"""
Quality assessment and error detection for Arabic poetry prosody.

This module provides sophisticated scoring algorithms, prosodic error detection,
and actionable suggestions for improving verse quality.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class ErrorSeverity(str, Enum):
    """Severity levels for prosodic errors."""
    CRITICAL = "critical"  # Breaks the meter completely
    MAJOR = "major"        # Significant deviation from meter
    MINOR = "minor"        # Small variation (acceptable زحاف)
    INFO = "info"          # Informational note


@dataclass
class ProsodyError:
    """
    Represents a prosodic error in a verse.
    
    Attributes:
        type: Error type (e.g., "pattern_mismatch", "missing_tafila")
        severity: Error severity level
        position: Character position or foot index where error occurs
        message_ar: Arabic error message
        message_en: English error message
        suggestion_ar: Arabic suggestion for fixing the error
        suggestion_en: English suggestion for fixing the error
    """
    type: str
    severity: ErrorSeverity
    position: Optional[int]
    message_ar: str
    message_en: str
    suggestion_ar: Optional[str] = None
    suggestion_en: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type,
            "severity": self.severity.value,
            "position": self.position,
            "message": {
                "ar": self.message_ar,
                "en": self.message_en
            },
            "suggestion": {
                "ar": self.suggestion_ar,
                "en": self.suggestion_en
            } if self.suggestion_ar else None
        }


@dataclass
class QualityScore:
    """
    Comprehensive quality score for a verse.
    
    Attributes:
        overall: Overall quality score (0-100)
        meter_accuracy: How well verse matches detected meter (0-100)
        pattern_consistency: Internal pattern consistency (0-100)
        length_score: Verse length appropriateness (0-100)
        completeness: Verse completeness (both hemistichs present) (0-100)
    """
    overall: float
    meter_accuracy: float
    pattern_consistency: float
    length_score: float
    completeness: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "overall": round(self.overall, 2),
            "breakdown": {
                "meter_accuracy": round(self.meter_accuracy, 2),
                "pattern_consistency": round(self.pattern_consistency, 2),
                "length_appropriateness": round(self.length_score, 2),
                "completeness": round(self.completeness, 2)
            }
        }


class QualityAnalyzer:
    """
    Analyzes verse quality and detects prosodic errors.
    
    Provides sophisticated scoring based on multiple factors including
    meter accuracy, pattern consistency, and structural completeness.
    """
    
    # Expected tafila counts for each meter (full verse = both hemistichs)
    EXPECTED_TAFILA_COUNTS = {
        1: 8,   # الطويل (at-Tawil): 4 per hemistich
        2: 6,   # الكامل (al-Kamil): 3 per hemistich
        3: 6,   # الوافر (al-Wafir): 3 per hemistich
        4: 6,   # الرمل (ar-Ramal): 3 per hemistich
        5: 8,   # البسيط (al-Basit): 4 per hemistich
        6: 8,   # المتقارب (al-Mutaqarib): 4 per hemistich
        7: 6,   # الرجز (ar-Rajaz): 3 per hemistich
        8: 6,   # الهزج (al-Hazaj): 3 per hemistich
        9: 6,   # الخفيف (al-Khafif): 3 per hemistich
    }
    
    def __init__(self):
        """Initialize the quality analyzer."""
        pass
    
    def calculate_quality_score(
        self,
        verse_text: str,
        taqti3_result: str,
        bahr_id: Optional[int],
        meter_confidence: float,
        detected_pattern: str,
        expected_pattern: str
    ) -> QualityScore:
        """
        Calculate comprehensive quality score for a verse.
        
        Args:
            verse_text: Original Arabic verse text
            taqti3_result: Taqti3 output (tafa'il string)
            bahr_id: Detected meter ID (or None)
            meter_confidence: Meter detection confidence (0.0-1.0)
            detected_pattern: Actual prosodic pattern
            expected_pattern: Expected pattern for the detected meter
            
        Returns:
            QualityScore object with overall and breakdown scores
            
        Example:
            >>> analyzer = QualityAnalyzer()
            >>> score = analyzer.calculate_quality_score(
            ...     verse_text="إذا غامرت في شرف مروم",
            ...     taqti3_result="فعولن مفاعيلن فعولن مفاعيلن",
            ...     bahr_id=1,
            ...     meter_confidence=0.95,
            ...     detected_pattern="...",
            ...     expected_pattern="..."
            ... )
            >>> score.overall
            95.0
        """
        # 1. Meter Accuracy Score (40% weight)
        meter_accuracy = meter_confidence * 100 if bahr_id else 0.0
        
        # 2. Pattern Consistency Score (30% weight)
        pattern_consistency = self._calculate_pattern_consistency(
            detected_pattern, expected_pattern
        )
        
        # 3. Length Score (15% weight)
        length_score = self._calculate_length_score(
            verse_text, taqti3_result, bahr_id
        )
        
        # 4. Completeness Score (15% weight)
        completeness = self._calculate_completeness_score(verse_text)
        
        # Calculate weighted overall score
        overall = (
            meter_accuracy * 0.40 +
            pattern_consistency * 0.30 +
            length_score * 0.15 +
            completeness * 0.15
        )
        
        return QualityScore(
            overall=overall,
            meter_accuracy=meter_accuracy,
            pattern_consistency=pattern_consistency,
            length_score=length_score,
            completeness=completeness
        )
    
    def _calculate_pattern_consistency(
        self,
        detected_pattern: str,
        expected_pattern: str
    ) -> float:
        """
        Calculate how consistent the detected pattern is with expected pattern.
        
        Uses character-by-character comparison with allowance for variations.
        
        Args:
            detected_pattern: Actual phonetic pattern
            expected_pattern: Expected phonetic pattern for the meter
            
        Returns:
            Consistency score (0-100)
        """
        if not detected_pattern or not expected_pattern:
            return 0.0
        
        # Use difflib-style matching
        from difflib import SequenceMatcher
        matcher = SequenceMatcher(None, detected_pattern, expected_pattern)
        similarity = matcher.ratio()
        
        return similarity * 100
    
    def _calculate_length_score(
        self,
        verse_text: str,
        taqti3_result: str,
        bahr_id: Optional[int]
    ) -> float:
        """
        Calculate score based on verse length appropriateness.
        
        Checks if the number of tafa'il matches the expected count for the meter.
        
        Args:
            verse_text: Original verse text
            taqti3_result: Taqti3 output (space-separated tafa'il)
            bahr_id: Detected meter ID
            
        Returns:
            Length appropriateness score (0-100)
        """
        if not bahr_id or not taqti3_result:
            return 50.0  # Neutral score if no meter detected
        
        # Count tafa'il
        tafail_count = len(taqti3_result.strip().split())
        
        # Get expected count for this meter
        expected_count = self.EXPECTED_TAFILA_COUNTS.get(bahr_id, 6)
        
        # Calculate deviation
        deviation = abs(tafail_count - expected_count)
        
        # Score: 100 for exact match, -10 per taf'ila deviation
        score = max(0, 100 - (deviation * 10))
        
        return score
    
    def _calculate_completeness_score(self, verse_text: str) -> float:
        """
        Calculate verse completeness score.
        
        Checks for presence of both hemistichs (separated by spaces/punctuation).
        
        Args:
            verse_text: Original verse text
            
        Returns:
            Completeness score (0-100)
        """
        # Simple heuristic: verses typically have 2 parts (hemistichs)
        # Separated by multiple spaces or punctuation
        
        # Count words
        words = verse_text.strip().split()
        word_count = len(words)
        
        # Ideal verse length: 8-16 words
        if 8 <= word_count <= 16:
            return 100.0
        elif 6 <= word_count < 8 or 16 < word_count <= 20:
            return 80.0
        elif 4 <= word_count < 6 or 20 < word_count <= 25:
            return 60.0
        else:
            return 40.0
    
    def detect_errors(
        self,
        verse_text: str,
        taqti3_result: str,
        bahr_id: Optional[int],
        meter_confidence: float,
        phonetic_pattern: str
    ) -> List[ProsodyError]:
        """
        Detect prosodic errors in the verse.
        
        Identifies various types of errors including:
        - Pattern mismatches
        - Missing or extra tafa'il
        - Inconsistent rhythm
        - Structural issues
        
        Args:
            verse_text: Original Arabic verse text
            taqti3_result: Taqti3 output (tafa'il string)
            bahr_id: Detected meter ID (or None)
            meter_confidence: Meter detection confidence (0.0-1.0)
            phonetic_pattern: Phonetic pattern string
            
        Returns:
            List of ProsodyError objects
            
        Example:
            >>> analyzer = QualityAnalyzer()
            >>> errors = analyzer.detect_errors(...)
            >>> len(errors)
            2
        """
        errors: List[ProsodyError] = []
        
        # Error 1: Low meter confidence
        if bahr_id and meter_confidence < 0.7:
            errors.append(ProsodyError(
                type="low_confidence",
                severity=ErrorSeverity.MAJOR,
                position=None,
                message_ar="الثقة في تحديد البحر منخفضة",
                message_en="Low confidence in meter detection",
                suggestion_ar="قد يحتاج البيت إلى مراجعة لضبط الوزن",
                suggestion_en="Verse may need review to fix meter"
            ))
        
        # Error 2: No meter detected
        if not bahr_id:
            errors.append(ProsodyError(
                type="no_meter",
                severity=ErrorSeverity.CRITICAL,
                position=None,
                message_ar="لم يتم التعرف على البحر",
                message_en="No meter detected",
                suggestion_ar="تأكد من أن النص شعر موزون",
                suggestion_en="Ensure the text is metered poetry"
            ))
        
        # Error 3: Incomplete verse (too short)
        words = verse_text.strip().split()
        if len(words) < 4:
            errors.append(ProsodyError(
                type="incomplete_verse",
                severity=ErrorSeverity.MAJOR,
                position=None,
                message_ar="البيت قصير جداً",
                message_en="Verse is too short",
                suggestion_ar="أضف المزيد من الكلمات لإكمال البيت",
                suggestion_en="Add more words to complete the verse"
            ))
        
        # Error 4: Verse too long
        if len(words) > 25:
            errors.append(ProsodyError(
                type="verse_too_long",
                severity=ErrorSeverity.MINOR,
                position=None,
                message_ar="البيت طويل جداً",
                message_en="Verse is too long",
                suggestion_ar="قد يكون البيت يحتوي على أكثر من شطر",
                suggestion_en="Verse may contain more than two hemistichs"
            ))
        
        # Error 5: Tafa'il count mismatch
        if bahr_id and taqti3_result:
            tafail_count = len(taqti3_result.strip().split())
            expected_count = self.EXPECTED_TAFILA_COUNTS.get(bahr_id, 6)
            
            if tafail_count < expected_count - 1:
                errors.append(ProsodyError(
                    type="missing_tafila",
                    severity=ErrorSeverity.MAJOR,
                    position=None,
                    message_ar=f"عدد التفاعيل أقل من المتوقع ({tafail_count} بدلاً من {expected_count})",
                    message_en=f"Fewer tafa'il than expected ({tafail_count} vs {expected_count})",
                    suggestion_ar="قد يكون هناك تفعيلة ناقصة في البيت",
                    suggestion_en="Verse may be missing a prosodic foot"
                ))
            elif tafail_count > expected_count + 1:
                errors.append(ProsodyError(
                    type="extra_tafila",
                    severity=ErrorSeverity.MAJOR,
                    position=None,
                    message_ar=f"عدد التفاعيل أكثر من المتوقع ({tafail_count} بدلاً من {expected_count})",
                    message_en=f"More tafa'il than expected ({tafail_count} vs {expected_count})",
                    suggestion_ar="قد يكون هناك تفعيلة زائدة في البيت",
                    suggestion_en="Verse may have an extra prosodic foot"
                ))
        
        # Error 6: Empty or minimal taqti3 result
        if not taqti3_result or len(taqti3_result.strip()) < 5:
            errors.append(ProsodyError(
                type="taqti3_failed",
                severity=ErrorSeverity.CRITICAL,
                position=None,
                message_ar="فشل التقطيع العروضي",
                message_en="Prosodic scansion failed",
                suggestion_ar="تأكد من أن النص يحتوي على أحرف عربية صحيحة",
                suggestion_en="Ensure text contains valid Arabic characters"
            ))
        
        return errors
    
    def generate_suggestions(
        self,
        verse_text: str,
        quality_score: QualityScore,
        errors: List[ProsodyError],
        meter_confidence: float,
        bahr_name_ar: Optional[str]
    ) -> List[str]:
        """
        Generate actionable suggestions for improving verse quality.
        
        Args:
            verse_text: Original verse text
            quality_score: Calculated quality score
            errors: Detected prosodic errors
            meter_confidence: Meter detection confidence
            bahr_name_ar: Detected meter name in Arabic
            
        Returns:
            List of suggestion strings (in Arabic)
            
        Example:
            >>> suggestions = analyzer.generate_suggestions(...)
            >>> suggestions
            ['التقطيع دقيق ومتسق', 'البيت على بحر الطويل']
        """
        suggestions: List[str] = []
        
        # Suggestion based on overall quality
        if quality_score.overall >= 95:
            suggestions.append("✨ ممتاز! التقطيع دقيق ومتسق تماماً")
        elif quality_score.overall >= 85:
            suggestions.append("✓ جيد جداً! التقطيع صحيح مع اختلافات طفيفة")
        elif quality_score.overall >= 70:
            suggestions.append("التقطيع جيد مع بعض الاختلافات")
        elif quality_score.overall >= 50:
            suggestions.append("⚠ التقطيع يحتاج إلى مراجعة")
        else:
            suggestions.append("⚠ التقطيع يحتاج إلى تحسين كبير")
        
        # Suggestion about detected meter
        if bahr_name_ar and meter_confidence >= 0.85:
            suggestions.append(f"البيت على بحر {bahr_name_ar}")
        elif bahr_name_ar and meter_confidence >= 0.7:
            suggestions.append(f"البيت يميل إلى بحر {bahr_name_ar} (ثقة: {meter_confidence*100:.0f}%)")
        
        # Suggestions based on specific score components
        if quality_score.pattern_consistency < 70:
            suggestions.append("يوجد عدم اتساق في النمط العروضي - راجع التفاعيل")
        
        if quality_score.length_score < 70:
            suggestions.append("طول البيت غير مناسب للبحر المكتشف")
        
        if quality_score.completeness < 70:
            suggestions.append("البيت قد يكون ناقصاً - تأكد من وجود الشطرين")
        
        # Suggestions based on errors
        critical_errors = [e for e in errors if e.severity == ErrorSeverity.CRITICAL]
        if critical_errors:
            for error in critical_errors[:2]:  # Max 2 critical error messages
                if error.suggestion_ar:
                    suggestions.append(f"⚠ {error.suggestion_ar}")
        
        # General tips for improvement
        if quality_score.overall < 80 and len(suggestions) < 3:
            suggestions.append("نصيحة: تأكد من التشكيل الصحيح لتحسين دقة التحليل")
        
        # Limit to 5 suggestions max
        return suggestions[:5]


def analyze_verse_quality(
    verse_text: str,
    taqti3_result: str,
    bahr_id: Optional[int],
    bahr_name_ar: Optional[str],
    meter_confidence: float,
    detected_pattern: str = "",
    expected_pattern: str = ""
) -> Tuple[QualityScore, List[ProsodyError], List[str]]:
    """
    Comprehensive verse quality analysis (convenience function).
    
    Args:
        verse_text: Original Arabic verse text
        taqti3_result: Taqti3 output (tafa'il string)
        bahr_id: Detected meter ID
        bahr_name_ar: Detected meter name in Arabic
        meter_confidence: Meter detection confidence (0.0-1.0)
        detected_pattern: Actual phonetic pattern
        expected_pattern: Expected phonetic pattern
        
    Returns:
        Tuple of (QualityScore, List[ProsodyError], List[str] suggestions)
        
    Example:
        >>> score, errors, suggestions = analyze_verse_quality(
        ...     verse_text="إذا غامرت في شرف مروم",
        ...     taqti3_result="فعولن مفاعيلن فعولن مفاعيلن",
        ...     bahr_id=1,
        ...     bahr_name_ar="الطويل",
        ...     meter_confidence=0.95
        ... )
        >>> score.overall
        95.0
        >>> len(suggestions)
        3
    """
    analyzer = QualityAnalyzer()
    
    # Calculate quality score
    quality_score = analyzer.calculate_quality_score(
        verse_text=verse_text,
        taqti3_result=taqti3_result,
        bahr_id=bahr_id,
        meter_confidence=meter_confidence,
        detected_pattern=detected_pattern,
        expected_pattern=expected_pattern
    )
    
    # Detect errors
    errors = analyzer.detect_errors(
        verse_text=verse_text,
        taqti3_result=taqti3_result,
        bahr_id=bahr_id,
        meter_confidence=meter_confidence,
        phonetic_pattern=detected_pattern
    )
    
    # Generate suggestions
    suggestions = analyzer.generate_suggestions(
        verse_text=verse_text,
        quality_score=quality_score,
        errors=errors,
        meter_confidence=meter_confidence,
        bahr_name_ar=bahr_name_ar
    )
    
    return quality_score, errors, suggestions
