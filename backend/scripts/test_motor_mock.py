"""
Motor Test with Mock Data
Mock verilerle motor hesaplaması
"""
import sys
sys.path.insert(0, '/home/endstp/endstp-platform/backend')

from app.core.motor_wrapper import MotorWrapper
from app.core.motor_registry import MotorType, SubscriptionTier
import asyncio


async def test_with_mock():
    """Mock verilerle motor testi"""
    
    print("=" * 60)
    print("MOTOR TEST - Mock Data")
    print("=" * 60)
    
    # Test senaryoları
    scenarios = [
        {
            "name": "FREE Tier - Basit Hesaplama",
            "tier": SubscriptionTier.FREE,
            "expected_version": "v1",
            "expected_features": 4
        },
        {
            "name": "BASIC Tier - 8 Feature",
            "tier": SubscriptionTier.BASIC,
            "expected_version": "v2",
            "expected_features": 8
        },
        {
            "name": "PREMIUM Tier - Full Features",
            "tier": SubscriptionTier.PREMIUM,
            "expected_version": "v2",
            "expected_features": 15
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"TEST: {scenario['name']}")
        print(f"{'='*60}")
        
        wrapper = MotorWrapper(MotorType.DIFFICULTY)
        
        result = await wrapper.execute(
            user_id="mock-student-123",
            user_tier=scenario['tier'],
            student_id="mock-student-123",
            topic_id="mock-topic-456"
        )
        
        # Sonuçları kontrol et
        metadata = result.get('motor_metadata', {})
        
        print(f"✅ Motor Version: {metadata.get('motor_version')}")
        print(f"✅ Features Used: {metadata.get('features_used')}")
        print(f"✅ Fallback Used: {metadata.get('fallback_used')}")
        print(f"\n📊 RESULTS:")
        print(f"   Difficulty: {result.get('difficulty_percentage', 0):.1f}%")
        print(f"   Level: {result.get('difficulty_level', 0)}/5")
        print(f"   Segment: {result.get('student_segment', 'N/A')}")
        print(f"   Message: {result.get('student_message', 'N/A')}")
        
        # Verify
        assert metadata.get('motor_version') == scenario['expected_version'], \
            f"Version mismatch! Expected {scenario['expected_version']}"
        
        if scenario['tier'] != SubscriptionTier.FREE:
            assert metadata.get('features_used') == scenario['expected_features'], \
                f"Features mismatch! Expected {scenario['expected_features']}"
        
        print(f"\n✅ Test PASSED: {scenario['name']}")
    
    print(f"\n{'='*60}")
    print("🎉 ALL TESTS PASSED!")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(test_with_mock())
