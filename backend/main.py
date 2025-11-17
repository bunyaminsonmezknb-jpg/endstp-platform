from fastapi import FastAPI, HTTPException, Depends
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
@app.post("/api/auth/signup")
async def signup(data: SignUpRequest):
    try:
        # Supabase Auth ile kullanıcı oluştur
        auth_response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })
        
        if auth_response.user:
            # Profile tablosuna ekle
            profile_data = {
                "id": auth_response.user.id,
                "email": data.email,
                "full_name": data.full_name,
                "role": data.role
            }
            
            supabase.table("profiles").insert(profile_data).execute()
            
            return {
                "message": "Kayıt başarılı! 🎉",
                "user": {
                    "id": auth_response.user.id,
                    "email": auth_response.user.email,
                    "role": data.role
                }
            }
        else:
            raise HTTPException(status_code=400, detail="Kayıt başarısız")
            
    except Exception as e:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)