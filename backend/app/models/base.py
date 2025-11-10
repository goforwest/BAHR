"""
Database models base configuration.

TODO (Week 1 Day 3): Implement SQLAlchemy models
- User model
- Analysis model
- Meter model
- Base model with common fields

See: docs/technical/DATABASE_SCHEMA.md for complete schema
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()


class TimestampMixin:
    """
    Mixin for created_at and updated_at timestamps.
    
    All models should inherit this to track creation/modification times.
    """
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# TODO (Week 1 Day 3): Create model files:
# - models/user.py
# - models/analysis.py
# - models/meter.py
# - models/__init__.py (export all models)

