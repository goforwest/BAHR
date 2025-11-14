"""
Analysis model - Poetry analysis results.

Stores results from prosodic analysis of Arabic poetry.
"""

import enum
import uuid

from sqlalchemy import DECIMAL, Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class AnalysisMode(str, enum.Enum):
    """Analysis mode enumeration."""

    FAST = "fast"
    ACCURATE = "accurate"
    DETAILED = "detailed"


class Analysis(Base, TimestampMixin):
    """
    Poetry analysis result model.

    Stores input text, detected meter, quality scores, and detailed
    prosodic analysis results.
    """

    __tablename__ = "analyses"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # User relationship (optional - can analyze without account)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)

    # Input data
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=False)
    language = Column(String(5), default="ar")
    dialect = Column(String(20))

    # Analysis metadata
    analysis_mode = Column(
        SQLEnum(AnalysisMode), nullable=False, default=AnalysisMode.ACCURATE
    )
    processing_time_ms = Column(Integer)
    algorithm_version = Column(String(20), nullable=False, default="1.0")

    # Prosodic analysis
    prosodic_pattern = Column(JSONB, nullable=False)  # Full pattern analysis
    syllable_count = Column(Integer)
    stress_pattern = Column(Text)
    taqti3 = Column(Text)  # التقطيع العروضي

    # Meter detection
    detected_meter = Column(String(50), index=True)
    meter_confidence = Column(DECIMAL(5, 4))  # 0.0000 to 1.0000
    alternative_meters = Column(JSONB, default=[])

    # Quality assessment
    quality_score = Column(DECIMAL(5, 4), index=True)  # 0.0000 to 1.0000
    quality_breakdown = Column(JSONB)  # Detailed quality metrics

    # Results and suggestions
    analysis_result = Column(JSONB, nullable=False)
    suggestions = Column(JSONB, default=[])
    corrections = Column(JSONB, default=[])

    # Visibility and engagement
    is_public = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<Analysis(id={self.id}, meter='{self.detected_meter}', confidence={self.meter_confidence})>"
