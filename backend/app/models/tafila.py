"""
Tafila model - Arabic prosodic feet (تفعيلة).

Represents the 8 base prosodic feet used in Arabic poetry meters.
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base, TimestampMixin


class Tafila(Base, TimestampMixin):
    """
    Arabic prosodic foot (تفعيلة) reference data.
    
    Contains the 8 base prosodic feet that compose meter patterns.
    """
    __tablename__ = "tafail"  # Plural: تفاعيل
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Names
    name_ar = Column(String(50), unique=True, nullable=False, index=True)  # الاسم العربي
    name_en = Column(String(50))  # Transliteration
    
    # Pattern
    pattern = Column(String(50), nullable=False)  # الرمز العروضي (e.g., "//0/0")
    arabic_notation = Column(String(50))  # التدوين العربي الكامل
    
    # Characteristics
    syllable_structure = Column(String(50))  # CV pattern (e.g., "CVCVCV")
    syllable_count = Column(Integer, nullable=False)
    long_syllables = Column(Integer, default=0)  # عدد المقاطع الطويلة
    short_syllables = Column(Integer, default=0)  # عدد المقاطع القصيرة
    
    # Variations
    common_variations = Column(JSONB, default=[])  # الزحافات والعلل
    alternative_forms = Column(ARRAY(String))  # أشكال بديلة
    
    # Usage
    used_in_meters = Column(ARRAY(String))  # البحور المستخدمة فيها
    usage_frequency = Column(DECIMAL(5, 4))  # مدى الاستخدام
    
    # Examples
    example_words = Column(JSONB, default=[])  # أمثلة على الكلمات
    description = Column(Text)  # وصف وشرح
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    def __repr__(self):
        return f"<Tafila(id={self.id}, name='{self.name_ar}', pattern='{self.pattern}')>"
