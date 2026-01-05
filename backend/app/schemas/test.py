"""
Test Schemas
Pydantic schemas for test entry and results
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID


class TopicResult(BaseModel):
    """Single topic result within a test"""
    topic_id: UUID
    questions_total: int = Field(..., ge=0)
    questions_correct: int = Field(..., ge=0)
    questions_wrong: int = Field(..., ge=0)
    questions_blank: int = Field(..., ge=0)
    time_spent_seconds: int = Field(..., ge=0)
    
    @validator("questions_correct", "questions_wrong", "questions_blank")
    def validate_question_sum(cls, v, values):
        """Validate that question counts sum to total"""
        if "questions_total" in values:
            total = values["questions_total"]
            # This will be checked after all fields are set
        return v
    
    @validator("questions_blank")
    def validate_total_matches(cls, v, values):
        """Final validation that all questions add up"""
        if all(k in values for k in ["questions_total", "questions_correct", "questions_wrong"]):
            total = values["questions_total"]
            correct = values["questions_correct"]
            wrong = values["questions_wrong"]
            blank = v
            
            if correct + wrong + blank != total:
                raise ValueError(
                    f"Question counts must sum to total: "
                    f"{correct} + {wrong} + {blank} != {total}"
                )
        return v


class TestEntryRequest(BaseModel):
    """Test entry request"""
    test_name: Optional[str] = None
    test_date: date
    test_type: str = "practice"  # mock_exam, practice, daily_quiz
    topics: List[TopicResult] = Field(..., min_items=1)
    
    @validator("test_date")
    def validate_test_date(cls, v):
        """Test date cannot be in the future"""
        if v > date.today():
            raise ValueError("Test date cannot be in the future")
        return v


class TestEntryResponse(BaseModel):
    """Test entry response"""
    test_record_id: UUID
    test_name: Optional[str]
    test_date: date
    topics_count: int
    total_questions: int
    motor_calculations: Dict[str, Any]  # Results from motors
    created_at: datetime
    
    class Config:
        from_attributes = True


class TestRecordSummary(BaseModel):
    """Test record summary (for list view)"""
    id: UUID
    test_name: Optional[str]
    test_date: date
    test_type: str
    topics_count: int
    total_questions: int
    average_success_rate: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TestRecordDetail(BaseModel):
    """Test record detail (for single view)"""
    id: UUID
    test_name: Optional[str]
    test_date: date
    test_type: str
    topics: List["TopicResultDetail"]
    summary_stats: Dict[str, Any]
    motor_analysis: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TopicResultDetail(BaseModel):
    """Topic result detail"""
    id: UUID
    topic_id: UUID
    topic_name: str
    subject_code: str
    questions_total: int
    questions_correct: int
    questions_wrong: int
    questions_blank: int
    time_spent_seconds: int
    success_rate: float
    speed_score: float
    bs_model_score: Optional[float] = None
    remembering_rate: Optional[float] = None
    priority_score: Optional[float] = None
    difficulty_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class TestListRequest(BaseModel):
    """Test list request (with filters)"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    test_type: Optional[str] = None
    subject_id: Optional[UUID] = None
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)


class TestListResponse(BaseModel):
    """Test list response"""
    tests: List[TestRecordSummary]
    total_count: int
    limit: int
    offset: int