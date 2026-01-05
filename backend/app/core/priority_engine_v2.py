"""
Priority Engine v2.0.0 - PRODUCTION READY
Context-aware priority enrichment with production-grade features

CRITICAL IMPROVEMENTS:
1. Engine metadata (standardized)
2. interpreted_urgency (simplified decision signal)
3. Segment-aware urgency adjustment
4. Request-level context cache
5. Focus plan output
6. Feature flags for incomplete features
7. enrichment_failed standardization
8. Segment source transparency
9. Enhanced logging

PHILOSOPHY:
- Consumes v1 scores (never changes them)
- Adds context-aware enrichment
- Detects prerequisite cascades
- Identifies cross-subject synergies
- Graceful degradation on missing data
- Production-grade performance

LOCK DATE: 2025-01-02
VERSION: 2.0.0 PRODUCTION
"""

import logging
from typing import List, Dict, Optional
from .priority_engine_v1 import PriorityEngineV1, TopicInput, PriorityConfig, PriorityOutput


logger = logging.getLogger(__name__)


class PriorityFeatureFlags:
    """Feature flags for incomplete features"""
    
    # Prerequisite cascade detection (requires mastery service)
    PREREQUISITE_CASCADE_ENABLED = False
    
    # Cross-subject synergy detection (requires context service)
    CROSS_SUBJECT_SYNERGY_ENABLED = False


class PriorityEngineV2:
    """
    Context-aware priority enrichment - PRODUCTION READY
    
    Features:
    - Segment-aware tone & urgency
    - Archetype-based urgency adjustment
    - Action suggestions
    - Prerequisite cascade detection (optional)
    - Cross-subject synergy opportunities (optional)
    - Request-level context caching
    """
    
    def __init__(self, context_service, segmentation_engine):
        self.v1_engine = PriorityEngineV1()
        self.context_service = context_service
        self.segmentation_engine = segmentation_engine
        self.feature_flags = PriorityFeatureFlags()
    
    def analyze(
        self,
        topics: List[TopicInput],
        student_id: str,
        config: Optional[PriorityConfig] = None
    ) -> Dict:
        """
        Enriched analysis with context (fail-safe + cached)
        
        Returns:
            {
                "priorities": [...enriched v1 results...],
                "cascade_warnings": [...],  # If enabled
                "synergy_opportunities": [...],  # If enabled
                "segment_context": {...},
                "engine": {...}
            }
        """
        
        # 1. Get v1 baseline (critical path)
        try:
            v1_results = self.v1_engine.analyze(topics, config)
        except Exception as e:
            logger.error(f"Priority v1 failed: {e}")
            raise  # v1 failure = critical, should bubble up to router
        
        # 2. Get student segment (with default fallback)
        segment = self._get_segment_safe(student_id)
        
        # 3. Initialize context cache (performance optimization)
        context_cache = {}
        
        # 4. Enrich each result (fail-safe + cached)
        enriched_results = []
        
        for result in v1_results:
            try:
                enriched = self._enrich_result(
                    result, 
                    segment, 
                    student_id,
                    context_cache
                )
                enriched_results.append(enriched)
            except Exception as e:
                logger.warning(
                    f"Enrichment failed for topic '{result.topic_name}' "
                    f"(id: {result.topic_id}): {e}"
                )
                # Fallback: return v1 result with minimal enrichment
                enriched_results.append({
                    **result.dict(),
                    "segment_level": segment["level"],
                    "enrichment_failed": True
                })
        
        # 5. Optional: Detect prerequisite cascades (if enabled)
        cascade_warnings = []
        if self.feature_flags.PREREQUISITE_CASCADE_ENABLED:
            cascade_warnings = self._detect_prerequisite_cascades_safe(
                v1_results, student_id, context_cache
            )
        
        # 6. Optional: Identify cross-subject synergies (if enabled)
        synergy_opportunities = []
        if self.feature_flags.CROSS_SUBJECT_SYNERGY_ENABLED:
            synergy_opportunities = self._detect_cross_subject_synergies_safe(
                v1_results, student_id, context_cache
            )
        
        return {
            "priorities": enriched_results,
            "cascade_warnings": cascade_warnings,
            "synergy_opportunities": synergy_opportunities,
            "segment_context": segment,
            "engine": {
                "name": "priority",
                "version": "2.0.0",
                "mode": "enriched"
            }
        }
    
    def _get_segment_safe(self, student_id: str) -> Dict:
        """
        Get segment with default fallback + source tracking
        """
        try:
            segment = self.segmentation_engine.get_level(student_id)
            if segment and "level" in segment:
                # Add source field for transparency
                segment["source"] = "segmentation_engine"
                return segment
        except Exception as e:
            logger.warning(f"Segmentation failed for {student_id}: {e}")
        
        # Default: L4 (neutral) with source tracking
        return {
            "level": "L4",
            "confidence": 0.5,
            "source": "default"
        }
    
    def _enrich_result(
        self,
        result: PriorityOutput,
        segment: Dict,
        student_id: str,
        context_cache: Dict
    ) -> Dict:
        """
        Enrich single priority result with caching
        """
        
        # Fetch context (cached)
        context = self._get_context_cached(result.topic_id, context_cache)
        
        # Archetype-based urgency adjustment
        urgency_adj = self._calculate_urgency_adjustment(
            result, 
            context, 
            segment
        )
        
        # Segment-based tone
        tone = self._select_message_tone(segment)
        
        # Action suggestions
        action_hints = self._generate_action_suggestions(result, segment)
        
        # Interpreted urgency (simplified decision signal)
        interpreted = self._calculate_interpreted_urgency(
            result.priority_level,
            urgency_adj["adjustment"]
        )
        
        return {
            **result.dict(),  # v1 fields untouched
            "segment_level": segment["level"],
            "urgency_adjustment": urgency_adj["adjustment"],
            "urgency_note": urgency_adj.get("note"),
            "interpreted_urgency": interpreted,
            "message_tone": tone,
            "suggested_sessions": action_hints["sessions"],
            "suggested_duration_minutes": action_hints["duration"],
            "archetype": context.get("archetype", "foundational"),
            "enrichment_failed": False  # Standardized
        }
    
    def _get_context_cached(
        self,
        topic_id: str,
        context_cache: Dict
    ) -> Dict:
        """
        Get topic context with request-level caching
        
        Performance optimization: Prevents duplicate calls
        """
        if topic_id in context_cache:
            return context_cache[topic_id]
        
        try:
            context = self.context_service.get_topic_context(topic_id)
            context_cache[topic_id] = context
            return context
        except Exception as e:
            logger.warning(f"Context fetch failed for {topic_id}: {e}")
            # Cache empty result too (prevent retry)
            context_cache[topic_id] = {}
            return {}
    
    def _calculate_urgency_adjustment(
        self,
        result: PriorityOutput,
        context: Dict,
        segment: Dict
    ) -> Dict:
        """
        Calculate urgency adjustment with segment awareness
        
        Returns:
            {
                "adjustment": "ELEVATED" | "NEUTRAL" | "RELAXED",
                "note": Optional explanation
            }
        """
        
        archetype = context.get("archetype", "foundational")
        base_level = result.priority_level
        student_level = segment["level"]
        
        # Foundational topics → elevated urgency
        if archetype == "foundational":
            if base_level in ["MEDIUM", "HIGH"]:
                # Segment modulation: L1-L2 need gentle approach
                if student_level in ["L1", "L2"]:
                    return {
                        "adjustment": "NEUTRAL",
                        "note": "Temel konu ama adım adım ilerle"
                    }
                else:
                    return {
                        "adjustment": "ELEVATED",
                        "note": "Temel konu - öncelik artırılmalı"
                    }
        
        # Synthesis topics → can be relaxed
        elif archetype == "synthesis":
            if base_level == "HIGH":
                # Segment modulation: L6-L7 can handle complexity
                if student_level in ["L6", "L7"]:
                    return {
                        "adjustment": "NEUTRAL",
                        "note": "Sentez konusu - performansını koruyabilirsin"
                    }
                else:
                    return {
                        "adjustment": "RELAXED",
                        "note": "Sentez konusu - temel sağlamsa pratikle gelişir"
                    }
        
        # Default: No adjustment
        return {
            "adjustment": "NEUTRAL",
            "note": None
        }
    
    def _calculate_interpreted_urgency(
        self,
        base_priority: str,
        adjustment: str
    ) -> str:
        """
        Calculate interpreted urgency (simplified decision signal)
        
        This is NOT an override, just a simplified signal for UI/planning
        
        Args:
            base_priority: LOW | MEDIUM | HIGH | CRITICAL
            adjustment: ELEVATED | NEUTRAL | RELAXED
        
        Returns:
            LOW | MODERATE | HIGH
        """
        
        # CRITICAL always maps to HIGH
        if base_priority == "CRITICAL":
            return "HIGH"
        
        # Mapping with adjustment
        if base_priority == "HIGH":
            if adjustment == "RELAXED":
                return "MODERATE"
            else:
                return "HIGH"
        
        elif base_priority == "MEDIUM":
            if adjustment == "ELEVATED":
                return "HIGH"
            elif adjustment == "RELAXED":
                return "LOW"
            else:
                return "MODERATE"
        
        elif base_priority == "LOW":
            if adjustment == "ELEVATED":
                return "MODERATE"
            else:
                return "LOW"
        
        # Default
        return "MODERATE"
    
    def _select_message_tone(self, segment: Dict) -> str:
        """Select message tone based on segment"""
        
        level = segment["level"]
        
        tone_map = {
            "L1": "protective",
            "L2": "supportive",
            "L3": "encouraging",
            "L4": "neutral",
            "L5": "clear",
            "L6": "strategic",
            "L7": "performance"
        }
        
        return tone_map.get(level, "neutral")
    
    def _generate_action_suggestions(
        self,
        result: PriorityOutput,
        segment: Dict
    ) -> Dict:
        """Generate action suggestions"""
        
        level = segment["level"]
        priority = result.priority_level
        
        # Base suggestions (L4 neutral)
        sessions = 2
        duration = 25
        
        # Adjust by segment
        if level in ["L1", "L2"]:
            sessions = 1
            duration = 15
        elif level in ["L6", "L7"]:
            sessions = 1
            duration = 20
        
        # Adjust by priority
        if priority == "CRITICAL":
            sessions += 1
            duration += 10
        elif priority == "HIGH":
            sessions += 1
        
        return {
            "sessions": max(1, sessions),
            "duration": max(15, min(45, duration))
        }
    
    def _detect_prerequisite_cascades_safe(
        self,
        results: List[PriorityOutput],
        student_id: str,
        context_cache: Dict
    ) -> List[Dict]:
        """Detect prerequisite cascades (fail-safe + cached)"""
        try:
            return self._detect_prerequisite_cascades(
                results, student_id, context_cache
            )
        except Exception as e:
            logger.warning(f"Cascade detection failed: {e}")
            return []
    
    def _detect_prerequisite_cascades(
        self,
        results: List[PriorityOutput],
        student_id: str,
        context_cache: Dict
    ) -> List[Dict]:
        """
        Detect high-priority topics with weak prerequisites
        
        Returns focus_plan format for UX
        """
        
        cascades = []
        
        for result in results:
            # Only check HIGH/CRITICAL priorities
            if result.priority_level not in ["HIGH", "CRITICAL"]:
                continue
            
            # Get prerequisites (safe + cached)
            try:
                prerequisites = self.context_service.get_prerequisites(result.topic_id)
            except Exception:
                continue
            
            if not prerequisites:
                continue
            
            # Check mastery for each prerequisite
            weak_prereqs = []
            weak_prereq_ids = []
            
            for prereq in prerequisites:
                try:
                    mastery = self._get_mastery_safe(student_id, prereq["topic_id"])
                    
                    # If mastery is None (unavailable), flag differently
                    if mastery is None:
                        logger.info(
                            f"Mastery unavailable for prerequisite '{prereq.get('topic_name')}' "
                            f"of topic '{result.topic_name}'"
                        )
                        continue
                    
                    if mastery < 60:
                        weak_prereqs.append({
                            "topic_id": prereq["topic_id"],
                            "topic_name": prereq.get("topic_name", "Unknown"),
                            "mastery": round(mastery, 1)
                        })
                        weak_prereq_ids.append(prereq["topic_id"])
                except Exception:
                    continue
            
            if weak_prereqs:
                cascades.append({
                    "target_topic": result.topic_name,
                    "target_priority": result.priority_level,
                    "weak_prerequisites": weak_prereqs,
                    "suggestion": (
                        f"{result.topic_name} için önce "
                        f"{len(weak_prereqs)} temel konuyu güçlendir"
                    ),
                    # Focus plan for UX (single-click study plan)
                    "focus_plan": {
                        "before": weak_prereq_ids,
                        "target": result.topic_id,
                        "reason": "weak_prerequisites"
                    }
                })
        
        return cascades
    
    def _detect_cross_subject_synergies_safe(
        self,
        results: List[PriorityOutput],
        student_id: str,
        context_cache: Dict
    ) -> List[Dict]:
        """Detect cross-subject synergies (fail-safe + cached)"""
        try:
            return self._detect_cross_subject_synergies(
                results, student_id, context_cache
            )
        except Exception as e:
            logger.warning(f"Synergy detection failed: {e}")
            return []
    
    def _detect_cross_subject_synergies(
        self,
        results: List[PriorityOutput],
        student_id: str,
        context_cache: Dict
    ) -> List[Dict]:
        """
        Detect topics that benefit multiple subjects
        
        Only for HIGH/CRITICAL priorities
        """
        
        synergies = []
        
        for result in results:
            # Only check HIGH/CRITICAL priorities
            if result.priority_level not in ["HIGH", "CRITICAL"]:
                continue
            
            # Get context (cached)
            context = self._get_context_cached(result.topic_id, context_cache)
            connections = context.get("cross_subject_connections", [])
            
            if not connections:
                continue
            
            # Collect affected subjects
            affected_subjects = []
            for conn in connections:
                subject_code = conn.get("subject_code")
                if subject_code:
                    affected_subjects.append(subject_code)
            
            if affected_subjects:
                synergies.append({
                    "topic_name": result.topic_name,
                    "topic_priority": result.priority_level,
                    "synergy_subjects": affected_subjects,
                    "benefit_note": (
                        f"Bu konuyu çalışırsan "
                        f"{', '.join(affected_subjects)} derslerinde de ilerlersin"
                    )
                })
        
        return synergies
    
    def _get_mastery_safe(self, student_id: str, topic_id: str) -> Optional[float]:
        """
        Get student mastery with None fallback
        
        Returns:
            float: Mastery score (0-100)
            None: Mastery unavailable
        
        TODO: Implement actual mastery lookup
        """
        # Placeholder: Return None (mastery service not ready)
        return None
