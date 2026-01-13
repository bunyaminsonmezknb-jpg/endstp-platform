# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: {FILENAME}
# Created: {DATE}
# Phase: MVP (Phase 1)
# Author: End.STP Team
# # Phase: FAZ 3 – Stub Performance Layer
# 🌍 LOCALIZATION STATUS:
#   [ ] UTC datetime handling
#   [ ] Multi-language support (Phase 2)
#   [ ] Database uses _tr/_en columns
#   [ ] API accepts Accept-Language header (Phase 2)
#   [ ] No hardcoded text
#
# 📋 HARDCODED ITEMS (Temporary - Mark with line numbers):
#   - (None yet - Add items as you code)
#   - Example: "TURKISH_MONTHS dict (Line 45) → Phase 2: Database lookup"
#
# 🚀 MIGRATION NOTES (Phase 2 Actions):
#   - (Actions will be listed here)
#   - Example: "Replace format_date_turkish() with format_date_localized()"
#
# 📚 RELATED DOCS:
#   - Guidelines: docs/GLOBAL_FIRST_GUIDE.md
#   - Migration: docs/PHASE2_MIGRATION_PLAN.md
# =============================================================================

"""
{FILENAME} - {SHORT_DESCRIPTION}

{DETAILED_DESCRIPTION}

Usage:
    {USAGE_EXAMPLE}
"""

# =============================================================================
# YOUR CODE STARTS HERE
# =============================================================================

# TODO: Implement your functions

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

# ❗ FAZ-3 STUB
# Gerçek hesaplar FAZ-4'te gelecek


def get_student_performance(
    student_id: str,
    use_cache: bool = True
) -> Dict[str, Any]:
    """
    FAZ-3 PERFORMANCE CONTRACT (STUB)

    Returns structure only.
    No real calculation yet.
    """

    return {
        "topic_performance": {},
        "all_tests": [],
        "projection": None,
        "metadata": {
            "source": "stub",
            "cached": False,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    }