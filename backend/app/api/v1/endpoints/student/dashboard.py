"""
Student Dashboard & Profile Endpoints
- Dashboard stats
- Profile
- Tests list
- Weekly subjects
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from app.db.session import get_supabase_admin
from .utils import calculate_remembering_rate, format_turkish_date, calculate_next_review_date, calculate_status, get_mock_topics, calculate_realistic_projection, EXAM_DATE

router = APIRouter()

# Mock data fonksiyonu (geçici)
def get_mock_dashboard():
    """Mock dashboard data"""
    return {
        "success": True,
        "message": "Mock data - henüz test girişi yok",
        "topics": []
    }

@router.get("/student/{student_id}/dashboard")
async def get_student_dashboard(student_id: str):
    """Öğrenci dashboard verisi"""
    
    supabase = get_supabase_admin()
    
    all_tests = supabase.table("student_topic_tests").select(
        "*, topics(name_tr, subjects(name_tr, icon))"
    ).eq("student_id", student_id).order("test_date", desc=True).execute()
    
    if not all_tests.data:
        return get_mock_dashboard()
    
    topic_performance = {}
    
    for test in all_tests.data:
        topic_id = test["topic_id"]
        
        if topic_id not in topic_performance:
            topic_performance[topic_id] = {
                "topic_id": topic_id,
                "topic_name": test["topics"]["name_tr"] if test.get("topics") else "Unknown",
                "subject_name": test["topics"]["subjects"]["name_tr"] if test.get("topics") and test["topics"].get("subjects") else "Unknown",
                "tests": []
            }
        
        topic_performance[topic_id]["tests"].append(test)
    
    topics_list = []
    now = datetime.now(timezone.utc)
    
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        latest_test = tests[0]
        
        remembering_rate = calculate_remembering_rate(tests)
        
        test_date = datetime.fromisoformat(latest_test["test_date"].replace('Z', '+00:00'))
        days_since_last_test = (now - test_date).days
        
        next_review = calculate_next_review_date(remembering_rate, test_date)
        
        status, status_text, emoji = calculate_status(remembering_rate, days_since_last_test)
        
        achievement_badge = None
        if len(tests) >= 2:
            improvement = tests[0]["success_rate"] - tests[-1]["success_rate"]
            if improvement > 20:
                achievement_badge = {
                    "text": f"+%{int(improvement)} ({len(tests)} test)",
                    "icon": "⭐"
                }
        
        topic_obj = {
            "id": topic_id,
            "name": data["topic_name"],
            "subject": data["subject_name"],
            "rememberingRate": remembering_rate,
            "status": status,
            "statusText": status_text,
            "emoji": emoji,
            "days_since_last_test": days_since_last_test,
            "total_tests": len(tests),
            "latest_net": float(latest_test["net_score"]),
            "latest_success_rate": float(latest_test["success_rate"]),
            "next_review": {
                "days_remaining": next_review["days_remaining"],
                "urgency": next_review["urgency"]
            }
        }
        
        if achievement_badge:
            topic_obj["achievementBadge"] = achievement_badge
        
        topics_list.append(topic_obj)
    
    topics_list.sort(key=lambda x: x["rememberingRate"])
    
    if len(topics_list) < 5:
        mock_topics = get_mock_topics()
        needed = 5 - len(topics_list)
        topics_list.extend(mock_topics[:needed])
    
    top_topics = topics_list[:5]
    
    projection = calculate_realistic_projection(all_tests.data, topic_performance)
    
    critical_alert = None
    if top_topics and top_topics[0]["rememberingRate"] < 50:
        worst = top_topics[0]
        critical_alert = {
            "show": True,
            "topicName": worst["name"],
            "daysAgo": worst["days_since_last_test"],
            "forgetRisk": 100 - worst["rememberingRate"]
        }
    
    week_ago = now - timedelta(days=7)
    weekly_tests = [
        t for t in all_tests.data 
        if datetime.fromisoformat(t["test_date"].replace('Z', '+00:00')) >= week_ago
    ]
    
    weekly_success = int((sum([t["success_rate"] for t in weekly_tests]) / len(weekly_tests)) if weekly_tests else 0)
    
    today = now.date()
    today_tests = [
        t for t in all_tests.data 
        if datetime.fromisoformat(t["test_date"].replace('Z', '+00:00')).date() == today
    ]
    
    return {
        "student_name": "Demo Öğrenci",
        "streak": 7,
        "daily_goal": {
            "current": len(today_tests),
            "target": 5
        },
        "weekly_success": weekly_success,
        "weekly_target": 85,
        "study_time_today": len(today_tests) * 15,
        "weekly_questions": len(weekly_tests) * 12,
        "weekly_increase": 25 if len(weekly_tests) > 0 else 0,
        "topics": top_topics,
        "critical_alert": critical_alert,
        "projection": projection
    }


def get_mock_dashboard():
    """Mock dashboard"""
    return {
        "student_name": "Demo Öğrenci",
        "streak": 0,
        "daily_goal": {"current": 0, "target": 5},
        "weekly_success": 0,
        "weekly_target": 85,
        "study_time_today": 0,
        "weekly_questions": 0,
        "weekly_increase": 0,
        "topics": get_mock_topics()[:5],
        "critical_alert": {"show": True, "topicName": "İlk Testinizi Ekleyin", "daysAgo": 0, "forgetRisk": 0},
        "projection": {
            "status": "no_data",
            "total_topics": 0,
            "completed_topics": 0,
            "remaining_topics": 0,
            "estimated_days": 0,
            "estimated_date": "Veri yetersiz",
            "velocity": "0 konu/gün",
            "warning_level": "info",
            "message": "Test ekledikçe hesaplanacak"
        }
    }


@router.get("/student/{student_id}/profile")
async def get_student_profile(student_id: str):
    return {"id": student_id, "name": "Demo Öğrenci", "email": "demo@endstp.com", "class": "11. Sınıf"}


@router.get("/student/{student_id}/tests")
async def get_student_tests(student_id: str):
    """
    Öğrencinin tüm test geçmişini getir
    """
    supabase = get_supabase_admin()
    
    # Testleri çek (topic ve subject bilgileriyle)
    tests_response = supabase.table("student_topic_tests").select(
        "*, topics(name_tr, subject_id, subjects(name_tr))"
    ).eq("student_id", student_id).order("test_date", desc=True).execute()
    
    if not tests_response.data:
        return {"tests": []}
    
    # Formatla
    formatted_tests = []
    for test in tests_response.data:
        formatted_tests.append({
            "id": test["id"],
            "test_date": test["test_date"],
            "correct_count": test["correct_count"],
            "wrong_count": test["wrong_count"],
            "empty_count": test["empty_count"],
            "net_score": float(test["net_score"]),
            "success_rate": float(test["success_rate"]),
            "topic": {
                "name_tr": test["topics"]["name_tr"] if test.get("topics") else "Bilinmeyen"
            },
            "subject": {
                "name_tr": test["topics"]["subjects"]["name_tr"] if test.get("topics") and test["topics"].get("subjects") else "Bilinmeyen"
            }
        })
    
    return {"tests": formatted_tests}
@router.get("/student/weekly-subjects")
async def get_weekly_subjects(student_id: str):
    """
    Son 7 günün ders bazlı performansı
    """
    try:
        supabase = get_supabase_admin()
        
        # Son 7 günün testlerini çek
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        
        tests = supabase.table("student_topic_tests").select(
            "*, topics(name_tr, subjects(id, name_tr))"
        ).eq("student_id", student_id).gte("test_date", week_ago.isoformat()).execute()
        
        if not tests.data:
            return {
                "success": True,
                "subjects": [],
                "message": "Son 7 günde test yok"
            }
        
        # Ders bazında grupla
        subject_stats = {}
        
        for test in tests.data:
            if not test.get("topics") or not test["topics"].get("subjects"):
                continue
                
            subject_id = test["topics"]["subjects"]["id"]
            subject_name = test["topics"]["subjects"]["name_tr"]
            
            if subject_id not in subject_stats:
                subject_stats[subject_id] = {
                    "name": subject_name,
                    "total_tests": 0,
                    "total_success": 0
                }
            
            subject_stats[subject_id]["total_tests"] += 1
            subject_stats[subject_id]["total_success"] += test["success_rate"]
        
        # Ortalama hesapla
        subjects = []
        for subject_id, stats in subject_stats.items():
            avg_success = int(stats["total_success"] / stats["total_tests"])
            subjects.append({
                "name": stats["name"],
                "avg_success": avg_success,
                "total_tests": stats["total_tests"]
            })
        
        # Başarıya göre sırala
        subjects.sort(key=lambda x: x["avg_success"])
        
        # En kötü 2, en iyi 2
        worst = subjects[:2] if len(subjects) >= 2 else subjects
        best = subjects[-2:] if len(subjects) >= 2 else []
        best.reverse()
        
        return {
            "success": True,
            "worst_subjects": worst,
            "best_subjects": best,
            "all_subjects": subjects
        }
        
    except Exception as e:
        print(f"Weekly subjects error: {str(e)}")
        return {"success": False, "error": str(e)}
# student.py'nin en sonuna ekle

# ============================================
# 📋 SUPPORT FEEDBACK ENDPOINTS
# ============================================
