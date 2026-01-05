"""
Subject Model
Database model for subjects (Math, Physics, etc.)
"""

from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class Subject:
    """
    Subject model (Ders)
    
    Example: Mathematics, Physics, Chemistry
    """
    
    __tablename__ = "subjects"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Localized names (GLOBAL-FIRST)
    name_tr = Column(String(255), nullable=False)
    name_en = Column(String(255))
    
    # Unique code (e.g., MAT, FIZ, KIM)
    code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Display order
    display_order = Column(Integer, default=0)
    
    # Active status
    is_active = Column(Boolean, default=True)
    
    # Optional description
    description_tr = Column(Text)
    description_en = Column(Text)
    
    # Relationships
    # topics = relationship("Topic", back_populates="subject")
    # exam_weights = relationship("SubjectExamWeight", back_populates="subject")
    
    def __repr__(self):
        return f"<Subject {self.code}: {self.name_tr}>"