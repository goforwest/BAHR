"""
Poem and Verse models.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Poem(Base):
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255))
    full_text = Column(Text)
    bahr = Column(String(50))
    is_complete = Column(Boolean, default=False)
    visibility = Column(String(20), default="public")  # public, private, unlisted

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    verses = relationship("Verse", back_populates="poem")

    def __repr__(self):
        return f"<Poem {self.title}>"


class Verse(Base):
    __tablename__ = "verses"

    id = Column(Integer, primary_key=True, index=True)
    poem_id = Column(Integer, ForeignKey("poems.id"), nullable=False)

    text = Column(Text, nullable=False)
    taqti3_pattern = Column(String(255))
    bahr = Column(String(50))
    line_number = Column(Integer)
    hemisphere = Column(String(10))  # 'sadr' or 'ajuz'

    # Relationships
    poem = relationship("Poem", back_populates="verses")

    def __repr__(self):
        return f"<Verse {self.id}>"
