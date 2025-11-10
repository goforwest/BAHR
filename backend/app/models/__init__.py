"""
Database models package.

TODO (Week 1 Day 3): Implement complete models as per DATABASE_SCHEMA.md

Models to create:
1. User - User accounts and authentication
2. Analysis - Poetry analysis results
3. Meter - Arabic prosodic meters reference data
4. UserProfile - Extended user information (optional)

Import all models here for easy access:
    from app.models import User, Analysis, Meter
"""

from .base import Base, TimestampMixin

__all__ = ['Base', 'TimestampMixin']

# TODO: Uncomment after creating model files
# from .user import User
# from .analysis import Analysis
# from .meter import Meter
# 
# __all__ = ['Base', 'TimestampMixin', 'User', 'Analysis', 'Meter']

