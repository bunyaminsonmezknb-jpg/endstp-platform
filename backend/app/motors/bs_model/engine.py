from __future__ import annotations

"""
bs_model v4B
Deterministic, explainable bs model scoring
"""
# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/bs_model/engine.py
# Created: 2026-01-17
# Phase: FAZ 4C (BS-Model Engine Integration)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded text (engine messages are codes; UI localizes)
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
# =============================================================================


from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from .types import (
    BSModelEngineInput,
    BSModelEngineOutput,
    BSModelTopicInput,
    BSItem,
    BSReason,
)

ENGINE_VERSION = "bs_model-v4c.1"


# -------------------------------------------------------------------------
# Helpers (defensive + UTC)
# -------------------------------------------------------------------------
def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(dt_iso: Optional[str]) -> Optional[datetime]:
    if not dt_iso:
        return None
    try:
        s = dt_iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _safe_int(v: Any, default: int = 0) -> int:
    try:
        if v is None:
            return default
        return int(v)
    except Exception:
        return default


def _safe_float(v: Any, default: float = 0.0) -> float:
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


# -------------------------------------------------------------------------
# v1 adapter wrapper
# -------------------------------------------------------------------------
def _bs_v1_calculate(topic: BSModelTopicInput) -> Dict[str, Any]:
    """
    Calls your BSModelV1 logic.

    IMPORTANT:
    - If your repo already has BSModelV1 somewhere, update this import path.
    - If not, you can paste your BSModelV1 code into a dedicated module and import it here.
    """
    # ✅ Path'i SENİN projendeki gerçek konuma göre ayarlayacağız:
    # ÖRN: from app.motors.bs_model.v1 import BSModelV1, BSModelInput
    # ŞİMDİ: en güvenli şekilde import dene, yoksa raise edip üst katmanda fallback verelim.
    try:
        from app.motors.bs_model.v1 import BSModelV1, BSModelInput  # type: ignore
    except Exception as e:
        raise RuntimeError(f"BSModelV1 import failed: {e}")

    inp = BSModelInput(
        correct=_safe_int(topic.correct, 0),
        incorrect=_safe_int(topic.incorrect, 0),
        blank=_safe_int(topic.blank, 0),
        total=_safe_int(topic.total, 0),
        difficulty=_safe_int(topic.difficulty, 3),

        current_ef=topic.current_ef,
        current_ia=topic.current_ia,
        actual_gap=topic.actual_gap,
        repetitions=_safe_int(topic.repetitions, 0),
    )

    out = BSModelV1.calculate(inp)
    # out is pydantic in your snippet => .dict() works
    return out.dict() if hasattr(out, "dict") else dict(out)


def _compute_due_and_overdue(
    *,
    now: datetime,
    last_test_date_iso: Optional[str],
    current_ia_days: Optional[int],
) -> Tuple[bool, int]:
    """
    due = gap >= interval
    overdue_days = max(0, gap - interval)
    """
    last_dt = _parse_iso(last_test_date_iso)
    if not last_dt:
        # If no last test date, treat as due (new topic / missing data)
        return True, 0

    gap_days = max(0, int((now - last_dt).total_seconds() // 86400))
    ia = _safe_int(current_ia_days, 0)

    if ia <= 0:
        return True, 0

    if gap_days >= ia:
        return True, max(0, gap_days - ia)

    return False, 0


def _remembering_rate_from_score(score_0_1: float) -> float:
    # simple mapping for v1 (v2 will replace with real retention curve/k_forget)
    return _clamp(score_0_1, 0.0, 1.0) * 100.0


# -------------------------------------------------------------------------
# Engine (FAZ 4C) - DB free
# -------------------------------------------------------------------------
def run_bs_model_engine(payload: BSModelEngineInput) -> BSModelEngineOutput:
    """
    BS-Model Engine (FAZ 4C)
    -----------------------
    - Pure function
    - Calls BSModel v1 as baseline
    - Produces orchestrator-facing signals:
        bs_due, bs_overdue_days, bs_remembering_rate
    - Leaves clean hooks for v2 + fallback selection (FAZ 4D/5)
    """

    now = payload.now or _utc_now()
    items: List[BSItem] = []

    for t in payload.topics:
        reasons: List[BSReason] = []

        # ---- v1 baseline ----
        try:
            v1 = _bs_v1_calculate(t)
        except Exception as e:
            # Fail-safe: never crash orchestrator, emit neutral item
            reasons.append(
                BSReason(
                    code="BS_V1_FAILED",
                    weight=0.0,
                    description="BS v1 calculation failed; neutral fallback emitted.",
                    meta={"error": str(e)},
                )
            )
            # neutral fallback
            status = "NORMAL"
            next_ef = 2.5
            next_ia = 1
            next_rep = _safe_int(t.repetitions, 0)
            score = 0.5
        else:
            status = str(v1.get("status", "NORMAL"))
            next_ef = _safe_float(v1.get("next_ef"), 2.5)
            next_ia = _safe_int(v1.get("next_ia"), 1)
            next_rep = _safe_int(v1.get("next_repetition"), _safe_int(t.repetitions, 0))
            score = _safe_float(v1.get("score"), 0.5)

            reasons.append(
                BSReason(
                    code=f"BS_STATUS_{status}",
                    weight=1.0,
                    description="BS v1 status computed.",
                    meta={"status": status},
                )
            )

        # ---- due/overdue signals ----
        # due calculation uses CURRENT interval; prefer t.current_ia (previous plan),
        # but if missing, use next_ia as best-effort.
        ia_for_due = t.current_ia if t.current_ia is not None else next_ia
        bs_due, bs_overdue_days = _compute_due_and_overdue(
            now=now,
            last_test_date_iso=t.last_test_date,
            current_ia_days=ia_for_due,
        )

        if bs_due:
            reasons.append(
                BSReason(
                    code="BS_DUE",
                    weight=10.0,
                    description="Review is due based on gap vs interval.",
                    meta={"overdue_days": bs_overdue_days},
                )
            )
        if bs_overdue_days > 0:
            reasons.append(
                BSReason(
                    code="BS_OVERDUE",
                    weight=min(30.0, 5.0 + bs_overdue_days * 1.5),
                    description="Review is overdue; forgetting risk increased.",
                    meta={"overdue_days": bs_overdue_days},
                )
            )

        # ---- remembering rate ----
        bs_remembering_rate = _remembering_rate_from_score(score)

        items.append(
            BSItem(
                topic_id=t.topic_id,
                subject_name=t.subject_name,
                topic_name=t.topic_name,
                status=status,  # type: ignore
                next_ef=round(next_ef, 2),
                next_ia=max(1, int(next_ia)),
                next_repetition=max(0, int(next_rep)),
                score=round(_clamp(score, 0.0, 1.0), 2),
                bs_due=bool(bs_due),
                bs_overdue_days=int(bs_overdue_days),
                bs_remembering_rate=round(bs_remembering_rate, 2),
                reasons=reasons,
                meta={
                    "engine": ENGINE_VERSION,
                    "input": {
                        "difficulty": t.difficulty,
                        "current_ef": t.current_ef,
                        "current_ia": t.current_ia,
                        "actual_gap": t.actual_gap,
                        "repetitions": t.repetitions,
                        "last_test_date": t.last_test_date,
                    },
                    "v1_baseline_used": True,
                },
            )
        )

    # due & overdue first (most urgent), then lower
    items.sort(key=lambda x: (not x.bs_due, -x.bs_overdue_days, -x.bs_remembering_rate))

    return BSModelEngineOutput(
        engine_version=ENGINE_VERSION,
        generated_at=now.isoformat(),
        items=items,
    )
