"""
Difficulty Engine v1.0.0 - HARDENED (KEMİK SİSTEM)
Topic Difficulty Calculation

PHILOSOPHY:
- Deterministic
- Stateless
- Fail-safe
- Never crash
- Config-driven

ROLE:
- Calculates topic difficulty (0-100)
- Based on: blank rate, wrong rate, volatility
- NO segmentation
- NO learning
- NO context

LOCK DATE: 2025-01-02
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DifficultyConfig(BaseModel):
    """All constants (tunable)"""
    # Weights (pedagogical priority: blank > wrong)
    weight_blank: float = 0.55
    weight_wrong: float = 0.30
    weight_volatility: float = 0.10
    weight_misconception: float = 0.05
    
    # Clamps (hardening)
    max_blank_rate: float = 1.0
    max_wrong_rate: float = 1.0
    max_volatility: float = 1.0
    max_difficulty: float = 100.0
    
    # Volatility calculation
    min_tests_for_volatility: int = 3


class DifficultyInput(BaseModel):
    """Input data for difficulty calculation"""
    topic_id: str
    questions_total: int = Field(gt=0, description="Total questions")
    questions_correct: int = Field(ge=0)
    questions_wrong: int = Field(ge=0)
    questions_blank: int = Field(ge=0)
    
    # Optional: Historical data for volatility
    recent_tests: Optional[list] = Field(
        default=None,
        description="Recent test results for volatility calculation"
    )


class DifficultyOutput(BaseModel):
    """Output contract (NEVER CHANGE)"""
    topic_id: str
    difficulty_score: float = Field(description="0-100")
    difficulty_level: str = Field(description="LOW|MEDIUM|HIGH|CRITICAL")
    factors: dict = Field(description="Component breakdown")
    analysis: str


class DifficultyEngineV1:
    """
    v1 Hardened Core
    
    Formula:
    Difficulty = blank_rate×0.55 + wrong_rate×0.30 + volatility×0.10 + misconception×0.05
    
    Scaled to 0-100
    """
    
    DEFAULT_CONFIG = DifficultyConfig()
    
    @classmethod
    def calculate(
        cls,
        input_data: DifficultyInput,
        config: Optional[DifficultyConfig] = None
    ) -> DifficultyOutput:
        """
        Calculate topic difficulty (deterministic, fail-safe)
        
        Args:
            input_data: Test performance data
            config: Custom config (optional)
        
        Returns:
            DifficultyOutput
        """
        
        if config is None:
            config = cls.DEFAULT_CONFIG
        
        # ================================
        # INPUT GUARDS (CRITICAL)
        # ================================
        
        if input_data.questions_total <= 0:
            return cls._neutral_response(
                input_data.topic_id,
                "Geçersiz soru sayısı"
            )
        
        # Effective total (batch safety)
        answered = (
            input_data.questions_correct +
            input_data.questions_wrong +
            input_data.questions_blank
        )
        effective_total = max(input_data.questions_total, answered, 1)
        
        # ================================
        # RATES (CLAMPED)
        # ================================
        
        blank_rate = min(
            input_data.questions_blank / effective_total,
            config.max_blank_rate
        )
        
        wrong_rate = min(
            input_data.questions_wrong / effective_total,
            config.max_wrong_rate
        )
        
        # ================================
        # VOLATILITY (if historical data)
        # ================================
        
        volatility = 0.0
        
        if (input_data.recent_tests and 
            len(input_data.recent_tests) >= config.min_tests_for_volatility):
            
            volatility = cls._calculate_volatility(
                input_data.recent_tests,
                config
            )
        
        # ================================
        # MISCONCEPTION FACTOR
        # ================================
        
        # Simple heuristic: wrong > blank indicates misconception
        misconception_factor = 0.0
        if wrong_rate > blank_rate and wrong_rate > 0.3:
            misconception_factor = min(wrong_rate - blank_rate, 0.3)
        
        # ================================
        # DIFFICULTY SCORE
        # ================================
        
        raw_difficulty = (
            blank_rate * config.weight_blank +
            wrong_rate * config.weight_wrong +
            volatility * config.weight_volatility +
            misconception_factor * config.weight_misconception
        )
        
        # Scale to 0-100
        difficulty_score = min(raw_difficulty * 100, config.max_difficulty)
        
        # ================================
        # LEVEL DETERMINATION
        # ================================
        
        if difficulty_score < 25:
            level = "LOW"
            analysis = "Bu konu senin için kolay"
        elif difficulty_score < 50:
            level = "MEDIUM"
            analysis = "Orta zorlukta bir konu"
        elif difficulty_score < 75:
            level = "HIGH"
            analysis = "Zorlayıcı bir konu"
        else:
            level = "CRITICAL"
            analysis = "Çok zorlanıyorsun"
        
        return DifficultyOutput(
            topic_id=input_data.topic_id,
            difficulty_score=round(difficulty_score, 2),
            difficulty_level=level,
            factors={
                "blank_contribution": round(blank_rate * config.weight_blank * 100, 2),
                "wrong_contribution": round(wrong_rate * config.weight_wrong * 100, 2),
                "volatility_contribution": round(volatility * config.weight_volatility * 100, 2),
                "misconception_contribution": round(misconception_factor * config.weight_misconception * 100, 2)
            },
            analysis=analysis
        )
    
    @classmethod
    def _calculate_volatility(
        cls,
        recent_tests: list,
        config: DifficultyConfig
    ) -> float:
        """Calculate performance volatility from recent tests"""
        
        if len(recent_tests) < config.min_tests_for_volatility:
            return 0.0
        
        # Extract success rates
        success_rates = []
        for test in recent_tests[-5:]:  # Last 5 tests max
            total = test.get("total", 1)
            correct = test.get("correct", 0)
            if total > 0:
                success_rates.append(correct / total)
        
        if len(success_rates) < 2:
            return 0.0
        
        # Calculate standard deviation
        mean = sum(success_rates) / len(success_rates)
        variance = sum((x - mean) ** 2 for x in success_rates) / len(success_rates)
        std_dev = variance ** 0.5
        
        # Normalize to 0-1
        volatility = min(std_dev * 2, config.max_volatility)
        
        return volatility
    
    @classmethod
    def _neutral_response(cls, topic_id: str, reason: str) -> DifficultyOutput:
        """Neutral response for edge cases"""
        return DifficultyOutput(
            topic_id=topic_id,
            difficulty_score=50.0,
            difficulty_level="MEDIUM",
            factors={
                "blank_contribution": 0.0,
                "wrong_contribution": 0.0,
                "volatility_contribution": 0.0,
                "misconception_contribution": 0.0
            },
            analysis=reason
        )