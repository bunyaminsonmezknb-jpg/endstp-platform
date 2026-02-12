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

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field

# NOTE:
# Bu dosyada DB erişimini projenizdeki mevcut pattern'e göre bağlamalısın.
# Aşağıdaki örnek: Supabase service role client ile insert + select yapar.
from app.core.supabase import get_supabase_service_client  # sende farklıysa uyarlayacağız
from app.api.v1.deps import utc_now

router = APIRouter(prefix="/admin/audit-log", tags=["admin-audit-log"])


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


def _get_ip(request: Request) -> Optional[str]:
    # reverse proxy varsa x-forwarded-for gelebilir
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    client = request.client
    return client.host if client else None


async def write_admin_audit_log(
    *,
    request: Request,
    actor_id: Optional[str],
    actor_email: Optional[str],
    action_type: str,
    entity: str,
    entity_id: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    diff: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
) -> None:
    """
    Append-only audit log writer.
    Uses service role client (RLS bypass) => güvenli ve stabil.
    """
    supabase = get_supabase_service_client()

    ip = _get_ip(request)
    user_agent = request.headers.get("user-agent")

    row = {
        "created_at": utc_now().isoformat(),
        "actor_id": actor_id,
        "actor_email": actor_email,
        "action_type": action_type,
        "entity": entity,
        "entity_id": entity_id,
        "request_id": request_id,
        "ip": ip,
        "user_agent": user_agent,
        "payload": payload,
        "diff": diff,
    }

    # best-effort: audit yazılamasa bile ana akış bozulmasın (ama log'a düşürmek istersin)
    try:
        supabase.table("admin_audit_logs").insert(row).execute()
    except Exception:
        # burada projenizdeki logger ile kaydetmek iyi olur
        return


@router.get("", response_model=AuditLogListResponse)
async def list_audit_logs(
    request: Request,
    q: Optional[str] = Query(default=None, description="Search in action_type/entity/actor_email/entity_id"),
    entity: Optional[str] = Query(default=None),
    action_type: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    # cursor: created_at ISO string (basit cursor)
    cursor: Optional[str] = Query(default=None),
):
    supabase = get_supabase_service_client()

    query = supabase.table("admin_audit_logs").select("*").order("created_at", desc=True).limit(limit)

    if cursor:
        # created_at < cursor
        query = query.lt("created_at", cursor)

    if entity:
        query = query.eq("entity", entity)

    if action_type:
        query = query.eq("action_type", action_type)

    if q:
        # Basit OR arama (ilkel ama Phase-1 için yeterli)
        qq = q.strip()
        query = query.or_(
            f"action_type.ilike.%{qq}%,entity.ilike.%{qq}%,actor_email.ilike.%{qq}%,entity_id.ilike.%{qq}%"
        )

    res = query.execute()
    data = res.data or []

    items = data
    next_cursor = items[-1]["created_at"] if len(items) == limit else None

    return {"items": items, "next_cursor": next_cursor}
