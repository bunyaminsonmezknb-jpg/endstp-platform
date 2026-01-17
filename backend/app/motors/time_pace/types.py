from __future__ import annotations

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
    engine_version: str = "time_v4b.1"
    now: Optional[datetime] = None


@dataclass(frozen=True)
class TimeEngineOutput:
    engine_version: str
    generated_at: str
    items: List[TimeItem]
