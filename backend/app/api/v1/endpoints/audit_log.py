# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/endpoints/audit_log.py
# Created: 2026-02-11
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [x] No hardcoded text (API messages minimal)
# =============================================================================

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel

from app.api.v1.deps_admin import get_current_admin
from app.db.session import get_supabase_admin

router = APIRouter(prefix="/admin/audit-log", tags=["admin-audit-log"])

# ✅ Canonical read surface for PostgREST: public schema view
AUDIT_READ_SOURCE = "v_admin_audit_logs"


class AuditLogItem(BaseModel):
    id: str
    created_at: datetime
    actor_id: Optional[str] = None
    actor_email: Optional[str] = None
    action_type: str
    entity: str
    entity_id: Optional[str] = None
    request_id: Optional[str] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    diff: Optional[Dict[str, Any]] = None


class AuditLogListResponse(BaseModel):
    items: List[AuditLogItem]
    next_cursor: Optional[str] = None


async def write_admin_audit_log(**_: Any) -> None:
    """
    ❌ DEPRECATED (L5):
    Audit log write işlemi endpoint seviyesinde yapılmaz.
    DB trigger (audit.capture_row_changes) append-only olarak yazar.
    """
    raise RuntimeError("L5 audit: write_admin_audit_log is disabled (DB-trigger only).")


@router.get("", response_model=AuditLogListResponse)
async def list_audit_logs(
    request: Request,
    _current_admin: dict = Depends(get_current_admin),  # ✅ admin guard
    q: Optional[str] = Query(default=None, description="Search in action_type/entity/actor_email/entity_id"),
    entity: Optional[str] = Query(default=None),
    action_type: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    cursor: Optional[str] = Query(default=None),  # created_at ISO string
):
    supabase = get_supabase_admin()

    query = (
        supabase.from_(AUDIT_READ_SOURCE)
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
    )

    if cursor:
        query = query.lt("created_at", cursor)

    if entity:
        query = query.eq("entity", entity)

    if action_type:
        query = query.eq("action_type", action_type)

    if q and q.strip():
        qq = q.strip()
        query = query.or_(
            f"action_type.ilike.%{qq}%,entity.ilike.%{qq}%,actor_email.ilike.%{qq}%,entity_id.ilike.%{qq}%"
        )

    res = query.execute()

    # ✅ Hata varsa 500 yerine açıklayıcı mesaj
    err = getattr(res, "error", None)
    if err:
        raise HTTPException(status_code=500, detail=f"Audit read failed: {err}")

    data = res.data or []
    next_cursor = data[-1]["created_at"] if len(data) == limit else None
    return {"items": data, "next_cursor": next_cursor}
