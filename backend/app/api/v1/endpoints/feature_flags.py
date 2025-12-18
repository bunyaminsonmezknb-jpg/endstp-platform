"""
Feature Flags - Health-Aware Control System
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

from app.db.session import get_supabase_admin
from app.core.auth import get_current_user

router = APIRouter()


class ToggleFlagRequest(BaseModel):
    reason: Optional[str] = None


class ReportErrorRequest(BaseModel):
    error_message: str
    error_trace: Optional[str] = None
    error_function: Optional[str] = None
    response_time_ms: Optional[int] = None
    rows_processed: Optional[int] = None


@router.get("")
async def get_public_flags():
    """
    Public endpoint - only enabled flags
    Motor/backend flags filtered out
    """
    supabase = get_supabase_admin()
    result = (
        supabase.table("feature_flags")
        .select("flag_key, is_enabled")
        .eq("is_enabled", True)
        .execute()
    )
    
    # Filter out backend-only flags
    public_flags = {
        f["flag_key"]: f["is_enabled"] 
        for f in (result.data or [])
        if not any(x in f["flag_key"] for x in ['_calculation', '_analysis', 'motor_driven'])
    }
    
    return {"flags": public_flags}


@router.get("/admin")
async def get_admin_flags():
    """Admin - all flags with health metrics"""
    supabase = get_supabase_admin()
    result = (
        supabase.table("feature_flags")
        .select("*")
        .order("phase", desc=False)
        .order("flag_key", desc=False)
        .execute()
    )
    return {"flags": result.data or []}


@router.post("/{flag_key}/toggle")
async def toggle_flag(
    flag_key: str, 
    request: ToggleFlagRequest
):
    """Toggle feature flag on/off"""
    supabase = get_supabase_admin()
    
    # Get current state
    flag_result = supabase.table("feature_flags").select("*").eq("flag_key", flag_key).execute()
    if not flag_result.data:
        raise HTTPException(404, "Flag not found")
    
    current_state = flag_result.data[0]["is_enabled"]
    new_state = not current_state
    
    # Prepare update
    update_data = {
        "is_enabled": new_state,
        "updated_at": datetime.utcnow().isoformat()
    }
    
    if not new_state:  # Disabling
        update_data["disabled_reason"] = request.reason or "Manual disable"
        update_data["disabled_by"] = "internal-admin"
        update_data["disabled_at"] = datetime.utcnow().isoformat()
    else:  # Enabling
        update_data["disabled_reason"] = None
        update_data["disabled_by"] = None
        update_data["disabled_at"] = None
        update_data["error_count"] = 0
        update_data["health_score"] = 100
    
    result = supabase.table("feature_flags").update(update_data).eq("flag_key", flag_key).execute()
    
    print(f"🎛️  Flag toggled: {flag_key} → {new_state}")
    
    return {
        "success": True, 
        "flag_key": flag_key, 
        "is_enabled": new_state
    }


class ReportErrorRequest(BaseModel):
    error_message: str
    error_trace: Optional[str] = None
    error_function: Optional[str] = None
    response_time_ms: Optional[int] = None
    rows_processed: Optional[int] = None

@router.post("/{flag_key}/report-error")
async def report_flag_error(flag_key: str, request: ReportErrorRequest):
    """Enhanced error reporting with runtime metrics"""
    supabase = get_supabase_admin()
    
    flag_result = supabase.table("feature_flags").select("*").eq("flag_key", flag_key).execute()
    if not flag_result.data:
        return {"success": False, "message": "Flag not found"}
    
    flag = flag_result.data[0]
    new_error_count = flag["error_count"] + 1
    
    # Health breakdown calculation
    latency_score = 100
    if request.response_time_ms:
        if request.response_time_ms > 5000:
            latency_score = 0
        elif request.response_time_ms > 2000:
            latency_score = 50
        elif request.response_time_ms > 1000:
            latency_score = 75
    
    error_score = max(0, 100 - (new_error_count * 10))
    data_volume_score = 100
    if request.rows_processed and request.rows_processed > 100000:
        data_volume_score = 50
    
    # Overall health = average of scores
    new_health = int((latency_score + error_score + data_volume_score + 100) / 4)
    
    # Severity detection
    error_msg = request.error_message.lower()
    severity = 'low'
    if any(word in error_msg for word in ['sql', 'timeout', 'database']):
        severity = 'high'
    if any(word in error_msg for word in ['crash', 'fatal', 'critical']):
        severity = 'critical'
    
    user_impact = 'high' if flag.get('phase') == 'mvp' else 'medium'
    if new_health < 50:
        user_impact = 'critical'
    
    # Error timeline
    error_timeline = flag.get('error_timeline', [])
    if not isinstance(error_timeline, list):
        error_timeline = []
    
    error_timeline.append({
        "timestamp": datetime.utcnow().isoformat(),
        "message": request.error_message[:100],
        "severity": severity,
        "function": request.error_function
    })
    
    # Keep last 20 errors
    error_timeline = error_timeline[-20:]
    
    update_data = {
        "error_count": new_error_count,
        "health_score": new_health,
        "last_error_at": datetime.utcnow().isoformat(),
        "last_error_message": request.error_message[:500],
        "last_error_trace": request.error_trace[:2000] if request.error_trace else None,
        "last_error_function": request.error_function,
        "error_severity": severity,
        "user_impact_level": user_impact,
        "error_rate_percent": min(100, (new_error_count / 100) * 100),
        "latency_score": latency_score,
        "error_score": error_score,
        "data_volume_score": data_volume_score,
        "error_timeline": error_timeline,
        "avg_response_time_ms": request.response_time_ms,
        "rows_processed": request.rows_processed
    }
    
    # Auto-disable if critical
    auto_disabled = False
    if new_health < 30 or severity == 'critical':
        update_data["is_enabled"] = False
        update_data["disabled_reason"] = f"Auto-disabled: {severity.upper()} - {request.error_message[:100]}"
        update_data["disabled_at"] = datetime.utcnow().isoformat()
        update_data["disabled_by"] = "system"
        auto_disabled = True
        print(f"🚨 CRITICAL AUTO-DISABLE: {flag_key}")
    
    supabase.table("feature_flags").update(update_data).eq("flag_key", flag_key).execute()
    
    return {
        "success": True,
        "health_score": new_health,
        "latency_score": latency_score,
        "error_score": error_score,
        "data_volume_score": data_volume_score,
        "severity": severity,
        "auto_disabled": auto_disabled
    }
# ============================================
# ENHANCED ERROR REPORTING & QUICK ACTIONS
# ============================================

@router.get("/health-status")
async def get_health_status():
    """Quick health check - critical alerts monitoring"""
    supabase = get_supabase_admin()
    
    result = supabase.table("feature_flags").select("*").execute()
    flags = result.data or []
    
    critical_count = len([f for f in flags if f.get('error_severity') == 'critical'])
    high_count = len([f for f in flags if f.get('error_severity') == 'high'])
    disabled_count = len([f for f in flags if not f.get('is_enabled')])
    low_health_count = len([f for f in flags if f.get('health_score', 100) < 50])
    
    critical_flags = [
        {
            "flag_key": f["flag_key"],
            "description": f.get("description", ""),
            "health_score": f["health_score"],
            "error_count": f["error_count"],
            "severity": f.get("error_severity", "low"),
            "user_impact": f.get("user_impact_level", "none"),
            "is_enabled": f["is_enabled"]
        }
        for f in flags 
        if f.get('error_severity') in ['critical', 'high'] or f['health_score'] < 50
    ]
    
    overall_status = "critical" if critical_count > 0 else "warning" if high_count > 0 else "healthy"
    
    return {
        "status": overall_status,
        "critical_count": critical_count,
        "high_count": high_count,
        "disabled_count": disabled_count,
        "low_health_count": low_health_count,
        "critical_flags": critical_flags,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/{flag_key}/quick-action")
async def quick_action(
    flag_key: str,
    action: str
):
    """Quick action buttons: reset_health, clear_errors, attempt_recovery"""
    supabase = get_supabase_admin()
    
    # Verify flag exists
    flag_result = supabase.table("feature_flags").select("*").eq("flag_key", flag_key).execute()
    if not flag_result.data:
        raise HTTPException(404, "Flag not found")
    
    flag = flag_result.data[0]
    update_data = {"updated_at": datetime.utcnow().isoformat()}
    
    if action == 'reset_health':
        update_data.update({
            "health_score": 100,
            "error_count": 0,
            "error_severity": "low",
            "error_rate_percent": 0,
            "last_error_at": None
        })
        print(f"💚 Health reset: {flag_key}")
        
    elif action == 'clear_errors':
        update_data.update({
            "error_count": 0,
            "last_error_at": None,
            "error_severity": "low",
            "error_rate_percent": 0
        })
        print(f"🧹 Errors cleared: {flag_key}")
        
    elif action == 'attempt_recovery':
        current_attempts = flag.get("recovery_attempts", 0)
        update_data.update({
            "recovery_attempts": current_attempts + 1,
            "last_recovery_attempt_at": datetime.utcnow().isoformat()
        })
        print(f"🔄 Recovery attempt #{current_attempts + 1}: {flag_key}")
        
    else:
        raise HTTPException(400, f"Unknown action: {action}")
    
    result = supabase.table("feature_flags").update(update_data).eq("flag_key", flag_key).execute()
    
    return {
        "success": True,
        "action": action,
        "flag_key": flag_key,
        "message": f"Action '{action}' completed successfully"
    }


# Enhanced error reporting (replace existing report-error)
@router.post("/{flag_key}/report-error")
async def report_flag_error(flag_key: str, request: ReportErrorRequest):
    """Enhanced error reporting with runtime metrics & health breakdown"""
    supabase = get_supabase_admin()
    
    flag_result = supabase.table("feature_flags").select("*").eq("flag_key", flag_key).execute()
    if not flag_result.data:
        return {"success": False, "message": "Flag not found"}
    
    flag = flag_result.data[0]
    new_error_count = flag["error_count"] + 1
    
    # ============================================
    # HEALTH BREAKDOWN CALCULATION
    # ============================================
    
    # 1. Latency Score
    latency_score = 100
    if request.response_time_ms:
        if request.response_time_ms > 5000:
            latency_score = 0
        elif request.response_time_ms > 2000:
            latency_score = 40
        elif request.response_time_ms > 1000:
            latency_score = 70
        elif request.response_time_ms > 500:
            latency_score = 85
    
    # 2. Error Score
    error_score = max(0, 100 - (new_error_count * 8))
    
    # 3. Data Volume Score
    data_volume_score = 100
    if request.rows_processed:
        if request.rows_processed > 100000:
            data_volume_score = 30
        elif request.rows_processed > 50000:
            data_volume_score = 60
        elif request.rows_processed > 10000:
            data_volume_score = 85
    
    # 4. Freshness Score (keep existing or 100)
    freshness_score = flag.get('freshness_score', 100)
    
    # Overall health = weighted average
    new_health = int(
        (latency_score * 0.3) + 
        (error_score * 0.3) + 
        (data_volume_score * 0.2) + 
        (freshness_score * 0.2)
    )
    
    # ============================================
    # SEVERITY DETECTION
    # ============================================
    error_msg = request.error_message.lower()
    severity = 'low'
    
    if any(word in error_msg for word in ['sql', 'timeout', 'database', 'connection']):
        severity = 'high'
    if any(word in error_msg for word in ['crash', 'fatal', 'critical', 'failed']):
        severity = 'critical'
    if new_error_count > 10:
        severity = 'critical'
    if new_health < 50:
        severity = 'high'
    
    # ============================================
    # USER IMPACT
    # ============================================
    user_impact = 'low'
    if flag.get('phase') == 'mvp':
        user_impact = 'high'
    if new_health < 70:
        user_impact = 'high'
    if new_health < 50:
        user_impact = 'critical'
    
    # ============================================
    # ERROR TIMELINE
    # ============================================
    error_timeline = flag.get('error_timeline', [])
    if not isinstance(error_timeline, list):
        error_timeline = []
    
    error_timeline.append({
        "timestamp": datetime.utcnow().isoformat(),
        "message": request.error_message[:100],
        "severity": severity,
        "function": request.error_function or "unknown",
        "response_time_ms": request.response_time_ms
    })
    
    # Keep last 50 errors
    error_timeline = error_timeline[-50:]
    
    # ============================================
    # UPDATE DATA
    # ============================================
    update_data = {
        "error_count": new_error_count,
        "health_score": new_health,
        "last_error_at": datetime.utcnow().isoformat(),
        "last_error_message": request.error_message[:500],
        "last_error_trace": request.error_trace[:2000] if request.error_trace else None,
        "last_error_function": request.error_function,
        "error_severity": severity,
        "user_impact_level": user_impact,
        "error_rate_percent": min(100, (new_error_count / 100) * 100),
        "latency_score": latency_score,
        "error_score": error_score,
        "data_volume_score": data_volume_score,
        "freshness_score": freshness_score,
        "error_timeline": error_timeline,
        "avg_response_time_ms": request.response_time_ms,
        "rows_processed": request.rows_processed
    }
    
    # ============================================
    # AUTO-DISABLE IF CRITICAL
    # ============================================
    auto_disabled = False
    if new_health < 30 or severity == 'critical':
        update_data["is_enabled"] = False
        update_data["disabled_reason"] = f"Auto-disabled: {severity.upper()} - {request.error_message[:100]}"
        update_data["disabled_at"] = datetime.utcnow().isoformat()
        update_data["disabled_by"] = "system"
        auto_disabled = True
        print(f"🚨 CRITICAL AUTO-DISABLE: {flag_key} (health: {new_health}, severity: {severity})")
    
    supabase.table("feature_flags").update(update_data).eq("flag_key", flag_key).execute()
    
    return {
        "success": True,
        "health_score": new_health,
        "health_breakdown": {
            "latency_score": latency_score,
            "error_score": error_score,
            "data_volume_score": data_volume_score,
            "freshness_score": freshness_score
        },
        "severity": severity,
        "user_impact": user_impact,
        "auto_disabled": auto_disabled
    }