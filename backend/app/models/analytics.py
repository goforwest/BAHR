"""
Analytics Event model - Usage tracking and analytics.

Stores user interaction events for analytics and usage monitoring.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from .base import Base


class AnalyticsEvent(Base):
    """
    Analytics event model.
    
    Tracks user interactions, page views, and system events
    for usage analytics and monitoring.
    """
    __tablename__ = "analytics_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event identification
    event_name = Column(String(100), nullable=False, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    user_id = Column(String(100), nullable=True, index=True)
    
    # Timing
    timestamp = Column(BigInteger, nullable=False, index=True)  # Unix timestamp in ms
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Event metadata
    properties = Column(JSONB, nullable=True)
    
    # Request context (optional)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    referrer = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<AnalyticsEvent(id={self.id}, event={self.event_name}, session={self.session_id[:8]})>"
