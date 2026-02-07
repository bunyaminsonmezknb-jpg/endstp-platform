# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/orchestrator/contract.py
# Created: 2026-01-17
# Phase: FAZ 4D (Orchestrator contract - Motor Aggregation)
# Author: End.STP Team
# =============================================================================

# backend/app/orchestrator/contract.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal, Dict, Any


# -----------------------------------------------------------------------------
# ENUM-LIKE TYPES
# -----------------------------------------------------------------------------

ActionType = Literal[
    "REVIEW_NOW",
    "REVIEW_SOON",
    "PRACTICE",
    "SKIP",
]

UrgencyLevel = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]


# -----------------------------------------------------------------------------
# INPUT CONTRACT
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class OrchestratorTopicInput:
    """
    Minimal topic snapshot shared by all motors.
    (Motor-specific fields live inside motor engines, not here.)
    """
    topic_id: str
    subject_name: str
    topic_name: str


@dataclass(frozen=True)
class OrchestratorInput:
    """
    Entry contract for orchestrator.
    """
    student_id: str
    topics: List[OrchestratorTopicInput]

    # Context (optional, Phase 2+)
    now: Optional[datetime] = None
    exam_date: Optional[datetime] = None
    meta: Dict[str, Any] = field(default_factory=dict)


# -----------------------------------------------------------------------------
# OUTPUT CONTRACT
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class OrchestratorDecision:
    """
    Final decision per topic.
    """
    topic_id: str

    action: ActionType
    urgency: UrgencyLevel

    confidence: float  # 0..1

    reasons: List[str] = field(default_factory=list)

    # For explainability & UI
    signals: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OrchestratorOutput:
    """
    Orchestrator result.
    """
    generated_at: str
    decisions: List[OrchestratorDecision]

    meta: Dict[str, Any] = field(default_factory=dict)
