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