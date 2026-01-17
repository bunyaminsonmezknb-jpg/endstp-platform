from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.db.session import get_db

from .engine import run_difficulty_engine
from .types import DifficultyEngineInput, DifficultyTopicInput

router = APIRouter(prefix="/student/motors/difficulty", tags=["Difficulty Motor"])


@router.get("")
def difficulty_adapter(
    student=Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Difficulty Motor Adapter (FAZ 4B)
    - Auth
    - DB fetch
    - Payload build
    - Engine call
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

    topics: list[DifficultyTopicInput] = []
    for r in rows:
        topics.append(
            DifficultyTopicInput(
                topic_id=str(r.get("topic_id")),
                topic_name=str(r.get("topic_name") or ""),
                subject_name=str(r.get("subject_name") or ""),
                success_rate=r.get("success_rate"),
                wrong_rate=r.get("wrong_rate"),
                blank_rate=r.get("blank_rate"),
                test_count=r.get("test_count"),
                avg_time_sec=r.get("avg_time_sec"),
                last_test_date=r.get("last_test_date"),
            )
        )

    payload = DifficultyEngineInput(topics=topics)
    return run_difficulty_engine(payload)
