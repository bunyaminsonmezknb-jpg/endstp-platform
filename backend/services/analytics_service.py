from typing import List, Dict
from models.schemas import (
    StudentDashboardResponse,
    Topic,
    DailyGoal,
    CriticalAlert,
    AchievementBadge,
    PartnerLink,
    RecoveryPlanResponse,
)


class AnalyticsService:
    """
    Öğrenci analitikleri ve unutma eğrisi hesaplamaları
    """
    
    @staticmethod
    def calculate_topic_status(remembering_rate: float) -> Dict[str, str]:
        """
        Hatırlama oranına göre konu durumunu hesaplar
        
        Args:
            remembering_rate: 0-100 arası hatırlama oranı
            
        Returns:
            status, status_text, emoji içeren dict
        """
        if remembering_rate <= 20:
            return {
                "status": "frozen",
                "status_text": "DONMUŞ - Acil Çöz",
                "emoji": "❄️"
            }
        elif remembering_rate <= 30:
            return {
                "status": "critical",
                "status_text": "KRİTİK DURUM",
                "emoji": "🔥"
            }
        elif remembering_rate <= 60:
            return {
                "status": "warning",
                "status_text": "DİKKAT - Bu Hafta",
                "emoji": "🟡"
            }
        elif remembering_rate <= 80:
            return {
                "status": "good",
                "status_text": "İYİ DURUMDA",
                "emoji": "🟢"
            }
        else:
            return {
                "status": "excellent",
                "status_text": "MÜKEMMEL",
                "emoji": "⭐"
            }
    
    @staticmethod
    def get_mock_student_dashboard(student_id: int) -> StudentDashboardResponse:
        """
        Mock öğrenci dashboard verisi döner
        İleride database'den çekilecek
        """
        return StudentDashboardResponse(
            student_name="Ahmet Yılmaz",
            streak=7,
            daily_goal=DailyGoal(current=5, target=12),
            weekly_success=72,
            weekly_target=85,
            study_time_today=150,
            weekly_questions=45,
            weekly_increase=25,
            topics=[
                Topic(
                    id=1,
                    name="Türev",
                    subject="Matematik",
                    remembering_rate=20,
                    status="critical",
                    status_text="KRİTİK DURUM",
                    emoji="🔥",
                    achievement_badge=AchievementBadge(
                        text="+%40 (3 gün)",
                        icon="⭐"
                    )
                ),
                Topic(
                    id=2,
                    name="Osmanlı Tarihi",
                    subject="Tarih",
                    remembering_rate=85,
                    status="excellent",
                    status_text="MÜKEMMEL",
                    emoji="🟢"
                ),
                Topic(
                    id=3,
                    name="Kinematik",
                    subject="Fizik",
                    remembering_rate=55,
                    status="warning",
                    status_text="DİKKAT - Bu Hafta",
                    emoji="🟡"
                ),
                Topic(
                    id=4,
                    name="Mol Kavramı",
                    subject="Kimya",
                    remembering_rate=15,
                    status="frozen",
                    status_text="DONMUŞ - Acil Çöz",
                    emoji="❄️"
                ),
                Topic(
                    id=5,
                    name="Cümle Çözümleme",
                    subject="Türkçe",
                    remembering_rate=78,
                    status="good",
                    status_text="İYİ DURUMDA",
                    emoji="🟢"
                ),
            ],
            critical_alert=CriticalAlert(
                show=True,
                topic_name="Türev",
                days_ago=2,
                forget_risk=60
            )
        )
    
    @staticmethod
    def get_recovery_plan(topic_id: int, topic_name: str) -> RecoveryPlanResponse:
        """
        Konu için kurtarma planı (partner linkleri) döner
        """
        return RecoveryPlanResponse(
            topic_id=topic_id,
            topic_name=topic_name,
            partner_links=[
                PartnerLink(
                    id="video",
                    partner_type="video",
                    partner_name="Dr. Biyoloji",
                    title=f"{topic_name} Özet Video",
                    subtitle="15 dakika • YouTube",
                    url="https://youtube.com/example",
                    icon="📹",
                    duration="15 dk"
                ),
                PartnerLink(
                    id="book",
                    partner_type="book",
                    partner_name="3D Yayınları",
                    title=f"{topic_name} Test Bankası",
                    subtitle="30 soru • Test 4",
                    url="https://3dyayinlari.com/test",
                    icon="📚",
                    duration="30 soru"
                ),
                PartnerLink(
                    id="self",
                    partner_type="self",
                    partner_name="Kendi Çalışma",
                    title="Kendi Notlarımdan Tekrar Edeceğim",
                    subtitle="Serbest çalışma",
                    url="self-study",
                    icon="📝"
                ),
            ]
        )
    
    @staticmethod
    def update_topic_remembering_rate(
        topic_id: int,
        new_rate: float,
        study_completed: bool
    ) -> Dict[str, any]:
        """
        Konu hatırlama oranını günceller
        İleride database'e yazılacak
        """
        status_data = AnalyticsService.calculate_topic_status(new_rate)
        
        # Simulated response
        return {
            "success": True,
            "topic_id": topic_id,
            "new_remembering_rate": new_rate,
            "new_status": status_data["status"],
            "study_completed": study_completed,
            "message": "Konu durumu güncellendi!"
        }
