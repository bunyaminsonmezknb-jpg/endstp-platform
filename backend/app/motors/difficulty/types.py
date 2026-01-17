# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/difficulty/types.py
# Created: 2026-01-17
# Phase: FAZ 4B (Unified Motor Architecture)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns (N/A for types)
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded text
#
# 📚 RELATED DOCS:
#   - docs/GLOBAL_FIRST_GUIDE.md
# =============================================================================

"""
Difficulty motor typed contracts (FAZ 4B)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DifficultyTopicInput:
    topic_id: str
    topic_name: str
    subject_name: str

    success_rate: Optional[float] = None      # 0..100
    wrong_rate: Optional[float] = None        # 0..100
    blank_rate: Optional[float] = None        # 0..100
    test_count: Optional[int] = None
    avg_time_sec: Optional[float] = None
    last_test_date: Optional[str] = None      # ISO (UTC preferred)


@dataclass(frozen=True)
class DifficultyReason:
    code: str
    weight: float
    description: Optional[str] = None


@dataclass(frozen=True)
class DifficultyItem:
    topic_id: str
    topic_name: str
    subject_name: str
    difficulty_score: float                  # 0..100

    reasons: List[DifficultyReason] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DifficultyEngineInput:
    topics: List[DifficultyTopicInput]
    engine_version: str = "difficulty_v4b.1"
    now: Optional[datetime] = None


@dataclass(frozen=True)
class DifficultyEngineOutput:
    engine_version: str
    generated_at: str
    items: List[DifficultyItem]
