"""
Time Analyzer v1.0.0 - HARDENED (KEMİK SİSTEM)
Speed Intelligence & Difficulty Modification

PHILOSOPHY:
- Deterministic
- Stateless
- Fail-safe
- Never crash
- Config-driven

ROLE:
- Analyzes test timing
- Produces difficulty modifier
- NO segmentation
- NO learning
- NO motivation

LOCK DATE: 2025-01-02
"""

from typing import Optional
from pydantic import BaseModel, Field


class TimeConfig(BaseModel):
    """All constants (tunable)"""
    # Thresholds
    fast_threshold: float = 0.7
    slow_threshold: float = 1.3
    
    # Modifiers
    fast_modifier: float = 0.9
    slow_modifier: float = 1.15
    
    # Timing
    ideal_time_per_question: float = 1.5
    
    # Caps (CRITICAL - Anti-manipulation)
    soft_cap_minutes: float = 25.0
    hard_cap_minutes: float = 40.0
    
    # Success threshold
    success_threshold: float = 0.8
    
    # Question count range
    min_questions: int = 8
    max_questions: int = 20
    base_questions: int = 12  # Standard


class TimeAnalysisResult(BaseModel):
    """Output contract (NEVER CHANGE)"""
    pace_ratio: float = Field(description="1.0 = ideal")
    time_modifier: float = Field(description="0.9-1.15")
    analysis: str
    is_fast: bool
    is_slow: bool
    duration_used: Optional[float] = None  # After capping


class TimeAnalyzerV1:
    """
    v1 Hardened Core
    
    Formula:
    - Fast (<0.7): modifier = 0.9
    - Normal (0.7-1.3): modifier = 1.0
    - Slow (>1.3): modifier = 1.15
    """
    
    DEFAULT_CONFIG = TimeConfig()
    
    @classmethod
    def analyze(
        cls,
        total_duration: Optional[float],
        total_questions: int,
        success_rate: Optional[float] = None,
        config: Optional[TimeConfig] = None
    ) -> TimeAnalysisResult:
        """
        Timing analysis (deterministic, fail-safe)
        
        Args:
            total_duration: Total time in minutes (optional)
            total_questions: Number of questions
            success_rate: Success rate 0-1 (optional)
            config: Custom config (optional)
        
        Returns:
            TimeAnalysisResult
        """
        
        if config is None:
            config = cls.DEFAULT_CONFIG
        
        # ================================
        # INPUT GUARDS (CRITICAL)
        # ================================
        
        # Question count validation
        if total_questions <= 0:
            return cls._neutral_response(
                "Geçersiz soru sayısı",
                duration_used=total_duration
            )
        
        # Question count range check
        if not (config.min_questions <= total_questions <= config.max_questions):
            return cls._neutral_response(
                f"Soru sayısı {config.min_questions}-{config.max_questions} arasında olmalı",
                duration_used=total_duration
            )
        
        # Duration validation & capping
        if total_duration is None or total_duration <= 0:
            return cls._neutral_response(
                "Süre bilgisi yok",
                duration_used=None
            )
        
        # SÜRE CAPPING (ANTI-MANIPULATION)
        original_duration = total_duration
        
        if total_duration > config.hard_cap_minutes:
            total_duration = config.hard_cap_minutes
        elif total_duration > config.soft_cap_minutes:
            total_duration = config.soft_cap_minutes
        
        # Success rate clamp
        if success_rate is not None:
            success_rate = max(0.0, min(1.0, success_rate))
        
        # ================================
        # CALCULATION
        # ================================
        
        # Ideal duration (12-question baseline)
        ideal_duration = config.base_questions * config.ideal_time_per_question
        
        # Pace ratio
        pace_ratio = total_duration / ideal_duration
        
        # Modifier & flags
        modifier = 1.0
        is_fast = False
        is_slow = False
        analysis = "Normal tempo"
        
        # FAST: <70% of ideal
        if pace_ratio < config.fast_threshold:
            is_fast = True
            
            # Fast & successful → Mastered
            if success_rate and success_rate >= config.success_threshold:
                modifier = config.fast_modifier
                analysis = (
                    f"Hızlı ve başarılı (×{pace_ratio:.2f}). "
                    f"Modifier: {modifier}"
                )
            else:
                # Fast but unsuccessful → Careless
                modifier = 1.0
                analysis = (
                    f"Hızlı ama hatalı (×{pace_ratio:.2f}). "
                    "Modifier: yok (dikkat et)"
                )
        
        # SLOW: >130% of ideal
        elif pace_ratio > config.slow_threshold:
            is_slow = True
            modifier = config.slow_modifier
            
            minutes_over = round(total_duration - ideal_duration, 1)
            analysis = (
                f"Yavaş tempo (×{pace_ratio:.2f}). "
                f"İdealden {minutes_over} dk fazla. "
                f"Modifier: {modifier}"
            )
        
        # NORMAL
        else:
            analysis = f"Normal tempo (×{pace_ratio:.2f}). Modifier: {modifier}"
        
        # Capping warning
        if original_duration != total_duration:
            analysis += f" (Süre {config.soft_cap_minutes if total_duration == config.soft_cap_minutes else config.hard_cap_minutes} dk'ya kapatıldı)"
        
        return TimeAnalysisResult(
            pace_ratio=round(pace_ratio, 2),
            time_modifier=round(modifier, 2),
            analysis=analysis,
            is_fast=is_fast,
            is_slow=is_slow,
            duration_used=total_duration
        )
    
    @classmethod
    def _neutral_response(cls, reason: str, duration_used: Optional[float]) -> TimeAnalysisResult:
        """Neutral response for edge cases"""
        return TimeAnalysisResult(
            pace_ratio=1.0,
            time_modifier=1.0,
            analysis=reason,
            is_fast=False,
            is_slow=False,
            duration_used=duration_used
        )
    
    @classmethod
    def apply_to_difficulty(
        cls,
        base_difficulty: float,
        time_analysis: TimeAnalysisResult
    ) -> float:
        """
        Apply time modifier to difficulty score
        
        Args:
            base_difficulty: Base difficulty (0-100)
            time_analysis: Time analysis result
        
        Returns:
            Modified difficulty (0-100)
        """
        modified = base_difficulty * time_analysis.time_modifier
        return max(0.0, min(100.0, round(modified, 2)))
