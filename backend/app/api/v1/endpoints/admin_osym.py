"""
Admin ÖSYM API Endpoints
- ÖSYM resmi konularını yönetme
- MEB-ÖSYM konu eşleştirme
- Toplu Excel yükleme
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_active_superuser
from pydantic import BaseModel
import pandas as pd
from datetime import datetime

router = APIRouter()


# ============= SCHEMAS =============

class OsymTopicCreate(BaseModel):
    exam_type_id: str
    official_name: str
    subject_name: str
    related_grade_levels: List[int]
    published_year: int = 2024


class OsymTopicResponse(BaseModel):
    id: str
    official_name: str
    subject_name: str
    exam_type_id: str
    related_grade_levels: List[int]
    published_year: int
    exam_types: dict
    
    class Config:
        from_attributes = True


class TopicOsymMappingCreate(BaseModel):
    meb_topic_id: str
    osym_topic_id: str
    match_type: str  # 'exact' or 'partial'
    match_percentage: int
    verified: bool = True
    created_by: str


class UnmappedTopicResponse(BaseModel):
    id: str
    name: str
    subject: str
    grade: int


class BulkUploadResponse(BaseModel):
    success: bool
    success_count: int
    error_count: int
    errors: List[str] = []


# ============= ENDPOINTS =============

@router.get("/osym/topics", response_model=dict)
async def get_osym_topics(
    exam_type_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    ÖSYM resmi konularını listele
    """
    query = """
        SELECT 
            ot.id,
            ot.official_name,
            ot.subject_name,
            ot.exam_type_id,
            ot.related_grade_levels,
            ot.published_year,
            json_build_object(
                'short_name', et.short_name,
                'code', et.code
            ) as exam_types
        FROM osym_topics ot
        JOIN exam_types et ON ot.exam_type_id = et.id
        WHERE ot.is_active = true
    """
    
    if exam_type_id:
        query += f" AND ot.exam_type_id = '{exam_type_id}'"
    
    query += " ORDER BY ot.subject_name, ot.official_name"
    
    result = db.execute(query)
    topics = [dict(row) for row in result]
    
    return {
        "osym_topics": topics,
        "total": len(topics)
    }


@router.post("/admin/osym-topics", response_model=dict)
async def create_osym_topic(
    topic: OsymTopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Yeni ÖSYM konusu ekle (tekli)
    """
    query = """
        INSERT INTO osym_topics (
            id, exam_type_id, official_name, subject_name,
            related_grade_levels, published_year, is_active, created_at
        ) VALUES (
            gen_random_uuid(), :exam_type_id, :official_name, :subject_name,
            :grade_levels, :published_year, true, NOW()
        )
        RETURNING id, official_name
    """
    
    result = db.execute(
        query,
        {
            "exam_type_id": topic.exam_type_id,
            "official_name": topic.official_name,
            "subject_name": topic.subject_name,
            "grade_levels": topic.related_grade_levels,
            "published_year": topic.published_year
        }
    )
    db.commit()
    
    row = result.fetchone()
    
    return {
        "success": True,
        "id": str(row[0]),
        "official_name": row[1],
        "message": "ÖSYM konusu eklendi"
    }


@router.post("/admin/osym-topics/bulk-upload", response_model=BulkUploadResponse)
async def bulk_upload_osym_topics(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Excel/CSV ile toplu ÖSYM konusu yükle
    
    Excel formatı:
    - exam_type_code (TYT/AYT)
    - official_name
    - subject_name
    - grade_levels (virgülle ayrılmış: "11,12")
    - published_year
    """
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Sadece Excel veya CSV dosyası yükleyebilirsiniz")
    
    try:
        # Dosyayı oku
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        success_count = 0
        error_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Exam type ID bul
                exam_type_query = "SELECT id FROM exam_types WHERE code = :code"
                exam_type_result = db.execute(exam_type_query, {"code": row['exam_type_code']})
                exam_type = exam_type_result.fetchone()
                
                if not exam_type:
                    errors.append(f"Satır {index+2}: Sınav türü bulunamadı: {row['exam_type_code']}")
                    error_count += 1
                    continue
                
                # Grade levels parse et
                grade_levels = [int(g.strip()) for g in str(row['grade_levels']).split(',')]
                
                # Insert
                insert_query = """
                    INSERT INTO osym_topics (
                        id, exam_type_id, official_name, subject_name,
                        related_grade_levels, published_year, is_active, created_at
                    ) VALUES (
                        gen_random_uuid(), :exam_type_id, :official_name, :subject_name,
                        :grade_levels, :published_year, true, NOW()
                    )
                """
                
                db.execute(
                    insert_query,
                    {
                        "exam_type_id": str(exam_type[0]),
                        "official_name": row['official_name'],
                        "subject_name": row['subject_name'],
                        "grade_levels": grade_levels,
                        "published_year": int(row.get('published_year', 2024))
                    }
                )
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"Satır {index+2}: {str(e)}")
                error_count += 1
        
        db.commit()
        
        return BulkUploadResponse(
            success=success_count > 0,
            success_count=success_count,
            error_count=error_count,
            errors=errors[:10]  # İlk 10 hatayı göster
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya işleme hatası: {str(e)}")


@router.get("/admin/unmapped-topics", response_model=dict)
async def get_unmapped_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    ÖSYM ile eşleştirilmemiş MEB konularını listele
    """
    query = """
        SELECT 
            t.id,
            t.name_tr as name,
            s.name_tr as subject,
            t.grade_level as grade
        FROM topics t
        JOIN subjects s ON t.subject_id = s.id
        WHERE t.id NOT IN (
            SELECT meb_topic_id FROM topic_osym_mappings WHERE is_active = true
        )
        AND t.is_active = true
        ORDER BY s.name_tr, t.grade_level, t.name_tr
        LIMIT 100
    """
    
    result = db.execute(query)
    topics = [dict(row) for row in result]
    
    return {
        "unmapped_topics": topics,
        "total": len(topics)
    }


@router.post("/admin/topic-osym-mapping", response_model=dict)
async def create_topic_osym_mapping(
    mapping: TopicOsymMappingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    MEB konusu ile ÖSYM konusunu eşleştir
    """
    query = """
        INSERT INTO topic_osym_mappings (
            id, meb_topic_id, osym_topic_id, match_type,
            match_percentage, verified, created_by, created_at, is_active
        ) VALUES (
            gen_random_uuid(), :meb_topic_id, :osym_topic_id, :match_type,
            :match_percentage, :verified, :created_by, NOW(), true
        )
        RETURNING id
    """
    
    result = db.execute(
        query,
        {
            "meb_topic_id": mapping.meb_topic_id,
            "osym_topic_id": mapping.osym_topic_id,
            "match_type": mapping.match_type,
            "match_percentage": mapping.match_percentage,
            "verified": mapping.verified,
            "created_by": mapping.created_by
        }
    )
    db.commit()
    
    row = result.fetchone()
    
    return {
        "success": True,
        "mapping_id": str(row[0]),
        "message": "Eşleştirme oluşturuldu"
    }
