# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/motors/bs_model/wrapper.py
# Created: 2026-01-17
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling (generated_at uses UTC)
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [ ] No hardcoded text
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - fallback_reason strings (Phase 2: i18n)
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - When v2 is wired, pass ContextService + SegmentationEngine
#   - Add feature-flag gating by subscription tier
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
#   - Migration: docs/PHASE2_MIGRATION_PLAN.md
# =============================================================================

from typing import Any, Optional, Dict
from datetime import datetime, timezone
import os

from .types import (
    BSModelRequest,
    BSModelWrappedResponse,
    BSModelRunContext,
    BSModelEngineVersion,
)
from .v1 import BSModelInput, BSModelV1


def _env_default_engine() -> BSModelEngineVersion:
    """
    Optional env override:
      BS_MODEL_ENGINE=v1|v2
    """
    val = (os.getenv("BS_MODEL_ENGINE") or "").strip().lower()
    if val in ("v1", "v2"):
        return val  # type: ignore[return-value]
    return "v1"


def run_bs_model(
    req: BSModelRequest,
    *,
    context_service: Any = None,
    segmentation_engine: Any = None,
) -> BSModelWrappedResponse:
    """
    Unified BS-Model entrypoint (wrapper + safe fallback).

    Rules:
    - Try selected engine (req.engine_version or env default)
    - If v2 fails for ANY reason -> fallback to v1 (never crash)
    - Always return a stable wrapped response
    """
    selected: BSModelEngineVersion = req.engine_version or _env_default_engine()

    # Parse v1 input safely (pydantic validates)
    input_obj = BSModelInput(**req.input)

    # Always have v1 baseline ready (our safety net)
    v1_out = BSModelV1.calculate(input_obj)

    # If forced v1 -> return immediately
    if selected == "v1":
        return BSModelWrappedResponse(
            **v1_out.dict(),
            used_engine="v1",
            motor_version="v1.0.0",
            generated_at=datetime.now(timezone.utc).isoformat(),
            fallback_used=False,
            fallback_reason=None,
        )

    # Try v2
    try:
        from .v2 import BSModelV2  # local import to keep module load safe

        v2 = BSModelV2(context_service=context_service, segmentation_engine=segmentation_engine)

        v2_result = v2.calculate(
            input_data=input_obj,
            ctx=req.ctx,
            analysis_allowed=req.analysis_allowed,
        )

        # v2_result is expected dict-like; normalize to wrapped response
        return BSModelWrappedResponse(
            status=v2_result.get("status", v1_out.status),
            next_ef=float(v2_result.get("next_ef", v1_out.next_ef)),
            next_ia=int(v2_result.get("next_ia", v1_out.next_ia)),
            next_repetition=int(v2_result.get("next_repetition", v1_out.next_repetition)),
            score=float(v2_result.get("score", v1_out.score)),
            analysis=str(v2_result.get("analysis", v1_out.analysis)),
            used_engine="v2",
            motor_version=str(v2_result.get("motor_version", "v2")),
            generated_at=str(v2_result.get("generated_at", datetime.now(timezone.utc).isoformat())),
            fallback_used=False,
            fallback_reason=None,
        )

    except Exception as e:
        # HARD RULE: Never crash, always fallback to v1
        return BSModelWrappedResponse(
            **v1_out.dict(),
            used_engine="v1",
            motor_version="v1.0.0",
            generated_at=datetime.now(timezone.utc).isoformat(),
            fallback_used=True,
            fallback_reason=f"v2_failed:{type(e).__name__}",
        )
