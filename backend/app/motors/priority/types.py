from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional, Dict


@dataclass(frozen=True)
class PriorityTopicInput:
    topic_id: str
    topic_name: str
    subject_name: str

    success_rate: Optional[float] = None  # 0..100
    test_count: Optional[int] = None
    last_test_date: Optional[str] = None  # ISO string (UTC tercih)


@dataclass(frozen=True)
class PriorityReason:
    code: str
    weight: float


@dataclass(frozen=True)
class PriorityItem:
    topic_id: str
    topic_name: str
    subject_name: str
    score: float
    reasons: List[PriorityReason] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PriorityEngineInput:
    topics: List[PriorityTopicInput]
    engine_version: str = "priority_v4b.1"
    now: Optional[datetime] = None


@dataclass(frozen=True)
class PriorityEngineOutput:
    engine_version: str
    generated_at: str
    items: List[PriorityItem]
