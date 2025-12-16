from fastapi import APIRouter, Depends
from app.db.session import get_supabase_admin
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/reflex-events")
async def get_reflex_events(current_user: dict = Depends(get_current_user)):
    """Backend proxy - RLS bypass"""
    try:
        supabase = get_supabase_admin()
        result = supabase.table("ui_reflex_events") \
            .select("*") \
            .eq("student_id", current_user["id"]) \
            .order("created_at", desc=True) \
            .limit(50) \
            .execute()
        
        return {"success": True, "events": result.data or []}
    except Exception as e:
        return {"success": False, "events": []}