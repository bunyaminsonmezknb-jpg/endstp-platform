from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

app = FastAPI(
    title="End.STP API",
    description="Konu Öğrenme Analitiği Platformu API",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Pydantic modeller
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "student"

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class TestResultCreate(BaseModel):
    user_id: str
    test_datetime: str  # test_date yerine test_datetime
    subject: str
    topic: str
    correct_count: int
    wrong_count: int
    empty_count: int
    net: float
    success_rate: float

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "End.STP API'ye Hoş Geldiniz! 🎯",
        "status": "Çalışıyor",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "End.STP Backend",
        "database": "connected" if supabase else "disconnected",
        "timestamp": datetime.now().isoformat()
    }

# Kayıt olma
@app.post("/api/test-results")
async def create_test_result(data: TestResultCreate):
    try:
        # Önce student kaydı var mı kontrol et, yoksa oluştur
        student_check = supabase.table("students").select("*").eq("user_id", data.user_id).execute()
        
        if not student_check.data:
            # Student kaydı yoksa oluştur
            profile = supabase.table("profiles").select("*").eq("id", data.user_id).execute()
            student_name = profile.data[0]["full_name"] if profile.data else "Öğrenci"
            
            new_student = supabase.table("students").insert({
                "user_id": data.user_id,
                "name": student_name,
                "class": "11. Sınıf"
            }).execute()
            
            student_id = new_student.data[0]["id"]
        else:
            student_id = student_check.data[0]["id"]
        
        # Test sonucunu kaydet
        result = supabase.table("test_results").insert({
            "student_id": student_id,
            "subject": data.subject,
            "topic": data.topic,
            "correct_count": data.correct_count,
            "wrong_count": data.wrong_count,
            "empty_count": data.empty_count,
            "net": data.net,
            "success_rate": data.success_rate,
            "entry_timestamp": data.test_datetime
        }).execute()
        
        return {
            "message": "Test sonucu kaydedildi! ✅",
            "data": result.data
        }
    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Giriş yapma
@app.post("/api/auth/signin")
async def signin(data: SignInRequest):
    try:
        # Supabase Auth ile giriş
        auth_response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password,
        })
        
        if auth_response.user:
            # Profile bilgilerini al
            profile = supabase.table("profiles").select("*").eq("id", auth_response.user.id).execute()
            
            return {
                "message": "Giriş başarılı! ✅",
                "access_token": auth_response.session.access_token,
                "user": {
                    "id": auth_response.user.id,
                    "email": auth_response.user.email,
                    "full_name": profile.data[0]["full_name"] if profile.data else None,
                    "role": profile.data[0]["role"] if profile.data else "student"
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Giriş başarısız")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")

# Test sonucu kaydetme
@app.post("/api/test-results")
async def create_test_result(data: TestResultCreate):
    try:
        # Test sonucunu kaydet
        result = supabase.table("test_results").insert({
            "student_id": data.user_id,
            "subject": data.subject,
            "topic": data.topic,
            "correct_count": data.correct_count,
            "wrong_count": data.wrong_count,
            "empty_count": data.empty_count,
            "net": data.net,
            "success_rate": data.success_rate,
            "entry_timestamp": data.test_date
        }).execute()
        
        return {
            "message": "Test sonucu kaydedildi! ✅",
            "data": result.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
# ============================================
# DYNAMIC DATA ENDPOINTS (Form için)
# ============================================

@app.get("/api/subjects")
async def get_subjects():
    """Ders listesini getir"""
    try:
        result = supabase.table("subjects").select(
            "id, code, name_tr, icon, color"
        ).eq("is_active", True).order("order_index").execute()
        
        return {
            "subjects": result.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/subjects/{subject_id}/topics")
async def get_topics_by_subject(subject_id: str):
    """Bir derse ait konuları getir"""
    try:
        result = supabase.table("topics").select(
            "id, code, name_tr, difficulty_level, exam_weight"
        ).eq("subject_id", subject_id).eq("is_active", True).order("order_index").execute()
        
        return {
            "topics": result.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/education-levels")
async def get_education_levels():
    """Eğitim seviyelerini getir"""
    try:
        result = supabase.table("education_levels").select(
            "id, code, name_tr, grade_range"
        ).eq("is_active", True).order("order_index").execute()
        
        return {
            "levels": result.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/class-levels")
async def get_class_levels():
    """Sınıf seviyelerini getir"""
    try:
        result = supabase.table("class_levels").select(
            "id, code, name_tr, grade_number"
        ).eq("is_active", True).order("order_index").execute()
        
        return {
            "classes": result.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 # ============================================
# DASHBOARD ENDPOINTS
# ============================================

@app.get("/api/students/{student_id}/dashboard")
async def get_student_dashboard(student_id: str):
    """Dashboard için tüm verileri getir"""
    try:
        # 1. Öğrenci bilgisi
        student = supabase.table("students").select("*").eq("id", student_id).single().execute()
        
        # 2. Toplam test sayısı
        test_count = supabase.table("test_results").select("id", count="exact").eq("student_id", student_id).execute()
        total_tests = test_count.count if test_count.count else 0
        
        # 3. Ortalama net
        test_results = supabase.table("test_results").select("net").eq("student_id", student_id).execute()
        nets = [t["net"] for t in test_results.data if t["net"]]
        avg_net = sum(nets) / len(nets) if nets else 0
        
        # 4. Son 7 gün test performansı (haftalık grafik)
        from datetime import datetime, timedelta
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        
        weekly_tests = supabase.table("test_results").select(
            "net, entry_timestamp"
        ).eq("student_id", student_id).gte("entry_timestamp", seven_days_ago).order("entry_timestamp").execute()
        
        # Günlere göre grupla
        daily_nets = {}
        for test in weekly_tests.data:
            date = test["entry_timestamp"][:10]  # YYYY-MM-DD
            if date not in daily_nets:
                daily_nets[date] = []
            daily_nets[date].append(test["net"])
        
        # Ortalama al
        weekly_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=6-i)).strftime("%Y-%m-%d")
            day_name = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"][(datetime.now() - timedelta(days=6-i)).weekday()]
            avg = sum(daily_nets.get(date, [0])) / len(daily_nets.get(date, [1])) if daily_nets.get(date) else 0
            weekly_data.append({
                "day": day_name,
                "net": round(avg, 2)
            })
        
        # 5. Öncelikli konular (başarı oranına göre)
        topic_stats = supabase.table("test_results").select(
            "subject, topic, success_rate"
        ).eq("student_id", student_id).execute()
        
        # Konulara göre grupla
        topic_performance = {}
        for test in topic_stats.data:
            key = f"{test['subject']}-{test['topic']}"
            if key not in topic_performance:
                topic_performance[key] = {
                    "subject": test["subject"],
                    "topic": test["topic"],
                    "rates": []
                }
            topic_performance[key]["rates"].append(test["success_rate"])
        
        # Ortalama başarı oranını hesapla
        priority_topics = []
        for key, data in topic_performance.items():
            avg_rate = sum(data["rates"]) / len(data["rates"])
            priority_topics.append({
                "subject": data["subject"],
                "topic": data["topic"],
                "score": round(avg_rate, 1),
                "priority": "urgent" if avg_rate < 50 else "high" if avg_rate < 70 else "medium"
            })
        
        # Başarı oranına göre sırala (en düşük önce)
        priority_topics.sort(key=lambda x: x["score"])
        
        return {
            "student": {
                "name": student.data["name"],
                "class": student.data["class"],
                "total_tests": total_tests,
                "average_net": round(avg_net, 2)
            },
            "weekly_data": weekly_data,
            "priority_topics": priority_topics[:5]  # İlk 5 konu
        }
        
    except Exception as e:
        print(f"Dashboard hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/user/{user_id}/student")
async def get_student_by_user(user_id: str):
    """User ID'den student ID'yi bul"""
    try:
        result = supabase.table("students").select("*").eq("user_id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
        
        return {
            "student": result.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))       
       # ============================================
# REPORTS ENDPOINTS
# ============================================

@app.get("/api/students/{student_id}/reports")
async def get_student_reports(student_id: str):
    """Detaylı raporlar için tüm verileri getir"""
    try:
        # 1. Tüm test sonuçları
        all_tests = supabase.table("test_results").select(
            "*, entry_timestamp"
        ).eq("student_id", student_id).order("entry_timestamp", desc=True).execute()
        
        # 2. Ders bazlı performans
        subject_performance = {}
        for test in all_tests.data:
            subject = test["subject"]
            if subject not in subject_performance:
                subject_performance[subject] = {
                    "total_tests": 0,
                    "total_net": 0,
                    "total_correct": 0,
                    "total_wrong": 0,
                    "total_empty": 0
                }
            
            subject_performance[subject]["total_tests"] += 1
            subject_performance[subject]["total_net"] += test["net"]
            subject_performance[subject]["total_correct"] += test["correct_count"]
            subject_performance[subject]["total_wrong"] += test["wrong_count"]
            subject_performance[subject]["total_empty"] += test["empty_count"]
        
        # Ortalamaları hesapla
        subject_stats = []
        for subject, data in subject_performance.items():
            avg_net = data["total_net"] / data["total_tests"]
            success_rate = (data["total_correct"] / (data["total_correct"] + data["total_wrong"] + data["total_empty"])) * 100 if (data["total_correct"] + data["total_wrong"] + data["total_empty"]) > 0 else 0
            
            subject_stats.append({
                "subject": subject,
                "test_count": data["total_tests"],
                "avg_net": round(avg_net, 2),
                "total_correct": data["total_correct"],
                "total_wrong": data["total_wrong"],
                "total_empty": data["total_empty"],
                "success_rate": round(success_rate, 1)
            })
        
        # Başarı oranına göre sırala
        subject_stats.sort(key=lambda x: x["avg_net"], reverse=True)
        
        # 3. Konu bazlı performans
        topic_performance = {}
        for test in all_tests.data:
            key = f"{test['subject']}-{test['topic']}"
            if key not in topic_performance:
                topic_performance[key] = {
                    "subject": test["subject"],
                    "topic": test["topic"],
                    "tests": [],
                    "total_net": 0,
                    "count": 0
                }
            
            topic_performance[key]["tests"].append({
                "net": test["net"],
                "date": test["entry_timestamp"]
            })
            topic_performance[key]["total_net"] += test["net"]
            topic_performance[key]["count"] += 1
        
        # Konu istatistiklerini hesapla
        topic_stats = []
        for key, data in topic_performance.items():
            avg_net = data["total_net"] / data["count"]
            
            # Trend hesapla (ilk test vs son test)
            if len(data["tests"]) >= 2:
                first_net = data["tests"][-1]["net"]  # En eski
                last_net = data["tests"][0]["net"]    # En yeni
                trend = last_net - first_net
            else:
                trend = 0
            
            topic_stats.append({
                "subject": data["subject"],
                "topic": data["topic"],
                "test_count": data["count"],
                "avg_net": round(avg_net, 2),
                "trend": round(trend, 2),
                "last_net": data["tests"][0]["net"] if data["tests"] else 0
            })
        
        # Net'e göre sırala
        topic_stats.sort(key=lambda x: x["avg_net"], reverse=True)
        
        # 4. Güçlü ve zayıf konular
        strong_topics = [t for t in topic_stats if t["avg_net"] >= 9][:5]
        weak_topics = [t for t in topic_stats if t["avg_net"] < 7][:5]
        
        # 5. Son testler (detaylı)
        recent_tests = []
        for test in all_tests.data[:10]:  # Son 10 test
            recent_tests.append({
                "id": test["id"],
                "subject": test["subject"],
                "topic": test["topic"],
                "net": test["net"],
                "correct": test["correct_count"],
                "wrong": test["wrong_count"],
                "empty": test["empty_count"],
                "success_rate": test["success_rate"],
                "date": test["entry_timestamp"]
            })
        
        # 6. Genel istatistikler
        total_tests = len(all_tests.data)
        total_net = sum([t["net"] for t in all_tests.data])
        avg_net = total_net / total_tests if total_tests > 0 else 0
        
        total_correct = sum([t["correct_count"] for t in all_tests.data])
        total_wrong = sum([t["wrong_count"] for t in all_tests.data])
        total_empty = sum([t["empty_count"] for t in all_tests.data])
        total_questions = total_correct + total_wrong + total_empty
        
        overall_success = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        return {
            "overall_stats": {
                "total_tests": total_tests,
                "avg_net": round(avg_net, 2),
                "total_correct": total_correct,
                "total_wrong": total_wrong,
                "total_empty": total_empty,
                "success_rate": round(overall_success, 1)
            },
            "subject_performance": subject_stats,
            "topic_performance": topic_stats,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "recent_tests": recent_tests
        }
        
    except Exception as e:
        print(f"Reports hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e)) 
      # ============================================
# ADMIN ENDPOINTS
# ============================================

# Admin kontrolü için helper
def is_admin(user_email: str) -> bool:
    """Email'e göre admin kontrolü (şimdilik basit)"""
    # TODO: Veritabanında admin role sistemi
    admin_emails = [
        "admin@endstp.com",
        "ogretmen@endstp.com"
    ]
    return user_email in admin_emails

@app.get("/api/admin/students")
async def get_all_students():
    """Tüm öğrencileri listele (Admin)"""
    try:
        # Öğrencileri ve profil bilgilerini çek
        students = supabase.table("students").select(
            "*, profiles!students_user_id_fkey(email, full_name)"
        ).order("created_at", desc=True).execute()
        
        # Test sayılarını ekle
        student_list = []
        for student in students.data:
            # Her öğrenci için test sayısı
            test_count = supabase.table("test_results").select(
                "id", count="exact"
            ).eq("student_id", student["id"]).execute()
            
            # Son test tarihi
            last_test = supabase.table("test_results").select(
                "entry_timestamp"
            ).eq("student_id", student["id"]).order(
                "entry_timestamp", desc=True
            ).limit(1).execute()
            
            student_list.append({
                "id": student["id"],
                "name": student["name"],
                "class": student["class"],
                "email": student["profiles"]["email"] if student["profiles"] else None,
                "test_count": test_count.count or 0,
                "last_test": last_test.data[0]["entry_timestamp"] if last_test.data else None,
                "created_at": student["created_at"]
            })
        
        return {
            "students": student_list,
            "total": len(student_list)
        }
        
    except Exception as e:
        print(f"Admin students hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/subjects")
async def get_all_subjects_admin():
    """Tüm dersleri listele (Admin)"""
    try:
        subjects = supabase.table("subjects").select(
            "*, education_systems(name_tr)"
        ).order("order_index").execute()
        
        # Her ders için konu sayısı
        subject_list = []
        for subject in subjects.data:
            topic_count = supabase.table("topics").select(
                "id", count="exact"
            ).eq("subject_id", subject["id"]).execute()
            
            subject_list.append({
                "id": subject["id"],
                "code": subject["code"],
                "name_tr": subject["name_tr"],
                "name_en": subject["name_en"],
                "icon": subject["icon"],
                "color": subject["color"],
                "total_questions": subject["total_questions"],
                "topic_count": topic_count.count or 0,
                "is_active": subject["is_active"]
            })
        
        return {
            "subjects": subject_list,
            "total": len(subject_list)
        }
        
    except Exception as e:
        print(f"Admin subjects hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/topics")
async def get_all_topics_admin():
    """Tüm konuları listele (Admin)"""
    try:
        topics = supabase.table("topics").select(
            "*, subjects(name_tr, icon)"
        ).order("created_at", desc=True).execute()
        
        # Her konu için test sayısı
        topic_list = []
        for topic in topics.data:
            test_count = supabase.table("test_results").select(
                "id", count="exact"
            ).eq("topic", topic["name_tr"]).execute()
            
            topic_list.append({
                "id": topic["id"],
                "code": topic["code"],
                "name_tr": topic["name_tr"],
                "name_en": topic["name_en"],
                "subject_name": topic["subjects"]["name_tr"] if topic["subjects"] else None,
                "subject_icon": topic["subjects"]["icon"] if topic["subjects"] else None,
                "difficulty_level": topic["difficulty_level"],
                "exam_weight": topic["exam_weight"],
                "test_count": test_count.count or 0,
                "is_active": topic["is_active"],
                "created_at": topic["created_at"]
            })
        
        return {
            "topics": topic_list,
            "total": len(topic_list)
        }
        
    except Exception as e:
        print(f"Admin topics hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/topics")
async def create_topic_admin(topic_data: dict):
    """Yeni konu ekle (Admin)"""
    try:
        # Konu ekle
        new_topic = supabase.table("topics").insert({
            "subject_id": topic_data["subject_id"],
            "code": topic_data.get("code", ""),
            "name_tr": topic_data["name_tr"],
            "name_en": topic_data.get("name_en", topic_data["name_tr"]),
            "difficulty_level": topic_data.get("difficulty_level", 3),
            "exam_weight": topic_data.get("exam_weight", 0),
            "bloom_level": topic_data.get("bloom_level", "apply"),
            "is_active": True
        }).execute()
        
        return {
            "success": True,
            "topic": new_topic.data[0]
        }
        
    except Exception as e:
        print(f"Create topic hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/admin/topics/{topic_id}")
async def update_topic_admin(topic_id: str, topic_data: dict):
    """Konu güncelle (Admin)"""
    try:
        updated_topic = supabase.table("topics").update({
            "name_tr": topic_data.get("name_tr"),
            "name_en": topic_data.get("name_en"),
            "difficulty_level": topic_data.get("difficulty_level"),
            "exam_weight": topic_data.get("exam_weight"),
            "is_active": topic_data.get("is_active"),
            "updated_at": "now()"
        }).eq("id", topic_id).execute()
        
        return {
            "success": True,
            "topic": updated_topic.data[0]
        }
        
    except Exception as e:
        print(f"Update topic hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/admin/topics/{topic_id}")
async def delete_topic_admin(topic_id: str):
    """Konu sil (soft delete) (Admin)"""
    try:
        # Soft delete - is_active = false
        deleted_topic = supabase.table("topics").update({
            "is_active": False,
            "updated_at": "now()"
        }).eq("id", topic_id).execute()
        
        return {
            "success": True,
            "message": "Konu deaktif edildi"
        }
        
    except Exception as e:
        print(f"Delete topic hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/stats")
async def get_admin_stats():
    """Admin dashboard istatistikleri"""
    try:
        # Toplam sayılar
        total_students = supabase.table("students").select(
            "id", count="exact"
        ).execute()
        
        total_tests = supabase.table("test_results").select(
            "id", count="exact"
        ).execute()
        
        total_topics = supabase.table("topics").select(
            "id", count="exact"
        ).eq("is_active", True).execute()
        
        total_subjects = supabase.table("subjects").select(
            "id", count="exact"
        ).eq("is_active", True).execute()
        
        # Son 7 gün aktivite
        from datetime import datetime, timedelta
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        
        recent_tests = supabase.table("test_results").select(
            "id", count="exact"
        ).gte("entry_timestamp", seven_days_ago).execute()
        
        return {
            "total_students": total_students.count or 0,
            "total_tests": total_tests.count or 0,
            "total_topics": total_topics.count or 0,
            "total_subjects": total_subjects.count or 0,
            "recent_tests": recent_tests.count or 0
        }
        
    except Exception as e:
        print(f"Admin stats hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        # backend/main.py en alta

@app.post("/api/admin/exam-history")
async def create_exam_history(exam_data: dict):
    """Yeni sınav verisi ekle"""
    try:
        # Sınav oluştur
        exam = supabase.table("exam_history").insert({
            "exam_system_id": exam_data["exam_system_id"],
            "year": exam_data["year"],
            "exam_date": exam_data.get("exam_date"),
            "exam_type": exam_data["exam_type"],
            "total_questions": exam_data["total_questions"],
            "is_official": True
        }).execute()
        
        exam_id = exam.data[0]["id"]
        
        return {
            "success": True,
            "exam_id": exam_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/topic-exam-data")
async def add_topic_to_exam(data: dict):
    """Bir konunun sınavdaki soru sayısını ekle/güncelle"""
    try:
        # Konu - sınav ilişkisi
        topic_exam = supabase.table("topic_exam_history").insert({
            "topic_id": data["topic_id"],
            "exam_history_id": data["exam_history_id"],
            "questions_count": data["questions_count"],
            "question_numbers": data.get("question_numbers", []),
            "is_primary_topic": data.get("is_primary_topic", True),
            "topic_coverage_percentage": data.get("coverage", 100)
        }).execute()
        
        # Yıllık istatistiği güncelle
        year = get_exam_year(data["exam_history_id"])
        exam_system_id = get_exam_system_id(data["exam_history_id"])
        
        # Mevcut kayıt var mı?
        existing = supabase.table("topic_yearly_stats").select("*").eq(
            "topic_id", data["topic_id"]
        ).eq("exam_system_id", exam_system_id).eq("year", year).execute()
        
        if existing.data:
            # Güncelle
            if data.get("is_primary_topic", True):
                supabase.table("topic_yearly_stats").update({
                    "primary_questions": existing.data[0]["primary_questions"] + data["questions_count"]
                }).eq("id", existing.data[0]["id"]).execute()
            else:
                supabase.table("topic_yearly_stats").update({
                    "secondary_questions": existing.data[0]["secondary_questions"] + data["questions_count"]
                }).eq("id", existing.data[0]["id"]).execute()
        else:
            # Yeni oluştur
            supabase.table("topic_yearly_stats").insert({
                "topic_id": data["topic_id"],
                "exam_system_id": exam_system_id,
                "year": year,
                "primary_questions": data["questions_count"] if data.get("is_primary_topic", True) else 0,
                "secondary_questions": 0 if data.get("is_primary_topic", True) else data["questions_count"],
                "total_questions": data["questions_count"],
                "question_numbers": data.get("question_numbers", [])
            }).execute()
        
        return {
            "success": True,
            "message": "Sınav verisi eklendi"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/topics/{topic_id}/yearly-stats")
async def get_topic_yearly_stats(topic_id: str, exam_system_id: str):
    """Konunun yıl yıl istatistiklerini getir"""
    try:
        stats = supabase.table("topic_yearly_stats").select("*").eq(
            "topic_id", topic_id
        ).eq("exam_system_id", exam_system_id).order("year", desc=True).execute()
        
        return {
            "stats": stats.data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/multi-topic-question")
async def add_multi_topic_question(data: dict):
    """Çok konulu soru ekle"""
    try:
        multi = supabase.table("multi_topic_questions").insert({
            "exam_history_id": data["exam_history_id"],
            "question_number": data["question_number"],
            "primary_topic_id": data["primary_topic_id"],
            "secondary_topics": data["secondary_topics"],
            "description": data.get("description", "")
        }).execute()
        
        return {
            "success": True,
            "multi_topic_question": multi.data[0]
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# ============================================
# ÖSYM KONU YÖNETİMİ
# ============================================

@app.get("/api/osym/topics")
async def get_osym_topics(exam_type_id: str = None, published_year: int = None):
    """ÖSYM resmi konu listesini getir"""
    try:
        query = supabase.table("osym_topics").select(
            "*, exam_types(code, name_tr, short_name)"
        )
        
        if exam_type_id:
            query = query.eq("exam_type_id", exam_type_id)
        
        if published_year:
            query = query.eq("published_year", published_year)
        
        topics = query.order("subject_name").execute()
        
        return {
            "osym_topics": topics.data,
            "total": len(topics.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/osym-topics")
async def create_osym_topic(data: dict):
    """Yeni ÖSYM konusu ekle"""
    try:
        new_topic = supabase.table("osym_topics").insert({
            "exam_type_id": data["exam_type_id"],
            "official_name": data["official_name"],
            "subject_name": data["subject_name"],
            "related_grade_levels": data.get("related_grade_levels", []),
            "published_year": data.get("published_year", 2024),
            "description": data.get("description", ""),
            "notes": data.get("notes", ""),
            "is_active": True
        }).execute()
        
        return {
            "success": True,
            "osym_topic": new_topic.data[0]
        }
        
    except Exception as e:
        print(f"Create ÖSYM topic hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/admin/osym-topics/{topic_id}")
async def update_osym_topic(topic_id: str, data: dict):
    """ÖSYM konusu güncelle"""
    try:
        updated = supabase.table("osym_topics").update({
            "official_name": data.get("official_name"),
            "subject_name": data.get("subject_name"),
            "related_grade_levels": data.get("related_grade_levels"),
            "published_year": data.get("published_year"),
            "description": data.get("description"),
            "notes": data.get("notes"),
            "is_active": data.get("is_active"),
            "updated_at": "now()"
        }).eq("id", topic_id).execute()
        
        return {
            "success": True,
            "osym_topic": updated.data[0]
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/admin/osym-topics/{topic_id}")
async def delete_osym_topic(topic_id: str):
    """ÖSYM konusu sil (soft delete)"""
    try:
        deleted = supabase.table("osym_topics").update({
            "is_active": False,
            "updated_at": "now()"
        }).eq("id", topic_id).execute()
        
        return {
            "success": True,
            "message": "ÖSYM konusu deaktif edildi"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================
# KONU EŞLEŞTIRME (MEB ↔ ÖSYM)
# ============================================

@app.get("/api/topics/{topic_id}/osym-mappings")
async def get_topic_osym_mappings(topic_id: str):
    """Bir MEB konusunun ÖSYM eşleştirmelerini getir"""
    try:
        mappings = supabase.table("topic_osym_mapping").select(
            "*, osym_topics(official_name, subject_name, exam_types(short_name, code))"
        ).eq("meb_topic_id", topic_id).execute()
        
        # Konu bilgisi
        topic = supabase.table("topics").select(
            "*, subjects(name_tr, class_level_id, class_levels(grade_number))"
        ).eq("id", topic_id).single().execute()
        
        return {
            "meb_topic": {
                "id": topic.data["id"],
                "name": topic.data["name_tr"],
                "subject": topic.data["subjects"]["name_tr"],
                "grade": topic.data["subjects"]["class_levels"]["grade_number"]
            },
            "osym_mappings": mappings.data,
            "total_mappings": len(mappings.data)
        }
        
    except Exception as e:
        print(f"Get topic ÖSYM mappings hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/topic-osym-mapping")
async def create_topic_osym_mapping(data: dict):
    """MEB-ÖSYM konu eşleştirmesi oluştur"""
    try:
        # Mevcut var mı?
        existing = supabase.table("topic_osym_mapping").select("*").eq(
            "meb_topic_id", data["meb_topic_id"]
        ).eq("osym_topic_id", data["osym_topic_id"]).execute()
        
        mapping_data = {
            "match_type": data.get("match_type", "exact"),
            "match_percentage": data.get("match_percentage", 100),
            "mapping_notes": data.get("mapping_notes", ""),
            "verified": data.get("verified", False),
            "created_by": data.get("created_by", "admin"),
            "updated_at": "now()"
        }
        
        if existing.data:
            # Güncelle
            updated = supabase.table("topic_osym_mapping").update(
                mapping_data
            ).eq("id", existing.data[0]["id"]).execute()
            
            return {
                "success": True,
                "message": "Eşleştirme güncellendi",
                "mapping": updated.data[0]
            }
        else:
            # Yeni oluştur
            mapping_data.update({
                "meb_topic_id": data["meb_topic_id"],
                "osym_topic_id": data["osym_topic_id"]
            })
            
            new_mapping = supabase.table("topic_osym_mapping").insert(
                mapping_data
            ).execute()
            
            return {
                "success": True,
                "message": "Eşleştirme oluşturuldu",
                "mapping": new_mapping.data[0]
            }
        
    except Exception as e:
        print(f"Create topic ÖSYM mapping hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/admin/topic-osym-mapping/{mapping_id}")
async def delete_topic_osym_mapping(mapping_id: str):
    """Eşleştirme sil"""
    try:
        deleted = supabase.table("topic_osym_mapping").delete().eq(
            "id", mapping_id
        ).execute()
        
        return {
            "success": True,
            "message": "Eşleştirme silindi"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/unmapped-topics")
async def get_unmapped_topics(exam_type_id: str = None):
    """Henüz ÖSYM eşleştirmesi yapılmamış konuları getir"""
    try:
        # Tüm konuları al
        all_topics_res = supabase.table("topics").select(
            "id, name_tr, subject_id"
        ).eq("is_active", True).execute()
        
        if not all_topics_res.data:
            return {
                "unmapped_topics": [],
                "total": 0
            }
        
        # Eşleştirmesi olanları al
        mapped = supabase.table("topic_osym_mapping").select("meb_topic_id").execute()
        mapped_ids = [m["meb_topic_id"] for m in mapped.data] if mapped.data else []
        
        # Eşleştirmesi olmayanları filtrele
        unmapped = []
        for t in all_topics_res.data:
            if t["id"] not in mapped_ids:
                # Subject bilgisi al
                subject = supabase.table("subjects").select(
                    "name_tr, class_level_id"
                ).eq("id", t["subject_id"]).single().execute()
                
                if subject.data:
                    grade_number = None
                    if subject.data.get("class_level_id"):
                        class_level = supabase.table("class_levels").select(
                            "grade_number"
                        ).eq("id", subject.data["class_level_id"]).single().execute()
                        
                        if class_level.data:
                            grade_number = class_level.data.get("grade_number")
                    
                    unmapped.append({
                        "id": t["id"],
                        "name": t["name_tr"],
                        "subject": subject.data["name_tr"],
                        "grade": grade_number or 0
                    })
        
        # Exam type'a göre filtrele (opsiyonel)
        if exam_type_id:
            # Sadece ilgili sınıf seviyelerindeki konuları getir
            grade_mappings = supabase.table("grade_exam_mapping").select(
                "class_level_id"
            ).eq("exam_type_id", exam_type_id).execute()
            
            if grade_mappings.data:
                relevant_class_level_ids = [gm["class_level_id"] for gm in grade_mappings.data]
                
                # Class level'lardan grade numaralarını al
                relevant_grades = []
                for cl_id in relevant_class_level_ids:
                    cl = supabase.table("class_levels").select(
                        "grade_number"
                    ).eq("id", cl_id).single().execute()
                    
                    if cl.data:
                        relevant_grades.append(cl.data["grade_number"])
                
                unmapped = [t for t in unmapped if t["grade"] in relevant_grades]
        
        return {
            "unmapped_topics": unmapped,
            "total": len(unmapped)
        }
        
    except Exception as e:
        print(f"Get unmapped topics hatası: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# SINIF SEVİYESİ - SINAV EŞLEŞTİRME
# ============================================

@app.get("/api/grade-levels/{grade_level_id}/exam-types")
async def get_grade_exam_types(grade_level_id: str):
    """Bir sınıf seviyesinin ilgili olduğu sınavları getir"""
    try:
        mappings = supabase.table("grade_exam_mapping").select(
            "*, exam_types(id, code, name_tr, short_name, total_questions)"
        ).eq("class_level_id", grade_level_id).execute()
        
        return {
            "exam_types": [m["exam_types"] for m in mappings.data],
            "mappings": mappings.data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/exam-types/{exam_type_id}/grades")
async def get_exam_type_grades(exam_type_id: str):
    """Bir sınav türünün ilgili olduğu sınıf seviyelerini getir"""
    try:
        mappings = supabase.table("grade_exam_mapping").select(
            "*, class_levels(id, grade_number, name_tr)"
        ).eq("exam_type_id", exam_type_id).execute()
        
        return {
            "grades": [m["class_levels"] for m in mappings.data],
            "mappings": mappings.data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================
# ÖĞRENCİ SINAV HEDEFİ
# ============================================

@app.post("/api/students/{student_id}/exam-goal")
async def set_student_exam_goal(student_id: str, goal_data: dict):
    """Öğrencinin sınav hedefini belirle (opsiyonel)"""
    try:
        # Mevcut aktif hedef var mı?
        existing = supabase.table("student_exam_goals").select("*").eq(
            "student_id", student_id
        ).eq("status", "active").execute()
        
        goal_info = {
            "exam_type_id": goal_data["exam_type_id"],
            "target_year": goal_data["target_year"],
            "target_date": goal_data.get("target_date"),
            "focus_subjects": goal_data.get("focus_subjects", []),
            "notes": goal_data.get("notes", ""),
            "updated_at": "now()"
        }
        
        if existing.data:
            # Güncelle
            updated = supabase.table("student_exam_goals").update(
                goal_info
            ).eq("id", existing.data[0]["id"]).execute()
            
            return {
                "success": True,
                "message": "Hedef güncellendi",
                "goal": updated.data[0]
            }
        else:
            # Yeni oluştur
            goal_info.update({
                "student_id": student_id,
                "status": "active"
            })
            
            new_goal = supabase.table("student_exam_goals").insert(
                goal_info
            ).execute()
            
            return {
                "success": True,
                "message": "Hedef oluşturuldu",
                "goal": new_goal.data[0]
            }
        
    except Exception as e:
        print(f"Set exam goal hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/students/{student_id}/exam-goal")
async def get_student_exam_goal(student_id: str):
    """Öğrencinin aktif sınav hedefini getir"""
    try:
        goal = supabase.table("student_exam_goals").select(
            "*, exam_types(code, name_tr, short_name, total_questions)"
        ).eq("student_id", student_id).eq("status", "active").execute()
        
        if goal.data:
            return {
                "has_goal": True,
                "goal": goal.data[0]
            }
        else:
            return {
                "has_goal": False,
                "message": "Öğrencinin sınav hedefi yok (sadece konu öğrenme odaklı)"
            }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================
# GENİŞLETİLMİŞ KONU ANALİZİ (ÖSYM Bağlamlı)
# ============================================

@app.get("/api/topics/{topic_id}/complete-info")
async def get_topic_complete_info(topic_id: str):
    """
    Konunun tam bilgisi:
    - MEB müfredat bilgisi
    - ÖSYM eşleştirmeleri
    - Geçmiş yıl sınav verileri
    - Sınav ağırlığı
    """
    try:
        # Temel konu bilgisi
        topic = supabase.table("topics").select(
            "*, subjects(name_tr, icon, class_level_id, class_levels(grade_number))"
        ).eq("id", topic_id).single().execute()
        
        # ÖSYM eşleştirmeleri
        osym_mappings = supabase.table("topic_osym_mapping").select(
            "*, osym_topics(official_name, subject_name, exam_type_id, exam_types(code, short_name))"
        ).eq("meb_topic_id", topic_id).execute()
        
        # Her ÖSYM konusu için geçmiş yıl verileri
        exam_data = []
        for mapping in osym_mappings.data:
            osym_topic = mapping["osym_topics"]
            exam_type_id = osym_topic.get("exam_type_id")
            
            if exam_type_id:
                yearly = supabase.table("topic_yearly_stats").select("*").eq(
                    "topic_id", topic_id
                ).eq("exam_type_id", exam_type_id).order(
                    "year", desc=True
                ).limit(5).execute()
                
                exam_data.append({
                    "osym_name": osym_topic["official_name"],
                    "exam_type": osym_topic["exam_types"]["short_name"] if osym_topic.get("exam_types") else None,
                    "yearly_stats": yearly.data,
                    "avg_questions": sum([y["total_questions"] for y in yearly.data]) / len(yearly.data) if yearly.data else 0
                })
        
        return {
            "meb_info": {
                "id": topic.data["id"],
                "name": topic.data["name_tr"],
                "subject": topic.data["subjects"]["name_tr"],
                "grade": topic.data["subjects"]["class_levels"]["grade_number"],
                "difficulty": topic.data["objective_difficulty"]
            },
            "osym_mappings": [
                {
                    "official_name": m["osym_topics"]["official_name"],
                    "match_type": m["match_type"],
                    "match_percentage": m["match_percentage"],
                    "exam_type": m["osym_topics"]["exam_types"]["short_name"] if m["osym_topics"].get("exam_types") else None
                }
                for m in osym_mappings.data
            ],
            "exam_data": exam_data,
            "has_exam_context": len(exam_data) > 0
        }
        
    except Exception as e:
        print(f"Get topic complete info hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================
# ÖĞRENCİ KONU ANALİZİ (Sınav Bağlamlı)
# ============================================

@app.get("/api/students/{student_id}/topic-analysis")
async def get_student_topic_analysis(
    student_id: str, 
    include_exam_context: bool = False
):
    """
    Öğrencinin konu bazlı analizi
    
    include_exam_context=False: SADECE konu öğrenme analizi (varsayılan)
    include_exam_context=True: Sınav bağlamı dahil (varsa)
    """
    try:
        # Öğrencinin sınav hedefi var mı?
        exam_goal = supabase.table("student_exam_goals").select(
            "*, exam_types(id, code, short_name)"
        ).eq("student_id", student_id).eq("status", "active").execute()
        
        exam_type_id = exam_goal.data[0]["exam_type_id"] if exam_goal.data else None
        
        # Temel konu zorluk analizini getir
        difficulties = supabase.table("student_topic_difficulty").select(
            "*, topics(id, name_tr, subject_id, subjects(name_tr, icon))"
        ).eq("student_id", student_id).order(
            "final_difficulty_score", desc=True
        ).execute()
        
        result = {
            "student_id": student_id,
            "analysis_type": "learning_focused",
            "has_exam_goal": bool(exam_goal.data),
            "exam_goal": exam_goal.data[0] if exam_goal.data else None,
            "topics": []
        }
        
        for diff in difficulties.data:
            topic_data = {
                "topic_id": diff["topic_id"],
                "topic_name": diff["topics"]["name_tr"],
                "subject_name": diff["topics"]["subjects"]["name_tr"],
                "subject_icon": diff["topics"]["subjects"]["icon"],
                "difficulty_score": diff["final_difficulty_score"],
                "difficulty_level": diff["difficulty_level"],
                "trend": diff["trend"],
                "total_tests": diff["total_tests"],
                "avg_net": diff["avg_net"],
                "days_since_last_test": diff["days_since_last_test"]
            }
            
            # Sınav bağlamı istendiyse ve hedef varsa ekle
            if include_exam_context and exam_type_id:
                # Bu konunun ÖSYM eşleştirmeleri var mı?
                osym_mappings = supabase.table("topic_osym_mapping").select(
                    "*, osym_topics(official_name, subject_name)"
                ).eq("meb_topic_id", diff["topic_id"]).execute()
                
                if osym_mappings.data:
                    # Geçmiş yıl verileri
                    yearly = supabase.table("topic_yearly_stats").select("*").eq(
                        "topic_id", diff["topic_id"]
                    ).eq("exam_type_id", exam_type_id).order(
                        "year", desc=True
                    ).limit(5).execute()
                    
                    avg_questions = sum([y["total_questions"] for y in yearly.data]) / len(yearly.data) if yearly.data else 0
                    
                    topic_data["exam_context"] = {
                        "osym_name": osym_mappings.data[0]["osym_topics"]["official_name"],
                        "avg_questions_per_year": round(avg_questions, 1),
                        "last_5_years": yearly.data
                    }
                    
                    result["analysis_type"] = "exam_focused"
            
            result["topics"].append(topic_data)
        
        return result
        
    except Exception as e:
        print(f"Student topic analysis hatası: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))