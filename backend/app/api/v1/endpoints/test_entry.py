"""
Test Entry Endpoints
Öğrenci test girişi için API'ler
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

# Ortam değişkenlerini yükle (Garanti olsun)
load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)

# ============================================
# SERVICE ROLE CLIENT OLUŞTURUCU (Yerel ve Güvenli)
# ============================================
def get_force_admin_client() -> Client:
    """
    Dışarıdan import edilen session'a güvenmek yerine,
    Admin yetkisini doğrudan burada oluşturuyoruz.
    """
    url = os.getenv("SUPABASE_URL")
    # BURASI KRİTİK: Service Key'i doğrudan çekiyoruz
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        logger.error("Supabase credentials eksik! .env dosyasını kontrol et.")
        raise HTTPException(
            status_code=500, 
            detail="Sunucu yapılandırma hatası: Admin anahtarı bulunamadı."
        )
        
    return create_client(url, key)

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class TestResultSubmit(BaseModel):
    student_id: str
    subject_id: str
    topic_id: str
    test_date: str  # ISO format: "2025-11-24T14:30:00"
    correct_count: int
    wrong_count: int
    empty_count: int
    net_score: float
    success_rate: float


# ============================================
# GET /api/v1/subjects
# ============================================

@router.get("/subjects")
async def get_subjects():
    """
    Tüm dersleri listele
    Frontend dropdown için
    """
    # Admin yetkisiyle bağlan
    supabase = get_force_admin_client()
    
    try:
        result = supabase.table("subjects").select(
            "id, code, name_tr, icon, color"
        ).eq("is_active", True).order("name_tr").execute()
        
        return result.data
    except Exception as e:
        logger.error(f"Subjects Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# GET /api/v1/subjects/{subject_id}/topics
# ============================================

@router.get("/subjects/{subject_id}/topics")
async def get_topics_by_subject(subject_id: str):
    """
    Bir derse ait konuları listele
    Frontend dropdown için
    """
    # Admin yetkisiyle bağlan
    supabase = get_force_admin_client()
    
    try:
        result = supabase.table("topics").select(
            "id, code, name_tr, difficulty_level, exam_weight"
        ).eq("subject_id", subject_id).eq("is_active", True).order("name_tr").execute()
        
        return result.data
    except Exception as e:
        logger.error(f"Topics Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# POST /api/v1/test-results
# ============================================

@router.post("/test-results")
async def submit_test_result(
    test_data: TestResultSubmit,
    authorization: Optional[str] = Header(None)
):
    """
    Test sonucu kaydet
    """
    # RLS Bypass için Service Role Key kullanan yerel client'ı çağır
    supabase = get_force_admin_client()
    
    try:
        # Debug: Hangi tabloya yazmaya çalıştığımızı görelim
        print(f"DEBUG: 'student_topic_tests' tablosuna yazılıyor...")
        
        # Total questions check (Opsiyonel validasyon)
        total_questions = test_data.correct_count + test_data.wrong_count + test_data.empty_count
        
        # Insert test result (Senin yapın birebir korundu)
        test_record = {
            "student_id": test_data.student_id,
            "subject_id": test_data.subject_id,
            "topic_id": test_data.topic_id,
            "test_date": test_data.test_date,
            "correct_count": test_data.correct_count,
            "wrong_count": test_data.wrong_count,
            "empty_count": test_data.empty_count,
            "net_score": test_data.net_score,
            "success_rate": test_data.success_rate,
            # Sistem alanları
            "is_processed": False,
            "processing_status": "pending",
            "test_source": "web_form",
            "question_type": "multiple_choice",
            "created_via": "web_form",
            "api_version": "v1",
            "request_id": str(uuid.uuid4()),
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Yazma İşlemi
        result = supabase.table("student_topic_tests").insert(test_record).execute()
        
        # Supabase bazen boş data dönebilir ama hata vermezse başarılıdır.
        # Yine de kontrol edelim.
        if not result.data:
            # Data boşsa ama hata yoksa, insert başarılı olabilir ama return policy kapalıdır.
            # RLS insert'e izin verir ama select'e izin vermezse data boş döner.
            # Admin olduğumuz için data dönmeli. Dönmüyorsa bir gariplik vardır.
            logger.warning("Insert yapıldı ama data boş döndü.")
            
            # ID'yi manuel alamayabiliriz bu durumda ama işlem başarılı sayılabilir.
            return {
                "success": True,
                "message": "Test kaydedildi (Data dönüşü yok)",
                "net_score": test_data.net_score
            }
        
        return {
            "success": True,
            "message": "Test başarıyla kaydedildi",
            "test_id": result.data[0].get("id"),
            "net_score": test_data.net_score
        }
        
    except Exception as e:
        logger.error(f"Test submit error: {str(e)}")
        print(f"CRITICAL ERROR: {str(e)}") # Konsolda kırmızı alarm
        raise HTTPException(
            status_code=500, 
            detail=f"Veritabanı hatası: {str(e)}"
        )