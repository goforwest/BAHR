"""
Cache model - Analysis result caching.

Stores cached analysis results for frequently analyzed texts.
"""

from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class AnalysisCache(Base):
    """
    Cache for analysis results to improve performance.

    Stores results by text hash to avoid re-analyzing identical texts.
    """

    __tablename__ = "analysis_cache"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Cache key (hash of normalized text)
    text_hash = Column(String(64), unique=True, nullable=False, index=True)

    # Original data
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=False)

    # Cached result
    cached_result = Column(JSONB, nullable=False)

    # Cache metadata
    hit_count = Column(Integer, default=0)
    algorithm_version = Column(String(20), nullable=False)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    last_accessed = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

    def __repr__(self):
        return f"<AnalysisCache(id={self.id}, hits={self.hit_count}, hash='{self.text_hash[:8]}...')>"

    def is_expired(self):
        """Check if cache entry has expired."""
        return datetime.utcnow() > self.expires_at

    @classmethod
    def default_expiry(cls):
        """Default cache expiry (30 days)."""
        return datetime.utcnow() + timedelta(days=30)
