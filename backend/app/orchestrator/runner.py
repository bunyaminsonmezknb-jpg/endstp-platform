from __future__ import annotations

# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/orchestrator/runner.py
# Created: 2026-01-17
# Phase: FAZ 4D (Orchestrator Runner - Motor Aggregation)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded UI text
#
# 📚 RELATED DOCS:
#   - docs/L5_ORCHESTRATION_GUIDE.md
# =============================================================================

from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.orchestrator.contract import (
    OrchestratorDecision,
    OrchestratorInput,
    OrchestratorOutput,
)

# Motors
from app.motors.bs_model.engine import run_bs_model_engine
from app.motors.bs_model.types import BSModelEngineInput, BSModelTopicInput

from app.motors.difficulty.engine import run_difficulty_engine
from app.motors.difficulty.types import DifficultyEngineInput, DifficultyTopicInput

from app.motors.priority.engine import run_priority_engine
from app.motors.priority.types import PriorityEngineInput, PriorityTopicInput

from app.motors.time_pace.engine import run_time_pace_engine
from app.motors.time_pace.types import TimePaceEngineInput, TimePaceTopicInput

RUNNER_VERSION = "orchestrator-v4d.a3.1"


# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------
def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_now(dt: Optional[datetime]) -> datetime:
    """Ensures timezone-aware UTC datetime."""
    if dt is None:
        return _utc_now()
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _urgency_from_overdue_days(overdue_days: int) -> str:
    """
    Baseline urgency policy (Phase 1).
    Later: feature-flag / segment-aware.
    """
    if overdue_days >= 7:
        return "CRITICAL"
    if overdue_days > 0:
        return "HIGH"
    return "MEDIUM"


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


def _dataclass_kwargs(cls: Any, raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build kwargs for an arbitrary dataclass by filtering only valid fields.
    This prevents breakage when PriorityTopicInput evolves (field rename etc.).
    """
    try:
        fset = {f.name for f in fields(cls)}
        return {k: v for k, v in raw.items() if k in fset}
    except Exception:
        # If it's not a dataclass (unexpected), fallback to raw (may raise).
        return raw


def _fallback_priority_score(
    *,
    bs_due: bool,
    overdue_days: int,
    difficulty_score: float,
) -> float:
    """
    Safe baseline scoring if Priority engine is unavailable.
    Returns 0..100.
    """
    base = 0.0
    if bs_due:
        base += 30.0
    base += min(40.0, max(0.0, overdue_days) * 5.0)  # 0..40
    base += max(0.0, min(30.0, difficulty_score * 0.3))  # 0..30
    return max(0.0, min(100.0, base))

def _priority_bucket(score: float) -> str:
    """
    Semantic priority bucket (A.3).
    UI / planning friendly abstraction.
    """
    if score >= 80:
        return "P1_CRITICAL"
    if score >= 60:
        return "P2_HIGH"
    if score >= 40:
        return "P3_MEDIUM"
    return "P4_LOW"

# -------------------------------------------------------------------------
# Runner
# -------------------------------------------------------------------------
def run_orchestrator(inp: OrchestratorInput) -> OrchestratorOutput:
    """
    L5 Orchestrator Runner (FAZ 4D-A3)

    Rules:
    - Contract-safe
    - Motor-safe
    - Never crashes
    - If a motor fails: proceed with remaining motors (best-effort),
      but DO NOT fabricate motor outputs; only add meta.error_* notes.
    """

    now = _normalize_now(inp.now)

    # Base maps from input topics
    topic_map: Dict[str, Any] = {t.topic_id: t for t in inp.topics}

    meta: Dict[str, Any] = {
        "runner_version": RUNNER_VERSION,
        "active_motors": [],
    }

    # =========================================================
    # 1) BS MODEL (timing / due)
    # =========================================================
    bs_items_by_topic: Dict[str, Any] = {}
    try:
        bs_payload = BSModelEngineInput(
            topics=[
                BSModelTopicInput(
                    topic_id=t.topic_id,
                    subject_name=t.subject_name,
                    topic_name=t.topic_name,
                    # Phase 1 placeholders (wired later)
                    correct=0,
                    incorrect=0,
                    blank=0,
                    total=1,
                    difficulty=3,
                    repetitions=0,
                )
                for t in inp.topics
            ],
            now=now,
        )
        bs_out = run_bs_model_engine(bs_payload)
        meta["active_motors"].append("bs_model")
        bs_items_by_topic = {it.topic_id: it for it in bs_out.items}
    except Exception as e:
        meta["error_bs_model"] = str(e)
        # Without bs_model we cannot make "REVIEW" decisions (timing signal missing)
        return OrchestratorOutput(
            generated_at=now.isoformat(),
            decisions=[],
            meta=meta,
        )

    # =========================================================
    # 2) DIFFICULTY (struggle likelihood)
    # =========================================================
    diff_items_by_topic: Dict[str, Any] = {}
    try:
        diff_payload = DifficultyEngineInput(
            topics=[
                DifficultyTopicInput(
                    topic_id=t.topic_id,
                    topic_name=t.topic_name,
                    subject_name=t.subject_name,
                    # Phase 1 placeholders (wired later)
                    success_rate=None,
                    wrong_rate=None,
                    blank_rate=None,
                    test_count=None,
                    avg_time_sec=None,
                    last_test_date=None,
                )
                for t in inp.topics
            ],
            now=now,
        )
        diff_out = run_difficulty_engine(diff_payload)
        meta["active_motors"].append("difficulty")
        diff_items_by_topic = {it.topic_id: it for it in diff_out.items}
    except Exception as e:
        meta["error_difficulty"] = str(e)
        # continue without difficulty

    # =========================================================
    # 2.5) TIME / PACE (speed & pressure)
    # =========================================================
    time_items_by_topic: Dict[str, Any] = {}
    try:
        time_payload = TimePaceEngineInput(
            topics=[
                TimePaceTopicInput(
                    topic_id=t.topic_id,
                    topic_name=t.topic_name,
                    subject_name=t.subject_name,
                    # Phase 1 placeholders (wired later)
                    avg_time_sec=None,
                    success_rate=None,
                    test_count=None,
                    last_test_date=None,
                )
                for t in inp.topics
            ],
            now=now,
        )
        time_out = run_time_pace_engine(time_payload)
        meta["active_motors"].append("time_pace")
        time_items_by_topic = {it.topic_id: it for it in time_out.items}
    except Exception as e:
        meta["error_time_pace"] = str(e)
        # continue without time/pace



    # =========================================================
    # 3) PRIORITY (ordering / strategic weight)
    #    - Best effort: call engine if types match
    #    - Safe fallback score if engine fails
    # =========================================================
    priority_items_by_topic: Dict[str, Any] = {}
    priority_fallback_scores: Dict[str, float] = {}

    # Prepare raw rows (we will adapt to PriorityTopicInput fields dynamically)
    raw_priority_topics: List[Dict[str, Any]] = []
    for tid, t in topic_map.items():
        bs_it = bs_items_by_topic.get(tid)
        diff_it = diff_items_by_topic.get(tid)
        time_it = time_items_by_topic.get(tid)

        bs_due = bool(getattr(bs_it, "bs_due", False)) if bs_it else False
        overdue_days = _safe_int(getattr(bs_it, "bs_overdue_days", 0), 0) if bs_it else 0
        difficulty_score = _safe_float(getattr(diff_it, "difficulty_score", 0.0), 0.0) if diff_it else 0.0

        raw_priority_topics.append(
            {
                "topic_id": tid,
                "subject_name": t.subject_name,
                "topic_name": t.topic_name,
                # common candidates (engine may use one or more)
                "bs_due": bs_due,
                "overdue_days": overdue_days,
                "bs_overdue_days": overdue_days,  # alternate naming candidate
                "difficulty_score": difficulty_score,
                "difficulty": difficulty_score,   # alternate naming candidate
            }
        )

        # Always compute fallback baseline (used if priority engine fails or item missing)
        priority_fallback_scores[tid] = _fallback_priority_score(
            bs_due=bs_due,
            overdue_days=overdue_days,
            difficulty_score=difficulty_score,
        )

    # Try to run priority engine
    try:
        pr_topics: List[Any] = []
        for row in raw_priority_topics:
            kwargs = _dataclass_kwargs(PriorityTopicInput, row)
            pr_topics.append(PriorityTopicInput(**kwargs))

        pr_in_kwargs = _dataclass_kwargs(PriorityEngineInput, {"topics": pr_topics, "now": now})
        pr_payload = PriorityEngineInput(**pr_in_kwargs)

        pr_out = run_priority_engine(pr_payload)
        meta["active_motors"].append("priority")

        # Map whatever the engine returns
        priority_items_by_topic = {it.topic_id: it for it in pr_out.items}  # type: ignore[attr-defined]
    except Exception as e:
        meta["error_priority"] = str(e)
        # continue with fallback only

    # =========================================================
    # 4) DECISION SYNTHESIS
    # =========================================================
    decisions: List[OrchestratorDecision] = []

    for tid, bs_it in bs_items_by_topic.items():

        # Only decisions when BS says due
        if not bool(getattr(bs_it, "bs_due", False)):
            continue

        overdue_days = _safe_int(getattr(bs_it, "bs_overdue_days", 0), 0)
        urgency = _urgency_from_overdue_days(overdue_days)

        # Confidence from remembering_rate (0..100 -> 0..1)
        rr = _safe_float(getattr(bs_it, "bs_remembering_rate", 0.0), 0.0)
        confidence = round(max(0.0, min(1.0, rr / 100.0)), 2)

        # Difficulty score
        diff_it = diff_items_by_topic.get(tid)
        difficulty_score = (
            round(_safe_float(getattr(diff_it, "difficulty_score", 0.0), 0.0), 2)
            if diff_it else 0.0
        )

        # Priority score
        pr_it = priority_items_by_topic.get(tid)
        pr_score = None
        for attr in ("priority_score", "score", "priority", "priorityValue"):
            if pr_it is not None and hasattr(pr_it, attr):
                pr_score = _safe_float(getattr(pr_it, attr), None)
                break

        if pr_score is None:
            pr_score = priority_fallback_scores.get(tid, 0.0)

        pr_score = round(float(pr_score), 2)

        # -------------------------
        # Time / Pace
        # -------------------------
        time_it = time_items_by_topic.get(tid)

        pace_score = None
        pace_bucket = None
        time_pressure = None

        if time_it is not None:
            pace_score = round(
                _safe_float(getattr(time_it, "pace_score", 0.0), 0.0), 2
            )

            if pace_score >= 70:
                pace_bucket = "PACE_SLOW"
                time_pressure = True
            elif pace_score >= 40:
                pace_bucket = "PACE_MEDIUM"
                time_pressure = False
            else:
                pace_bucket = "PACE_OK"
                time_pressure = False

        # -------------------------
        # A.4.3 RISK CLUSTER
        # -------------------------
        risk_cluster = False

        if (
            bool(getattr(bs_it, "bs_due", False))
            and difficulty_score >= 60
            and pace_score is not None
            and pace_score >= 60
        ):
            risk_cluster = True

        # -------------------------
        # Reasons
        # -------------------------
        reasons: List[str] = []

        try:
            for r in getattr(bs_it, "reasons", []) or []:
                code = getattr(r, "code", None)
                if code:
                    reasons.append(str(code))
        except Exception:
            pass

        if diff_it is not None:
            try:
                for r in getattr(diff_it, "reasons", []) or []:
                    code = getattr(r, "code", None)
                    if code:
                        reasons.append(str(code))
            except Exception:
                pass

        # -------------------------
        # Signals (single source of truth)
        # -------------------------
        signals: Dict[str, Any] = {
            "engine": getattr(bs_it, "meta", {}).get("engine", "bs_model")
                if hasattr(bs_it, "meta") else "bs_model",
            "bs_due": True,
            "bs_overdue_days": overdue_days,
            "status": str(getattr(bs_it, "status", "NORMAL")),
            "bs_remembering_rate": round(rr, 2),
            "difficulty_score": difficulty_score,
            "priority_score": pr_score,
            "priority_bucket": _priority_bucket(pr_score),
            "pace_score": pace_score,
            "pace_bucket": pace_bucket,
            "time_pressure": time_pressure,
            "risk_cluster": risk_cluster,
        }

        decisions.append(
            OrchestratorDecision(
                topic_id=tid,
                action="REVIEW",
                urgency=urgency,
                confidence=confidence,
                reasons=reasons,
                signals=signals,
            )
        )

    # =========================================================
    # Final ordering & ranking
    # =========================================================
    decisions.sort(
        key=lambda d: _safe_float(d.signals.get("priority_score"), 0.0),
        reverse=True
    )

    for idx, d in enumerate(decisions, start=1):
        d.signals["priority_rank"] = idx

    return OrchestratorOutput(
        generated_at=now.isoformat(),
        decisions=decisions,
        meta=meta,
    )
