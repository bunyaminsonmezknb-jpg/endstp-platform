"""
Authentication Middleware
"""
from fastapi import Header, HTTPException, status
from app.db.session import get_supabase

async def get_current_user(authorization: str = Header(None)):
    """Token'dan kullanıcıyı al"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header gerekli"
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        supabase = get_supabase()
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz token"
            )
        
        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "full_name": user_response.user.user_metadata.get("full_name", ""),
            "role": user_response.user.user_metadata.get("role", "student")
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Auth error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication başarısız"
        )
