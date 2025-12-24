"""
Progress & Goals - Pydantic Models
"""
from pydantic import BaseModel
from typing import List, Optional

class ProgressProjection(BaseModel):
    overall_progress: float
    estimated_completion_date: str
    days_remaining: int
    weekly_improvement: float
    topics_mastered: int
    topics_in_progress: int
    topics_not_started: int

class SubjectProgress(BaseModel):
    subject_id: str
    subject_name: str
    subject_code: str
    progress_percentage: float
    topics_total: int
    topics_mastered: int
    topics_in_progress: int
    topics_not_started: int
    avg_success_rate: float
    trend: str

class TrendDataset(BaseModel):
    label: str
    data: List[Optional[float]]
    subject_id: str

class TrendData(BaseModel):
    labels: List[str]
    datasets: List[TrendDataset]
    overall_trend: List[Optional[float]]
    period: str