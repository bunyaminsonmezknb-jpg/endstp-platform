# 🎓 End.STP - Akıllı Öğrenme Analiz Sistemi

## 📋 Proje Özeti

End.STP, öğrenci performansını analiz eden, kişiselleştirilmiş öğrenme yolları oluşturan ve unutma eğrisi tahminleri yapan modern bir eğitim teknolojisi platformudur.

### ✅ Tamamlanan: Öğrenci Dashboard (MVP v1.5)

**Son Güncellemeler (v1.5):**
- 🎴 **Flip Cards**: Bugünkü Durum kartları çevrilebilir (ön/arka yüz)
- 🔽 **Accordion**: Konulara tıkla, detaylar açılsın
- 🎯 **Partner Links**: Her konu için önerilen çalışma kaynakları
- 📅 **Next Review Date**: Spaced repetition bazlı tekrar tarihleri
- 🌍 **Gerçekçi Projeksiyon**: Son 30 günün performansına göre bitiş tahmini (Türkçe tarih)
- 🎨 **Renkli Progress Barlar**: Critical (kırmızı+blink), Frozen (mavi+pulse), Good (yeşil), Excellent (açık yeşil)

## 🏗️ Mimari
```
end-stp-project/
├── backend/              # FastAPI (PORT 8000) - ✅ ÇALIŞIYOR
└── frontend/             # Next.js 14 (PORT 3000) - ✅ ÇALIŞIYOR
```

## 🚀 Özellikler

### ✅ Öğrenci Dashboard v1.5

**Kritik Uyarı Sistemi:**
- Unutma eğrisi tahminleri ile acil müdahale gereken konular
- Kırmızı uyarı kutusu (yanıp sönen animasyon)

**Bilgi Sağlığı Barları:**
- Health bar mantığı ile konu başarı takibi
- Accordion ile detay görüntüleme:
  - 📜 Son Çalışma
  - 📊 Son Başarı (net + yüzde)
  - �� Toplam Test Sayısı
  - 📅 Sonraki Tekrar Tarihi
- Partner link kartları (Kurtarma Reçetesi)

**Gamification:**
- 7 günlük streak sistemi
- Achievement badge'ler (gelişim göstergesi)
- Progress tracking

**Flip Cards:**
- 3 çevrilebilir kart (Günlük Hedef, Haftalık Başarı, Çalışma Süresi)
- Arka yüzde detaylı bilgiler
- Smooth 3D rotation animasyonu

**Smart Curator:**
- Partner linkleri ile içerik yönlendirme sistemi
- Önerilen Çalışma (Video, Test, Pratik)

**Gerçekçi Projeksiyon:**
- Son 30 günün velocity'sine göre hesaplama
- Velocity: Tamamlanan konu / 30 gün
- Estimated Date: Türkçe format (8 Aralık)
- Warning Level: danger/warning/success
- Required Velocity: Sınava yetişmek için gereken hız

**Responsive Design:**
- Mobil, tablet ve desktop uyumlu
- Tailwind CSS utility-first yaklaşım

## 💻 Teknoloji Stack

### Backend ✅
- **FastAPI** (Python 3.10.12)
- **Supabase/PostgreSQL** (38 tablo)
- **Pydantic** (Data validation)
- **JWT Authentication**

### Frontend ✅
- **Next.js 14** (App Router)
- **TypeScript** (Strict mode)
- **Tailwind CSS**
- **Zustand** (State Management)
- **React 18**

## 🎯 Kurulum ve Çalıştırma

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend: `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:3000`

### Production Build
```bash
# Backend
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Frontend
npm run build
npm start
```

## 📁 Proje Yapısı
```
frontend/
├── app/
│   ├── student/
│   │   └── dashboard/
│   │       ├── page.tsx                 # Ana dashboard sayfası
│   │       └── components/
│   │           ├── CriticalAlert.tsx    # Kırmızı uyarı kutusu
│   │           ├── HeroStats.tsx        # 3 Flip Card
│   │           ├── ActionCards.tsx      # Hızlı aksiyon kartları
│   │           ├── TopicHealthBar.tsx   # Accordion + Partner Links
│   │           ├── RecoveryModal.tsx    # Partner link modal (deprecated)
│   │           └── DashboardHeader.tsx  # Üst başlık
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── lib/
│   └── store/
│       └── studentDashboardStore.ts     # Zustand state management
└── public/

backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── student.py           # Dashboard endpoint (v3.1)
│   ├── db/
│   │   └── session.py                   # Supabase client
│   └── main.py                          # FastAPI app
└── requirements.txt
```

## 🎨 Design System

### Renk Paleti
- **Primary**: `#667eea` (End Purple)
- **Primary Dark**: `#764ba2` (End Purple Dark)
- **Critical**: `#e74c3c` (Kırmızı) - Blink animasyon
- **Warning**: `#f39c12` (Turuncu)
- **Good**: `#27ae60` (Yeşil)
- **Excellent**: `#10b981` (Açık Yeşil)
- **Frozen**: `#60a5fa` (Mavi) - Pulse animasyon

### Animasyonlar
- `animate-pulse-slow`: Frozen barlar (3s)
- `animate-blink`: Critical barlar (1.5s)
- `animate-fade-in`: Accordion açılma (0.3s)
- `animate-bounce-slow`: Projeksiyon ikonu (2s)

## 📊 State Management (Zustand)
```typescript
// Store kullanımı
const { dashboardData, isLoading, error, fetchDashboardData } = useStudentDashboard();

// Data fetch
useEffect(() => {
  const user = JSON.parse(localStorage.getItem('user'));
  fetchDashboardData(user.id);
}, []);

// Projection data
const projection = dashboardData.projection;
// {
//   status: "in_progress",
//   velocity: "0.2 konu/gün",
//   estimatedDate: "8 Aralık",
//   warningLevel: "success",
//   message: "Harika! Bu hızla 45 gün önceden bitecek."
// }
```

## 🔮 Algoritma Detayları

### Unutma Eğrisi (Forgetting Curve)
```python
def calculate_remembering_rate(tests_data):
    latest_test = tests_data[0]
    days_passed = (now - test_date).days
    
    success_rate = latest_test["success_rate"]
    forgetting_factor = max(0, 100 - (days_passed * 5))
    remembering_rate = int((success_rate * forgetting_factor) / 100)
    
    return max(0, min(100, remembering_rate))
```

### Gerçekçi Projeksiyon
```python
def calculate_realistic_projection(all_tests, topic_performance):
    # 1. Son 30 günde tamamlanan konu sayısı
    recent_completions = get_completed_last_30_days()
    
    # 2. Velocity (Hız)
    velocity = recent_completions / 30  # konu/gün
    
    # 3. Kalan konular
    remaining = total_topics - completed_topics
    
    # 4. Tahmini gün
    days_needed = remaining / velocity
    
    # 5. Bitiş tarihi
    estimated_date = now + timedelta(days=days_needed)
    
    # 6. Sınav tarihine göre warning level
    if estimated_date > exam_date:
        warning_level = "danger"
    elif days_difference < 30:
        warning_level = "warning"
    else:
        warning_level = "success"
```

### Spaced Repetition
```python
def calculate_next_review_date(remembering_rate):
    if remembering_rate >= 85:
        return 14  # 2 hafta sonra
    elif remembering_rate >= 70:
        return 7   # 1 hafta sonra
    elif remembering_rate >= 50:
        return 3   # 3 gün sonra
    elif remembering_rate >= 30:
        return 1   # 1 gün sonra
    else:
        return 0   # HEMEN
```

## 🔮 Gelecek Planlar

### Backend API
- [ ] Chart.js / Recharts entegrasyonu (Trend grafikleri)
- [ ] WebSocket notifications
- [ ] Drag & drop report builder
- [ ] Export to PDF

### Dashboard'lar
- [x] Öğrenci Dashboard ✅
- [ ] Admin Dashboard
- [ ] Öğretmen/Koç Dashboard

### Özellikler
- [ ] Real-time data binding
- [ ] Gerçek partner API entegrasyonları
- [ ] Sınav tarihi configuration (DB'den)
- [ ] Konu prerequisite grafiği

## 🎯 MVP Timeline

- **Week 1**: ✅ Öğrenci Dashboard v1.0
- **Week 2**: ✅ Accordion + Flip Cards + Projection (v1.5)
- **Week 3**: Admin Dashboard + Backend optimization
- **Week 4**: Testing + Deployment

## 📝 Notlar

### UX Prensipleri
1. **5 Saniyede Anlaşılır**: Öğrenci dashboard'a girdiğinde ne yapması gerektiğini anında görür
2. **Health Bar Mantığı**: Dolu bar = İyi, Boş bar = Kötü
3. **Aksiyon Odaklı**: Her element bir harekete yönlendirir
4. **Gamification**: Streak, badge'ler, progress tracking
5. **Psikolojik Baskı**: Gerçekçi projeksiyon ile motivasyon/uyarı

### API Satış Modeli
- Backend API standalone olarak kurulacak
- OpenAPI/Swagger otomatik dökümantasyon (`/docs`)
- API Key authentication
- Rate limiting
- Versioned endpoints (`/api/v1/`)

## 🤝 Katkıda Bulunma

Bu proje aktif geliştirme aşamasındadır. Öneriler ve geri bildirimler için iletişime geçin.

## 📄 Lisans

Proprietary - End.STP © 2024

---

**Geliştirici Notları:**
- Canlı veri (Gerçek backend API bağlantısı) ✅
- Tailwind CSS direkt kullanılmış (@apply yok)
- TypeScript strict mode aktif
- Next.js 14 App Router kullanılıyor
- Production-ready build ✅
- FastAPI + Supabase entegrasyonu ✅
