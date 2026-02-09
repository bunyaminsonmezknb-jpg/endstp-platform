# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: dashboard.py
# Role: Admin dashboard settings management endpoints
# Created: 2026-02-09
# Author: End.STP Team
#
# Golden rules:
# - UTC timestamps (timestamptz)
# - Admin-only access (get_current_admin guard)
# - Audit logging on all mutations
# - Singleton table (dashboard_settings)
# =============================================================================

from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.deps_admin import get_current_admin
from app.db.session import get_supabase_admin
from typing import Dict, Any

router = APIRouter()


@router.get("/dashboard/settings")
async def get_dashboard_settings(
    current_admin: dict = Depends(get_current_admin)
):
    """
    Get dashboard card visibility settings
    
    Auth: Admin only
    Returns: Dashboard settings
    """
    supabase = get_supabase_admin()
    result = supabase.table("dashboard_settings").select("*").execute()
    
    if not result.data or len(result.data) == 0:
        raise HTTPException(404, "Dashboard settings not found")
    
    return result.data[0]


@router.put("/dashboard/settings")
async def update_dashboard_settings(
    settings: Dict[str, Any],
    current_admin: dict = Depends(get_current_admin)
):
    """
    Update dashboard settings
    
    Auth: Admin only
    Creates audit log entry
    """
    supabase = get_supabase_admin()
    
    # Get current state
    before = supabase.table("dashboard_settings").select("*").execute()
    before_data = before.data[0] if before.data else None
    
    # Update (singleton table with singleton=true)
    after = supabase.table("dashboard_settings").update({
        **settings,
        "updated_by": current_admin["id"]
    }).eq("singleton", True).execute()
    
    # Audit log
    supabase.table("admin_audit_log").insert({
        "admin_id": current_admin["id"],
        "action_type": "update_dashboard_settings",
        "action_category": "dashboard_settings",
        "before_state": before_data,
        "after_state": after.data[0] if after.data else None
    }).execute()
    
    return after.data[0] if after.data else None
