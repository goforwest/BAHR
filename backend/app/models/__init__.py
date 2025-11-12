"""
Database models package.

All SQLAlchemy models for the BAHR application.

Core MVP Models:
1. User - User accounts and authentication
2. Meter - Arabic prosodic meters (بحور) reference data
3. Tafila - Prosodic feet (تفعيلة) reference data
4. Analysis - Poetry analysis results
5. AnalysisCache - Cached analysis results

Import all models here for easy access:
    from app.models import User, Meter, Tafila, Analysis, AnalysisCache
"""

from .analysis import Analysis, AnalysisMode
from .base import Base, TimestampMixin
from .cache import AnalysisCache
from .meter import Meter, MeterType
from .tafila import Tafila
from .user import PrivacyLevel, User, UserRole

__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "UserRole",
    "PrivacyLevel",
    "Meter",
    "MeterType",
    "Tafila",
    "Analysis",
    "AnalysisMode",
    "AnalysisCache",
]
