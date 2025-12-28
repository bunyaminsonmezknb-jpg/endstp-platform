"""
Motor Integration Tests
Test actual motor execution with wrapper
"""
import pytest
from app.core.motor_wrapper import MotorWrapper
from app.core.motor_registry import MotorType, SubscriptionTier


class TestMotorIntegration:
    """Test motor wrapper integration"""
    
    @pytest.mark.asyncio
    async def test_free_tier_uses_v1(self):
        """Free tier should execute v1 motor"""
        wrapper = MotorWrapper(MotorType.DIFFICULTY)
        
        result = await wrapper.execute(
            user_id="test-free-user",
            user_tier=SubscriptionTier.FREE,
            student_id="test-student",
            topic_id="test-topic"
        )
        
        # Should have v1 metadata
        assert result["motor_metadata"]["motor_version"] == "v1"
        assert result["motor_metadata"]["features_used"] == 4
        assert result["difficulty_percentage"] > 0
    
    @pytest.mark.asyncio
    async def test_premium_tier_uses_v2(self):
        """Premium tier should execute v2 motor"""
        wrapper = MotorWrapper(MotorType.DIFFICULTY)
        
        result = await wrapper.execute(
            user_id="test-premium-user",
            user_tier=SubscriptionTier.PREMIUM,
            student_id="test-student",
            topic_id="test-topic"
        )
        
        # Should have v2 metadata
        assert result["motor_metadata"]["motor_version"] == "v2"
        assert result["motor_metadata"]["features_used"] == 15
        assert result["difficulty_percentage"] >= 0
    
    @pytest.mark.asyncio
    async def test_basic_tier_uses_v2_with_8_features(self):
        """Basic tier should use v2 with 8 features"""
        wrapper = MotorWrapper(MotorType.DIFFICULTY)
        
        result = await wrapper.execute(
            user_id="test-basic-user",
            user_tier=SubscriptionTier.BASIC,
            student_id="test-student",
            topic_id="test-topic"
        )
        
        # Should have v2 with limited features
        assert result["motor_metadata"]["motor_version"] == "v2"
        assert result["motor_metadata"]["features_used"] == 8
