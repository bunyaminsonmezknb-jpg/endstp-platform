# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/deps.py
# Created: 2026-02-11
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded text
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - (None yet)
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - (None yet)
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
#   - Migration: docs/PHASE2_MIGRATION_PLAN.md
# =============================================================================

"""
deps.py - API dependency helpers (FastAPI deps)

Phase-1: Common dependency utilities (auth/guards/db/session helpers) are located here.

Usage:
    from app.api.v1.deps import <dependency>
"""

from datetime import datetime, timezone  # ⚠️ ALWAYS use timezone.utc!

from fastapi import Depends, Request
from sqlalchemy import text

# ⚠️ Bunlar sende projede zaten var olmalı.
# Eğer isimler farklıysa, bu iki import'u kendi projene göre değiştir.
from app.db.session import get_db  # AsyncSession dependency (varsayılan)
from app.core.auth import get_current_admin_user  # Admin guard (varsayılan)


def utc_now() -> datetime:
    """Return timezone-aware UTC now (global-first standard)."""
    return datetime.now(timezone.utc)


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


async def whisper_audit_context(
    db,
    *,
    request: Request,
    actor_id: str | None,
    actor_email: str | None,
    request_id: str | None,
) -> None:
    """
    "DB'ye fısıldama": Trigger'ların current_setting('app.*') ile okuyacağı request context'i set eder.
    set_config(..., true) transaction-local'dir (pool'a sızmaz).
    """

    ip = ""
    try:
        xff = request.headers.get("x-forwarded-for")
        if xff:
            ip = xff.split(",")[0].strip()
        elif request.client:
            ip = request.client.host or ""
    except Exception:
        ip = ""

    ua = request.headers.get("user-agent", "") or ""

    await db.execute(
        AUDIT_CTX_SQL,
        {
            "actor_id": actor_id or "",
            "actor_email": actor_email or "",
            "request_id": request_id or "",
            "ip": ip,
            "user_agent": ua,
        },
    )


async def get_admin_db(
    request: Request,
    db=Depends(get_db),
    current_admin=Depends(get_current_admin_user),
):
    """
    Admin endpoint'leri için DB dependency:
    - Admin guard zaten geçti (current_admin).
    - Transaction başında audit context set edilir.
    """
    request_id = request.headers.get("x-request-id")
    if not request_id and hasattr(request.state, "request_id"):
        request_id = getattr(request.state, "request_id", None)

    await whisper_audit_context(
        db,
        request=request,
        actor_id=str(getattr(current_admin, "id", "") or ""),
        actor_email=str(getattr(current_admin, "email", "") or ""),
        request_id=request_id,
    )

    yield db
