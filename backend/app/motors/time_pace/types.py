from __future__ import annotations
# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: {FILENAME}
# Created: {DATE}
# Phase: MVP (Phase 1)
# Author: End.STP Team
# 
# 🌍 LOCALIZATION STATUS:
#   [ ] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [ ] No hardcoded text
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - (None yet - Add items as you code)
#   - Example: "TURKISH_MONTHS dict (Line 45) → Phase 2: Database lookup"
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - (Actions will be listed here)
#   - Example: "Replace format_date_turkish() with format_date_localized()"
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
#   - Migration: docs/PHASE2_MIGRATION_PLAN.md
# =============================================================================

"""
{FILENAME} - {SHORT_DESCRIPTION}

{DETAILED_DESCRIPTION}

Usage:
    {USAGE_EXAMPLE}
"""

from datetime import datetime, timezone  # ⚠️ ALWAYS use timezone.utc!
from typing import List, Dict, Any, Optional

# =============================================================================
# YOUR CODE STARTS HERE
# =============================================================================

# TODO: Implement your functions


from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class TimeTopicInput:
    topic_id: str
    topic_name: str
    subject_name: str

    avg_time_sec: Optional[float] = None      # soru başı süre
    success_rate: Optional[float] = None      # 0..100
    test_count: Optional[int] = None
    last_test_date: Optional[str] = None      # ISO string


@dataclass(frozen=True)
class TimeReason:
    code: str
    weight: float
    description: Optional[str] = None


@dataclass(frozen=True)
class TimeItem:
    topic_id: str
    topic_name: str
    subject_name: str
    pace_score: float                         # 0..100 (yavaşlık riski)
    reasons: List[TimeReason] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TimeEngineInput:
    topics: List[TimeTopicInput]
    engine_version: str = "timep_pace_v4b.1"
    now: Optional[datetime] = None


@dataclass(frozen=True)
class TimeEngineOutput:
    engine_version: str
    generated_at: str
    items: List[TimeItem]
