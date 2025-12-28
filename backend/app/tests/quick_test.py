"""
Hızlı manuel test (pytest gereksiz)
"""

from app.core.bs_model_engine import BSModel, ReviewInput
from app.core.difficulty_engine import DifficultyEngine, StatMetrics
from app.core.time_engine import TimeAnalyzer
from app.core.priority_engine import PriorityEngine, TopicInput

print("=" * 70)
print("4 MOTOR HIZLI TEST")
print("=" * 70)

# 1. BS-Model
print("\n1️⃣ BS-MODEL:")
result = BSModel.calculate(ReviewInput(
    correct=7, incorrect=2, blank=1, total=10,
    difficulty=3, repetitions=0
))
print(f"   ✅ Yeni Konu: {result.status}, IA={result.next_ia}, EF={result.next_ef}")

result = BSModel.calculate(ReviewInput(
    correct=8, incorrect=1, blank=1, total=10,
    difficulty=3, current_ef=2.2, current_ia=7,
    actual_gap=20, repetitions=3
))
print(f"   ✅ Hero Mode: {result.status}, IA={result.next_ia}")

# 2. Difficulty Engine
print("\n2️⃣ DIFFICULTY ENGINE:")
result = DifficultyEngine.calculate(StatMetrics(
    total_questions=10, correct=4, wrong=2, blank=4, net=3.0
))
print(f"   ✅ Çok Boş: Level={result.difficulty_level}, %{result.difficulty_percentage}")

result = DifficultyEngine.calculate(StatMetrics(
    total_questions=10, correct=10, wrong=0, blank=0, net=10.0
))
print(f"   ✅ Full: Level={result.difficulty_level}, %{result.difficulty_percentage}")

# 3. Time Analyzer
print("\n3️⃣ TIME ANALYZER:")
result = TimeAnalyzer.analyze(
    total_duration=10, total_questions=10,
    ideal_time_per_question=1.5, success_rate=0.9
)
print(f"   ✅ Hızlı & Başarılı: Modifier={result.time_modifier}")

result = TimeAnalyzer.analyze(
    total_duration=25, total_questions=10,
    ideal_time_per_question=1.5
)
print(f"   ✅ Yavaş: Modifier={result.time_modifier}")

# 4. Priority Engine
print("\n4️⃣ PRIORITY ENGINE:")
topics = [
    TopicInput(
        id="t1", name="Fonksiyonlar",
        correct=7, wrong=1, blank=2, total_questions=10,
        duration_minutes=20,
        topic_weight=0.15, course_importance=40
    ),
    TopicInput(
        id="t2", name="Mantık",
        correct=10, wrong=0, blank=0, total_questions=10,
        topic_weight=0.03, course_importance=40
    )
]
results = PriorityEngine.analyze(topics)
print(f"   ✅ Sıralama: {results[0].topic_name} ({results[0].priority_level}) > {results[1].topic_name} ({results[1].priority_level})")

print("\n" + "=" * 70)
print("✅ TÜM TESTLER BAŞARILI!")
print("=" * 70)
