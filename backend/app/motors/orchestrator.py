# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/orchestrator.py
# Created: 2026-01-17
# Phase: FAZ 4B (Analysis Plane)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded text
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - None
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - Orchestrator decision layer will be introduced (FAZ 5)
#   - Current orchestrator is coordination-only (non-decision)
#
# 📚 RELATED DOCS:
#   - docs/GLOBAL_FIRST_GUIDE.md
#   - docs/ARCHITECTURE/FAZ_4B_MOTORS.md
# =============================================================================

"""
Unified Motor Orchestrator (FAZ 4B)

Coordinates independent analysis motors:
- Priority
- Difficulty
- Time/Pace

This layer:
- DOES NOT make decisions
- DOES NOT apply pedagogy
- ONLY aggregates motor outputs in a deterministic way

Used by:
- Unified adapter
- Task generation pipelines (read-only)
"""

# app/motors/orchestrator.py
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.motors.priority.engine import run_priority_engine
from app.motors.priority.types import PriorityEngineInput, PriorityEngineOutput

from app.motors.difficulty.engine import run_difficulty_engine
from app.motors.difficulty.types import DifficultyEngineInput, DifficultyEngineOutput

from app.motors.time_pace.engine import run_time_pace_engine
from app.motors.time_pace.types import TimePaceEngineInput, TimePaceEngineOutput


ENGINE_VERSION = "orchestrator_v4b.1"


def _to_jsonable(obj: Any) -> Any:
    """
    Dataclass'lari dict'e cevirerek JSON-uyumlu cikti garanti eder.
    (Sessiz bug'lari engellemek icin)
    """
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, list):
        return [_to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    return obj


def run_unified_motors(
    *,
    priority_payload: Optional[PriorityEngineInput] = None,
    difficulty_payload: Optional[DifficultyEngineInput] = None,
    time_pace_payload: Optional[TimePaceEngineInput] = None,
) -> Dict[str, Any]:
    """
    Unified Motor Orchestrator (FAZ 4B)
    ----------------------------------
    - Motorlari koordine eder
    - Motorlar arasi bagimlilik YOK (her biri independent)
    - Kontrat & serialize guvenligi saglar
    - Missing payload = motor calistirilmaz (neutral)
    """

    generated_at = datetime.now(timezone.utc).isoformat()

    results: Dict[str, Any] = {
        "orchestrator_version": ENGINE_VERSION,
        "generated_at": generated_at,
        "motors": {},
    }

    # ======================
    # PRIORITY MOTOR
    # ======================
    if priority_payload is not None:
        out: PriorityEngineOutput = run_priority_engine(priority_payload)
        results["motors"]["priority"] = {
            "engine_version": out.engine_version,
            "generated_at": out.generated_at,
            "items": _to_jsonable(out.items),
        }

    # ======================
    # DIFFICULTY MOTOR
    # ======================
    if difficulty_payload is not None:
        out: DifficultyEngineOutput = run_difficulty_engine(difficulty_payload)
        results["motors"]["difficulty"] = {
            "engine_version": out.engine_version,
            "generated_at": out.generated_at,
            "items": _to_jsonable(out.items),
        }

    # ======================
    # TIME / PACE MOTOR
    # ======================
    if time_pace_payload is not None:
        out: TimePaceEngineOutput = run_time_pace_engine(time_pace_payload)
        results["motors"]["time_pace"] = {
            "engine_version": out.engine_version,
            "generated_at": out.generated_at,
            "items": _to_jsonable(out.items),
        }

    return results
