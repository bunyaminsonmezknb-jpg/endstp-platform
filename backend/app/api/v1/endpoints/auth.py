"""
Authentication Endpoints
Supabase Auth kullanarak
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.db.session import get_supabase

router = APIRouter()


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/auth/signin", response_model=TokenResponse)
async def signin(credentials: SignInRequest):
    """
    Login endpoint - Supabase Auth
    """
    try:
        supabase = get_supabase()
        
        # Supabase Auth ile giriş
        auth_response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email veya şifre hatalı"
            )
        
        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "role": auth_response.user.user_metadata.get("role", "student")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Auth Hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Giriş yapılamadı"
        )


@router.get("/auth/me")
async def get_current_user():
    """Mevcut kullanıcı bilgisi"""
    return {"message": "User info endpoint - ileride eklenecek"}
