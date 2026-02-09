# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: router.py
# Role: Admin API router aggregation
# Created: 2026-02-09
# Author: End.STP Team
#
# Golden rules:
# - Aggregates all admin sub-routers
# - Modular design (features, dashboard, audit separate)
# - Included in api.py with prefix="/admin"
# =============================================================================

from fastapi import APIRouter
from . import features, dashboard, audit

router = APIRouter()

# Feature flags
router.include_router(features.router, tags=["admin-features"])

# Dashboard settings
router.include_router(dashboard.router, tags=["admin-dashboard"])

# Audit log
router.include_router(audit.router, tags=["admin-audit"])
