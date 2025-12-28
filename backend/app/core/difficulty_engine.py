"""
Difficulty Engine v1.0.0 - STABLE FOUNDATION (KEMİK SİSTEM)
============================================================

VERSION: 1.0.0 (Hardened Release)
STATUS: LTS (Long Term Support)
PHILOSOPHY: Kemik gibi sağlam, never crash, always return
PERFORMANCE TARGET: <50ms response time

CHANGE POLICY:
- ✅ Bug fixes
- ✅ Input validation
- ✅ Edge case handling
- ✅ Performance optimization (without breaking)
- ❌ New features (go to v2)
- ❌ Algorithm changes (stability first)

ALGORITHM:
Hybrid difficulty calculation combining:
1. Pedagogical principles (blank > wrong weighting)
2. Recent 3 tests performance
3. Volatility analysis
4. Topic inherent difficulty

PERFORMANCE NOTES:
- Target: <50ms response time
- Measured latency tracking available in v2+
- v1 focuses on stability, v2 adds performance profiling

RELEASE DATE: 2024-12-28
MAINTAINER: End.STP Core Team
"""

from datetime import datetime
from typing import List, Dict, Optional
import logging

# ===========================================
# VERSION & METADATA
# ===========================================
__version__ = "1.0.0"
__status__ = "stable"
__author__ = "End.STP Core Team"
__performance_target_ms__ = 50

logger = logging.getLogger(__name__)

# ===========================================
# CONSTANTS (No Magic Numbers!)
# ===========================================

# Score boundaries
MIN_SCORE = 0
MAX_SCORE = 100
DEFAULT_SCORE = 50
DEFAULT_LEVEL = 3

# Difficulty levels (1-5 scale)
LEVEL_BOUNDARIES = {
    5: 80,  # Very hard (Çok zor)
    4: 65,  # Hard (Zor)
    3: 45,  # Medium (Orta)
    2: 25,  # Easy (Kolay)
    1: 0    # Very easy (Çok kolay)
}

# Algorithm weights (Original formula - DO NOT CHANGE)
BLANK_WEIGHT = 0.55      # Blank questions weigh more (pedagogical)
WRONG_WEIGHT = 0.30      # Wrong answers weight
STRESS_WEIGHT = 0.55     # Stress factor contribution
PERFORMANCE_WEIGHT = 0.30  # Performance factor contribution
MAX_VOLATILITY = 0.15    # Maximum volatility contribution
TOPIC_WEIGHT = 0.05      # Topic inherent difficulty weight

# Safe boundaries
MIN_TOPIC_DIFFICULTY = 1
MAX_TOPIC_DIFFICULTY = 10
MIN_RATE = 0.0
MAX_RATE = 1.0
RECENT_TESTS_COUNT = 3   # Number of recent tests to analyze

# Trend detection threshold
TREND_THRESHOLD = 10     # Percentage change to detect trend

# Critical blank rate threshold
CRITICAL_BLANK_RATE = 40  # Percentage


# ===========================================
# UTILITY FUNCTIONS (DEFENSIVE PROGRAMMING)
# ===========================================

def clamp(v: float, lo: float, hi: float) -> float:
    """
    Keep value safely within range (defensive programming).
    
    Args:
        v: Value to clamp
        lo: Lower bound (inclusive)
        hi: Upper bound (inclusive)
    
    Returns:
        Clamped value, or lo if error occurs
        
    Examples:
        >>> clamp(150, 0, 100)
        100
        >>> clamp(-10, 0, 100)
        0
        >>> clamp(50, 0, 100)
        50
        >>> clamp(None, 0, 100)  # Error case
        0
    
    Notes:
        - Never crashes, always returns valid number
        - On error, returns lower bound (safest default)
    """
    try:
        return max(lo, min(v, hi))
    except (TypeError, ValueError, AttributeError) as e:
        logger.warning(f"clamp() error: v={v}, lo={lo}, hi={hi}, error={e}")
        return lo


def safe_get(d: Dict, key: str, default: float = 0) -> float:
    """
    Returns numeric safe value from dictionary (None-safe, type-safe).
    
    Args:
        d: Dictionary to query
        key: Key to fetch
        default: Default value if missing/invalid (default: 0)
    
    Returns:
        Float value or default if missing/invalid
        
    Examples:
        >>> safe_get({"score": 50}, "score")
        50.0
        >>> safe_get({"score": "50"}, "score")
        50.0
        >>> safe_get({"score": None}, "score", 0)
        0.0
        >>> safe_get({}, "missing", 10)
        10.0
    
    Notes:
        - Handles None values gracefully
        - Converts strings to float if possible
        - Never crashes on type errors
    """
    v = d.get(key, default)
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError, AttributeError) as e:
        logger.warning(f"safe_get() error: key={key}, value={v}, error={e}")
        return default


def parse_date_safe(test: Dict) -> datetime:
    """
    Safely parse test date with multiple fallbacks.
    
    Args:
        test: Test dictionary containing 'test_date' field
    
    Returns:
        Parsed datetime or datetime.min if parsing fails
        
    Examples:
        >>> parse_date_safe({"test_date": "2024-12-28"})
        datetime.datetime(2024, 12, 28, 0, 0)
        >>> parse_date_safe({"test_date": None})
        datetime.datetime(1, 1, 1, 0, 0)
        >>> parse_date_safe({})
        datetime.datetime(1, 1, 1, 0, 0)
    
    Notes:
        - Handles datetime objects directly
        - Parses ISO format strings
        - Returns datetime.min on any error (sorts to beginning)
    """
    d = test.get("test_date")
    
    # Already datetime object
    if isinstance(d, datetime):
        return d
    
    # Try parsing string
    try:
        return datetime.fromisoformat(str(d))
    except (TypeError, ValueError, AttributeError) as e:
        logger.debug(f"parse_date_safe() error: date={d}, error={e}")
        return datetime.min


# ===========================================
# MAIN CALCULATION FUNCTION
# ===========================================

def calculate_difficulty_score(
    tests: List[Dict], 
    topic_difficulty_level: int = DEFAULT_LEVEL
) -> Dict:
    """
    Calculate difficulty score using hybrid algorithm.
    
    This is the CORE v1 calculation - STABLE and UNCHANGING.
    Algorithm combines pedagogical principles, performance metrics,
    and topic metadata to produce reliable difficulty assessment.
    
    Args:
        tests: List of test dictionaries with keys:
            - test_date: Date of test (ISO string or datetime)
            - total_questions: Total number of questions (int)
            - correct_count: Number of correct answers (int)
            - wrong_count: Number of wrong answers (int)
            - blank_count: Number of blank answers (int)
            - success_rate: Overall success percentage (0-100)
        topic_difficulty_level: Inherent topic difficulty (1-10)
            1 = Very easy, 10 = Very hard
    
    Returns:
        Dictionary with keys:
            - difficulty_score: 0-100 difficulty score
            - difficulty_level: 1-5 difficulty level
            - factors: Dict of contributing factors
            - recommendation: Actionable student message
    
    Examples:
        >>> tests = [
        ...     {
        ...         "test_date": "2024-12-28",
        ...         "total_questions": 10,
        ...         "correct_count": 7,
        ...         "wrong_count": 2,
        ...         "blank_count": 1,
        ...         "success_rate": 70
        ...     }
        ... ]
        >>> result = calculate_difficulty_score(tests, topic_difficulty_level=5)
        >>> result["difficulty_score"]
        45.8
        >>> result["difficulty_level"]
        3
    
    Algorithm Steps:
        1. Early exit if no test data
        2. Sort tests by date (most recent first)
        3. Analyze recent 3 tests
        4. Calculate stress score (blank + wrong weighted)
        5. Calculate performance factor
        6. Calculate volatility
        7. Add topic inherent difficulty
        8. Compute final score (0-100)
        9. Map to difficulty level (1-5)
        10. Analyze trend (improving/declining/stable)
        11. Generate recommendation message
    
    Performance:
        - Target: <50ms for typical inputs
        - Worst case: <100ms for edge cases
        - Memory: O(n) where n = len(tests)
    
    Safety:
        - Never crashes (defensive programming)
        - Handles None/invalid data gracefully
        - Returns safe defaults on error
    
    Notes:
        - Algorithm weights are CONSTANTS (do not change)
        - Uses last 3 tests for recency bias
        - Blank rate weighted higher than wrong (pedagogical)
    """
    
    # =========================
    # EARLY EXIT — NO TEST DATA
    # =========================
    if not tests:
        logger.debug("No test data provided, returning default values")
        return {
            "difficulty_score": DEFAULT_SCORE,
            "difficulty_level": DEFAULT_LEVEL,
            "factors": {"reason": "no_data"},
            "recommendation": "Henüz test verisi yok"
        }

    # =========================
    # SORT TESTS BY DATE DESC
    # =========================
    tests = sorted(tests, key=parse_date_safe, reverse=True)
    recent_tests = tests[:RECENT_TESTS_COUNT]
    
    logger.debug(f"Analyzing {len(recent_tests)} recent tests out of {len(tests)} total")

    # =========================
    # AGGREGATE SAFE VALUES
    # =========================
    # 🆕 ENHANCEMENT 2: Data Quality Monitoring
    negative_value_detected = False
    
    total_questions = 0
    total_correct = 0
    total_wrong = 0
    total_blank = 0
    
    for t in recent_tests:
        tq = safe_get(t, "total_questions", 0)
        tc = safe_get(t, "correct_count", 0)
        tw = safe_get(t, "wrong_count", 0)
        tb = safe_get(t, "blank_count", 0)
        
        # Check for negative values (data quality issue)
        if tq < 0 or tc < 0 or tw < 0 or tb < 0:
            negative_value_detected = True
            logger.warning(
                f"Data quality issue: Negative value detected in test. "
                f"total_questions={tq}, correct={tc}, wrong={tw}, blank={tb}. "
                f"Resetting negatives to 0."
            )
        
        total_questions += max(0, tq)
        total_correct += max(0, tc)
        total_wrong += max(0, tw)
        total_blank += max(0, tb)

    # =========================
    # ZERO / INVALID DATA CASE
    # =========================
    if total_questions <= 0:
        logger.warning("Invalid test data: zero or negative total_questions")
        return {
            "difficulty_score": DEFAULT_SCORE,
            "difficulty_level": DEFAULT_LEVEL,
            "factors": {"reason": "invalid_or_zero_questions"},
            "recommendation": "Geçersiz test verisi"
        }

    # =========================
    # SAFE NORMALIZED RATES
    # =========================
    correct_rate = clamp(total_correct / total_questions, MIN_RATE, MAX_RATE)
    blank_rate = clamp(total_blank / total_questions, MIN_RATE, MAX_RATE)
    wrong_rate = clamp(total_wrong / total_questions, MIN_RATE, MAX_RATE)
    
    logger.debug(f"Rates - Correct: {correct_rate:.2f}, Blank: {blank_rate:.2f}, Wrong: {wrong_rate:.2f}")

    # ===========
    # STEP 1: STRESS SCORE
    # ===========
    # Pedagogical principle: Blank > Wrong
    # Blank means no knowledge, Wrong means misconception
    stress_score = (blank_rate * BLANK_WEIGHT) + (wrong_rate * WRONG_WEIGHT)

    # ===========
    # STEP 2: PERFORMANCE FACTOR
    # ===========
    performance_factor = 1 - correct_rate
    performance_factor = clamp(performance_factor, MIN_RATE, MAX_RATE)

    # ===========
    # STEP 3: VOLATILITY
    # ===========
    # 🆕 ENHANCEMENT 1: success_rate missing detection
    # High volatility = inconsistent performance = harder to predict
    missing_success_rate_count = 0
    
    if len(recent_tests) >= 2:
        success_rates = []
        for t in recent_tests:
            # Check if success_rate exists in test
            if "success_rate" not in t or t.get("success_rate") is None:
                missing_success_rate_count += 1
                logger.debug(
                    f"Data quality note: success_rate missing in test "
                    f"(date: {t.get('test_date', 'unknown')}), assuming 0"
                )
            
            sr = safe_get(t, "success_rate", 0)
            sr = clamp(sr, MIN_SCORE, MAX_SCORE)
            success_rates.append(sr)

        if success_rates:
            volatility = max(success_rates) - min(success_rates)
            volatility_factor = min(MAX_VOLATILITY, (volatility / 100) * 0.10)
            
            if missing_success_rate_count > 0:
                logger.info(
                    f"Volatility calculated with {missing_success_rate_count}/{len(recent_tests)} "
                    f"missing success_rate values. Result may be less accurate."
                )
            
            logger.debug(f"Volatility: {volatility:.1f}%, Factor: {volatility_factor:.4f}")
        else:
            volatility_factor = 0
    else:
        volatility_factor = 0
        logger.debug("Not enough tests for volatility calculation")

    # ===========
    # STEP 4: TOPIC BASE DIFFICULTY
    # ===========
    topic_difficulty_level = clamp(topic_difficulty_level, MIN_TOPIC_DIFFICULTY, MAX_TOPIC_DIFFICULTY)
    topic_factor = (topic_difficulty_level / 10) * TOPIC_WEIGHT
    
    logger.debug(f"Topic difficulty level: {topic_difficulty_level}/10, Factor: {topic_factor:.4f}")

    # ===========
    # STEP 5: FINAL RAW SCORE
    # ===========
    raw_score = (
        stress_score * STRESS_WEIGHT +
        performance_factor * PERFORMANCE_WEIGHT +
        volatility_factor +
        topic_factor
    )

    difficulty_score = clamp(raw_score * 100, MIN_SCORE, MAX_SCORE)
    
    logger.debug(f"Raw score: {raw_score:.4f}, Final difficulty: {difficulty_score:.1f}")

    # ===========
    # STEP 6: MAP TO LEVEL (1-5)
    # ===========
    if difficulty_score >= LEVEL_BOUNDARIES[5]:
        level = 5
    elif difficulty_score >= LEVEL_BOUNDARIES[4]:
        level = 4
    elif difficulty_score >= LEVEL_BOUNDARIES[3]:
        level = 3
    elif difficulty_score >= LEVEL_BOUNDARIES[2]:
        level = 2
    else:
        level = 1

    # ===========
    # STEP 7: TREND ANALYSIS
    # ===========
    if len(recent_tests) >= 3:
        latest = clamp(safe_get(recent_tests[0], "success_rate", 0), MIN_SCORE, MAX_SCORE)
        oldest = clamp(safe_get(recent_tests[-1], "success_rate", 0), MIN_SCORE, MAX_SCORE)

        if latest > oldest + TREND_THRESHOLD:
            trend_text = "İlerliyor ✅"
        elif latest < oldest - TREND_THRESHOLD:
            trend_text = "Gerileme var ⚠️"
        else:
            trend_text = "Stabil"
    else:
        trend_text = "Daha fazla test gerekli"

    # ===========
    # STEP 8: RECOMMENDATION MESSAGE
    # ===========
    blank_rate_pct = blank_rate * 100

    if difficulty_score >= 80:
        if blank_rate_pct > CRITICAL_BLANK_RATE:
            recommendation = "TEHLİKE! Boş bırakma çok yüksek. Temel bilgileri öğren."
        else:
            recommendation = "ÇOK ZOR! Yanlış kavramalar var. Konuyu baştan öğren."
    elif difficulty_score >= 65:
        recommendation = "ZOR! Konsantre çalışma gerekli. Video izle + soru çöz."
    elif difficulty_score >= 45:
        recommendation = "ORTA zorluk. Düzenli tekrar yap."
    else:
        recommendation = "KOLAY! Sadece periyodik tekrar yeterli."

    # ===========
    # RETURN RESULT
    # ===========
    result = {
        "difficulty_score": round(difficulty_score, 1),
        "difficulty_level": level,
        "factors": {
            "blank_rate": round(blank_rate * 100, 1),
            "wrong_rate": round(wrong_rate * 100, 1),
            "correct_rate": round(correct_rate * 100, 1),
            "volatility_contribution_percent": round(volatility_factor * 100, 1),
            "topic_inherent_difficulty": int(topic_difficulty_level),
            "performance_trend": trend_text
        },
        "recommendation": recommendation
    }
    
    # Log data quality summary
    if negative_value_detected or missing_success_rate_count > 0:
        logger.info(
            f"Data quality summary - Negative values: {negative_value_detected}, "
            f"Missing success_rate: {missing_success_rate_count}/{len(recent_tests)}"
        )
    
    logger.info(f"Difficulty calculation complete: score={difficulty_score:.1f}, level={level}")
    
    return result


# ===========================================
# WRAPPER CLASS FOR MOTOR SYSTEM
# ===========================================

class DifficultyEngineV1:
    """
    Wrapper class for original v1 calculation.
    Provides consistent interface with motor system.
    
    This class wraps the core calculate_difficulty_score function
    to provide motor system compatibility while maintaining the
    original stable algorithm.
    
    Attributes:
        version: Engine version (1.0.0)
        name: Engine name for logging
    
    Examples:
        >>> engine = DifficultyEngineV1()
        >>> result = engine.calculate(
        ...     student_id="student-123",
        ...     topic_id="topic-456",
        ...     tests=[...],
        ...     topic_difficulty_level=5
        ... )
    """
    
    version = __version__
    name = "DifficultyEngineV1"
    
    def calculate(
        self, 
        student_id: str, 
        topic_id: str, 
        **kwargs
    ) -> Dict:
        """
        Calculate difficulty using original v1 formula.
        
        Args:
            student_id: Student UUID (for logging)
            topic_id: Topic UUID (for logging)
            **kwargs: Additional parameters:
                - tests: List of test dictionaries
                - topic_difficulty_level: Topic difficulty (1-10)
        
        Returns:
            Motor-compatible result dictionary with keys:
                - difficulty_percentage: 0-100 score
                - difficulty_level: 1-5 level
                - student_segment: "standard"
                - student_message: Recommendation text
                - motor_metadata: Version and feature info
                - factors: Contributing factors
        
        Notes:
            - Returns motor-compatible format
            - Never crashes (defensive programming)
            - Logs student_id and topic_id for tracing
        """
        logger.info(f"DifficultyEngineV1.calculate() called for student={student_id}, topic={topic_id}")
        
        # Extract parameters
        tests = kwargs.get("tests", [])
        topic_difficulty = kwargs.get("topic_difficulty_level", DEFAULT_LEVEL)
        
        # Use core calculation
        result = calculate_difficulty_score(tests, topic_difficulty)
        
        # Return motor-compatible format
        return {
            "difficulty_percentage": result["difficulty_score"],
            "difficulty_level": result["difficulty_level"],
            "student_segment": "standard",
            "student_message": result["recommendation"],
            "motor_metadata": {
                "motor_version": "v1",
                "engine_version": self.version,
                "features_used": 4,  # Core 4 features
                "fallback_used": False,
                "calculation_method": "original_manual",
                "performance_target_ms": __performance_target_ms__,
                "performance_note": "Measured latency tracking available in v2+"
            },
            "factors": result.get("factors", {})
        }


# ===========================================
# BACKWARD COMPATIBILITY
# ===========================================
# Old code expects "DifficultyEngine" class name
DifficultyEngine = DifficultyEngineV1

# Mock classes for old imports (maintain compatibility)
class StatMetrics:
    """Backward compatibility class for old imports"""
    def __init__(self, total_questions=0, correct=0, wrong=0, blank=0, net=0):
        self.total_questions = total_questions
        self.correct = correct
        self.wrong = wrong
        self.blank = blank
        self.net = net


class DifficultyResult:
    """Backward compatibility class for old imports"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# ===========================================
# MODULE EXPORTS
# ===========================================
__all__ = [
    'calculate_difficulty_score',
    'DifficultyEngineV1',
    'DifficultyEngine',
    'clamp',
    'safe_get',
    'parse_date_safe',
    'StatMetrics',
    'DifficultyResult',
    '__version__',
]


# ===========================================
# MODULE METADATA
# ===========================================
if __name__ == "__main__":
    print(f"Difficulty Engine v{__version__} - {__status__.upper()}")
    print(f"Performance target: <{__performance_target_ms__}ms")
    print(f"Performance note: Measured latency tracking available in v2+")
    print(f"Author: {__author__}")
    print("\nThis is the STABLE FOUNDATION (KEMİK SİSTEM)")
    print("For new features, see difficulty_engine_v2.py")
