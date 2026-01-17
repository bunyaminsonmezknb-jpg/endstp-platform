# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/priority/types.py
# Created: 2026-01-17
# Phase: FAZ 4B (Unified Motor Architecture)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling (engine uses timezone-aware now)
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns (N/A for types)
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded text (types only)
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - None
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - Consider localized reason messages in adapters (not here)
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
# =============================================================================

"""
Priority motor typed contracts (FAZ 4B)

- Engine input/output dataclasses
- Pure / DB-free engines consume these
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Literal


Trend = Literal["declining", "stable", "improving", "unknown"]


@dataclass(frozen=True)
class PriorityTopicInput:
    topic_id: str
    topic_name: str
    subject_name: str

    success_rate: Optional[float] = None  # 0..100
    test_count: Optional[int] = None
    last_test_date: Optional[str] = None  # ISO string (UTC preferred)
    trend: Optional[Trend] = "unknown"


@dataclass(frozen=True)
class PriorityReason:
    code: str
    weight: float
    description: Optional[str] = None


@dataclass(frozen=True)
class PriorityItem:
    topic_id: str
    topic_name: str
    subject_name: str
    score: float  # 0..100

    reasons: List[PriorityReason] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PriorityEngineInput:
    topics: List[PriorityTopicInput]
    engine_version: str = "priority_v4b.1"
    now: Optional[datetime] = None


@dataclass(frozen=True)
class PriorityEngineOutput:
    engine_version: str
    generated_at: str
    items: List[PriorityItem]
