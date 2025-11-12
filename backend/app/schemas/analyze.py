"""
Pydantic schemas for the analyze endpoint.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    """
    Request schema for verse analysis.
    
    Attributes:
        text: Arabic verse or text to analyze (required)
        detect_bahr: Whether to detect the meter (default: True)
        suggest_corrections: Whether to suggest corrections (default: False)
    """
    text: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Arabic verse or text to analyze",
        examples=["إذا غامَرتَ في شَرَفٍ مَرومِ"]
    )
    detect_bahr: bool = Field(
        default=True,
        description="Whether to detect the meter (bahr)"
    )
    suggest_corrections: bool = Field(
        default=False,
        description="Whether to suggest prosodic corrections"
    )
    analyze_rhyme: bool = Field(
        default=True,
        description="Whether to analyze rhyme (qafiyah)"
    )
    precomputed_pattern: Optional[str] = Field(
        default=None,
        description="Pre-computed phonetic pattern (optional, for advanced users). Format: /=haraka, o=sakin. Example: '/o////o/o/o/o//o//o/'"
    )
    expected_meter: Optional[str] = Field(
        default=None,
        description="Expected meter name in Arabic (optional, enables smart disambiguation). Example: 'الطويل'"
    )

    @field_validator('text')
    @classmethod
    def validate_arabic(cls, v: str) -> str:
        """Validate that text contains Arabic characters."""
        # Edge case: Strip whitespace for validation
        stripped = v.strip()
        
        if not stripped:
            raise ValueError('Text cannot be empty or only whitespace')
        
        if len(stripped) < 5:
            raise ValueError('Text must be at least 5 characters long')
        
        # Check for Arabic characters
        arabic_char_count = sum(1 for ch in v if '\u0600' <= ch <= '\u06FF')
        
        if arabic_char_count == 0:
            raise ValueError('Text must contain Arabic characters')
        
        # Edge case: Warn if text has very little Arabic (< 30%)
        if arabic_char_count / len(stripped) < 0.3:
            raise ValueError('Text must be primarily in Arabic (at least 30% Arabic characters)')
        
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
                    "detect_bahr": True,
                    "suggest_corrections": False
                },
                {
                    "text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً",
                    "detect_bahr": True,
                    "suggest_corrections": True
                }
            ]
        }
    }


class BahrInfo(BaseModel):
    """
    Information about a detected meter (bahr).

    Attributes:
        id: Unique identifier for the meter
        name_ar: Arabic name of the meter
        name_en: English transliteration
        confidence: Detection confidence score (0.0 to 1.0)
        match_quality: Quality of match (exact, strong, moderate, weak) - NEW in v2
        matched_pattern: The exact phonetic pattern that matched - NEW in v2
        transformations: List of zihafat/ilal applied at each position - NEW in v2
        explanation_ar: Arabic explanation of the match - NEW in v2
        explanation_en: English explanation of the match - NEW in v2
    """
    id: int = Field(..., description="Unique identifier for the meter")
    name_ar: str = Field(..., description="Arabic name of the meter")
    name_en: str = Field(..., description="English transliteration")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Detection confidence score"
    )

    # NEW: Explainability fields from BahrDetectorV2
    match_quality: Optional[str] = Field(
        None,
        description="Match quality: exact, strong, moderate, or weak"
    )
    matched_pattern: Optional[str] = Field(
        None,
        description="The exact phonetic pattern that matched"
    )
    transformations: Optional[List[str]] = Field(
        None,
        description="Zihafat/Ilal applied at each position (e.g., ['base', 'قبض', 'base', 'حذف'])"
    )
    explanation_ar: Optional[str] = Field(
        None,
        description="Arabic explanation of how the match was made"
    )
    explanation_en: Optional[str] = Field(
        None,
        description="English explanation of how the match was made"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name_ar": "الطويل",
                    "name_en": "at-Tawil",
                    "confidence": 0.97,
                    "match_quality": "strong",
                    "matched_pattern": "/o////o/o/o/o//o//o/o/o",
                    "transformations": ["base", "قبض", "base", "base"],
                    "explanation_ar": "مطابقة مع زحافات: قبض",
                    "explanation_en": "Match with variations: qabd"
                }
            ]
        }
    }


class RhymeInfo(BaseModel):
    """
    Information about rhyme (qafiyah) in the verse.
    
    Attributes:
        rawi: The main rhyme letter (حرف الروي)
        rawi_vowel: Vowel on the rawi ('i', 'u', 'a', or '' for sukun)
        rhyme_types: List of rhyme type classifications
        description_ar: Arabic description of the qafiyah
        description_en: English description of the qafiyah
    """
    rawi: str = Field(..., description="Main rhyme letter (حرف الروي)")
    rawi_vowel: str = Field(..., description="Vowel on rawi")
    rhyme_types: List[str] = Field(..., description="Rhyme type classifications")
    description_ar: str = Field(..., description="Arabic description")
    description_en: str = Field(..., description="English description")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "rawi": "م",
                    "rawi_vowel": "",
                    "rhyme_types": ["مقيدة", "مجردة"],
                    "description_ar": "القافية: روي:م (مقيدة, مجردة)",
                    "description_en": "Qafiyah: rawi=م"
                }
            ]
        }
    }


class AnalyzeResponse(BaseModel):
    """
    Response schema for verse analysis.
    
    Attributes:
        text: Original input text
        taqti3: Prosodic scansion result (tafa'il)
        bahr: Detected meter information (if detect_bahr=True)
        errors: List of prosodic errors detected
        suggestions: List of suggestions for improvement
        score: Overall quality score (0-100)
    """
    text: str = Field(..., description="Original input text")
    taqti3: str = Field(..., description="Prosodic scansion (tafa'il pattern)")
    bahr: Optional[BahrInfo] = Field(
        None,
        description="Detected meter information"
    )
    rhyme: Optional[RhymeInfo] = Field(
        None,
        description="Rhyme (qafiyah) information"
    )
    errors: List[str] = Field(
        default_factory=list,
        description="List of prosodic errors"
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="List of improvement suggestions"
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Overall quality score (0-100)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
                    "taqti3": "فعولن مفاعيلن فعولن مفاعيلن",
                    "bahr": {
                        "id": 1,
                        "name_ar": "الطويل",
                        "name_en": "at-Tawil",
                        "confidence": 0.95
                    },
                    "rhyme": {
                        "rawi": "م",
                        "rawi_vowel": "",
                        "rhyme_types": ["مقيدة", "مجردة"],
                        "description_ar": "القافية: روي:م (مقيدة, مجردة)",
                        "description_en": "Qafiyah: rawi=م"
                    },
                    "errors": [],
                    "suggestions": ["التقطيع دقيق ومتسق"],
                    "score": 95.0
                }
            ]
        }
    }
