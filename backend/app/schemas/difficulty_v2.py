"""
Difficulty Analysis v2 Schemas
===============================

Pydantic models for Master Difficulty Engine v2.6 API.

Request/Response schemas with comprehensive validation.
Backward compatible with v1 for smooth migration.

Author: End.STP Team
Version: 2.0
Date: 2024-12-27
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from enum import Enum


# ============================================
# ENUMS
# ============================================

class StudentSegmentEnum(str, Enum):
    """Student performance segments"""
    STRUGGLING = "struggling"
    STANDARD = "standard"
    ELITE = "elite"


class BehaviorModeEnum(str, Enum):
    """Student behavior patterns"""
    NORMAL = "normal"
    HIGH_PRECISION = "high_precision"
    AT_RISK = "at_risk"
    PLATEAU = "plateau"
    ANOMALOUS_DECAY = "anomalous_decay"
    POSITIVE_BREAKTHROUGH = "positive_breakthrough"
    ERRATIC_WITH_ANOMALY = "erratic_with_anomaly"
    HIGH_RISK = "high_risk"


class TrendDirectionEnum(str, Enum):
    """Performance trend"""
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"


class ConfidenceLevelEnum(str, Enum):
    """Statistical confidence level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ============================================
# REQUEST SCHEMAS
# ============================================

class DifficultyCalculationRequest(BaseModel):
    """
    Request to calculate difficulty for a topic.
    
    Minimal required data: student_id, topic_id.
    System will fetch test history from database.
    """
    student_id: str = Field(..., description="Student UUID")
    topic_id: str = Field(..., description="Topic UUID")
    
    # Feature toggles (optional, defaults from subscription tier)
    enable_prerequisite: Optional[bool] = Field(None, description="Enable prerequisite analysis")
    enable_bs_model: Optional[bool] = Field(None, description="Enable BS-Model integration")
    enable_course_context: Optional[bool] = Field(None, description="Enable course context")
    enable_speed: Optional[bool] = Field(None, description="Enable speed normalization")
    enable_metacognition: Optional[bool] = Field(None, description="Enable metacognition gap")
    enable_digital_exhaust: Optional[bool] = Field(None, description="Enable digital exhaust")
    enable_circadian: Optional[bool] = Field(None, description="Enable circadian alignment")
    
    class Config:
        schema_extra = {
            "example": {
                "student_id": "550e8400-e29b-41d4-a716-446655440000",
                "topic_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "enable_prerequisite": True,
                "enable_bs_model": True
            }
        }


class ManualDifficultyRequest(BaseModel):
    """
    Manual calculation with provided test data.
    
    Used for testing, batch processing, or external integrations.
    Does not query database.
    """
    student_id: str = Field(..., description="Student UUID")
    topic_id: str = Field(..., description="Topic UUID")
    
    # Test data (manually provided)
    tests: List[Dict[str, Any]] = Field(..., description="List of test records")
    
    # Optional context data
    prerequisite_data: Optional[Dict] = Field(None, description="Prerequisite analysis")
    bs_model_data: Optional[Dict] = Field(None, description="BS-Model data")
    course_data: Optional[Dict] = Field(None, description="Course context")
    speed_benchmark: Optional[Dict] = Field(None, description="Speed benchmarks")
    feedback_data: Optional[Dict] = Field(None, description="Student feedback")
    learning_profile: Optional[Dict] = Field(None, description="Learning profile")
    exam_system: Optional[Dict] = Field(None, description="Exam system config")
    
    # Feature toggles
    enable_prerequisite: bool = Field(True)
    enable_bs_model: bool = Field(True)
    enable_course_context: bool = Field(True)
    enable_speed: bool = Field(True)
    enable_metacognition: bool = Field(True)
    enable_digital_exhaust: bool = Field(True)
    enable_circadian: bool = Field(True)
    
    @validator('tests')
    def validate_tests(cls, v):
        """Validate test data structure"""
        if not v:
            raise ValueError("At least one test required")
        
        for test in v:
            required_fields = [
                'test_id', 'topic_id', 'test_date', 
                'total_questions', 'correct', 'wrong', 'blank',
                'time_seconds', 'entry_timestamp'
            ]
            missing = [f for f in required_fields if f not in test]
            if missing:
                raise ValueError(f"Missing required fields in test: {missing}")
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "student_id": "550e8400-e29b-41d4-a716-446655440000",
                "topic_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "tests": [
                    {
                        "test_id": "test-001",
                        "topic_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                        "test_date": "2024-12-20",
                        "total_questions": 10,
                        "correct": 6,
                        "wrong": 2,
                        "blank": 2,
                        "time_seconds": 480,
                        "entry_timestamp": "2024-12-20T10:30:00Z"
                    }
                ]
            }
        }


# ============================================
# RESPONSE SCHEMAS
# ============================================

class DifficultyFactorsResponse(BaseModel):
    """Detailed breakdown of difficulty calculation factors"""
    
    # Core metrics
    base_difficulty: float = Field(..., ge=0, le=100, description="Base difficulty score")
    blank_weight: float = Field(..., description="Blank coefficient used")
    wrong_weight: float = Field(..., description="Wrong coefficient used")
    volatility: float = Field(..., ge=0, description="Performance volatility")
    
    # Enhancements
    prerequisite_ceiling: Optional[float] = Field(None, description="Max difficulty ceiling from prerequisites")
    bs_model_decay_risk: float = Field(0.0, description="Forgetting curve decay risk")
    course_context_multiplier: float = Field(1.0, description="Subject-level context multiplier")
    speed_penalty: float = Field(0.0, description="Speed normalization penalty")
    speed_warning: Optional[str] = Field(None, description="Speed warning message")
    time_decay_bonus: float = Field(0.0, description="Time decay adjustment")
    
    # Statistical
    confidence_score: float = Field(1.0, ge=0, le=1, description="Statistical confidence 0-1")
    confidence_warning: Optional[str] = Field(None, description="Confidence warning message")
    sample_size: int = Field(0, ge=0, description="Number of tests used")
    
    # Metacognition
    metacognitive_gap: float = Field(0.0, description="Self-assessment vs actual gap")
    trust_weighted_adjustment: float = Field(0.0, description="Trust score adjustment")
    
    # Behavioral
    digital_exhaust_factor: float = Field(1.0, description="Behavioral clues factor")
    recovery_velocity_bonus: float = Field(0.0, description="Resilience bonus")
    
    # Context
    exam_system_multiplier: float = Field(1.0, description="Exam system weight")
    circadian_penalty: float = Field(0.0, description="Study time penalty")
    circadian_timestamp: Optional[datetime] = Field(None, description="Test timestamp analyzed")
    
    # Counts
    daily_discarded_tests_count: int = Field(0, description="Tests filtered out (First-Contact Rule)")
    outliers_detected: int = Field(0, description="Outlier tests detected")
    
    class Config:
        schema_extra = {
            "example": {
                "base_difficulty": 45.5,
                "blank_weight": 0.55,
                "wrong_weight": 0.30,
                "volatility": 12.3,
                "prerequisite_ceiling": 75.0,
                "bs_model_decay_risk": 0.08,
                "course_context_multiplier": 1.1,
                "speed_penalty": 0.05,
                "confidence_score": 0.85,
                "sample_size": 5
            }
        }


class DifficultyResponse(BaseModel):
    """
    Comprehensive difficulty analysis result.
    
    Contains difficulty score, segment, behavior mode, factors, messages.
    """
    
    # Core results
    difficulty_percentage: float = Field(..., ge=0, le=100, description="Final difficulty 0-100")
    difficulty_level: int = Field(..., ge=1, le=5, description="Difficulty level 1-5")
    
    # Classification
    student_segment: StudentSegmentEnum = Field(..., description="Performance segment")
    behavior_mode: BehaviorModeEnum = Field(..., description="Behavioral pattern")
    trend: TrendDirectionEnum = Field(..., description="Performance trend")
    
    # Detailed factors
    factors: DifficultyFactorsResponse = Field(..., description="Calculation breakdown")
    
    # Messages
    student_message: str = Field(..., description="Student-facing message")
    coach_message: str = Field(..., description="Coach-facing message")
    recommendations: List[str] = Field(default_factory=list, description="Action recommendations")
    
    # Quality indicators
    confidence_level: ConfidenceLevelEnum = Field(..., description="Statistical confidence")
    warnings: List[str] = Field(default_factory=list, description="Warnings and alerts")
    
    # Metadata
    api_version: str = Field("2.0", description="API version")
    engine_version: str = Field("master_v2.6", description="Engine version")
    calculated_at: datetime = Field(default_factory=datetime.utcnow, description="Calculation timestamp (UTC)")
    
    class Config:
        schema_extra = {
            "example": {
                "difficulty_percentage": 58.7,
                "difficulty_level": 3,
                "student_segment": "standard",
                "behavior_mode": "normal",
                "trend": "improving",
                "factors": {
                    "base_difficulty": 45.5,
                    "volatility": 12.3,
                    "sample_size": 5
                },
                "student_message": "Moderate difficulty (59%). Continue practicing.",
                "coach_message": "Segment: standard | Mode: normal | Trend: improving",
                "recommendations": ["Practice speed exercises", "Review fundamentals"],
                "confidence_level": "high",
                "warnings": [],
                "api_version": "2.0",
                "engine_version": "master_v2.6"
            }
        }


# ============================================
# ERROR SCHEMAS
# ============================================

class DifficultyErrorResponse(BaseModel):
    """Error response for difficulty calculation"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp (UTC)")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "INSUFFICIENT_DATA",
                "message": "Need at least 3 tests for difficulty calculation",
                "details": {
                    "current_tests": 1,
                    "required_tests": 3
                },
                "timestamp": "2024-12-27T12:00:00Z"
            }
        }


# ============================================
# BATCH SCHEMAS
# ============================================

class BatchDifficultyRequest(BaseModel):
    """
    Calculate difficulty for multiple topics at once.
    
    Efficient for dashboard loading, batch reports.
    """
    student_id: str = Field(..., description="Student UUID")
    topic_ids: List[str] = Field(..., min_items=1, max_items=50, description="List of topic UUIDs (max 50)")
    
    # Feature toggles (applied to all)
    enable_prerequisite: Optional[bool] = None
    enable_bs_model: Optional[bool] = None
    enable_course_context: Optional[bool] = None
    enable_speed: Optional[bool] = None
    enable_metacognition: Optional[bool] = None
    enable_digital_exhaust: Optional[bool] = None
    enable_circadian: Optional[bool] = None
    
    @validator('topic_ids')
    def validate_unique_topics(cls, v):
        """Ensure no duplicate topics"""
        if len(v) != len(set(v)):
            raise ValueError("Duplicate topic_ids not allowed")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "student_id": "550e8400-e29b-41d4-a716-446655440000",
                "topic_ids": [
                    "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                    "7cb8c920-aebc-22e2-91c5-11d15fe541d9"
                ]
            }
        }


class BatchDifficultyResponse(BaseModel):
    """Batch calculation results"""
    results: List[DifficultyResponse] = Field(..., description="Difficulty results per topic")
    failed_topics: List[Dict[str, str]] = Field(default_factory=list, description="Topics that failed")
    total_topics: int = Field(..., description="Total topics requested")
    successful_topics: int = Field(..., description="Successfully calculated topics")
    
    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {
                        "difficulty_percentage": 58.7,
                        "difficulty_level": 3,
                        "student_segment": "standard",
                        "behavior_mode": "normal"
                    }
                ],
                "failed_topics": [],
                "total_topics": 2,
                "successful_topics": 2
            }
        }


# ============================================
# COMPARISON SCHEMAS
# ============================================

class DifficultyComparisonRequest(BaseModel):
    """
    Compare difficulty across multiple students for same topic.
    
    Used by coaches to compare student performance.
    """
    topic_id: str = Field(..., description="Topic UUID")
    student_ids: List[str] = Field(..., min_items=2, max_items=20, description="Student UUIDs (2-20)")
    
    class Config:
        schema_extra = {
            "example": {
                "topic_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "student_ids": [
                    "550e8400-e29b-41d4-a716-446655440000",
                    "660f9511-f3ac-52e5-b827-557766551111"
                ]
            }
        }


class StudentDifficultyComparison(BaseModel):
    """Single student comparison result"""
    student_id: str
    difficulty_percentage: float
    difficulty_level: int
    segment: StudentSegmentEnum
    behavior_mode: BehaviorModeEnum
    trend: TrendDirectionEnum


class DifficultyComparisonResponse(BaseModel):
    """Comparison results across students"""
    topic_id: str = Field(..., description="Topic UUID")
    topic_name: str = Field(..., description="Topic name")
    students: List[StudentDifficultyComparison] = Field(..., description="Student results")
    
    # Aggregate stats
    avg_difficulty: float = Field(..., description="Average difficulty across all students")
    min_difficulty: float = Field(..., description="Minimum difficulty")
    max_difficulty: float = Field(..., description="Maximum difficulty")
    
    class Config:
        schema_extra = {
            "example": {
                "topic_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "topic_name": "Türev Alma Kuralları",
                "students": [
                    {
                        "student_id": "550e8400-e29b-41d4-a716-446655440000",
                        "difficulty_percentage": 58.7,
                        "difficulty_level": 3,
                        "segment": "standard",
                        "behavior_mode": "normal",
                        "trend": "improving"
                    }
                ],
                "avg_difficulty": 58.7,
                "min_difficulty": 45.2,
                "max_difficulty": 72.3
            }
        }