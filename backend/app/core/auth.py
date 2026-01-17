# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: auth.py
# Created: 2025-01-02
# Phase: MVP (Phase 1)
# Author: End.STP Team
#
# ROLE:
# - Domain-level auth aliases
# - Student / Admin abstraction
# - NO JWT LOGIC HERE
#
# IMPORTANT:
# - This file MUST remain thin
# - Real auth logic lives in auth_hs256.py
# =============================================================================

"""
Auth Domain Aliases
-------------------
This module exposes semantic aliases for authentication dependencies.

Actual JWT validation is implemented in:
    app.core.auth_hs256
"""

from app.core.auth_hs256 import (
    get_current_user,
    get_current_active_user,
)

# =========================================================
# DOMAIN ALIASES
# =========================================================

# Student-facing APIs
get_current_student = get_current_user

# Future-proof placeholders
get_current_admin = get_current_user
get_current_institution_user = get_current_user
