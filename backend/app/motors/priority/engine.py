from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, List, Optional

from .types import (
    PriorityEngineInput,
    PriorityEngineOutput,
    PriorityItem,
    PriorityReason,
)


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


def run_priority_engine(payload: PriorityEngineInput) -> PriorityEngineOutput:
    """
    Priority Engine v4b.1
    - Saf fonksiyon
    - DB/HTTP yok
    - Skorlar ve sıralar
    """
    now = payload.now or datetime.now(timezone.utc)

    items: List[PriorityItem] = []

    for t in payload.topics:
        topic_id = t.topic_id
        topic_name = t.topic_name
        subject_name = t.subject_name

        success_rate = _safe_float(t.success_rate, 0.0)  # 0..100
        test_count = _safe_int(t.test_count, 0)
        last_test_days = _days_since(t.last_test_date, now)

        # 1) düşük başarı -> daha yüksek öncelik
        success_component = max(0.0, 100.0 - success_rate)  # 0..100

        # 2) az test -> belirsizlik
        uncertainty_component = 0.0
        if test_count == 0:
            uncertainty_component = 25.0
        elif test_count < 3:
            uncertainty_component = 15.0
        elif test_count < 5:
            uncertainty_component = 8.0

        # 3) unutma riski
        forgetting_component = 0.0
        if last_test_days is None:
            forgetting_component = 10.0
        else:
            if last_test_days > 21:
                forgetting_component = 30.0
            elif last_test_days > 14:
                forgetting_component = 20.0
            elif last_test_days > 7:
                forgetting_component = 10.0

        # 4) trend etkisi
        trend_component = 0.0
        trend = (getattr(t, "trend", None) or "").lower() if hasattr(t, "trend") else ""
        # (Not: trend'i types'a koymadık; adapter meta’ya koyabilir. Şimdilik safe.)
        if trend == "declining":
            trend_component = 20.0
        elif trend == "stable":
            trend_component = 8.0
        elif trend == "improving":
            trend_component = 2.0

        raw_score = (
            success_component * 0.45
            + uncertainty_component * 0.20
            + forgetting_component * 0.25
            + trend_component * 0.10
        )
        score = max(0.0, min(100.0, raw_score))

        reasons: List[PriorityReason] = []
        if success_rate < 50:
            reasons.append(PriorityReason(code="LOW_SUCCESS", weight=success_component))
        if test_count == 0:
            reasons.append(PriorityReason(code="NO_TESTS", weight=uncertainty_component))
        elif test_count < 3:
            reasons.append(PriorityReason(code="LOW_SAMPLE", weight=uncertainty_component))
        if (last_test_days or 0) > 14:
            reasons.append(PriorityReason(code="TEST_GAP", weight=forgetting_component))
        if trend == "declining":
            reasons.append(PriorityReason(code="DECLINING_TREND", weight=trend_component))

        items.append(
            PriorityItem(
                topic_id=topic_id,
                topic_name=topic_name,
                subject_name=subject_name,
                score=round(score, 2),
                reasons=reasons,
                meta={
                    "success_rate": success_rate,
                    "test_count": test_count,
                    "days_since_last_test": last_test_days,
                    "trend": trend or None,
                },
            )
        )

    items.sort(key=lambda x: x.score, reverse=True)

    return PriorityEngineOutput(
        engine_version=payload.engine_version or "priority_v4b.1",
        generated_at=now.isoformat(),
        items=items,
    )
