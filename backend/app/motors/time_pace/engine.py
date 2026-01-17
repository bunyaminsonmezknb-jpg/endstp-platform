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
# app/motors/time/engine.py

from datetime import datetime, timezone
from typing import Any, List, Optional

from .types import (
    TimeEngineInput,
    TimeEngineOutput,
    TimeItem,
    TimeReason,
)

ENGINE_VERSION = "time-v4b.1"


# =========================
# Helpers
# =========================
def _safe_float(v: Any, default: float = 0.0) -> float:
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


def _safe_int(v: Any, default: int = 0) -> int:
    try:
        if v is None:
            return default
        return int(v)
    except Exception:
        return default


def _days_since(date_iso: Optional[str], now: datetime) -> Optional[int]:
    if not date_iso:
        return None
    try:
        s = date_iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = now - dt.astimezone(timezone.utc)
        return max(0, int(delta.total_seconds() // 86400))
    except Exception:
        return None


# =========================
# Engine
# =========================
def run_time_engine(payload: TimeEngineInput) -> TimeEngineOutput:
    """
    Time / Pace Engine (FAZ 4B)
    --------------------------
    - Saf fonksiyon
    - Hız / tempo riskini ölçer
    - pace_score: 0..100 (yüksek = yavaşlık riski)
    """

    now = payload.now or datetime.now(timezone.utc)
    items: List[TimeItem] = []

    for t in payload.topics:
        avg_time = _safe_float(t.avg_time_sec, 0.0)
        success_rate = _safe_float(t.success_rate, 0.0)
        test_count = _safe_int(t.test_count, 0)
        days_since = _days_since(t.last_test_date, now)

        # =========================
        # Bileşenler
        # =========================

        # 1️⃣ Ortalama süre (ana etki)
        time_component = 0.0
        if avg_time > 0:
            if avg_time > 150:
                time_component = 40.0
            elif avg_time > 120:
                time_component = 30.0
            elif avg_time > 90:
                time_component = 18.0
            elif avg_time > 60:
                time_component = 8.0

        # 2️⃣ Düşük başarı + yavaşlık birlikteyse
        efficiency_component = 0.0
        if avg_time > 90 and success_rate < 50:
            efficiency_component = 15.0

        # 3️⃣ Az test = hız güvenilmez
        uncertainty_component = 0.0
        if test_count == 0:
            uncertainty_component = 15.0
        elif test_count < 3:
            uncertainty_component = 8.0

        # 4️⃣ Uzun ara → tempo düşer
        forgetting_component = 0.0
        if days_since is not None and days_since > 21:
            forgetting_component = 10.0

        raw_score = (
            time_component
            + efficiency_component
            + uncertainty_component
            + forgetting_component
        )

        pace_score = max(0.0, min(100.0, raw_score))

        # =========================
        # Reasons
        # =========================
        reasons: List[TimeReason] = []

        if time_component > 0:
            reasons.append(
                TimeReason(
                    code="SLOW_PACE",
                    weight=round(time_component, 2),
                    description="Soru çözüm süresi uzun"
                )
            )

        if efficiency_component > 0:
            reasons.append(
                TimeReason(
                    code="LOW_EFFICIENCY",
                    weight=round(efficiency_component, 2),
                    description="Yavaşlık + düşük başarı birlikte"
                )
            )

        if uncertainty_component > 0:
            reasons.append(
                TimeReason(
                    code="LOW_SAMPLE",
                    weight=round(uncertainty_component, 2),
                    description="Az test verisi"
                )
            )

        if forgetting_component > 0:
            reasons.append(
                TimeReason(
                    code="FORGETTING_RISK",
                    weight=round(forgetting_component, 2),
                    description="Uzun süre test yapılmamış"
                )
            )

        items.append(
            TimeItem(
                topic_id=t.topic_id,
                topic_name=t.topic_name,
                subject_name=t.subject_name,
                pace_score=round(pace_score, 2),
                reasons=reasons,
                meta={
                    "avg_time_sec": avg_time,
                    "success_rate": success_rate,
                    "test_count": test_count,
                    "days_since_last_test": days_since,
                },
            )
        )

    items.sort(key=lambda x: x.pace_score, reverse=True)

    return TimeEngineOutput(
        engine_version=ENGINE_VERSION,
        generated_at=now.isoformat(),
        items=items,
    )
# =============================================================================
# Alias for orchestrator compatibility (FAZ 4D)
# =============================================================================
def run_time_pace_engine(payload: TimeEngineInput) -> TimeEngineOutput:
    """
    Alias wrapper for orchestrator.
    Keeps naming consistent with other motors:
    - run_bs_model_engine
    - run_difficulty_engine
    - run_priority_engine
    - run_time_pace_engine
    """
    return run_time_engine(payload)
