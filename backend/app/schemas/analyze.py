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
        name_ar: Arabic name of the meter
        name_en: English transliteration
        confidence: Detection confidence score (0.0 to 1.0)
    """
    name_ar: str = Field(..., description="Arabic name of the meter")
    name_en: str = Field(..., description="English transliteration")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Detection confidence score"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name_ar": "الطويل",
                    "name_en": "at-Tawil",
                    "confidence": 0.95
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
                        "name_ar": "الطويل",
                        "name_en": "at-Tawil",
                        "confidence": 0.95
                    },
                    "errors": [],
                    "suggestions": ["التقطيع دقيق ومتسق"],
                    "score": 95.0
                }
            ]
        }
    }
