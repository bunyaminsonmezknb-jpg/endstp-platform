from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.db.session import get_supabase_admin

router = APIRouter(tags=["Student Notifications"])


@router.get("/reflex-notifications")
async def get_reflex_notifications(
    current_user: dict = Depends(get_current_user)
):
    supabase = get_supabase_admin()

    res = (
        supabase
        .table("ui_reflex_events")
        .select("*")
        .eq("student_id", current_user["id"])
        .eq("delivered", False)
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "notifications": res.data or []
    }


@router.post("/reflex-notifications/{event_id}/dismiss")
async def dismiss_reflex_notification(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    supabase = get_supabase_admin()

    supabase.table("ui_reflex_events") \
        .update({
            "delivered": True,
            "delivered_at": "now()"
        }) \
        .eq("id", event_id) \
        .eq("student_id", current_user["id"]) \
        .execute()

    return {"ok": True}
