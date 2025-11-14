"""
Analytics schemas for API validation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalyticsEventCreate(BaseModel):
    """Schema for creating an analytics event."""

    name: str = Field(..., min_length=1, max_length=100, description="Event name")
    session_id: str = Field(
        ..., min_length=1, max_length=100, description="Session identifier"
    )
    timestamp: int = Field(..., description="Unix timestamp in milliseconds")
    user_id: Optional[str] = Field(None, max_length=100, description="User identifier")
    properties: Optional[Dict[str, Any]] = Field(None, description="Event metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "analyze_submit",
                "session_id": "1234567890-abc123",
                "timestamp": 1699999999999,
                "properties": {"verse_length": 45, "has_diacritics": True},
            }
        }


class AnalyticsEventResponse(BaseModel):
    """Schema for analytics event response."""

    id: str
    event_name: str
    session_id: str
    timestamp: int
    created_at: datetime

    class Config:
        from_attributes = True


class AnalyticsStatsResponse(BaseModel):
    """Schema for analytics statistics."""

    total_sessions: int
    total_events: int
    total_analyses: int
    success_rate: float
    top_events: List[Dict[str, Any]]
    recent_activity: List[AnalyticsEventResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "total_sessions": 1234,
                "total_events": 5678,
                "total_analyses": 890,
                "success_rate": 0.95,
                "top_events": [
                    {"name": "analyze_submit", "count": 890},
                    {"name": "page_view", "count": 1234},
                ],
                "recent_activity": [],
            }
        }
