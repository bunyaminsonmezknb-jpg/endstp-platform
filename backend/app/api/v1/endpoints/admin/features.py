# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: features.py
# Role: Admin feature flags management endpoints
# Created: 2026-02-09
# Author: End.STP Team
#
# Golden rules:
# - UTC timestamps (timestamptz)
# - Admin-only access (get_current_admin guard)
# - Audit logging on all mutations
# - Kill switches for motors and UI components
# =============================================================================

from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.deps_admin import get_current_admin
from app.db.session import get_supabase_admin
from typing import List, Dict, Any

router = APIRouter()


@router.get("/feature-flags", response_model=List[Dict[str, Any]])
async def get_admin_feature_flags(
    current_admin: dict = Depends(get_current_admin)
):
    """
    Get all admin panel feature flags
    
    Auth: Admin only
    Returns: List of feature flags
    """
    supabase = get_supabase_admin()
    result = supabase.table("admin_feature_flags").select(
        "id, flag_key, flag_name_tr, flag_name_en, "
        "is_enabled, category, criticality, updated_at"
    ).order("category", "criticality").execute()
    
    return result.data


@router.put("/feature-flags/{flag_key}")
async def toggle_feature_flag(
    flag_key: str,
    enabled: bool,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Toggle feature flag on/off
    
    Auth: Admin only
    Creates audit log entry
    """
    supabase = get_supabase_admin()
    
    # Get current state
    before = supabase.table("admin_feature_flags").select("*").eq(
        "flag_key", flag_key
    ).single().execute()
    
    if not before.data:
        raise HTTPException(404, f"Flag {flag_key} not found")
    
    # Update
    after = supabase.table("admin_feature_flags").update({
        "is_enabled": enabled,
        "updated_by": current_admin["id"]
    }).eq("flag_key", flag_key).execute()
    
    # Audit log
    supabase.table("admin_audit_log").insert({
        "admin_id": current_admin["id"],
        "action_type": "toggle_feature_flag",
        "action_category": "feature_flags",
        "before_state": before.data,
        "after_state": after.data[0] if after.data else None
    }).execute()
    
    return after.data[0] if after.data else None
