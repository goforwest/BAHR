"""
SQLAlchemy base and imports.
"""

# Import Base from models.base (already defined there)
from app.models.base import Base

# Import all models here for Alembic auto-detection
from app.models.user import User
from app.models.bahr import Bahr, Taf3ila
from app.models.poem import Poem, Verse
from app.models.meter import Meter
from app.models.tafila import Tafila
from app.models.analysis import Analysis
# Add more as you create them

__all__ = ["Base", "User", "Bahr", "Taf3ila", "Poem", "Verse", "Meter", "Tafila", "Analysis"]
