# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: {FILENAME}
# Created: {DATE}
# Phase: MVP (Phase 1)
# Author: End.STP Team
# 
# 🌍 LOCALIZATION STATUS:
#   [ ] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [ ] No hardcoded text
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - (None yet - Add items as you code)
#   - Example: "TURKISH_MONTHS dict (Line 45) → Phase 2: Database lookup"
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - (Actions will be listed here)
#   - Example: "Replace format_date_turkish() with format_date_localized()"
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
#   - Migration: docs/PHASE2_MIGRATION_PLAN.md
# =============================================================================

"""
{FILENAME} - {SHORT_DESCRIPTION}

{DETAILED_DESCRIPTION}

Usage:
    {USAGE_EXAMPLE}
"""

from datetime import datetime, timezone  # ⚠️ ALWAYS use timezone.utc!
from typing import List, Dict, Any, Optional

# =============================================================================
# YOUR CODE STARTS HERE
# =============================================================================

# TODO: Implement your functions
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.db.session import get_db

from app.motors.orchestrator import run_unified_motors
from app.motors.priority.types import PriorityEngineInput, PriorityTopicInput
from app.motors.difficulty.types import DifficultyEngineInput, DifficultyTopicInput
from app.motors.time_pace.types import TimeEngineInput, TimeTopicInput

router = APIRouter(
    prefix="/student/motors/unified",
    tags=["Unified Motor"],
)


@router.get("")
def unified_motor_adapter(
    student=Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Unified Motor Adapter (FAZ 4B)
    -----------------------------
    - Auth (student)
    - DB snapshot fetch
    - Motor payload build
    - Unified orchestrator call
    """

    rows = db.execute(
        """
        SELECT
            topic_id,
            topic_name,
            subject_name,

            -- common
            success_rate,
            progress_percent,
            test_count,
            last_test_date,
            trend,

            -- difficulty
            wrong_rate,
            blank_rate,

            -- time / pace
            avg_time_sec,

            -- BS-model
            bs_due,
            bs_overdue_days,
            bs_remembering_rate
        FROM student_topic_summary
        WHERE student_id = :student_id
        """,
        {"student_id": student.id},
    ).mappings().all()

    # ============================
    # PRIORITY PAYLOAD
    # ============================
    priority_topics = [
        PriorityTopicInput(
            topic_id=str(r["topic_id"]),
            topic_name=r["topic_name"],
            subject_name=r["subject_name"],
            success_rate=r["success_rate"],
            test_count=r["test_count"],
            last_test_date=r["last_test_date"],
            trend=r["trend"],
        )
        for r in rows
    ]

    priority_payload = PriorityEngineInput(topics=priority_topics)

    # ============================
    # DIFFICULTY PAYLOAD
    # ============================
    difficulty_topics = [
        DifficultyTopicInput(
            topic_id=str(r["topic_id"]),
            topic_name=r["topic_name"],
            subject_name=r["subject_name"],
            success_rate=r["success_rate"],
            wrong_rate=r["wrong_rate"],
            blank_rate=r["blank_rate"],
            test_count=r["test_count"],
            avg_time_sec=r["avg_time_sec"],
            last_test_date=r["last_test_date"],
        )
        for r in rows
    ]

    difficulty_payload = DifficultyEngineInput(topics=difficulty_topics)

    # ============================
    # TIME / PACE PAYLOAD
    # ============================
    time_topics = [
        TimeTopicInput(
            topic_id=str(r["topic_id"]),
            topic_name=r["topic_name"],
            subject_name=r["subject_name"],
            avg_time_sec=r["avg_time_sec"],
            success_rate=r["success_rate"],
            test_count=r["test_count"],
            last_test_date=r["last_test_date"],
        )
        for r in rows
    ]

    time_payload = TimeEngineInput(topics=time_topics)

    # ============================
    # UNIFIED ORCHESTRATOR
    # ============================
    return run_unified_motors(
        priority_payload=priority_payload,
        difficulty_payload=difficulty_payload,
        time_payload=time_payload,
    )
