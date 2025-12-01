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
@router.put("/tests/{test_id}")  # ✅ DOĞRU - Başında boşluk YOK
async def update_test(test_id: str, test_data: dict):
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
async def delete_test(test_id: str):
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
    
    return {"success": True, "message": "Test silindi"}
@router.post("/student/analyze")
async def analyze_student_performance(request: dict):
    """
    4 Motor Analizi
    BS-Model, Difficulty Engine, Time Analyzer, Priority Engine
    """
    student_id = request.get("student_id")
    
    if not student_id:
        return {"error": "student_id gerekli"}
    
    supabase = get_supabase_admin()
    
    # Tüm testleri çek
    all_tests = supabase.table("student_topic_tests").select(
        "*, topics(name_tr, difficulty_level, subjects(name_tr))"
    ).eq("student_id", student_id).order("test_date", desc=True).execute()
    
    if not all_tests.data or len(all_tests.data) == 0:
        return {
            "status": "no_data",
            "message": "Henüz test verisi yok",
            "bs_model": {"urgent_topics": []},
            "difficulty_engine": {"struggling_topics": []},
            "time_analyzer": {"slow_topics": []},
            "priority_engine": {"this_week_topics": []}
        }
    
    # Topic bazında grupla
    topic_performance = {}
    now = datetime.now(timezone.utc)
    
    for test in all_tests.data:
        topic_id = test["topic_id"]
        
        if topic_id not in topic_performance:
            topic_performance[topic_id] = {
                "topic_id": topic_id,
                "topic_name": test["topics"]["name_tr"] if test.get("topics") else "Unknown",
                "subject_name": test["topics"]["subjects"]["name_tr"] if test.get("topics") and test["topics"].get("subjects") else "Unknown",
                "difficulty_level": test["topics"].get("difficulty_level", 3) if test.get("topics") else 3,
                "tests": []
            }
        
        topic_performance[topic_id]["tests"].append(test)
    
    # BS-MODEL
    bs_model_topics = []
    
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        latest_test = tests[0]
        test_date = datetime.fromisoformat(latest_test["test_date"].replace('Z', '+00:00'))
        days_since = (now - test_date).days
        
        remembering_rate = calculate_remembering_rate(tests)
        next_review = calculate_next_review_date(remembering_rate, test_date)
        
        urgency_score = 0
        
        if next_review["urgency"] == "HEMEN":
            urgency_score = 100
        elif next_review["urgency"] == "ACİL":
            urgency_score = 80
        elif next_review["urgency"] == "YAKIN":
            urgency_score = 60
        elif next_review["urgency"] == "NORMAL":
            urgency_score = 40
        else:
            urgency_score = 20
        
        forgetting_risk = 100 - remembering_rate
        urgency_score += forgetting_risk * 0.3
        urgency_score = min(100, urgency_score)
        
        if urgency_score >= 60:
            bs_model_topics.append({
                "topic_name": data["topic_name"],
                "subject_name": data["subject_name"],
                "remembering_rate": remembering_rate,
                "days_since_last_test": days_since,
                "next_review_urgency": next_review["urgency"],
                "urgency_score": int(urgency_score),
                "recommendation": f"{next_review['urgency']} - {next_review['days_remaining']} gün içinde tekrar et"
            })
    
    bs_model_topics.sort(key=lambda x: x["urgency_score"], reverse=True)
    
    # DIFFICULTY ENGINE
    difficulty_topics = []
    
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        recent_tests = tests[:3]
        avg_success = sum([t["success_rate"] for t in recent_tests]) / len(recent_tests)
        
        difficulty_score = 0
        
        if avg_success < 50:
            difficulty_score = 80 + (50 - avg_success)
        elif avg_success < 70:
            difficulty_score = 60 + (70 - avg_success)
        else:
            difficulty_score = max(0, 60 - (avg_success - 70))
        
        if len(tests) < 3 and avg_success < 60:
            difficulty_score += 20
        
        difficulty_score = min(100, difficulty_score)
        
        if difficulty_score >= 60:
            difficulty_topics.append({
                "topic_name": data["topic_name"],
                "subject_name": data["subject_name"],
                "difficulty_score": int(difficulty_score),
                "average_success": round(avg_success, 1),
                "total_tests": len(tests),
                "topic_difficulty_level": data["difficulty_level"],
                "recommendation": "Bu konuya daha fazla zaman ayır"
            })
    
    difficulty_topics.sort(key=lambda x: x["difficulty_score"], reverse=True)
    
    # TIME ANALYZER
    time_topics = []
    
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        
        if len(tests) >= 2:
            intervals = []
            for i in range(len(tests) - 1):
                t1 = datetime.fromisoformat(tests[i]["test_date"].replace('Z', '+00:00'))
                t2 = datetime.fromisoformat(tests[i+1]["test_date"].replace('Z', '+00:00'))
                intervals.append((t1 - t2).days)
            
            avg_interval = sum(intervals) / len(intervals)
            
            if avg_interval > 30:
                time_topics.append({
                    "topic_name": data["topic_name"],
                    "subject_name": data["subject_name"],
                    "average_interval_days": round(avg_interval, 1),
                    "total_tests": len(tests),
                    "recommendation": f"Bu konuya {int(avg_interval)} günde bir dönüyorsun. Daha sık tekrar et!"
                })
    
    time_topics.sort(key=lambda x: x["average_interval_days"], reverse=True)
    
    # PRIORITY ENGINE
    priority_topics = []
    
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        latest_test = tests[0]
        
        remembering_rate = calculate_remembering_rate(tests)
        
        priority_score = 0
        forgetting_risk = 100 - remembering_rate
        priority_score += forgetting_risk * 0.5
        
        difficulty = data["difficulty_level"]
        priority_score += difficulty * 5
        
        if len(tests) < 3:
            priority_score += 20
        
        if latest_test["success_rate"] < 60:
            priority_score += 15
        
        priority_score = min(100, priority_score)
        
        if priority_score >= 50:
            priority_level = "CRITICAL" if priority_score >= 80 else "HIGH" if priority_score >= 65 else "MEDIUM" 
            
            priority_topics.append({
                "topic_name": data["topic_name"],
                "subject_name": data["subject_name"],
                "priority_score": int(priority_score),
                "priority_level": priority_level,
                "remembering_rate": remembering_rate,
                "difficulty_level": difficulty,
                "total_tests": len(tests),
                "recommendation": f"{priority_level} öncelik - Bu hafta mutlaka çalış"
            })
    
    priority_topics.sort(key=lambda x: x["priority_score"], reverse=True)
    
    return {
        "status": "success",
        "analyzed_topics": len(topic_performance),
        "bs_model": {
            "name": "Akıllı Tekrar Planlayıcı",
            "description": "Unutma eğrisine göre optimal tekrar zamanı",
            "urgent_topics": bs_model_topics[:10]
        },
        "difficulty_engine": {
            "name": "Zorluk Analizi",
            "description": "Hangi konularda zorlanıyorsun",
            "struggling_topics": difficulty_topics[:10]
        },
        "time_analyzer": {
            "name": "Hız Analizi",
            "description": "Hangi konulara yeterince zaman ayırmıyorsun",
            "slow_topics": time_topics[:10]
        },
        "priority_engine": {
            "name": "Öncelik Motoru",
            "description": "Bu hafta hangi konulara odaklanmalısın",
            "this_week_topics": priority_topics[:10]
        }
    }