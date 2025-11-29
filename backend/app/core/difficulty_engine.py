"""
Difficulty Analysis Engine (VBA Logic Port)
Öğrenci performansına göre konu öğrenme zorluğu hesaplama
"""

from typing import Optional
from pydantic import BaseModel, Field


class StatMetrics(BaseModel):
    """Test istatistikleri"""
    total_questions: int = Field(gt=0, description="Toplam soru")
    correct: int = Field(ge=0, description="Doğru sayısı")
    wrong: int = Field(ge=0, description="Yanlış sayısı")
    blank: int = Field(ge=0, description="Boş sayısı")
    net: float = Field(description="Net puan")


class DifficultyResult(BaseModel):
    """Zorluk analiz sonucu"""
    difficulty_percentage: float = Field(description="Zorluk yüzdesi (0-100)")
    difficulty_level: int = Field(ge=1, le=5, description="Zorluk seviyesi (1-5)")
    factors: dict = Field(description="Alt faktörler")
    analysis: str = Field(description="Metin analiz")


class DifficultyEngine:
    """
    VBA mantığını koruyan zorluk analiz motoru
    
    Formül: (Boş×0.8 + Yanlış×0.4) × (1 - Net³)
    Bağlam: %70 Konu + %30 Ders Geneli
    """
    
    # Katsayılar (VBA'dan)
    BLANK_WEIGHT_TOPIC = 0.8
    WRONG_WEIGHT_TOPIC = 0.4
    BLANK_WEIGHT_COURSE = 0.9
    WRONG_WEIGHT_COURSE = 0.4
    POWER_FACTOR_TOPIC = 3
    POWER_FACTOR_COURSE = 2
    
    @classmethod
    def calculate(
        cls,
        topic_stats: StatMetrics,
        course_total_stats: Optional[StatMetrics] = None
    ) -> DifficultyResult:
        """
        Konu zorluğunu hesapla
        
        Args:
            topic_stats: Konunun istatistikleri
            course_total_stats: Dersin tüm istatistikleri (opsiyonel)
            
        Returns:
            DifficultyResult: Zorluk analizi
        """
        
        # 1. KONU BAZLI ZORLUK (Topic Score)
        topic_difficulty = cls._calculate_topic_difficulty(topic_stats)
        
        # 2. BAĞLAMSAL ZORLUK (Context Score)
        if course_total_stats and course_total_stats.total_questions > topic_stats.total_questions:
            context_difficulty = cls._calculate_context_difficulty(
                topic_stats, 
                course_total_stats
            )
        else:
            # Ders verisi yoksa, konu zorluğunu kullan
            context_difficulty = topic_difficulty
        
        # 3. NİHAİ ZORLUK (Weighted Final)
        # VBA: %70 Konu + %30 Ders Geneli
        final_percentage = (topic_difficulty * 0.70) + (context_difficulty * 0.30)
        final_percentage = min(100, max(0, final_percentage * 100))
        
        # 4. SEVİYE DÖNÜŞÜMÜ (1-5 Skalası)
        level = cls._percentage_to_level(final_percentage)
        
        # 5. YORUM ÜRET
        analysis = cls._generate_analysis(level, topic_stats)
        
        return DifficultyResult(
            difficulty_percentage=round(final_percentage, 2),
            difficulty_level=level,
            factors={
                "topic_stress": round(topic_difficulty, 2),
                "context_stress": round(context_difficulty, 2)
            },
            analysis=analysis
        )
    
    @classmethod
    def _calculate_topic_difficulty(cls, stats: StatMetrics) -> float:
        """Konu bazlı zorluk hesapla"""
        
        if stats.total_questions <= 0:
            return 0.0
        
        blank_rate = stats.blank / stats.total_questions
        wrong_rate = stats.wrong / stats.total_questions
        net_rate = stats.net / stats.total_questions
        
        # VBA Mantığı: Boş (0.8) > Yanlış (0.4)
        raw_stress = (blank_rate * cls.BLANK_WEIGHT_TOPIC) + (wrong_rate * cls.WRONG_WEIGHT_TOPIC)
        
        # Power Factor: Net düştükçe zorluk üssel artar
        performance_factor = 1 - pow(max(-1, net_rate), cls.POWER_FACTOR_TOPIC)
        
        return max(0, raw_stress * performance_factor)
    
    @classmethod
    def _calculate_context_difficulty(
        cls,
        topic_stats: StatMetrics,
        course_stats: StatMetrics
    ) -> float:
        """Ders geneli bağlamsal zorluk"""
        
        # Ders toplamından şu anki konuyu çıkar
        rest_q = course_stats.total_questions - topic_stats.total_questions
        rest_wrong = course_stats.wrong - topic_stats.wrong
        rest_blank = course_stats.blank - topic_stats.blank
        rest_net = course_stats.net - topic_stats.net
        
        if rest_q <= 0:
            return 0.0
        
        c_blank_rate = rest_blank / rest_q
        c_wrong_rate = rest_wrong / rest_q
        c_net_rate = rest_net / rest_q
        
        # VBA: Genel derste boş ağırlığı 0.9'a çıkarılmış
        course_stress = (c_blank_rate * cls.BLANK_WEIGHT_COURSE) + (c_wrong_rate * cls.WRONG_WEIGHT_COURSE)
        
        # Power Factor 2 (daha yumuşak)
        c_perf_factor = 1 - pow(max(-1, c_net_rate), cls.POWER_FACTOR_COURSE)
        
        return max(0, course_stress * c_perf_factor)
    
    @staticmethod
    def _percentage_to_level(percentage: float) -> int:
        """Yüzdeyi 1-5 seviyesine dönüştür"""
        if percentage > 80:
            return 5  # Çok Zor
        elif percentage > 60:
            return 4  # Zor
        elif percentage > 40:
            return 3  # Orta
        elif percentage > 20:
            return 2  # Kolay
        else:
            return 1  # Çok Kolay
    
    @staticmethod
    def _generate_analysis(level: int, stats: StatMetrics) -> str:
        """Seviyeye göre metin üret"""
        
        blank_rate = stats.blank / stats.total_questions
        
        if level == 5:
            if blank_rate > 0.4:
                return "Kritik seviyede zorlanma. Temel eksikliği yüksek (Boş oranı fazla)."
            else:
                return "Kritik seviyede zorlanma. Kavram yanılgıları var (Yanlış oranı yüksek)."
        elif level == 4:
            return "Zor konu. Öncelikli çalışma gerekiyor."
        elif level == 3:
            return "Orta seviye güçlük. Pratik eksikliği olabilir."
        elif level == 2:
            return "Kolay konu. Küçük eksiklikler var."
        else:
            return "Konuya hakimiyet tam. Zorluk seviyesi düşük."


# Test fonksiyonu
def test_difficulty_engine():
    """Örnek testler"""
    
    # Test 1: Çok boş bırakmış (Zor)
    topic1 = StatMetrics(
        total_questions=10,
        correct=4,
        wrong=2,
        blank=4,
        net=3.0
    )
    result1 = DifficultyEngine.calculate(topic1)
    print(f"Test 1 (Çok Boş): Level={result1.difficulty_level}, %{result1.difficulty_percentage}")
    print(f"  Analiz: {result1.analysis}\n")
    
    # Test 2: Çok yanlış yapmış (Orta-Zor)
    topic2 = StatMetrics(
        total_questions=10,
        correct=2,
        wrong=8,
        blank=0,
        net=-4.0
    )
    result2 = DifficultyEngine.calculate(topic2)
    print(f"Test 2 (Çok Yanlış): Level={result2.difficulty_level}, %{result2.difficulty_percentage}")
    print(f"  Analiz: {result2.analysis}\n")
    
    # Test 3: Full (Çok Kolay)
    topic3 = StatMetrics(
        total_questions=10,
        correct=10,
        wrong=0,
        blank=0,
        net=10.0
    )
    result3 = DifficultyEngine.calculate(topic3)
    print(f"Test 3 (Full): Level={result3.difficulty_level}, %{result3.difficulty_percentage}")
    print(f"  Analiz: {result3.analysis}\n")
    
    # Test 4: Course Context ile
    course = StatMetrics(
        total_questions=100,
        correct=60,
        wrong=20,
        blank=20,
        net=50.0
    )
    result4 = DifficultyEngine.calculate(topic1, course)
    print(f"Test 4 (Context ile): Level={result4.difficulty_level}, %{result4.difficulty_percentage}")
    print(f"  Topic Stress: {result4.factors['topic_stress']}")
    print(f"  Context Stress: {result4.factors['context_stress']}")
    print(f"  Analiz: {result4.analysis}")


if __name__ == "__main__":
    test_difficulty_engine()
