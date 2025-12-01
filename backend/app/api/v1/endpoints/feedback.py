"""
Feedback API Endpoints
Öğrencilerin dashboard component'lerine geri bildirim vermesi için
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from app.db.session import get_supabase_admin

router = APIRouter()


@router.post("/feedback/submit", response_model=dict)
async def submit_feedback(request: dict):
    """
    Öğrenci feedback'i gönderir
    
    Request body:
    {
        "student_id": "uuid",
        "component_type": "motor_analysis",
        "component_id": "optional",
        "feedback_type": "like",
        "rating": 5,
        "comment": "optional",
        "metadata": {}
    }
    """
    try:
        supabase = get_supabase_admin()
        
        # Request'ten verileri al
        student_id = request.get("student_id")
        component_type = request.get("component_type")
        component_id = request.get("component_id")
        feedback_type = request.get("feedback_type")
        rating = request.get("rating")
        comment = request.get("comment")
        metadata = request.get("metadata", {})
        
        # Validation
        if not student_id:
            raise HTTPException(status_code=400, detail="student_id gerekli")
        
        if not component_type:
            raise HTTPException(status_code=400, detail="component_type gerekli")
        
        valid_types = ['motor_analysis', 'action_card', 'critical_alert', 'goal_card', 'projection_card']
        if component_type not in valid_types:
            raise HTTPException(
                status_code=400, 
                detail=f"component_type must be one of {valid_types}"
            )
        
        if not feedback_type:
            raise HTTPException(status_code=400, detail="feedback_type gerekli")
        
        valid_feedback_types = ['like', 'dislike', 'rating']
        if feedback_type not in valid_feedback_types:
            raise HTTPException(
                status_code=400,
                detail=f"feedback_type must be one of {valid_feedback_types}"
            )
        
        # Rating validation
        if feedback_type == 'rating':
            if rating is None:
                raise HTTPException(status_code=400, detail="rating gerekli when feedback_type is 'rating'")
            if not (1 <= rating <= 5):
                raise HTTPException(status_code=400, detail="rating must be between 1 and 5")
        
        # Feedback verisini hazırla
        feedback_data = {
            "id": str(uuid.uuid4()),  # UUID oluştur
            "student_id": student_id,
            "component_type": component_type,
            "component_id": component_id,
            "feedback_type": feedback_type,
            "rating": rating,
            "comment": comment,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Database'e kaydet
        result = supabase.table("user_feedback").insert(feedback_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Feedback kaydedilemedi")
        
        return {
            "success": True,
            "message": "Geri bildiriminiz kaydedildi. Teşekkürler!",
            "feedback_id": feedback_data["id"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Feedback submit error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback hatası: {str(e)}")


@router.get("/feedback/my-feedbacks")
async def get_my_feedbacks(
    student_id: str,
    component_type: Optional[str] = None,
    limit: int = 50
):
    """
    Öğrencinin kendi feedback'lerini getirir
    """
    try:
        supabase = get_supabase_admin()
        
        query = supabase.table("user_feedback").select("*").eq(
            "student_id", student_id
        ).order("created_at", desc=True).limit(limit)
        
        if component_type:
            query = query.eq("component_type", component_type)
        
        result = query.execute()
        
        return result.data or []
        
    except Exception as e:
        print(f"Get feedbacks error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feedback/stats/{component_type}")
async def get_feedback_stats(
    component_type: str,
    component_id: Optional[str] = None
):
    """
    Belirli bir component için feedback istatistikleri
    """
    try:
        supabase = get_supabase_admin()
        
        query = supabase.table("user_feedback").select("*").eq(
            "component_type", component_type
        )
        
        if component_id:
            query = query.eq("component_id", component_id)
        
        result = query.execute()
        feedbacks = result.data or []
        
        # İstatistikleri hesapla
        total = len(feedbacks)
        likes = len([f for f in feedbacks if f['feedback_type'] == 'like'])
        dislikes = len([f for f in feedbacks if f['feedback_type'] == 'dislike'])
        
        # Ortalama rating
        ratings = [f['rating'] for f in feedbacks if f['rating'] is not None]
        avg_rating = sum(ratings) / len(ratings) if ratings else None
        
        return {
            "component_type": component_type,
            "total_feedbacks": total,
            "likes": likes,
            "dislikes": dislikes,
            "average_rating": round(avg_rating, 1) if avg_rating else None
        }
        
    except Exception as e:
        print(f"Get stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))