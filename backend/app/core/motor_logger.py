"""
Motor Activity Logger
Her motor çağrısını JSON dosyasına kaydeder
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class MotorActivityLogger:
    def __init__(self):
        self.log_file = Path("logs/motor_activity.log")
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log_execution(
        self,
        motor_type: str,
        version: str,
        user_tier: str,
        features_used: int,
        execution_time_ms: float,
        fallback_used: bool,
        user_id: str = None,
        topic_id: str = None,
        success: bool = True,
        error: str = None
    ):
        """Motor çağrısını logla"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "motor_type": motor_type,
            "version": version,
            "user_tier": user_tier,
            "features_used": features_used,
            "execution_time_ms": round(execution_time_ms, 2),
            "fallback_used": fallback_used,
            "success": success,
            "user_id": user_id,
            "topic_id": topic_id,
            "error": error
        }
        
        # Append to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

# Global instance
motor_logger = MotorActivityLogger()
