"""
Authentication Endpoints (Supabase v2)
- signup/signin: Supabase üzerinden session üretir
- me: Backend tarafında Authorization Bearer token ile doğrulama (HS256)
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, EmailStr

from app.db.session import get_supabase
from app.core.auth_hs256 import get_current_user  # ✅ HS256 doğrulama

router = APIRouter()


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "student"


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: Optional[str]
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str = "authenticated"


@router.post("/signup", response_model=TokenResponse)
async def signup(credentials: SignUpRequest):
    supabase = get_supabase()
    try:
        auth_response = supabase.auth.sign_up(
            {
                "email": credentials.email,
                "password": credentials.password,
                "options": {"data": {"full_name": credentials.full_name, "role": credentials.role}},
            }
        )
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Kayıt oluşturulamadı")

        session = auth_response.session
        return {
            "access_token": session.access_token if session else None,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": credentials.email,
                "full_name": credentials.full_name,
                "role": credentials.role,
            },
        }
    except Exception as e:
        print("❌ signup error:", str(e))
        raise HTTPException(status_code=400, detail="Kayıt yapılamadı")


@router.post("/signin", response_model=TokenResponse)
async def signin(credentials: SignInRequest):
    supabase = get_supabase()
    try:
        auth_response = supabase.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
        if not auth_response.user:
            raise HTTPException(status_code=401, detail="Email veya şifre hatalı")

        session = auth_response.session
        return {
            "access_token": session.access_token if session else None,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "full_name": (auth_response.user.user_metadata or {}).get("full_name", ""),
                "role": (auth_response.user.user_metadata or {}).get("role", "student"),
            },
        }
    except Exception as e:
        print("❌ signin error:", str(e))
        raise HTTPException(status_code=401, detail="Giriş yapılamadı")


@router.post("/signout")
async def signout(authorization: Optional[str] = Header(None)):
    # Backend signout idempotent: frontend signOut esas.
    return {"success": True, "message": "Signed out"}


@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user.get("id") or current_user.get("sub"),
        "email": current_user.get("email"),
        "full_name": current_user.get("full_name"),
        "role": current_user.get("role", "authenticated"),
    }
