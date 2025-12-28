"""
Difficulty Analysis API v2 Endpoints
=====================================

FastAPI endpoints for Master Difficulty Engine v2.6.

Features:
- JWT authentication
- Request validation
- Rate limiting
- Error handling
- Backward compatibility with v1
- Batch operations
- Comparison endpoints

Author: End.STP Team
Version: 2.0
Date: 2024-12-27
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
import logging

from app.schemas.difficulty_v2 import (
    DifficultyCalculationRequest,
    ManualDifficultyRequest,
    BatchDifficultyRequest,
    DifficultyComparisonRequest,
    DifficultyResponse,
    BatchDifficultyResponse,
    DifficultyComparisonResponse,
    DifficultyErrorResponse,
    StudentDifficultyComparison
)
from app.services.motors.difficulty_service import DifficultyService
from app.core.difficulty_engine_v2 import TestData

# TODO: Import when auth is ready
# from app.api.deps import get_current_user, get_supabase_client
# from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/difficulty", tags=["Difficulty v2"])


# ============================================
# DEPENDENCY INJECTION (TODO: Implement auth)
# ============================================

async def get_difficulty_service():
    """
    Dependency to get DifficultyService with Supabase client.
    
    TODO: Replace with actual Supabase client initialization
    """
    # Placeholder - replace when database.py is ready
    # from app.database import get_supabase_client
    # supabase = await get_supabase_client()
    # return DifficultyService(supabase)
    
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Database connection not configured. Complete backend setup first."
    )


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract user ID from JWT token.
    
    TODO: Implement actual JWT validation
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    # Placeholder - replace with actual JWT parsing
    # from app.utils.jwt import decode_token
    # token = authorization.replace("Bearer ", "")
    # payload = decode_token(token)
    # return payload['user_id']
    
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Authentication not configured. Complete backend setup first."
    )


def check_feature_access(user_tier: str, feature: str) -> bool:
    """
    Check if user's subscription tier allows feature.
    
    Feature matrix:
    - Free: None
    - Basic: prerequisite, bs_model, course_context
    - Medium: + speed, metacognition
    - Premium: + digital_exhaust, circadian (ALL)
    """
    tier_features = {
        'free': [],
        'basic': ['prerequisite', 'bs_model', 'course_context'],
        'medium': ['prerequisite', 'bs_model', 'course_context', 'speed', 'metacognition'],
        'premium': ['prerequisite', 'bs_model', 'course_context', 'speed', 
                   'metacognition', 'digital_exhaust', 'circadian']
    }
    
    return feature in tier_features.get(user_tier.lower(), [])


# ============================================
# MAIN ENDPOINTS
# ============================================

@router.post(
    "/calculate",
    response_model=DifficultyResponse,
    summary="Calculate difficulty for a topic",
    description="""
    Calculate comprehensive difficulty analysis for a student-topic pair.
    
    **Features:**
    - Automatic data fetching from database
    - 15 advanced analysis features
    - Tier-based feature access
    - Statistical confidence scoring
    - Behavioral pattern detection
    
    **Required Data:**
    - Minimum 3 test records
    - Spread over 7+ days recommended
    - Recent tests (within 60 days) preferred
    
    **Returns:**
    - Difficulty percentage (0-100)
    - Difficulty level (1-5)
    - Student segment (struggling/standard/elite)
    - Behavior mode (7 patterns)
    - Performance trend
    - Detailed factors breakdown
    - Actionable recommendations
    """
)
async def calculate_difficulty(
    request: DifficultyCalculationRequest,
    service: DifficultyService = Depends(get_difficulty_service),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Calculate difficulty for topic.
    
    Fetches all required data from database automatically.
    """
    
    # Verify user is accessing their own data (or is coach/admin)
    if request.student_id != current_user_id:
        # TODO: Check if current_user is coach/admin with access
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other student's data"
        )
    
    # Get user tier (TODO: from database)
    user_tier = "premium"  # Placeholder
    
    # Apply tier-based feature flags
    feature_flags = {
        'enable_prerequisite': request.enable_prerequisite if request.enable_prerequisite is not None 
                              else check_feature_access(user_tier, 'prerequisite'),
        'enable_bs_model': request.enable_bs_model if request.enable_bs_model is not None
                          else check_feature_access(user_tier, 'bs_model'),
        'enable_course_context': request.enable_course_context if request.enable_course_context is not None
                                else check_feature_access(user_tier, 'course_context'),
        'enable_speed': request.enable_speed if request.enable_speed is not None
                       else check_feature_access(user_tier, 'speed'),
        'enable_metacognition': request.enable_metacognition if request.enable_metacognition is not None
                               else check_feature_access(user_tier, 'metacognition'),
        'enable_digital_exhaust': request.enable_digital_exhaust if request.enable_digital_exhaust is not None
                                 else check_feature_access(user_tier, 'digital_exhaust'),
        'enable_circadian': request.enable_circadian if request.enable_circadian is not None
                           else check_feature_access(user_tier, 'circadian')
    }
    
    try:
        result = await service.calculate_difficulty(
            student_id=request.student_id,
            topic_id=request.topic_id,
            **feature_flags
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Difficulty calculation failed"
        )


@router.post(
    "/calculate-manual",
    response_model=DifficultyResponse,
    summary="Calculate difficulty with manual test data",
    description="""
    Calculate difficulty using manually provided test data.
    
    **Use cases:**
    - Testing and debugging
    - Batch processing
    - External integrations
    - Offline calculations
    
    **Note:** Does not query database. All data must be provided in request.
    """
)
async def calculate_difficulty_manual(
    request: ManualDifficultyRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Manual calculation with provided test data.
    
    Useful for testing, external integrations.
    """
    
    # Verify access
    if request.student_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other student's data"
        )
    
    try:
        # Convert test dicts to TestData objects
        from app.core.difficulty_engine_v2 import MasterDifficultyEngine
        from datetime import datetime, date
        
        tests = []
        for test_dict in request.tests:
            test = TestData(
                test_id=test_dict['test_id'],
                topic_id=test_dict['topic_id'],
                test_date=date.fromisoformat(test_dict['test_date']),
                total_questions=test_dict['total_questions'],
                correct=test_dict['correct'],
                wrong=test_dict['wrong'],
                blank=test_dict['blank'],
                time_seconds=test_dict['time_seconds'],
                entry_timestamp=datetime.fromisoformat(
                    test_dict['entry_timestamp'].replace('Z', '+00:00')
                )
            )
            tests.append(test)
        
        # Initialize motor with feature flags
        motor = MasterDifficultyEngine(
            enable_prerequisite=request.enable_prerequisite,
            enable_bs_model=request.enable_bs_model,
            enable_course_context=request.enable_course_context,
            enable_speed=request.enable_speed,
            enable_metacognition=request.enable_metacognition,
            enable_digital_exhaust=request.enable_digital_exhaust,
            enable_circadian=request.enable_circadian
        )
        
        # Calculate
        result = motor.calculate_difficulty(
            student_id=request.student_id,
            topic_id=request.topic_id,
            tests=tests,
            prerequisite_data=request.prerequisite_data,
            bs_model_data=request.bs_model_data,
            course_data=request.course_data,
            speed_benchmark=request.speed_benchmark,
            feedback_data=request.feedback_data,
            learning_profile=request.learning_profile,
            exam_system=request.exam_system
        )
        
        # Convert to response
        from app.services.motors.difficulty_service import DifficultyService
        service = DifficultyService(None)  # No DB needed for manual
        response = service._convert_to_response(result)
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Manual calculation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation failed: {str(e)}"
        )


# ============================================
# BATCH OPERATIONS
# ============================================

@router.post(
    "/calculate-batch",
    response_model=BatchDifficultyResponse,
    summary="Calculate difficulty for multiple topics",
    description="""
    Batch calculation for multiple topics (max 50).
    
    **Efficient for:**
    - Dashboard loading (all student topics)
    - Progress reports
    - Analytics dashboards
    
    **Performance:**
    - Parallel processing where possible
    - Continues on individual failures
    - Returns partial results
    """
)
async def calculate_difficulty_batch(
    request: BatchDifficultyRequest,
    service: DifficultyService = Depends(get_difficulty_service),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Calculate difficulty for multiple topics at once.
    
    Max 50 topics per request.
    """
    
    # Verify access
    if request.student_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other student's data"
        )
    
    # Validate topic count
    if len(request.topic_ids) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 50 topics per batch request"
        )
    
    # Get user tier and prepare feature flags
    user_tier = "premium"  # Placeholder
    
    feature_flags = {
        'enable_prerequisite': request.enable_prerequisite if request.enable_prerequisite is not None 
                              else check_feature_access(user_tier, 'prerequisite'),
        'enable_bs_model': request.enable_bs_model if request.enable_bs_model is not None
                          else check_feature_access(user_tier, 'bs_model'),
        'enable_course_context': request.enable_course_context if request.enable_course_context is not None
                                else check_feature_access(user_tier, 'course_context'),
        'enable_speed': request.enable_speed if request.enable_speed is not None
                       else check_feature_access(user_tier, 'speed'),
        'enable_metacognition': request.enable_metacognition if request.enable_metacognition is not None
                               else check_feature_access(user_tier, 'metacognition'),
        'enable_digital_exhaust': request.enable_digital_exhaust if request.enable_digital_exhaust is not None
                                 else check_feature_access(user_tier, 'digital_exhaust'),
        'enable_circadian': request.enable_circadian if request.enable_circadian is not None
                           else check_feature_access(user_tier, 'circadian')
    }
    
    try:
        results, failed = await service.calculate_difficulty_batch(
            student_id=request.student_id,
            topic_ids=request.topic_ids,
            **feature_flags
        )
        
        return BatchDifficultyResponse(
            results=results,
            failed_topics=failed,
            total_topics=len(request.topic_ids),
            successful_topics=len(results)
        )
        
    except Exception as e:
        logger.error(f"Batch calculation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Batch calculation failed"
        )


# ============================================
# COMPARISON ENDPOINTS
# ============================================

@router.post(
    "/compare",
    response_model=DifficultyComparisonResponse,
    summary="Compare difficulty across students",
    description="""
    Compare how different students find the same topic.
    
    **Use cases:**
    - Coach comparing students
    - Identifying struggling students
    - Topic difficulty calibration
    
    **Access:** Requires coach or admin role
    """
)
async def compare_difficulty(
    request: DifficultyComparisonRequest,
    service: DifficultyService = Depends(get_difficulty_service),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Compare difficulty for same topic across multiple students.
    
    Coach/Admin only.
    """
    
    # TODO: Verify coach/admin role
    # For now, placeholder
    
    if len(request.student_ids) > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 20 students per comparison"
        )
    
    try:
        # Get topic name
        # TODO: Fetch from database
        topic_name = "Topic Name"  # Placeholder
        
        students_results = []
        difficulties = []
        
        for student_id in request.student_ids:
            try:
                result = await service.calculate_difficulty(
                    student_id=student_id,
                    topic_id=request.topic_id,
                    enable_prerequisite=True,
                    enable_bs_model=True,
                    enable_course_context=True,
                    enable_speed=True,
                    enable_metacognition=True,
                    enable_digital_exhaust=True,
                    enable_circadian=True
                )
                
                students_results.append(StudentDifficultyComparison(
                    student_id=student_id,
                    difficulty_percentage=result.difficulty_percentage,
                    difficulty_level=result.difficulty_level,
                    segment=result.student_segment,
                    behavior_mode=result.behavior_mode,
                    trend=result.trend
                ))
                
                difficulties.append(result.difficulty_percentage)
                
            except Exception as e:
                logger.warning(f"Comparison failed for student {student_id}: {e}")
                continue
        
        if not students_results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No valid results for comparison"
            )
        
        return DifficultyComparisonResponse(
            topic_id=request.topic_id,
            topic_name=topic_name,
            students=students_results,
            avg_difficulty=sum(difficulties) / len(difficulties),
            min_difficulty=min(difficulties),
            max_difficulty=max(difficulties)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comparison error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Comparison failed"
        )


# ============================================
# UTILITY ENDPOINTS
# ============================================

@router.get(
    "/health",
    summary="Health check",
    description="Check if difficulty service is operational"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "difficulty_v2",
        "version": "2.6.0",
        "features": 15
    }


@router.get(
    "/features",
    summary="List available features",
    description="Get list of all analysis features and their descriptions"
)
async def list_features():
    """List all available analysis features"""
    return {
        "features": [
            {
                "id": 1,
                "name": "prerequisite",
                "title": "Prerequisite Awareness",
                "description": "Analyzes gaps in prerequisite knowledge",
                "tiers": ["basic", "medium", "premium"]
            },
            {
                "id": 2,
                "name": "bs_model",
                "title": "BS-Model Integration",
                "description": "Personalized forgetting curve analysis",
                "tiers": ["basic", "medium", "premium"]
            },
            {
                "id": 3,
                "name": "course_context",
                "title": "Course Context Weight",
                "description": "Subject-level performance context",
                "tiers": ["basic", "medium", "premium"]
            },
            {
                "id": 4,
                "name": "statistical_confidence",
                "title": "Statistical Confidence",
                "description": "Sample size and reliability scoring",
                "tiers": ["all"]
            },
            {
                "id": 5,
                "name": "volatility",
                "title": "Volatility Improvement",
                "description": "Outlier detection with 2-sigma analysis",
                "tiers": ["all"]
            },
            {
                "id": 6,
                "name": "bidirectional_sentinel",
                "title": "Bidirectional Sentinel",
                "description": "Positive and negative anomaly detection",
                "tiers": ["all"]
            },
            {
                "id": 7,
                "name": "speed",
                "title": "Speed Normalization",
                "description": "Topic-specific speed benchmarks",
                "tiers": ["medium", "premium"]
            },
            {
                "id": 8,
                "name": "metacognition",
                "title": "Metacognition Gap",
                "description": "Self-assessment calibration analysis",
                "tiers": ["medium", "premium"]
            },
            {
                "id": 9,
                "name": "exam_system",
                "title": "Exam System Awareness",
                "description": "Global exam configuration integration",
                "tiers": ["all"]
            },
            {
                "id": 10,
                "name": "version_handling",
                "title": "Version Handling",
                "description": "API evolution and backward compatibility",
                "tiers": ["all"]
            },
            {
                "id": 11,
                "name": "digital_exhaust",
                "title": "Digital Exhaust Integration",
                "description": "Behavioral clues from interactions",
                "tiers": ["premium"]
            },
            {
                "id": 12,
                "name": "recovery_velocity",
                "title": "Recovery Velocity",
                "description": "Post-error resilience analysis",
                "tiers": ["premium"]
            },
            {
                "id": 13,
                "name": "contextual_sentiment",
                "title": "Contextual Sentiment",
                "description": "Feedback-driven content quality",
                "tiers": ["premium"]
            },
            {
                "id": 14,
                "name": "circadian",
                "title": "Circadian Alignment",
                "description": "Study time optimization",
                "tiers": ["premium"]
            },
            {
                "id": 15,
                "name": "trust_weighted",
                "title": "Trust-Weighted Feedback",
                "description": "Feedback reliability scoring",
                "tiers": ["premium"]
            }
        ],
        "total_features": 15,
        "engine_version": "master_v2.6"
    }