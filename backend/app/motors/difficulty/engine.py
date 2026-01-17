# app/motors/difficulty/engine.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, List, Optional

from .types import (
    DifficultyEngineInput,
    DifficultyEngineOutput,
    DifficultyItem,
    DifficultyReason,
)

ENGINE_VERSION = "difficulty-v4b.1"


# =========================
# Helpers (defensive)
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
def run_difficulty_engine(payload: DifficultyEngineInput) -> DifficultyEngineOutput:
    """
    Difficulty Engine (FAZ 4B)
    -------------------------
    - Saf fonksiyon (DB / HTTP YOK)
    - Deterministik
    - Açıklanabilir
    - 0..100 difficulty_score üretir

    Zorluk = öğrencinin o konuyu yaparken zorlanma ihtimali
    """

    now = payload.now or datetime.now(timezone.utc)
    items: List[DifficultyItem] = []

    for t in payload.topics:
        # ---- Güvenli okuma ----
        success_rate = _safe_float(t.success_rate, 0.0)
        wrong_rate = _safe_float(t.wrong_rate, 0.0)
        blank_rate = _safe_float(t.blank_rate, 0.0)
        test_count = _safe_int(t.test_count, 0)
        avg_time = _safe_float(t.avg_time_sec, 0.0)
        days_since = _days_since(t.last_test_date, now)

        # =========================
        # Bileşenler
        # =========================

        # 1️⃣ Başarı düşüklüğü
        success_component = max(0.0, 100.0 - success_rate) * 0.35

        # 2️⃣ Yanlış + boş oranı
        error_component = (wrong_rate * 0.6 + blank_rate * 0.4) * 0.30

        # 3️⃣ Az test = belirsizlik
        uncertainty_component = 0.0
        if test_count == 0:
            uncertainty_component = 20.0
        elif test_count < 3:
            uncertainty_component = 12.0
        elif test_count < 5:
            uncertainty_component = 6.0

        # 4️⃣ Süre baskısı (yavaş çözüm)
        time_component = 0.0
        if avg_time > 0:
            if avg_time > 120:
                time_component = 15.0
            elif avg_time > 90:
                time_component = 8.0

        # 5️⃣ Unutma etkisi
        forgetting_component = 0.0
        if days_since is not None and days_since > 21:
            forgetting_component = 10.0

        # =========================
        # Toplam skor
        # =========================
        raw_score = (
            success_component
            + error_component
            + uncertainty_component
            + time_component
            + forgetting_component
        )

        difficulty_score = max(0.0, min(100.0, raw_score))

        # =========================
        # Açıklanabilir nedenler
        # =========================
        reasons: List[DifficultyReason] = []

        if success_rate < 50:
            reasons.append(
                DifficultyReason(
                    code="LOW_SUCCESS",
                    weight=round(success_component, 2),
                    description="Başarı oranı düşük"
                )
            )

        if wrong_rate + blank_rate > 40:
            reasons.append(
                DifficultyReason(
                    code="HIGH_ERROR",
                    weight=round(error_component, 2),
                    description="Yanlış/boş oranı yüksek"
                )
            )

        if test_count < 3:
            reasons.append(
                DifficultyReason(
                    code="LOW_SAMPLE",
                    weight=round(uncertainty_component, 2),
                    description="Az test verisi"
                )
            )

        if time_component > 0:
            reasons.append(
                DifficultyReason(
                    code="TIME_PRESSURE",
                    weight=round(time_component, 2),
                    description="Soru çözüm süresi uzun"
                )
            )

        if forgetting_component > 0:
            reasons.append(
                DifficultyReason(
                    code="FORGETTING_RISK",
                    weight=round(forgetting_component, 2),
                    description="Uzun süre test yapılmamış"
                )
            )

        # =========================
        # Item
        # =========================
        items.append(
            DifficultyItem(
                topic_id=t.topic_id,
                topic_name=t.topic_name,
                subject_name=t.subject_name,
                difficulty_score=round(difficulty_score, 2),
                reasons=reasons,
                meta={
                    "success_rate": success_rate,
                    "wrong_rate": wrong_rate,
                    "blank_rate": blank_rate,
                    "test_count": test_count,
                    "avg_time_sec": avg_time,
                    "days_since_last_test": days_since,
                },
            )
        )

    # Zorluk yüksekten düşüğe
    items.sort(key=lambda x: x.difficulty_score, reverse=True)

    return DifficultyEngineOutput(
        engine_version=ENGINE_VERSION,
        generated_at=now.isoformat(),
        items=items,
    )
