"""
Motor Logging Test Endpoint
Sadece logging sistemini test etmek için basit endpoint
"""
from fastapi import APIRouter, Query
from app.core.motor_wrapper import MotorWrapper
from app.core.motor_registry import MotorType, MotorVersion, SubscriptionTier
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/test-logging")
async def test_motor_logging(
    user_id: str = Query(default="test-user-123"),
    topic_id: str = Query(default="test-topic-456"),
    tier: str = Query(default="premium")
):
    """
    🧪 Motor logging test endpoint
    
    Basit bir motor çağrısı yapar ve logging sistemini test eder.
    """
    
    logger.info(f"🧪 Testing motor logging: user={user_id}, topic={topic_id}, tier={tier}")
    
    try:
        # SubscriptionTier enum'a çevir
        tier_map = {
            "free": SubscriptionTier.FREE,
            "basic": SubscriptionTier.BASIC,
            "medium": SubscriptionTier.MEDIUM,
            "premium": SubscriptionTier.PREMIUM
        }
        user_tier = tier_map.get(tier.lower(), SubscriptionTier.PREMIUM)
        
        # Motor wrapper oluştur (sadece motor_type parametresi)
        wrapper = MotorWrapper(motor_type=MotorType.DIFFICULTY)
        
        # Motor çağrısı yap
        result = await wrapper.execute(
            user_id=user_id,
            topic_id=topic_id,
            tests=[],  # Boş test listesi
            user_tier=user_tier
        )
        
        return {
            "status": "success",
            "message": "Motor logging test completed",
            "result": result,
            "log_file": "logs/motor_activity.log",
            "check_command": "cat logs/motor_activity.log"
        }
        
    except Exception as e:
        logger.error(f"❌ Motor test failed: {e}")
        return {
            "status": "error",
            "message": str(e),
            "log_file": "logs/motor_activity.log"
        }
