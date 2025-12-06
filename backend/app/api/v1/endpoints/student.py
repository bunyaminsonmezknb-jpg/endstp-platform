"""
Student Dashboard Endpoints
v3.1: Türkçe Tarih + Gerçekçi Projeksiyon
"""

from fastapi import APIRouter, HTTPException, Header
from app.db.session import get_supabase_admin
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Türkçe ay isimleri
TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}


# Timezone helper
def get_user_date(user_timezone: str = "UTC"):
    """
    Kullanıcının timezone'una göre bugünün tarihini döndür
    """
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(user_timezone)
        return datetime.now(tz).date()
    except Exception as e:
        print(f"Timezone error: {e}, falling back to UTC")
        return datetime.now(timezone.utc).date()
# Sınav tarihi (Config - Gerçekte DB'den gelecek)
EXAM_DATE = datetime(2026, 6, 15, tzinfo=timezone.utc)


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
@router.post("/student/projection")
async def get_student_projection(request: dict):
    """
    Öğrenci ilerleme projeksiyonu
    """
    student_id = request.get("student_id")
    
    if not student_id:
        return {"error": "student_id gerekli"}
    
    try:
        supabase = get_supabase_admin()
        
        # ✅ DÜZELTME: student_topic_tests tablosundan çek
        all_tests = supabase.table("student_topic_tests").select(
            "*, topics(name_tr, subjects(name_tr))"
        ).eq("student_id", student_id).order("test_date", desc=True).execute()
        
        if not all_tests.data:
            return {
                "status": "no_data",
                "projection": {
                    "total_topics": 0,
                    "completed_topics": 0,
                    "remaining_topics": 0,
                    "progress_percent": 0,
                    "velocity": 0,
                    "estimated_days": 0,
                    "estimated_date": "Veri yetersiz"
                }
            }
        
        # Topic bazında grupla
        topic_performance = {}
        for test in all_tests.data:
            topic_id = test["topic_id"]
            if topic_id not in topic_performance:
                topic_performance[topic_id] = {
                    "tests": []
                }
            topic_performance[topic_id]["tests"].append(test)
        
        total_topics = len(topic_performance)
        
        # Tamamlanan konular (%85+ hatırlama oranı)
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
        remaining_topics = total_topics - completed_count
        
        # İlerleme yüzdesi
        progress_percent = (completed_count / total_topics * 100) if total_topics > 0 else 0
        
        # VELOCITY HESAPLAMA
        from datetime import datetime, timedelta
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)
        
        recent_completions = [
            c for c in completed_topics 
            if datetime.fromisoformat(c["completed_at"].replace('Z', '+00:00')) >= thirty_days_ago
        ]
        
        velocity = len(recent_completions) / 30
        
        if velocity == 0 and completed_count > 0:
            # Tüm geçmişe göre hesapla
            first_test_date = min([test["test_date"] for test in all_tests.data])
            days_since_start = (now - datetime.fromisoformat(first_test_date.replace('Z', '+00:00'))).days
            if days_since_start > 0:
                velocity = completed_count / max(days_since_start, 1)
        
        # TAHMİNİ SÜRE
        if velocity > 0 and remaining_topics > 0:
            estimated_days = int(remaining_topics / velocity)
        elif remaining_topics == 0:
            estimated_days = 0
        else:
            # Varsayılan: Haftada 2 konu
            estimated_days = int(remaining_topics * 3.5)
        
        # TAHMİNİ TARİH - TÜRKÇE
        estimated_date_obj = now + timedelta(days=estimated_days)
        estimated_date = format_turkish_date(estimated_date_obj)
        
        return {
            "status": "success",
            "projection": {
                "total_topics": total_topics,
                "completed_topics": completed_count,
                "remaining_topics": remaining_topics,
                "progress_percent": round(progress_percent, 1),
                "velocity": round(velocity, 2),
                "estimated_days": estimated_days,
                "estimated_date": estimated_date
            }
        }
        
    except Exception as e:
        print(f"Projection error: {str(e)}")
        return {"error": str(e)}
@router.post("/student/goal")
async def get_university_goal(request: dict):
    """
    Üniversite hedefi ilerlemesi (MVP - 12. sınıf için)
    """
    student_id = request.get("student_id")
    
    if not student_id:
        return {"error": "student_id gerekli"}
    
    try:
        supabase = get_supabase_admin()
        
        # Öğrencinin tüm testlerini al
        all_tests = supabase.table("student_topic_tests").select(
            "*, topics(name_tr, subjects(name_tr))"
        ).eq("student_id", student_id).order("test_date", desc=True).execute()
        
        if not all_tests.data:
            return {
                "status": "no_data",
                "active_goal": None,
                "ladder": []
            }
        
        # Ders bazlı net hesaplama
        subject_stats = {}
        for test in all_tests.data:
            subject = test["topics"]["subjects"]["name_tr"] if test.get("topics") and test["topics"].get("subjects") else "Diğer"
            
            if subject not in subject_stats:
                subject_stats[subject] = {
                    'total_correct': 0,
                    'total_questions': 0
                }
            
            subject_stats[subject]['total_correct'] += test['correct_count']
            subject_stats[subject]['total_questions'] += (test['correct_count'] + test['wrong_count'] + test['empty_count'])
        
        # TYT Tahmini (120 soru: Türkçe 40, Matematik 40, Sosyal 20, Fen 20)
        tyt_structure = {
            'Türkçe': 40,
            'Matematik': 40,
            'Sosyal Bilimler': 20,
            'Fen Bilimleri': 20
        }
        
        tyt_subjects = []
        tyt_total = 0
        for subject, question_count in tyt_structure.items():
            stats = subject_stats.get(subject, {'total_correct': 0, 'total_questions': 1})
            ratio = stats['total_correct'] / stats['total_questions'] if stats['total_questions'] > 0 else 0
            estimated = int(question_count * ratio)
            
            tyt_subjects.append({
                'name': subject,
                'current': estimated,
                'target': question_count
            })
            tyt_total += estimated
        
        # AYT Sayısal Tahmini (80 soru: Mat 40, Fiz 14, Kim 13, Bio 13)
        ayt_structure = {
            'Matematik': 40,
            'Fizik': 14,
            'Kimya': 13,
            'Biyoloji': 13
        }
        
        ayt_subjects = []
        ayt_total = 0
        for subject, question_count in ayt_structure.items():
            stats = subject_stats.get(subject, {'total_correct': 0, 'total_questions': 1})
            ratio = stats['total_correct'] / stats['total_questions'] if stats['total_questions'] > 0 else 0
            estimated = int(question_count * ratio)
            
            ayt_subjects.append({
                'name': subject,
                'current': estimated,
                'target': question_count
            })
            ayt_total += estimated
        
        # Hedef tercihler (Mock data - gerçekte DB'den gelecek)
        GOALS = [
            {"priority": 1, "university": "Konya Teknik Ünv.", "department": "Bilgisayar Müh.", "tyt": 20, "ayt": 15},
            {"priority": 2, "university": "Antalya Bilim Ünv.", "department": "Bilgisayar Müh.", "tyt": 85, "ayt": 60},
            {"priority": 3, "university": "Selçuk Üniversitesi", "department": "Bilgisayar Müh.", "tyt": 100, "ayt": 76},
            {"priority": 4, "university": "Ankara Üniversitesi", "department": "Bilgisayar Müh.", "tyt": 105, "ayt": 80},
            {"priority": 5, "university": "İTÜ", "department": "Bilgisayar Müh.", "tyt": 110, "ayt": 85},
        ]
        
        # Aktif hedef (3. tercih)
        # Aktif hedef = İlk başarılmamış tercih
        active_goal = None
        for goal in GOALS:
            tyt_p = min(100, int((tyt_total / goal["tyt"]) * 100))
            ayt_p = min(100, int((ayt_total / goal["ayt"]) * 100))
            combined_p = int((tyt_p * 0.4) + (ayt_p * 0.6))
            
            if combined_p < 100:  # Henüz başarılmamış
                active_goal = goal
                break

        # Eğer hepsi başarıldıysa, en son tercihi göster
        if not active_goal:
            active_goal = GOALS[-1]
        
        # TYT progress
        tyt_progress = min(100, int((tyt_total / active_goal["tyt"]) * 100))
        tyt_remaining = max(0, active_goal["tyt"] - tyt_total)
        
        # AYT progress
        ayt_progress = min(100, int((ayt_total / active_goal["ayt"]) * 100))
        ayt_remaining = max(0, active_goal["ayt"] - ayt_total)
        
        # Genel progress (ağırlıklı: TYT %40, AYT %60)
        overall_progress = int((tyt_progress * 0.4) + (ayt_progress * 0.6))
        
        # Sınava kalan gün
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        exam_date = datetime(2026, 6, 15, tzinfo=timezone.utc)
        days_remaining = (exam_date - now).days
        
        # Günlük artış gerekliliği (TYT için)
        if tyt_remaining > 0 and days_remaining > 0:
            tyt_daily_increase = round(tyt_remaining / days_remaining, 1)
        else:
            tyt_daily_increase = 0.0

        # Günlük artış gerekliliği (AYT için)
        if ayt_remaining > 0 and days_remaining > 0:
            ayt_daily_increase = round(ayt_remaining / days_remaining, 1)
        else:
            ayt_daily_increase = 0.0
        
        # Merdiven (5 tercih)
        ladder = []
        for goal in GOALS:
            tyt_p = min(100, int((tyt_total / goal["tyt"]) * 100))
            ayt_p = min(100, int((ayt_total / goal["ayt"]) * 100))
            combined_p = int((tyt_p * 0.4) + (ayt_p * 0.6))
            
            if combined_p >= 100:
                status = "achieved"
            elif combined_p >= 80:
                status = "close"
            elif combined_p >= 50:
                status = "inProgress"
            else:
                status = "distant"
            
            ladder.append({
                "priority": goal["priority"],
                "universityName": goal["university"],
                "departmentName": goal["department"],
                "requiredTYT": goal["tyt"],
                "requiredAYT": goal["ayt"],
                "currentProgress": combined_p,
                "status": status
            })
        
        return {
            "status": "success",
            "overall_progress": overall_progress,
            "days_remaining": days_remaining,
            "tyt": {
                "current_net": tyt_total,
                "target_net": active_goal["tyt"],
                "progress_percent": tyt_progress,
                "remaining_net": tyt_remaining,
                "daily_increase_needed": tyt_daily_increase,  # ← YENİ
                "subjects": tyt_subjects
            },
            "ayt": {
                "current_net": ayt_total,
                "target_net": active_goal["ayt"],
                "progress_percent": ayt_progress,
                "remaining_net": ayt_remaining,
                "daily_increase_needed": ayt_daily_increase,  # ← Değişken adı
                "subjects": ayt_subjects
            },
            "active_goal": {
                "university": active_goal["university"],
                "department": active_goal["department"],
                "level": active_goal["priority"]
            },
            "ladder": ladder
        }
        
    except Exception as e:
        print(f"Goal error: {str(e)}")
        return {"error": str(e)}

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
        
        # Test süreleri varsa hesapla
        test_durations = [t["test_duration_minutes"] for t in tests if t.get("test_duration_minutes")]
        
        if test_durations:
            # Soru başına ortalama süre (12 soru varsayımı)
            avg_duration_per_question = sum(test_durations) / len(test_durations) / 12
            avg_duration_per_question = round(avg_duration_per_question, 2)
            
            # Hedef: 2 dk/soru (iyi), 2-3 dk (normal), 3+ dk (yavaş)
            if avg_duration_per_question > 2.0:
                time_topics.append({
                    "topic_name": data["topic_name"],
                    "subject_name": data["subject_name"],
                    "average_interval_days": avg_duration_per_question,  # Şimdi bu "dk/soru" anlamında
                    "total_tests": len(tests),
                    "days_since_last_test": (now - datetime.fromisoformat(tests[0]["test_date"].replace('Z', '+00:00'))).days,
                    "average_success": sum([t["success_rate"] for t in tests]) / len(tests),
                    "recommendation": f"Soru başına {avg_duration_per_question} dk - {'Hızını artırmalısın!' if avg_duration_per_question > 3 else 'Biraz daha hızlı ol'}"
                })
        elif len(tests) >= 2:
            # Eski mantık: Testler arası gün sayısı (fallback)
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
                    "days_since_last_test": (now - datetime.fromisoformat(tests[0]["test_date"].replace('Z', '+00:00'))).days,
                    "average_success": sum([t["success_rate"] for t in tests]) / len(tests),
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
# ============================================
# 🎯 BUGÜNKÜ GÖREVLER (3 KART)
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

class TodaysTasksDataOld(BaseModel):
    at_risk_topics: List[TopicAtRisk]
    total_at_risk: int
    priority_topics: List[PriorityTopic]
    total_priority: int
    streak: StudyStreak
    time_stats: TimeStats
    generated_at: str
    student_id: str

class TodaysTasksResponseOld(BaseModel):
    success: bool
    data: TodaysTasksDataOld
    message: Optional[str] = None


@router.get("/student/todays-tasks", response_model=TodaysTasksResponseOld)
async def get_todays_tasks(x_user_timezone: str = Header("UTC")):
    """🎯 Bugünkü Görevler - Gerçek Veri"""
    try:
        # Demo student ID (gerçekte auth'dan gelecek)
        student_id = "53a971d3-7492-4670-a31d-ca8422d0781b"
        
        supabase = get_supabase_admin()
        
        # Tüm testleri çek
        all_tests = supabase.table("student_topic_tests").select(
            "*, topics(name_tr, subjects(name_tr))"
        ).eq("student_id", student_id).order("test_date", desc=True).execute()
        
        if not all_tests.data:
            # Veri yoksa mock data döndür
            return get_mock_todays_tasks()
        
        # Topic bazında grupla
        topic_performance = {}
        for test in all_tests.data:
            topic_id = test["topic_id"]
            if topic_id not in topic_performance:
                topic_performance[topic_id] = {
                    "topic_name": test["topics"]["name_tr"] if test.get("topics") else "Bilinmeyen",
                    "subject_name": test["topics"]["subjects"]["name_tr"] if test.get("topics") and test["topics"].get("subjects") else "Bilinmeyen",
                    "tests": []
                }
            topic_performance[topic_id]["tests"].append(test)
        
        # AT RISK TOPICS (retention rate düşük)
        at_risk = []
        for topic_id, data in topic_performance.items():
            latest = data["tests"][0]
            retention = int(latest["success_rate"])
            days_ago = (datetime.now(timezone.utc) - datetime.fromisoformat(latest["test_date"].replace('Z', '+00:00'))).days
            
            if retention < 80 and days_ago >= 1:
                at_risk.append(TopicAtRisk(
                    topic_id=topic_id,
                    topic_name=data["topic_name"],
                    subject=data["subject_name"],
                    retention_rate=retention,
                    days_until_forgotten=max(1, 7 - days_ago),
                    last_studied=latest["test_date"],
                    difficulty_score=70,
                    priority_score=85
                ))
        
        at_risk.sort(key=lambda x: x.retention_rate)
        at_risk = at_risk[:3]
        
        # PRIORITY TOPICS (success rate düşük)
        priority = []
        for topic_id, data in topic_performance.items():
            avg_success = sum([t["success_rate"] for t in data["tests"][:3]]) / min(3, len(data["tests"]))
            
            if avg_success < 75:
                priority.append(PriorityTopic(
                    topic_id=topic_id,
                    topic_name=data["topic_name"],
                    subject=data["subject_name"],
                    priority_score=int(100 - avg_success),
                    priority_reason="difficulty" if avg_success < 60 else "retention",
                    difficulty_score=int(100 - avg_success),
                    retention_rate=int(avg_success),
                    estimated_study_time=45
                ))
        
        priority.sort(key=lambda x: x.priority_score, reverse=True)
        priority = priority[:3]
        
        # STREAK (günlük test girişi)
        today = get_user_date(x_user_timezone)
        streak_days = []
        check_date = today
        
        for _ in range(365):
            day_tests = [t for t in all_tests.data 
                        if datetime.fromisoformat(t["test_date"].replace('Z', '+00:00')).date() == check_date]
            if day_tests:
                streak_days.append(check_date)
                check_date -= timedelta(days=1)
            else:
                break
        
        current_streak = len(streak_days)
        
        return TodaysTasksResponseOld(
            success=True,
            data=TodaysTasksDataOld(
                at_risk_topics=at_risk,
                total_at_risk=len(at_risk),
                priority_topics=priority,
                total_priority=len(priority),
                streak=StudyStreak(
                    current_streak=current_streak,
                    longest_streak=12,
                    streak_status="active" if current_streak > 0 else "broken",
                    last_study_date=str(streak_days[0]) if streak_days else "",
                    next_milestone=7
                ),
                time_stats=TimeStats(
                    total_study_time_today=45,
                    total_study_time_week=380,
                    avg_daily_time=54,
                    target_daily_time=120,
                    time_efficiency=75
                ),
                generated_at=datetime.now(timezone.utc).isoformat(),
                student_id=student_id
            ),
            message="Gerçek veri"
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return get_mock_todays_tasks()


def get_mock_todays_tasks():
    """Fallback mock data"""
    return TodaysTasksResponseOld(
        success=True,
        data=TodaysTasksDataOld(
            at_risk_topics=[],
            total_at_risk=0,
            priority_topics=[],
            total_priority=0,
            streak=StudyStreak(current_streak=0, longest_streak=0, streak_status="broken", last_study_date="", next_milestone=7),
            time_stats=TimeStats(total_study_time_today=0, total_study_time_week=0, avg_daily_time=0, target_daily_time=120, time_efficiency=0),
            generated_at=datetime.now(timezone.utc).isoformat(),
            student_id="demo"
        ),
        message="Mock data (no tests)"
    )# ============================================
# 🎯 GÖREV TAMAMLAMA
# ============================================

@router.post("/student/tasks/{task_id}/complete")
async def complete_task(task_id: str, manual: bool = True):
    """
    Görevi tamamla
    manual=True → Öğrenci manuel tik attı
    manual=False → Test girişi sonrası otomatik
    """
    try:
        supabase = get_supabase_admin()
        
        # Görevi bul
        task = supabase.table("student_tasks").select("*").eq("id", task_id).execute()
        
        if not task.data:
            return {"success": False, "error": "Görev bulunamadı"}
        
        # Tamamla
        update_data = {
            "status": "completed",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "manual_completion": manual
        }
        
        result = supabase.table("student_tasks").update(update_data).eq("id", task_id).execute()
        
        return {
            "success": True,
            "task": result.data[0],
            "message": "Görev tamamlandı! 🎉"
        }
        
    except Exception as e:
        print(f"Task completion error: {str(e)}")
        return {"success": False, "error": str(e)}


@router.get("/student/tasks/today")
async def get_todays_tasks_list(student_id: str, x_user_timezone: str = Header("UTC")):
    """
    Bugünün görev listesi (5 görev)
    """
    try:
        today = get_user_date(x_user_timezone).isoformat()
        
        supabase = get_supabase_admin()
        
        # Bugünün görevlerini getir
        tasks = supabase.table("student_tasks").select("*").eq(
            "student_id", student_id
        ).eq(
            "task_date", today
        ).order("priority_level", desc=False).execute()
        
        # Eğer bugün için görev yoksa, oluştur
        if not tasks.data:
            # 4 Motor'dan görev oluştur (şimdilik mock)
            created_tasks = create_daily_tasks(student_id, today)
            tasks = supabase.table("student_tasks").select("*").eq(
                "student_id", student_id
            ).eq(
                "task_date", today
            ).execute()
        
        # Süre hesapla
        total_time = sum([t["estimated_time_minutes"] for t in tasks.data])
        completed_time = sum([t["estimated_time_minutes"] for t in tasks.data if t["status"] == "completed"])
          # Topic testlerini çek
        
        # AT RISK HESAPLAMA
        at_risk = []
        topic_tests = supabase.table("student_topic_tests").select(
            "*, topics(id, name_tr, subjects(name_tr))"
        ).eq("student_id", student_id).order("test_date", desc=True).execute()
        
        # Topic bazında grupla
        topic_performance = {}
        for test in topic_tests.data:
            if not test.get("topics"):
                continue
            topic_id = test["topics"]["id"]
            if topic_id not in topic_performance:
                topic_performance[topic_id] = {
                    "topic_name": test["topics"]["name_tr"],
                    "subject_name": test["topics"]["subjects"]["name_tr"] if test["topics"].get("subjects") else "Unknown",
                    "tests": []
                }
            topic_performance[topic_id]["tests"].append(test)
        
        # At risk konuları filtrele
        for topic_id, data in topic_performance.items():
            latest = data["tests"][0]
            retention = int(latest["success_rate"])
            days_ago = (datetime.now(timezone.utc) - datetime.fromisoformat(latest["test_date"].replace('Z', '+00:00'))).days
            
            if retention < 80 and days_ago >= 1:
                at_risk.append({
                    "topic_id": topic_id,
                    "topic_name": data["topic_name"],
                    "subject": data["subject_name"],
                    "retention_rate": retention,
                    "days_until_forgotten": max(1, 7 - days_ago),
                    "last_studied": latest["test_date"],
                    "difficulty_score": 70,
                    "priority_score": 85
                })
        
        at_risk.sort(key=lambda x: x["retention_rate"])
        at_risk = at_risk[:3]      
        return {
                    "success": True,
                    "tasks": tasks.data,
                    "summary": {
                        "total_tasks": len(tasks.data),
                        "completed_tasks": len([t for t in tasks.data if t["status"] == "completed"]),
                        "total_time_minutes": total_time,
                        "completed_time_minutes": completed_time,
                        "remaining_time_minutes": total_time - completed_time
                    },
                    "at_risk_topics": at_risk,
                    "total_at_risk": len(at_risk),
                    "date": today
                }
        
    except Exception as e:
        print(f"Todays tasks error: {str(e)}")
        return {"success": False, "error": str(e)}


def create_daily_tasks(student_id: str, date: str):
    """
    🎯 4 Motor'dan Günlük Görevler Oluştur (Gerçek Analiz)
    
    Her gün 5 görev:
    - BS-Model (Tekrar): 2 görev
    - Priority Engine: 1 görev
    - Difficulty Engine: 1 görev
    - Time Analyzer: 1 görev
    """
    supabase = get_supabase_admin()
    
    print(f"🚀 create_daily_tasks ÇAĞRILDI: student={student_id}, date={date}")
    # Öğrencinin tüm testlerini çek
    all_tests = supabase.table("student_topic_tests").select(
        "*, topics(id, name_tr, difficulty_level, subjects(id, name_tr))"
    ).eq("student_id", student_id).order("test_date", desc=True).execute()
    print(f"📊 Test sayısı: {len(all_tests.data) if all_tests.data else 0}")
    
    if not all_tests.data or len(all_tests.data) < 3:
        # Yeterli veri yok, mock görev döndür
    print(f"⚠️ FALLBACK kullanılıyor!")
        return create_fallback_tasks(student_id, date)
    
    # Topic bazında performans analizi
    topic_performance = {}
    now = datetime.now(timezone.utc)
    
    for test in all_tests.data:
        topic_id = test["topic_id"]
        
        if topic_id not in topic_performance:
            topic_performance[topic_id] = {
                "topic_id": topic_id,
                "topic_name": test["topics"]["name_tr"] if test.get("topics") else "Unknown",
                "subject_id": test["topics"]["subjects"]["id"] if test.get("topics") and test["topics"].get("subjects") else None,
                "subject_name": test["topics"]["subjects"]["name_tr"] if test.get("topics") and test["topics"].get("subjects") else "Unknown",
                "difficulty_level": test["topics"].get("difficulty_level", 3) if test.get("topics") else 3,
                "tests": []
            }
        
        topic_performance[topic_id]["tests"].append(test)
    
    # 1️⃣ BS-MODEL: Tekrar Zamanı Gelmiş Konular (2 görev)
    bs_candidates = []
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        latest_test = tests[0]
        test_date = datetime.fromisoformat(latest_test["test_date"].replace('Z', '+00:00'))
        days_since = (now - test_date).days
        
        remembering_rate = calculate_remembering_rate(tests)
        
        if remembering_rate < 70 and days_since >= 1:
            urgency = 100 - remembering_rate + (days_since * 5)
            bs_candidates.append({
                "topic_id": topic_id,
                "topic_name": data["topic_name"],
                "subject_id": data["subject_id"],
                "urgency_score": min(100, urgency),
                "remembering_rate": remembering_rate
            })
    
    bs_candidates.sort(key=lambda x: x["urgency_score"], reverse=True)
    bs_tasks = bs_candidates[:2]
    
    # 2️⃣ PRIORITY ENGINE: En Yüksek Öncelik (1 görev)
    priority_candidates = []
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        latest_test = tests[0]
        
        remembering_rate = calculate_remembering_rate(tests)
        forgetting_risk = 100 - remembering_rate
        
        priority_score = 0
        priority_score += forgetting_risk * 0.5
        priority_score += data["difficulty_level"] * 5
        
        if len(tests) < 3:
            priority_score += 20
        
        if latest_test["success_rate"] < 60:
            priority_score += 15
        
        priority_score = min(100, priority_score)
        
        # BS-Model'de zaten seçilenleri atla
        if topic_id not in [t["topic_id"] for t in bs_tasks]:
            priority_candidates.append({
                "topic_id": topic_id,
                "topic_name": data["topic_name"],
                "subject_id": data["subject_id"],
                "priority_score": int(priority_score)
            })
    
    priority_candidates.sort(key=lambda x: x["priority_score"], reverse=True)
    priority_task = priority_candidates[:1]
    
    # 3️⃣ DIFFICULTY ENGINE: En Zor Konu (1 görev)
    difficulty_candidates = []
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        avg_success = sum([t["success_rate"] for t in tests]) / len(tests)
        
        if avg_success < 70:
            # Zaten seçilenleri atla
            if topic_id not in [t["topic_id"] for t in bs_tasks] and \
               topic_id not in [t["topic_id"] for t in priority_task]:
                difficulty_candidates.append({
                    "topic_id": topic_id,
                    "topic_name": data["topic_name"],
                    "subject_id": data["subject_id"],
                    "avg_success": avg_success
                })
    
    difficulty_candidates.sort(key=lambda x: x["avg_success"])
    difficulty_task = difficulty_candidates[:1]
    
    # 4️⃣ TIME ANALYZER: 30+ Gün veya Yavaş (1 görev)
    time_candidates = []
    for topic_id, data in topic_performance.items():
        tests = data["tests"]
        latest_test = tests[0]
        test_date = datetime.fromisoformat(latest_test["test_date"].replace('Z', '+00:00'))
        days_since = (now - test_date).days
        
        if days_since > 30:
            # Zaten seçilenleri atla
            if topic_id not in [t["topic_id"] for t in bs_tasks] and \
               topic_id not in [t["topic_id"] for t in priority_task] and \
               topic_id not in [t["topic_id"] for t in difficulty_task]:
                time_candidates.append({
                    "topic_id": topic_id,
                    "topic_name": data["topic_name"],
                    "subject_id": data["subject_id"],
                    "days_since": days_since
                })
    
    time_candidates.sort(key=lambda x: x["days_since"], reverse=True)
    time_task = time_candidates[:1]
    
    # Görevleri oluştur
    tasks = []
    priority_level = 1
    
    # BS-Model görevleri (2 adet)
    for task_data in bs_tasks:
        tasks.append({
            "student_id": student_id,
            "task_date": date,
            "task_type": "test",
            "subject_id": task_data["subject_id"],
            "topic_id": task_data["topic_id"],
            "topic_name": task_data["topic_name"],
            "source_motor": "bs_model",
            "priority_level": priority_level,
            "estimated_time_minutes": 20,
            "question_count": 12,
            "status": "pending"
        })
        priority_level += 1
    
    # Priority görev (1 adet)
    if priority_task:
        task_data = priority_task[0]
        tasks.append({
            "student_id": student_id,
            "task_date": date,
            "task_type": "test",
            "subject_id": task_data["subject_id"],
            "topic_id": task_data["topic_id"],
            "topic_name": task_data["topic_name"],
            "source_motor": "priority",
            "priority_level": priority_level,
            "estimated_time_minutes": 20,
            "question_count": 12,
            "status": "pending"
        })
        priority_level += 1
    
    # Difficulty görev (1 adet)
    if difficulty_task:
        task_data = difficulty_task[0]
        tasks.append({
            "student_id": student_id,
            "task_date": date,
            "task_type": "study",
            "subject_id": task_data["subject_id"],
            "topic_id": task_data["topic_id"],
            "topic_name": task_data["topic_name"],
            "source_motor": "difficulty",
            "priority_level": priority_level,
            "estimated_time_minutes": 30,
            "status": "pending"
        })
        priority_level += 1
    
    # Time görev (1 adet)
    if time_task:
        task_data = time_task[0]
        tasks.append({
            "student_id": student_id,
            "task_date": date,
            "task_type": "study",
            "subject_id": task_data["subject_id"],
            "topic_id": task_data["topic_id"],
            "topic_name": task_data["topic_name"],
            "source_motor": "time",
            "priority_level": priority_level,
            "estimated_time_minutes": 25,
            "status": "pending"
        })
    
    # 5'ten az görev varsa fallback kullan
    if len(tasks) < 5:
        return create_fallback_tasks(student_id, date)
    
    # Database'e kaydet
    for task in tasks:
        supabase.table("student_tasks").insert(task).execute()
    
    return tasks


def create_fallback_tasks(student_id: str, date: str):
    """
    Yeterli veri yoksa fallback görevler (eski mock mantık)
    """
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
            "source_motor": "fallback",
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
            "source_motor": "fallback",
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
            "source_motor": "fallback",
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
            "source_motor": "fallback",
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
            "source_motor": "fallback",
            "priority_level": 5,
            "estimated_time_minutes": 15,
            "question_count": 12,
            "status": "pending"
        }
    ]
    
    for task in tasks:
        supabase.table("student_tasks").insert(task).execute()
    
    return tasks

@router.delete("/student/tasks/cleanup")
async def cleanup_tasks(student_id: str, date: str):
    """Belirli bir günün tüm görevlerini sil"""
    try:
        supabase = get_supabase_admin()
        
        result = supabase.table("student_tasks").delete().eq(
            "student_id", student_id
        ).eq("task_date", date).execute()
        
        return {
            "success": True,
            "message": f"{date} tarihli görevler silindi",
            "deleted_count": len(result.data) if result.data else 0
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/student/tasks/{task_id}/uncomplete")
async def uncomplete_task(task_id: str):
    """
    Görevi geri al (sadece manuel tamamlamalar için)
    """
    try:
        supabase = get_supabase_admin()
        
        # Görevi kontrol et
        task = supabase.table("student_tasks").select("*").eq("id", task_id).execute()
        
        if not task.data:
            return {"success": False, "error": "Görev bulunamadı"}
        
        task_data = task.data[0]
        
        # Sadece manuel tamamlamalara izin ver
        if not task_data.get("manual_completion", False):
            return {
                "success": False,
                "error": "Bu görev otomatik tamamlanmış, geri alınamaz!"
            }
        
        # Geri al
        update_data = {
            "status": "pending",
            "completed_at": None,
            "manual_completion": False
        }
        
        result = supabase.table("student_tasks").update(update_data).eq("id", task_id).execute()
        
        return {
            "success": True,
            "task": result.data[0],
            "message": "Görev geri alındı"
        }
        
    except Exception as e:
        print(f"Task uncomplete error: {str(e)}")
        return {"success": False, "error": str(e)}


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
