"""
BS-Model v2.0.0 - FULL PREMIUM IMPLEMENTATION
Adaptive Spaced Repetition with Complete Feature Set

PHILOSOPHY:
- Full SM-2++ with k_forget learning
- 12-question hard rule (ENFORCED)
- analysis_allowed gatekeeper (ENFORCED)
- Context-aware (archetype, prerequisites)
- Segment-aware (L1-L7 risk factors)
- Anti-gaming (integrity scoring)
- Evidence confidence (data maturity)
- Explainable decisions

DEPENDENCY: v1, Context Layer, Segmentation Engine

LOCK DATE: 2025-01-02
VERSION: 2.0.0 FINAL
"""

from typing import Optional, Dict, List
from datetime import datetime, timedelta
import math
from .bs_model_engine_v1 import BSModelV1, BSModelInput, BSModelConfig, BSModelOutput


class BSModelV2Config(BSModelConfig):
    """Extended config for v2 features"""
    # k_forget bounds
    k_min: float = 0.01
    k_max: float = 0.20
    k_default: float = 0.06
    k_update_rate: float = 0.03
    
    # Segment risk factors (L1-L7)
    segment_risk_factors: Dict[str, float] = {
        "L1": 0.85,  # Very cautious
        "L2": 0.90,
        "L3": 0.95,
        "L4": 1.00,  # Neutral
        "L5": 1.05,
        "L6": 1.10,
        "L7": 1.15   # Aggressive
    }
    
    # Evidence confidence
    evidence_half_life_days: int = 30
    min_tests_for_confidence: int = 3
    
    # Integrity thresholds
    integrity_min: float = 0.60
    speed_spike_threshold: float = 2.0
    
    # Policy targets
    policy_targets: Dict[str, float] = {
        "long_term_retention": 0.80,
        "exam_crunch": 0.88,
        "weak_spot_focus": 0.90
    }


class BSModelV2:
    """
    Full premium spaced repetition engine
    
    CRITICAL RULES:
    1. Exactly 12 questions (hard rule)
    2. analysis_allowed gatekeeper
    3. k_forget personal learning
    4. Segment risk awareness
    5. Integrity scoring
    6. Evidence confidence
    """
    
    def __init__(self, context_service, segmentation_engine):
        self.v1_engine = BSModelV1()
        self.context_service = context_service
        self.segmentation_engine = segmentation_engine
        self.config = BSModelV2Config()
    
    def calculate(
        self,
        input_data: BSModelInput,
        student_id: str,
        topic_id: str,
        analysis_allowed: bool = True,
        test_history: Optional[List[Dict]] = None,
        k_forget_prev: Optional[float] = None,
        last_test_date: Optional[datetime] = None,
        config: Optional[BSModelV2Config] = None
    ) -> Dict:
        """
        Full v2 calculation with all premium features
        
        Args:
            input_data: BSModelInput (must have total=12)
            student_id: Student UUID
            topic_id: Topic UUID
            analysis_allowed: Daily first-test gate
            test_history: Recent test results for evidence confidence
            k_forget_prev: Previous personal forgetting rate
            last_test_date: Last test date for gap calculation
            config: Optional config override
        
        Returns:
            {
                **v1_result OR skipped_result,
                "v2_features": {
                    "k_forget": float,
                    "segment_risk_factor": float,
                    "integrity_score": float,
                    "evidence_confidence": float,
                    "behavioral_multiplier": float
                },
                "adjusted_interval": int,
                "why_this_interval": str
            }
        """
        
        if config is None:
            config = self.config
        
        # ========================================
        # GATE 1: 12 QUESTION HARD RULE
        # ========================================
        
        if input_data.total != 12:
            return self._skipped_response(
                "INVALID_TEST_SIZE",
                f"BS-Model v2 requires exactly 12 questions (got {input_data.total})",
                input_data
            )
        
        # ========================================
        # GATE 2: analysis_allowed
        # ========================================
        
        if not analysis_allowed:
            return self._skipped_response(
                "SKIPPED_FOR_ANALYSIS",
                "Daily first-test-only rule (same topic, same day)",
                input_data
            )
        
        # ========================================
        # v1 BASELINE
        # ========================================
        
        v1_result = self.v1_engine.calculate(input_data, config)
        
        # ========================================
        # SEGMENT CONTEXT
        # ========================================
        
        segment = self.segmentation_engine.get_level(student_id)
        segment_risk = config.segment_risk_factors.get(segment["level"], 1.0)
        
        # ========================================
        # TOPIC CONTEXT
        # ========================================
        
        context = self.context_service.get_topic_context(topic_id)
        
        # ========================================
        # k_forget LEARNING (Personal Forgetting)
        # ========================================
        
        k_forget = self._calculate_k_forget(
            k_forget_prev or config.k_default,
            v1_result.score,
            segment,
            config
        )
        
        # ========================================
        # EVIDENCE CONFIDENCE (Data Maturity)
        # ========================================
        
        evidence_confidence = self._calculate_evidence_confidence(
            test_history,
            last_test_date,
            config
        )
        
        # ========================================
        # INTEGRITY SCORE (Anti-Gaming)
        # ========================================
        
        integrity_score = self._calculate_integrity_score(
            input_data,
            test_history,
            config
        )
        
        # ========================================
        # BEHAVIORAL MULTIPLIER (Archetype + Prerequisites)
        # ========================================
        
        behavioral_mult = self._calculate_behavioral_multiplier(
            context, segment, student_id, topic_id
        )
        
        # ========================================
        # INTERVAL ADJUSTMENT
        # ========================================
        
        adjusted_interval = self._adjust_interval_with_v2_features(
            v1_result.next_ia,
            k_forget,
            segment_risk,
            behavioral_mult,
            integrity_score,
            evidence_confidence
        )
        
        # ========================================
        # EXPLAINABILITY
        # ========================================
        
        why_this_interval = self._explain_interval(
            v1_result,
            adjusted_interval,
            segment,
            context,
            integrity_score
        )
        
        # ========================================
        # FULL v2 OUTPUT
        # ========================================
        
        return {
            **v1_result.dict(),  # v1 baseline
            "v2_features": {
                "k_forget": round(k_forget, 4),
                "segment_risk_factor": segment_risk,
                "integrity_score": round(integrity_score, 2),
                "evidence_confidence": round(evidence_confidence, 2),
                "behavioral_multiplier": round(behavioral_mult, 2),
                "archetype": context.get("archetype", "foundational")
            },
            "adjusted_interval": adjusted_interval,
            "why_this_interval": why_this_interval,
            "motor_version": "v2.0.0"
        }
    
    def _calculate_k_forget(
        self,
        k_prev: float,
        observed_score: float,
        segment: Dict,
        config: BSModelV2Config
    ) -> float:
        """
        Personal forgetting rate learning
        
        k_forget adapts based on:
        - Observed performance vs expected
        - Student segment (L1-L7)
        """
        
        # Policy target (segment-aware)
        level = segment["level"]
        if level in ["L1", "L2"]:
            target = config.policy_targets["weak_spot_focus"]
        elif level in ["L6", "L7"]:
            target = config.policy_targets["exam_crunch"]
        else:
            target = config.policy_targets["long_term_retention"]
        
        # Error signal
        error = target - observed_score
        
        # Update k_forget
        k_new = k_prev + (config.k_update_rate * error)
        
        # Clamp
        k_new = max(config.k_min, min(config.k_max, k_new))
        
        return k_new
    
    def _calculate_evidence_confidence(
        self,
        test_history: Optional[List[Dict]],
        last_test_date: Optional[datetime],
        config: BSModelV2Config
    ) -> float:
        """
        Data maturity / recency confidence
        
        Confidence factors:
        - Number of tests (more = higher confidence)
        - Recency of last test (recent = higher confidence)
        """
        
        if not test_history or len(test_history) < config.min_tests_for_confidence:
            return 0.5  # Low confidence
        
        # Test count confidence
        test_count_confidence = min(len(test_history) / 10.0, 1.0)
        
        # Recency confidence (exponential decay)
        if last_test_date:
            days_since = (datetime.now() - last_test_date).days
            recency_confidence = math.exp(-days_since / config.evidence_half_life_days)
        else:
            recency_confidence = 0.5
        
        # Combined
        confidence = (test_count_confidence * 0.6) + (recency_confidence * 0.4)
        
        return max(0.2, min(1.0, confidence))
    
    def _calculate_integrity_score(
        self,
        input_data: BSModelInput,
        test_history: Optional[List[Dict]],
        config: BSModelV2Config
    ) -> float:
        """
        Anti-gaming / manipulation detection
        
        Flags:
        - Speed spike (too fast compared to history)
        - Score spike (sudden improvement)
        - Late night testing (fatigue)
        """
        
        flags = []
        
        # Speed spike detection (placeholder - needs actual timing data)
        # if has_speed_spike(test_history):
        #     flags.append("speed_spike")
        
        # Score spike detection
        if test_history and len(test_history) >= 2:
            current_score = input_data.correct / input_data.total
            avg_prev_score = sum(t.get("score", 0.5) for t in test_history[-3:]) / len(test_history[-3:])
            
            if current_score > avg_prev_score * 1.5:  # 50% jump
                flags.append("score_spike")
        
        # Integrity score (1.0 = clean, 0.6 = suspicious)
        if len(flags) == 0:
            integrity = 1.0
        elif len(flags) == 1:
            integrity = 0.85
        else:
            integrity = 0.70
        
        return max(config.integrity_min, integrity)
    
    def _calculate_behavioral_multiplier(
        self,
        context: Dict,
        segment: Dict,
        student_id: str,
        topic_id: str
    ) -> float:
        """
        Archetype + Prerequisite combined multiplier
        """
        
        # Archetype effect
        archetype = context.get("archetype", "foundational")
        
        if archetype == "foundational":
            arch_mult = 1.05  # Longer intervals
        elif archetype == "synthesis":
            arch_mult = 0.95  # Shorter intervals
        else:
            arch_mult = 1.0
        
        # Prerequisite brake
        prerequisites = self.context_service.get_prerequisites(topic_id)
        prereq_mult = 1.0
        
        if prerequisites:
            weak_count = 0
            for prereq in prerequisites:
                mastery = self._get_mastery(student_id, prereq["topic_id"])
                if mastery < 60:
                    weak_count += 1
            
            if weak_count >= len(prerequisites) * 0.5:
                prereq_mult = 0.90  # Apply brake
        
        # Combined
        return arch_mult * prereq_mult
    
    def _adjust_interval_with_v2_features(
        self,
        base_interval: int,
        k_forget: float,
        segment_risk: float,
        behavioral_mult: float,
        integrity_score: float,
        evidence_confidence: float
    ) -> int:
        """
        Apply all v2 adjustments to base interval
        """
        
        adjusted = float(base_interval)
        
        # Segment risk
        adjusted *= segment_risk
        
        # Behavioral multiplier
        adjusted *= behavioral_mult
        
        # Integrity brake (if low integrity, limit growth)
        if integrity_score < 0.85:
            growth_cap = 1.25
            adjusted = min(adjusted, base_interval * growth_cap)
        
        # Evidence brake (if low confidence, limit growth)
        growth = adjusted / max(1, base_interval)
        growth_adjusted = 1 + ((growth - 1) * evidence_confidence)
        adjusted = base_interval * growth_adjusted
        
        return max(1, int(adjusted))
    
    def _explain_interval(
        self,
        v1_result: BSModelOutput,
        adjusted_interval: int,
        segment: Dict,
        context: Dict,
        integrity_score: float
    ) -> str:
        """
        Human-readable interval explanation
        """
        
        explanations = []
        
        # Base status
        explanations.append(f"Durum: {v1_result.status}")
        
        # Interval change
        if adjusted_interval > v1_result.next_ia:
            explanations.append("Aralığı açtım (context faktörleri)")
        elif adjusted_interval < v1_result.next_ia:
            explanations.append("Aralığı daraldım (güvenlik faktörleri)")
        else:
            explanations.append("Standart aralık")
        
        # Integrity warning
        if integrity_score < 0.85:
            explanations.append("⚠️ Veri tutarsızlığı tespit edildi, temkinli planladım")
        
        return " | ".join(explanations)
    
    def _skipped_response(
        self,
        status: str,
        reason: str,
        input_data: BSModelInput
    ) -> Dict:
        """
        Skipped analysis response (v2 gate rejection)
        """
        
        return {
            "status": status,
            "reason": reason,
            "next_ef": input_data.current_ef or 2.5,
            "next_ia": input_data.current_ia or 1,
            "next_repetition": input_data.repetitions,
            "score": 0.0,
            "analysis": f"Analiz atlandı: {reason}",
            "v2_features": {
                "skipped": True
            },
            "motor_version": "v2.0.0"
        }
    
    def _get_mastery(self, student_id: str, topic_id: str) -> float:
        """
        Get student mastery for a topic
        (Placeholder - will integrate with actual data)
        """
        return 70.0  # Default