"""
Student Tasks Endpoints
- /todays-tasks          (dashboard summary)
- /tasks/today           (today task list + summary) ✅ AUTO-CREATE
- /tasks/{task_id}/complete
- /tasks/{task_id}/uncomplete
- /tasks/cleanup
"""

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta

from app.db.session import get_supabase_admin
from app.core.auth import get_current_user
from .utils import (
    get_user_date,
    calculate_remembering_rate,
    calculate_next_review_date,
)

router = APIRouter()


# ============================================
# PYDANTIC MODELS
# ============================================

class TopicAtRisk(BaseModel):
    topic_id: str
    topic_name: str
    subject: str
    retention_rate: int
    days_until_forgotten: int
    last_studied: str
    difficulty_score: int
    priority_score: int


class PriorityTopic(BaseModel):
    topic_id: str
    topic_name: str
    subject: str
    priority_score: int
    priority_reason: str
    difficulty_score: int
    retention_rate: int
    estimated_study_time: int


class StudyStreak(BaseModel):
    current_streak: int
    longest_streak: int
    streak_status: str
    last_study_date: str
    next_milestone: int


class TimeStats(BaseModel):
    total_study_time_today: int
    total_study_time_week: int
    avg_daily_time: int
    target_daily_time: int
    time_efficiency: int


class TodaysTasksData(BaseModel):
    at_risk_topics: List[TopicAtRisk]
    total_at_risk: int
    priority_topics: List[PriorityTopic]
    total_priority: int
    streak: StudyStreak
    time_stats: TimeStats
    generated_at: str
    student_id: str


class TodaysTasksResponse(BaseModel):
    success: bool
    data: TodaysTasksData
    message: Optional[str] = None


# ============================================
# HELPERS
# ============================================

def build_mock_todays_tasks(student_id: str = "demo", message: str = "Mock data") -> TodaysTasksResponse:
    """Unified mock response"""
    return TodaysTasksResponse(
        success=True,
        data=TodaysTasksData(
            at_risk_topics=[],
            total_at_risk=0,
            priority_topics=[],
            total_priority=0,
            streak=StudyStreak(
                current_streak=0,
                longest_streak=0,
                streak_status="inactive",
                last_study_date="",
                next_milestone=7
            ),
            time_stats=TimeStats(
                total_study_time_today=0,
                total_study_time_week=0,
                avg_daily_time=0,
                target_daily_time=120,
                time_efficiency=0
            ),
            generated_at=datetime.now(timezone.utc).isoformat(),
            student_id=student_id
        ),
        message=message
    )


def group_tests_by_topic(topic_tests: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Groups student_topic_tests by topic_id"""
    topic_performance: Dict[str, Dict[str, Any]] = {}

    for test in topic_tests:
        topic_id = test.get("topic_id")
        if not topic_id:
            continue

        topic_name = "Bilinmeyen"
        subject_name = "Bilinmeyen"

        topics = test.get("topics")
        if topics:
            topic_name = topics.get("name_tr") or topic_name
            subjects = topics.get("subjects")
            if subjects:
                subject_name = subjects.get("name_tr") or subject_name

        if topic_id not in topic_performance:
            topic_performance[topic_id] = {
                "topic_name": topic_name,
                "subject_name": subject_name,
                "tests": []
            }

        topic_performance[topic_id]["tests"].append(test)

    return topic_performance


def calculate_at_risk_topics(topic_performance: Dict[str, Dict[str, Any]], limit: int = 3) -> List[TopicAtRisk]:
    """✅ MOTOR-ALIGNED: At-risk calculation"""
    at_risk: List[TopicAtRisk] = []

    print(f"\n🔍 === AT RISK CALCULATION START ===")
    print(f"📊 Total topics to check: {len(topic_performance)}")

    for topic_id, data in topic_performance.items():
        tests = data.get("tests", [])
        if not tests:
            continue

        latest = tests[0]
        latest_date_raw = latest.get("test_date", "")
        if not latest_date_raw:
            continue

        test_date = datetime.fromisoformat(latest_date_raw.replace("Z", "+00:00"))
        remembering_rate = calculate_remembering_rate(tests)
        next_review = calculate_next_review_date(remembering_rate, test_date)

        topic_name = data.get("topic_name", "Unknown")[:50]
        print(f"\n📌 Topic: {topic_name}")
        print(f"   Rate: {remembering_rate}% | Urgency: {next_review.get('urgency')} | Days: {next_review.get('days_remaining')}")

        if next_review.get("urgency") in ["HEMEN", "ACİL", "YAKIN"]:
            print(f"   ✅ ADDED")
            at_risk.append(
                TopicAtRisk(
                    topic_id=topic_id,
                    topic_name=data.get("topic_name", "Bilinmeyen"),
                    subject=data.get("subject_name", "Bilinmeyen"),
                    retention_rate=int(remembering_rate),
                    days_until_forgotten=int(next_review.get("days_remaining", 0)),
                    last_studied=latest_date_raw,
                    difficulty_score=70,
                    priority_score=85,
                )
            )
        else:
            print(f"   ❌ SKIPPED")

    at_risk.sort(key=lambda x: x.retention_rate)
    print(f"\n📊 SUMMARY: {len(at_risk)} at-risk, returning {len(at_risk[:limit])}")
    print(f"=== END ===\n")

    return at_risk[:limit]


def calculate_priority_topics(topic_performance: Dict[str, Dict[str, Any]], limit: int = 3) -> List[PriorityTopic]:
    """Priority topics based on avg success"""
    priority: List[PriorityTopic] = []

    for topic_id, data in topic_performance.items():
        tests = data.get("tests", [])
        if not tests:
            continue

        recent = tests[:3]
        success_values = [t.get("success_rate", 0) for t in recent]
        avg_success = sum(success_values) / max(1, len(success_values))

        if avg_success < 75:
            pr_score = int(max(0, 100 - avg_success))
            priority.append(
                PriorityTopic(
                    topic_id=topic_id,
                    topic_name=data.get("topic_name", "Bilinmeyen"),
                    subject=data.get("subject_name", "Bilinmeyen"),
                    priority_score=pr_score,
                    priority_reason="difficulty" if avg_success < 60 else "retention",
                    difficulty_score=pr_score,
                    retention_rate=int(avg_success),
                    estimated_study_time=45
                )
            )

    priority.sort(key=lambda x: x.priority_score, reverse=True)
    return priority[:limit]


def calculate_streak(all_tests: List[Dict[str, Any]], x_user_timezone: str) -> StudyStreak:
    """Streak: consecutive days with test entries"""
    today = get_user_date(x_user_timezone)
    streak_days = []
    check_date = today

    for _ in range(365):
        day_tests = [
            t for t in all_tests
            if datetime.fromisoformat(t["test_date"].replace("Z", "+00:00")).date() == check_date
        ]
        if day_tests:
            streak_days.append(check_date)
            check_date -= timedelta(days=1)
        else:
            break

    current_streak = len(streak_days)

    return StudyStreak(
        current_streak=current_streak,
        longest_streak=max(current_streak, 12),
        streak_status="active" if current_streak > 0 else "broken",
        last_study_date=str(streak_days[0]) if streak_days else "",
        next_milestone=7
    )


# ============================================
# TASK CREATION HELPER
# ============================================

def create_daily_tasks(student_id: str, date: str):
    """Create 5 demo tasks for today (will be motor-driven in Batch 2)"""
    supabase = get_supabase_admin()

    MATH_SUBJECT_ID = "e576c099-c3ae-4022-be5c-919929437966"

    tasks = [
        {
            "student_id": student_id,
            "task_date": date,
            "task_type": "test",
            "subject_id": MATH_SUBJECT_ID,
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
            "subject_id": MATH_SUBJECT_ID,
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
            "subject_id": MATH_SUBJECT_ID,
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
            "subject_id": MATH_SUBJECT_ID,
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
            "subject_id": MATH_SUBJECT_ID,
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
    return tasks


# ============================================
# ENDPOINTS
# ============================================

@router.get("/todays-tasks", response_model=TodaysTasksResponse)
async def get_todays_tasks(
    current_user: dict = Depends(get_current_user),
    x_user_timezone: str = Header("UTC")
):
    """🎯 Dashboard Summary"""
    try:
        student_id = current_user["id"]
        supabase = get_supabase_admin()

        all_tests_res = (
            supabase.table("student_topic_tests")
            .select("*, topics(name_tr, subjects(name_tr))")
            .eq("student_id", student_id)
            .order("test_date", desc=True)
            .execute()
        )

        all_tests = all_tests_res.data or []

        if not all_tests:
            return build_mock_todays_tasks(student_id=student_id, message="Henüz test eklenmedi")

        topic_performance = group_tests_by_topic(all_tests)

        at_risk = calculate_at_risk_topics(topic_performance, limit=3)
        priority = calculate_priority_topics(topic_performance, limit=3)
        streak = calculate_streak(all_tests, x_user_timezone)

        time_stats = TimeStats(
            total_study_time_today=45,
            total_study_time_week=380,
            avg_daily_time=54,
            target_daily_time=120,
            time_efficiency=75
        )

        return TodaysTasksResponse(
            success=True,
            data=TodaysTasksData(
                at_risk_topics=at_risk,
                total_at_risk=len(at_risk),
                priority_topics=priority,
                total_priority=len(priority),
                streak=streak,
                time_stats=time_stats,
                generated_at=datetime.now(timezone.utc).isoformat(),
                student_id=student_id
            ),
            message="Gerçek veri"
        )

    except Exception as e:
        print(f"[todays-tasks] Error: {str(e)}")
        student_id = current_user.get("id", "demo") if isinstance(current_user, dict) else "demo"
        return build_mock_todays_tasks(student_id=student_id, message="Fallback mock")


@router.get("/tasks/today")
async def get_todays_tasks_list(
    current_user: dict = Depends(get_current_user),
    x_user_timezone: str = Header("UTC")
):
    """✅ Bugünün görev listesi + AUTO-CREATE"""
    try:
        student_id = current_user["id"]
        supabase = get_supabase_admin()

        today_date = get_user_date(x_user_timezone)
        today_str = today_date.isoformat()

        tasks_res = (
            supabase.table("student_tasks")
            .select("*")
            .eq("student_id", student_id)
            .eq("task_date", today_str)
            .order("priority_level", desc=False)
            .execute()
        )

        tasks = tasks_res.data or []

        # ✅ OTOMATİK TASK CREATION
        if not tasks:
            print(f"⚠️  No tasks for {today_str}, creating...")
            create_daily_tasks(student_id, today_str)
            
            # Yeniden çek
            tasks = (
                supabase.table("student_tasks")
                .select("*")
                .eq("student_id", student_id)
                .eq("task_date", today_str)
                .order("priority_level", desc=False)
                .execute()
            ).data or []

        total_time = sum([t.get("estimated_time_minutes", 0) for t in tasks])
        completed_time = sum([t.get("estimated_time_minutes", 0) for t in tasks if t.get("status") == "completed"])

        # At-risk calculation
        topic_tests_res = (
            supabase.table("student_topic_tests")
            .select("*, topics(name_tr, subjects(name_tr))")
            .eq("student_id", student_id)
            .order("test_date", desc=True)
            .execute()
        )
        topic_tests = topic_tests_res.data or []
        topic_performance = group_tests_by_topic(topic_tests)

        at_risk_models = calculate_at_risk_topics(topic_performance, limit=3)
        at_risk = [m.model_dump() for m in at_risk_models]

        return {
            "success": True,
            "tasks": tasks,
            "summary": {
                "total_tasks": len(tasks),
                "completed_tasks": len([t for t in tasks if t.get("status") == "completed"]),
                "total_time_minutes": total_time,
                "completed_time_minutes": completed_time,
                "remaining_time_minutes": total_time - completed_time
            },
            "at_risk_topics": at_risk,
            "total_at_risk": len(at_risk),
            "date": today_str
        }

    except Exception as e:
        print(f"[tasks/today] Error: {str(e)}")
        return {"success": False, "error": str(e)}


@router.post("/tasks/{task_id}/complete")
async def complete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    manual: bool = True
):
    """Görevi tamamla"""
    try:
        supabase = get_supabase_admin()

        task_res = supabase.table("student_tasks").select("*").eq("id", task_id).execute()
        if not task_res.data:
            return {"success": False, "error": "Görev bulunamadı"}

        task = task_res.data[0]
        if task.get("student_id") != current_user.get("id"):
            raise HTTPException(status_code=403, detail="Bu göreve erişiminiz yok")

        update_data = {
            "status": "completed",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "manual_completion": manual
        }

        result = supabase.table("student_tasks").update(update_data).eq("id", task_id).execute()

        return {
            "success": True,
            "task": result.data[0] if result.data else None,
            "message": "Görev tamamlandı! 🎉"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[complete_task] Error: {str(e)}")
        return {"success": False, "error": str(e)}


@router.post("/tasks/{task_id}/uncomplete")
async def uncomplete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Görevi geri al"""
    try:
        supabase = get_supabase_admin()

        task_res = supabase.table("student_tasks").select("*").eq("id", task_id).execute()
        if not task_res.data:
            return {"success": False, "error": "Görev bulunamadı"}

        task = task_res.data[0]
        if task.get("student_id") != current_user.get("id"):
            raise HTTPException(status_code=403, detail="Bu göreve erişiminiz yok")

        if not task.get("manual_completion", False):
            return {"success": False, "error": "Bu görev otomatik tamamlanmış, geri alınamaz!"}

        update_data = {
            "status": "pending",
            "completed_at": None,
            "manual_completion": False
        }

        result = supabase.table("student_tasks").update(update_data).eq("id", task_id).execute()

        return {
            "success": True,
            "task": result.data[0] if result.data else None,
            "message": "Görev geri alındı"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[uncomplete_task] Error: {str(e)}")
        return {"success": False, "error": str(e)}


@router.delete("/tasks/cleanup")
async def cleanup_tasks(
    date: str,
    current_user: dict = Depends(get_current_user)
):
    """Belirli bir günün görevlerini sil"""
    try:
        supabase = get_supabase_admin()
        student_id = current_user["id"]

        result = (
            supabase.table("student_tasks")
            .delete()
            .eq("student_id", student_id)
            .eq("task_date", date)
            .execute()
        )

        return {
            "success": True,
            "message": f"{date} tarihli görevler silindi",
            "deleted_count": len(result.data) if result.data else 0
        }

    except Exception as e:
        print(f"[cleanup_tasks] Error: {str(e)}")
        return {"success": False, "error": str(e)}