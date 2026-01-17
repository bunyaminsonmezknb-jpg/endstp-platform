from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DifficultyTopicInput:
    topic_id: str
    topic_name: str
    subject_name: str

    success_rate: Optional[float] = None      # 0..100
    wrong_rate: Optional[float] = None        # 0..100
    blank_rate: Optional[float] = None        # 0..100
    test_count: Optional[int] = None
    avg_time_sec: Optional[float] = None      # soru başı süre
    last_test_date: Optional[str] = None      # ISO string


@dataclass(frozen=True)
class DifficultyReason:
    code: str
    weight: float
    description: Optional[str] = None


@dataclass(frozen=True)
class DifficultyItem:
    topic_id: str
    topic_name: str
    subject_name: str
    difficulty_score: float
    reasons: List[DifficultyReason] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DifficultyEngineInput:
    topics: List[DifficultyTopicInput]
    engine_version: str = "difficulty_v4b.1"
    now: Optional[datetime] = None


@dataclass(frozen=True)
class DifficultyEngineOutput:
    engine_version: str
    generated_at: str
    items: List[DifficultyItem]
