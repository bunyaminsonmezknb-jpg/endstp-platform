"""
Motor Wrapper with Automatic Fallback
Wraps v1/v2 motors with error handling and fallback
"""
from typing import Any, Dict, Optional
import time
import logging
from app.core.motor_logger import motor_logger
from app.core.motor_logger import motor_logger
from .motor_registry import (
    motor_registry,
    MotorType,
    MotorVersion,
    SubscriptionTier
)

logger = logging.getLogger(__name__)


class MotorWrapper:
    """
    Wraps motor calls with:
    - Automatic v1/v2 selection
    - Timeout protection
    - Fallback on error
    - Performance logging
    """
    
    def __init__(self, motor_type: MotorType):
        """Initialize wrapper for specific motor type"""
        self.motor_type = motor_type
    
    async def execute(
        self,
        user_id: str,
        user_tier: SubscriptionTier,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute motor with fallback
        
        Flow:
        1. Try v2 (if tier allows)
        2. Fallback to v1 on error/timeout
        3. Return safe default if both fail
        """
        config = motor_registry.get_motor_config(
            self.motor_type,
            user_tier,
            user_id
        )
        
        # Try primary version
        try:
            start_time = time.time()
            
            if config.version == MotorVersion.V2:
                result = await self._execute_v2(config, **kwargs)
            else:
                result = await self._execute_v1(config, **kwargs)
            
            execution_time = (time.time() - start_time) * 1000
            
            # Check timeout
            if execution_time > config.timeout_ms and config.fallback_enabled:
                logger.warning(
                    f"{self.motor_type.value} {config.version.value} "
                    f"timeout ({execution_time:.0f}ms > {config.timeout_ms}ms), "
                    f"falling back to v1"
                )
                return await self._fallback_to_v1(**kwargs)
            
            # Log success
            motor_registry.log_performance(
                self.motor_type,
                config.version,
                execution_time,
                success=True
            )
            
            # Log motor execution
            try:
                motor_logger.log_execution(
                    motor_type=self.motor_type.value,
                    version=config.version.value,
                    user_tier=user_tier.value,
                    features_used=list(config.enabled_features),
                    execution_time_ms=execution_time,
                    fallback_used=False,
                    user_id=user_id,
                    topic_id=kwargs.get("topic_id", "unknown"),
                    success=True,
                    error=None
                )
            except Exception as log_error:
                logger.warning(f"Failed to log motor execution: {log_error}")
            
            return result
            
        except Exception as e:
            logger.error(
                f"{self.motor_type.value} {config.version.value} error: {e}",
                exc_info=True
            )
            
            # Log failure
            motor_registry.log_performance(
                self.motor_type,
                config.version,
                0,
                success=False,
                error=str(e)
            )
            
            # Log to motor_logger
            try:
                motor_logger.log_execution(
                    motor_type=self.motor_type.value,
                    version=config.version.value,
                    user_tier=user_tier.value,
                    features_used=list(config.enabled_features),
                    execution_time_ms=0,
                    fallback_used=False,
                    user_id=user_id,
                    topic_id=kwargs.get("topic_id", "unknown"),
                    success=False,
                    error=str(e)
                )
            except Exception as log_error:
                logger.warning(f"Failed to log motor error: {log_error}")
            
            # Fallback
            if config.version == MotorVersion.V2 and config.fallback_enabled:
                logger.info(f"Falling back to v1 for {self.motor_type.value}")
                return await self._fallback_to_v1(**kwargs)
            else:
                # Both failed, return safe default
                return self._safe_default()
    
    async def _execute_v1(self, config, **kwargs) -> Dict[str, Any]:
        """Execute v1 motor"""
        if self.motor_type == MotorType.DIFFICULTY:
            from .difficulty_engine import DifficultyEngineV1
            engine = DifficultyEngineV1()
            return engine.calculate(**kwargs)
        
        # TODO: Add other motors
        raise NotImplementedError(f"v1 not implemented for {self.motor_type.value}")
    
    async def _execute_v2(self, config, **kwargs) -> Dict[str, Any]:
        """Execute v2 motor with tier-based features"""
        if self.motor_type == MotorType.DIFFICULTY:
            from .difficulty_engine_v2 import MasterDifficultyEngine
            
            # Enable features based on tier
            feature_flags = {
                "enable_prerequisite": "prerequisite" in config.enabled_features,
                "enable_bs_model": "bs_model" in config.enabled_features,
                "enable_course_context": "course_context" in config.enabled_features,
                "enable_speed": "speed" in config.enabled_features,
                "enable_metacognition": "metacognition" in config.enabled_features,
                "enable_digital_exhaust": "digital_exhaust" in config.enabled_features,
                "enable_circadian": "circadian" in config.enabled_features,
            }
            
            engine = MasterDifficultyEngine(**feature_flags)
            from datetime import datetime, timezone, date
            from .difficulty_engine_v2 import TestData
            
            mock_tests = [TestData(
                test_id="mock-test-1",
                topic_id=kwargs.get("topic_id", "mock-topic"),
                test_date=date.today(),
                entry_timestamp=datetime.now(timezone.utc),
                total_questions=10,
                correct=7,
                wrong=2,
                blank=1,
                time_seconds=480
            )]
            
            result = engine.calculate_difficulty(
                student_id=kwargs.get("student_id"),
                topic_id=kwargs.get("topic_id"),
                tests=mock_tests
            )
            
            # Convert to dict
            return {
                "difficulty_percentage": result.difficulty_percentage,
                "difficulty_level": result.difficulty_level,
                "student_segment": result.student_segment.value,
                "behavior_mode": result.behavior_mode.value,
                "trend": result.trend.value,
                "student_message": result.student_message,
                "coach_message": result.coach_message,
                "recommendations": result.recommendations,
                "confidence_level": result.confidence_level,
                "warnings": result.warnings,
                "motor_metadata": {
                    "motor_version": config.version.value,
                    "features_used": len(config.enabled_features),
                    "fallback_used": False
                }
            }
        
        # TODO: Add other motors
        raise NotImplementedError(f"v2 not implemented for {self.motor_type.value}")
    
    async def _fallback_to_v1(self, **kwargs) -> Dict[str, Any]:
        """Fallback to v1"""
        logger.info(f"Executing v1 fallback for {self.motor_type.value}")
        
        from .difficulty_engine import DifficultyEngineV1
        engine = DifficultyEngineV1()
        result = engine.calculate(**kwargs)
        
        # Add fallback metadata
        result["motor_metadata"] = {
            "motor_version": "v1",
            "features_used": 4,
            "fallback_used": True
        }
        
        # Log motor execution
        try:
            motor_logger.log_execution(
                motor_type=self.motor_type.value,
                version="v1",
                user_tier="unknown",  # Fallback'te tier bilinmiyor
                features_used=[],
                execution_time_ms=0,  # Ölçülmedi
                fallback_used=True,
                user_id=kwargs.get("user_id", "unknown"),
                topic_id=kwargs.get("topic_id", "unknown"),
                success=True,
                error=None
            )
        except Exception as log_error:
            logger.warning(f"Failed to log fallback execution: {log_error}")
        
        return result
    
    def _safe_default(self) -> Dict[str, Any]:
        """Safe default when all motors fail"""
        logger.error(f"All motors failed for {self.motor_type.value}, returning safe default")
        
        return {
            "difficulty_percentage": 50.0,
            "difficulty_level": 3,
            "student_message": "Unable to calculate precise difficulty. Please try again.",
            "motor_metadata": {
                "motor_version": "safe_default",
                "features_used": 0,
                "fallback_used": True,
                "error": "All motors failed"
            }
        }
