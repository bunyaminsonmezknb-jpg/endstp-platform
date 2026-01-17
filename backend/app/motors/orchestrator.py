# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/orchestrator.py
# Created: 2026-01-17
# Phase: FAZ 4B (Analysis Plane)
# Author: End.STP Team
# =============================================================================

"""
Unified Motor Orchestrator (FAZ 4B)

Coordinates independent analysis motors:
- Priority
- Difficulty
- Time/Pace

❗ This layer:
- DOES NOT make decisions
- DOES NOT apply pedagogy
- ONLY aggregates motor outputs
"""

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
    - Coordination only
    - No decisions
    """

    generated_at = datetime.now(timezone.utc).isoformat()

    results: Dict[str, Any] = {
        "orchestrator_version": ENGINE_VERSION,
        "generated_at": generated_at,
        "motors": {},
    }

    if priority_payload is not None:
        out: PriorityEngineOutput = run_priority_engine(priority_payload)
        results["motors"]["priority"] = {
            "engine_version": out.engine_version,
            "generated_at": out.generated_at,
            "items": _to_jsonable(out.items),
        }

    if difficulty_payload is not None:
        out: DifficultyEngineOutput = run_difficulty_engine(difficulty_payload)
        results["motors"]["difficulty"] = {
            "engine_version": out.engine_version,
            "generated_at": out.generated_at,
            "items": _to_jsonable(out.items),
        }

    if time_pace_payload is not None:
        out: TimePaceEngineOutput = run_time_pace_engine(time_pace_payload)
        results["motors"]["time_pace"] = {
            "engine_version": out.engine_version,
            "generated_at": out.generated_at,
            "items": _to_jsonable(out.items),
        }

    return results
