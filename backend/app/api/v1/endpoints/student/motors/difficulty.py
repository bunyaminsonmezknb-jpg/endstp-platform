# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/endpoints/student/motors/difficulty.py
# Created: 2026-01-17
# Phase: FAZ 4B
# Author: End.STP Team
# =============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.db.session import get_db

from app.motors.difficulty.engine import run_difficulty_engine
from app.motors.difficulty.types import (
    DifficultyEngineInput,
    DifficultyTopicInput,
)

router = APIRouter(
    prefix="/student/motors/difficulty",
    tags=["Difficulty Motor"],
)


@router.get("")
def difficulty_adapter(
    student=Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Difficulty Motor Adapter (FAZ 4B)
    """

    rows = db.execute(
        """
        SELECT
            topic_id,
            topic_name,
            subject_name,
            success_rate,
            wrong_rate,
            blank_rate,
            test_count,
            avg_time_sec,
            last_test_date
        FROM student_topic_summary
        WHERE student_id = :student_id
        """,
        {"student_id": student.id},
    ).mappings().all()

    topics = [
        DifficultyTopicInput(
            topic_id=str(r["topic_id"]),
            topic_name=r["topic_name"] or "",
            subject_name=r["subject_name"] or "",
            success_rate=r["success_rate"],
            wrong_rate=r["wrong_rate"],
            blank_rate=r["blank_rate"],
            test_count=r["test_count"],
            avg_time_sec=r["avg_time_sec"],
            last_test_date=r["last_test_date"],
        )
        for r in rows
    ]

    payload = DifficultyEngineInput(topics=topics)
    return run_difficulty_engine(payload)
