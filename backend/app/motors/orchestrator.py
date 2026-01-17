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
from app.motors.time_pace.types import TimeEngineInput, TimeEngineOutput


ENGINE_VERSION = "orchestrator_v4b.1"


def _to_jsonable(obj: Any) -> Any:
    """
    Dataclass -> dict dönüşümü
    JSON uyumluluğu garanti edilir
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
    time_payload: Optional[TimeEngineInput] = None,
) -> Dict[str, Any]:
    """
    Unified Motor Orchestrator (FAZ 4B)
    ----------------------------------
    - Motorlar birbirinden bağımsız
    - Payload yoksa motor çalışmaz
    - Sadece orchestration yapar (iş mantığı YOK)
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
    if time_payload is not None:
        out: TimeEngineOutput = run_time_pace_engine(time_payload)
        results["motors"]["time_pace"] = {
            "engine_version": out.engine_version,
            "generated_at": out.generated_at,
            "items": _to_jsonable(out.items),
        }

    return results
