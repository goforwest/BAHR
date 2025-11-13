"""
Pydantic schemas for feedback collection.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class MeterFeedback(BaseModel):
    """
    User feedback on meter detection.

    Collected when users select a different meter than what was detected,
    or when they confirm the detection was correct.

    Attributes:
        text: Original input text (as submitted by user)
        normalized_text: Normalized version of the text
        detected_meter: The meter that was detected by the system
        detected_confidence: Confidence score of the detected meter
        user_selected_meter: The meter the user selected (may be same as detected)
        alternatives_shown: List of alternative meters shown to the user
        has_tashkeel: Whether the input text had diacritical marks
        user_comment: Optional comment from the user
        timestamp: When the feedback was submitted
    """

    text: str = Field(..., description="Original input text")
    normalized_text: str = Field(..., description="Normalized text")
    detected_meter: str = Field(..., description="Detected meter (Arabic name)")
    detected_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score of detected meter"
    )
    user_selected_meter: str = Field(
        ..., description="User-selected meter (Arabic name)"
    )
    alternatives_shown: List[str] = Field(
        default_factory=list, description="Alternative meters shown to user"
    )
    has_tashkeel: bool = Field(..., description="Whether text had diacritics")
    user_comment: Optional[str] = Field(default="", description="Optional user comment")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Feedback submission timestamp"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "قفا نبك من ذكرى حبيب ومنزل",
                    "normalized_text": "قفا نبك من ذكري حبيب ومنزل",
                    "detected_meter": "الرجز",
                    "detected_confidence": 0.9839,
                    "user_selected_meter": "الطويل",
                    "alternatives_shown": ["الرجز", "الطويل", "السريع"],
                    "has_tashkeel": False,
                    "user_comment": "This is the famous Mu'allaqah verse by Imru' al-Qais",
                    "timestamp": "2025-11-12T10:30:00Z",
                }
            ]
        }
    }


class FeedbackResponse(BaseModel):
    """
    Response after feedback submission.

    Attributes:
        status: Success or error status
        message: User-friendly message (bilingual)
        feedback_id: Unique identifier for this feedback
    """

    status: str = Field(..., description="Status (success or error)")
    message: str = Field(..., description="User-friendly message")
    feedback_id: str = Field(..., description="Unique feedback identifier")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "message": "شكراً لملاحظاتك! | Thank you for your feedback!",
                    "feedback_id": "fb_1731409800",
                }
            ]
        }
    }
