# 🏷️ ALTIN ETIKETLER
End.STP Proje Yönetimi - Ertelenmiş Konular

> Son Güncelleme: 2026-01-09  
> Toplam Etiket: 5

---

## 📊 DURUM ÖZET

- 🟢 DOKUNMA: 3
- 🟡 BEKLET: 1
- 🔴 BLOKER: 1

---

## 🟢 DOKUNMA

_(Bilinçli mimari kararlar, çalışıyor, değiştirilmemeli)_

---

## 🟡 BEKLET

_(Bilinçli ertelenen konular, zamanı gelince kaldığı yerden devam)_

---

## 🔴 BLOKER

_(İlerlemeyi durduran konular, öncelikli ama şu an kilitli)_

---

## 📜 TARIHÇE

- 2026-01-09: Altın Etiketleme Sistemi kuruldu

## 🟢 DOKUNMA - AUTH & SESSION ZİNCİRİ

- **Alan:** Auth / Backend / Frontend
- **Durum:** %100 (Çalışıyor)
- **Neden durdu:** Durmadı, bilinçli koruma altında
- **Şu ana kadar yapılanlar:**
  - ✓ Supabase auth helpers entegrasyonu (createBrowserClient, createMiddlewareClient)
  - ✓ Backend JWT validation (HS256)
  - ✓ Token flow (Frontend → Middleware → Backend)
  - ✓ Session management
- **Açık kalan sorular:**
  1. RS256 migration gerekli mi? (Şu an hayır, HS256 çalışıyor)
  2. Token rotation strategy? (Supabase managed)
  3. Rate limiting per user? (Faz 5)
- **Risk:** Güvenlik
- **Geçici karar:**
  - Auth zinciri %100 çalışıyor, HS256 production-ready
  - Dokunmak = regression riski
- **Planlanan Faz:** FAZ-5 (Security hardening)
- **Devam ederken ilk bakılacak yer:**
  - `backend/app/core/auth.py`
  - `frontend/middleware.ts`
  - `frontend/lib/supabase/client.ts`

---

## 🟢 DOKUNMA - MOTOR CORE LOGIC

- **Alan:** Backend / Motors
- **Durum:** %100 (Çalışıyor)
- **Neden durdu:** Durmadı, bilinçli koruma altında
- **Şu ana kadar yapılanlar:**
  - ✓ BS-Model remembering rate calculation
  - ✓ Priority engine
  - ✓ Difficulty engine
  - ✓ Time analyzer
  - ✓ Fallback mechanisms
- **Açık kalan sorular:**
  1. Formül parameters optimal mi? (A/B test Faz 6)
  2. Accuracy metrics? (Faz 3'te ölçülecek)
  3. Config-driven parameters? (Faz 5)
- **Risk:** Pedagojik doğruluk
- **Geçici karar:**
  - Motor formülleri çalışıyor, davranış değişimi = büyük risk
  - Sadece performans katmanına dokun (query, cache)
  - Algoritma/formül değişimi Faz 3'e ertelendi
- **Planlanan Faz:** FAZ-3 (Accuracy fine-tuning)
- **Devam ederken ilk bakılacak yer:**
  - `backend/app/api/v1/endpoints/student/utils.py`
  - `calculate_remembering_rate()`
  - `calculate_next_review_date()`

---

## 🟢 DOKUNMA - ÇALIŞAN ENDPOINT İÇERİKLERİ

- **Alan:** Backend / API
- **Durum:** %100 (200 OK dönüyor)
- **Neden durdu:** Durmadı, bilinçli koruma altında
- **Şu ana kadar yapılanlar:**
  - ✓ `/student/dashboard` endpoint
  - ✓ `/student/tasks/today` endpoint
  - ✓ `/student/weekly-subjects` endpoint
  - ✓ Motor calculations integration
- **Açık kalan sorular:**
  1. N+1 query var mı? (Faz 1'de tespit edilecek)
  2. Tekrarlayan hesaplamalar? (Faz 1'de tespit edilecek)
  3. Cache stratejisi? (Faz 2'de eklenecek)
- **Risk:** Regression
- **Geçici karar:**
  - Endpoint'lerin içini "temizleme" yapmıyoruz
  - Yeni ihtiyaç = yeni endpoint veya wrapper
  - Performans iyileştirmesi = query/cache katmanında
- **Planlanan Faz:** FAZ-2 (Performans iyileştirme)
- **Devam ederken ilk bakılacak yer:**
  - `backend/app/api/v1/endpoints/student/dashboard.py`
  - `backend/app/api/v1/endpoints/student/tasks_today.py`

---

## 🔴 BLOKER - RLS POLICY TEMİZLİĞİ

- **Alan:** Database / Security
- **Durum:** %0 (Başlanmadı)
- **Neden durdu:** Yüksek risk, düşük öncelik
- **Şu ana kadar yapılanlar:**
  - ✓ Basic RLS policies çalışıyor
  - ✓ student_topic_tests erişimi çalışıyor
- **Açık kalan sorular:**
  1. Policy order sorunlu mu?
  2. Duplicate policy'ler var mı?
  3. Casting issues?
- **Risk:** Güvenlik
- **Geçici karar:**
  - Şu an çalışıyor, dokunma
  - Policy order/duplicate sessizce patlar
  - Faz 4'te kontrollü şekilde temizlenecek
- **Planlanan Faz:** FAZ-4 (Database optimization)
- **Devam ederken ilk bakılacak yer:**
  - Supabase Dashboard → Database → Policies
  - `student_topic_tests` table policies

---

## 🟡 BEKLET - PERFORMANS MİKRO-OPTİMİZASYONU

- **Alan:** Frontend / Performance
- **Durum:** %0 (Başlanmadı)
- **Neden durdu:** Erken optimizasyon, ölçüm yok
- **Şu ana kadar yapılanlar:**
  - ✓ Basic React patterns kullanılıyor
  - ✓ API client working
- **Açık kalan sorular:**
  1. useEffect optimization gerekli mi?
  2. Memoization nerede eklenecek?
  3. Bundle size sorunlu mu?
- **Risk:** Teknik borç (düşük)
- **Geçici karar:**
  - Şu an ölçüm yok, hissedilir yavaşlık yok
  - Profiling Faz 5'te yapılacak
  - Erken optimizasyon = karmaşıklık riski
- **Planlanan Faz:** FAZ-5 (Frontend optimization)
- **Devam ederken ilk bakılacak yer:**
  - Chrome DevTools → Performance tab
  - React DevTools → Profiler


## 🟡 [ENV-001] Dependency Drift - Supabase SDK

**Alan:** Backend / Environment  
**Faz:** FAZ 4  
**Durum:** ÇÖZÜLDÜ (geçici)  
**Tarih:** 2026-01-10

**Sorun:**
- Motor optimizasyonu sırasında supabase uninstall/install
- requirements.txt → supabase==2.3.0
- runtime → supabase==2.27.1 kuruldu
- Versiyon uyumsuzluğu (websockets.asyncio)

**Karar:**
- requirements.txt'e sadık kalındı (2.3.0)
- venv ile clean environment kuruldu
- Supabase SDK upgrade FAZ 4'e ertelendi

**Neden Ertelendi:**
- SDK upgrade = FAZ kararı (debug sırasında değil)
- Çalışan sistem var, risk almaya gerek yok
- Motor optimizasyonu supabase versiyonundan bağımsız

**FAZ 4'te Yapılacaklar:**
- [ ] Supabase SDK upgrade (2.3.0 → latest)
- [ ] Dependency pinning review
- [ ] Changelog kontrol (breaking changes)
- [ ] Test suite ile doğrulama

**İlk Bakılacak Yer:**
- backend/requirements.txt


## ✅ [ENV-001] Dependency Drift - Supabase SDK (ÇÖZÜLDÜ)

**Alan:** Backend / Environment  
**Faz:** FAZ 2 (çözüldü), FAZ 4 (cleanup)  
**Durum:** ✅ ÇÖZÜLDÜ  
**Tarih:** 2026-01-10

**Sorun:**
- Motor optimizasyonu sırasında supabase uninstall/install
- Eski requirements.txt → supabase==2.3.0
- Kurulum → supabase==2.27.1 denendi
- Versiyon uyumsuzlukları (websockets.asyncio, proxy hatası)
- "proxy" parametresi eski supabase'de gotrue paketi içinde kullanılıyor
- Yeni httpx ile uyumsuz

**Karar:**
- ✅ Yeni supabase 2.27.1'e upgrade edildi
- ✅ Tüm bağımlılıklar uyumlu versiyonlarda kuruldu
- ✅ requirements.txt güncellendi
- ✅ venv ile clean environment sağlandı
- ✅ Proxy hatası çözüldü

**Yapılanlar:**
1. Sistem paketleri temizlendi (sudo pip uninstall)
2. User paketleri temizlendi
3. venv aktif edildi
4. supabase==2.27.1 kuruldu (tüm bağımlılıklarla)
5. Backend başarıyla başlatıldı
6. /api/v1/subjects endpoint test edildi ✅
7. requirements.txt modernize edildi

**Sonuç:**
- Backend çalışıyor ✅
- Proxy hatası yok ✅
- Test Entry dersler yükleniyor ✅
- Modern dependency stack ✅

**Öğrenilenler:**
- requirements.txt = sözleşme, her zaman güncel tutulmalı
- venv kullanımı zorunlu (sudo pip değil!)
- Dependency upgrade FAZ kararı (debug sırasında değil)
- Ama bazen yeni versiyona geçmek daha doğru çözüm

**FAZ 4'te Yapılacaklar:**
- [ ] CI/CD pipeline kur (requirements.txt otomatik test)
- [ ] Dependency pinning stratejisi belirle
- [ ] Pre-commit hooks ekle (requirements.txt kontrolü)
- [ ] Virtual environment standardını dokümante et

**İlk Bakılacak Yer:**
- backend/requirements.txt
- backend/venv/ (artık aktif kullanılıyor)

**Kaynaklar:**
- Supabase Python SDK Changelog: https://github.com/supabase-community/supabase-py/releases
- Motor optimizasyonu transcript: /mnt/transcripts/2026-01-10-*-motor-optimization.txt


## 🟡 [FE-AUTH-003] test-entry Legacy localStorage Auth (ÇÖZÜLDÜ)

**Alan:** Frontend / Auth  
**Faz:** FAZ 2 (çözüldü)  
**Durum:** ✅ ÇÖZÜLDÜ  
**Tarih:** 2026-01-10

**Sorun:**
- Supabase cookie-based auth aktif ✅
- test-entry hâlâ localStorage.getItem('user') arıyor ❌
- Middleware session var, backend token validate ediyor ✅
- Ama page.tsx "Lütfen giriş yapın" diyor ❌

**Sebep:**
- Eski auth mimarisinden kalan kod
- localStorage-based auth eski sistemde kullanılıyordu
- Yeni Supabase cookie-based auth'a geçildi
- test-entry güncellenmemiş

**Çözüm:**
```typescript
// ❌ ESKİ (localStorage)
const userStr = localStorage.getItem('user');
const accessToken = localStorage.getItem('access_token');
if (!userStr || !accessToken) throw new Error('Lütfen giriş yapın');

// ✅ YENİ (Supabase session)
const supabase = createBrowserClient(...);
const { data: { user } } = await supabase.auth.getUser();
const { data: { session } } = await supabase.auth.getSession();
const accessToken = session?.access_token;
```

**Yapılanlar:**
1. localStorage auth kontrolü kaldırıldı
2. supabase.auth.getUser() kullanıldı
3. supabase.auth.getSession() ile token alındı
4. Backup alındı (page.tsx.backup_auth)

**Sonuç:**
- "Lütfen giriş yapın" hatası çözüldü ✅
- Cookie-based auth kullanılıyor ✅
- Middleware ile uyumlu ✅

**Öğrenilenler:**
- localStorage auth KULLANMA (sadece theme/preference için)
- Tek auth kapısı: Supabase session
- Middleware'e güven, page'de auth kontrolü yapma
- Cookie-based auth > localStorage

**İlk Bakılacak Yer:**
- frontend/app/student/test-entry/page.tsx

**İlgili Etiketler:**
- ENV-001 (Backend dependency çözüldü)
- FE-AUTH-003 (Frontend auth çözüldü)


## 🎉 [MOTOR-FAZ2] Performance Optimization (TAMAMLANDI)

**Alan:** Backend / Performance  
**Faz:** FAZ 2  
**Durum:** ✅ TAMAMLANDI  
**Tarih:** 2026-01-10

**Hedef:**
- Motor hesaplamalarını optimize et
- Cache sistemi kur
- Dashboard performansını artır

**Yapılanlar:**
1. performance.py modülü (261 satır)
2. LRU cache (128 entry, 30s TTL)
3. Dashboard entegrasyonu
4. Performance test
5. Dokümantasyon

**Sonuçlar:**
- Speedup: ~2-3x (cache HIT)
- DB query azaldı
- Unified calculation system

**Dosyalar:**
- `backend/app/api/v1/endpoints/student/performance.py`
- `backend/app/api/v1/endpoints/student/dashboard.py`
- `MOTOR_FAZ2_TAMAMLANDI.md`

**Sonraki Faz:**
- FAZ 3: Frontend Optimization
- FAZ 4: Motor V2 Integration

