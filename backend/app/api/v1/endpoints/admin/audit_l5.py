# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: audit_l5
# Created: 2026-02-12
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [x] No hardcoded text
#
# 📚 RELATED DOCS:
#   - ENDSTP_RELEASE_GUARD.md
# =============================================================================

"""
audit_l5.py - L5 Admin Audit Log (READ-ONLY, Supabase)

Reads from canonical audit schema:
- audit.admin_audit_logs

No endpoint-level writes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, Request, HTTPException

from app.db.session import get_supabase_admin
from app.core.auth import get_current_admin_user  # senin projede var (hook mesajlarında da vardı)

router = APIRouter(prefix="/admin/audit-log", tags=["admin-audit"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@router.get("")
async def list_audit_logs(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    table_name: Optional[str] = Query(None),
    action: Optional[str] = Query(None, description="INSERT | UPDATE | DELETE"),
    actor_id: Optional[str] = Query(None, description="UUID"),
    request_id: Optional[str] = Query(None),
    current_admin=Depends(get_current_admin_user),
) -> dict[str, Any]:
    """
    Read-only audit log list.
    Filtering is optional. Ordered by occurred_at DESC.
    """
    # admin guard passed
    _ = current_admin

    sb = get_supabase_admin()

    q = sb.schema("audit").table("admin_audit_logs").select(
        "occurred_at,actor_id,actor_email,request_id,ip,user_agent,action,table_schema,table_name,record_pk,diff",
        count="exact",
    )

    if table_name:
        q = q.eq("table_name", table_name)
    if action:
        q = q.eq("action", action)
    if actor_id:
        q = q.eq("actor_id", actor_id)
    if request_id:
        q = q.eq("request_id", request_id)

    # order + pagination
    q = q.order("occurred_at", desc=True).range(offset, offset + limit - 1)

    res = q.execute()

    if getattr(res, "error", None):
        raise HTTPException(status_code=500, detail=str(res.error))

    data = res.data or []
    total = 0
    try:
        total = int(res.count or 0)
    except Exception:
        total = 0

    return {
        "meta": {
            "limit": limit,
            "offset": offset,
            "total": total,
            "generated_at": utc_now().isoformat(),
        },
        "items": data,
    }
