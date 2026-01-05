"""
Context Service
Provides rich context data for v2 motors
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from app.db.session import get_supabase_admin

logger = logging.getLogger(__name__)


class ContextService:
    """
    Centralized context provider for v2 motors
    """

    def __init__(self):
        """Initialize context service with admin Supabase client"""
        self.supabase = get_supabase_admin()
        self._cache: Dict[str, tuple] = {}
        self._cache_ttl: int = 300  # seconds (5 min)
        logger.info("🔒 ContextService initialized with ADMIN CLIENT")

    # ========================================
    # TOPIC CONTEXT
    # ========================================

    def get_topic_context(self, topic_id: str) -> Dict[str, Any]:
        """
        Get comprehensive topic context
        
        Returns:
            {
                "topic_id": str,
                "archetype": str,
                "difficulty_baseline": float,
                "prerequisites": List[Dict],
                "common_misconceptions": List[str],
                "metadata": Dict
            }
        """
        cache_key = f"topic_context:{topic_id}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        try:
            topic_result = (
                self.supabase
                .table("topics")
                .select("id, code, name_tr, difficulty_level")
                .eq("id", topic_id)
                .execute()
            )

            if not topic_result.data:
                return self._default_topic_context(topic_id)

            topic = topic_result.data[0]

            prereq_result = (
                self.supabase
                .table("prerequisites")
                .select("prerequisite_topic_id, strength")
                .eq("topic_id", topic_id)
                .execute()
            )

            context = {
                "topic_id": topic_id,
                "code": topic.get("code"),
                "name": topic.get("name_tr"),
                "archetype": self._infer_archetype(topic),
                "difficulty_baseline": float(topic.get("difficulty_level", 5)),
                "prerequisites": [
                    {
                        "topic_id": p["prerequisite_topic_id"],
                        "strength": float(p.get("strength", 0.5))
                    }
                    for p in (prereq_result.data or [])
                ],
                "common_misconceptions": [],
                "metadata": {}
            }

            self._set_cache(cache_key, context)
            return context

        except Exception as e:
            logger.error(f"Error fetching topic context: {e}")
            return self._default_topic_context(topic_id)

    def _infer_archetype(self, topic: Dict) -> str:
        """Infer topic archetype from code"""
        code = (topic.get("code") or "").lower()

        if any(x in code for x in ["form", "denk", "hesap"]):
            return "formula_heavy"
        if any(x in code for x in ["kav", "teor", "ilke"]):
            return "concept_based"
        if any(x in code for x in ["prob", "soru", "örnek"]):
            return "problem_solving"
        return "mixed"

    def _default_topic_context(self, topic_id: str) -> Dict[str, Any]:
        """Default context when data unavailable"""
        return {
            "topic_id": topic_id,
            "archetype": "mixed",
            "difficulty_baseline": 5.0,
            "prerequisites": [],
            "common_misconceptions": [],
            "metadata": {"fallback": True}
        }

    # ========================================
    # STUDENT HISTORY
    # ========================================

    def get_student_history(
        self,
        student_id: str,
        topic_id: Optional[str] = None,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Get student's learning history
        
        Returns:
            {
                "student_id": str,
                "topic_id": Optional[str],
                "test_count": int,
                "avg_success_rate": float,
                "trend": str,
                "last_test_date": Optional[str],
                "study_patterns": Dict
            }
        """
        cache_key = f"student_history:{student_id}:{topic_id}:{days_back}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        try:
            query = (
                self.supabase
                .table("topic_test_results")
                .select("questions_correct, questions_total, time_spent_seconds, entry_timestamp")
                .eq("user_id", student_id)
            )

            if topic_id:
                query = query.eq("topic_id", topic_id)

            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            result = query.gte("entry_timestamp", cutoff_date).execute()

            if not result.data:
                return self._default_student_history(student_id, topic_id)

            tests = result.data
            success_rates = [
                (t["questions_correct"] / t["questions_total"] * 100)
                if t["questions_total"] > 0 else 0
                for t in tests
            ]

            avg_success = sum(success_rates) / len(success_rates)
            trend = "stable"

            if len(success_rates) >= 10:
                recent_avg = sum(success_rates[-5:]) / 5
                old_avg = sum(success_rates[:5]) / 5
                
                if recent_avg > old_avg + 10:
                    trend = "improving"
                elif recent_avg < old_avg - 10:
                    trend = "declining"

            history = {
                "student_id": student_id,
                "topic_id": topic_id,
                "test_count": len(tests),
                "avg_success_rate": round(avg_success, 2),
                "trend": trend,
                "last_test_date": tests[-1]["entry_timestamp"],
                "study_patterns": {
                    "session_length_avg": int(
                        sum(t["time_spent_seconds"] for t in tests) / len(tests)
                    ),
                    "preferred_time": "afternoon"
                }
            }

            self._set_cache(cache_key, history)
            return history

        except Exception as e:
            logger.error(f"Error fetching student history: {e}")
            return self._default_student_history(student_id, topic_id)

    def _default_student_history(self, student_id: str, topic_id: Optional[str]) -> Dict:
        """Default history when data unavailable"""
        return {
            "student_id": student_id,
            "topic_id": topic_id,
            "test_count": 0,
            "avg_success_rate": 0.0,
            "trend": "unknown",
            "last_test_date": None,
            "study_patterns": {},
            "metadata": {"fallback": True}
        }


    # ========================================
    # PREREQUISITES
    # ========================================

    def get_prerequisites(self, topic_id: str) -> List[Dict[str, Any]]:
        """
        Get prerequisite topics for a given topic.
        Used by BS-Model v2.
        
        Returns:
            List of prerequisites with topic_id and strength
        """
        cache_key = f"prerequisites:{topic_id}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        try:
            result = (
                self.supabase
                .table("prerequisites")
                .select("prerequisite_topic_id, strength")
                .eq("topic_id", topic_id)
                .execute()
            )

            prerequisites = [
                {
                    "topic_id": row["prerequisite_topic_id"],
                    "strength": float(row.get("strength", 0.5))
                }
                for row in (result.data or [])
            ]

            self._set_cache(cache_key, prerequisites)
            return prerequisites

        except Exception as e:
            logger.error(f"Error fetching prerequisites: {e}")
            return []

    # ========================================
    # CACHE HELPERS
    # ========================================

    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Get from cache if not expired"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if (datetime.now() - timestamp).seconds < self._cache_ttl:
                return value
            del self._cache[key]
        return None

    def _set_cache(self, key: str, value: Dict):
        """Set cache with timestamp"""
        self._cache[key] = (value, datetime.now())
