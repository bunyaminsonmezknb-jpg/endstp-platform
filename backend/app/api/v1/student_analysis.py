"""
Student Analysis API
4 motoru birleştiren ana endpoint
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

# Motor importları - DOĞRU isimler!
from app.core.bs_model_engine import BSModel, ReviewInput
from app.core.difficulty_engine import DifficultyEngine, StatMetrics, DifficultyResult
from app.core.time_engine import TimeAnalyzer
from app.core.priority_engine import PriorityEngine, TopicInput

router = APIRouter(prefix="/api/v1/student", tags=["Student Analysis"])


# ============================================
# REQUEST & RESPONSE MODELS
# ============================================

class TopicTestInput(BaseModel):
    """Tek bir konu testi girdi"""
    topic_id: int
    topic_name: str
    correct: int = Field(ge=0)
    incorrect: int = Field(ge=0)
    blank: int = Field(ge=0)
    total_questions: int = Field(gt=0)
    
    # BS-Model için
    current_ease_factor: Optional[float] = None
    current_interval: Optional[int] = None
    actual_gap_days: Optional[int] = None
    repetitions: int = 0
    
    # Time Analyzer için
    duration_minutes: Optional[float] = None
    
    # Priority için
    topic_weight: float = Field(default=0.025, ge=0, le=1)
    course_importance: float = Field(default=40, ge=0)
    difficulty_baseline: int = Field(default=3, ge=1, le=5)


class CourseContextInput(BaseModel):
    """Ders geneli context"""
    course_id: int
    course_name: str
    total_correct: int = Field(ge=0)
    total_incorrect: int = Field(ge=0)
    total_blank: int = Field(ge=0)
    total_questions: int = Field(gt=0)


class AnalyzeRequest(BaseModel):
    """Ana analiz request"""
    student_id: str
    topics: List[TopicTestInput]
    course_context: Optional[CourseContextInput] = None


class TopicAnalysisOutput(BaseModel):
    """Tek bir konunun tam analizi"""
    topic_id: int
    topic_name: str
    next_review_date: str
    next_ease_factor: float
    next_interval: int
    status: str
    difficulty_level: int
    difficulty_percentage: float
    pace_ratio: float
    time_modifier: float
    speed_note: str
    priority_score: float
    priority_level: str
    suggestion: str


class AnalyzeResponse(BaseModel):
    """Ana analiz response"""
    student_id: str
    analyzed_at: str
    topics: List[TopicAnalysisOutput]
    summary: dict


# ============================================
# ENDPOINT
# ============================================

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_student_topics(request: AnalyzeRequest):
    """4 motoru çalıştır"""
    
    if not request.topics:
        raise HTTPException(400, "En az 1 konu gerekli")
    
    course_stats = None
    if request.course_context:
        cc = request.course_context
        course_stats = StatMetrics(
            total_questions=cc.total_questions,
            correct=cc.total_correct,
            wrong=cc.total_incorrect,
            blank=cc.total_blank,
            net=cc.total_correct - (cc.total_incorrect * 0.25)
        )
    
    priority_inputs = []
    results = []
    
    for topic in request.topics:
        # BS-MODEL
        bs_result = BSModel.calculate(ReviewInput(
            correct=topic.correct,
            incorrect=topic.incorrect,
            blank=topic.blank,
            total=topic.total_questions,
            difficulty=topic.difficulty_baseline,
            current_ef=topic.current_ease_factor,
            current_ia=topic.current_interval,
            actual_gap=topic.actual_gap_days,
            repetitions=topic.repetitions
        ))
        
        next_review = datetime.now() + timedelta(days=bs_result.next_ia)
        
        # DIFFICULTY ENGINE
        topic_stats = StatMetrics(
            total_questions=topic.total_questions,
            correct=topic.correct,
            wrong=topic.incorrect,
            blank=topic.blank,
            net=topic.correct - (topic.incorrect * 0.25)
        )
        
        diff_result = DifficultyEngine.calculate(
            topic_stats=topic_stats,
            course_total_stats=course_stats
        )
        
        # TIME ANALYZER
        success_rate = topic.correct / topic.total_questions
        time_result = TimeAnalyzer.analyze(
            total_duration=topic.duration_minutes,
            total_questions=topic.total_questions,
            ideal_time_per_question=1.5,
            success_rate=success_rate
        )
        
        # PRIORITY INPUT
        priority_inputs.append(TopicInput(
            id=str(topic.topic_id),
            name=topic.topic_name,
            correct=topic.correct,
            wrong=topic.incorrect,
            blank=topic.blank,
            total_questions=topic.total_questions,
            duration_minutes=topic.duration_minutes,
            topic_weight=topic.topic_weight,
            course_importance=topic.course_importance
        ))
        
        results.append({
            "topic_id": topic.topic_id,
            "topic_name": topic.topic_name,
            "bs_result": bs_result,
            "diff_result": diff_result,
            "time_result": time_result,
            "next_review_date": next_review.strftime("%Y-%m-%d")
        })
    
    # PRIORITY ENGINE
    priority_results = PriorityEngine.analyze(priority_inputs)
    priority_map = {p.topic_id: p for p in priority_results}
    
    final_topics = []
    for r in results:
        topic_id = str(r["topic_id"])
        priority = priority_map.get(topic_id)
        
        final_topics.append(TopicAnalysisOutput(
            topic_id=r["topic_id"],
            topic_name=r["topic_name"],
            next_review_date=r["next_review_date"],
            next_ease_factor=r["bs_result"].next_ef,
            next_interval=r["bs_result"].next_ia,
            status=r["bs_result"].status,
            difficulty_level=r["diff_result"].difficulty_level,
            difficulty_percentage=r["diff_result"].difficulty_percentage,
            pace_ratio=r["time_result"].pace_ratio,
            time_modifier=r["time_result"].time_modifier,
            speed_note=r["time_result"].analysis,
            priority_score=priority.priority_score if priority else 0,
            priority_level=priority.priority_level if priority else "LOW",
            suggestion=priority.suggestion if priority else ""
        ))
    
    final_topics.sort(key=lambda x: x.priority_score, reverse=True)
    
    critical_count = sum(1 for t in final_topics if t.priority_level == "CRITICAL")
    high_count = sum(1 for t in final_topics if t.priority_level == "HIGH")
    
    return AnalyzeResponse(
        student_id=request.student_id,
        analyzed_at=datetime.now().isoformat(),
        topics=final_topics,
        summary={
            "total_topics": len(final_topics),
            "critical_topics": critical_count,
            "high_priority_topics": high_count,
            "next_review_today": sum(1 for t in final_topics if t.next_interval <= 1)
        }
    )


@router.get("/health")
async def health_check():
    """Motor durumu"""
    return {
        "status": "healthy",
        "motors": {
            "bs_model": "active",
            "difficulty_engine": "active",
            "time_analyzer": "active",
            "priority_engine": "active"
        }
    }
