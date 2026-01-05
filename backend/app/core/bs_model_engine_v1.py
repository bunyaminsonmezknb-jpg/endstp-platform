"""
BS-Model v1.0.0 - HARDENED (KEMİK SİSTEM)
Simple Spaced Repetition

PHILOSOPHY:
- Deterministic
- Stateless
- Fail-safe
- Never crash
- 4 states only

ROLE:
- Calculate next review interval
- Status: NEW | HERO | RESET | NORMAL
- NO segmentation
- NO context
- NO learning

LOCK DATE: 2025-01-02
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta


class BSModelConfig(BaseModel):
    """All constants (tunable)"""
    # EF bounds
    ef_min: float = 1.3
    ef_max: float = 2.5
    ef_default: float = 2.5
    
    # Thresholds
    hero_threshold: float = 0.7
    reset_threshold: float = 0.35
    
    # Difficulty adjustment
    difficulty_ef_penalty: float = 0.1  # per difficulty level


class BSModelInput(BaseModel):
    """Input data for BS-Model"""
    # Performance
    correct: int = Field(ge=0)
    incorrect: int = Field(ge=0)
    blank: int = Field(ge=0)
    total: int = Field(gt=0)
    difficulty: int = Field(ge=1, le=5, default=3)
    
    # State (optional for first test)
    current_ef: Optional[float] = Field(default=None, ge=1.3, le=2.5)
    current_ia: Optional[int] = Field(default=None, ge=0)
    actual_gap: Optional[int] = Field(default=None, ge=0)
    repetitions: int = Field(ge=0, default=0)
    
class ReviewInput(BaseModel):
    """Input for single review/answer"""
    topic_id: int
    correct: bool
    response_time: Optional[float] = None
    timestamp: Optional[datetime] = None

class BSModelOutput(BaseModel):
    """Output contract (NEVER CHANGE)"""
    status: str = Field(description="NEW|HERO|RESET|NORMAL")
    next_ef: float
    next_ia: int
    next_repetition: int
    score: float = Field(description="Net score 0-1")
    analysis: str


class BSModelV1:
    """
    v1 Hardened Core
    
    States:
    - NEW: First test (rep=0)
    - HERO: Late but good performance
    - RESET: Poor performance (score < 0.35)
    - NORMAL: Standard progression
    """
    
    DEFAULT_CONFIG = BSModelConfig()
    
    @classmethod
    def calculate(
        cls,
        input_data: BSModelInput,
        config: Optional[BSModelConfig] = None
    ) -> BSModelOutput:
        """
        Calculate next review interval (deterministic, fail-safe)
        
        Args:
            input_data: Test performance + state
            config: Custom config (optional)
        
        Returns:
            BSModelOutput
        """
        
        if config is None:
            config = cls.DEFAULT_CONFIG
        
        # ================================
        # INPUT GUARDS
        # ================================
        
        if input_data.total <= 0:
            return cls._neutral_response("Geçersiz soru sayısı")
        
        # ================================
        # PERFORMANCE METRICS
        # ================================
        
        # Success rate
        success_rate = input_data.correct / input_data.total
        
        # Net score (penalize wrong answers)
        net = input_data.correct - (input_data.incorrect * 0.25)
        score = max(0, net / input_data.total)
        
        # ================================
        # STATE HANDLING (None-safe)
        # ================================
        
        current_ef = (
            input_data.current_ef 
            if input_data.current_ef is not None 
            else config.ef_default
        )
        
        current_ia = (
            input_data.current_ia 
            if input_data.current_ia is not None 
            else 1
        )
        
        actual_gap = (
            input_data.actual_gap 
            if input_data.actual_gap is not None 
            else 0
        )
        
        repetitions = input_data.repetitions
        
        # ================================
        # STATUS LOGIC
        # ================================
        
        # NEW: First test
        if repetitions == 0:
            new_ef = max(
                config.ef_min,
                current_ef - (input_data.difficulty * config.difficulty_ef_penalty)
            )
            
            return BSModelOutput(
                status="NEW",
                next_ef=round(new_ef, 2),
                next_ia=1,
                next_repetition=1,
                score=round(score, 2),
                analysis=f"İlk test. Başarı: {success_rate*100:.0f}%"
            )
        
        # HERO: Late but good
        if score >= config.hero_threshold and actual_gap > current_ia:
            bonus = min(0.1, (actual_gap - current_ia) * 0.01)
            new_ef = min(config.ef_max, current_ef + bonus)
            new_ia = int(current_ia * new_ef * 1.2)
            
            return BSModelOutput(
                status="HERO",
                next_ef=round(new_ef, 2),
                next_ia=new_ia,
                next_repetition=repetitions + 1,
                score=round(score, 2),
                analysis="Mükemmel! Gecikmeye rağmen başarılı."
            )
        
        # RESET: Poor performance
        if score < config.reset_threshold:
            penalty_ef = max(config.ef_min, current_ef - 0.2)
            
            return BSModelOutput(
                status="RESET",
                next_ef=round(penalty_ef, 2),
                next_ia=1,
                next_repetition=1,
                score=round(score, 2),
                analysis="Zorluk var. Baştan başlıyoruz."
            )
        
        # NORMAL: Standard progression
        ef_change = (score - 0.5) * 0.15
        new_ef = max(config.ef_min, min(config.ef_max, current_ef + ef_change))
        new_ia = int(current_ia * new_ef)
        
        return BSModelOutput(
            status="NORMAL",
            next_ef=round(new_ef, 2),
            next_ia=max(1, new_ia),
            next_repetition=repetitions + 1,
            score=round(score, 2),
            analysis=f"Normal ilerleme. Başarı: {success_rate*100:.0f}%"
        )
    
    @classmethod
    def _neutral_response(cls, reason: str) -> BSModelOutput:
        """Neutral response for edge cases"""
        return BSModelOutput(
            status="NORMAL",
            next_ef=2.5,
            next_ia=1,
            next_repetition=0,
            score=0.5,
            analysis=reason
        )