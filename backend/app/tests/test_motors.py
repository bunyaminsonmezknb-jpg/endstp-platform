"""
4 Motor için birim testler
pytest ile çalıştırılır: pytest app/tests/test_motors.py -v
"""

import pytest
from datetime import datetime, timedelta
from app.core.bs_model_engine import BSModel, ReviewInput
from app.core.difficulty_engine import DifficultyEngine, StatMetrics
from app.core.time_engine import TimeAnalyzer
from app.core.priority_engine import PriorityEngine, TopicInput


class TestBSModel:
    """BS-Model testleri"""
    
    def test_new_topic(self):
        """Yeni konu testi"""
        result = BSModel.calculate(ReviewInput(
            correct=7, incorrect=2, blank=1, total=10,
            difficulty=3, repetitions=0
        ))
        assert result.status == "NEW"
        assert result.next_ia == 1
        assert result.next_ef == 2.2  # 2.5 - (3 * 0.1)
        assert result.next_repetition == 1
    
    def test_hero_mode(self):
        """Hero mode testi"""
        result = BSModel.calculate(ReviewInput(
            correct=8, incorrect=1, blank=1, total=10,
            difficulty=3, current_ef=2.2, current_ia=7,
            actual_gap=20, repetitions=3
        ))
        assert result.status == "HERO"
        assert result.next_ia > 20  # Gecikmeyi ödüllendir
        assert result.score > 0.6
    
    def test_reset_mode(self):
        """Reset mode testi"""
        result = BSModel.calculate(ReviewInput(
            correct=3, incorrect=5, blank=2, total=10,
            difficulty=4, current_ef=2.0, current_ia=7,
            actual_gap=25, repetitions=3
        ))
        assert result.status == "RESET"
        assert result.next_ia == 1
        assert result.next_ef == 1.3
        assert result.next_repetition == 1
    
    def test_normal_mode(self):
        """Normal mode testi"""
        result = BSModel.calculate(ReviewInput(
            correct=7, incorrect=2, blank=1, total=10,
            difficulty=3, current_ef=2.2, current_ia=6,
            actual_gap=7, repetitions=2
        ))
        assert result.status == "NORMAL"
        assert result.next_ia > 6
        assert result.next_ef > 0


class TestDifficultyEngine:
    """Difficulty Engine testleri"""
    
    def test_high_blank_rate(self):
        """Yüksek boş oranı testi"""
        result = DifficultyEngine.calculate(StatMetrics(
            total_questions=10, correct=4, wrong=2, blank=4, net=3.0
        ))
        assert result.difficulty_level >= 2
        assert "Boş" in result.analysis or "boş" in result.analysis.lower()
    
    def test_high_wrong_rate(self):
        """Yüksek yanlış oranı testi"""
        result = DifficultyEngine.calculate(StatMetrics(
            total_questions=10, correct=2, wrong=8, blank=0, net=-4.0
        ))
        assert result.difficulty_level >= 2
    
    def test_perfect_score(self):
        """Mükemmel skor testi"""
        result = DifficultyEngine.calculate(StatMetrics(
            total_questions=10, correct=10, wrong=0, blank=0, net=10.0
        ))
        assert result.difficulty_level == 1
        assert result.difficulty_percentage == 0.0
    
    def test_with_course_context(self):
        """Course context testi"""
        topic = StatMetrics(
            total_questions=10, correct=4, wrong=2, blank=4, net=3.0
        )
        course = StatMetrics(
            total_questions=100, correct=60, wrong=20, blank=20, net=50.0
        )
        result = DifficultyEngine.calculate(topic, course)
        assert result.factors["context_stress"] > 0


class TestTimeAnalyzer:
    """Time Analyzer testleri"""
    
    def test_fast_and_successful(self):
        """Hızlı ve başarılı testi"""
        result = TimeAnalyzer.analyze(
            total_duration=10, total_questions=10,
            ideal_time_per_question=1.5, success_rate=0.9
        )
        assert result.is_fast is True
        assert result.time_modifier == 0.9
    
    def test_fast_but_failed(self):
        """Hızlı ama başarısız testi"""
        result = TimeAnalyzer.analyze(
            total_duration=10, total_questions=10,
            ideal_time_per_question=1.5, success_rate=0.4
        )
        assert result.is_fast is True
        assert result.time_modifier == 1.0  # Ceza yok
    
    def test_slow(self):
        """Yavaş testi"""
        result = TimeAnalyzer.analyze(
            total_duration=25, total_questions=10,
            ideal_time_per_question=1.5
        )
        assert result.is_slow is True
        assert result.time_modifier == 1.15
    
    def test_no_duration(self):
        """Süre yok testi"""
        result = TimeAnalyzer.analyze(
            total_duration=None, total_questions=10
        )
        assert result.time_modifier == 1.0
        assert result.pace_ratio == 1.0


class TestPriorityEngine:
    """Priority Engine testleri"""
    
    def test_high_priority_topic(self):
        """Yüksek öncelikli konu testi"""
        topics = [
            TopicInput(
                id="t1", name="Fonksiyonlar",
                correct=5, wrong=3, blank=2, total_questions=10,
                topic_weight=0.15, course_importance=40
            ),
            TopicInput(
                id="t2", name="Mantık",
                correct=10, wrong=0, blank=0, total_questions=10,
                topic_weight=0.03, course_importance=40
            )
        ]
        results = PriorityEngine.analyze(topics)
        assert len(results) == 2
        assert results[0].topic_name == "Fonksiyonlar"  # En yüksek öncelik
        assert results[0].priority_score > results[1].priority_score
    
    def test_speed_penalty(self):
        """Hız cezası testi"""
        topics = [
            TopicInput(
                id="t1", name="Test",
                correct=7, wrong=2, blank=1, total_questions=10,
                duration_minutes=25,  # Yavaş
                topic_weight=0.1, course_importance=40
            )
        ]
        results = PriorityEngine.analyze(topics)
        assert results[0].analysis["speed_factor"] == 1.25
        assert "hız" in results[0].suggestion.lower()
    
    def test_absolute_threshold(self):
        """Absolute threshold testi"""
        # İyi öğrenci
        topics = [
            TopicInput(
                id="g1", name="Kolay",
                correct=9, wrong=1, blank=0, total_questions=10,
                topic_weight=0.05, course_importance=40
            ),
            TopicInput(
                id="g2", name="Daha Kolay",
                correct=10, wrong=0, blank=0, total_questions=10,
                topic_weight=0.03, course_importance=40
            )
        ]
        results = PriorityEngine.analyze(topics)
        # İyi öğrenci için LOW çıkmalı
        assert any(r.priority_level == "LOW" for r in results)


# Pytest komutları
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
