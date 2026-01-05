"""
Schemas Package
Pydantic schemas for request/response validation
"""

from .auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserInfo,
    PasswordResetRequest,
    PasswordResetConfirm,
)

from .student import (
    StudentProfile,
    StudentStats,
    TopicHealth,
    StudentDashboard,
    ProgressUpdate,
    GoalCreate,
    GoalResponse,
)

from .test import (
    TopicResult,
    TestEntryRequest,
    TestEntryResponse,
    TestRecordSummary,
    TestRecordDetail,
    TopicResultDetail,
    TestListRequest,
    TestListResponse,
)

__all__ = [
    # Auth
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "UserInfo",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    # Student
    "StudentProfile",
    "StudentStats",
    "TopicHealth",
    "StudentDashboard",
    "ProgressUpdate",
    "GoalCreate",
    "GoalResponse",
    # Test
    "TopicResult",
    "TestEntryRequest",
    "TestEntryResponse",
    "TestRecordSummary",
    "TestRecordDetail",
    "TopicResultDetail",
    "TestListRequest",
    "TestListResponse",
]