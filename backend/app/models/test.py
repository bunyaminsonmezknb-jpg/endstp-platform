"""
Test Models
Database models for test records and topic test results
"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


class TestRecord:
    """
    Test Record model (Deneme Kaydı)
    
    Represents a single test attempt
    """
    
    __tablename__ = "test_records"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Test info
    test_name = Column(String(255))
    test_date = Column(Date, nullable=False, index=True)
    test_type = Column(String(50))  # mock_exam, practice, daily_quiz
    
    # Total questions (optional, for validation)
    total_questions = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # user = relationship("User", back_populates="test_records")
    # topic_results = relationship("TopicTestResult", back_populates="test_record")
    
    def __repr__(self):
        return f"<TestRecord {self.test_name} - {self.test_date}>"


class TopicTestResult:
    """
    Topic Test Result model (Konu Bazlı Test Sonucu)
    
    Represents performance on a specific topic within a test
    """
    
    __tablename__ = "topic_test_results"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Keys
    test_record_id = Column(UUID(as_uuid=True), ForeignKey("test_records.id"), nullable=False, index=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Performance metrics
    questions_total = Column(Integer, nullable=False)
    questions_correct = Column(Integer, nullable=False)
    questions_wrong = Column(Integer, nullable=False)
    questions_blank = Column(Integer, nullable=False)
    
    # Timing data (crucial for BS-Model)
    time_spent_seconds = Column(Integer, nullable=False)
    entry_timestamp = Column(DateTime, default=datetime.utcnow)  # Must be within 24h of test_date
    
    # Derived metrics (calculated by backend)
    success_rate = Column(DECIMAL(5, 2))  # (correct / total) * 100
    speed_score = Column(DECIMAL(5, 2))   # time_spent / questions_total
    
    # Motor outputs (calculated by engines)
    bs_model_score = Column(DECIMAL(5, 2))
    remembering_rate = Column(DECIMAL(5, 2))
    priority_score = Column(DECIMAL(5, 2))
    difficulty_score = Column(DECIMAL(5, 2))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # test_record = relationship("TestRecord", back_populates="topic_results")
    # topic = relationship("Topic", back_populates="test_results")
    # user = relationship("User", back_populates="topic_test_results")
    
    def __repr__(self):
        return f"<TopicTestResult {self.topic_id} - {self.success_rate}%>"