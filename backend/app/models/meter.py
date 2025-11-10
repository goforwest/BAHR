"""
Meter (Bahr) model - Arabic prosodic meters reference data.

Represents the 16 classical Arabic poetry meters and their patterns.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, Enum as SQLEnum, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum
from .base import Base, TimestampMixin


class MeterType(str, enum.Enum):
    """Meter type classification."""
    CLASSICAL = "classical"  # البحور الخليلية
    MODERN = "modern"  # البحور الحديثة
    FOLK = "folk"  # الشعبية
    EXPERIMENTAL = "experimental"  # التجريبية


class Meter(Base, TimestampMixin):
    """
    Arabic prosodic meter (بحر) reference data.
    
    Contains the 16 classical meters with their patterns, characteristics,
    and usage statistics.
    """
    __tablename__ = "meters"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Names
    name = Column(String(100), unique=True, nullable=False, index=True)  # اسم البحر
    english_name = Column(String(100))
    
    # Pattern information
    base_pattern = Column(Text, nullable=False)  # النمط الأساسي
    pattern_type = Column(SQLEnum(MeterType), nullable=False, default=MeterType.CLASSICAL, index=True)
    complexity_level = Column(Integer)  # 1-5 scale
    
    # Characteristics
    syllable_count = Column(Integer)
    foot_pattern = Column(ARRAY(String))  # تفعيلات البحر
    common_variations = Column(JSONB, default=[])
    
    # Usage statistics
    frequency_rank = Column(Integer, index=True)
    usage_count = Column(Integer, default=0)
    difficulty_score = Column(DECIMAL(3, 2))  # 1.0-5.0 scale
    
    # Historical and cultural info
    origin_period = Column(String(50))
    famous_poets = Column(ARRAY(String))
    description_ar = Column(Text)
    description_en = Column(Text)
    
    # Examples
    example_verses = Column(JSONB, default=[])
    audio_samples = Column(JSONB, default=[])
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_classical = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Meter(id={self.id}, name='{self.name}', type='{self.pattern_type.value}')>"
