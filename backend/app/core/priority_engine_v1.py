"""
Priority Engine v1.0.0 - HARDENED (KEMİK SİSTEM)
Strategic Topic Prioritization

PHILOSOPHY:
- Deterministic
- Stateless  
- Fail-safe
- Explainable
- Never crash, always return

ROLE:
- Calculates raw priority scores
- Sorts topics by importance
- NO segmentation
- NO learning
- NO motivation logic

LOCK DATE: 2025-01-02
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class TopicInput(BaseModel):
    """Topic-level input (safe for batch)"""
    id: str
    name: str
    course_importance: float = Field(gt=0)
    topic_weight: float = Field(ge=0, le=1)
    correct: int = Field(ge=0)
    wrong: int = Field(ge=0)
    blank: int = Field(ge=0)
    total_questions: int = Field(gt=0)
    duration_minutes: Optional[float] = None


class PriorityConfig(BaseModel):
    """All constants (tunable)"""
    # Gap weights (pedagogical)
    weight_blank: float = 4.0
    weight_wrong: float = 2.5
    weight_failure: float = 1.5
    
    # Speed calculation
    ideal_time_per_question: float = 1.5
    speed_penalty_threshold: float = 1.3
    speed_bonus_threshold: float = 0.7
    
    # Thresholds
    absolute_critical_threshold: float = 15.0
    
    # Hardening limits (CRITICAL)
    max_gap_score: float = 8.0
    max_strategic_value: float = 10.0
    max_raw_priority: float = 10_000.0


class PriorityOutput(BaseModel):
    """Output contract (NEVER CHANGE)"""
    topic_id: str
    topic_name: str
    priority_score: float = Field(description="0-100")
    priority_level: str = Field(description="LOW|MEDIUM|HIGH|CRITICAL")
    analysis: dict
    suggestion: str


class PriorityEngineV1:
    """
    v1 Hardened Core
    
    Formula: RawPriority = GapScore × StrategicValue × SpeedMultiplier × 100
    """
    
    DEFAULT_CONFIG = PriorityConfig()
    
    @classmethod
    def analyze(
        cls,
        topics: List[TopicInput],
        config: Optional[PriorityConfig] = None
    ) -> List[PriorityOutput]:
        """Calculate priorities (deterministic, fail-safe)"""
        
        if not topics:
            return []
        
        if config is None:
            config = cls.DEFAULT_CONFIG
        
        calculated = []
        
        for topic in topics:
            # FAIL-SAFE: Skip invalid
            if topic.total_questions <= 0:
                continue
            
            # Effective total (batch safety)
            answered = topic.correct + topic.wrong + topic.blank
            effective_total = max(topic.total_questions, answered, 1)
            
            # RATES (SAFE)
            blank_rate = min(topic.blank / effective_total, 1.0)
            wrong_rate = min(topic.wrong / effective_total, 1.0)
            success_rate = min(topic.correct / effective_total, 1.0)
            failure_rate = max(0.0, 1.0 - success_rate)
            
            # GAP SCORE (CLAMPED)
            gap_score = (
                blank_rate * config.weight_blank +
                wrong_rate * config.weight_wrong +
                failure_rate * config.weight_failure
            )
            gap_score = min(gap_score, config.max_gap_score)
            
            # SPEED MULTIPLIER
            speed_mult = 1.0
            speed_note = "Normal"
            
            # Negative duration protection
            if (topic.duration_minutes is not None 
                and topic.duration_minutes > 0):
                
                ideal_duration = effective_total * config.ideal_time_per_question
                if ideal_duration > 0:
                    pace_ratio = topic.duration_minutes / ideal_duration
                    
                    if pace_ratio > config.speed_penalty_threshold:
                        speed_mult = 1.25
                        speed_note = "Yavaş"
                    elif (pace_ratio < config.speed_bonus_threshold 
                          and success_rate > 0.8):
                        speed_mult = 0.8
                        speed_note = "Hızlı"
            
            # STRATEGIC VALUE (CLAMPED)
            strategic_value = topic.topic_weight * topic.course_importance
            strategic_value = min(strategic_value, config.max_strategic_value)
            
            # RAW PRIORITY (CLAMPED)
            raw_priority = gap_score * strategic_value * speed_mult * 100
            raw_priority = min(raw_priority, config.max_raw_priority)
            
            calculated.append({
                "topic": topic,
                "raw_priority": raw_priority,
                "gap_score": gap_score,
                "strategic_value": strategic_value,
                "speed_mult": speed_mult,
                "speed_note": speed_note
            })
        
        if not calculated:
            return []
        
        # NORMALIZATION (0-100)
        raw_values = [c["raw_priority"] for c in calculated]
        max_raw = max(raw_values)
        min_raw = min(raw_values)
        range_raw = max(max_raw - min_raw, 1e-6)
        
        results = []
        
        for item in calculated:
            normalized = ((item["raw_priority"] - min_raw) / range_raw) * 100
            normalized = max(0.0, min(normalized, 100.0))  # HARD CLAMP
            
            # LEVEL DETERMINATION
            level = "LOW"
            suggestion = ""
            
            raw_low = item["raw_priority"] < config.absolute_critical_threshold
            
            if normalized < 40 or raw_low:
                level = "LOW"
                suggestion = (
                    "Öncelikli değil. Mevcut durumun yeterli, "
                    "koruma tekrarları yap."
                )
                
                # Good-student protection
                if normalized > 70 and raw_low:
                    normalized = min(normalized, 45)
                    suggestion = (
                        "Listedeki diğerlerine göre en zayıf konu, "
                        "ama genel performansın iyi. Panik yapma."
                    )
            
            elif normalized < 75:
                level = "MEDIUM"
                suggestion = "Geliştirilmesi gerek. Programına ekle."
            
            else:
                level = "HIGH"
                suggestion = (
                    "Sınav başarını doğrudan etkiliyor. "
                    "Öncelikli çalışmalısın."
                )
                
                if item["raw_priority"] > config.absolute_critical_threshold * 2:
                    level = "CRITICAL"
                    suggestion = (
                        "ALARM: Bu konu puanını ciddi şekilde düşürüyor. "
                        "İlk sıraya al."
                    )
            
            if item["speed_mult"] > 1.0:
                suggestion += " (Not: İşlem hızın sınav standartlarının altında.)"
            
            results.append(
                PriorityOutput(
                    topic_id=item["topic"].id,
                    topic_name=item["topic"].name,
                    priority_score=round(normalized, 1),
                    priority_level=level,
                    analysis={
                        "raw_gap_score": round(item["gap_score"], 2),
                        "strategic_impact": round(item["strategic_value"], 2),
                        "speed_factor": item["speed_mult"],
                        "speed_note": item["speed_note"]
                    },
                    suggestion=suggestion
                )
            )
        
        # SORT: highest first
        results.sort(key=lambda x: x.priority_score, reverse=True)
        return results
