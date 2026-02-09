# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: deps_admin.py
# Role: Admin authentication guard - Enforces role=admin via user_profiles
# Created: 2026-02-09
# Author: End.STP Team
#
# Golden rules:
# - Uses Supabase HS256 auth (single source of truth)
# - Enforces role=admin via user_profiles table
# - Returns 403 if user is not admin
# =============================================================================

from fastapi import Depends, HTTPException, status
from app.core.auth_hs256 import get_current_user
from app.db.session import get_supabase_admin


def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Ensure current user is admin.
    current_user expected shape from auth_hs256:
      { "id": <uuid>, ... }
    """
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session user",
        )

    supabase = get_supabase_admin()

    res = (
        supabase.table("user_profiles")
        .select("id, role")
        .eq("id", user_id)
        .single()
        .execute()
    )

    profile = res.data
    if not profile or profile.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    # Optionally attach role
    current_user["role"] = profile.get("role")
    return current_user
