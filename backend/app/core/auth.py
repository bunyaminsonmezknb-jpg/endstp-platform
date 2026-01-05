from fastapi import Header, HTTPException, status
from app.db.session import SUPABASE_URL, SUPABASE_ANON_KEY
import requests
import traceback

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header gerekli"
        )

    token = authorization.replace("Bearer ", "").strip()
    
    # DEBUG: Token'ı göster (ilk 20 karakter)
    print(f"AUTH TOKEN DEBUG: {token[:20]}...")

    url = f"{SUPABASE_URL}/auth/v1/user"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": SUPABASE_ANON_KEY,
    }
    
    # DEBUG: Headers'ı göster
    print(f"AUTH HEADERS: Authorization={headers['Authorization'][:30]}..., apikey={SUPABASE_ANON_KEY[:20]}...")

    try:
        res = requests.get(url, headers=headers, timeout=5)
        
        print(f"AUTH DEBUG: Status={res.status_code}")

        if res.status_code != 200:
            print(f"AUTH ERROR RESPONSE: {res.text}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Geçersiz token: {res.json().get('msg', 'Unknown error')}"
            )

        user = res.json()

        return {
            "id": user.get("id"),
            "email": user.get("email"),
            "full_name": user.get("user_metadata", {}).get("full_name", ""),
            "role": user.get("user_metadata", {}).get("role", "student"),
            "access_token": token
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"AUTH ERROR DETAILED: {type(e).__name__}: {str(e)}")
        print(f"TRACEBACK: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication başarısız"
        )
