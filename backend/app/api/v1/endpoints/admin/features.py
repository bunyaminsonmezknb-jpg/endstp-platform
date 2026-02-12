# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/endpoints/admin/features.py
# Role: Admin feature flags management endpoints
# Created: 2026-02-09
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# Golden rules:
# - UTC timestamps (timestamptz)
# - Admin-only access (get_current_admin guard)
# - ❌ No endpoint-level audit writes (DB trigger writes)
# - Kill switches for motors and UI components
# =============================================================================

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.v1.deps_admin import get_current_admin
from app.db.session import get_supabase_admin

router = APIRouter()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ToggleFeatureFlagBody(BaseModel):
    enabled: bool


@router.get("/feature-flags", response_model=List[Dict[str, Any]])
async def get_admin_feature_flags(
    _current_admin: dict = Depends(get_current_admin),
):
    """
    Get all admin panel feature flags
    Auth: Admin only
    """
    supabase = get_supabase_admin()

    res = (
        supabase.table("admin_feature_flags")
        .select(
            "id, flag_key, flag_name_tr, flag_name_en, is_enabled, category, criticality, updated_at, updated_by"
        )
        .order("category")
        .order("criticality")
        .execute()
    )

    err = getattr(res, "error", None)
    if err:
        raise HTTPException(status_code=500, detail=f"Feature flags read failed: {err}")

    return res.data or []


@router.put("/feature-flags/{flag_key}")
async def toggle_feature_flag(
    flag_key: str,
    body: ToggleFeatureFlagBody,
    current_admin: dict = Depends(get_current_admin),
):
    """
    Toggle feature flag on/off
    Auth: Admin only
    Body: { "enabled": true/false }
    ❌ Audit log insert burada yok (DB trigger yazar).
    """
    supabase = get_supabase_admin()

    # Var mı kontrolü (frontend hata mesajı için)
    before = (
        supabase.table("admin_feature_flags")
        .select("id, flag_key, is_enabled")
        .eq("flag_key", flag_key)
        .limit(1)
        .execute()
    )
    if not (before.data or []):
        raise HTTPException(status_code=404, detail=f"Flag {flag_key} not found")

    res = (
        supabase.table("admin_feature_flags")
        .update(
            {
                "is_enabled": bool(body.enabled),
                "updated_by": current_admin.get("id"),
                "updated_at": utc_now_iso(),
            }
        )
        .eq("flag_key", flag_key)
        .execute()
    )

    err = getattr(res, "error", None)
    if err:
        raise HTTPException(status_code=500, detail=f"Feature flag update failed: {err}")

    data = res.data or []
    if not data:
        return {"success": True}

    return data[0]
