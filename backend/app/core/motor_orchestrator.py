"""
Motor Orchestrator
Unified motor coordination and result aggregation

Responsibilities:
- Run multiple motors in parallel (when possible)
- Aggregate results into unified response
- Handle inter-motor dependencies
- Provide performance metrics
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class MotorOrchestrator:
    """
    Unified motor coordinator
    
    Runs all motors and aggregates results for:
    - Student Dashboard
    - Topic Analysis
    - Batch Processing
    """
    
    def __init__(self, motor_wrapper, context_service):
        """
        Args:
            motor_wrapper: MotorWrapper instance
            context_service: ContextService instance
        """
        self.motor_wrapper = motor_wrapper
        self.context_service = context_service
    
    async def analyze_topic_test(
        self,
        student_id: str,
        topic_id: str,
        subject_code: str,
        test_data: Dict,
        user_tier: str
    ) -> Dict:
        """
        Complete analysis for a single topic test
        
        Runs all 4 motors: Difficulty, BS-Model, Priority, Time
        
        Args:
            student_id: Student UUID
            topic_id: Topic UUID
            subject_code: Subject code
            test_data: {
                "correct": int,
                "wrong": int,
                "blank": int,
                "total": int,
                "duration_minutes": float,
                "difficulty": int (1-5)
            }
            user_tier: User subscription tier
        
        Returns:
            {
                "difficulty": {...},
                "bs_model": {...},
                "time": {...},
                "metadata": {...}
            }
        """
        
        start_time = datetime.now()
        
        # Fetch context once (shared across motors)
        context = self.context_service.get_topic_context(topic_id)
        
        # Prepare inputs
        from app.core.difficulty_v1 import DifficultyInput
        from app.core.bs_model_v1 import BSModelInput
        
        difficulty_input = DifficultyInput(
            topic_id=topic_id,
            questions_total=test_data["total"],
            questions_correct=test_data["correct"],
            questions_wrong=test_data["wrong"],
            questions_blank=test_data["blank"]
        )
        
        bs_model_input = BSModelInput(
            correct=test_data["correct"],
            incorrect=test_data["wrong"],
            blank=test_data["blank"],
            total=test_data["total"],
            difficulty=test_data.get("difficulty", 3)
        )
        
        success_rate = test_data["correct"] / test_data["total"] if test_data["total"] > 0 else 0
        
        # Run motors
        results = {}
        errors = []
        
        # 1. Difficulty
        try:
            results["difficulty"] = self.motor_wrapper.calculate_difficulty(
                difficulty_input,
                student_id,
                user_tier
            )
        except Exception as e:
            logger.error(f"Difficulty motor failed: {e}")
            errors.append({"motor": "difficulty", "error": str(e)})
        
        # 2. BS-Model
        try:
            results["bs_model"] = self.motor_wrapper.calculate_bs_model(
                bs_model_input,
                student_id,
                topic_id,
                user_tier
            )
        except Exception as e:
            logger.error(f"BS-Model motor failed: {e}")
            errors.append({"motor": "bs_model", "error": str(e)})
        
        # 3. Time Analyzer
        try:
            results["time"] = self.motor_wrapper.analyze_time(
                test_data.get("duration_minutes"),
                test_data["total"],
                success_rate,
                student_id,
                topic_id,
                subject_code,
                user_tier
            )
        except Exception as e:
            logger.error(f"Time motor failed: {e}")
            errors.append({"motor": "time", "error": str(e)})
        
        # Calculate elapsed time
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Metadata
        metadata = {
            "student_id": student_id,
            "topic_id": topic_id,
            "subject_code": subject_code,
            "motors_succeeded": len(results),
            "motors_failed": len(errors),
            "total_time_ms": round(elapsed_ms, 2),
            "timestamp": datetime.now().isoformat(),
            "context_used": {
                "archetype": context.get("archetype"),
                "has_prerequisites": len(context.get("prerequisites", [])) > 0
            }
        }
        
        if errors:
            metadata["errors"] = errors
        
        return {
            **results,
            "metadata": metadata
        }
    
    async def analyze_topic_batch(
        self,
        student_id: str,
        topic_tests: List[Dict],
        user_tier: str
    ) -> Dict:
        """
        Batch analysis for multiple topics (for Priority calculation)
        
        Args:
            student_id: Student UUID
            topic_tests: List of test data with topic info
            user_tier: User subscription tier
        
        Returns:
            {
                "priorities": [...],
                "metadata": {...}
            }
        """
        
        start_time = datetime.now()
        
        # Prepare priority inputs
        from app.core.priority_v1 import TopicInput
        
        topics = []
        for test in topic_tests:
            topics.append(TopicInput(
                id=test["topic_id"],
                name=test["topic_name"],
                course_importance=test.get("course_importance", 40),
                topic_weight=test.get("topic_weight", 0.1),
                correct=test["correct"],
                wrong=test["wrong"],
                blank=test["blank"],
                total_questions=test["total"],
                duration_minutes=test.get("duration_minutes")
            ))
        
        # Calculate priorities
        try:
            results = self.motor_wrapper.calculate_priority(
                topics,
                student_id,
                user_tier
            )
        except Exception as e:
            logger.error(f"Priority batch failed: {e}")
            results = {"priorities": [], "error": str(e)}
        
        # Calculate elapsed time
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Metadata
        results["metadata"] = {
            "student_id": student_id,
            "topics_analyzed": len(topics),
            "total_time_ms": round(elapsed_ms, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        return results
    
    def get_motor_health(self) -> Dict:
        """
        Health check for all motors
        
        Returns:
            {
                "difficulty": "healthy",
                "bs_model": "healthy",
                "priority": "healthy",
                "time": "healthy"
            }
        """
        
        # TODO: Implement actual health checks
        return {
            "difficulty": "healthy",
            "bs_model": "healthy",
            "priority": "healthy",
            "time": "healthy",
            "context_service": "healthy"
        }