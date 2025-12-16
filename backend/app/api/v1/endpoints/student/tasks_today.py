from fastapi import APIRouter, Depends, Header
from datetime import datetime, timezone
from app.db.session import get_supabase_admin
from app.core.auth import get_current_user
from .utils import (
    get_user_date,
    calculate_remembering_rate,
    calculate_next_review_date,
)

router = APIRouter()

# ==================================================
# MAIN ENDPOINT — SINGLE SOURCE OF TRUTH
# ==================================================

@router.get("/tasks/today")
async def get_tasks_today(
    current_user: dict = Depends(get_current_user),
    x_user_timezone: str = Header("UTC")
):
    supabase = get_supabase_admin()
    student_id = current_user["id"]

    today = get_user_date(x_user_timezone)
    today_str = today.isoformat()

    # ----------------------------------
    # 1️⃣ BUGÜNÜN GÖREVLERİNİ ÇEK
    # ----------------------------------
    tasks_res = (
        supabase.table("student_tasks")
        .select("*")
        .eq("student_id", student_id)
        .eq("task_date", today_str)
        .order("priority_level")
        .execute()
    )

    tasks = tasks_res.data or []

    # ----------------------------------
    # 2️⃣ BUGÜN HİÇ GÖREV YOKSA → YENİDEN ÜRET
    # ----------------------------------
    if not tasks:
        create_daily_tasks(student_id, today_str)

        tasks = (
            supabase.table("student_tasks")
            .select("*")
            .eq("student_id", student_id)
            .eq("task_date", today_str)
            .order("priority_level")
            .execute()
        ).data or []

    # ----------------------------------
    # 3️⃣ MOTOR VERİLERİ (TEK HESAPLAMA)
    # ----------------------------------
    topic_tests = (
        supabase.table("student_topic_tests")
        .select("*, topics(id, name_tr, subjects(name_tr))")
        .eq("student_id", student_id)
        .order("test_date", desc=True)
        .execute()
    ).data or []

    topic_performance = {}
    for t in topic_tests:
        topic_id = t.get("topic_id") or t.get("topics", {}).get("id")
        if not topic_id:
            continue

        topic_performance.setdefault(topic_id, {
            "topic_name": t["topics"]["name_tr"],
            "subject": t["topics"]["subjects"]["name_tr"],
            "tests": []
        })["tests"].append(t)

    # ----------------------------------
    # 4️⃣ AT RISK TOPICS
    # ----------------------------------
    at_risk = []
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        latest = tests[0]
        test_date = datetime.fromisoformat(latest["test_date"].replace("Z", "+00:00"))

        rate = calculate_remembering_rate(tests)
        next_review = calculate_next_review_date(rate, test_date)

        if next_review["urgency"] in ["HEMEN", "ACİL", "YAKIN", "critical", "high"]:
            at_risk.append({
                "topic_id": topic_id,
                "topic_name": data["topic_name"],
                "subject": data["subject"],
                "retention_rate": rate,
                "days_until_forgotten": next_review["days_remaining"],
            })

    # ----------------------------------
    # 5️⃣ SUMMARY
    # ----------------------------------
    total_time = sum(t["estimated_time_minutes"] for t in tasks)
    completed_time = sum(
        t["estimated_time_minutes"] for t in tasks if t["status"] == "completed"
    )

    return {
        "success": True,
        "date": today_str,
        "tasks": tasks,
        "summary": {
            "total_tasks": len(tasks),
            "completed_tasks": len([t for t in tasks if t["status"] == "completed"]),
            "total_time_minutes": total_time,
            "completed_time_minutes": completed_time,
            "remaining_time_minutes": total_time - completed_time,
        },
        "at_risk_topics": at_risk[:3],
        "total_at_risk": len(at_risk),
    }
def create_daily_tasks(student_id: str, date: str):
    """
    Bugün için görev yoksa otomatik oluştur
    Gerçek motorlar bağlanana kadar demo veriler
    """
    supabase = get_supabase_admin()
    
    # Matematik subject ID
    MATH_SUBJECT = "e576c099-c3ae-4022-be5c-919929437966"
    
    tasks = [
        {
            "student_id": student_id,
            "task_date": date,
            "task_type": "test",
            "subject_id": MATH_SUBJECT,
            "topic_id": "f82f6d64-1689-41ef-aa36-3f505637854d",
            "topic_name": "Limit",
            "source_motor": "priority",
            "priority_level": 1,
            "estimated_time_minutes": 20,
            "question_count": 12,
            "status": "pending"
        },
        {
            "student_id": student_id,
            "task_date": date,
            "task_type": "test",
            "subject_id": MATH_SUBJECT,
            "topic_id": "4c972d83-9848-43db-87d6-5ddb3b584591",
            "topic_name": "İntegral",
            "source_motor": "repetition",
            "priority_level": 2,
            "estimated_time_minutes": 20,
            "question_count": 12,
            "status": "pending"
        },
        {
            "student_id": student_id,
            "task_date": date,
            "task_type": "study",
            "subject_id": MATH_SUBJECT,
            "topic_id": "c3d5aee0-2ec7-48a9-867e-cd52e75e07ff",
            "topic_name": "Türev",
            "source_motor": "weakness",
            "priority_level": 3,
            "estimated_time_minutes": 30,
            "status": "pending"
        },
        {
            "student_id": student_id,
            "task_date": date,
            "task_type": "study",
            "subject_id": MATH_SUBJECT,
            "topic_id": "9c8a8646-86b7-4f1c-9108-cee4d4c7e923",
            "topic_name": "Fonksiyonlar",
            "source_motor": "speed",
            "priority_level": 4,
            "estimated_time_minutes": 25,
            "status": "pending"
        },
        {
            "student_id": student_id,
            "task_date": date,
            "task_type": "test",
            "subject_id": MATH_SUBJECT,
            "topic_id": "f82f6d64-1689-41ef-aa36-3f505637854d",
            "topic_name": "Limit (Tekrar)",
            "source_motor": "priority",
            "priority_level": 5,
            "estimated_time_minutes": 15,
            "question_count": 12,
            "status": "pending"
        }
    ]
    
    for task in tasks:
        supabase.table("student_tasks").insert(task).execute()
    
    print(f"✅ Created {len(tasks)} tasks for {date}")