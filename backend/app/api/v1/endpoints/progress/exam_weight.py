"""
Progress & Goals - Exam Weight Multiplier
⭐ Priority score calculation with exam weights
"""
from typing import Tuple

def calculate_exam_weight_multiplier(
    exam_weight_data: list
) -> Tuple[float, int]:
    """
    Sınav ağırlığına göre çarpan hesapla
    
    Args:
        exam_weight_data: subject_exam_weights tablosundan question_count'lar
    
    Returns:
        (exam_multiplier, total_exam_questions)
        
    Formula:
        exam_multiplier = min(2.0, max(0.5, total_questions / 40.0))
        
    Examples:
        5 soru → 0.5x (minimum)
        40 soru → 1.0x (baseline)
        80 soru → 2.0x (maximum)
    """
    if not exam_weight_data:
        return (1.0, 0)
    
    total_exam_questions = sum(w['question_count'] for w in exam_weight_data)
    
    # Normalize: 5-80 soru arası → 0.5x-2.0x çarpan
    exam_multiplier = min(2.0, max(0.5, total_exam_questions / 40.0))
    
    return (exam_multiplier, total_exam_questions)

def calculate_priority_score(
    progress_percentage: float,
    avg_success_rate: float,
    exam_multiplier: float
) -> float:
    """
    Final priority score hesapla
    
    Formula:
        base_priority = (100 - progress%) * 0.6 + (100 - success_rate%) * 0.4
        final_priority = base_priority * exam_multiplier
    
    Args:
        progress_percentage: İlerleme yüzdesi (0-100)
        avg_success_rate: Ortalama başarı (0-100)
        exam_multiplier: Sınav ağırlık çarpanı (0.5-2.0)
    
    Returns:
        float: Final priority score (yüksek = daha öncelikli)
    """
    # Inverse logic: Düşük progress = yüksek priority
    base_priority = (100 - progress_percentage) * 0.6 + (100 - avg_success_rate) * 0.4
    
    # Exam weight uygula
    final_priority = base_priority * exam_multiplier
    
    return round(final_priority, 1)