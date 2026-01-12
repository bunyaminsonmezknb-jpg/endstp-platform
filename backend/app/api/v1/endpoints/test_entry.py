"""
Test Entry Endpoints
Öğrenci test girişi için API'ler
"""

import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.session import get_supabase_admin
from app.core.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


# ============================================
# REQUEST MODEL
# ============================================

class TestResultSubmit(BaseModel):
    # ⚠️ frontend gönderse bile backend override eder
    student_id: Optional[str] = None

    subject_id: str
    topic_id: str

    # frontend: "YYYY-MM-DDTHH:MM"
    test_date: str

    correct_count: int
    wrong_count: int
    empty_count: int

    # ⚠️ backend hesaplar
    net_score: Optional[float] = None
    success_rate: Optional[float] = None

    test_duration_minutes: Optional[int] = None


# ============================================
# PUBLIC ENDPOINTS
# ============================================

@router.get("/subjects")
async def get_subjects():
    supabase = get_supabase_admin()
    try:
        result = (
            supabase.table("subjects")
            .select("id, code, name_tr, icon, color")
            .eq("is_active", True)
            .order("name_tr")
            .execute()
        )
        return result.data
    except Exception as e:
        logger.error(f"Subjects Error: {e}")
        raise HTTPException(500, "Subjects load failed")


@router.get("/subjects/{subject_id}/topics")
async def get_topics_by_subject(subject_id: str):
    supabase = get_supabase_admin()
    try:
        result = (
            supabase.table("topics")
            .select("id, code, name_tr, difficulty_level, exam_weight")
            .eq("subject_id", subject_id)
            .eq("is_active", True)
            .order("name_tr")
            .execute()
        )
        return result.data
    except Exception as e:
        logger.error(f"Topics Error: {e}")
        raise HTTPException(500, "Topics load failed")


# ============================================
# AUTO COMPLETE TASK
# ============================================

def auto_complete_task_if_exists(
    student_id: str,
    topic_id: str,
    test_result_id: str
):
    supabase = get_supabase_admin()
    try:
        today = datetime.now(timezone.utc).date().isoformat()

        tasks = (
            supabase.table("student_tasks")
            .select("*")
            .eq("student_id", student_id)
            .eq("task_date", today)
            .eq("topic_id", topic_id)
            .eq("status", "pending")
            .execute()
        )

        if tasks.data:
            task = tasks.data[0]
            supabase.table("student_tasks").update({
                "status": "completed",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "manual_completion": False,
                "test_result_id": test_result_id
            }).eq("id", task["id"]).execute()

            return {
                "auto_completed": True,
                "task_id": task["id"],
                "task_name": task.get("topic_name")
            }

        return {"auto_completed": False}

    except Exception as e:
        logger.error(f"Auto-complete task error: {e}")
        return {"auto_completed": False}


# ============================================
# POST /api/v1/test-results
# ============================================

@router.post("/test-results")
async def submit_test_result(
    test_data: TestResultSubmit,
    current_user: dict = Depends(get_current_user)
):
    """
    MÜHÜRLÜ TEST ENTRY
    - Auth zorunlu
    - student_id backend override
    - 12 soru kuralı backend
    - success_rate & net_score backend hesap
    - LOCAL → UTC normalize
    - Gelecek tarih engeli (UTC)
    """

    supabase = get_supabase_admin()

    try:
        # 🔒 AUTH OVERRIDE
        student_id = current_user["id"]
        # 🚦 RATE LIMIT (SPAM GUARD)
        recent = (
            supabase.table("student_topic_tests")
            .select("id")
            .eq("student_id", student_id)
            .gte(
                "created_at",
                (datetime.now(timezone.utc) - timedelta(seconds=5)).isoformat()
            )
            .execute()
        )

        if recent.data and len(recent.data) >= 3:
            raise HTTPException(
                status_code=429,
                detail="Çok hızlı test girişi. Lütfen birkaç saniye bekleyin."
            )

        # 📏 12 SORU KURALI
        total = (
            test_data.correct_count
            + test_data.wrong_count
            + test_data.empty_count
        )

        if total != 12:
            raise HTTPException(422, "Toplam soru sayısı 12 olmalıdır")

        # 🕒 TEST DATE NORMALIZE (LOCAL → UTC)
        try:
            local_dt = datetime.fromisoformat(test_data.test_date)
        except ValueError:
            raise HTTPException(422, "Geçersiz test tarihi formatı")

        # timezone yoksa → local kabul et
        if local_dt.tzinfo is None:
            local_dt = local_dt.astimezone()

        test_date_utc = local_dt.astimezone(timezone.utc)
        # 🛑 Aynı testin tekrar gönderilmesini engelle
        existing = (
            supabase.table("student_topic_tests")
            .select("id")
            .eq("student_id", student_id)
            .eq("topic_id", test_data.topic_id)
            .eq("test_date", test_date_utc.isoformat())
            .execute()
        )

        if existing.data:
            raise HTTPException(
                status_code=409,
                detail="Bu test zaten girilmiş"
            )

        # ⛔ GELECEK TARİH ENGELİ
        now_utc = datetime.now(timezone.utc)

        # 🟢 1 dakikalık tolerance
        if test_date_utc > now_utc + timedelta(minutes=1):
            raise HTTPException(
                status_code=422,
                detail="Gelecek tarihli test girilemez"
            )


        # 📊 BACKEND HESAPLAMALARI
        success_rate = round(
            (test_data.correct_count / total) * 100, 2
        )
        net_score = round(
            test_data.correct_count - (test_data.wrong_count / 4), 2
        )
        # 🛡️ test_duration_minutes guard
        duration = test_data.test_duration_minutes
        if duration is not None and duration <= 0:
            duration = None

        # 🧾 DB KAYDI
        test_record = {
            "student_id": student_id,
            "subject_id": test_data.subject_id,
            "topic_id": test_data.topic_id,

            # 🔑 UTC KAYIT
            "test_date": test_date_utc.isoformat(),

            "correct_count": test_data.correct_count,
            "wrong_count": test_data.wrong_count,
            "empty_count": test_data.empty_count,

            "net_score": net_score,
            "success_rate": success_rate,
            "test_duration_minutes": duration,
 
            "is_processed": False,
            "processing_status": "pending",
            "test_source": "web_form",
            "question_type": "multiple_choice",
            "created_via": "web_form",
            "api_version": "v1",
            "request_id": str(uuid.uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        result = (
            supabase.table("student_topic_tests")
            .insert(test_record)
            .execute()
        )

        if not result.data:
            return {
                "success": True,
                "message": "Test kaydedildi",
                "net_score": net_score,
                "task_auto_completed": False
            }

        test_id = result.data[0]["id"]

        task_result = auto_complete_task_if_exists(
            student_id=student_id,
            topic_id=test_data.topic_id,
            test_result_id=test_id
        )

        response = {
            "success": True,
            "message": "Test başarıyla kaydedildi",
            "test_id": test_id,
            "net_score": net_score,
            "success_rate": success_rate,
            "task_auto_completed": task_result.get("auto_completed", False)
        }

        if task_result.get("auto_completed"):
            response["completed_task"] = {
                "task_id": task_result.get("task_id"),
                "task_name": task_result.get("task_name")
            }
            response["message"] += " ve görev otomatik tamamlandı 🎉"

        return response

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("❌ Test submit error")
        raise HTTPException(
            status_code=500,
            detail="Test kaydı sırasında sunucu hatası"
        )
