"""
Authentication Endpoints (Supabase v2)
"""
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.session import get_supabase
from app.core.auth import get_current_user

router = APIRouter()

# -----------------------------
# MODELS
# -----------------------------
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "student"


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str


# -----------------------------
# SIGNUP
# -----------------------------
@router.post("/signup", response_model=TokenResponse)
async def signup(credentials: SignUpRequest):
    """Kayıt ol"""
    supabase = get_supabase()

    try:
        auth_response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password,
            "options": {
                "data": {
                    "full_name": credentials.full_name,
                    "role": credentials.role
                }
            }
        })

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
                "role": credentials.role
            }
        }

    except Exception as e:
        print("❌ signup error:", str(e))
        raise HTTPException(status_code=400, detail="Kayıt yapılamadı")


# -----------------------------
# SIGNIN
# -----------------------------
@router.post("/signin", response_model=TokenResponse)
async def signin(credentials: SignInRequest):
    """Giriş yap"""
    supabase = get_supabase()

    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })

        if not auth_response.user:
            raise HTTPException(status_code=401, detail="Email veya şifre hatalı")

        session = auth_response.session

        return {
            "access_token": session.access_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "full_name": auth_response.user.user_metadata.get("full_name", ""),
                "role": auth_response.user.user_metadata.get("role", "student")
            }
        }

    except Exception as e:
        print("❌ signin error:", str(e))
        raise HTTPException(status_code=401, detail="Giriş yapılamadı")


# -----------------------------
# SIGNOUT
# -----------------------------
@router.post("/signout")
async def signout(authorization: Optional[str] = Header(None)):
    """Çıkış yap"""
    if authorization:
        supabase = get_supabase()
        supabase.auth.sign_out()
    return {"success": True, "message": "Signed out"}


# -----------------------------
# CURRENT USER
# -----------------------------
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Mevcut kullanıcı"""
    return current_user
