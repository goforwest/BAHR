"""
Bahr (meter) and Taf'ila models.
"""

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text

from app.models.base import Base


class Bahr(Base):
    __tablename__ = "bahrs"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(50), nullable=False, unique=True)
    name_en = Column(String(50))
    pattern = Column(String(255), nullable=False)  # Tafa'il pattern
    description = Column(Text)
    example_verse = Column(Text)

    def __repr__(self):
        return f"<Bahr {self.name_ar}>"


class Taf3ila(Base):
    __tablename__ = "tafa3il"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    pattern = Column(String(50), nullable=False)  # Prosodic pattern
    variations = Column(JSON)  # Zihafat variations
    bahr_id = Column(Integer, ForeignKey("bahrs.id"), nullable=True)

    def __repr__(self):
        return f"<Taf3ila {self.name}>"
