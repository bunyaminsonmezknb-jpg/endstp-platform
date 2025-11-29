"""
Priority Engine - Strategic Prioritization
Hangi konuya önce çalışmalı? Stratejik önceliklendirme motoru
"""

from typing import List, Optional
from pydantic import BaseModel, Field
import random


class TopicInput(BaseModel):
    """Konu girdi verisi"""
    id: str = Field(description="Konu ID")
    name: str = Field(description="Konu adı")
    course_importance: float = Field(description="Ders önemi (soru sayısı/katsayı)")
    topic_weight: float = Field(ge=0, le=1, description="Konunun sınavdaki ağırlığı (0-1)")
    
    # Performans
    correct: int = Field(ge=0)
    wrong: int = Field(ge=0)
    blank: int = Field(ge=0)
    total_questions: int = Field(gt=0)
    
    # Opsiyonel süre
    duration_minutes: Optional[float] = None


class PriorityConfig(BaseModel):
    """Motor konfigürasyonu"""
    weight_blank: float = 4.0
    weight_wrong: float = 2.5
    weight_failure: float = 1.5
    ideal_time_per_question: float = 1.5
    speed_penalty_threshold: float = 1.3
    speed_bonus_threshold: float = 0.7
    absolute_critical_threshold: float = 15.0  # Ham puan altında KRİTİK verme


class PriorityOutput(BaseModel):
    """Öncelik sonucu"""
    topic_id: str
    topic_name: str
    priority_score: float = Field(description="Öncelik puanı (0-100)")
    priority_level: str = Field(description="LOW/MEDIUM/HIGH/CRITICAL")
    analysis: dict = Field(description="Alt faktörler")
    suggestion: str = Field(description="Öğrenciye öneri")


class PriorityEngine:
    """
    Stratejik önceliklendirme motoru
    
    Formül: GapScore × StrategicValue × SpeedMultiplier × 100
    
    GapScore = (Boş×4 + Yanlış×2.5 + Başarısızlık×1.5)
    StrategicValue = topic_weight × course_importance
    SpeedMultiplier = 1.0 (normal), 1.25 (yavaş), 0.8 (hızlı)
    """
    
    DEFAULT_CONFIG = PriorityConfig()
    
    @classmethod
    def analyze(
        cls,
        topics: List[TopicInput],
        config: Optional[PriorityConfig] = None
    ) -> List[PriorityOutput]:
        """
        Konu listesini analiz et ve öncelik sırasına göre döndür
        
        Args:
            topics: Konu listesi
            config: Özel konfigurasyon (opsiyonel)
            
        Returns:
            List[PriorityOutput]: Öncelik sıralı liste
        """
        
        if not config:
            config = cls.DEFAULT_CONFIG
        
        if not topics:
            return []
        
        # 1. Her konu için ham puan hesapla
        calculated_data = []
        
        for topic in topics:
            if topic.total_questions <= 0:
                continue
            
            # Oranlar
            blank_rate = topic.blank / topic.total_questions
            wrong_rate = topic.wrong / topic.total_questions
            success_rate = topic.correct / topic.total_questions
            failure_rate = 1 - success_rate
            
            # Bilgi Eksikliği Puanı (Gap Score)
            # (Boş × 4) + (Yanlış × 2.5) + (Başarısızlık × 1.5)
            gap_score = (
                (blank_rate * config.weight_blank) +
                (wrong_rate * config.weight_wrong) +
                (failure_rate * config.weight_failure)
            )
            
            # Hız Çarpanı (Speed Multiplier)
            speed_mult = 1.0
            speed_note = "Normal"
            
            if topic.duration_minutes and topic.duration_minutes > 0:
                ideal_duration = topic.total_questions * config.ideal_time_per_question
                pace_ratio = topic.duration_minutes / ideal_duration
                
                if pace_ratio > config.speed_penalty_threshold:
                    # Yavaş → Risk var
                    speed_mult = 1.25
                    speed_note = "Yavaş"
                elif pace_ratio < config.speed_bonus_threshold and success_rate > 0.8:
                    # Hızlı ve Başarılı → Ustalaşmış
                    speed_mult = 0.8
                    speed_note = "Hızlı"
            
            # Stratejik Değer
            strategic_value = topic.topic_weight * topic.course_importance
            
            # Nihai Ham Puan
            raw_priority = gap_score * strategic_value * speed_mult * 100
            
            calculated_data.append({
                "topic": topic,
                "raw_priority": raw_priority,
                "gap_score": gap_score,
                "strategic_value": strategic_value,
                "speed_mult": speed_mult,
                "speed_note": speed_note
            })
        
        if not calculated_data:
            return []
        
        # 2. Normalizasyon (0-100)
        max_raw = max(d["raw_priority"] for d in calculated_data)
        min_raw = min(d["raw_priority"] for d in calculated_data)
        range_raw = max_raw - min_raw if max_raw > min_raw else 1
        
        # 3. Çıktı üretimi
        results = []
        
        for item in calculated_data:
            # Relative Score
            normalized = ((item["raw_priority"] - min_raw) / range_raw) * 100
            
            # Kategori belirleme
            level = "LOW"
            suggestion = ""
            
            # ABSOLUTE THRESHOLD KORUMASI
            is_raw_low = item["raw_priority"] < config.absolute_critical_threshold
            
            if normalized < 40 or is_raw_low:
                level = "LOW"
                suggestion = "Öncelikli değil. Mevcut durumun yeterli, koruma tekrarları yap."
                
                # İyi öğrenci için uyarı
                if normalized > 70 and is_raw_low:
                    suggestion = "Listedeki diğerlerine göre en zayıfın, ama genel durumun iyi. Panik yapma."
                    normalized = min(normalized, 45)  # Görsel düzeltme
            
            elif normalized < 75:
                level = "MEDIUM"
                suggestion = "Geliştirilmesi gerek. Programına ekle."
            
            else:
                level = "HIGH"
                suggestion = "Sınav başarını doğrudan etkiliyor. Acil çalışmalısın."
                
                # CRITICAL kontrolü
                if item["raw_priority"] > (config.absolute_critical_threshold * 2):
                    level = "CRITICAL"
                    suggestion = "ALARM: Bu konu puanını ciddi şekilde aşağı çekiyor. İlk sıraya al."
            
            # Hız uyarısı ekle
            if item["speed_mult"] > 1.0:
                suggestion += " (Not: İşlem hızın sınav standartlarının altında.)"
            
            results.append(PriorityOutput(
                topic_id=item["topic"].id,
                topic_name=item["topic"].name,
                priority_score=round(normalized, 1),
                priority_level=level,
                analysis={
                    "raw_gap_score": round(item["gap_score"], 2),
                    "speed_factor": item["speed_mult"],
                    "speed_note": item["speed_note"],
                    "strategic_impact": round(item["strategic_value"], 2)
                },
                suggestion=suggestion
            ))
        
        # Öncelik sırasına göre sırala (en yüksek önce)
        results.sort(key=lambda x: x.priority_score, reverse=True)
        
        return results


# Test fonksiyonu
def test_priority_engine():
    """Örnek testler"""
    
    print("=" * 70)
    print("PRIORITY ENGINE TEST")
    print("=" * 70)
    
    # Test konuları
    topics = [
        # 1. Fonksiyonlar: Önemli konu, boş çok, yavaş
        TopicInput(
            id="t1",
            name="Fonksiyonlar",
            correct=7,
            wrong=1,
            blank=2,
            total_questions=10,
            duration_minutes=20,  # İdeal: 15 dk (yavaş)
            topic_weight=0.15,
            course_importance=40
        ),
        
        # 2. Kümeler: Az önemli, çok yanlış, hızlı
        TopicInput(
            id="t2",
            name="Kümeler",
            correct=2,
            wrong=8,
            blank=0,
            total_questions=10,
            duration_minutes=10,  # İdeal: 15 dk (hızlı)
            topic_weight=0.05,
            course_importance=40
        ),
        
        # 3. Mantık: Full, hızlı
        TopicInput(
            id="t3",
            name="Mantık",
            correct=10,
            wrong=0,
            blank=0,
            total_questions=10,
            duration_minutes=12,
            topic_weight=0.03,
            course_importance=40
        ),
        
        # 4. Türev: Çok önemli, orta başarı
        TopicInput(
            id="t4",
            name="Türev",
            correct=5,
            wrong=3,
            blank=2,
            total_questions=10,
            topic_weight=0.125,
            course_importance=40
        )
    ]
    
    # Analiz yap
    results = PriorityEngine.analyze(topics)
    
    print(f"\n📊 ÖNCELIK SIRALAMASI ({len(results)} konu):\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.topic_name} [{result.priority_level}]")
        print(f"   Priority Score: {result.priority_score}")
        print(f"   Gap Score: {result.analysis['raw_gap_score']}")
        print(f"   Strategic Impact: {result.analysis['strategic_impact']}")
        print(f"   Speed: {result.analysis['speed_note']} (×{result.analysis['speed_factor']})")
        print(f"   💡 {result.suggestion}")
        print()
    
    print("=" * 70)
    
    # İyi öğrenci testi (Absolute Threshold)
    print("\n🎓 İYİ ÖĞRENCİ TESTİ (Absolute Threshold):\n")
    
    good_topics = [
        TopicInput(
            id="g1", name="Geometri",
            correct=9, wrong=1, blank=0, total_questions=10,
            topic_weight=0.1, course_importance=40
        ),
        TopicInput(
            id="g2", name="Olasılık",
            correct=8, wrong=2, blank=0, total_questions=10,
            topic_weight=0.08, course_importance=40
        ),
        TopicInput(
            id="g3", name="Kombinasyon",
            correct=10, wrong=0, blank=0, total_questions=10,
            topic_weight=0.05, course_importance=40
        )
    ]
    
    good_results = PriorityEngine.analyze(good_topics)
    
    for i, result in enumerate(good_results, 1):
        print(f"{i}. {result.topic_name} [{result.priority_level}]")
        print(f"   Score: {result.priority_score}")
        print(f"   💡 {result.suggestion}")
        print()
    
    print("=" * 70)


if __name__ == "__main__":
    test_priority_engine()
