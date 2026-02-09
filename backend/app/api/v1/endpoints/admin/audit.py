# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: audit.py
# Role: Admin audit log viewer endpoints
# Created: 2026-02-09
# Author: End.STP Team
#
# Golden rules:
# - UTC timestamps (timestamptz)
# - Admin-only access (get_current_admin guard)
# - Query filtering (category, admin_id, limit)
# =============================================================================

from fastapi import APIRouter, Depends, Query
from app.api.v1.deps_admin import get_current_admin
from app.db.session import get_supabase_admin
from typing import List, Dict, Any, Optional

router = APIRouter()


@router.get("/audit-log", response_model=List[Dict[str, Any]])
async def get_audit_log(
    current_admin: dict = Depends(get_current_admin),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    admin_id: Optional[str] = None
):
    """
    Get admin audit log entries
    
    Auth: Admin only
    Returns: List of audit entries
    """
    supabase = get_supabase_admin()
    
    query = supabase.table("admin_audit_log").select(
        "id, admin_id, action_type, action_category, "
        "before_state, after_state, created_at"
    )
    
    if category:
        query = query.eq("action_category", category)
    
    if admin_id:
        query = query.eq("admin_id", admin_id)
    
    result = query.order("created_at", desc=True).limit(limit).execute()
    
    return result.data
