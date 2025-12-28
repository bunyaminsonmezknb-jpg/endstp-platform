import time
from app.core.difficulty_engine import calculate_difficulty_score

# Mock test data
tests = [
    {
        "test_date": "2024-12-28",
        "total_questions": 10,
        "correct_count": 7,
        "wrong_count": 2,
        "blank_count": 1,
        "success_rate": 70
    }
]

# 1000 iteration benchmark
start = time.perf_counter()
for _ in range(1000):
    result = calculate_difficulty_score(tests, 5)
end = time.perf_counter()

avg_ms = ((end - start) / 1000) * 1000
print(f"✅ Average time per call: {avg_ms:.3f}ms")
print(f"✅ Target: <50ms")
print(f"✅ Status: {'PASS' if avg_ms < 50 else 'FAIL'}")
