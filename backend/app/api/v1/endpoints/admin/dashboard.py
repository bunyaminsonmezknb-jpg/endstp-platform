# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/endpoints/admin/dashboard.py
# Role: Admin dashboard settings management endpoints
# Created: 2026-02-09
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# Golden rules:
# - UTC timestamps (timestamptz)
# - Admin-only access (get_current_admin guard)
# - ❌ No endpoint-level audit writes (DB trigger writes)
# - Singleton table (dashboard_settings)
# =============================================================================

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.api.v1.deps_admin import get_current_admin
from app.db.session import get_supabase_admin

router = APIRouter()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DashboardSettingsUpdate(BaseModel):
    # Flexible payload (frontend delta gönderiyor)
    # Pydantic extra allow => bilinmeyen alanları da kabul eder
    class Config:
        extra = "allow"


@router.get("/dashboard/settings")
async def get_dashboard_settings(
    _current_admin: dict = Depends(get_current_admin),
):
    """
    Get dashboard card visibility settings (singleton row).
    Auth: Admin only
    """
    supabase = get_supabase_admin()

    # Singleton stratejin: ya `singleton=true` ya da `id='singleton'`.
    # Mevcutta update singleton=true olduğu için burada da ona göre okuyalım.
    res = (
        supabase.table("dashboard_settings")
        .select("*")
        .eq("singleton", True)
        .limit(1)
        .execute()
    )

    data = res.data or []
    if not data:
        raise HTTPException(status_code=404, detail="Dashboard settings not found")

    return data[0]


@router.put("/dashboard/settings")
async def update_dashboard_settings(
    payload: DashboardSettingsUpdate,
    request: Request,
    current_admin: dict = Depends(get_current_admin),
):
    """
    Update dashboard settings (singleton).
    Auth: Admin only
    ❌ Audit log insert burada yok (DB trigger yazar).
    """
    supabase = get_supabase_admin()

    update_data: Dict[str, Any] = dict(payload)

    # Standard fields
    update_data["updated_by"] = current_admin.get("id")
    update_data["updated_at"] = utc_now_iso()

    res = (
        supabase.table("dashboard_settings")
        .update(update_data)
        .eq("singleton", True)
        .execute()
    )

    err = getattr(res, "error", None)
    if err:
        raise HTTPException(status_code=500, detail=f"Dashboard settings update failed: {err}")

    data = res.data or []
    if not data:
        # update başarılı ama data dönmediyse
        return {"success": True}

    return data[0]
