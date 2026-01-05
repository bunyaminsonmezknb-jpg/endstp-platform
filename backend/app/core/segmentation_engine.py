"""
Segmentation Engine v1.0.0 - FINAL (WITH 7 CRITICAL IMPROVEMENTS)
Student Level Classifier (L1-L7) - Rule-Based

PHILOSOPHY:
- Deterministic rule-based segmentation
- Signal-driven (not motor-aware)
- Graceful degradation on missing data
- Cold start friendly
- Override rule support
- Production-grade safety

CRITICAL IMPROVEMENTS:
1. Weight sum validation (assert)
2. Signal semantics documentation
3. Confidence penalty for volatility
4. Config-driven override rules
5. Sorted threshold mapping
6. Explicit safeguard comments
7. Future-proof cohort API

LOCK DATE: 2025-01-02
VERSION: SSE.v1.0.0 FINAL
"""

from typing import Dict, List, Optional
from datetime import datetime
import math


class SegmentationConfig:
    """
    Configuration for segmentation thresholds
    
    CRITICAL: All weights must sum to 1.0
    CRITICAL: All signals must be 0-1 normalized
    """
    
    # Version & Mode
    VERSION = "SSE.v1.0.0-FINAL"
    MODE = "deterministic"  # rule-based
    
    # Level thresholds (score → level mapping)
    LEVEL_THRESHOLDS = {
        "L1": (0, 25),      # Beginner (struggling)
        "L2": (25, 40),     # Developing
        "L3": (40, 55),     # Progressing
        "L4": (55, 70),     # Average (DEFAULT)
        "L5": (70, 82),     # Above Average
        "L6": (82, 92),     # Advanced
        "L7": (92, 100),    # Expert
    }
    
    # Signal weights (MUST sum to 1.0)
    SIGNAL_WEIGHTS = {
        "success_rate": 0.35,        # Most important
        "speed_consistency": 0.20,
        "difficulty_progression": 0.20,
        "bs_model_health": 0.15,
        "test_frequency": 0.10
    }
    
    # Signal semantics documentation (CRITICAL FOR v2 AND EXTERNAL DEVS)
    SIGNAL_DEFINITIONS = {
        "success_rate": {
            "range": "0-1",
            "direction": "higher is better",
            "description": "Proportion of correct answers"
        },
        "speed_consistency": {
            "range": "0-1",
            "direction": "higher is better",
            "description": "Stability of solving speed (low variance = high consistency)"
        },
        "difficulty_progression": {
            "range": "0-1",
            "direction": "higher is better",
            "description": "Ability to solve harder topics over time"
        },
        "bs_model_health": {
            "range": "0-1",
            "direction": "higher is better",
            "description": "Memory retention strength (BS-Model remembering rate)"
        },
        "test_frequency": {
            "range": "0-1",
            "direction": "higher is better",
            "description": "Study consistency (normalized test count)"
        }
    }
    
    # Cold start thresholds
    MIN_TESTS_FOR_SEGMENTATION = 3
    MIN_SIGNALS_FOR_CONFIDENCE = 2
    
    # Confidence calculation
    CONFIDENCE_BASE = 0.3
    CONFIDENCE_PER_TEST = 0.05  # up to 10 tests
    CONFIDENCE_PER_SIGNAL = 0.1  # up to 5 signals
    
    # Confidence penalty thresholds
    VOLATILITY_PENALTY_THRESHOLD = 0.3  # speed_consistency < 0.3 → penalty
    VOLATILITY_PENALTY_FACTOR = 0.85    # multiply confidence by 0.85
    
    # Override rules (config-driven, NOT hard-coded)
    OVERRIDE_RULES = {
        "high_overdue": {
            "threshold": 5,      # overdue_count >= 5
            "max_level": "L4",   # cap at L4
            "reason": "High risk (many overdue topics)"
        },
        "low_activity": {
            "threshold": 5,      # test_count < 5
            "max_level": "L3",   # cap at L3
            "reason": "Insufficient activity"
        }
    }
    
    # Default segment (cold start / error)
    DEFAULT_LEVEL = "L4"
    DEFAULT_CONFIDENCE = 0.5


class SegmentationEngineV1:
    """
    Student Segmentation Engine v1.0.0 FINAL
    
    Rule-based deterministic segmentation with production-grade safety
    """
    
    def __init__(self, config: Optional[SegmentationConfig] = None):
        """
        Args:
            config: Optional custom configuration
        
        Raises:
            ValueError: If signal weights don't sum to 1.0
        """
        self.config = config or SegmentationConfig()
        
        # CRITICAL SAFETY CHECK: Validate weight sum
        self._validate_weights()
    
    def _validate_weights(self):
        """
        Validate that signal weights sum to 1.0
        
        This prevents silent scoring errors from config changes
        """
        total = sum(self.config.SIGNAL_WEIGHTS.values())
        if not math.isclose(total, 1.0, rel_tol=1e-3):
            raise ValueError(
                f"SIGNAL_WEIGHTS must sum to 1.0, got {total:.4f}. "
                f"Check config for errors."
            )
    
    def get_level(
        self,
        student_id: str,
        signals: Optional[Dict] = None,
        window_days: int = 14
    ) -> Dict:
        """
        Calculate student segmentation level
        
        Args:
            student_id: Student UUID
            signals: Normalized signals from motors (0-1 range)
                {
                    "success_rate": 0.75,
                    "speed_consistency": 0.60,
                    "difficulty_progression": 0.55,
                    "bs_model_health": 0.70,
                    "test_frequency": 0.80,
                    "test_count": 12,
                    "overdue_count": 2
                }
            window_days: Analysis window (default 14 days)
        
        Returns:
            {
                "level": "L1-L7",
                "confidence": 0.0-1.0,
                "score": 0.0-100.0,
                "signals_used": [...],
                "missing_signals": [...],
                "fallback_used": bool,
                "version": "SSE.v1.0.0-FINAL",
                "computed_at": ISO timestamp
            }
        """
        
        try:
            # 1. Cold start check
            if not signals or signals.get("test_count", 0) < self.config.MIN_TESTS_FOR_SEGMENTATION:
                return self._cold_start_response(student_id, signals)
            
            # 2. Normalize signals
            normalized = self._normalize_signals(signals)
            
            # 3. Calculate score
            score = self._calculate_score(normalized)
            
            # 4. Map score to level (with sorted thresholds)
            level = self._map_score_to_level(score)
            
            # 5. Apply override rules (config-driven)
            level, override_applied = self._apply_override_rules(level, signals)
            
            # 6. Calculate confidence (with volatility penalty)
            confidence = self._calculate_confidence(
                normalized,
                signals.get("test_count", 0),
                signals
            )
            
            # 7. Build response
            response = {
                "level": level,
                "confidence": round(confidence, 2),
                "score": round(score, 2),
                "signals_used": list(normalized.keys()),
                "missing_signals": self._get_missing_signals(signals),
                "fallback_used": False,
                "version": self.config.VERSION,
                "computed_at": datetime.utcnow().isoformat()
            }
            
            # Add override info if applied
            if override_applied:
                response["override_applied"] = override_applied
            
            return response
        
        except Exception as e:
            # Fallback to default
            return self._fallback_response(student_id, str(e))
    
    def _normalize_signals(self, signals: Dict) -> Dict:
        """
        Normalize and validate signals
        
        Rules:
        - Only include signals present in input
        - Clamp to [0, 1] range
        - Skip NaN/inf values
        """
        
        normalized = {}
        
        for signal_name, weight in self.config.SIGNAL_WEIGHTS.items():
            if signal_name in signals:
                value = signals[signal_name]
                
                # Validate
                if isinstance(value, (int, float)) and not math.isnan(value) and not math.isinf(value):
                    # Clamp to [0, 1]
                    clamped = max(0.0, min(1.0, float(value)))
                    normalized[signal_name] = clamped
        
        return normalized
    
    def _calculate_score(self, normalized_signals: Dict) -> float:
        """
        Calculate weighted score (0-100)
        
        Formula: Score = Σ(signal × weight) × 100
        
        Missing signals are ignored (not zeroed)
        """
        
        if not normalized_signals:
            # SAFEGUARD: This should never be reached under normal conditions
            # Cold start returns early, fallback catches errors
            # If we're here, something unexpected happened
            return 50.0  # Neutral score
        
        # Calculate weighted sum
        total_weight = 0.0
        weighted_sum = 0.0
        
        for signal_name, value in normalized_signals.items():
            weight = self.config.SIGNAL_WEIGHTS.get(signal_name, 0.0)
            if weight > 0:
                weighted_sum += value * weight
                total_weight += weight
        
        # Normalize by actual weight used
        if total_weight > 0:
            score = (weighted_sum / total_weight) * 100
        else:
            # SAFEGUARD: Should never happen (weights validated in __init__)
            score = 50.0
        
        return max(0.0, min(100.0, score))
    
    def _map_score_to_level(self, score: float) -> str:
        """
        Map score to segment level
        
        CRITICAL: Thresholds are sorted to prevent order-dependent bugs
        
        Args:
            score: 0-100
        
        Returns:
            Level: L1-L7
        """
        
        # Sort thresholds by min_score to guarantee correct mapping
        sorted_thresholds = sorted(
            self.config.LEVEL_THRESHOLDS.items(),
            key=lambda x: x[1][0]  # Sort by min_score
        )
        
        for level, (min_score, max_score) in sorted_thresholds:
            if min_score <= score < max_score:
                return level
        
        # Edge case: score = 100 or > max threshold
        if score >= 92:
            return "L7"
        
        return self.config.DEFAULT_LEVEL
    
    def _apply_override_rules(self, level: str, signals: Dict) -> tuple[str, Optional[str]]:
        """
        Apply config-driven override rules
        
        Returns:
            (adjusted_level, override_reason)
        """
        
        overdue_count = signals.get("overdue_count", 0)
        test_count = signals.get("test_count", 0)
        
        # Rule 1: High overdue (config-driven)
        high_overdue_rule = self.config.OVERRIDE_RULES["high_overdue"]
        if overdue_count >= high_overdue_rule["threshold"]:
            level_num = int(level[1])
            max_level_num = int(high_overdue_rule["max_level"][1])
            
            if level_num > max_level_num:
                return (
                    high_overdue_rule["max_level"],
                    high_overdue_rule["reason"]
                )
        
        # Rule 2: Low activity (config-driven)
        low_activity_rule = self.config.OVERRIDE_RULES["low_activity"]
        if test_count < low_activity_rule["threshold"]:
            level_num = int(level[1])
            max_level_num = int(low_activity_rule["max_level"][1])
            
            if level_num > max_level_num:
                return (
                    low_activity_rule["max_level"],
                    low_activity_rule["reason"]
                )
        
        return (level, None)
    
    def _calculate_confidence(
        self,
        normalized_signals: Dict,
        test_count: int,
        raw_signals: Dict
    ) -> float:
        """
        Calculate confidence with volatility penalty
        
        Factors:
        - Signal coverage
        - Test count
        - Volatility penalty (if speed_consistency low)
        """
        
        # Base confidence
        confidence = self.config.CONFIDENCE_BASE
        
        # Signal coverage bonus
        signal_count = len(normalized_signals)
        if signal_count >= self.config.MIN_SIGNALS_FOR_CONFIDENCE:
            signal_bonus = min(signal_count * self.config.CONFIDENCE_PER_SIGNAL, 0.5)
            confidence += signal_bonus
        
        # Test count bonus
        test_bonus = min(test_count * self.config.CONFIDENCE_PER_TEST, 0.5)
        confidence += test_bonus
        
        # Volatility penalty (if speed_consistency very low)
        speed_consistency = raw_signals.get("speed_consistency", 1.0)
        if speed_consistency < self.config.VOLATILITY_PENALTY_THRESHOLD:
            confidence *= self.config.VOLATILITY_PENALTY_FACTOR
        
        return max(0.0, min(1.0, confidence))
    
    def _get_missing_signals(self, signals: Dict) -> List[str]:
        """Identify missing signals"""
        expected_signals = set(self.config.SIGNAL_WEIGHTS.keys())
        provided_signals = set(signals.keys()) if signals else set()
        missing = expected_signals - provided_signals
        return sorted(list(missing))
    
    def _cold_start_response(self, student_id: str, signals: Optional[Dict]) -> Dict:
        """Response for cold start (insufficient data)"""
        test_count = signals.get("test_count", 0) if signals else 0
        
        return {
            "level": "L1",
            "confidence": 0.3,
            "score": 20.0,
            "signals_used": [],
            "missing_signals": list(self.config.SIGNAL_WEIGHTS.keys()),
            "fallback_used": False,
            "cold_start": True,
            "reason": f"Insufficient data (tests: {test_count}, min: {self.config.MIN_TESTS_FOR_SEGMENTATION})",
            "version": self.config.VERSION,
            "computed_at": datetime.utcnow().isoformat()
        }
    
    def _fallback_response(self, student_id: str, error: str) -> Dict:
        """Fallback response on error"""
        return {
            "level": self.config.DEFAULT_LEVEL,
            "confidence": self.config.DEFAULT_CONFIDENCE,
            "score": 50.0,
            "signals_used": [],
            "missing_signals": list(self.config.SIGNAL_WEIGHTS.keys()),
            "fallback_used": True,
            "error": error,
            "version": self.config.VERSION,
            "computed_at": datetime.utcnow().isoformat()
        }
    
    def get_cohort_for_level(
        self,
        level: str,
        window_days: int = 30
    ) -> Dict:
        """
        Get precomputed cohort statistics for a level
        
        NOTE: This READS precomputed data, does NOT calculate
        
        Args:
            level: L1-L7
            window_days: Time window for cohort calculation (default 30)
        
        Returns:
            {
                "level": "L4",
                "window_days": 30,
                "student_count": 1000,
                "avg_score": 62.5,
                "percentiles": {...}
            }
        """
        
        # TODO: Read from precomputed cohort table
        # This is a PLACEHOLDER
        
        return {
            "level": level,
            "window_days": window_days,
            "student_count": 0,
            "avg_score": 0.0,
            "percentiles": {
                "p25": 0.0,
                "p50": 0.0,
                "p75": 0.0
            },
            "precomputed": False,
            "note": "Cohort statistics not yet implemented"
        }

# ========================================
# GLOBAL INSTANCE & GETTER
# ========================================

# Global segmentation engine instance
_segmentation_engine_instance = None


def get_segmentation_engine() -> SegmentationEngineV1:
    """
    Get or create global segmentation engine instance
    
    Singleton pattern for segmentation engine
    
    Returns:
        SegmentationEngineV1 instance
    """
    global _segmentation_engine_instance
    
    if _segmentation_engine_instance is None:
        _segmentation_engine_instance = SegmentationEngineV1()
    
    return _segmentation_engine_instance
