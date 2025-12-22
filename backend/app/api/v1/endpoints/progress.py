"""
Progress & Goals Endpoints
Gerçek test verilerinden hesaplama yapar
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, date, timedelta
from collections import defaultdict

from app.core.auth import get_current_user
from app.db.session import get_supabase_admin

router = APIRouter()

# ==================== RESPONSE MODELS ====================

from pydantic import BaseModel

class ProgressProjection(BaseModel):
    overall_progress: float
    estimated_completion_date: str
    days_remaining: int
    weekly_improvement: float
    topics_mastered: int
    topics_in_progress: int
    topics_not_started: int

class SubjectProgress(BaseModel):
    subject_id: str
    subject_name: str
    subject_code: str
    progress_percentage: float
    topics_total: int
    topics_mastered: int
    topics_in_progress: int
    topics_not_started: int
    avg_success_rate: float
    trend: str

class TrendDataset(BaseModel):
    label: str
    data: List[Optional[float]]
    subject_id: str

class TrendData(BaseModel):
    labels: List[str]
    datasets: List[TrendDataset]
    overall_trend: List[Optional[float]]
    period: str

# ==================== HELPER FUNCTIONS ====================

def calculate_topic_mastery_level(tests: List[dict]) -> str:
    """
    Konu başarı seviyesi belirle (GEVŞEK KRİTERLER)
    - mastered: Ortalama >=80% ve 2+ test VEYA >=70% ve 3+ test
    - in_progress: En az 1 test var
    - not_started: Test yok
    """
    if not tests:
        return "not_started"
    
    avg_success = sum(t.get('success_rate', 0) for t in tests) / len(tests)
    test_count = len(tests)
    
    # Mastered: Yüksek başarı + az test VEYA iyi başarı + çok test
    if (avg_success >= 80 and test_count >= 2) or (avg_success >= 70 and test_count >= 3):
        return "mastered"
    else:
        return "in_progress"

def calculate_trend(recent_tests: List[dict]) -> str:
    """
    Son testlere göre trend hesapla
    """
    if len(recent_tests) < 2:
        return "stable"
    
    # Son 5 testi al
    last_5 = sorted(recent_tests, key=lambda x: x['test_date'])[-5:]
    
    if len(last_5) < 2:
        return "stable"
    
    # İlk yarı vs ikinci yarı karşılaştır
    mid = len(last_5) // 2
    first_half_avg = sum(t['success_rate'] for t in last_5[:mid]) / mid
    second_half_avg = sum(t['success_rate'] for t in last_5[mid:]) / (len(last_5) - mid)
    
    diff = second_half_avg - first_half_avg
    
    if diff > 5:
        return "improving"
    elif diff < -5:
        return "declining"
    else:
        return "stable"

def get_week_start(test_date: str) -> str:
    """Haftanın başlangıç tarihini döndür (Pazartesi)"""
    dt = datetime.fromisoformat(test_date.replace('Z', '+00:00'))
    days_since_monday = dt.weekday()
    monday = dt - timedelta(days=days_since_monday)
    return monday.strftime('%Y-%m-%d')

def get_month_start(test_date: str) -> str:
    """Ayın başlangıç tarihini döndür"""
    dt = datetime.fromisoformat(test_date.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-01')

# ==================== ENDPOINTS ====================

@router.get("/student/progress/projection")
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
            "id, topic_id, success_rate, test_date, created_at"
        ).eq("student_id", student_id).execute()
        
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
        
        # Haftalık gelişme (son 4 hafta)
        now = datetime.now()
        four_weeks_ago = now - timedelta(weeks=4)
        
        recent_tests = [
            t for t in tests 
            if datetime.fromisoformat(t['test_date'].replace('Z', '+00:00')) > four_weeks_ago
        ]
        
        weekly_improvement = 0.0
        if len(recent_tests) >= 5:
            sorted_recent = sorted(recent_tests, key=lambda x: x['test_date'])
            first_week_avg = sum(t['success_rate'] for t in sorted_recent[:5]) / 5
            last_week_avg = sum(t['success_rate'] for t in sorted_recent[-5:]) / 5
            weekly_improvement = (last_week_avg - first_week_avg) / 4  # 4 hafta
        
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
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/student/progress/subjects")
async def get_subject_progress(
    current_user: dict = Depends(get_current_user),
    supabase = Depends(get_supabase_admin)
):
    """
    Ders bazlı ilerleme (KADEMELI MODEL - PHASE 1)
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
            
# ==================== PHASE 1-2-3: KADEMELI MODEL ====================
            if test_count == 0:
                progress_percentage = 0.0
                avg_success_rate = 0.0
                trend = "stable"
                trend_icon = "→"
                phase = "no_data"
                disclaimer = "Henüz test girilmedi"
                
            elif test_count < 5:
                # ==================== PHASE 1: Sadece Başarı ====================
                avg_success_rate = sum(t['success_rate'] for t in tests) / test_count
                progress_percentage = avg_success_rate
                phase = "early"
                disclaimer = "İlerleme test başarına göre hesaplanıyor"
                
                # Adaptif Momentum (3+ test varsa)
                if test_count >= 3:
                    sorted_tests = sorted(tests, key=lambda x: x['test_date'])
                    window = min(5, len(tests) // 2)

                    if len(tests) >= 2 * window:
                        recent_avg = sum(t['success_rate'] for t in sorted_tests[-window:]) / window
                        previous_avg = sum(t['success_rate'] for t in sorted_tests[-2*window:-window]) / window
                        momentum = recent_avg - previous_avg
                    else:
                        # Yeterli veri yok, trend hesaplanmaz
                        recent_avg = avg_success_rate
                        previous_avg = avg_success_rate
                        momentum = 0
                    
                    # Test sayısına göre hassasiyet (tau)
                    tau = 0.08  # Başlangıç - geniş tolerans
                    
                    # Adaptif eşikler (kalan gelişim alanına göre)
                    improving_threshold = (100 - previous_avg) * tau
                    declining_threshold = previous_avg * tau
                    
                    if momentum > improving_threshold:
                        trend = "improving"
                        trend_icon = "🔥"
                    elif momentum < -declining_threshold:
                        trend = "declining"
                        trend_icon = "⚠️"
                    else:
                        trend = "stable"
                        trend_icon = "→"
                else:
                    trend = "stable"
                    trend_icon = "→"
                    
            else:
                # ==================== PHASE 2-3: Coverage + Ustalık ====================
                avg_success_rate = sum(t['success_rate'] for t in tests) / test_count
                
                # Test edilen konu sayısı
                tested_topics = len(set(t['topic_id'] for t in tests))
                topic_coverage = (tested_topics / topics_total) * 100 if topics_total > 0 else 0
                
                if test_count < 15:
                    # ==================== PHASE 2: Coverage Eklenir (5-15 test) ====================
                    # Dinamik ağırlık
                    coverage_weight = min(0.3, test_count / 50)
                    success_weight = 1 - coverage_weight
                    
                    progress_percentage = (
                        (topic_coverage * coverage_weight) +
                        (avg_success_rate * success_weight)
                    )
                    
                    phase = "growing"
                    disclaimer = f"İlerleme başarı (%{int(success_weight*100)}) + kapsam (%{int(coverage_weight*100)}) göre hesaplanıyor"
                    
                else:
                    # ==================== PHASE 3: Full Model (15+ test) ====================
                    # Ustalık oranını hesapla
                    topic_tests_dict_full = defaultdict(list)
                    for test in tests:
                        topic_tests_dict_full[test['topic_id']].append(test)
                    
                    mastered_count = 0
                    for topic_id, topic_tests in topic_tests_dict_full.items():
                        topic_avg = sum(t['success_rate'] for t in topic_tests) / len(topic_tests)
                        topic_count = len(topic_tests)
                        
                        # Evrensel ustalık
                        if topic_avg >= 80 and topic_count >= 2:
                            mastered_count += 1
                    
                    mastery_ratio = (mastered_count / tested_topics * 100) if tested_topics > 0 else 0
                    
                    # Full model weights
                    progress_percentage = (
                        (topic_coverage * 0.4) +
                        (avg_success_rate * 0.4) +
                        (mastery_ratio * 0.2)
                    )
                    
                    phase = "mature"
                    disclaimer = "İlerleme başarı (%40) + kapsam (%40) + ustalık (%20) göre hesaplanıyor"
                
                # ==================== Adaptif Momentum (5+ test) ====================
                sorted_tests = sorted(tests, key=lambda x: x['test_date'])
                window = min(5, len(tests) // 2)
                
                if len(tests) >= 2 * window:
                    recent_avg = sum(t['success_rate'] for t in sorted_tests[-window:]) / window
                    previous_avg = sum(t['success_rate'] for t in sorted_tests[-2*window:-window]) / window
                else:
                    recent_avg = avg_success_rate
                    previous_avg = avg_success_rate
                
                momentum = recent_avg - previous_avg
                
                # Test sayısına göre hassasiyet (tau)
                if test_count < 15:
                    tau = 0.05  # Gelişim - orta hassasiyet
                else:
                    tau = 0.03  # Olgunluk - ince ayar
                
                # Adaptif eşikler
                improving_threshold = (100 - previous_avg) * tau
                declining_threshold = previous_avg * tau
                
                if momentum > improving_threshold:
                    trend = "improving"
                    trend_icon = "🔥"
                elif momentum < -declining_threshold:
                    trend = "declining"
                    trend_icon = "⚠️"
                else:
                    trend = "stable"
                    trend_icon = "→"
            
            # ==================== İKİLİ USTALIK ====================
            # Konu bazında mastery hesapla
            topic_tests_dict = defaultdict(list)
            for test in tests:
                topic_tests_dict[test['topic_id']].append(test)
            
            # Evrensel ustalık (hard rule)
            topics_mastered_universal = 0
            # Kişisel güçlü (soft rule)
            topics_mastered_personal = 0
            topics_in_progress = 0
            
            # Basit personal average (PRL ilk hali)
            personal_avg = avg_success_rate if test_count > 0 else 0
            
            for topic_id in [t['id'] for t in topics]:
                topic_tests = topic_tests_dict.get(topic_id, [])
                
                if not topic_tests:
                    continue
                
                topic_avg = sum(t['success_rate'] for t in topic_tests) / len(topic_tests)
                topic_count = len(topic_tests)
                
                # Evrensel ustalık
                if topic_avg >= 80 and topic_count >= 2:
                    topics_mastered_universal += 1
                
                # Kişisel güçlü
                if topic_avg > personal_avg and topic_count >= 1:
                    topics_mastered_personal += 1
                
                # In progress
                if topic_count > 0:
                    topics_in_progress += 1
            
            topics_not_started = topics_total - topics_in_progress
            
            subject_progress.append({
                "subject_id": subject_id,
                "subject_name": subject['name_tr'],
                "subject_code": subject['code'],
                "progress_percentage": round(progress_percentage, 1),
                "topics_total": topics_total,
                "topics_mastered": topics_mastered_universal,  # 🏆 Evrensel
                "topics_mastered_personal": topics_mastered_personal,  # 🧠 Kişisel
                "topics_in_progress": topics_in_progress,
                "topics_not_started": topics_not_started,
                "avg_success_rate": round(avg_success_rate, 1),
                "trend": trend,
                "trend_icon": trend_icon,
                "test_count": test_count,
                "phase": phase,
                "disclaimer": disclaimer
            })
        
        return {
            "success": True,
            "data": subject_progress
        }
    
    except Exception as e:
        print(f"❌ Subject progress error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/student/progress/trends")
async def get_progress_trends(
    period: str = "weekly",
    current_user: dict = Depends(get_current_user),
    supabase = Depends(get_supabase_admin)
):
    """
    Haftalık/aylık trend grafiği (GELİŞTİRİLMİŞ LABEL'LAR)
    """
    try:
        student_id = current_user.get("id")
        
        # Tüm testleri al
        tests_result = supabase.table("student_topic_tests").select(
            "id, subject_id, success_rate, test_date, created_at"
        ).eq("student_id", student_id).execute()
        
        tests = tests_result.data or []
        
        if not tests:
            # Boş data
            if period == "weekly":
                labels = ["7 hafta önce", "6 hafta önce", "5 hafta önce", 
                         "4 hafta önce", "3 hafta önce", "2 hafta önce", "Geçen hafta", "Bu hafta"]
            else:
                labels = ["6 ay önce", "5 ay önce", "4 ay önce", "3 ay önce", "2 ay önce", "Geçen ay", "Bu ay"]
            
            return {
                "success": True,
                "data": {
                    "labels": labels,
                    "datasets": [],
                    "overall_trend": [None] * len(labels),
                    "period": period
                }
            }
        
        # Period gruplama
        if period == "weekly":
            num_periods = 8
            now = datetime.now()
            period_starts = [
                (now - timedelta(weeks=i)).strftime('%Y-%m-%d')
                for i in range(num_periods-1, -1, -1)
            ]
                        # ✅ LOG EKLE - DOĞRULAMA İÇİN
            print(f"\n📅 HAFTALIK PERIOD KONTROLÜ")
            print(f"Bugün: {now.strftime('%Y-%m-%d %A')}")
            print(f"Period başlangıçları:")
            for idx, ps in enumerate(period_starts):
                print(f"  [{idx}] {ps}")
            # DOĞRU LABEL'LAR (soldan sağa: eskiden yeniye)
            labels = []
            for i in range(num_periods):
                age = num_periods - 1 - i
                if age == 0:
                    labels.append("Bu hafta")
                elif age == 1:
                    labels.append("Geçen hafta")
                else:
                    labels.append(f"{age} hafta önce")
            
            group_func = get_week_start
        else:
            num_periods = 7
            now = datetime.now()
            period_starts = [
                (now - timedelta(days=30*i)).strftime('%Y-%m-01')
                for i in range(num_periods-1, -1, -1)
            ]
            
            # DOĞRU LABEL'LAR (soldan sağa: eskiden yeniye)
            labels = []
            for i in range(num_periods):
                age = num_periods - 1 - i
                if age == 0:
                    labels.append("Bu ay")
                elif age == 1:
                    labels.append("Geçen ay")
                else:
                    labels.append(f"{age} ay önce")
            
            group_func = get_month_start
        
        # Test'leri period'lara grupla
        period_tests = defaultdict(list)
        for test in tests:
            period_key = group_func(test['test_date'])
            period_tests[period_key].append(test)
        
        # Overall trend hesapla
        overall_trend = []
        for period_start in period_starts:
            period_data = period_tests.get(period_start, [])
            if period_data:
                avg = sum(t['success_rate'] for t in period_data) / len(period_data)
                overall_trend.append(round(avg, 1))
            else:
                overall_trend.append(None)
        
        # Subject bazında datasets (en çok test yapılan 3 ders)
        subject_tests = defaultdict(list)
        for test in tests:
            subject_tests[test['subject_id']].append(test)
        
        top_subjects = sorted(subject_tests.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        
        datasets = []
        for subject_id, subject_test_list in top_subjects:
            # Subject adını al
            subject_result = supabase.table("subjects").select("name_tr").eq("id", subject_id).execute()
            subject_name = subject_result.data[0]['name_tr'] if subject_result.data else "Bilinmeyen"
            
            # Period bazında hesapla
            subject_data = []
            for period_start in period_starts:
                period_data = [t for t in subject_test_list if group_func(t['test_date']) == period_start]
                if period_data:
                    avg = sum(t['success_rate'] for t in period_data) / len(period_data)
                    subject_data.append(round(avg, 1))
                else:
                    subject_data.append(None)
            
            datasets.append({
                "label": subject_name,
                "data": subject_data,
                "subject_id": subject_id
            })
        
        return {
            "success": True,
            "data": {
                "labels": labels,
                "datasets": datasets,
                "overall_trend": overall_trend,
                "period": period
            }
        }
    
    except Exception as e:
        print(f"❌ Trends error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def progress_health():
    """Health check"""
    return {
        "status": "healthy",
        "endpoints": 3,
        "features": ["projection", "subjects", "trends"],
        "data_source": "student_topic_tests"
    }