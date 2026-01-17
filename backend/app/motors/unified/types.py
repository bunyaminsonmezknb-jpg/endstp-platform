# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/unified/types.py
# Created: 2026-01-17
# Phase: FAZ 4D (Orchestrator Runner - Motor Aggregation)
# Author: End.STP Team
# =============================================================================

from typing import Dict, Any, List
from pydantic import BaseModel


class UnifiedAnalysisResult(BaseModel):
    student_id: str
    subject_id: str
    priority: Dict[str, Any]
    difficulty: Dict[str, Any]
    time_pace: Dict[str, Any]
    explanations: List[str]
