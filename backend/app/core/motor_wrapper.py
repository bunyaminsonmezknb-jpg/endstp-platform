from app.core.motor_registry import motor_registry, MotorType, MotorVersion, SubscriptionTier
import time
"""
Motor Wrapper v2.1.0 - WITH EMERGENCY FALLBACK
Automatic v1/v2 selection with comprehensive fallback mechanism

PHILOSOPHY:
- Selects correct motor version
- Falls back on error (v2 → v1)
- Emergency fallback (wrapper failure → direct v1)
- Returns result UNTOUCHED in envelope
- NEVER CRASHES

NEW IN v2.1.0:
- Emergency v1 fallback (last resort)
- fallback_reason field (optional, for debug)
- Never crash guarantee

RESPONSIBILITIES:
1. Select motor version (based on tier)
2. Handle v2 errors → silent v1 fallback
3. Handle wrapper errors → emergency v1 fallback
4. Envelope response (data + meta)
5. Minimal error logging

LOCK DATE: 2025-01-02
VERSION: 2.1.0
"""

import logging
from typing import Dict, Optional, List, Any
from enum import Enum


logger = logging.getLogger(__name__)


class UserTier(str, Enum):
    """User subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    MEDIUM = "medium"
    PREMIUM = "premium"
    INSTITUTION = "institution"


class MotorWrapper:
    """
    Motor version orchestration with comprehensive fallback
    
    Fallback Levels:
    1. Normal: v2 → v1 (if v2 fails)
    2. Emergency: Wrapper fail → Direct v1 call
    
    Never crashes guarantee
    """
    
    def __init__(
        self,
        difficulty_v1,
        difficulty_v2,
        bs_model_v1,
        bs_model_v2,
        priority_v1,
        priority_v2,
        time_v1,
        time_v2,
        context_service=None,
        segmentation_engine=None
    ):
        """Initialize with all motor instances"""
        self.difficulty_v1 = difficulty_v1
        self.difficulty_v2 = difficulty_v2
        self.bs_model_v1 = bs_model_v1
        self.bs_model_v2 = bs_model_v2
        self.priority_v1 = priority_v1
        self.priority_v2 = priority_v2
        self.time_v1 = time_v1
        self.time_v2 = time_v2
        self.context_service = context_service
        self.segmentation_engine = segmentation_engine
    
    # ========================================
    # HELPER: v2 ELIGIBILITY CHECK
    # ========================================
    
    @staticmethod
    def _can_use_v2(user_tier: UserTier, *required_fields) -> bool:
        """Check if v2 can be used"""
        tier_eligible = user_tier in [UserTier.PREMIUM, UserTier.INSTITUTION]
        fields_present = all(field is not None for field in required_fields)
        return tier_eligible and fields_present
    
    @staticmethod
    def _envelope_response(
        data: Any,
        motor_version: str,
        fallback_used: bool,
        user_tier: UserTier,
        fallback_reason: Optional[str] = None
    ) -> Dict:
        """
        Wrap motor result in response envelope
        
        Args:
            data: Motor result (untouched)
            motor_version: "v1" or "v2"
            fallback_used: Whether fallback occurred
            user_tier: User tier
            fallback_reason: Why fallback happened (optional, for debug)
        
        Returns:
            Enveloped response
        """
        meta = {
            "motor_version": motor_version,
            "fallback_used": fallback_used,
            "tier": user_tier.value
        }
        
        # Add fallback_reason if present (optional field)
        if fallback_reason:
            meta["fallback_reason"] = fallback_reason
        
        return {
            "data": data,
            "meta": meta
        }
    
    # ========================================
    # DIFFICULTY MOTOR
    # ========================================
    



    def calculate_time(
        self,
        student_id: str,
        topic_id: str,
        user_tier: UserTier
    ) -> dict:
        """Calculate Time/Speed score with v1/v2 selection + CONTEXT"""
        
        config = motor_registry.get_motor_config(
            motor_type=MotorType.TIME,
            user_tier=SubscriptionTier(user_tier.value),
            user_id=student_id
        )
        
        start_time = time.time()
        
        # Default values
        total_duration = 300.0  # 5 minutes
        total_questions = 10
        success_rate = 0.7
        
        # Context integration (optional, for v2)
        if self.context_service and config.version == MotorVersion.V2:
            try:
                history = self.context_service.get_student_history(
                    student_id=student_id,
                    topic_id=topic_id,
                    days_back=30
                )
                
                # Extract timing data if available
                if history.get("tests"):
                    tests = history["tests"]
                    if tests:
                        # Calculate averages from recent tests
                        total_duration = sum(t.get("duration", 300) for t in tests) / len(tests)
                        total_questions = sum(t.get("total", 10) for t in tests) / len(tests)
                        
                        total_correct = sum(t.get("correct", 0) for t in tests)
                        total_all = sum(t.get("total", 1) for t in tests)
                        success_rate = total_correct / max(1, total_all)
                        
            except Exception as ctx_error:
                print(f"Time context fetch warning: {ctx_error}")
                # Continue with defaults
        
        try:
            if config.version == MotorVersion.V2:
                # V2: Context-aware analysis with full parameters
                
                # Get subject_code from context
                subject_code = "unknown"
                if self.context_service:
                    try:
                        topic_ctx = self.context_service.get_topic_context(topic_id)
                        subject_code = topic_ctx.get("subject_code", "unknown")
                    except:
                        pass
                
                result = self.time_v2.analyze(
                    total_duration=total_duration,
                    total_questions=int(total_questions),
                    success_rate=success_rate,
                    student_id=student_id,
                    topic_id=topic_id,
                    subject_code=subject_code,
                    exam_type=None,
                    question_times=None,
                    config=None
                )
            else:
                # V1: Simple analysis
                result = self.time_v1.analyze(
                    total_duration=total_duration,
                    total_questions=int(total_questions),
                    success_rate=success_rate,
                    config=None
                )
            
            execution_time = (time.time() - start_time) * 1000
            
            motor_registry.log_performance(
                motor_type=MotorType.TIME,
                version=config.version,
                success=True,
                execution_time_ms=execution_time,
                user_tier=user_tier.value if hasattr(user_tier, "value") else user_tier
            )
            
            return {
                "data": result,
                "meta": {
                    "motor_version": config.version.value,
                    "fallback_used": False,
                    "tier": user_tier.value
                }
            }
            
        except Exception as e:
            print(f"Time v2 failed, falling back to v1: {e}")
            try:
                result = self.time_v1.analyze(
                    total_duration=total_duration,
                    total_questions=int(total_questions),
                    success_rate=success_rate,
                    config=None
                )
                
                return {
                    "data": result,
                    "meta": {
                        "motor_version": "v1",
                        "fallback_used": True,
                        "tier": user_tier.value,
                        "fallback_reason": str(e)
                    }
                }
            except Exception as e2:
                print(f"Time v1 also failed: {e2}")
                raise

    def calculate_priority(
        self,
        student_id: str,
        topic_id: str,
        test_date: str,
        user_tier: UserTier
    ) -> dict:
        """Calculate Priority score with v1/v2 selection + CONTEXT"""
        
        from app.core.priority_engine_v1 import TopicInput
        
        # Context integration: Get real topic data
        topic_name = "Unknown"
        course_importance = 1.0
        topic_weight = 1.0
        correct = 0
        wrong = 0
        blank = 0
        total_questions = 1
        
        if self.context_service:
            try:
                # Get topic context
                topic_context = self.context_service.get_topic_context(topic_id)
                topic_name = topic_context.get("name", "Unknown")
                
                # Get student history for this topic
                history = self.context_service.get_student_history(
                    student_id=student_id,
                    topic_id=topic_id,
                    days_back=30
                )
                
                # Extract performance data
                if history.get("tests"):
                    tests = history["tests"]
                    if tests:
                        # Use most recent test or aggregate
                        total_questions = sum(t.get("total", 0) for t in tests)
                        correct = sum(t.get("correct", 0) for t in tests)
                        wrong = sum(t.get("wrong", 0) for t in tests)
                        blank = sum(t.get("blank", 0) for t in tests)
                        
                        # Calculate weights from context
                        topic_weight = topic_context.get("difficulty_baseline", 1.0) / 10.0
                        course_importance = 1.0  # TODO: Get from exam_weights
                        
            except Exception as ctx_error:
                print(f"Priority context fetch warning: {ctx_error}")
                # Continue with defaults
        
        # TopicInput with real data
        topic = TopicInput(
            id=topic_id,
            name=topic_name,
            course_importance=course_importance,
            topic_weight=topic_weight,
            correct=correct,
            wrong=wrong,
            blank=blank,
            total_questions=max(1, total_questions)
        )
        
        config = motor_registry.get_motor_config(
            motor_type=MotorType.PRIORITY,
            user_tier=SubscriptionTier(user_tier.value),
            user_id=student_id
        )
        
        start_time = time.time()
        
        try:
            if config.version == MotorVersion.V2:
                # V2: batch + student_id + context
                result = self.priority_v2.analyze(
                    topics=[topic],
                    student_id=student_id,
                    config=None
                )
            else:
                # V1: sadece batch
                results = self.priority_v1.analyze(
                    topics=[topic],
                    config=None
                )
                result = results[0] if results else {}
            
            execution_time = (time.time() - start_time) * 1000
            
            motor_registry.log_performance(
                motor_type=MotorType.PRIORITY,
                version=config.version,
                success=True,
                execution_time_ms=execution_time,
                user_tier=user_tier.value
            )
            
            return {
                "data": result,
                "meta": {
                    "motor_version": config.version.value,
                    "fallback_used": False,
                    "tier": user_tier.value
                }
            }
            
        except Exception as e:
            print(f"Priority v2 failed, falling back to v1: {e}")
            try:
                results = self.priority_v1.analyze(topics=[topic], config=None)
                result = results[0] if results else {}
                
                return {
                    "data": result,
                    "meta": {
                        "motor_version": "v1",
                        "fallback_used": True,
                        "tier": user_tier.value,
                        "fallback_reason": str(e)
                    }
                }
            except Exception as e2:
                print(f"Priority v1 also failed: {e2}")
                raise

    def calculate_bs_model(
        self,
        input_data,
        student_id: str,
        topic_id: str,
        user_tier: UserTier
    ) -> dict:
        """Calculate BS-Model score with v1/v2 selection + CONTEXT"""
        
        config = motor_registry.get_motor_config(
            motor_type=MotorType.BS_MODEL,
            user_tier=SubscriptionTier(user_tier.value),
            user_id=student_id
        )
        
        start_time = time.time()
        
        try:
            if config.version == MotorVersion.V2:
                # Context integration
                test_history = None
                last_test_date = None
                
                if self.context_service:
                    try:
                        history = self.context_service.get_student_history(
                            student_id=student_id,
                            topic_id=topic_id,
                            days_back=30
                        )
                        
                        if history.get("last_test_date"):
                            from datetime import datetime
                            last_test_date = datetime.fromisoformat(
                                history["last_test_date"].replace("Z", "+00:00")
                            )
                        
                        test_history = history.get("tests", [])
                    except Exception as ctx_error:
                        print(f"Context fetch warning: {ctx_error}")
                
                result = self.bs_model_v2.calculate(
                    input_data=input_data,
                    student_id=student_id,
                    topic_id=topic_id,
                    analysis_allowed=True,
                    test_history=test_history,
                    k_forget_prev=None,
                    last_test_date=last_test_date,
                    config=None
                )
            else:
                result = self.bs_model_v1.calculate(input_data)
            
            execution_time = (time.time() - start_time) * 1000
            
            motor_registry.log_performance(
                motor_type=MotorType.BS_MODEL,
                version=config.version,
                success=True,
                execution_time_ms=execution_time,
                user_tier=user_tier.value
            )
            
            return {
                "data": result,
                "meta": {
                    "motor_version": config.version.value,
                    "fallback_used": False,
                    "tier": user_tier.value
                }
            }
            
        except Exception as e:
            print(f"BS-Model v2 failed, falling back to v1: {e}")
            result = self.bs_model_v1.calculate(input_data)
            
            return {
                "data": result,
                "meta": {
                    "motor_version": "v1",
                    "fallback_used": True,
                    "tier": user_tier.value,
                    "fallback_reason": "v2_exception"
                }
            }

    def calculate_difficulty(
        self,
        input_data,
        student_id: Optional[str] = None,
        user_tier: UserTier = UserTier.FREE,
        config: Optional[object] = None
    ) -> Dict:
        """
        Calculate difficulty with automatic v1/v2 selection + emergency fallback
        """
        
        try:
            # Check if v2 available
            if not self._can_use_v2(user_tier, student_id):
                result = self.difficulty_v1.calculate(input_data, config)
                return self._envelope_response(result, "v1", False, user_tier)
            
            # Try v2, fallback to v1 on error
            try:
                result = self.difficulty_v2.calculate(input_data, student_id, config)
                return self._envelope_response(result, "v2", False, user_tier)
            except Exception as e:
                logger.error(f"Difficulty v2 failed, falling back to v1: {e}")
                result = self.difficulty_v1.calculate(input_data, config)
                return self._envelope_response(
                    result, "v1", True, user_tier,
                    fallback_reason="v2_exception"
                )
        
        except Exception as e:
            # EMERGENCY: Wrapper completely failed
            logger.critical(
                f"MotorWrapper.calculate_difficulty failed completely, "
                f"emergency v1 engaged: {e}"
            )
            return self._emergency_v1_difficulty(input_data, config, str(e), user_tier)
    
    # ========================================
    # BS-MODEL MOTOR
    # ========================================
    
