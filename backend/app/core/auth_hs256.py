# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: auth_hs256.py
# Created: 2025-01-02
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
#   - EXPECTED_AUDIENCE = "authenticated"
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - JWKS-based validation (RS256) when enabled
#
# 📚 RELATED DOCS:
#   - docs/AUTH_SECURITY.md
# =============================================================================

"""
Supabase JWT Authentication (HS256)
----------------------------------
Fallback authentication when JWKS is unavailable.

Responsibilities:
- Validate JWT via HS256 + SUPABASE_JWT_SECRET
- Enforce issuer & audience
- Return normalized user payload

IMPORTANT:
- This file is SECURITY-CRITICAL
- Do NOT modify logic without explicit review
"""

from typing import Optional
import os

from fastapi import Header, HTTPException
from jose import jwt, JWTError


# =============================================================================
# CONFIG
# =============================================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL not set")

if not SUPABASE_JWT_SECRET:
    raise RuntimeError("SUPABASE_JWT_SECRET not set")

EXPECTED_ISSUER = f"{SUPABASE_URL}/auth/v1"
EXPECTED_AUDIENCE = "authenticated"


# =============================================================================
# AUTH CORE
# =============================================================================

def get_current_user(
    authorization: Optional[str] = Header(None),
):
    """
    Validate Supabase JWT (HS256)

    Returns:
        {
            id: str,
            sub: str,
            email: Optional[str],
            role: str
        }
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header required",
        )

    token = authorization.split(" ", 1)[1].strip()

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
        )

        return {
            "id": payload["sub"],
            "sub": payload["sub"],
            "email": payload.get("email"),
            "role": payload.get("role", "authenticated"),
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


def get_current_active_user(
    authorization: Optional[str] = Header(None),
):
    """
    Alias for get_current_user
    (reserved for future active/disabled checks)
    """
    return get_current_user(authorization)
