"""
Motor Strategy Tests
Test v1/v2 selection, fallback, and tier logic
"""
import pytest
from app.core.motor_registry import (
    motor_registry,
    MotorType,
    MotorVersion,
    SubscriptionTier
)


class TestMotorRegistry:
    """Test motor registry logic"""
    
    def test_free_tier_gets_v1(self):
        """Free tier should get v1 motors"""
        version = motor_registry.get_motor_version(
            MotorType.DIFFICULTY,
            SubscriptionTier.FREE
        )
        assert version == MotorVersion.V1
    
    def test_premium_tier_gets_v2(self):
        """Premium tier should get v2 motors"""
        version = motor_registry.get_motor_version(
            MotorType.DIFFICULTY,
            SubscriptionTier.PREMIUM
        )
        assert version == MotorVersion.V2
    
    def test_global_override(self):
        """Global override should force version"""
        # Set override
        motor_registry.set_override(
            "global",
            MotorType.DIFFICULTY,
            MotorVersion.V1
        )
        
        # Even premium should get v1
        version = motor_registry.get_motor_version(
            MotorType.DIFFICULTY,
            SubscriptionTier.PREMIUM
        )
        assert version == MotorVersion.V1
        
        # Cleanup
        motor_registry.clear_override("global")
    
    def test_user_override(self):
        """User override should override tier"""
        user_id = "test-user-123"
        
        # Set user override
        motor_registry.set_override(
            user_id,
            MotorType.DIFFICULTY,
            MotorVersion.V2
        )
        
        # Free tier user should get v2
        version = motor_registry.get_motor_version(
            MotorType.DIFFICULTY,
            SubscriptionTier.FREE,
            user_id
        )
        assert version == MotorVersion.V2
        
        # Cleanup
        motor_registry.clear_override(user_id)
    
    def test_tier_feature_counts(self):
        """Different tiers get different feature counts"""
        # Free: 4 features
        config_free = motor_registry.get_motor_config(
            MotorType.DIFFICULTY,
            SubscriptionTier.FREE
        )
        assert len(config_free.enabled_features) == 0  # v1 has no feature list
        
        # Basic: 8 features
        config_basic = motor_registry.get_motor_config(
            MotorType.DIFFICULTY,
            SubscriptionTier.BASIC
        )
        assert len(config_basic.enabled_features) == 8
        
        # Premium: 15 features
        config_premium = motor_registry.get_motor_config(
            MotorType.DIFFICULTY,
            SubscriptionTier.PREMIUM
        )
        assert len(config_premium.enabled_features) == 15
