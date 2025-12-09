"""
Todays Tasks Endpoint - Standalone
"""

from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

router = APIRouter()


# ============================================
# MODELS
# ============================================

class TopicAtRisk(BaseModel):
    topic_id: str
    topic_name: str
    subject: str
    retention_rate: int
    days_until_forgotten: int
    last_studied: str
    difficulty_score: int
    priority_score: int


class PriorityTopic(BaseModel):
    topic_id: str
    topic_name: str
    subject: str
    priority_score: int
    priority_reason: str
    difficulty_score: int
    retention_rate: int
    estimated_study_time: int


class StudyStreak(BaseModel):
    current_streak: int
    longest_streak: int
    streak_status: str
    last_study_date: str
    next_milestone: int


class TimeStats(BaseModel):
    total_study_time_today: int
    total_study_time_week: int
    avg_daily_time: int
    target_daily_time: int
    time_efficiency: int


class TodaysTasksDataOld(BaseModel):
    at_risk_topics: List[TopicAtRisk]
    total_at_risk: int
    priority_topics: List[PriorityTopic]
    total_priority: int
    streak: StudyStreak
    time_stats: TimeStats
    generated_at: str
    student_id: str


class TodaysTasksResponseOld(BaseModel):
    success: bool
    data: TodaysTasksDataOld
    message: Optional[str] = None


# ============================================
# ENDPOINT
# ============================================

@router.get("/student/todays-tasks", response_model=TodaysTasksResponseOld)
async def get_todays_tasks(current_user: dict = Depends(get_current_user)):
    """
    🎯 Bugünkü Görevler (3 Kart)
    
    Mock data - authentication yok
    """
    return TodaysTasksResponseOld(
        success=True,
        data=TodaysTasksDataOld(
            at_risk_topics=[
                TopicAtRisk(
                    topic_id="mat-001",
                    topic_name="Türev Alma Kuralları",
                    subject="Matematik",
                    retention_rate=45,
                    days_until_forgotten=2,
                    last_studied="2025-11-28T14:30:00Z",
                    difficulty_score=68,
                    priority_score=85
                ),
                TopicAtRisk(
                    topic_id="fiz-003",
                    topic_name="Elektromanyetik İndüksiyon",
                    subject="Fizik",
                    retention_rate=52,
                    days_until_forgotten=3,
                    last_studied="2025-11-27T10:15:00Z",
                    difficulty_score=72,
                    priority_score=78
                ),
                TopicAtRisk(
                    topic_id="kim-005",
                    topic_name="Kimyasal Denge",
                    subject="Kimya",
                    retention_rate=38,
                    days_until_forgotten=1,
                    last_studied="2025-11-29T16:45:00Z",
                    difficulty_score=81,
                    priority_score=92
                ),
            ],
            total_at_risk=3,
            
            priority_topics=[
                PriorityTopic(
                    topic_id="mat-015",
                    topic_name="İntegral Uygulamaları",
                    subject="Matematik",
                    priority_score=88,
                    priority_reason="prerequisite",
                    difficulty_score=75,
                    retention_rate=55,
                    estimated_study_time=45
                ),
                PriorityTopic(
                    topic_id="fiz-008",
                    topic_name="Kuvvet ve Hareket",
                    subject="Fizik",
                    priority_score=82,
                    priority_reason="difficulty",
                    difficulty_score=85,
                    retention_rate=48,
                    estimated_study_time=60
                ),
                PriorityTopic(
                    topic_id="biy-012",
                    topic_name="Hücre Bölünmesi",
                    subject="Biyoloji",
                    priority_score=76,
                    priority_reason="never_studied",
                    difficulty_score=0,
                    retention_rate=0,
                    estimated_study_time=90
                ),
            ],
            total_priority=3,
            
            streak=StudyStreak(
                current_streak=5,
                longest_streak=12,
                streak_status="active",
                last_study_date="2025-12-04T09:00:00Z",
                next_milestone=7
            ),
            
            time_stats=TimeStats(
                total_study_time_today=45,
                total_study_time_week=380,
                avg_daily_time=54,
                target_daily_time=120,
                time_efficiency=75
            ),
            
            generated_at=datetime.now(timezone.utc).isoformat(),
            student_id="demo-student"
        ),
        message="Mock data (3 kart)"
    )
