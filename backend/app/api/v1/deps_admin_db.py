# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/deps_admin_db.py
# Created: 2026-02-12
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [x] No hardcoded text
# =============================================================================

from __future__ import annotations

from fastapi import Depends, Request
from sqlalchemy import text

from app.db.session import get_db
from app.api.v1.deps_admin import get_current_admin

AUDIT_CTX_SQL = text(
    """
select
  set_config('app.actor_id',    :actor_id,    true),
  set_config('app.actor_email', :actor_email, true),
  set_config('app.request_id',  :request_id,  true),
  set_config('app.ip',          :ip,          true),
  set_config('app.user_agent',  :user_agent,  true)
"""
)

def _get_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return ""

async def get_admin_db(
    request: Request,
    db=Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    """
    Admin write path için DB dependency:
    - Admin guard geçer
    - Transaction-local audit context set edilir (pool'a sızmaz)
    """
    request_id = request.headers.get("x-request-id", "") or ""
    ip = _get_ip(request)
    ua = request.headers.get("user-agent", "") or ""

    await db.execute(
        AUDIT_CTX_SQL,
        {
            "actor_id": str(current_admin.get("id", "") or ""),
            "actor_email": str(current_admin.get("email", "") or ""),
            "request_id": request_id,
            "ip": ip,
            "user_agent": ua,
        },
    )

    return db
