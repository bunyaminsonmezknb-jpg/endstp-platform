from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd
import io

# Load environment variables
load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# JWT setup
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="End.STP API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# MODELS
# ============================================

class UserSignIn(BaseModel):
    email: str
    password: str

class TestResultCreate(BaseModel):
    student_id: str
    exam_type_id: str
    topic_results: List[dict]
    test_date: Optional[str] = None

class OsymTopicCreate(BaseModel):
    exam_type_id: str
    official_name: str
    subject_name: str
    related_grade_levels: List[int]
    published_year: int = 2024
    notes: Optional[str] = None

class TopicMappingCreate(BaseModel):
    meb_topic_id: str
    osym_topic_id: str
    match_type: str = "exact"
    match_percentage: int = 100
    verified: bool = False
    created_by: str

# ============================================
# HELPER FUNCTIONS
# ============================================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ============================================
# ROUTES
# ============================================

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
        "status": "Çalışıyor",
        "message": "End.STP API sağlıklı çalışıyor",
        "timestamp": datetime.now().isoformat()
    }

# ============================================
# AUTH
# ============================================

@app.post("/api/auth/signin")
async def signin(user_data: UserSignIn):
    try:
        # Profile bul
        profile_res = supabase.table("profiles").select("*").eq(
            "email", user_data.email
        ).execute()
        
        # DEBUG
        print("=" * 50)
        print(f"EMAIL: {user_data.email}")
        print(f"PROFILE RESULT: {profile_res.data}")
        print("=" * 50)
        
        if not profile_res.data or len(profile_res.data) == 0:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
        
        profile = profile_res.data[0]
        
        # Şifreyi kontrol et
        user_auth_res = supabase.table("user_auth").select("password_hash").eq(
            "user_id", profile["id"]
        ).execute()
        
        if not user_auth_res.data or len(user_auth_res.data) == 0:
            raise HTTPException(status_code=401, detail="Şifre bulunamadı")
        
        user_auth = user_auth_res.data[0]
        
        if not verify_password(user_data.password, user_auth["password_hash"]):
            raise HTTPException(status_code=401, detail="Yanlış şifre")
        
        # Token oluştur
        access_token = create_access_token(
            data={"sub": profile["email"], "user_id": profile["id"]}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": profile
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signin error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# SUBJECTS & TOPICS
# ============================================

@app.get("/api/subjects")
async def get_subjects():
    try:
        result = supabase.table("subjects").select(
            "id, name_tr, class_level_id, class_levels(grade_number)"
        ).eq("is_active", True).execute()
        
        return {"subjects": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/subjects/{subject_id}/topics")
async def get_topics_by_subject(subject_id: str):
    try:
        result = supabase.table("topics").select("*").eq(
            "subject_id", subject_id
        ).eq("is_active", True).execute()
        
        return {"topics": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# EDUCATION LEVELS & CLASS LEVELS
# ============================================

@app.get("/api/education-levels")
async def get_education_levels():
    try:
        result = supabase.table("education_levels").select("*").eq(
            "is_active", True
        ).execute()
        
        return {"education_levels": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/class-levels")
async def get_class_levels():
    try:
        result = supabase.table("class_levels").select("*").eq(
            "is_active", True
        ).order("grade_number").execute()
        
        return {"class_levels": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# STUDENT DASHBOARD
# ============================================

@app.get("/api/students/{student_id}/dashboard")
async def get_student_dashboard(student_id: str):
    try:
        # Student bilgisi
        student = supabase.table("students").select("*").eq(
            "id", student_id
        ).single().execute()
        
        if not student.data:
            raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
        
        # Test sonuçları (ESKİ TABLO YAPISI)
        test_results = supabase.table("test_results").select("*").eq(
            "student_id", student_id
        ).order("created_at", desc=True).limit(10).execute()
        
        # Topic performance yok, boş liste dön
        topic_performance = []
        
        return {
            "student": student.data,
            "recent_tests": test_results.data or [],
            "topic_performance": topic_performance
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Dashboard hatası: {str(e)}")

@app.get("/api/user/{user_id}/student")
async def get_student_by_user(user_id: str):
    """User ID'den student bilgisini al"""
    try:
        result = supabase.table("students").select("*").eq(
            "user_id", user_id
        ).single().execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
        
        # DEBUG
        print("=" * 50)
        print(f"USER ID: {user_id}")
        print(f"STUDENT DATA: {result.data}")
        print(f"STUDENT ID: {result.data['id']}")
        print("=" * 50)
        
        return result.data  # Tüm student nesnesini döndür
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get student error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{student_id}/reports")
async def get_student_reports(student_id: str):
    """Öğrencinin detaylı raporlarını getir (ESKİ TABLO YAPISI)"""
    try:
        # Tüm test sonuçlarını al
        test_results = supabase.table("test_results").select("*").eq(
            "student_id", student_id
        ).order("entry_timestamp", desc=True).execute()
        
        tests = test_results.data or []
        
        if not tests:
            return {
                "overall_stats": {
                    "total_tests": 0,
                    "avg_net": 0,
                    "total_correct": 0,
                    "total_wrong": 0,
                    "total_empty": 0,
                    "success_rate": 0
                },
                "subject_performance": [],
                "topic_performance": [],
                "strong_topics": [],
                "weak_topics": [],
                "recent_tests": []
            }
        
        # Genel istatistikler
        total_tests = len(tests)
        total_net = sum(t.get("net", 0) for t in tests)
        total_correct = sum(t.get("correct_count", 0) for t in tests)
        total_wrong = sum(t.get("wrong_count", 0) for t in tests)
        total_empty = sum(t.get("empty_count", 0) for t in tests)
        
        overall_stats = {
            "total_tests": total_tests,
            "avg_net": round(total_net / total_tests, 2) if total_tests > 0 else 0,
            "total_correct": total_correct,
            "total_wrong": total_wrong,
            "total_empty": total_empty,
            "success_rate": round((total_correct / (total_correct + total_wrong + total_empty) * 100), 1) if (total_correct + total_wrong + total_empty) > 0 else 0
        }
        
        # Ders bazlı performans
        subject_stats = {}
        for test in tests:
            subject = test.get("subject", "Bilinmeyen")
            if subject not in subject_stats:
                subject_stats[subject] = {
                    "test_count": 0,
                    "total_net": 0,
                    "total_correct": 0,
                    "total_wrong": 0,
                    "total_empty": 0
                }
            
            subject_stats[subject]["test_count"] += 1
            subject_stats[subject]["total_net"] += test.get("net", 0)
            subject_stats[subject]["total_correct"] += test.get("correct_count", 0)
            subject_stats[subject]["total_wrong"] += test.get("wrong_count", 0)
            subject_stats[subject]["total_empty"] += test.get("empty_count", 0)
        
        subject_performance = []
        for subject, stats in subject_stats.items():
            total_questions = stats["total_correct"] + stats["total_wrong"] + stats["total_empty"]
            subject_performance.append({
                "subject": subject,
                "test_count": stats["test_count"],
                "avg_net": round(stats["total_net"] / stats["test_count"], 2),
                "total_correct": stats["total_correct"],
                "total_wrong": stats["total_wrong"],
                "total_empty": stats["total_empty"],
                "success_rate": round((stats["total_correct"] / total_questions * 100), 1) if total_questions > 0 else 0
            })
        
        # Konu bazlı performans
        topic_stats = {}
        for test in tests:
            topic = test.get("topic", "Bilinmeyen")
            subject = test.get("subject", "Bilinmeyen")
            key = f"{subject}:{topic}"
            
            if key not in topic_stats:
                topic_stats[key] = {
                    "subject": subject,
                    "topic": topic,
                    "test_count": 0,
                    "total_net": 0,
                    "nets": []
                }
            
            topic_stats[key]["test_count"] += 1
            topic_stats[key]["total_net"] += test.get("net", 0)
            topic_stats[key]["nets"].append(test.get("net", 0))
        
        topic_performance = []
        for key, stats in topic_stats.items():
            avg_net = round(stats["total_net"] / stats["test_count"], 2)
            
            # Trend hesapla (son ile ilk net karşılaştırması)
            trend = 0
            if len(stats["nets"]) >= 2:
                trend = round(stats["nets"][0] - stats["nets"][-1], 1)
            
            topic_performance.append({
                "subject": stats["subject"],
                "topic": stats["topic"],
                "test_count": stats["test_count"],
                "avg_net": avg_net,
                "trend": trend,
                "last_net": stats["nets"][0] if stats["nets"] else 0
            })
        
        # Güçlü ve zayıf konular
        sorted_topics = sorted(topic_performance, key=lambda x: x["avg_net"], reverse=True)
        strong_topics = sorted_topics[:5]
        weak_topics = sorted_topics[-5:][::-1]
        
        # Son testler
        recent_tests = []
        for test in tests[:10]:
            recent_tests.append({
                "id": test["id"],
                "subject": test.get("subject", ""),
                "topic": test.get("topic", ""),
                "net": test.get("net", 0),
                "correct": test.get("correct_count", 0),
                "wrong": test.get("wrong_count", 0),
                "empty": test.get("empty_count", 0),
                "success_rate": test.get("success_rate", 0),
                "date": test.get("entry_timestamp", "")
            })
        
        return {
            "overall_stats": overall_stats,
            "subject_performance": subject_performance,
            "topic_performance": topic_performance,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "recent_tests": recent_tests
        }
        
    except Exception as e:
        print(f"Reports error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# TEST RESULTS
# ============================================

@app.post("/api/test-results")
async def create_test_result(test_data: dict):
    """Test sonucu kaydet (ESKİ TABLO YAPISI)"""
    try:
        # DEBUG
        print("=" * 50)
        print("GELEN TEST VERİSİ:")
        print(test_data)
        print("=" * 50)
        
        # UUID oluştur (test_id için)
        import uuid
        test_uuid = str(uuid.uuid4())
        
        # Yeni test sonucu ekle
        new_test = supabase.table("test_results").insert({
            "student_id": test_data.get("student_id"),
            "test_id": test_uuid,  # ← DÜZELTİLDİ: UUID oluştur
            "subject": test_data.get("subject", ""),
            "topic": test_data.get("topic", ""),
            "correct_count": test_data.get("correct_count", 0),
            "wrong_count": test_data.get("wrong_count", 0),
            "empty_count": test_data.get("empty_count", 0),
            "net": test_data.get("net", 0),
            "success_rate": test_data.get("success_rate", 0),
            "entry_timestamp": test_data.get("entry_timestamp")
        }).execute()
        
        print("SUPABASE CEVABI:")
        print(new_test.data)
        print("=" * 50)
        
        return {
            "success": True,
            "test_id": new_test.data[0]["id"],
            "message": "Test sonucu kaydedildi"
        }
        
    except Exception as e:
        print(f"❌ Test result error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ADMIN - STUDENTS
# ============================================

@app.get("/api/admin/students")
async def get_all_students():
    try:
        result = supabase.table("students").select(
            "*, profiles(email, role)"
        ).order("created_at", desc=True).execute()
        
        return {"students": result.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ADMIN - SUBJECTS
# ============================================

@app.get("/api/admin/subjects")
async def get_all_subjects_admin():
    try:
        result = supabase.table("subjects").select(
            "*, class_levels(grade_number, education_level_id)"
        ).order("name_tr").execute()
        
        return {"subjects": result.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ADMIN - TOPICS
# ============================================

@app.get("/api/admin/topics")
async def get_all_topics_admin():
    try:
        result = supabase.table("topics").select(
            "*, subjects(name_tr, class_levels(grade_number))"
        ).order("name_tr").execute()
        
        return {"topics": result.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/topics")
async def create_topic_admin(topic_data: dict):
    try:
        new_topic = supabase.table("topics").insert(topic_data).execute()
        
        return {
            "success": True,
            "topic": new_topic.data[0],
            "message": "Konu oluşturuldu"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/topics/{topic_id}")
async def update_topic_admin(topic_id: str, topic_data: dict):
    try:
        updated = supabase.table("topics").update(topic_data).eq(
            "id", topic_id
        ).execute()
        
        return {
            "success": True,
            "topic": updated.data[0],
            "message": "Konu güncellendi"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/topics/{topic_id}")
async def delete_topic_admin(topic_id: str):
    try:
        supabase.table("topics").update({"is_active": False}).eq(
            "id", topic_id
        ).execute()
        
        return {
            "success": True,
            "message": "Konu silindi"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ADMIN - EXAM HISTORY
# ============================================

@app.post("/api/admin/exam-history")
async def create_exam_history(exam_data: dict):
    try:
        new_exam = supabase.table("exam_history").insert(exam_data).execute()
        
        return {
            "success": True,
            "exam": new_exam.data[0]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ADMIN - TOPIC-EXAM DATA
# ============================================

@app.post("/api/admin/topic-exam-data")
async def create_topic_exam_data(data: dict):
    try:
        new_data = supabase.table("topic_exam_data").insert(data).execute()
        
        return {
            "success": True,
            "data": new_data.data[0]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ADMIN - STATS
# ============================================

@app.get("/api/admin/stats")
async def get_admin_stats():
    try:
        students = supabase.table("students").select("id", count="exact").execute()
        tests = supabase.table("test_results").select("id", count="exact").execute()
        topics = supabase.table("topics").select("id", count="exact").eq(
            "is_active", True
        ).execute()
        
        return {
            "total_students": students.count,
            "total_tests": tests.count,
            "total_topics": topics.count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ÖSYM TOPICS
# ============================================

@app.get("/api/osym/topics")
async def get_osym_topics(exam_type_id: str = None):
    try:
        query = supabase.table("osym_topics").select(
            "*, exam_types(short_name, name_tr)"
        ).eq("is_active", True)
        
        if exam_type_id:
            query = query.eq("exam_type_id", exam_type_id)
        
        result = query.order("official_name").execute()
        
        return {"osym_topics": result.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/osym-topics")
async def create_osym_topic(topic_data: OsymTopicCreate):
    try:
        new_topic = supabase.table("osym_topics").insert({
            "exam_type_id": topic_data.exam_type_id,
            "official_name": topic_data.official_name,
            "subject_name": topic_data.subject_name,
            "related_grade_levels": topic_data.related_grade_levels,
            "published_year": topic_data.published_year,
            "notes": topic_data.notes,
            "is_active": True
        }).execute()
        
        return {
            "success": True,
            "topic": new_topic.data[0],
            "message": "ÖSYM konusu eklendi"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/osym-topics/bulk-upload")
async def bulk_upload_osym_topics(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        required_cols = ['exam_type_code', 'subject_name', 'official_name']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Eksik kolonlar: {', '.join(missing_cols)}"
            )
        
        exam_types = supabase.table("exam_types").select("id, code").execute()
        exam_type_map = {et["code"]: et["id"] for et in exam_types.data}
        
        success_count = 0
        error_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                exam_type_code = str(row['exam_type_code']).strip().upper()
                
                if exam_type_code not in exam_type_map:
                    errors.append(f"Satır {index + 2}: '{exam_type_code}' sınav türü bulunamadı")
                    error_count += 1
                    continue
                
                exam_type_id = exam_type_map[exam_type_code]
                
                related_grades = []
                for grade in [9, 10, 11, 12]:
                    col_name = f'grade_{grade}'
                    if col_name in df.columns and row[col_name] == 1:
                        related_grades.append(grade)
                
                if not related_grades:
                    related_grades = [9, 10]
                
                supabase.table("osym_topics").insert({
                    "exam_type_id": exam_type_id,
                    "official_name": str(row['official_name']).strip(),
                    "subject_name": str(row['subject_name']).strip(),
                    "related_grade_levels": related_grades,
                    "published_year": 2024,
                    "notes": str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else None,
                    "is_active": True
                }).execute()
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"Satır {index + 2}: {str(e)}")
                error_count += 1
                continue
        
        return {
            "success": True,
            "message": f"{success_count} konu başarıyla eklendi",
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors[:10]
        }
        
    except Exception as e:
        print(f"Bulk upload hatası: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# TOPIC-ÖSYM MAPPING
# ============================================

@app.get("/api/admin/unmapped-topics")
async def get_unmapped_topics(exam_type_id: str = None):
    try:
        all_topics_res = supabase.table("topics").select(
            "id, name_tr, subject_id"
        ).eq("is_active", True).execute()
        
        if not all_topics_res.data:
            return {
                "unmapped_topics": [],
                "total": 0
            }
        
        mapped = supabase.table("topic_osym_mapping").select("meb_topic_id").execute()
        mapped_ids = [m["meb_topic_id"] for m in mapped.data] if mapped.data else []
        
        unmapped = []
        for t in all_topics_res.data:
            if t["id"] not in mapped_ids:
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
        
        return {
            "unmapped_topics": unmapped,
            "total": len(unmapped)
        }
        
    except Exception as e:
        print(f"Get unmapped topics hatası: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/topic-osym-mapping")
async def create_topic_mapping(mapping_data: TopicMappingCreate):
    try:
        new_mapping = supabase.table("topic_osym_mapping").insert({
            "meb_topic_id": mapping_data.meb_topic_id,
            "osym_topic_id": mapping_data.osym_topic_id,
            "match_type": mapping_data.match_type,
            "match_percentage": mapping_data.match_percentage,
            "verified": mapping_data.verified,
            "created_by": mapping_data.created_by
        }).execute()
        
        return {
            "success": True,
            "mapping": new_mapping.data[0],
            "message": "Eşleştirme oluşturuldu"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)