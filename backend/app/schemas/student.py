"""
Student Schemas
Pydantic schemas for student-related endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID


class StudentProfile(BaseModel):
    """Student profile"""
    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudentStats(BaseModel):
    """Student statistics"""
    total_tests: int
    total_topics_studied: int
    average_success_rate: float
    streak_days: int
    critical_topics_count: int
    frozen_topics_count: int


class TopicHealth(BaseModel):
    """Topic health status"""
    topic_id: UUID
    topic_name: str
    subject_code: str
    remembering_rate: float  # 0-100
    last_test_date: Optional[date] = None
    days_since_last_test: Optional[int] = None
    status: str  # healthy, warning, critical, frozen
    priority_score: Optional[float] = None


class StudentDashboard(BaseModel):
    """Student dashboard data"""
    profile: StudentProfile
    stats: StudentStats
    critical_alerts: List[Dict[str, Any]]
    today_tasks: List[Dict[str, Any]]
    topic_health: List[TopicHealth]
    recent_tests: List[Dict[str, Any]]


class ProgressUpdate(BaseModel):
    """Progress update request"""
    topic_id: UUID
    action: str  # reviewed, practiced, mastered
    notes: Optional[str] = None


class GoalCreate(BaseModel):
    """Create goal request"""
    goal_type: str  # university, exam, topic_mastery
    target_value: str
    target_date: date
    description: Optional[str] = None


class GoalResponse(BaseModel):
    """Goal response"""
    id: UUID
    goal_type: str
    target_value: str
    target_date: date
    progress_percentage: float
    status: str  # active, completed, overdue
    created_at: datetime
    
    class Config:
        from_attributes = True