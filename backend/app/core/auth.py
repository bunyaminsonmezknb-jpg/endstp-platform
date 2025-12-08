"""
Supabase JWT Authentication
"""
import jwt
import os
from fastapi import Header, HTTPException

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_JWT_SECRET:
    raise Exception("❌ SUPABASE_JWT_SECRET .env'de tanımlı değil!")

async def get_current_user(authorization: str = Header(None)):
    """
    Supabase JWT token'ını decode eder
    Authorization: Bearer <token>
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header gerekli")
    
    try:
        # "Bearer " kısmını temizle
        token = authorization.replace("Bearer ", "")
        
        # JWT decode (Supabase Secret ile)
        payload = jwt.decode(
            token, 
            SUPABASE_JWT_SECRET, 
            algorithms=["HS256"],
            audience="authenticated"
        )
        
        # User bilgisi döndür
        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role", "authenticated")
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token süresi dolmuş")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Geçersiz token: {str(e)}")
