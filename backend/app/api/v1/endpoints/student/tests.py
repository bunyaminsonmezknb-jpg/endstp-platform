"""
Student Tests Endpoints
- Update test
- Delete test
"""
from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import get_current_user
from app.db.session import get_supabase_admin
from datetime import datetime, timezone

router = APIRouter()

@router.put("/tests/{test_id}")
async def update_test(test_id: str, test_data: dict, current_user: dict = Depends(get_current_user)):
    """
    Testi güncelle
    """
    supabase = get_supabase_admin()
    
    # Net score'u hesapla
    correct = test_data.get("correct_count", 0)
    wrong = test_data.get("wrong_count", 0)
    net_score = correct - (wrong * 0.25)
    
    # Success rate hesapla
    total = correct + wrong + test_data.get("empty_count", 0)
    success_rate = (correct / total * 100) if total > 0 else 0
    
    # Güncelleme datası
    update_data = {
        "test_date": test_data.get("test_date"),
        "correct_count": correct,
        "wrong_count": wrong,
        "empty_count": test_data.get("empty_count", 0),
        "net_score": net_score,
        "success_rate": success_rate,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Güncelle
    response = supabase.table("student_topic_tests").update(
        update_data
    ).eq("id", test_id).execute()
    
    if not response.data:
        return {"success": False, "error": "Test bulunamadı"}
    
    return {"success": True, "test": response.data[0]}

@router.delete("/tests/{test_id}")
async def delete_test(test_id: str, current_user: dict = Depends(get_current_user)):
    """
    Testi sil
    """
    supabase = get_supabase_admin()
    
    # Sil
    response = supabase.table("student_topic_tests").delete().eq(
        "id", test_id
    ).execute()
    
    if not response.data:
        return {"success": False, "error": "Test bulunamadı"}
    
    return {"success": True}
