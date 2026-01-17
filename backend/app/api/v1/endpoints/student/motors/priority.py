# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/endpoints/student/motors/priority.py
# Created: 2026-01-17
# Phase: FAZ 4B (Unified Motor Architecture)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [x] Database uses _tr/_en columns (where applicable)
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded UI text (API response is machine-readable)
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - None
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - Consider Accept-Language & reason message localization
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
# =============================================================================

"""
Priority Motor Endpoint (FAZ 4B)

- Auth enforced (student)
- DB snapshot fetch
- Builds typed PriorityEngineInput
- Calls pure engine: app.motors.priority.engine.run_priority_engine
- Returns typed engine output (JSON-serializable)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.db.session import get_db

from app.motors.priority.engine import run_priority_engine
from app.motors.priority.types import PriorityEngineInput, PriorityTopicInput

router = APIRouter(prefix="/student/motors/priority", tags=["Priority Motor"])


@router.get("")
def get_priority(
    student=Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Returns priority ranking for student's topics.
    """
    rows = db.execute(
        """
        SELECT
            topic_id,
            topic_name,
            subject_name,
            success_rate,
            test_count,
            last_test_date,
            trend
        FROM student_topic_summary
        WHERE student_id = :student_id
        """,
        {"student_id": student.id},
    ).mappings().all()

    topics: list[PriorityTopicInput] = []
    for r in rows:
        topics.append(
            PriorityTopicInput(
                topic_id=str(r.get("topic_id")),
                topic_name=str(r.get("topic_name") or ""),
                subject_name=str(r.get("subject_name") or ""),
                success_rate=r.get("success_rate"),
                test_count=r.get("test_count"),
                last_test_date=r.get("last_test_date"),
                trend=r.get("trend"),
            )
        )

    payload = PriorityEngineInput(topics=topics)
    return run_priority_engine(payload)
