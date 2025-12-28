"""
Motor Integration Tests (Sync Version)
Test motor registry logic without async
"""
import pytest
from app.core.motor_registry import (
    motor_registry,
    MotorType,
    MotorVersion,
    SubscriptionTier
)


class TestMotorIntegrationSync:
    """Test motor wrapper integration (sync)"""
    
    def test_free_tier_config(self):
        """Free tier should get v1 config"""
        config = motor_registry.get_motor_config(
            MotorType.DIFFICULTY,
            SubscriptionTier.FREE
        )
        
        assert config.version == MotorVersion.V1
        assert config.timeout_ms == 500
        assert config.fallback_enabled == True
    
    def test_premium_tier_config(self):
        """Premium tier should get v2 with 15 features"""
        config = motor_registry.get_motor_config(
            MotorType.DIFFICULTY,
            SubscriptionTier.PREMIUM
        )
        
        assert config.version == MotorVersion.V2
        assert len(config.enabled_features) == 15
        assert "trust_weighted" in config.enabled_features
    
    def test_basic_tier_config(self):
        """Basic tier should get v2 with 8 features"""
        config = motor_registry.get_motor_config(
            MotorType.DIFFICULTY,
            SubscriptionTier.BASIC
        )
        
        assert config.version == MotorVersion.V2
        assert len(config.enabled_features) == 8
        assert "prerequisite" in config.enabled_features
        assert "trust_weighted" not in config.enabled_features
    
    def test_override_changes_version(self):
        """Override should change motor version"""
        # Set override
        motor_registry.set_override(
            "test-user",
            MotorType.DIFFICULTY,
            MotorVersion.V2
        )
        
        # Free tier user should get v2
        version = motor_registry.get_motor_version(
            MotorType.DIFFICULTY,
            SubscriptionTier.FREE,
            "test-user"
        )
        
        assert version == MotorVersion.V2
        
        # Cleanup
        motor_registry.clear_override("test-user")
