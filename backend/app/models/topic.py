"""
Topic Model
Database model for topics within subjects
"""

from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class Topic:
    """
    Topic model (Konu)
    
    Example: Türev, Limit, İntegral
    """
    
    __tablename__ = "topics"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key to subject
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False, index=True)
    
    # Localized names (GLOBAL-FIRST)
    name_tr = Column(String(255), nullable=False)
    name_en = Column(String(255))
    
    # Unique code (e.g., MAT_TUREV, FIZ_HAREKET)
    code = Column(String(100), unique=True, nullable=False, index=True)
    
    # Difficulty level (1-10)
    difficulty_level = Column(Integer)
    
    # Estimated study time (minutes)
    estimated_study_minutes = Column(Integer)
    
    # Active status
    is_active = Column(Boolean, default=True)
    
    # Optional description
    description_tr = Column(Text)
    description_en = Column(Text)
    
    # Metadata (JSONB for flexible data)
    # metadata = Column(JSONB)
    
    # Relationships
    # subject = relationship("Subject", back_populates="topics")
    # test_results = relationship("TopicTestResult", back_populates="topic")
    # prerequisites = relationship("Prerequisite", foreign_keys="Prerequisite.topic_id")
    
    def __repr__(self):
        return f"<Topic {self.code}: {self.name_tr}>"