"""
Supabase JWT Authentication (HS256 - JWT_SECRET)
JWKS boş olduğunda kullan!
"""
from fastapi import Header, HTTPException
from jose import jwt, JWTError
import os
from typing import Optional

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL not set")

if not SUPABASE_JWT_SECRET:
    raise RuntimeError("SUPABASE_JWT_SECRET not set")

EXPECTED_ISSUER = f"{SUPABASE_URL}/auth/v1"
EXPECTED_AUDIENCE = "authenticated"


def get_current_user(authorization: Optional[str] = Header(None)):
    """HS256 + JWT_SECRET ile doğrulama"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, 
            detail="Authorization header gerekli"
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

        print(f"✅ Token validated (HS256) for {payload.get('email')}")

        return {
            "id": payload["sub"],
            "sub": payload["sub"],
            "email": payload.get("email"),
            "role": payload.get("role", "authenticated"),
        }

    except JWTError as e:
        print(f"❌ JWT validation failed: {e}")
        raise HTTPException(
            status_code=401, 
            detail="Geçersiz token"
        )


def get_current_active_user(authorization: Optional[str] = Header(None)):
    return get_current_user(authorization)
