"""
Student Dashboard & Profile Endpoints
FAZ-3 COMPLIANT
- Dashboard reads only from performance module
- No local calculations
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime, timezone, timedelta

from app.db.session import get_supabase_admin
from app.core.auth import get_current_user
from .performance import get_student_performance

router = APIRouter()


# ============================================================
# MOCK / EMPTY DASHBOARD (NO TEST DATA)
# ============================================================

def get_empty_dashboard() -> Dict[str, Any]:
    return {
        "success": True,
        "topics": [],
        "analytics": {
            "weakestTopic": 0,
            "forgetRisk": 0
        },
        "weekly": {
            "tests": 0,
            "average_success": 0
        },
        "monthly": {
            "tests": 0
        },
        "projection": None,
        "cache_info": {
            "source": "empty"
        }
    }


# ============================================================
# DASHBOARD
# ============================================================

@router.get("/dashboard")
async def get_student_dashboard(
    current_user: dict = Depends(get_current_user)
):
    student_id = current_user["id"]

    perf_data = get_student_performance(
        student_id=student_id,
        use_cache=True
    )

    topic_performance = perf_data.get("topic_performance", {})
    all_tests = perf_data.get("all_tests", [])

    if not all_tests:
        return get_empty_dashboard()

    topics_list = []

    for topic_id, data in topic_performance.items():
        tests = data.get("tests", [])

        achievement_badge = None
        if len(tests) >= 2:
            improvement = (
                tests[0].get("success_rate", 0)
                - tests[-1].get("success_rate", 0)
            )
            if improvement > 20:
                achievement_badge = {
                    "text": f"+%{int(improvement)} ({len(tests)} test)",
                    "icon": "⭐"
                }

        topic_obj = {
            "id": topic_id,
            "name": data.get("topic_name"),
            "subject": data.get("subject_name"),
            "rememberingRate": data.get("remembering_rate", 0),
            "status": data.get("status"),
            "statusText": data.get("status_text"),
            "emoji": data.get("emoji"),
            "days_since_last_test": data.get("days_since_last_test"),
            "total_tests": data.get("total_tests", 0),
            "latest_net": data.get("latest_net"),
            "latest_success_rate": data.get("latest_success_rate"),
            "next_review": data.get("next_review")
        }

        if achievement_badge:
            topic_obj["achievementBadge"] = achievement_badge

        topics_list.append(topic_obj)

    topics_list.sort(key=lambda x: x["rememberingRate"])

    worst_topic = topics_list[0]["rememberingRate"] if topics_list else 0

    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    weekly_tests = [
        t for t in all_tests
        if datetime.fromisoformat(
            t["test_date"].replace("Z", "+00:00")
        ) >= week_ago
    ]

    monthly_tests = [
        t for t in all_tests
        if datetime.fromisoformat(
            t["test_date"].replace("Z", "+00:00")
        ) >= month_ago
    ]

    weekly_success = (
        int(sum(t.get("success_rate", 0) for t in weekly_tests) / len(weekly_tests))
        if weekly_tests else 0
    )

    return {
        "success": True,
        "topics": topics_list,
        "analytics": {
            "weakestTopic": worst_topic,
            "forgetRisk": 100 - worst_topic
        },
        "weekly": {
            "tests": len(weekly_tests),
            "average_success": weekly_success
        },
        "monthly": {
            "tests": len(monthly_tests)
        },
        "projection": perf_data.get("projection"),
        "cache_info": perf_data.get("metadata", {})
    }


# ============================================================
# PROFILE
# ============================================================

@router.get("/profile")
async def get_student_profile(
    current_user: dict = Depends(get_current_user)
):
    return {
        "id": current_user["id"],
        "name": current_user.get("name"),
        "email": current_user.get("email"),
        "class": current_user.get("class")
    }


# ============================================================
# TEST LIST
# ============================================================

@router.get("/tests")
async def get_student_tests(
    current_user: dict = Depends(get_current_user)
):
    student_id = current_user["id"]
    supabase = get_supabase_admin()

    tests_response = (
        supabase
        .table("student_topic_tests")
        .select("*, topics(name_tr, subjects(name_tr))")
        .eq("student_id", student_id)
        .order("test_date", desc=True)
        .execute()
    )

    if not tests_response.data:
        return {"tests": []}

    formatted = []
    for test in tests_response.data:
        formatted.append({
            "id": test["id"],
            "test_date": test["test_date"],
            "correct_count": test["correct_count"],
            "wrong_count": test["wrong_count"],
            "empty_count": test["empty_count"],
            "net_score": float(test["net_score"]),
            "success_rate": float(test["success_rate"]),
            "topic": {
                "name_tr": test["topics"]["name_tr"]
                if test.get("topics") else None
            },
            "subject": {
                "name_tr": (
                    test["topics"]["subjects"]["name_tr"]
                    if test.get("topics") and test["topics"].get("subjects")
                    else None
                )
            }
        })

    return {"tests": formatted}


# ============================================================
# WEEKLY SUBJECTS
# ============================================================

@router.get("/weekly-subjects")
async def get_weekly_subjects(
    current_user: dict = Depends(get_current_user)
):
    student_id = current_user["id"]
    supabase = get_supabase_admin()

    week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    tests = (
        supabase
        .table("student_topic_tests")
        .select("*, topics(subjects(id, name_tr))")
        .eq("student_id", student_id)
        .gte("test_date", week_ago.isoformat())
        .execute()
    )

    if not tests.data:
        return {
            "success": True,
            "subjects": []
        }

    subject_stats = {}

    for test in tests.data:
        subj = test.get("topics", {}).get("subjects")
        if not subj:
            continue

        sid = subj["id"]
        subject_stats.setdefault(sid, {
            "name": subj["name_tr"],
            "total_tests": 0,
            "total_success": 0
        })

        subject_stats[sid]["total_tests"] += 1
        subject_stats[sid]["total_success"] += test["success_rate"]

    subjects = [
        {
            "name": s["name"],
            "avg_success": int(s["total_success"] / s["total_tests"]),
            "total_tests": s["total_tests"]
        }
        for s in subject_stats.values()
    ]

    subjects.sort(key=lambda x: x["avg_success"])

    return {
        "success": True,
        "worst_subjects": subjects[:2],
        "best_subjects": list(reversed(subjects[-2:])),
        "all_subjects": subjects
    }
