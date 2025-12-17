"""
Student endpoints - Modular structure
"""
from fastapi import APIRouter

# Ana router
router = APIRouter()

# Alt modülleri import et
from .dashboard import router as dashboard_router
from .tests import router as tests_router
from .analytics import router as analytics_router
from .tasks import router as tasks_router
from .support_feedback import router as support_feedback_router
from .reflex_notifications import router as reflex_notifications_router


# Tüm router'ları birleştir
router.include_router(dashboard_router, tags=["student-dashboard"])
router.include_router(tests_router, tags=["student-tests"])
router.include_router(analytics_router, tags=["student-analytics"])
router.include_router(tasks_router, tags=["student-tasks"])
router.include_router(support_feedback_router, tags=["student-support-feedback"])
router.include_router(reflex_notifications_router, tags=["student-reflex-notifications"])
