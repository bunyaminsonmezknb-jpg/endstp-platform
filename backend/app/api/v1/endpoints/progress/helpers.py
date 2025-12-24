from datetime import datetime, timedelta, timezone, date
from dateutil import parser
from typing import List

# ==================================================
# 1️⃣ ISO Datetime → UTC Date Normalizasyonu
# ==================================================
def to_utc_date(value) -> date:
    """
    Verilen datetime string / datetime objesini
    UTC'ye normalize edip saf date döndürür.
    Destekler:
    - "2025-12-24T18:22:11.000000+03:00"
    - "2025-12-24"
    - datetime objesi
    """
    if value is None:
        raise ValueError("Date value cannot be None")
    
    # already date
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    
    # if datetime
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.astimezone(timezone.utc)
        return value.date()
    
    # string case
    if isinstance(value, str):
        dt = parser.isoparse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.date()
    
    raise TypeError(f"Unsupported date type: {type(value)}")

# ==================================================
# 2️⃣ Haftanın Pazartesi Gününü Bul
# ==================================================
def get_week_start_utc(value) -> date:
    """
    Verilen tarih hangi ülkede olursa olsun,
    haftanın UTC Pazartesi başlangıcını döner.
    """
    d = to_utc_date(value)
    monday = d - timedelta(days=d.weekday())  # 0 = Monday
    return monday

# ==================================================
# 3️⃣ Ayın 1. Gününü Bul
# ==================================================
def get_month_start_utc(value) -> date:
    d = to_utc_date(value)
    return date(d.year, d.month, 1)

# ==================================================
# 4️⃣ Haftalık Period Başlangıçlarını Üret
# ==================================================
def generate_week_periods(num_periods: int) -> List[date]:
    """
    Son N hafta için UTC bazlı Pazartesi listesi döner.
    Bu hafta dahil.
    """
    today = to_utc_date(datetime.utcnow())
    current_monday = get_week_start_utc(today)
    
    return [
        current_monday - timedelta(weeks=i)
        for i in reversed(range(num_periods))
    ]

# ==================================================
# 5️⃣ Aylık Period Başlangıçlarını Üret
# ==================================================
def generate_month_periods(num_periods: int) -> List[date]:
    today = to_utc_date(datetime.utcnow())
    first = get_month_start_utc(today)
    
    months = []
    for i in reversed(range(num_periods)):
        year = first.year
        month = first.month - i
        
        while month <= 0:
            month += 12
            year -= 1
        
        months.append(date(year, month, 1))
    
    return months