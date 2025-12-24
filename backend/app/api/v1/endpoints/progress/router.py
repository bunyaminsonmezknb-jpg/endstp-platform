"""
Progress & Goals Router - Main Endpoints
⭐ MODULAR VERSION with Exam Weight Integration
⭐ UTC-AWARE with Period Key Fix (2024-12-24)
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime, timedelta
from collections import defaultdict

from app.core.auth import get_current_user
from app.db.session import get_supabase_admin

# Local imports
from .models import ProgressProjection, SubjectProgress, TrendData
from .helpers import (
    to_utc_date,
    get_week_start_utc,
    get_month_start_utc,
    generate_week_periods,
    generate_month_periods
)
from .calculators import (
    calculate_topic_mastery_level,
    calculate_phase_and_progress,
    calculate_mastery_counts,
    calculate_trends  # ⭐ YENİ - Trend hesaplama
)
from .exam_weight import (
    calculate_exam_weight_multiplier,
    calculate_priority_score
)

router = APIRouter(
    prefix="/student/progress",  # ⭐ OLMALI!
    tags=["progress"]
)

# ==================== ENDPOINT 1: PROJECTION ====================

@router.get("/projection")
async def get_progress_projection(
    current_user: dict = Depends(get_current_user),
    supabase = Depends(get_supabase_admin)
):
    """
    Genel ilerleme tahmini
    """
    try:
        student_id = current_user.get("id")
        
        # Tüm testleri al
        tests_result = supabase.table("student_topic_tests").select(
            "id, subject_id, topic_id, success_rate, test_date, created_at"
        ).eq("student_id", student_id).order("test_date").execute()
        
        tests = tests_result.data or []

        if not tests:
            return {
                "success": True,
                "data": {
                    "overall_progress": 0.0,
                    "estimated_completion_date": "Belirsiz",
                    "days_remaining": 999,
                    "weekly_improvement": 0.0,
                    "topics_mastered": 0,
                    "topics_in_progress": 0,
                    "topics_not_started": 0
                }
            }
        
        # Konu bazında grupla
        topics_dict = defaultdict(list)
        for test in tests:
            topics_dict[test['topic_id']].append(test)
        
        # Mastery hesapla
        topics_mastered = 0
        topics_in_progress = 0
        
        for topic_id, topic_tests in topics_dict.items():
            mastery = calculate_topic_mastery_level(topic_tests)
            if mastery == "mastered":
                topics_mastered += 1
            elif mastery == "in_progress":
                topics_in_progress += 1
        
        # Toplam konu sayısı
        total_topics_result = supabase.table("topics").select("id", count="exact").eq("is_active", True).execute()
        total_topics = total_topics_result.count or 150
        
        topics_not_started = max(0, total_topics - topics_mastered - topics_in_progress)
        
        # Overall progress
        overall_progress = (topics_mastered / total_topics * 100) if total_topics > 0 else 0
        
        # Haftalık gelişme (son 4 hafta) - UTC-AWARE ⭐
        now = datetime.utcnow()
        four_weeks_ago = now - timedelta(weeks=4)
        
        recent_tests = []
        for t in tests:
            test_dt = to_utc_date(t['test_date'])
            test_datetime = datetime.combine(test_dt, datetime.min.time())
            if test_datetime > four_weeks_ago:
                recent_tests.append(t)
        
        weekly_improvement = 0.0
        if len(recent_tests) >= 5:
            sorted_recent = sorted(recent_tests, key=lambda x: x['test_date'])
            first_week_avg = sum(t['success_rate'] for t in sorted_recent[:5]) / 5
            last_week_avg = sum(t['success_rate'] for t in sorted_recent[-5:]) / 5
            weekly_improvement = (last_week_avg - first_week_avg) / 4
        
        # Tahmini bitiriş
        if weekly_improvement > 0:
            remaining_progress = 100 - overall_progress
            weeks_needed = remaining_progress / weekly_improvement
            days_remaining = int(weeks_needed * 7)
            completion_date = (now + timedelta(days=days_remaining)).strftime("%Y-%m-%d")
        else:
            days_remaining = 999
            completion_date = "Belirsiz"
        
        return {
            "success": True,
            "data": {
                "overall_progress": round(overall_progress, 1),
                "estimated_completion_date": completion_date,
                "days_remaining": days_remaining,
                "weekly_improvement": round(weekly_improvement, 2),
                "topics_mastered": topics_mastered,
                "topics_in_progress": topics_in_progress,
                "topics_not_started": topics_not_started
            }
        }
    
    except Exception as e:
        print(f"❌ Projection error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINT 2: SUBJECTS (WITH EXAM WEIGHT) ⭐ ====================

@router.get("/subjects")
async def get_subject_progress(
    current_user: dict = Depends(get_current_user),
    supabase = Depends(get_supabase_admin)
):
    """
    Ders bazlı ilerleme (KADEMELI MODEL + EXAM WEIGHT + UNIQUE TOPICS)
    ⭐ Priority score with exam weight multiplier
    ⭐ Unique topics tested tracking
    """
    try:
        student_id = current_user.get("id")
        
        # Tüm active subjects
        subjects_result = supabase.table("subjects").select(
            "id, code, name_tr"
        ).eq("is_active", True).execute()
        
        subjects = subjects_result.data or []
        
        if not subjects:
            return {"success": True, "data": []}
        
        # Tüm testleri al
        tests_result = supabase.table("student_topic_tests").select(
            "id, subject_id, topic_id, success_rate, test_date, created_at"
        ).eq("student_id", student_id).execute()
        
        all_tests = tests_result.data or []
        
        # Subject bazında grupla
        subject_tests = defaultdict(list)
        for test in all_tests:
            subject_tests[test['subject_id']].append(test)
        
        subject_progress = []
        
        for subject in subjects:
            subject_id = subject['id']
            tests = subject_tests.get(subject_id, [])
            
            # Bu dersin konularını al
            topics_result = supabase.table("topics").select(
                "id"
            ).eq("subject_id", subject_id).eq("is_active", True).execute()
            
            topics = topics_result.data or []
            topics_total = len(topics)
            
            if topics_total == 0:
                continue
            
            test_count = len(tests)
            
            # ==================== UNIQUE TOPICS TESTED ⭐ ====================
            unique_topics_tested = len(set(test['topic_id'] for test in tests)) if tests else 0
            
            # ==================== PHASE CALCULATION ====================
            (
                progress_percentage,
                avg_success_rate,
                trend,
                trend_icon,
                phase,
                disclaimer
            ) = calculate_phase_and_progress(tests, topics_total)
            
            # ==================== 0 TEST DURUMU (HİBRİT MODEL) ⭐ ====================
            if test_count == 0:
                trend = "unknown"
                phase = "BAŞLANMAMIŞ"
                disclaimer = f"Bu derste henüz yeterli veri yok. İlk testini çözerek analizi aktif hale getirebilirsin. ({topics_total} konu mevcut)"
            
            # ==================== PHASE DISCLAIMER GÜNCELLEMESİ ⭐ ====================
            # Disclaimer'ı unique_topics_tested ile güncelle (sadece test_count > 0 için)
            elif test_count < 5:
                phase = "PHASE 1: Keşif"
                disclaimer = f"📊 {test_count} test ve {unique_topics_tested} farklı konu ile başlangıç aşamasındasınız. Daha fazla konu çalışarak kapsam artırın!"
            elif test_count < 15:
                phase = "PHASE 2: Gelişim"
                disclaimer = f"📈 {test_count} test ve {unique_topics_tested}/{topics_total} konu kapsamı ile gelişim sürecinde. Kapsam artışı önemli!"
            else:
                phase = "PHASE 3: Olgunluk"
                disclaimer = f"🎯 {test_count} test ve {unique_topics_tested}/{topics_total} konu ile olgun aşamasındasınız. Unutma eğrisi takibi aktif."            
            # ==================== MASTERY COUNTS ====================
            (
                topics_mastered_universal,
                topics_mastered_personal,
                topics_in_progress,
                topics_not_started
            ) = calculate_mastery_counts(tests, [t['id'] for t in topics])
            
            # ==================== EXAM WEIGHT MULTIPLIER ⭐ ====================
            exam_multiplier = 1.0
            total_exam_questions = 0
            
            try:
                exam_weight_result = supabase.table("subject_exam_weights").select(
                    "question_count"
                ).eq("subject_id", subject_id).execute()
                
                exam_multiplier, total_exam_questions = calculate_exam_weight_multiplier(
                    exam_weight_result.data or []
                )
            except Exception as e:
                # ⚠️ Tablo yoksa default değer kullan
                print(f"⚠️ Exam weight fallback: {subject['code']}")
            
            # Priority score hesapla
            priority_score = calculate_priority_score(
                progress_percentage,
                avg_success_rate,
                exam_multiplier
            )
            
            # ==================== LAST TEST DATE ====================
            last_test_date = None
            if tests:
                # En son test tarihini bul
                sorted_tests = sorted(tests, key=lambda x: x.get('test_date', ''), reverse=True)
                last_test_date = sorted_tests[0].get('test_date')
            
            subject_progress.append({
                "subject_id": subject_id,
                "subject_name": subject['name_tr'],
                "subject_code": subject['code'],
                "progress_percentage": progress_percentage,
                "topics_total": topics_total,
                "topics_mastered": topics_mastered_universal,
                "topics_mastered_personal": topics_mastered_personal,
                "topics_in_progress": topics_in_progress,
                "topics_not_started": topics_not_started,
                "unique_topics_tested": unique_topics_tested,  # ⭐ YENİ
                "avg_success_rate": avg_success_rate,
                "trend": trend,
                "trend_icon": trend_icon,
                "test_count": test_count,
                "phase": phase,
                "disclaimer": disclaimer,
                "exam_weight_multiplier": round(exam_multiplier, 2),
                "total_exam_questions": total_exam_questions,
                "priority_score": priority_score,
                "last_test_date": last_test_date  # ⭐ YENİ
            })
        
        # ⭐ Priority score'a göre sırala (en yüksek önce)
        subject_progress.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return {
            "success": True,
            "data": subject_progress
        }
    
    except Exception as e:
        print(f"❌ Subject progress error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINT 3: TRENDS (UTC-AWARE FIX) ⭐⭐⭐ ====================

@router.get("/trends")
async def get_progress_trends(
    period: str = Query("weekly", regex="^(weekly|monthly)$"),
    num_periods: int = Query(8, ge=2, le=24),
    current_user: dict = Depends(get_current_user),
    supabase = Depends(get_supabase_admin)
):
    """
    Haftalık/aylık trend grafiği
    ⭐ UTC-AWARE - Period key mismatch fix
    ⭐ calculators.calculate_trends() kullanıyor
    """
    try:
        student_id = current_user.get("id")
        
        # ===============================
        # 1) Öğrencinin tüm testlerini çek
        # ===============================
        tests_result = supabase.table("student_topic_tests").select(
            "id, test_date, subject_id, topic_id, success_rate"
        ).eq("student_id", student_id).order("test_date").execute()
        
        tests = tests_result.data or []
        
        # ===============================
        # 2) Ders isimlerini çek (tek sorgu)
        # ===============================
        subjects_result = supabase.table("subjects").select(
            "id, name_tr"
        ).execute()
        
        subjects_map = {
            s["id"]: s["name_tr"]
            for s in (subjects_result.data or [])
        }
        
        # ===============================
        # 3) Trend Hesapla (calculators.py kullanıyor)
        # ===============================
        data = calculate_trends(
            tests=tests,
            period=period,
            num_periods=num_periods,
            subjects=subjects_map
        )
        
        # ===============================
        # 4) DEBUG OUTPUT (isteğe bağlı)
        # ===============================
        print(f"\n📊 TREND DEBUG:")
        print(f"Period: {period}")
        print(f"Total tests: {data['count']}")
        print(f"Period starts: {data['period_starts'][:3]}...")
        print(f"Overall trend: {data['overall_trend'][:3]}...")
        print(f"Subjects: {len(data['subjects'])}")
        
        # ===============================
        # 5) Response Format (Chart.js uyumlu)
        # ===============================
        return {
            "success": True,
            "data": {
                "labels": data["labels"],
                "datasets": [
                    {
                        "label": s["label"],
                        "data": s["data"],
                        "subject_id": s["subject_id"]
                    }
                    for s in data["subjects"]
                ],
                "overall_trend": data["overall_trend"],
                "period": data["period"]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Trends error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Trend calculation failed: {e}")

# ==================== ENDPOINT 4: PREDICTION ====================

@router.get("/prediction")
async def get_forgetting_prediction(
    period: str = "weekly",
    current_user: dict = Depends(get_current_user),
    supabase = Depends(get_supabase_admin)
):
    """
    Unutma eğrisi tahmini (gelecek 4 hafta/ay)
    """
    try:
        student_id = current_user.get("id")
        
        tests_result = supabase.table("student_topic_tests").select(
            "subject_id, success_rate, test_date"
        ).eq("student_id", student_id).order("test_date", desc=True).execute()
        
        tests = tests_result.data or []
        
        if not tests:
            return {
                "success": True,
                "data": {
                    "predictions": {},
                    "steepest_decline": None
                }
            }
        
        subject_data = defaultdict(list)
        for test in tests:
            subject_data[test['subject_id']].append({
                'success_rate': test['success_rate'],
                'test_date': test['test_date']
            })
        
        predictions = {}
        steepest_decline = {"subject_id": None, "decline_rate": 0}
        
        for subject_id, subject_tests in subject_data.items():
            last_success = subject_tests[0]['success_rate']
            
            # UTC-AWARE tarih parse ⭐
            last_date_obj = to_utc_date(subject_tests[0]['test_date'])
            last_date = datetime.combine(last_date_obj, datetime.min.time())
            
            if len(subject_tests) >= 2:
                recent_avg = sum(t['success_rate'] for t in subject_tests[:3]) / min(3, len(subject_tests))
                older_avg = sum(t['success_rate'] for t in subject_tests[3:6]) / max(1, min(3, len(subject_tests[3:6])))
                decay_rate = max(0.02, (recent_avg - older_avg) / 100) if recent_avg < older_avg else 0.05
            else:
                decay_rate = 0.05
            
            future_predictions = []
            current_prediction = last_success
            
            for i in range(1, 5):
                current_prediction = max(0, current_prediction - (last_success * decay_rate))
                future_predictions.append(round(current_prediction, 1))
            
            predictions[subject_id] = {
                "current": last_success,
                "future": future_predictions,
                "decay_rate": round(decay_rate * 100, 1),
                "last_test_date": last_date.strftime('%Y-%m-%d')
            }
            
            total_decline = last_success - future_predictions[-1]
            if total_decline > steepest_decline["decline_rate"]:
                steepest_decline = {
                    "subject_id": subject_id,
                    "decline_rate": round(total_decline, 1)
                }
        
        if steepest_decline["subject_id"]:
            subject_result = supabase.table("subjects").select("name_tr").eq(
                "id", steepest_decline["subject_id"]
            ).execute()
            if subject_result.data:
                steepest_decline["subject_name"] = subject_result.data[0]['name_tr']
        
        return {
            "success": True,
            "data": {
                "predictions": predictions,
                "steepest_decline": steepest_decline if steepest_decline["subject_id"] else None
            }
        }
    
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ==================== HEALTH CHECK ====================

@router.get("/health")
async def progress_health():
    """Health check"""
    return {
        "status": "healthy",
        "endpoints": 4,
        "features": ["projection", "subjects", "trends", "prediction"],
        "data_source": "student_topic_tests",
        "exam_weight_enabled": True,
        "modular_structure": True,
        "utc_aware": True,  # ⭐ YENİ
        "period_key_fix": "2024-12-24"  # ⭐ YENİ
    }