# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/api/v1/deps.py
# Created: 2026-02-11
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# 🌍 LOCALIZATION STATUS:
#   [x] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [x] No hardcoded text
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - (None yet)
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - (None yet)
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
#   - Migration: docs/PHASE2_MIGRATION_PLAN.md
# =============================================================================

"""
deps.py - API dependency helpers (FastAPI deps)

Phase-1: Common dependency utilities (auth/guards/db/session helpers) are located here.

Usage:
    from app.api.v1.deps import <dependency>
"""

from datetime import datetime, timezone  # ⚠️ ALWAYS use timezone.utc!

# =============================================================================
# YOUR CODE STARTS HERE
# =============================================================================

def utc_now() -> datetime:
    """Return timezone-aware UTC now (global-first standard)."""
    return datetime.now(timezone.utc)

# TODO:
# - If you already have dependency functions in this file, keep them below.
# - Do not add hardcoded text; prefer constants or i18n layer later.
