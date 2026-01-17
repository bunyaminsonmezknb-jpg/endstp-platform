from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.db.session import get_db

from .engine import run_time_engine
from .types import TimeEngineInput, TimeTopicInput

router = APIRouter(prefix="/student/motors/time", tags=["Time Motor"])


@router.get("")
def time_adapter(
    student=Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Time / Pace Motor Adapter (FAZ 4B)
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
            avg_time_sec,
            success_rate,
            test_count,
            last_test_date
        FROM student_topic_summary
        WHERE student_id = :student_id
        """,
        {"student_id": student.id},
    ).mappings().all()

    topics: list[TimeTopicInput] = []
    for r in rows:
        topics.append(
            TimeTopicInput(
                topic_id=str(r.get("topic_id")),
                topic_name=str(r.get("topic_name") or ""),
                subject_name=str(r.get("subject_name") or ""),
                avg_time_sec=r.get("avg_time_sec"),
                success_rate=r.get("success_rate"),
                test_count=r.get("test_count"),
                last_test_date=r.get("last_test_date"),
            )
        )

    payload = TimeEngineInput(topics=topics)
    return run_time_engine(payload)
