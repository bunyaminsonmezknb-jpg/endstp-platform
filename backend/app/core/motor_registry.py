"""
Motor Registry System
Manages v1/v2 motor selection, fallback, and performance monitoring
"""
from typing import Dict, Optional, Any, Literal
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class MotorVersion(Enum):
    """Motor versions"""
    V1 = "v1"
    V2 = "v2"


class MotorType(Enum):
    """Available motor types"""
    DIFFICULTY = "difficulty"
    PRIORITY = "priority"
    SPEED = "speed"
    BS_MODEL = "bs_model"


class SubscriptionTier(Enum):
    """Subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    MEDIUM = "medium"
    PREMIUM = "premium"


@dataclass
class MotorConfig:
    """Motor configuration"""
    motor_type: MotorType
    version: MotorVersion
    enabled_features: list[str]
    timeout_ms: int = 500
    fallback_enabled: bool = True


class MotorRegistry:
    """
    Central motor management system
    
    Features:
    - Automatic v1/v2 selection based on tier
    - Fallback on error/timeout
    - Performance monitoring
    - Admin override support
    """
    
    # Tier-based motor versions
    TIER_MOTOR_MAP: Dict[SubscriptionTier, Dict[MotorType, MotorVersion]] = {
        SubscriptionTier.FREE: {
            MotorType.DIFFICULTY: MotorVersion.V1,
            MotorType.PRIORITY: MotorVersion.V1,
            MotorType.SPEED: MotorVersion.V1,
            MotorType.BS_MODEL: MotorVersion.V1,
        },
        SubscriptionTier.BASIC: {
            MotorType.DIFFICULTY: MotorVersion.V2,
            MotorType.PRIORITY: MotorVersion.V2,
            MotorType.SPEED: MotorVersion.V1,
            MotorType.BS_MODEL: MotorVersion.V1,
        },
        SubscriptionTier.MEDIUM: {
            MotorType.DIFFICULTY: MotorVersion.V2,
            MotorType.PRIORITY: MotorVersion.V2,
            MotorType.SPEED: MotorVersion.V2,
            MotorType.BS_MODEL: MotorVersion.V2,
        },
        SubscriptionTier.PREMIUM: {
            MotorType.DIFFICULTY: MotorVersion.V2,
            MotorType.PRIORITY: MotorVersion.V2,
            MotorType.SPEED: MotorVersion.V2,
            MotorType.BS_MODEL: MotorVersion.V2,
        },
    }
    
    # Feature counts per tier
    TIER_FEATURES: Dict[SubscriptionTier, Dict[MotorType, int]] = {
        SubscriptionTier.FREE: {
            MotorType.DIFFICULTY: 4,   # Base + statistical + volatility + sentinel
        },
        SubscriptionTier.BASIC: {
            MotorType.DIFFICULTY: 8,   # + prerequisite + bs_model + course + exam
        },
        SubscriptionTier.MEDIUM: {
            MotorType.DIFFICULTY: 12,  # + speed + metacog + digital + circadian
        },
        SubscriptionTier.PREMIUM: {
            MotorType.DIFFICULTY: 15,  # ALL features
        },
    }
    
    def __init__(self):
        """Initialize motor registry"""
        self.performance_log: list[Dict] = []
        self.override_settings: Dict[str, Any] = {}
    
    def get_motor_version(
        self,
        motor_type: MotorType,
        user_tier: SubscriptionTier,
        user_id: Optional[str] = None
    ) -> MotorVersion:
        """
        Determine which motor version to use
        
        Priority:
        1. User-specific override (admin)
        2. Global override (maintenance mode)
        3. Tier-based auto-selection
        """
        # Check user override
        if user_id and user_id in self.override_settings:
            override = self.override_settings[user_id].get(motor_type.value)
            if override:
                logger.info(f"User override: {user_id} → {motor_type.value} = {override}")
                return MotorVersion(override)
        
        # Check global override
        global_override = self.override_settings.get("global", {}).get(motor_type.value)
        if global_override:
            logger.info(f"Global override: {motor_type.value} = {global_override}")
            return MotorVersion(global_override)
        
        # Tier-based selection
        return self.TIER_MOTOR_MAP[user_tier][motor_type]
    
    def get_motor_config(
        self,
        motor_type: MotorType,
        user_tier: SubscriptionTier,
        user_id: Optional[str] = None
    ) -> MotorConfig:
        """Get complete motor configuration"""
        version = self.get_motor_version(motor_type, user_tier, user_id)
        
        # Get enabled features for this tier
        feature_count = self.TIER_FEATURES.get(user_tier, {}).get(motor_type, 4)
        
        # Build feature list (for v2 motors)
        enabled_features = []
        if version == MotorVersion.V2:
            all_features = [
                "base", "statistical", "volatility", "sentinel",  # 4 (FREE)
                "prerequisite", "bs_model", "course_context", "exam_system",  # +4 (BASIC)
                "speed", "metacognition", "digital_exhaust", "circadian",  # +4 (MEDIUM)
                "trust_weighted", "recovery_velocity", "ai_insights"  # +3 (PREMIUM)
            ]
            enabled_features = all_features[:feature_count]
        
        return MotorConfig(
            motor_type=motor_type,
            version=version,
            enabled_features=enabled_features,
            timeout_ms=500,
            fallback_enabled=True
        )
    
    def set_override(
        self,
        target: Literal["global"] | str,
        motor_type: MotorType,
        version: MotorVersion
    ):
        """
        Set motor override (admin only)
        
        Args:
            target: "global" or user_id
            motor_type: Which motor
            version: Force v1 or v2
        """
        if target not in self.override_settings:
            self.override_settings[target] = {}
        
        self.override_settings[target][motor_type.value] = version.value
        logger.warning(f"Override set: {target} → {motor_type.value} = {version.value}")
    
    def clear_override(self, target: Literal["global"] | str):
        """Clear override"""
        if target in self.override_settings:
            del self.override_settings[target]
            logger.info(f"Override cleared: {target}")
    
    def log_performance(
        self,
        motor_type: MotorType,
        version: MotorVersion,
        execution_time_ms: float,
        success: bool,
        error: Optional[str] = None
    ):
        """Log motor performance"""
        self.performance_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "motor_type": motor_type.value,
            "version": version.value,
            "execution_time_ms": execution_time_ms,
            "success": success,
            "error": error
        })
        
        # Keep only last 1000 entries
        if len(self.performance_log) > 1000:
            self.performance_log = self.performance_log[-1000:]


# Global instance
motor_registry = MotorRegistry()
