"""
User model - Account management and authentication.

Represents user accounts with authentication, profiles, and gamification.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text, DECIMAL, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum
from .base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    """User role enumeration."""
    STUDENT = "student"
    POET = "poet"
    TEACHER = "teacher"
    MODERATOR = "moderator"
    ADMIN = "admin"


class PrivacyLevel(str, enum.Enum):
    """Privacy level enumeration."""
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"


class User(Base, TimestampMixin):
    """
    User model for authentication and profile management.
    
    Includes gamification features (level, XP, coins) and privacy settings.
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(100), nullable=False)
    bio = Column(Text)
    avatar_url = Column(String(500))
    birth_date = Column(Date)
    location = Column(String(100))
    website = Column(String(255))
    
    # Role and permissions
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT, index=True)
    
    # Gamification
    level = Column(Integer, default=1, index=True)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    
    # Account status
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime(timezone=True))
    last_login = Column(DateTime(timezone=True))
    
    # Preferences
    preferred_language = Column(String(5), default='ar')
    theme = Column(String(10), default='light')
    notifications = Column(JSONB, default={"email": True, "push": True})
    
    # Privacy
    profile_visibility = Column(SQLEnum(PrivacyLevel), default=PrivacyLevel.PUBLIC)
    analysis_privacy = Column(SQLEnum(PrivacyLevel), default=PrivacyLevel.PRIVATE)
    
    # Soft delete
    deleted_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"
