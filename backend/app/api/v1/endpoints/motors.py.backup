"""
Motor Management API
Admin endpoints for motor control
"""
from fastapi import APIRouter, HTTPException
from typing import Literal
from pydantic import BaseModel

from app.core.motor_registry import (
    motor_registry,
    MotorType,
    MotorVersion,
    SubscriptionTier
)
from app.core.motor_wrapper import MotorWrapper

router = APIRouter()


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
# PUBLIC ENDPOINTS
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
    user_tier: str = "free"
):
    """
    Calculate difficulty using appropriate motor version
    
    Automatically selects v1/v2 based on user tier
    Falls back to v1 on v2 timeout/error
    """
    try:
        wrapper = MotorWrapper(MotorType.DIFFICULTY)
        
        result = await wrapper.execute(
            user_id=student_id,
            user_tier=SubscriptionTier(user_tier),
            student_id=student_id,
            topic_id=topic_id
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# 4 MOTOR ANALYZE (EKRAN İÇİN)
# ============================================

@router.post("/analyze", tags=["motors"])
async def analyze_student_topic(
    student_id: str,
    topic_id: str,
    user_tier: str = "free"
):
    """
    4 Motor Analizi (Ekrandaki mor buton)
    
    Returns:
    - Akıllı Tekrar (BS-Model)
    - Zorluk (Difficulty)
    - Hız (Speed)
    - Öncelik (Priority)
    """
    try:
        results = {}
        tier = SubscriptionTier(user_tier)
        
        # 1. Difficulty Motor
        difficulty_wrapper = MotorWrapper(MotorType.DIFFICULTY)
        results["difficulty"] = await difficulty_wrapper.execute(
            user_id=student_id,
            user_tier=tier,
            student_id=student_id,
            topic_id=topic_id
        )
        
        # 2. BS-Model (TODO: henüz wrapper yok)
        results["bs_model"] = {
            "next_review_date": "2024-12-30",
            "confidence": "high",
            "motor_metadata": {"motor_version": "v1", "features_used": 3}
        }
        
        # 3. Speed (TODO: henüz wrapper yok)
        results["speed"] = {
            "speed_score": 75.5,
            "segment": "standard",
            "motor_metadata": {"motor_version": "v1", "features_used": 2}
        }
        
        # 4. Priority (TODO: henüz wrapper yok)
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
