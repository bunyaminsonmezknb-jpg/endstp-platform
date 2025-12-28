"""
Difficulty Engine v1 (Original Manual Calculation)
Hybrid difficulty calculation combining pedagogical principles
"""
from datetime import datetime, timezone
from typing import List, Dict


def calculate_difficulty_score(tests: List[Dict], topic_difficulty_level: int = 3) -> Dict:
    """
    Hybrid difficulty calculation combining:
    - Pedagogical principles (blank vs wrong)
    - Recent performance weighting
    - Topic inherent difficulty
    
    Returns:
        {
            "difficulty_score": 0-100,
            "difficulty_level": 1-5,
            "factors": {...},
            "recommendation": str
        }
    """
    if not tests:
        return {
            "difficulty_score": 50,
            "difficulty_level": 3,
            "factors": {"reason": "no_data"},
            "recommendation": "Henüz test verisi yok"
        }
    
    # Son 3 test
    recent_tests = tests[:3]
    
    # Aggregate stats
    total_questions = sum(t.get("total_questions", 0) for t in recent_tests)
    total_correct = sum(t.get("correct_count", 0) for t in recent_tests)
    total_wrong = sum(t.get("wrong_count", 0) for t in recent_tests)
    total_blank = sum(t.get("blank_count", 0) for t in recent_tests)
    
    if total_questions == 0:
        return {
            "difficulty_score": 50,
            "difficulty_level": 3,
            "factors": {"reason": "invalid_data"},
            "recommendation": "Geçersiz test verisi"
        }
    
    # 1️⃣ PEDAGOGICAL WEIGHTS (blank > wrong)
    blank_rate = total_blank / total_questions
    wrong_rate = total_wrong / total_questions
    correct_rate = total_correct / total_questions
    
    stress_score = (blank_rate * 0.55) + (wrong_rate * 0.30)
    
    # 2️⃣ PERFORMANCE FACTOR
    performance_factor = 1 - correct_rate
    
    # 3️⃣ VOLATILITY
    if len(recent_tests) >= 2:
        success_rates = [t.get("success_rate", 0) for t in recent_tests]
        volatility = max(success_rates) - min(success_rates)
        volatility_factor = min(0.15, volatility / 100 * 0.10)
    else:
        volatility_factor = 0
    
    # 4️⃣ TOPIC INHERENT DIFFICULTY
    topic_factor = (topic_difficulty_level / 10) * 0.05
    
    # 5️⃣ FINAL SCORE
    raw_score = (
        stress_score * 0.55 +
        performance_factor * 0.30 +
        volatility_factor +
        topic_factor
    )
    
    difficulty_score = min(100, max(0, raw_score * 100))
    
    # 6️⃣ LEVEL (1-5)
    if difficulty_score >= 80:
        level = 5
    elif difficulty_score >= 65:
        level = 4
    elif difficulty_score >= 45:
        level = 3
    elif difficulty_score >= 25:
        level = 2
    else:
        level = 1
    
    # 7️⃣ TREND
    if len(recent_tests) >= 3:
        latest_success = recent_tests[0].get("success_rate", 0)
        oldest_success = recent_tests[-1].get("success_rate", 0)
        if latest_success > oldest_success + 10:
            trend_text = "İlerliyor ✅"
        elif latest_success < oldest_success - 10:
            trend_text = "Gerileme var ⚠️"
        else:
            trend_text = "Stabil"
    else:
        trend_text = "Daha fazla test gerekli"
    
    # 8️⃣ RECOMMENDATION
    if difficulty_score >= 80:
        if blank_rate > 0.4:
            recommendation = "TEHLIKE! Boş bırakma çok yüksek. Temel bilgileri öğren."
        else:
            recommendation = "ÇOK ZOR! Yanlış kavramalar var. Konuyu baştan öğren."
    elif difficulty_score >= 65:
        recommendation = "ZOR! Konsantre çalışma gerekli. Video izle + soru çöz."
    elif difficulty_score >= 45:
        recommendation = "ORTA zorluk. Düzenli tekrar yap."
    else:
        recommendation = "KOLAY! Sadece periyodik tekrar yeterli."
    
    return {
        "difficulty_score": round(difficulty_score, 1),
        "difficulty_level": level,
        "factors": {
            "blank_rate": round(blank_rate * 100, 1),
            "wrong_rate": round(wrong_rate * 100, 1),
            "correct_rate": round(correct_rate * 100, 1),
            "volatility": round(volatility_factor * 100, 1) if len(recent_tests) >= 2 else 0,
            "topic_inherent_difficulty": topic_difficulty_level,
            "performance_trend": trend_text
        },
        "recommendation": recommendation
    }


# ============================================
# WRAPPER CLASS FOR MOTOR SYSTEM
# ============================================

class DifficultyEngineV1:
    """
    Wrapper class for original manual calculation
    Provides consistent interface with motor system
    """
    
    def calculate(self, student_id: str, topic_id: str, **kwargs):
        """
        Calculate difficulty using original formula
        
        Returns motor-compatible format
        """
        # Get test data from kwargs
        tests = kwargs.get("tests", [])
        topic_difficulty = kwargs.get("topic_difficulty_level", 3)
        
        # Use original calculation
        result = calculate_difficulty_score(tests, topic_difficulty)
        
        # Return motor-compatible format
        return {
            "difficulty_percentage": result["difficulty_score"],
            "difficulty_level": result["difficulty_level"],
            "student_segment": "standard",
            "student_message": result["recommendation"],
            "motor_metadata": {
                "motor_version": "v1",
                "features_used": 4,
                "fallback_used": False,
                "calculation_method": "original_manual"
            },
            "factors": result.get("factors", {})
        }


# ============================================
# BACKWARD COMPATIBILITY
# ============================================
# Old code expects "DifficultyEngine" class
DifficultyEngine = DifficultyEngineV1

# Mock classes for old imports
class StatMetrics:
    def __init__(self, total_questions=0, correct=0, wrong=0, blank=0, net=0):
        self.total_questions = total_questions
        self.correct = correct
        self.wrong = wrong
        self.blank = blank
        self.net = net

class DifficultyResult:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
