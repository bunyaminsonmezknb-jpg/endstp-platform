"""
Motor Registry v2.0
===================

Central registry for motor management with:
- Motor version selection (v1/v2)
- Subscription tier mapping
- Override mechanism (admin control)
- Performance tracking

LOCK DATE: 2025-01-03
VERSION: 2.0
"""

from typing import Dict, Type, Optional, List, Any
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# ========================================
# ENUMS
# ========================================

class MotorType(str, Enum):
    """Motor types"""
    DIFFICULTY = "difficulty"
    BS_MODEL = "bs_model"
    PRIORITY = "priority"
    TIME = "time"


class MotorVersion(str, Enum):
    """Motor versions"""
    V1 = "v1"
    V2 = "v2"


class SubscriptionTier(str, Enum):
    """User subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    MEDIUM = "medium"
    PREMIUM = "premium"
    INSTITUTION = "institution"


# ========================================
# MOTOR CONFIG
# ========================================

class MotorConfig:
    """Motor configuration for a specific user/tier"""
    
    def __init__(
        self,
        motor_type: MotorType,
        version: MotorVersion,
        enabled_features: List[str],
        timeout_ms: int = 5000,
        fallback_enabled: bool = True
    ):
        self.motor_type = motor_type
        self.version = version
        self.enabled_features = enabled_features
        self.timeout_ms = timeout_ms
        self.fallback_enabled = fallback_enabled


# ========================================
# MOTOR REGISTRY
# ========================================

class MotorRegistry:
    """
    Central registry for all motors
    
    Features:
    - Motor class registration
    - Version selection based on tier
    - Admin override mechanism
    - Performance tracking
    """
    
    def __init__(self):
        # Motor classes registry
        # {motor_name: {version: class}}
        self._registry: Dict[str, Dict[int, Type]] = {}
        
        # Override settings
        # {"global": {"difficulty": "v2"}, "user-123": {"priority": "v1"}}
        self.override_settings: Dict[str, Dict[str, str]] = {}
        
        # Performance log
        self.performance_log: List[Dict[str, Any]] = []
        
        # Tier to version mapping
        self._tier_mapping = {
            SubscriptionTier.FREE: MotorVersion.V1,
            SubscriptionTier.BASIC: MotorVersion.V1,
            SubscriptionTier.MEDIUM: MotorVersion.V1,
            SubscriptionTier.PREMIUM: MotorVersion.V2,
            SubscriptionTier.INSTITUTION: MotorVersion.V2
        }
    
    # ========================================
    # REGISTRATION
    # ========================================
    
    def register(self, motor_name: str, version: int, motor_cls: Type) -> None:
        """
        Register a motor class
        
        Args:
            motor_name: Motor name (difficulty, priority, etc.)
            version: Version number (1, 2)
            motor_cls: Motor class reference
        """
        motor_name = motor_name.lower()
        
        if motor_name not in self._registry:
            self._registry[motor_name] = {}
        
        self._registry[motor_name][version] = motor_cls
        
        logger.debug(
            f"Motor registered: {motor_name} v{version} -> {motor_cls.__name__}"
        )
    
    # ========================================
    # VERSION SELECTION
    # ========================================
    
    def get_motor_version(
        self,
        motor_type: MotorType,
        user_tier: SubscriptionTier,
        user_id: Optional[str] = None
    ) -> MotorVersion:
        """
        Get motor version for user
        
        Priority:
        1. User-specific override
        2. Global override
        3. Tier-based default
        """
        # Check user-specific override
        if user_id and user_id in self.override_settings:
            if motor_type.value in self.override_settings[user_id]:
                return MotorVersion(self.override_settings[user_id][motor_type.value])
        
        # Check global override
        if "global" in self.override_settings:
            if motor_type.value in self.override_settings["global"]:
                return MotorVersion(self.override_settings["global"][motor_type.value])
        
        # Default: tier-based
        return self._tier_mapping.get(user_tier, MotorVersion.V1)
    
    def get_motor_config(
        self,
        motor_type: MotorType,
        user_tier: SubscriptionTier,
        user_id: Optional[str] = None
    ) -> MotorConfig:
        """
        Get complete motor configuration
        """
        version = self.get_motor_version(motor_type, user_tier, user_id)
        
        # Feature mapping based on version
        if version == MotorVersion.V2:
            features = ["context", "segmentation", "prerequisites"]
        else:
            features = ["basic"]
        
        return MotorConfig(
            motor_type=motor_type,
            version=version,
            enabled_features=features,
            timeout_ms=5000,
            fallback_enabled=True
        )
    
    # ========================================
    # OVERRIDE MANAGEMENT
    # ========================================
    
    def set_override(
        self,
        target: str,
        motor_type: MotorType,
        version: MotorVersion
    ) -> None:
        """
        Set motor version override
        
        Args:
            target: "global" or user_id
            motor_type: Motor type
            version: Version to force
        """
        if target not in self.override_settings:
            self.override_settings[target] = {}
        
        self.override_settings[target][motor_type.value] = version.value
        
        logger.info(
            f"Override set: {target} -> {motor_type.value} = {version.value}"
        )
    
    def clear_override(self, target: str) -> None:
        """Clear all overrides for target"""
        if target in self.override_settings:
            del self.override_settings[target]
            logger.info(f"Override cleared: {target}")
    
    # ========================================
    # PERFORMANCE TRACKING
    # ========================================
    
    def log_performance(
        self,
        motor_type: MotorType,
        version: MotorVersion,
        execution_time_ms: float,
        success: bool,
        user_tier: SubscriptionTier
    ) -> None:
        """Log motor performance"""
        self.performance_log.append({
            "motor_type": motor_type.value,
            "version": version.value,
            "execution_time_ms": execution_time_ms,
            "success": success,
            "user_tier": user_tier.value if hasattr(user_tier, "value") else user_tier,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 1000 entries
        if len(self.performance_log) > 1000:
            self.performance_log = self.performance_log[-1000:]
    
    # ========================================
    # MOTOR LOOKUP
    # ========================================
    
    def get(self, motor_name: str, version: int) -> Type:
        """
        Get motor class by name and version
        
        Raises:
            KeyError if not found
        """
        motor_name = motor_name.lower()
        
        if motor_name not in self._registry:
            raise KeyError(f"Motor '{motor_name}' not registered")
        
        if version not in self._registry[motor_name]:
            raise KeyError(
                f"Motor '{motor_name}' version {version} not registered"
            )
        
        return self._registry[motor_name][version]
    
    def get_or_fallback(
        self,
        motor_name: str,
        preferred_version: int,
        fallback_version: int = 1
    ) -> Optional[Type]:
        """
        Try preferred version, fallback if not found
        """
        try:
            return self.get(motor_name, preferred_version)
        except KeyError:
            logger.warning(
                f"Motor {motor_name} v{preferred_version} not found, "
                f"falling back to v{fallback_version}"
            )
            try:
                return self.get(motor_name, fallback_version)
            except KeyError:
                logger.error(
                    f"Fallback motor {motor_name} v{fallback_version} "
                    f"also not found"
                )
                return None
    
    # ========================================
    # INTROSPECTION
    # ========================================
    
    def list_motors(self) -> Dict[str, Dict[int, str]]:
        """List all registered motors"""
        return {
            motor: {
                version: cls.__name__
                for version, cls in versions.items()
            }
            for motor, versions in self._registry.items()
        }


# ========================================
# GLOBAL INSTANCE
# ========================================

motor_registry = MotorRegistry()