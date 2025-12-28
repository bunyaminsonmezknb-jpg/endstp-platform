from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal
from datetime import datetime


# ============================================
# AUTH SCHEMAS
# ============================================

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    role: Literal["student", "teacher", "admin"] = "student"


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    message: str
    access_token: str
    user: dict


# ============================================
# TEST ENTRY SCHEMAS
# ============================================

class TestResultCreate(BaseModel):
    student_id: str  # UUID from Supabase
    subject: str
    topic: str
    correct_count: int = Field(..., ge=0)
    wrong_count: int = Field(..., ge=0)
    empty_count: int = Field(..., ge=0)
    net: float = Field(..., ge=0)
    success_rate: float = Field(..., ge=0, le=100)
    entry_timestamp: datetime


class TestResultResponse(BaseModel):
    message: str
    data: dict


# ============================================
# FORMS SCHEMAS (Subjects, Topics, etc.)
# ============================================

class SubjectResponse(BaseModel):
    id: str
    code: str
    name_tr: str
    icon: str
    color: str


class TopicResponse(BaseModel):
    id: str
    code: str
    name_tr: str
    difficulty_level: Optional[int]
    exam_weight: Optional[float]


class EducationLevelResponse(BaseModel):
    id: str
    code: str
    name_tr: str
    grade_range: str


class ClassLevelResponse(BaseModel):
    id: str
    code: str
    name_tr: str
    grade_number: int


# ============================================
# STUDENT DASHBOARD SCHEMAS (Existing)
# ============================================


class DailyGoal(BaseModel):
    current: int = Field(..., description="Bugünkü tamamlanan soru sayısı")
    target: int = Field(..., description="Bugünkü hedef soru sayısı")


class AchievementBadge(BaseModel):
    text: str = Field(..., description="Badge metni, örn: '+%40 (3 gün)'")
    icon: str = Field(..., description="Badge ikonu, örn: '⭐'")


class Topic(BaseModel):
    id: int
    name: str = Field(..., description="Konu adı, örn: 'Türev'")
    subject: str = Field(..., description="Ders adı, örn: 'Matematik'")
    remembering_rate: float = Field(..., ge=0, le=100, description="Hatırlama oranı (0-100)")
    status: Literal["critical", "warning", "good", "excellent", "frozen"]
    status_text: str = Field(..., description="Durum metni, örn: 'KRİTİK DURUM'")
    emoji: str = Field(..., description="Durum emojisi")
    achievement_badge: Optional[AchievementBadge] = None


class CriticalAlert(BaseModel):
    show: bool
    topic_name: str
    days_ago: int = Field(..., description="Kaç gün önce çalışıldı")
    forget_risk: int = Field(..., ge=0, le=100, description="Unutma riski yüzdesi")


class StudentDashboardResponse(BaseModel):
    student_name: str
    streak: int = Field(..., ge=0, description="Kaç gündür aralıksız çalışıyor")
    daily_goal: DailyGoal
    weekly_success: int = Field(..., ge=0, le=100, description="Son 7 gün başarı yüzdesi")
    weekly_target: int = Field(..., ge=0, le=100, description="Haftalık hedef yüzde")
    study_time_today: int = Field(..., ge=0, description="Bugünkü çalışma süresi (dakika)")
    weekly_questions: int = Field(..., ge=0, description="Bu hafta çözülen soru sayısı")
    weekly_increase: int = Field(..., description="Haftalık artış yüzdesi")
    topics: List[Topic] = Field(..., max_length=10, description="En fazla 10 konu")
    critical_alert: Optional[CriticalAlert] = None


class PartnerLink(BaseModel):
    id: str
    partner_type: Literal["video", "book", "course", "self"]
    partner_name: str = Field(..., description="Partner adı, örn: 'Dr. Biyoloji'")
    title: str = Field(..., description="Link başlığı")
    subtitle: str = Field(..., description="Link açıklaması")
    url: str = Field(..., description="Partner linki (affiliate/referral)")
    icon: str = Field(default="📹", description="İkon")
    duration: Optional[str] = Field(None, description="Süre bilgisi, örn: '15 dk'")


class RecoveryPlanResponse(BaseModel):
    topic_id: int
    topic_name: str
    partner_links: List[PartnerLink]


class TopicUpdateRequest(BaseModel):
    topic_id: int
    new_remembering_rate: float = Field(..., ge=0, le=100)
    study_completed: bool = Field(default=False, description="Çalışma tamamlandı mı?")
