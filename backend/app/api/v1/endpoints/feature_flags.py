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
async def get_admin_flags(current_user: dict = Depends(get_current_user)):
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
    request: ToggleFlagRequest,
    current_user: dict = Depends(get_current_user)
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
        update_data["disabled_by"] = current_user.get("email", "unknown")
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


@router.post("/{flag_key}/report-error")
async def report_flag_error(flag_key: str, request: ReportErrorRequest):
    """Report error for health monitoring (auto-disable if critical)"""
    supabase = get_supabase_admin()
    
    # Get current metrics
    flag_result = supabase.table("feature_flags").select("error_count, health_score, is_enabled").eq("flag_key", flag_key).execute()
    if not flag_result.data:
        return {"success": False, "message": "Flag not found"}
    
    flag = flag_result.data[0]
    new_error_count = flag["error_count"] + 1
    new_health = max(0, flag["health_score"] - 10)
    
    update_data = {
        "error_count": new_error_count,
        "health_score": new_health,
        "last_error_at": datetime.utcnow().isoformat()
    }
    
    # Auto-disable if health critical
    auto_disabled = False
    if new_health < 30 and flag["is_enabled"]:
        update_data["is_enabled"] = False
        update_data["disabled_reason"] = f"Auto-disabled: Health {new_health}, {new_error_count} errors"
        update_data["disabled_at"] = datetime.utcnow().isoformat()
        auto_disabled = True
        print(f"🚨 AUTO-DISABLED: {flag_key} (health: {new_health})")
    
    supabase.table("feature_flags").update(update_data).eq("flag_key", flag_key).execute()
    
    return {
        "success": True,
        "health_score": new_health,
        "error_count": new_error_count,
        "auto_disabled": auto_disabled
    }