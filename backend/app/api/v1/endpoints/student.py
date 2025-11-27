"""
Student Dashboard Endpoints
v3.1: Türkçe Tarih + Gerçekçi Projeksiyon
"""

from fastapi import APIRouter
from app.db.session import get_supabase_admin
from datetime import datetime, timedelta, timezone

router = APIRouter()

# Türkçe ay isimleri
TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}

# Sınav tarihi (Config - Gerçekte DB'den gelecek)
EXAM_DATE = datetime(2025, 6, 15, tzinfo=timezone.utc)


def format_turkish_date(date_obj):
    """Tarihi Türkçe formatta döndür: '8 Aralık'"""
    day = date_obj.day
    month = TURKISH_MONTHS[date_obj.month]
    return f"{day} {month}"


def calculate_next_review_date(remembering_rate, last_test_date):
    """Optimal tekrar tarihini hesapla"""
    if remembering_rate >= 85:
        interval_days = 14
        urgency = "RAHAT"
    elif remembering_rate >= 70:
        interval_days = 7
        urgency = "NORMAL"
    elif remembering_rate >= 50:
        interval_days = 3
        urgency = "YAKIN"
    elif remembering_rate >= 30:
        interval_days = 1
        urgency = "ACİL"
    else:
        interval_days = 0
        urgency = "HEMEN"
    
    next_date = last_test_date + timedelta(days=interval_days)
    
    return {
        "date": next_date,
        "days_remaining": interval_days,
        "urgency": urgency
    }


def calculate_remembering_rate(tests_data):
    """Basit unutma eğrisi hesaplama"""
    if not tests_data:
        return 0
    
    latest_test = tests_data[0]
    test_date = datetime.fromisoformat(latest_test["test_date"].replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    days_passed = (now - test_date).days
    
    success_rate = latest_test["success_rate"]
    forgetting_factor = max(0, 100 - (days_passed * 5))
    remembering_rate = int((success_rate * forgetting_factor) / 100)
    
    return max(0, min(100, remembering_rate))


def calculate_status(remembering_rate, days_since_last_test):
    """Konu durumunu hesapla"""
    if remembering_rate >= 85:
        return "excellent", "MÜKEMMEL", "🟢"
    elif remembering_rate >= 70:
        return "good", "İYİ GİDİYOR", "💚"
    elif remembering_rate >= 50:
        return "warning", "DİKKAT - Bu Hafta", "🟡"
    elif remembering_rate >= 30:
        return "frozen", "DONMUŞ - Acil Çöz", "❄️"
    else:
        return "critical", "KRİTİK DURUM", "🔥"


def calculate_realistic_projection(all_tests, topic_performance):
    """
    ✅ GERÇEKÇI PROJEKSİYON ALGORİTMASI
    Son 30 günün performansına göre tahmin
    """
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    
    total_topics = len(topic_performance)
    
    completed_topics = []
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        remembering_rate = calculate_remembering_rate(tests)
        if remembering_rate >= 85:
            completed_topics.append({
                "topic_id": topic_id,
                "completed_at": tests[0]["test_date"]
            })
    
    completed_count = len(completed_topics)
    remaining_count = total_topics - completed_count
    
    recent_completions = [
        c for c in completed_topics
        if datetime.fromisoformat(c["completed_at"].replace('Z', '+00:00')) >= thirty_days_ago
    ]
    recent_completion_count = len(recent_completions)
    
    if recent_completion_count == 0:
        velocity = 0.1
        velocity_text = "0.1 konu/gün (ÇOK YAVAŞ!)"
    else:
        velocity = recent_completion_count / 30
        velocity_text = f"{velocity:.2f} konu/gün"
    
    if remaining_count == 0:
        return {
            "status": "completed",
            "total_topics": total_topics,
            "completed_topics": completed_count,
            "remaining_topics": 0,
            "estimated_days": 0,
            "estimated_date": "Tamamlandı! 🎉",
            "velocity": velocity_text,
            "warning_level": "success",
            "message": "Tebrikler! Tüm konular yeşil! 🎉"
        }
    
    days_needed = int(remaining_count / velocity)
    estimated_finish_date = now + timedelta(days=days_needed)
    
    days_until_exam = (EXAM_DATE - now).days
    days_difference = (EXAM_DATE - estimated_finish_date).days
    
    if days_difference < 0:
        warning_level = "danger"
        percentage_complete_by_exam = int((days_until_exam * velocity / remaining_count) * 100)
        message = f"TEHLİKE! Bu hızla sınava konuların sadece %{percentage_complete_by_exam}'i yetişecek!"
    elif days_difference < 30:
        warning_level = "warning"
        message = f"DİKKAT! Bitiş tarihi sınava çok yakın. Hızlanmalısın!"
    else:
        warning_level = "success"
        message = f"Harika! Bu hızla {days_difference} gün önceden bitecek. Son ay full tekrar!"
    
    target_finish_date = EXAM_DATE - timedelta(days=30)
    days_until_target = (target_finish_date - now).days
    
    if days_until_target > 0:
        required_velocity = remaining_count / days_until_target
        required_velocity_text = f"{required_velocity:.2f} konu/gün"
        
        if velocity < required_velocity:
            velocity_warning = f"Gerekli hız: {required_velocity_text} (Şu anki: {velocity_text})"
        else:
            velocity_warning = None
    else:
        required_velocity_text = "Çok geç!"
        velocity_warning = "Hedef tarih geçti!"
    
    return {
        "status": "in_progress",
        "total_topics": total_topics,
        "completed_topics": completed_count,
        "remaining_topics": remaining_count,
        "estimated_days": days_needed,
        "estimated_date": format_turkish_date(estimated_finish_date),  # ✅ TÜRKÇE TARİH
        "velocity": velocity_text,
        "required_velocity": required_velocity_text,
        "warning_level": warning_level,
        "message": message,
        "velocity_warning": velocity_warning,
        "days_until_exam": days_until_exam
    }


def get_mock_topics():
    """Mock konular"""
    return [
        {
            "id": "mock-1",
            "name": "Daha fazla konu test et",
            "subject": "Test Entry'den ekle",
            "rememberingRate": 0,
            "status": "warning",
            "statusText": "YENİ TEST BEKLİYOR",
            "emoji": "📝",
            "days_since_last_test": 999,
            "total_tests": 0,
            "latest_net": 0,
            "latest_success_rate": 0,
            "next_review": {
                "days_remaining": 0,
                "urgency": "BEKLIYOR"
            }
        }
    ]


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
