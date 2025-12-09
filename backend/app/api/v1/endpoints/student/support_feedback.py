"""
Student Feedback Endpoints
- Support feedback submission
- My feedbacks
- Admin stats & list
"""
from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import get_current_user
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
from collections import Counter

from app.db.session import get_supabase_admin

router = APIRouter()

# ============================================
# PYDANTIC MODELS
# ============================================

class SupportFeedbackSubmit(BaseModel):
    """Kullanıcı support feedback gönderir"""
    page_url: str
    satisfaction_score: Optional[int] = None  # 1-5
    issue_categories: Optional[List[str]] = []
    message: Optional[str] = None
    browser_info: Optional[dict] = {}

class SupportFeedbackResponse(BaseModel):
    """Support feedback response"""
    id: str
    user_id: str
    page_url: str
    satisfaction_score: Optional[int]
    issue_categories: List[str]
    message: Optional[str]
    status: str
    created_at: str

# ============================================
# ENDPOINTS
# ============================================

@router.post("/support-feedback/submit")
async def submit_support_feedback(feedback: SupportFeedbackSubmit, current_user: dict = Depends(get_current_user)):
    """🎯 Kullanıcı support feedback gönderir"""
    try:
        supabase = get_supabase_admin()
        
        feedback_data = {
            "user_id": "53a971d3-7492-4670-a31d-ca8422d0781b",  # Hardcoded for now
            "page_url": feedback.page_url,
            "satisfaction_score": feedback.satisfaction_score,
            "issue_categories": feedback.issue_categories or [],
            "message": feedback.message,
            "browser_info": feedback.browser_info or {},
            "status": "new"
        }
        
        result = supabase.table("user_support_feedback").insert(feedback_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Feedback kaydedilemedi")
        
        return {
            "success": True,
            "message": "Geri bildiriminiz alındı! Teşekkür ederiz 🙏",
            "feedback_id": result.data[0]["id"]
        }
        
    except Exception as e:
        print(f"❌ Support feedback error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/support-feedback/my-feedbacks")
async def get_my_support_feedbacks(current_user: dict = Depends(get_current_user), limit: int = 20):
    """Kullanıcının kendi support feedback'lerini getirir"""
    try:
        supabase = get_supabase_admin()
        
        result = supabase.table("user_support_feedback").select("*").eq(
            "user_id", "53a971d3-7492-4670-a31d-ca8422d0781b"
        ).order("created_at", desc=True).limit(limit).execute()
        
        return {
            "success": True,
            "feedbacks": result.data or []
        }
        
    except Exception as e:
        print(f"❌ Get feedbacks error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/support-feedback/admin/stats")
async def get_support_feedback_stats(current_user: dict = Depends(get_current_user)):
    """📊 Admin: Feedback istatistikleri"""
    try:
        supabase = get_supabase_admin()
        
        result = supabase.table("user_support_feedback").select("*").execute()
        feedbacks = result.data or []
        
        total = len(feedbacks)
        new_count = len([f for f in feedbacks if f["status"] == "new"])
        resolved_count = len([f for f in feedbacks if f["status"] == "resolved"])
        
        scores = [f["satisfaction_score"] for f in feedbacks if f.get("satisfaction_score")]
        avg_satisfaction = round(sum(scores) / len(scores), 1) if scores else None
        
        all_issues = []
        for f in feedbacks:
            if f.get("issue_categories"):
                all_issues.extend(f["issue_categories"])
        
        issue_counts = Counter(all_issues)
        top_issues = [{"category": cat, "count": count} for cat, count in issue_counts.most_common(5)]
        
        return {
            "success": True,
            "stats": {
                "total_feedbacks": total,
                "new": new_count,
                "resolved": resolved_count,
                "average_satisfaction": avg_satisfaction,
                "top_issues": top_issues
            }
        }
        
    except Exception as e:
        print(f"❌ Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/support-feedback/admin/list")
async def get_all_support_feedbacks(
    current_user: dict = Depends(get_current_user),
    status: Optional[str] = None,
    limit: int = 50
):
    """📋 Admin: Tüm feedback'leri listele"""
    try:
        supabase = get_supabase_admin()
        
        query = supabase.table("user_support_feedback").select("*")
        
        if status:
            query = query.eq("status", status)
        
        result = query.order("created_at", desc=True).limit(limit).execute()
        
        return {
            "success": True,
            "feedbacks": result.data or []
        }
        
    except Exception as e:
        print(f"❌ List feedbacks error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
