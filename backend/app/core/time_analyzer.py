"""
Time Analyzer - Speed Intelligence
İşlem hızı analizi ve zorluk modifikasyonu
"""

from typing import Optional
from pydantic import BaseModel, Field


class TimeAnalysisResult(BaseModel):
    """Süre analiz sonucu"""
    pace_ratio: float = Field(description="Tempo oranı (1.0 = ideal)")
    time_modifier: float = Field(description="Zorluk çarpanı (0.9-1.15)")
    analysis: str = Field(description="Metin açıklama")
    is_fast: bool = Field(description="Hızlı mı?")
    is_slow: bool = Field(description="Yavaş mı?")


class TimeAnalyzer:
    """
    Süre bazlı tempo analizi
    
    Mantık:
    - Hızlı (< %70 ideal): Modifier 0.9 (zorluk düşür)
    - Normal (%70-130): Modifier 1.0 (değişiklik yok)
    - Yavaş (> %130 ideal): Modifier 1.15 (zorluk artır)
    """
    
    # Eşikler
    FAST_THRESHOLD = 0.7      # İdeal sürenin %70'i
    SLOW_THRESHOLD = 1.3      # İdeal sürenin %130'u
    FAST_MODIFIER = 0.9       # Hızlı → Zorluk düşür
    SLOW_MODIFIER = 1.15      # Yavaş → Zorluk artır
    
    @classmethod
    def analyze(
        cls,
        total_duration: Optional[float],
        total_questions: int,
        ideal_time_per_question: float = 1.5,
        success_rate: Optional[float] = None
    ) -> TimeAnalysisResult:
        """
        Süre analizi yap
        
        Args:
            total_duration: Toplam süre (dakika), None ise atla
            total_questions: Soru sayısı
            ideal_time_per_question: Soru başı ideal süre (dk)
            success_rate: Başarı oranı (0-1), hızlı ve başarılı için
            
        Returns:
            TimeAnalysisResult: Tempo analizi
        """
        
        # Süre girilmemişse nötr dön
        if total_duration is None or total_duration <= 0:
            return TimeAnalysisResult(
                pace_ratio=1.0,
                time_modifier=1.0,
                analysis="Süre bilgisi yok",
                is_fast=False,
                is_slow=False
            )
        
        # İdeal süre hesapla
        ideal_duration = total_questions * ideal_time_per_question
        
        # Tempo oranı (1.0 = tam zamanında)
        pace_ratio = total_duration / ideal_duration
        
        # Modifier ve analiz
        modifier = 1.0
        is_fast = False
        is_slow = False
        analysis = "Normal tempo"
        
        # HIZLI: %30'dan daha hızlı
        if pace_ratio < cls.FAST_THRESHOLD:
            is_fast = True
            
            # Eğer başarılıysa (>%80) → Ustalaşmış
            if success_rate and success_rate > 0.8:
                modifier = cls.FAST_MODIFIER
                analysis = "Çok hızlı ve başarılı! Konuya hakim. (Zorluk düşürüldü)"
            else:
                # Hızlı ama başarısız → Dikkatsizlik
                modifier = 1.0
                analysis = "Hızlı ama hatalı. Daha dikkatli ol."
        
        # YAVAŞ: %30'dan daha uzun
        elif pace_ratio > cls.SLOW_THRESHOLD:
            is_slow = True
            modifier = cls.SLOW_MODIFIER
            minutes_over = round((total_duration - ideal_duration), 1)
            analysis = f"Yavaş tempo. İdeal süreden {minutes_over} dk fazla. (Zorluk artırıldı)"
        
        # NORMAL
        else:
            analysis = "Normal tempo. İdeal sürede tamamladın."
        
        return TimeAnalysisResult(
            pace_ratio=round(pace_ratio, 2),
            time_modifier=round(modifier, 2),
            analysis=analysis,
            is_fast=is_fast,
            is_slow=is_slow
        )
    
    @classmethod
    def apply_to_difficulty(
        cls,
        base_difficulty: float,
        time_analysis: TimeAnalysisResult
    ) -> float:
        """
        Zorluk puanına süre modifierini uygula
        
        Args:
            base_difficulty: Temel zorluk (0-100)
            time_analysis: Süre analiz sonucu
            
        Returns:
            float: Güncellenmiş zorluk (0-100)
        """
        
        modified = base_difficulty * time_analysis.time_modifier
        return max(0, min(100, round(modified, 2)))


# Test fonksiyonu
def test_time_analyzer():
    """Örnek testler"""
    
    print("=" * 60)
    print("TIME ANALYZER TEST")
    print("=" * 60)
    
    # Test 1: Hızlı ve başarılı (Ustalaşmış)
    result1 = TimeAnalyzer.analyze(
        total_duration=10,      # 10 dk
        total_questions=10,     # 10 soru
        ideal_time_per_question=1.5,  # İdeal: 15 dk
        success_rate=0.9        # %90 başarı
    )
    print(f"\n1. HIZLI & BAŞARILI:")
    print(f"   Süre: 10 dk (İdeal: 15 dk)")
    print(f"   Pace Ratio: {result1.pace_ratio} (< 0.7 → Hızlı)")
    print(f"   Modifier: {result1.time_modifier}")
    print(f"   Analiz: {result1.analysis}")
    
    # Test 2: Hızlı ama başarısız (Dikkatsizlik)
    result2 = TimeAnalyzer.analyze(
        total_duration=10,
        total_questions=10,
        ideal_time_per_question=1.5,
        success_rate=0.4        # %40 başarı
    )
    print(f"\n2. HIZLI AMA BAŞARISIZ:")
    print(f"   Süre: 10 dk (İdeal: 15 dk)")
    print(f"   Pace Ratio: {result2.pace_ratio}")
    print(f"   Modifier: {result2.time_modifier} (Değişiklik yok)")
    print(f"   Analiz: {result2.analysis}")
    
    # Test 3: Yavaş (Risk)
    result3 = TimeAnalyzer.analyze(
        total_duration=25,      # 25 dk
        total_questions=10,
        ideal_time_per_question=1.5,  # İdeal: 15 dk
        success_rate=0.7
    )
    print(f"\n3. YAVAŞ:")
    print(f"   Süre: 25 dk (İdeal: 15 dk)")
    print(f"   Pace Ratio: {result3.pace_ratio} (> 1.3 → Yavaş)")
    print(f"   Modifier: {result3.time_modifier}")
    print(f"   Analiz: {result3.analysis}")
    
    # Test 4: Normal
    result4 = TimeAnalyzer.analyze(
        total_duration=15,
        total_questions=10,
        ideal_time_per_question=1.5
    )
    print(f"\n4. NORMAL:")
    print(f"   Süre: 15 dk (İdeal: 15 dk)")
    print(f"   Pace Ratio: {result4.pace_ratio}")
    print(f"   Modifier: {result4.time_modifier}")
    print(f"   Analiz: {result4.analysis}")
    
    # Test 5: Süre yok
    result5 = TimeAnalyzer.analyze(
        total_duration=None,
        total_questions=10
    )
    print(f"\n5. SÜRE GİRİLMEMİŞ:")
    print(f"   Modifier: {result5.time_modifier} (Nötr)")
    print(f"   Analiz: {result5.analysis}")
    
    # Test 6: Zorluk modifikasyonu
    print(f"\n6. ZORLUK MODİFİKASYONU:")
    base_diff = 50.0
    print(f"   Temel Zorluk: {base_diff}")
    print(f"   Hızlı (0.9x): {TimeAnalyzer.apply_to_difficulty(base_diff, result1)}")
    print(f"   Normal (1.0x): {TimeAnalyzer.apply_to_difficulty(base_diff, result4)}")
    print(f"   Yavaş (1.15x): {TimeAnalyzer.apply_to_difficulty(base_diff, result3)}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_time_analyzer()
