from datetime import date
from typing import List, Dict, Any, Optional
from collections import defaultdict

from .helpers import (
    to_utc_date,
    get_week_start_utc,
    get_month_start_utc,
    generate_week_periods,
    generate_month_periods
)

# ==================================================
# TÜRKÇE TARİH FORMATLAMA
# ==================================================

# TODO: PHASE-2-I18N - Replace with database-driven translations
# MIGRATION-GUIDE:
#   1. Create translations table with month names
#   2. Implement get_translation(key, language) function
#   3. Replace this dict with: await get_translation("month.jan.short", language)
#   4. Update all callers to pass language parameter
# ALLOWED: Temporary hardcoded solution for MVP
TURKISH_MONTHS = {
    1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
    7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"
}

# TODO: PHASE-2-I18N - Rename to format_date_localized and add language parameter
# MIGRATION-GUIDE:
#   Change signature to: async def format_date_localized(dt: date, language: str, format_type: str)
#   Use database lookups instead of TURKISH_MONTHS dict
def format_date_turkish(dt: date, format_type: str = "short") -> str:
    """
    Tarihi Türkçe formatla
    
    TEMPORARY: Hardcoded Turkish-only formatting for MVP
    FUTURE: Will become format_date_localized(dt, language, format_type)
    
    Args:
        dt: date objesi
        format_type: "short" -> "17 Kas" | "long" -> "Kas 2024"
    
    Returns:
        Türkçe formatlı tarih string
    """
    if format_type == "short":
        # Haftalık: "17 Kas"
        return f"{dt.day} {TURKISH_MONTHS[dt.month]}"
    else:
        # Aylık: "Kas 2024"
        return f"{TURKISH_MONTHS[dt.month]} {dt.year}"

# ==================================================
# MASTERY & PHASE CALCULATIONS
# ==================================================

def calculate_topic_mastery_level(topic_tests: list) -> str:
    """
    Bir konudaki testlere bakarak mastery seviyesi belirle
    
    Returns:
        - "mastered": 3+ test, ortalama >80
        - "in_progress": 1+ test, ortalama 40-80
        - "not_started": test yok veya ortalama <40
    """
    if not topic_tests:
        return "not_started"
    
    if len(topic_tests) < 3:
        return "in_progress"
    
    # Son 3 testin ortalaması
    recent_tests = sorted(topic_tests, key=lambda x: x.get('test_date', ''), reverse=True)[:3]
    avg = sum(t.get('success_rate', 0) for t in recent_tests) / len(recent_tests)
    
    if avg >= 80:
        return "mastered"
    elif avg >= 40:
        return "in_progress"
    else:
        return "not_started"


def calculate_phase_and_progress(tests: list, topics_total: int) -> tuple:
    """
    Ders bazlı phase ve progress hesapla
    
    Returns:
        (progress_percentage, avg_success_rate, trend, trend_icon, phase, disclaimer)
    """
    if not tests:
        # TODO: PHASE-2-I18N - These strings should come from translations
        return (0.0, 0.0, "unknown", "➖", "BAŞLANMAMIŞ", "Henüz test girilmemiş")
    
    test_count = len(tests)
    
    # Ortalama başarı
    avg_success_rate = sum(t.get('success_rate', 0) for t in tests) / test_count
    
    # Trend hesapla (son 5 vs önceki 5)
    if test_count >= 10:
        sorted_tests = sorted(tests, key=lambda x: x.get('test_date', ''))
        recent_avg = sum(t.get('success_rate', 0) for t in sorted_tests[-5:]) / 5
        older_avg = sum(t.get('success_rate', 0) for t in sorted_tests[-10:-5]) / 5
        
        if recent_avg > older_avg + 5:
            trend = "improving"
            trend_icon = "📈"
        elif recent_avg < older_avg - 5:
            trend = "declining"
            trend_icon = "📉"
        else:
            trend = "stable"
            trend_icon = "➡️"
    else:
        trend = "insufficient_data"
        trend_icon = "➖"
    
    # Progress percentage (unique topic coverage)
    unique_topics_tested = len(set(t.get('topic_id') for t in tests))
    progress_percentage = (unique_topics_tested / topics_total * 100) if topics_total > 0 else 0
    
    # TODO: PHASE-2-I18N - Phase names and disclaimers should be localized
    # Phase belirleme
    if test_count < 5:
        phase = "PHASE 1: Keşif"
        disclaimer = f"{test_count} test ile başlangıç aşaması"
    elif test_count < 15:
        phase = "PHASE 2: Gelişim"
        disclaimer = f"{test_count} test ile gelişim süreci"
    else:
        phase = "PHASE 3: Olgunluk"
        disclaimer = f"{test_count} test ile olgun aşama"
    
    return (
        round(progress_percentage, 1),
        round(avg_success_rate, 1),
        trend,
        trend_icon,
        phase,
        disclaimer
    )


def calculate_mastery_counts(tests: list, all_topic_ids: list) -> tuple:
    """
    Mastery durumlarını say
    
    Returns:
        (topics_mastered_universal, topics_mastered_personal, topics_in_progress, topics_not_started)
    """
    if not tests:
        return (0, 0, 0, len(all_topic_ids))
    
    # Konu bazında grupla
    from collections import defaultdict
    topic_tests = defaultdict(list)
    for test in tests:
        topic_tests[test['topic_id']].append(test)
    
    mastered_universal = 0
    mastered_personal = 0
    in_progress = 0
    
    for topic_id in all_topic_ids:
        t_tests = topic_tests.get(topic_id, [])
        level = calculate_topic_mastery_level(t_tests)
        
        if level == "mastered":
            mastered_universal += 1
            mastered_personal += 1
        elif level == "in_progress":
            in_progress += 1
    
    not_started = len(all_topic_ids) - mastered_universal - in_progress
    
    return (mastered_universal, mastered_personal, in_progress, not_started)

# ==================================================
# TREND CALCULATION HELPERS
# ==================================================

def get_success(test: dict) -> Optional[float]:
    """
    success_rate hem % hem 0-1 formatında olabilir.
    None dönebilir — o durumda None geçilir.
    """
    if test is None:
        return None

    v = test.get("success_rate")
    if v is None:
        return None

    # 0-1 scale → %
    if 0 <= v <= 1:
        return round(v * 100, 2)

    return round(float(v), 2)


def get_period_key(test: dict, period: str) -> date:
    """
    Test için period anahtarı üret (UTC-aware)
    """
    d = to_utc_date(test["test_date"])

    if period == "weekly":
        return get_week_start_utc(d)

    return get_month_start_utc(d)


def calculate_trends(
    tests: List[dict],
    period: str = "weekly",
    num_periods: int = 8,
    subjects: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Trend verisi hesapla (UTC-aware, Türkçe tarihler)
    
    Input:
      - tests: student_topic_tests satırları
      - period: weekly | monthly
      - num_periods: kaç period geriye gidilecek
      - subjects: {subject_id: subject_name}

    Output:
      {
         labels: [...],  # Türkçe tarihler
         period_starts: [...date...],
         overall_trend: [...],
         subjects: [
            {label: name, id: id, data:[...]},
            ...
         ]
      }
    """

    if not subjects:
        subjects = {}

    # --------------------------
    # 1) Period başlangıçlarını üret
    # --------------------------
    if period == "weekly":
        period_starts = generate_week_periods(num_periods)
        # TODO: PHASE-2-I18N - Replace with: labels = [await format_date_localized(p, language, "short") for p in period_starts]
        labels = [format_date_turkish(p, "short") for p in period_starts]
    else:
        period_starts = generate_month_periods(num_periods)
        # TODO: PHASE-2-I18N - Replace with: labels = [await format_date_localized(p, language, "long") for p in period_starts]
        labels = [format_date_turkish(p, "long") for p in period_starts]

    # --------------------------
    # 2) Testleri period'lara grupla
    # --------------------------
    period_tests = defaultdict(list)

    for t in tests:
        key = get_period_key(t, period)
        period_tests[key].append(t)

    # --------------------------
    # 3) OVERALL TREND
    # --------------------------
    overall_trend = []

    for p in period_starts:
        pts = period_tests.get(p, [])
        vals = [get_success(t) for t in pts if get_success(t) is not None]

        if vals:
            overall_trend.append(round(sum(vals) / len(vals), 1))
        else:
            overall_trend.append(None)

    # --------------------------
    # 4) SUBJECT BAZLI TREND
    # --------------------------
    per_subject = defaultdict(lambda: defaultdict(list))

    for p in period_starts:
        pts = period_tests.get(p, [])

        for t in pts:
            sid = t.get("subject_id")
            per_subject[sid][p].append(t)

    subject_datasets = []

    for sid, period_map in per_subject.items():
        data_points = []

        for p in period_starts:
            pts = period_map.get(p, [])
            vals = [get_success(t) for t in pts if get_success(t) is not None]

            if vals:
                data_points.append(round(sum(vals) / len(vals), 1))
            else:
                data_points.append(None)

        subject_datasets.append({
            "subject_id": sid,
            "label": subjects.get(sid, "Bilinmeyen Ders"),
            "data": data_points
        })

    return {
        "labels": labels,
        "period_starts": [p.isoformat() for p in period_starts],
        "overall_trend": overall_trend,
        "subjects": subject_datasets,
        "period": period,
        "count": len(tests)
    }
