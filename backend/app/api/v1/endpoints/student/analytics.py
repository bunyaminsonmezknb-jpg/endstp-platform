"""
Student Analytics Endpoints
- Projection (ilerleme tahmini)
- Goal (hedef belirleme)
- Analyze (4 Motor: BS-Model, Priority, Difficulty, Time)
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from app.core.motor_wrapper import MotorWrapper
from app.core.motor_registry import MotorType, SubscriptionTier
from app.db.session import get_supabase_admin
from app.core.auth import get_current_user  # ← EKLE
from pydantic import BaseModel
from .utils import calculate_remembering_rate, format_turkish_date, calculate_next_review_date, EXAM_DATE

router = APIRouter()

@router.post("/projection")
async def get_student_projection(current_user: dict = Depends(get_current_user)):
    """
    Öğrenci ilerleme projeksiyonu
    """
    student_id = current_user["id"]
    
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
@router.post("/goal")
async def set_student_goal(current_user: dict = Depends(get_current_user)):
    """
    Üniversite hedefi ilerlemesi (MVP - 12. sınıf için)
    """
    student_id = current_user["id"]
    
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

@router.post("/analyze")
async def analyze_student_performance(current_user: dict = Depends(get_current_user)):
    """
    4 Motor Analizi
    BS-Model, Difficulty Engine, Time Analyzer, Priority Engine
    """
    student_id = current_user["id"]
    
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
        
        # ✅ YENİ: MotorWrapper ile dene (tier-based v1/v2)
        try:
            wrapper = MotorWrapper()
            user_tier = current_user.get("tier", "free")
            motor_result = wrapper.calculate_difficulty(
                motor_type="difficulty",
                user_tier=user_tier,
                topic_id=topic_id,
                user_id=student_id
            )
            difficulty_score = motor_result["difficulty_percentage"]
        except:
            # ✅ ESKİ: Manuel hesaplama (fallback)
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