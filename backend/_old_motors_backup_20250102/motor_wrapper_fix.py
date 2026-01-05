# Motor wrapper v2 için test data oluştur

# Mock test data
from datetime import datetime, timezone

mock_tests = [
    {
        "test_id": "mock-test-1",
        "attempt_date": datetime.now(timezone.utc),
        "questions_total": 10,
        "questions_correct": 7,
        "questions_wrong": 2,
        "questions_blank": 1,
        "time_spent_seconds": 480,
        "success_rate": 70.0
    }
]
