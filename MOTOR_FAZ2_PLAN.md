# ⚡ FAZ 2: PERFORMANS OPTİMİZASYONU

**Tarih:** 2026-01-09  
**Hedef:** %40-50 performans artışı  
**Risk:** ⭐ ÇOK DÜŞÜK (Read-only cache, query optimization)  
**Süre:** 1-2 gün

---

## 🎯 HEDEFLER

1. ✅ Tekrarlayan hesaplamaları elimine et
2. ✅ Request-level cache ekle
3. ✅ Query sayısını azalt
4. ✅ Datetime parsing optimize et

---

## 📋 ADIMLAR (KONTROLLÜ İLERLEME)

### ADIM 1: Shared Performance Module (YENİ DOSYA)
**Dosya:** `backend/app/api/v1/endpoints/student/performance.py`

**İçerik:**
- `get_student_performance()` - Tüm hesaplamaları tek seferde yap
- Cache decorator ile 30 saniye TTL
- Dashboard ve Tasks Today bu fonksiyonu çağırsın

**Risk:** ⭐ YOK (Yeni dosya, mevcut koda dokunmuyor)

---

### ADIM 2: Cache Implementation
**Kütüphane:** `functools.lru_cache` (Python built-in, ekstra paket gerektirmiyor)

**Strateji:**
```python
from functools import lru_cache
from datetime import datetime, timedelta

# TTL için manual cache invalidation
_cache_timestamp = {}

@lru_cache(maxsize=128)
def cached_get_performance(student_id: str, cache_key: str):
    """Cache'lenmiş performans hesaplaması"""
    # Hesaplamalar burada
    return performance_data

def get_performance_with_ttl(student_id: str, ttl_seconds: int = 30):
    """TTL ile cache wrapper"""
    now = datetime.now()
    cache_key = f"{student_id}_{now.timestamp() // ttl_seconds}"
    return cached_get_performance(student_id, cache_key)
```

**Risk:** ⭐ ÇOK DÜŞÜK (Built-in Python, production-tested)

---

### ADIM 3: Datetime Parsing Optimization
**Şu an:**
```python
for topic_id, data in topic_performance.items():
    test_date = datetime.fromisoformat(
        latest["test_date"].replace('Z', '+00:00')
    )  # ← HER LOOP'TA
```

**İyileşme:**
```python
# Loop dışında toplu parse
for test in tests:
    test["_parsed_date"] = datetime.fromisoformat(
        test["test_date"].replace('Z', '+00:00')
    )

# Loop içinde direkt kullan
for topic_id, data in topic_performance.items():
    test_date = latest["_parsed_date"]  # ← HAZIR
```

**Risk:** ⭐ YOK (Sadece timing değişimi)

---

### ADIM 4: Integration (MEVCUT ENDPOINT'LERE MİNİMAL DOKUNUŞ)

**dashboard.py değişimi:**
```python
# ŞU AN
all_tests = supabase.table("student_topic_tests").select(...)
topic_performance = {}
for test in all_tests.data:
    # ... hesaplamalar

# YENİ (tek satır değişiklik)
from .performance import get_student_performance

# Cache'li performans verisi
topic_performance = get_student_performance(student_id, use_cache=True)
```

**Risk:** ⭐ DÜŞÜK (Tek import, tek fonksiyon çağrısı)

---

## 🔒 DOKUNULMAYACAK ALANLAR

1. ❌ Motor formülleri (calculate_remembering_rate, calculate_next_review_date)
2. ❌ Utils.py içeriği
3. ❌ Endpoint response formatı
4. ❌ Database schema
5. ❌ app/core/ motorlar (henüz değil)

---

## ✅ GÜVENLİK KONTROL LİSTESİ

Her adımdan sonra:
- [ ] Backend restart
- [ ] GET /api/v1/student/dashboard → 200 OK
- [ ] GET /api/v1/student/tasks/today → 200 OK
- [ ] Response formatı değişmedi mi?
- [ ] Data accuracy korundu mu?

Herhangi biri FAIL olursa → Geri al, analiz et, tekrar dene

---

## 📊 BAŞARI KRİTERLERİ

### Before (Baseline):
```
Dashboard + Tasks Today (aynı user):
- DB Query: 2× (tekrar)
- Motor Hesaplama: 2× (tekrar)
- Response Time: ~143ms
```

### After (Target):
```
Dashboard + Tasks Today (aynı user):
- DB Query: 1× (cache hit)
- Motor Hesaplama: 1× (cache hit)
- Response Time: ~73ms (-49%)
```

### Ölçüm:
```bash
# Backend log'dan
time curl http://localhost:8000/api/v1/student/dashboard
time curl http://localhost:8000/api/v1/student/tasks/today
```

---

## 🎯 İLERLEME TAKİBİ

- [ ] ADIM 1: performance.py oluştur
- [ ] ADIM 2: Cache implement et
- [ ] ADIM 3: Datetime parsing optimize et
- [ ] ADIM 4: Dashboard'a entegre et
- [ ] ADIM 5: Tasks Today'e entegre et
- [ ] ADIM 6: Test et
- [ ] ADIM 7: Performans ölç (before/after)

---

**Hazırlayan:** AI Assistant  
**Tarih:** 2026-01-09  
**Durum:** 📋 PLAN HAZIR - Onay bekleniyor
