from fastapi import APIRouter, Depends, HTTPException, Query
from collections import defaultdict

from app.core.auth import get_current_user
from app.db.session import get_supabase_admin

# progress calculators'ı yeniden kullanacağız
from app.api.v1.endpoints.progress.calculators import calculate_trends

router = APIRouter(prefix="/student", tags=["student-analytics"])

@router.post("/trend")
async def student_trend_post_alias(
    period: str = Query("weekly", pattern="^(weekly|monthly)$"),
    num_periods: int = Query(8, ge=2, le=24),
    current_user: dict = Depends(get_current_user),
    supabase = Depends(get_supabase_admin),
):
    """
    BACKWARD COMPAT:
    Frontend şu an POST /student/trend çağırıyor.
    Biz bunu progress.calculate_trends ile cevaplıyoruz.
    """
    try:
        student_id = current_user.get("id")

        tests_result = supabase.table("student_topic_tests").select(
            "id, test_date, subject_id, topic_id, success_rate"
        ).eq("student_id", student_id).order("test_date").execute()

        tests = tests_result.data or []

        subjects_result = supabase.table("subjects").select("id, name_tr").execute()
        subjects_map = {s["id"]: s["name_tr"] for s in (subjects_result.data or [])}

        data = calculate_trends(
            tests=tests,
            period=period,
            num_periods=num_periods,
            subjects=subjects_map
        )

        return {
            "success": True,
            "data": {
                "labels": data["labels"],
                "datasets": [
                    {"label": s["label"], "data": s["data"], "subject_id": s["subject_id"]}
                    for s in data["subjects"]
                ],
                "overall_trend": data["overall_trend"],
                "period": data["period"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend alias failed: {e}")
