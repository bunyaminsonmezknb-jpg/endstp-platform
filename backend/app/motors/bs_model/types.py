from __future__ import annotations

"""
bs_model v4B
Deterministic, explainable bs model scoring
"""
# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/bs_model/types.py
# Created: 2026-01-17
# Phase: FAZ 4C (BS-Model Engine Integration)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded text (engine strings minimal; UI handles localization later)
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
# =============================================================================


from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Literal


BSStatus = Literal["NEW", "HERO", "RESET", "NORMAL"]


@dataclass(frozen=True)
class BSModelTopicInput:
    """
    Minimal BS snapshot per topic.
    NOTE: This mirrors your existing BSModelInput fields conceptually,
    but adapted to dataclasses for motor architecture consistency.
    """
    topic_id: str
    subject_name: str
    topic_name: str

    # Performance (last test)
    correct: int
    incorrect: int
    blank: int
    total: int
    difficulty: int = 3  # 1..5

    # State
    current_ef: Optional[float] = None
    current_ia: Optional[int] = None
    actual_gap: Optional[int] = None
    repetitions: int = 0

    # Dates (optional)
    last_test_date: Optional[str] = None  # ISO string (UTC preferred)


@dataclass(frozen=True)
class BSReason:
    code: str
    weight: float
    description: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BSItem:
    topic_id: str
    subject_name: str
    topic_name: str

    status: BSStatus
    next_ef: float
    next_ia: int
    next_repetition: int
    score: float  # 0..1

    # Orchestrator-facing signals (what unified expects)
    bs_due: bool
    bs_overdue_days: int
    bs_remembering_rate: float  # 0..100

    reasons: List[BSReason] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BSModelEngineInput:
    topics: List[BSModelTopicInput]
    engine_version: str = "bs_model_v1"
    now: Optional[datetime] = None


@dataclass(frozen=True)
class BSModelEngineOutput:
    engine_version: str
    generated_at: str
    items: List[BSItem]
