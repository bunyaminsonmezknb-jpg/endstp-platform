"""
Student Helper Functions
- calculate_remembering_rate
- get_user_date
- format_turkish_date
- calculate_next_review_date
"""
from datetime import datetime, timezone, timedelta
from typing import List

# Türkçe aylar
TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}

# Sınav tarihi
EXAM_DATE = datetime(2026, 6, 15, tzinfo=timezone.utc)

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
    """Optimal tekrar tarihini hesapla + gecikme kontrolü"""
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
    
    now = datetime.now(timezone.utc)
    next_date = last_test_date + timedelta(days=interval_days)
    
    # Gerçek gün farkı (negatif olabilir)
    actual_days = (next_date - now).days
    
    # Gecikme hesabı
    if actual_days < 0:
        overdue_days = abs(actual_days)
        days_remaining = 0
        status = "overdue"  # Gecikmiş
    else:
        overdue_days = 0
        days_remaining = actual_days
        status = "upcoming"  # Yaklaşan
    
    return {
        "date": next_date,
        "days_remaining": days_remaining,
        "overdue_days": overdue_days,  # ✅ YENİ
        "status": status,  # ✅ YENİ
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


