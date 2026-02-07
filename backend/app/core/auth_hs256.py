# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: auth_hs256.py
# Role: Supabase HS256 JWT verification for FastAPI (backend)
#
# Golden rules:
# - No token value logging (ever)
# - Only safe debug when AUTH_DEBUG=1
# =============================================================================

from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional, Tuple

from fastapi import Header, HTTPException
from jose import JWTError, ExpiredSignatureError, jwt


def _is_debug() -> bool:
    return (os.getenv("AUTH_DEBUG") or "").strip() in ("1", "true", "TRUE", "yes", "YES")


def _safe_print(*args: Any) -> None:
    if _is_debug():
        print(*args)


def _get_config() -> Tuple[str, str, str]:
    """
    Returns:
      (secret, expected_issuer, expected_audience)
    """
    supabase_url = (os.getenv("SUPABASE_URL") or "").rstrip("/")
    secret = (os.getenv("SUPABASE_JWT_SECRET") or "").strip()

    if not supabase_url:
        raise RuntimeError("SUPABASE_URL not set")
    if not secret:
        raise RuntimeError("SUPABASE_JWT_SECRET not set")

    expected_issuer = f"{supabase_url}/auth/v1"
    expected_audience = os.getenv("SUPABASE_JWT_AUD") or "authenticated"

    # SAFE DEBUG
    _safe_print(
        "AUTH DEBUG config:",
        {
            "supabase_url_present": bool(supabase_url),
            "secret_len": len(secret) if secret else None,
            "expected_issuer": expected_issuer,
            "expected_audience": expected_audience,
        },
    )

    return secret, expected_issuer, expected_audience


def _decode_claims_unverified(token: str) -> Dict[str, Any]:
    """
    Unverified claims only for SAFE debug (iss/aud/exp/sub).
    """
    try:
        claims = jwt.get_unverified_claims(token)
        # SAFE subset
        safe = {k: claims.get(k) for k in ("iss", "aud", "exp", "sub")}
        _safe_print("AUTH DEBUG token_claims:", safe)
        return claims
    except Exception:
        return {}


def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    FastAPI dependency:
      Authorization: Bearer <access_token>
    Returns normalized dict:
      { id/sub, email, full_name, role }
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")

    token = authorization.replace("Bearer ", "", 1).strip()
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header required")

    secret, expected_issuer, expected_audience = _get_config()

    # SAFE debug: show only subset of claims (unverified)
    _decode_claims_unverified(token)

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            issuer=expected_issuer,
            audience=expected_audience,
            options={
                "verify_signature": True,
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
            },
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Supabase access token standard fields
    user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_metadata = payload.get("user_metadata") or {}
    app_metadata = payload.get("app_metadata") or {}

    email = payload.get("email") or user_metadata.get("email")
    full_name = user_metadata.get("full_name")
    role = user_metadata.get("role") or app_metadata.get("role") or payload.get("role") or "authenticated"

    return {
        "id": user_id,
        "sub": user_id,
        "email": email,
        "full_name": full_name,
        "role": role,
        "iat": payload.get("iat"),
        "exp": payload.get("exp"),
    }


def get_current_active_user(current_user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder for future: blocked/disabled checks etc.
    """
    return current_user
