from fastapi import Header, HTTPException, status
from app.db.session import SUPABASE_URL, SUPABASE_ANON_KEY
import requests

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header gerekli"
        )

    token = authorization.replace("Bearer ", "").strip()

    url = f"{SUPABASE_URL}/auth/v1/user"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": SUPABASE_ANON_KEY,
    }

    try:
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz token"
            )

        user = res.json()

        return {
            "id": user.get("id"),
            "email": user.get("email"),
            "full_name": user.get("user_metadata", {}).get("full_name", ""),
            "role": user.get("user_metadata", {}).get("role", "student")
        }

    except Exception as e:
        print("AUTH ERROR:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication başarısız"
        )
