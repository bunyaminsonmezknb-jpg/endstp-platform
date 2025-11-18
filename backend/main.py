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