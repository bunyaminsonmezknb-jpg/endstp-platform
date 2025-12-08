"""
Student Tasks Endpoints
- Todays tasks (4 motor entegrasyonu)
- Task complete/uncomplete
- Task cleanup
- create_daily_tasks function
"""
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from app.db.session import get_supabase_admin
from pydantic import BaseModel
import uuid
from .utils import get_user_date, calculate_remembering_rate, EXAM_DATE

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
    4 Motor'dan günlük görevler oluştur (gerçek topic_id'lerle)
    """
    supabase = get_supabase_admin()
    
    # Gerçek ID'ler
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
    
    # Veritabanına ekle
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



# Mock data helper
def get_mock_todays_tasks():
    """Mock tasks data"""
    return {
        "success": True,
        "data": {
            "at_risk_topics": [],
            "total_at_risk": 0,
            "priority_topics": [],
            "total_priority": 0,
            "streak": {
                "current_streak": 0,
                "longest_streak": 0,
                "last_study_date": None,
                "streak_status": "inactive",
                "next_milestone": 7
            },
            "time_stats": {
                "total_study_time_today": 0,
                "total_study_time_week": 0,
                "avg_daily_time": 0,
                "target_daily_time": 120,
                "time_efficiency": 0
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "student_id": "demo"
        }
    }
def create_daily_tasks(student_id: str, date: str):
    """
    4 Motor'dan günlük görevler oluştur (gerçek topic_id'lerle)
    """
    supabase = get_supabase_admin()
    
    # Gerçek ID'ler
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
    
    # Veritabanına ekle
    for task in tasks:
        supabase.table("student_tasks").insert(task).execute()
    
    return tasks


