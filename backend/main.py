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
