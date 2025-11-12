"""
SQLAlchemy base and imports.
"""

from app.models.analysis import Analysis
from app.models.analytics import AnalyticsEvent
from app.models.bahr import Bahr, Taf3ila

# Import Base from models.base (already defined there)
from app.models.base import Base
from app.models.meter import Meter
from app.models.poem import Poem, Verse
from app.models.tafila import Tafila

# Import all models here for Alembic auto-detection
from app.models.user import User

# Add more as you create them

__all__ = [
    "Base",
    "User",
    "Bahr",
    "Taf3ila",
    "Poem",
    "Verse",
    "Meter",
    "Tafila",
    "Analysis",
    "AnalyticsEvent",
]
