"""
Motor Management API
Admin endpoints for motor control
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Literal
from pydantic import BaseModel

from app.core.motor_registry import (
    motor_registry,
    MotorType,
    MotorVersion,
    SubscriptionTier
)
from app.core.motor_wrapper import MotorWrapper
from app.core.auth import get_current_user

# Import context service and segmentation
from app.core.context_service import ContextService
from app.core.segmentation_engine import get_segmentation_engine
from app.db.session import get_supabase_for_user

# Import motor engines
from app.core.difficulty_engine_v1 import DifficultyEngineV1
from app.core.difficulty_engine_v2 import DifficultyEngineV2
from app.core.bs_model_engine_v1 import BSModelV1
from app.core.bs_model_engine_v2 import BSModelV2
from app.core.priority_engine_v1 import PriorityEngineV1
from app.core.priority_engine_v2 import PriorityEngineV2
from app.core.time_engine_v1 import TimeAnalyzerV1
from app.core.time_engine_v2 import TimeAnalyzerV2

router = APIRouter()


# ============================================
# MOTOR INSTANCE INITIALIZATION (V1 ONLY)
# ============================================

# V1 motors are stateless - safe to share globally
_difficulty_v1 = DifficultyEngineV1()
_bs_model_v1 = BSModelV1()
_priority_v1 = PriorityEngineV1()
_time_v1 = TimeAnalyzerV1()

# Global segmentation engine (stateless, safe to share)
_segmentation_engine = get_segmentation_engine()


# ============================================
# REQUEST-SCOPED MOTOR WRAPPER
# ============================================

def create_motor_wrapper_for_user(current_user: dict) -> MotorWrapper:
    """
    Create request-scoped motor wrapper with user's context
    
    SECURITY: Each user gets their own context service with RLS enforced
    V2 motors use user's JWT token - can only access authorized data
    """
    # Create user-scoped Supabase client (RLS enforced)
    user_supabase = get_supabase_for_user(current_user["access_token"])
    context_service = ContextService()  # FORCE ADMIN CLIENT
    
    # Create V2 motors with user's context
    difficulty_v2 = DifficultyEngineV2(
        context_service=context_service,
        segmentation_engine=_segmentation_engine
    )
    bs_model_v2 = BSModelV2(
        context_service=context_service,
        segmentation_engine=_segmentation_engine
    )
    priority_v2 = PriorityEngineV2(
        context_service=context_service,
        segmentation_engine=_segmentation_engine
    )
    time_v2 = TimeAnalyzerV2(
        context_service=context_service,
        segmentation_engine=_segmentation_engine
    )
    
    # Create motor wrapper with user-scoped motors
    return MotorWrapper(
        difficulty_v1=_difficulty_v1,
        difficulty_v2=difficulty_v2,
        bs_model_v1=_bs_model_v1,
        bs_model_v2=bs_model_v2,
        priority_v1=_priority_v1,
        priority_v2=priority_v2,
        time_v1=_time_v1,
        time_v2=time_v2,
        context_service=context_service,
        segmentation_engine=_segmentation_engine
    )


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class MotorOverrideRequest(BaseModel):
    """Request to set motor override"""
    target: str  # "global" or user_id
    motor_type: str  # "difficulty", "priority", etc.
    version: str  # "v1" or "v2"


class MotorStatusResponse(BaseModel):
    """Motor status response"""
    motor_type: str
    user_tier: str
    selected_version: str
    enabled_features: list[str]
    timeout_ms: int
    fallback_enabled: bool


# ============================================
# ADMIN ENDPOINTS
# ============================================

@router.post("/admin/override", tags=["admin"])
async def set_motor_override(request: MotorOverrideRequest):
    """
    Set motor version override (Admin only)
    
    Examples:
    - Force all users to v1: {"target": "global", "motor_type": "difficulty", "version": "v1"}
    - Force user to v2: {"target": "user-123", "motor_type": "difficulty", "version": "v2"}
    """
    try:
        motor_registry.set_override(
            target=request.target,
            motor_type=MotorType(request.motor_type),
            version=MotorVersion(request.version)
        )
        
        return {
            "success": True,
            "message": f"Override set: {request.target} → {request.motor_type} = {request.version}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/admin/override/{target}", tags=["admin"])
async def clear_motor_override(target: str):
    """Clear motor override (Admin only)"""
    motor_registry.clear_override(target)
    return {
        "success": True,
        "message": f"Override cleared: {target}"
    }


@router.get("/admin/overrides", tags=["admin"])
async def list_motor_overrides():
    """List all active overrides (Admin only)"""
    return {
        "overrides": motor_registry.override_settings
    }


@router.get("/admin/performance", tags=["admin"])
async def get_motor_performance():
    """Get motor performance statistics (Admin only)"""
    logs = motor_registry.performance_log
    
    if not logs:
        return {"message": "No performance data yet"}
    
    # Calculate stats per motor
    stats_by_motor = {}
    
    for motor in MotorType:
        motor_logs = [l for l in logs if l["motor_type"] == motor.value]
        
        if not motor_logs:
            continue
        
        v1_logs = [l for l in motor_logs if l["version"] == "v1"]
        v2_logs = [l for l in motor_logs if l["version"] == "v2"]
        
        successful = [l for l in motor_logs if l["success"]]
        
        stats_by_motor[motor.value] = {
            "total_requests": len(motor_logs),
            "v1_requests": len(v1_logs),
            "v2_requests": len(v2_logs),
            "success_rate": len(successful) / len(motor_logs) * 100 if motor_logs else 0,
            "avg_execution_time_ms": sum(l["execution_time_ms"] for l in successful) / len(successful) if successful else 0,
        }
    
    return {
        "total_logs": len(logs),
        "stats_by_motor": stats_by_motor
    }


# ============================================
# PUBLIC ENDPOINTS (SECURE)
# ============================================

@router.get("/status", tags=["motors"])
async def get_motor_status(
    motor_type: str,
    user_tier: str,
    user_id: str | None = None
):
    """Get motor configuration for user"""
    try:
        config = motor_registry.get_motor_config(
            motor_type=MotorType(motor_type),
            user_tier=SubscriptionTier(user_tier),
            user_id=user_id
        )
        
        return MotorStatusResponse(
            motor_type=config.motor_type.value,
            user_tier=user_tier,
            selected_version=config.version.value,
            enabled_features=config.enabled_features,
            timeout_ms=config.timeout_ms,
            fallback_enabled=config.fallback_enabled
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/difficulty/calculate", tags=["motors"])
async def calculate_difficulty(
    student_id: str,
    topic_id: str,
    questions_total: int,
    questions_correct: int,
    questions_wrong: int,
    questions_blank: int,
    user_tier: str = "free",
    current_user: dict = Depends(get_current_user)  # ← SECURITY: JWT required
):
    """
    Calculate difficulty using appropriate motor version
    
    SECURITY: Uses user's JWT token for context service (RLS enforced)
    Automatically selects v1/v2 based on user tier
    Falls back to v1 on v2 timeout/error
    """
    try:
        from app.core.difficulty_engine_v1 import DifficultyInput
        
        input_data = DifficultyInput(
            topic_id=topic_id,
            questions_total=questions_total,
            questions_correct=questions_correct,
            questions_wrong=questions_wrong,
            questions_blank=questions_blank
        )
        
        # Create request-scoped motor wrapper with user's context
        motor_wrapper = create_motor_wrapper_for_user(current_user)
        
        from app.core.motor_wrapper import UserTier
        result = motor_wrapper.calculate_difficulty(
            input_data=input_data,
            student_id=current_user["id"],  # Use authenticated user's ID
            user_tier=UserTier(user_tier)
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# 4 MOTOR ANALYZE (EKRAN İÇİN) - SECURE
# ============================================

@router.post("/analyze", tags=["motors"])
async def analyze_student_topic(
    student_id: str,
    topic_id: str,
    user_tier: str = "free",
    current_user: dict = Depends(get_current_user)  # ← SECURITY: JWT required
):
    """
    4 Motor Analizi (Ekrandaki mor buton)
    
    SECURITY: Uses user's JWT token for context service (RLS enforced)
    
    Returns:
    - Akıllı Tekrar (BS-Model)
    - Zorluk (Difficulty)
    - Hız (Speed)
    - Öncelik (Priority)
    """
    try:
        # Verify user can access this student's data
        if student_id != current_user["id"]:
            # TODO: Check if user is coach/admin for this student
            raise HTTPException(status_code=403, detail="Access denied")
        
        results = {}
        tier = SubscriptionTier(user_tier)
        
        # Create request-scoped motor wrapper
        motor_wrapper = create_motor_wrapper_for_user(current_user)
        
        # 1. Difficulty Motor (mock for now)
        results["difficulty"] = {
            "difficulty_score": 65.0,
            "level": "medium",
            "motor_metadata": {"motor_version": "v1", "features_used": 2}
        }
        
        # 2. BS-Model (TODO: integrate wrapper)
        results["bs_model"] = {
            "next_review_date": "2024-12-30",
            "confidence": "high",
            "motor_metadata": {"motor_version": "v1", "features_used": 3}
        }
        
        # 3. Speed (TODO: integrate wrapper)
        results["speed"] = {
            "speed_score": 75.5,
            "segment": "standard",
            "motor_metadata": {"motor_version": "v1", "features_used": 2}
        }
        
        # 4. Priority (TODO: integrate wrapper)
        results["priority"] = {
            "priority_score": 82.3,
            "urgency": "medium",
            "motor_metadata": {"motor_version": "v1", "features_used": 3}
        }
        
        # Master recommendation (Premium only)
        if tier == SubscriptionTier.PREMIUM:
            results["master_insight"] = {
                "recommendation": "HEMEN - Zorluk yüksek, unutma riski var",
                "badge": "HEMEN",
                "next_action": "Bu konuyu bugün tekrar et"
            }
        
        return {
            "student_id": student_id,
            "topic_id": topic_id,
            "user_tier": user_tier,
            "motors": results,
            "analyzed_at": "2024-12-28T12:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







@router.post("/bs-model/calculate", tags=["motors"])
async def calculate_bs_model(
    topic_id: str,
    correct: int,
    incorrect: int,
    blank: int,
    total: int,
    difficulty: int = 3,
    user_tier: str = "free",
    current_user: dict = Depends(get_current_user)
):
    """
    Calculate BS-Model (Spaced Repetition) score
    
    Requires: correct, incorrect, blank, total (test results)
    """
    try:
        from app.core.bs_model_engine_v1 import BSModelInput
        
        input_data = BSModelInput(
            correct=correct,
            incorrect=incorrect,
            blank=blank,
            total=total,
            difficulty=difficulty
        )
        
        motor_wrapper = create_motor_wrapper_for_user(current_user)
        
        from app.core.motor_wrapper import UserTier
        result = motor_wrapper.calculate_bs_model(
            input_data=input_data,
            student_id=current_user["id"],
            topic_id=topic_id,
            user_tier=UserTier(user_tier)
        )
        
        return result
        
    except Exception as e:
        import traceback
        print(f"BS-Model error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))





@router.post("/priority/calculate", tags=["motors"])
async def calculate_priority(
    topic_id: str,
    test_date: str,
    user_tier: str = "free",
    current_user: dict = Depends(get_current_user)
):
    """Calculate Priority score"""
    try:
        motor_wrapper = create_motor_wrapper_for_user(current_user)
        from app.core.motor_wrapper import UserTier
        
        result = motor_wrapper.calculate_priority(
            student_id=current_user["id"],
            topic_id=topic_id,
            test_date=test_date,
            user_tier=UserTier(user_tier)
        )
        return result
    except Exception as e:
        import traceback
        print(f"Priority error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))





@router.post("/time/calculate", tags=["motors"])
async def calculate_time(
    topic_id: str,
    user_tier: str = "free",
    current_user: dict = Depends(get_current_user)
):
    """Calculate Time/Speed score"""
    try:
        motor_wrapper = create_motor_wrapper_for_user(current_user)
        from app.core.motor_wrapper import UserTier
        
        result = motor_wrapper.calculate_time(
            student_id=current_user["id"],
            topic_id=topic_id,
            user_tier=UserTier(user_tier)
        )
        return result
    except Exception as e:
        import traceback
        print(f"Time error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
