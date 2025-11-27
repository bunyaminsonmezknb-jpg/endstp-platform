"""
Admin Exams API Endpoints
- Konulara yıllık sınav verisi ekleme
- Yıllık istatistikleri görüntüleme
- Ana/Tali konu ayrımı
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_active_superuser
from pydantic import BaseModel

router = APIRouter()


# ============= SCHEMAS =============

class TopicYearlyDataCreate(BaseModel):
    topic_id: str
    exam_system_id: str
    year: int
    primary_questions: int = 0
    secondary_questions: int = 0
    question_numbers: List[int] = []
    notes: Optional[str] = None


class YearlyStatsResponse(BaseModel):
    year: int
    primary_questions: int
    secondary_questions: int
    total_questions: int
    question_numbers: List[int]
    notes: Optional[str] = None


# ============= ENDPOINTS =============

@router.post("/admin/topic-yearly-data", response_model=dict)
async def create_topic_yearly_data(
    data: TopicYearlyDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Konuya yıllık sınav verisi ekle
    
    - Ana konu soru sayısı
    - Tali konu soru sayısı
    - Soru numaraları
    """
    
    # Önce exam_history var mı kontrol et
    exam_history_query = """
        SELECT id FROM exam_history 
        WHERE exam_system_id = :exam_system_id 
        AND year = :year
        LIMIT 1
    """
    
    exam_history = db.execute(
        exam_history_query,
        {"exam_system_id": data.exam_system_id, "year": data.year}
    ).fetchone()
    
    # Yoksa oluştur
    if not exam_history:
        create_exam_history = """
            INSERT INTO exam_history (
                id, exam_system_id, year, exam_date, 
                total_questions, created_at
            ) VALUES (
                gen_random_uuid(), :exam_system_id, :year, 
                make_date(:year, 6, 15), 40, NOW()
            )
            RETURNING id
        """
        
        result = db.execute(
            create_exam_history,
            {"exam_system_id": data.exam_system_id, "year": data.year}
        )
        exam_history_id = result.fetchone()[0]
    else:
        exam_history_id = exam_history[0]
    
    # Şimdi topic_yearly_stats'a ekle
    insert_query = """
        INSERT INTO topic_yearly_stats (
            id, topic_id, exam_history_id, year,
            primary_questions, secondary_questions, total_questions,
            question_numbers, notes, created_at, updated_at
        ) VALUES (
            gen_random_uuid(), :topic_id, :exam_history_id, :year,
            :primary_questions, :secondary_questions, :total_questions,
            :question_numbers, :notes, NOW(), NOW()
        )
        ON CONFLICT (topic_id, exam_history_id) 
        DO UPDATE SET
            primary_questions = EXCLUDED.primary_questions,
            secondary_questions = EXCLUDED.secondary_questions,
            total_questions = EXCLUDED.total_questions,
            question_numbers = EXCLUDED.question_numbers,
            notes = EXCLUDED.notes,
            updated_at = NOW()
        RETURNING id
    """
    
    total_questions = data.primary_questions + data.secondary_questions
    
    result = db.execute(
        insert_query,
        {
            "topic_id": data.topic_id,
            "exam_history_id": str(exam_history_id),
            "year": data.year,
            "primary_questions": data.primary_questions,
            "secondary_questions": data.secondary_questions,
            "total_questions": total_questions,
            "question_numbers": data.question_numbers,
            "notes": data.notes
        }
    )
    
    db.commit()
    
    row = result.fetchone()
    
    return {
        "success": True,
        "id": str(row[0]),
        "message": f"{data.year} yılı için veri eklendi"
    }


@router.get("/admin/topics/{topic_id}/yearly-stats", response_model=dict)
async def get_topic_yearly_stats(
    topic_id: str,
    exam_system_id: str = Query(..., description="Sınav sistemi ID (YKS vb.)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Konunun yıllık istatistiklerini getir
    
    - Her yıl için ana/tali soru sayısı
    - Soru numaraları
    - Notlar
    """
    
    query = """
        SELECT 
            tys.year,
            tys.primary_questions,
            tys.secondary_questions,
            tys.total_questions,
            tys.question_numbers,
            tys.notes
        FROM topic_yearly_stats tys
        JOIN exam_history eh ON tys.exam_history_id = eh.id
        WHERE tys.topic_id = :topic_id
        AND eh.exam_system_id = :exam_system_id
        ORDER BY tys.year DESC
    """
    
    result = db.execute(
        query,
        {"topic_id": topic_id, "exam_system_id": exam_system_id}
    )
    
    stats = []
    for row in result:
        stats.append({
            "year": row[0],
            "primary_questions": row[1],
            "secondary_questions": row[2],
            "total_questions": row[3],
            "question_numbers": row[4] or [],
            "notes": row[5]
        })
    
    return {
        "stats": stats,
        "total_years": len(stats)
    }


@router.get("/admin/exam-systems", response_model=dict)
async def get_exam_systems(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Sınav sistemlerini listele (YKS, LGS vb.)
    """
    query = """
        SELECT 
            id, 
            code, 
            name_tr, 
            description
        FROM exam_systems
        WHERE is_active = true
        ORDER BY name_tr
    """
    
    result = db.execute(query)
    systems = [dict(row) for row in result]
    
    return {
        "exam_systems": systems,
        "total": len(systems)
    }
