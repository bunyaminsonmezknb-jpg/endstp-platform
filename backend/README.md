# 🎓 End.STP - Akıllı Öğrenme Analiz Sistemi

## 📋 Proje Özeti

End.STP, Türkiye'deki üniversite sınav hazırlığı (OSYM) için yapay zeka destekli öğrenme analitikleri platformudur. Unutma eğrisi tahminleri, kişiselleştirilmiş öğrenme yolları ve 4-motor analiz sistemi ile öğrenci performansını optimize eder.

### 🎯 Mevcut Durum (Aralık 2025)

**✅ TAMAMLANDI**:
- ✅ Backend API (FastAPI + 4-Motor Sistemi)
- ✅ Database (Supabase - 38 tablo)
- ✅ Authentication (Supabase Auth)
- ✅ Test Management System (Ekle/Düzenle/Sil)
- ✅ Student Dashboard v1 (Analytics + Visualizations)
- ✅ API Endpoints (Today's Tasks, Priority Engine, etc.)

**🚧 DEVAM EDİYOR**:
- 🚧 Bugünkü Durum Kartları (3 kart - frontend entegrasyonu)

**📅 PLANLANAN**:
- [ ] Admin Dashboard
- [ ] Öğretmen/Koç Dashboard  
- [ ] API Commercialization
- [ ] Mobile App

## 🏗️ Mimari

```
endstp-platform/
├── backend/              # FastAPI (PORT 8000) - ✅ ÇALIŞIYOR
│   ├── app/
│   │   ├── api/v1/      # API endpoints
│   │   ├── models/      # Pydantic schemas
│   │   ├── services/    # Business logic (4-motor sistemi)
│   │   ├── core/        # Config, auth, database
│   │   └── utils/       # Helpers
│   └── main.py
│
└── frontend/             # Next.js 14 (PORT 3000) - ✅ ÇALIŞIYOR
    ├── app/
    │   ├── student/     # Student dashboard
    │   ├── tests/       # Test management
    │   └── auth/        # Login/Register
    ├── lib/
    │   ├── api/         # API client (TypeScript)
    │   └── store/       # Zustand state management
    └── components/      # Reusable UI components
```

## 🚀 Özellikler

### ✅ Backend (4-Motor Analiz Sistemi)

#### 1️⃣ **BS-Model (Akıllı Tekrar Planlayıcı)**
- Unutma eğrisi tahminleri (S-effective parametreleri)
- Kişiselleştirilmiş tekrar tarihleri
- Retention rate tracking

#### 2️⃣ **Difficulty Engine (Zorluk Motoru)**
- Learning difficulty calculation:
  - Blank rate (0.55)
  - Wrong rate (0.30)
  - Volatility factor (0.10)
  - Misconception factor (0.05)

#### 3️⃣ **Time Analyzer (Zaman Analizi)**
- Soru başına ortalama süre
- Tempo analizi (hızlı/yavaş)
- Efficiency scoring

#### 4️⃣ **Priority Engine (Önceliklendirme)**
- Prerequisite relationships (α ve β parametreleri)
- Weighted scoring
- Dynamic priority updates

### ✅ Frontend

#### **Student Dashboard**
- **Hero Stats**: Total tests, topics studied, current streak
- **Critical Alerts**: Forgetting curve warnings (48-hour window)
- **Topic Health Bars**: Visual health indicators
- **Test Management**: Add, edit, delete test results
- **Gamification**: Streak system, achievement badges
- **Responsive Design**: Mobile, tablet, desktop optimized

#### **Test Management System**
- Her konu testi bağımsız kayıt (session grouping yok)
- Attempt date tracking (unutma eğrisi için kritik)
- Edit history preservation
- Bulk import (Excel/CSV) - Planned

## 💻 Teknoloji Stack

### Backend
- **FastAPI** (Python 3.10.12)
- **Supabase/PostgreSQL** (38 tables)
- **Pydantic v2** (Data validation)
- **SQLAlchemy** (ORM)
- **JWT Authentication** (Supabase Auth)
- **Uvicorn** (ASGI server)

### Frontend
- **Next.js 14** (App Router + Server Components)
- **TypeScript** (Strict mode)
- **Tailwind CSS** (Utility-first)
- **Zustand** (State Management)
- **React 18** (Concurrent features)
- **Axios** (API client with retry logic)

### Database
- **Supabase** (PostgreSQL)
- **38 Tables**: Users, Tests, Topics, Analytics, Subscriptions, etc.
- **Row Level Security** (RLS enabled)
- **Real-time subscriptions** (planned)

## 🎯 Kurulum ve Çalıştırma

### Gereksinimler
- **Node.js**: v20.19.5+
- **Python**: 3.10.12+
- **Supabase**: Account + Project setup
- **WSL2** (Windows için önerilen)

### Backend Setup

```bash
cd backend

# Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment variables (.env)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_service_key
JWT_SECRET=your_jwt_secret

# Run server
uvicorn app.main:app --reload --port 8000
```

Backend API: `http://localhost:8000`  
Swagger Docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Dependencies
npm install

# Environment variables (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Development
npm run dev

# Production build
npm run build
npm start
```

Frontend: `http://localhost:3000`

### Demo Login
```
Email: demo@end-stp.com
Password: demo123
```

## 📁 Proje Yapısı

### Backend Structure
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── student.py          # Student endpoints
│   │           ├── tests.py            # Test management
│   │           ├── analytics.py        # Analytics endpoints
│   │           └── auth.py             # Authentication
│   ├── models/
│   │   └── schemas.py                  # Pydantic models
│   ├── services/
│   │   ├── bs_model.py                 # Spaced repetition
│   │   ├── difficulty_engine.py        # Difficulty calculation
│   │   ├── time_analyzer.py            # Time analysis
│   │   └── priority_engine.py          # Topic prioritization
│   ├── core/
│   │   ├── config.py                   # Settings
│   │   ├── security.py                 # JWT, auth
│   │   └── database.py                 # Supabase client
│   └── utils/
│       └── helpers.py                  # Helper functions
├── main.py                             # FastAPI app
└── requirements.txt

### Frontend Structure
```
frontend/
├── app/
│   ├── student/
│   │   └── dashboard/
│   │       ├── page.tsx                # Main dashboard
│   │       └── components/
│   │           ├── CriticalAlert.tsx
│   │           ├── HeroStats.tsx
│   │           ├── TopicHealthBar.tsx
│   │           ├── TodayStatusCards.tsx  # 🚧 IN PROGRESS
│   │           └── ...
│   ├── tests/
│   │   ├── page.tsx                    # Test list
│   │   ├── add/
│   │   └── [id]/edit/                  # Edit test
│   ├── auth/
│   │   ├── login/
│   │   └── register/
│   └── globals.css
├── lib/
│   ├── api/
│   │   ├── client.ts                   # Axios instance
│   │   ├── studentApi.ts               # Student API calls
│   │   └── testsApi.ts                 # Test API calls
│   ├── store/
│   │   └── studentDashboardStore.ts    # Zustand state
│   └── types/
│       └── index.ts                    # TypeScript types
├── components/
│   ├── ui/                             # Reusable components
│   └── layout/                         # Layout components
└── package.json
```

## 🎨 Design System

### Renk Paleti
- **Primary**: `#667eea` (End Purple)
- **Primary Dark**: `#764ba2` (End Purple Dark)
- **Critical**: `#e74c3c` (Kırmızı - Kritik uyarılar)
- **Warning**: `#f39c12` (Turuncu - Dikkat gerektiren)
- **Success**: `#27ae60` (Yeşil - Başarılı durum)
- **Info**: `#3498db` (Mavi - Bilgilendirme)
- **Frozen**: `#E3F2FD` (Buz Mavisi - Donmuş konular)

### Health Bar Color Logic
```typescript
// Health bar renk sistemi
≥ 80%: Yeşil (Success)     // Sağlıklı
60-79%: Sarı (Warning)      // Orta risk
40-59%: Turuncu (Warning)   // Yüksek risk
< 40%: Kırmızı (Critical)   // Kritik durum
```

### Animasyonlar
- `animate-pulse-slow`: Kritik uyarı kutusu (3s cycle)
- `animate-shake`: Uyarı ikonu sallama
- `animate-blink`: Kritik durum barları yanıp sönme
- `animate-shine`: Shine efekti (başarı durumları)

### Typography
- **Font**: Inter (Google Fonts)
- **Headings**: font-bold, tracking-tight
- **Body**: font-normal, leading-relaxed
- **Numbers**: tabular-nums (mono-spaced)

## 📊 State Management

### Zustand Store Pattern
```typescript
// Store tanımı
interface StudentDashboardState {
  dashboardData: DashboardData | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setDashboardData: (data: DashboardData) => void;
  updateTopicStatus: (topicId: string, rate: number) => void;
  fetchDashboard: () => Promise<void>;
}

// Hook kullanımı
const { dashboardData, isLoading, fetchDashboard } = useStudentDashboard();

// Auto-fetch on mount
useEffect(() => {
  fetchDashboard();
}, []);
```

### API Client (Axios)
```typescript
// Error handling with retry logic
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Automatic retry (3 attempts)
apiClient.interceptors.response.use(
  response => response,
  error => retryRequest(error, 3)
);
```

## 🔌 API Endpoints

### Authentication
```
POST   /api/v1/auth/register          # Kullanıcı kaydı
POST   /api/v1/auth/login             # Giriş
POST   /api/v1/auth/refresh           # Token yenileme
POST   /api/v1/auth/logout            # Çıkış
```

### Student
```
GET    /api/v1/student/dashboard      # Dashboard data
GET    /api/v1/student/todays-tasks   # Bugünkü görevler ✅
GET    /api/v1/student/topics         # Tüm konular
GET    /api/v1/student/topic/{id}     # Konu detayı
```

### Tests
```
GET    /api/v1/tests                  # Test listesi
POST   /api/v1/tests                  # Test ekleme
GET    /api/v1/tests/{id}             # Test detayı
PUT    /api/v1/tests/{id}             # Test güncelleme
DELETE /api/v1/tests/{id}             # Test silme
```

### Analytics (4-Motor)
```
POST   /api/v1/analytics/bs-model     # Unutma eğrisi tahmini
POST   /api/v1/analytics/difficulty   # Zorluk hesaplama
POST   /api/v1/analytics/time         # Zaman analizi
POST   /api/v1/analytics/priority     # Önceliklendirme
```

### Swagger Documentation
Tüm endpoints için interaktif API dökümantasyonu:  
`http://localhost:8000/docs`

## 💾 Database Schema (Supabase)

### Core Tables (38 total)
```sql
-- Users & Auth
users                    # Kullanıcı bilgileri
user_profiles           # Profil detayları
user_settings           # Kullanıcı ayarları

-- Tests & Results
tests                   # Test kayıtları
test_results            # Test sonuçları
topic_attempts          # Her konu testi bağımsız kayıt ⚠️

-- Topics & Content
topics                  # Konu listesi (OSYM/MEB uyumlu)
topic_relationships     # Prerequisite ilişkileri
subject_areas          # Alan/ders grupları

-- Analytics
learning_analytics      # Öğrenme istatistikleri
forgetting_curves       # Unutma eğrisi parametreleri
difficulty_scores       # Zorluk skorları
time_analytics         # Zaman analizleri

-- Subscriptions
subscription_plans      # Paket planları (Basic/Medium/Premium)
user_subscriptions     # Kullanıcı abonelikleri
feature_access         # Özellik erişim kontrolü

-- Goals & Progress
student_goals          # 5-tier university goal system
progress_tracking      # İlerleme takibi
achievements           # Badge'ler, başarılar

-- System
audit_logs            # System logs
error_tracking        # Hata takibi
```

### Key Design Decisions
1. **Her konu testi bağımsız kayıt** (topic_attempts)
   - Session grouping YOK
   - attempt_date kritik (unutma eğrisi için)
   - 24 saat içinde girilmeli

2. **Foreign Key Cleanup** (12 tablo)
   - FK'lar kaldırıldı (performans için)
   - Uygulama katmanında kontrol

3. **Row Level Security (RLS)**
   - Tüm tablolarda aktif
   - User-based isolation

## 🔮 Gelecek Planlar

### Kısa Vadeli (1-2 Ay)
- [x] Backend API ✅
- [x] Database setup ✅
- [x] Student Dashboard v1 ✅
- [x] Test Management ✅
- [ ] **Bugünkü Durum Kartları** 🚧 (IN PROGRESS)
- [ ] Admin Dashboard
- [ ] Öğretmen/Koç Dashboard

### Orta Vadeli (3-6 Ay)
- [ ] Real-time analytics updates
- [ ] Chart.js / Recharts entegrasyonu
- [ ] WebSocket notifications
- [ ] Drag & drop report builder
- [ ] Export to PDF/Excel
- [ ] Bulk test import (Excel/CSV)
- [ ] Mobile responsive optimizations

### Uzun Vadeli (6-12 Ay)
- [ ] Mobile app (React Native)
- [ ] API Commercialization (B2B2C model)
- [ ] Integration with schools/institutions
- [ ] AI-powered personalized coaching
- [ ] Video content integration
- [ ] Gamification 2.0 (leaderboards, competitions)

### API Satış Modeli
- **Modüler API**: Diğer eğitim platformlarına satılabilir
- **OpenAPI/Swagger**: Otomatik dökümantasyon
- **API Key authentication**: Güvenli erişim
- **Rate limiting**: Tier-based limits
- **Versioned endpoints**: `/api/v1/`, `/api/v2/`
- **Fiyatlandırma**: Basic/Pro/Enterprise tiers

## 📝 UX Prensipleri

### 1. **5 Saniyede Anlaşılır**
Öğrenci dashboard'a girdiğinde ne yapması gerektiğini anında görür:
- 🔴 Kritik uyarı varsa → EN ÜSTTE belirgin
- 📊 Genel durum → Hero stats (3 kart)
- 🎯 Bugünkü görevler → TodayStatusCards (3 kart)
- 📈 Detaylı analiz → Health bars, trend grafikleri

### 2. **Health Bar Mantığı**
```
Dolu bar (yeşil) = İyi durum
Yarı dolu (sarı) = Dikkat gerektiren
Boş bar (kırmızı) = Kritik durum
```
→ Oyun UI'ından esinlenen, sezgisel progress tracking

### 3. **Aksiyon Odaklı Design**
Her element bir harekete yönlendirir:
- "Hemen Çalış" butonu → Partner content'e yönlendirme
- "Test Gir" butonu → Test management sayfası
- "Detaylı Rapor" → Analytics sayfası

### 4. **Gamification**
- **Streak System**: 7 günlük çalışma streaki
- **Achievement Badges**: Milestone başarıları
- **Progress Tracking**: Visual progress bars
- **Motivational Coaching**: Pozitif pekiştirme

### 5. **Smart Curator (Partner Links)**
End.STP içerik üretmez, yönlendirir:
- Kritik konular → En iyi kaynak önerileri
- Partner platformlara trafik yönlendirme
- Affiliate model ile revenue sharing

## 💼 Business Model

### Hedef Müşteri Segmentleri

#### 1️⃣ **Öğrenci Paketleri** (B2C)
- **Basic**: ₺99/ay - Temel analytics
- **Medium**: ₺199/ay - 4-motor sistemi
- **Premium**: ₺299/ay - Full features + coaching

#### 2️⃣ **Koç/Öğretmen Paketleri** (B2B)
- **Starter**: ₺499/ay - 10 öğrenci
- **Professional**: ₺999/ay - 50 öğrenci
- **Enterprise**: Custom pricing - Unlimited

#### 3️⃣ **Kurumsal Paketler** (B2B2C)
- Dershane/okul entegrasyonları
- White-label çözümler
- API commercialization

### Value Proposition
- **Geleneksel koçluk maliyetinin 1/10'u**
- **Veri-odaklı, subjektif değil**
- **7/24 erişim, her yerden**
- **OSYM/MEB uyumlu** (resmi müfredat)

### Revenue Streams
1. **Subscription Revenue** (ana gelir)
2. **API Licensing** (B2B)
3. **Partner Affiliate** (içerik yönlendirme)
4. **Premium Features** (add-ons)

## 🔐 Security Architecture

### Token Lifecycle & Authentication Flow

```
1. Login Request
   ↓
2. Supabase Auth validates credentials
   ↓
3. JWT Token generated (access + refresh)
   ↓
4. Client stores tokens (httpOnly cookies)
   ↓
5. API requests include access token
   ↓
6. FastAPI validates token signature
   ↓
7. Token expires → Refresh flow
   ↓
8. Logout → Token revocation
```

**Token Properties**:
- **Access Token**: 1 hour expiry, stored in httpOnly cookie
- **Refresh Token**: 7 days expiry, single-use rotation
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Signature Key**: 256-bit secret (rotated monthly)

### RBAC Model (Role-Based Access Control)

```sql
-- Role Hierarchy
ADMIN
  ├── Full system access
  ├── User management
  ├── Analytics override
  └── Subscription management

COACH
  ├── Student analytics (assigned only)
  ├── Test review
  ├── Report generation
  └── Goal setting

STUDENT
  ├── Own dashboard
  ├── Test entry
  ├── Analytics view
  └── Profile management

GUEST
  └── Public pages only
```

**Permission Matrix**:

| Resource | ADMIN | COACH | STUDENT | GUEST |
|----------|-------|-------|---------|-------|
| Dashboard | ✅ All | ✅ Assigned | ✅ Own | ❌ |
| Tests | ✅ CRUD All | ✅ Read Assigned | ✅ CRUD Own | ❌ |
| Analytics | ✅ All | ✅ Assigned | ✅ Own | ❌ |
| Users | ✅ CRUD | ✅ Read Assigned | ✅ Read Own | ❌ |
| Reports | ✅ All | ✅ Generate | ✅ Own | ❌ |
| Settings | ✅ System | ❌ | ✅ Own | ❌ |

### Row Level Security (RLS) Logic Flow

**Supabase RLS Policies** (Applied at database level):

```sql
-- Example: tests table
CREATE POLICY "Users can view own tests"
ON tests FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Coaches can view assigned student tests"
ON tests FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM coach_assignments
    WHERE coach_id = auth.uid()
    AND student_id = tests.user_id
  )
);

CREATE POLICY "Admins can view all tests"
ON tests FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM user_profiles
    WHERE user_id = auth.uid()
    AND role = 'ADMIN'
  )
);
```

**RLS Benefits**:
- ✅ Database-level security (cannot be bypassed)
- ✅ Automatic filtering of queries
- ✅ No application-level logic needed
- ✅ Performance optimized (PostgreSQL)

### Rate Limiting

**Endpoint-Level Limits**:

| Endpoint Type | Free | Basic | Medium | Premium |
|---------------|------|-------|--------|---------|
| Dashboard | 60/min | 120/min | 300/min | Unlimited |
| Test Entry | 10/min | 30/min | 60/min | 100/min |
| Analytics | 30/min | 60/min | 120/min | Unlimited |
| API Access | ❌ | 1000/day | 5000/day | 10000/day |

**Rate Limit Implementation**:
```python
# FastAPI middleware
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/student/dashboard")
@limiter.limit("60/minute")
async def get_dashboard():
    ...
```

**Rate Limit Headers**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1638360000
```

### Service Role Isolation

**Architecture**:
```
┌─────────────────────────────────────┐
│   Client (Browser/Mobile)           │
└──────────────┬──────────────────────┘
               │ JWT Token
               ↓
┌─────────────────────────────────────┐
│   API Gateway (FastAPI)              │
│   - Token validation                 │
│   - Rate limiting                    │
│   - CORS handling                    │
└──────────────┬──────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ↓                 ↓
┌──────────┐    ┌──────────────┐
│ Supabase │    │ Service Role │
│ (Anon)   │    │ (Backend)    │
│ - Public │    │ - Admin ops  │
│ - RLS ON │    │ - Batch jobs │
└──────────┘    └──────────────┘
```

**Anon Key**: Client-side (RLS enforced)  
**Service Key**: Backend-only (RLS bypass for admin operations)

### Endpoint Access Matrix

| Endpoint | Public | Student | Coach | Admin | Service |
|----------|--------|---------|-------|-------|---------|
| `/auth/register` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/auth/login` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/student/dashboard` | ❌ | ✅ Own | ✅ Assigned | ✅ All | ✅ |
| `/tests` | ❌ | ✅ CRUD Own | ✅ Read Assigned | ✅ All | ✅ |
| `/analytics/*` | ❌ | ✅ Own | ✅ Assigned | ✅ All | ✅ |
| `/admin/*` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `/api/v1/batch/*` | ❌ | ❌ | ❌ | ❌ | ✅ |

### Security Best Practices

✅ **Implemented**:
- JWT token rotation on refresh
- Password hashing (bcrypt, 12 rounds)
- SQL injection prevention (Pydantic + SQLAlchemy)
- XSS protection (React escape by default)
- CSRF tokens (SameSite cookies)
- HTTPS enforcement (TLS 1.3)
- Audit logging (all mutations)

🚧 **Planned**:
- [ ] 2FA (Time-based OTP)
- [ ] IP whitelisting (Enterprise tier)
- [ ] Anomaly detection (ML-based)
- [ ] Encryption at rest (field-level)
- [ ] DDoS protection (Cloudflare)

### Compliance

- **GDPR**: Right to access, delete, port data
- **KVKK** (Turkey): Data localization, consent management
- **ISO 27001**: Information security standards (planned)
- **SOC 2**: Security audit (planned for enterprise)

## 🏛️ System Environment Architecture

### High-Level System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  Browser/Mobile  →  Next.js SSR  →  React Components  →  Zustand    │
│  (User Interface)   (PORT 3000)     (UI Logic)          (State)     │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP/HTTPS (REST API)
                             │ Authorization: Bearer <JWT>
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        API GATEWAY LAYER                             │
├─────────────────────────────────────────────────────────────────────┤
│  FastAPI  →  Rate Limiter  →  Auth Middleware  →  CORS Handler     │
│  (PORT 8000)   (slowapi)       (JWT Validation)    (Security)       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ↓                 ↓
┌──────────────────────────┐  ┌──────────────────────────┐
│   BUSINESS LOGIC LAYER   │  │    SERVICE LAYER         │
├──────────────────────────┤  ├──────────────────────────┤
│  4-Motor Analytics       │  │  Email Service           │
│  - BS Model              │  │  - Notifications         │
│  - Difficulty Engine     │  │  - Alerts                │
│  - Time Analyzer         │  │  Storage Service         │
│  - Priority Engine       │  │  - File uploads          │
└────────────┬─────────────┘  └────────────┬─────────────┘
             │                             │
             ↓                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Supabase PostgreSQL  →  Row Level Security  →  Audit Logs         │
│  (38 Tables)             (RLS Policies)         (Change Tracking)   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ↓                 ↓
┌──────────────────────────┐  ┌──────────────────────────┐
│   STORAGE LAYER          │  │    CACHE LAYER           │
├──────────────────────────┤  ├──────────────────────────┤
│  Supabase Storage        │  │  Redis (Planned)         │
│  - User uploads          │  │  - Session cache         │
│  - Profile images        │  │  - Analytics cache       │
│  - Export files          │  │  - Rate limit counters   │
└──────────────────────────┘  └──────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      MONITORING & LOGS                               │
├─────────────────────────────────────────────────────────────────────┤
│  Application Logs  →  Error Tracking  →  Performance Metrics        │
│  (FastAPI Logger)     (Sentry - Planned)  (Custom Dashboard)        │
└─────────────────────────────────────────────────────────────────────┘
```

### Detailed Request Flow

```
1️⃣  USER ACTION
    │
    ↓
2️⃣  FRONTEND (Next.js)
    ├─ User clicks "Test Gir"
    ├─ Zustand store triggered
    ├─ API client (Axios) prepares request
    └─ JWT token attached to header
    │
    ↓
3️⃣  API GATEWAY (FastAPI)
    ├─ CORS check
    ├─ Rate limit check (slowapi)
    ├─ JWT validation (Supabase Auth)
    ├─ Route to endpoint handler
    └─ Pydantic schema validation
    │
    ↓
4️⃣  BUSINESS LOGIC
    ├─ Service layer called
    ├─ 4-Motor analytics executed
    ├─ Data transformations
    └─ Prepare response
    │
    ↓
5️⃣  DATABASE (Supabase)
    ├─ RLS policy check
    ├─ SQL query execution
    ├─ Audit log entry
    └─ Return results
    │
    ↓
6️⃣  RESPONSE PIPELINE
    ├─ Data serialization (Pydantic)
    ├─ Response headers (rate limit, cache)
    ├─ JSON formatting
    └─ Send to client
    │
    ↓
7️⃣  FRONTEND UPDATE
    ├─ Axios receives response
    ├─ Zustand state update
    ├─ React components re-render
    └─ UI update (smooth animations)
```

### Network Architecture

```
                         INTERNET
                            │
                            ↓
                     ┌──────────────┐
                     │  CloudFlare  │
                     │  (Planned)   │
                     │  - CDN       │
                     │  - DDoS      │
                     └──────┬───────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ↓                               ↓
    ┌──────────────┐              ┌──────────────┐
    │  Frontend    │              │  Backend     │
    │  Next.js     │              │  FastAPI     │
    │  Vercel      │              │  Railway     │
    │  (PORT 3000) │◄────────────►│  (PORT 8000) │
    └──────────────┘   REST API   └──────┬───────┘
                                          │
                                          ↓
                                  ┌──────────────┐
                                  │  Supabase    │
                                  │  PostgreSQL  │
                                  │  Storage     │
                                  │  Auth        │
                                  └──────────────┘
```

### Data Flow Patterns

#### 1️⃣ **Read Pattern** (Dashboard Load)
```
Client → GET /api/v1/student/dashboard
       → FastAPI validates JWT
       → Service layer aggregates data
       → Supabase queries (RLS applied)
       → 4-Motor calculations
       → Response serialization
       → Client state update
       → UI render
```

#### 2️⃣ **Write Pattern** (Test Entry)
```
Client → POST /api/v1/tests
       → FastAPI validates JWT + data
       → Business logic validation
       → Supabase INSERT (RLS applied)
       → Audit log creation
       → Success response
       → Client state update
       → Dashboard refresh trigger
```

#### 3️⃣ **Real-time Pattern** (Planned)
```
Client → WebSocket connection
       → Supabase real-time subscription
       → Change detected in DB
       → Push notification to client
       → Zustand state update
       → UI update (no refresh)
```

### Environment Variables

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
```

**Backend (.env)**:
```bash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx...  # Anon key
SUPABASE_SERVICE_KEY=eyJxxx...  # Service role key
JWT_SECRET=your_256_bit_secret
ENVIRONMENT=development  # development|staging|production
```

### Port Configuration

| Service | Local Port | Production |
|---------|-----------|------------|
| Frontend | 3000 | 443 (HTTPS) |
| Backend | 8000 | 443 (HTTPS) |
| PostgreSQL | 5432 | Managed by Supabase |
| Redis (Planned) | 6379 | Managed |

## 🧮 Analytics Engine – Internal Formula Book

### Motor Overview

| Motor | Input | Output | Formula Complexity | Failure Modes |
|-------|-------|--------|-------------------|---------------|
| **BS-Model** | Test history, timestamps | Next review date, retention rate | **Medium** (Exponential decay) | Missing timestamps, irregular testing |
| **Difficulty Engine** | Blank/wrong answers, volatility | Difficulty score (0-100) | **Low** (Weighted average) | Zero attempts, skewed data |
| **Time Analyzer** | Question times, correct/wrong | Tempo score, efficiency | **Low** (Statistical) | Outliers, incomplete data |
| **Priority Engine** | Difficulty, retention, prerequisites | Priority ranking | **High** (Graph traversal) | Circular dependencies, missing links |

---

### 1️⃣ BS-Model (Spaced Repetition Engine)

**Purpose**: Predict when student will forget a topic and schedule optimal review time.

#### Core Formula

```python
# Retention Rate Calculation
R(t) = R₀ × e^(-t/S_effective)

Where:
- R(t) = Retention rate at time t (0-100%)
- R₀ = Initial retention after learning (usually 100%)
- t = Time elapsed since last review (days)
- S_effective = Stability parameter (personalized)
- e = Euler's number (2.71828...)
```

#### S_effective Calculation

```python
S_effective = S_base × (1 + quality_factor × repetition_bonus)

S_base = 2.0  # Initial stability (2 days)
quality_factor = (correct_rate - 0.5) × 2  # Range: -1 to +1
repetition_bonus = 0.2 × (attempt_count - 1)  # Grows with repetitions
```

#### Next Review Date

```python
# Target retention rate for review: 80%
# Solve for t when R(t) = 0.80

t_review = -S_effective × ln(0.80 / R₀)

# If R₀ = 100%:
t_review = -S_effective × ln(0.80)
         = S_effective × 0.223

Example:
If S_effective = 10 days:
t_review = 10 × 0.223 = 2.23 days
```

#### Implementation Example

```python
from datetime import datetime, timedelta
import math

def calculate_next_review(
    last_attempt_date: datetime,
    correct_rate: float,
    attempt_count: int,
    current_retention: float = 100.0
) -> datetime:
    """
    Calculate optimal next review date.
    
    Returns:
        datetime: Recommended review date
    """
    # Calculate S_effective
    quality_factor = (correct_rate - 0.5) * 2
    repetition_bonus = 0.2 * (attempt_count - 1)
    s_effective = 2.0 * (1 + quality_factor * repetition_bonus)
    
    # Calculate days until review
    target_retention = 0.80
    days_until_review = -s_effective * math.log(target_retention / (current_retention / 100))
    
    # Add to last attempt date
    next_review = last_attempt_date + timedelta(days=days_until_review)
    
    return next_review
```

**Failure Modes**:
- ❌ Missing `attempt_date` → Cannot calculate time decay
- ❌ Irregular testing → S_effective becomes unreliable
- ❌ All tests wrong (correct_rate = 0) → Negative quality_factor

**Mitigation**:
```python
# Enforce 24-hour entry rule
if (datetime.now() - test_date).days > 1:
    raise ValueError("Test must be entered within 24 hours")

# Clamp quality_factor
quality_factor = max(-0.8, min(0.8, quality_factor))

# Minimum S_effective
s_effective = max(1.0, s_effective)  # At least 1 day
```

---

### 2️⃣ Difficulty Engine

**Purpose**: Calculate learning difficulty based on student performance.

#### Core Formula

```python
Difficulty = (
    0.55 × blank_rate +
    0.30 × wrong_rate +
    0.10 × volatility_factor +
    0.05 × misconception_factor
) × 100

Range: 0-100 (higher = more difficult)
```

#### Component Definitions

```python
# 1. Blank Rate (Empty answers)
blank_rate = blank_count / total_questions

# 2. Wrong Rate (Incorrect answers)
wrong_rate = wrong_count / total_questions

# 3. Volatility Factor (Performance consistency)
volatility_factor = std_dev(scores) / mean(scores)
# Measures how much performance varies across attempts

# 4. Misconception Factor (Systematic errors)
misconception_factor = repeated_error_count / total_errors
# Identifies recurring mistakes on same question types
```

#### Implementation Example

```python
import numpy as np

def calculate_difficulty(
    blank_count: int,
    wrong_count: int,
    correct_count: int,
    attempt_scores: list[float]
) -> dict:
    """
    Calculate topic difficulty score.
    
    Returns:
        dict: {
            'difficulty_score': float (0-100),
            'breakdown': dict of components
        }
    """
    total = blank_count + wrong_count + correct_count
    
    if total == 0:
        return {'difficulty_score': 50.0, 'breakdown': {}}
    
    # Component calculations
    blank_rate = blank_count / total
    wrong_rate = wrong_count / total
    
    # Volatility (requires 2+ attempts)
    if len(attempt_scores) >= 2:
        volatility = np.std(attempt_scores) / (np.mean(attempt_scores) + 1e-6)
        volatility_factor = min(1.0, volatility)  # Cap at 1.0
    else:
        volatility_factor = 0.0
    
    # Misconception (simplified - would need detailed error analysis)
    misconception_factor = 0.0  # Placeholder
    
    # Weighted difficulty
    difficulty = (
        0.55 * blank_rate +
        0.30 * wrong_rate +
        0.10 * volatility_factor +
        0.05 * misconception_factor
    ) * 100
    
    return {
        'difficulty_score': round(difficulty, 2),
        'breakdown': {
            'blank_contribution': round(0.55 * blank_rate * 100, 2),
            'wrong_contribution': round(0.30 * wrong_rate * 100, 2),
            'volatility_contribution': round(0.10 * volatility_factor * 100, 2),
            'misconception_contribution': round(0.05 * misconception_factor * 100, 2)
        }
    }
```

**Failure Modes**:
- ❌ Zero attempts → No data for calculation
- ❌ All same result → Volatility = 0 (division by zero risk)
- ❌ Single attempt → Cannot calculate volatility

**Mitigation**:
```python
# Require minimum attempts
if total < 5:
    return {'difficulty_score': 50.0, 'note': 'Insufficient data'}

# Handle division by zero
volatility = np.std(scores) / (np.mean(scores) + 1e-6)  # Add epsilon
```

---

### 3️⃣ Time Analyzer

**Purpose**: Measure solving speed and efficiency.

#### Core Formulas

```python
# 1. Average Time per Question
avg_time = total_time_seconds / question_count

# 2. Tempo Score (Relative to target)
target_time_per_question = 90  # seconds (1.5 min)
tempo_score = (target_time / avg_time) × 100

tempo_score > 100 → Fast (efficient)
tempo_score < 100 → Slow (needs practice)

# 3. Efficiency Score
efficiency = (correct_count / total_count) × (target_time / avg_time) × 100

Combines accuracy + speed
```

#### Implementation Example

```python
def analyze_time_performance(
    total_time: int,  # seconds
    correct_count: int,
    wrong_count: int,
    blank_count: int,
    target_time_per_question: int = 90
) -> dict:
    """
    Analyze time efficiency and tempo.
    
    Returns:
        dict: Tempo and efficiency metrics
    """
    total_questions = correct_count + wrong_count + blank_count
    
    if total_questions == 0 or total_time == 0:
        return {'error': 'Invalid input'}
    
    # Calculate metrics
    avg_time = total_time / total_questions
    tempo_score = (target_time_per_question / avg_time) * 100
    accuracy = correct_count / total_questions
    efficiency = accuracy * (target_time_per_question / avg_time) * 100
    
    # Tempo classification
    if tempo_score > 120:
        tempo_label = "Çok Hızlı (Risk: Hata artışı)"
    elif tempo_score > 90:
        tempo_label = "Optimal"
    elif tempo_score > 70:
        tempo_label = "Yavaş"
    else:
        tempo_label = "Çok Yavaş (Pratik gerekli)"
    
    return {
        'avg_time_per_question': round(avg_time, 1),
        'tempo_score': round(tempo_score, 2),
        'tempo_label': tempo_label,
        'efficiency_score': round(efficiency, 2),
        'time_budget_usage': round((avg_time / target_time_per_question) * 100, 1)
    }
```

**Failure Modes**:
- ❌ Outlier times (e.g., paused test) → Skews average
- ❌ Incomplete time data → Cannot calculate
- ❌ Extremely fast times (< 10s) → Likely guessing

**Mitigation**:
```python
# Remove outliers (IQR method)
Q1 = np.percentile(times, 25)
Q3 = np.percentile(times, 75)
IQR = Q3 - Q1
filtered_times = [t for t in times if Q1 - 1.5*IQR <= t <= Q3 + 1.5*IQR]

# Enforce minimum time
if avg_time < 10:
    warnings.append("Suspiciously fast - possible guessing")
```

---

### 4️⃣ Priority Engine

**Purpose**: Rank topics by urgency using multiple factors.

#### Core Formula

```python
Priority = (
    α × difficulty_weight +
    β × retention_weight +
    γ × prerequisite_weight
)

Where:
α = 0.40  # Difficulty importance
β = 0.35  # Retention importance
γ = 0.25  # Prerequisite importance
```

#### Component Calculations

```python
# 1. Difficulty Weight
difficulty_weight = difficulty_score / 100  # Normalized

# 2. Retention Weight (inverse - lower retention = higher priority)
retention_weight = 1 - (retention_rate / 100)

# 3. Prerequisite Weight
# Topics that are prerequisites for many others get higher priority
prerequisite_weight = dependent_topic_count / max_dependencies
```

#### Graph Traversal for Prerequisites

```python
from collections import defaultdict, deque

def calculate_prerequisite_impact(
    topic_id: str,
    prerequisite_graph: dict[str, list[str]]
) -> int:
    """
    Calculate how many topics depend on this topic (BFS).
    
    Args:
        topic_id: Current topic
        prerequisite_graph: {topic_id: [dependent_topic_ids]}
    
    Returns:
        int: Number of dependent topics
    """
    visited = set()
    queue = deque([topic_id])
    count = 0
    
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        
        # Get topics that depend on current
        dependents = prerequisite_graph.get(current, [])
        count += len(dependents)
        queue.extend(dependents)
    
    return count
```

#### Complete Implementation

```python
def calculate_topic_priority(
    topic_id: str,
    difficulty_score: float,
    retention_rate: float,
    prerequisite_graph: dict[str, list[str]],
    max_dependencies: int = 10
) -> dict:
    """
    Calculate comprehensive priority score.
    
    Returns:
        dict: Priority score and breakdown
    """
    # Weights
    alpha, beta, gamma = 0.40, 0.35, 0.25
    
    # Components
    difficulty_weight = difficulty_score / 100
    retention_weight = 1 - (retention_rate / 100)
    
    dependent_count = calculate_prerequisite_impact(topic_id, prerequisite_graph)
    prerequisite_weight = min(1.0, dependent_count / max_dependencies)
    
    # Final priority
    priority = (
        alpha * difficulty_weight +
        beta * retention_weight +
        gamma * prerequisite_weight
    ) * 100
    
    return {
        'priority_score': round(priority, 2),
        'breakdown': {
            'difficulty_contribution': round(alpha * difficulty_weight * 100, 2),
            'retention_contribution': round(beta * retention_weight * 100, 2),
            'prerequisite_contribution': round(gamma * prerequisite_weight * 100, 2)
        },
        'dependent_topic_count': dependent_count
    }
```

**Failure Modes**:
- ❌ Circular dependencies → Infinite loop in BFS
- ❌ Missing prerequisite data → Underestimated priority
- ❌ All topics same priority → No differentiation

**Mitigation**:
```python
# Detect circular dependencies
def has_cycle(graph: dict[str, list[str]]) -> bool:
    visited = set()
    rec_stack = set()
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True  # Cycle detected
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node):
                raise ValueError(f"Circular dependency detected involving {node}")
    
    return False

# Validate before processing
if has_cycle(prerequisite_graph):
    raise ValueError("Cannot process: circular dependencies exist")
```

---

### Formula Validation Tests

```python
# Unit test examples
def test_bs_model_extreme_cases():
    # Perfect performance
    assert calculate_next_review(..., correct_rate=1.0) > 7  # days
    
    # Poor performance
    assert calculate_next_review(..., correct_rate=0.2) < 3  # days
    
    # Edge case: zero attempts
    with pytest.raises(ValueError):
        calculate_next_review(..., attempt_count=0)

def test_difficulty_engine_boundaries():
    # All wrong
    result = calculate_difficulty(blank=0, wrong=10, correct=0)
    assert 25 <= result['difficulty_score'] <= 35  # 0.30 weight
    
    # All blank
    result = calculate_difficulty(blank=10, wrong=0, correct=0)
    assert 50 <= result['difficulty_score'] <= 60  # 0.55 weight

## 🚀 Deployment Plan

### Environment Strategy

```
┌─────────────────────────────────────────────────────────────┐
│  LOCAL → QA → STAGING → PRODUCTION                          │
│  (Dev)   (Test) (Pre-prod) (Live)                           │
└─────────────────────────────────────────────────────────────┘
```

#### 1️⃣ **LOCAL** (Development)

**Purpose**: Individual developer testing

**Configuration**:
```yaml
Environment: development
Backend: localhost:8000
Frontend: localhost:3000
Database: Supabase (dev project)
Auth: Supabase Auth (test users)
Logging: Console output
Hot Reload: Enabled (FastAPI + Next.js)
```

**Setup**:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

**Data**:
- Mock data in `tests/fixtures/`
- Demo user: `demo@end-stp.com / demo123`
- Seed scripts: `python scripts/seed_db.py`

---

#### 2️⃣ **QA** (Quality Assurance)

**Purpose**: Automated testing + manual QA

**Configuration**:
```yaml
Environment: qa
Backend: https://qa-api.end-stp.com
Frontend: https://qa.end-stp.com
Database: Supabase (qa project)
Auth: Supabase Auth (qa users)
Logging: File + Console
CI/CD: GitHub Actions
```

**Deployment**:
```yaml
# .github/workflows/qa-deploy.yml
name: QA Deployment

on:
  push:
    branches: [ develop ]

jobs:
  deploy-qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run tests
        run: |
          pytest tests/
          npm run test
      
      - name: Deploy Backend
        run: |
          # Deploy to Railway/Render (QA environment)
          railway deploy --environment qa
      
      - name: Deploy Frontend
        run: |
          # Deploy to Vercel (QA)
          vercel deploy --env qa
```

**Testing**:
- ✅ Unit tests (pytest, Jest)
- ✅ Integration tests
- ✅ E2E tests (Playwright)
- ✅ Load testing (Locust)
- ✅ Manual QA checklist

---

#### 3️⃣ **STAGING** (Pre-Production)

**Purpose**: Final validation before production

**Configuration**:
```yaml
Environment: staging
Backend: https://staging-api.end-stp.com
Frontend: https://staging.end-stp.com
Database: Supabase (staging project - production clone)
Auth: Supabase Auth (staging users)
Logging: Centralized (Papertrail/Datadog)
Monitoring: Full metrics (same as production)
```

**Deployment**:
```yaml
# Triggered by: PR merge to main
name: Staging Deployment

on:
  pull_request:
    branches: [ main ]
    types: [ closed ]

jobs:
  deploy-staging:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Run full test suite
        run: |
          pytest tests/ --cov --cov-report=xml
          npm run test:e2e
      
      - name: Database migration
        run: |
          alembic upgrade head
      
      - name: Deploy
        run: |
          railway deploy --environment staging
          vercel deploy --env staging
      
      - name: Smoke tests
        run: |
          curl -f https://staging-api.end-stp.com/health
          curl -f https://staging.end-stp.com
```

**Validation**:
- ✅ Full regression testing
- ✅ Performance benchmarks
- ✅ Security scan (OWASP ZAP)
- ✅ Accessibility audit
- ✅ Stakeholder approval

---

#### 4️⃣ **PRODUCTION** (Live)

**Purpose**: Public-facing production system

**Configuration**:
```yaml
Environment: production
Backend: https://api.end-stp.com
Frontend: https://end-stp.com
Database: Supabase (production project)
Auth: Supabase Auth (real users)
CDN: CloudFlare
Logging: Centralized + Archived
Monitoring: 24/7 (PagerDuty alerts)
Backup: Automated daily + point-in-time recovery
```

**Deployment Strategy**: **Blue-Green Deployment**

```
BLUE (Current)              GREEN (New Version)
     │                           │
     ↓                           ↓
[ v1.4.0 ]                  [ v1.5.0 ]
  100% traffic              0% traffic
     │                           │
     └─────── Switch ────────────┘
                │
           Gradual cutover
                │
         ┌──────┴──────┐
         ↓             ↓
    [ v1.4.0 ]    [ v1.5.0 ]
    20% traffic   80% traffic
         │             │
         └─────────────┘
              Rollback option
```

**Deployment Process**:
```yaml
name: Production Deployment

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Create deployment
        run: |
          # Deploy to GREEN environment
          railway deploy --environment production-green
          vercel deploy --prod --alias green.end-stp.com
      
      - name: Health check GREEN
        run: |
          ./scripts/health_check.sh green.end-stp.com
      
      - name: Gradual traffic shift (Canary)
        run: |
          # 10% → GREEN
          cloudflare-traffic-split blue:90 green:10
          sleep 300  # Monitor for 5 minutes
          
          # 50% → GREEN
          cloudflare-traffic-split blue:50 green:50
          sleep 600  # Monitor for 10 minutes
          
          # 100% → GREEN
          cloudflare-traffic-split blue:0 green:100
      
      - name: Promote GREEN to BLUE
        run: |
          # GREEN becomes new BLUE
          railway promote green to blue
          vercel alias set green.end-stp.com end-stp.com
      
      - name: Notify team
        run: |
          slack-notify "✅ Production deployment v${{ github.ref_name }} complete"
```

**Rollback Plan**:
```bash
# Instant rollback (< 30 seconds)
cloudflare-traffic-split blue:100 green:0

# Full rollback
railway rollback production --to-version v1.4.0
vercel rollback end-stp.com
```

---

### CI/CD Pipeline

**GitHub Actions Workflow**:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  # 1. Code Quality
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Python lint
        run: |
          pip install ruff
          ruff check app/
      - name: TypeScript lint
        run: |
          npm run lint

  # 2. Unit Tests
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11]
    steps:
      - uses: actions/checkout@v3
      - name: Backend tests
        run: |
          pytest tests/unit/ --cov
      - name: Frontend tests
        run: |
          npm run test -- --coverage

  # 3. Integration Tests
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
    steps:
      - name: Integration tests
        run: |
          pytest tests/integration/

  # 4. E2E Tests
  e2e:
    runs-on: ubuntu-latest
    steps:
      - name: E2E tests (Playwright)
        run: |
          npm run test:e2e

  # 5. Security Scan
  security:
    runs-on: ubuntu-latest
    steps:
      - name: Dependency check
        run: |
          pip install safety
          safety check
      - name: SAST scan
        uses: github/super-linter@v4

  # 6. Build
  build:
    needs: [lint, test, integration]
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: |
          docker build -t end-stp-backend:${{ github.sha }} ./backend
          docker build -t end-stp-frontend:${{ github.sha }} ./frontend
      - name: Push to registry
        run: |
          docker push end-stp-backend:${{ github.sha }}

  # 7. Deploy
  deploy:
    needs: [build]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          # Production deployment (manual approval required)
          gh workflow run production-deploy.yml
```

---

### Backup Strategy

#### Database Backups

**Automated Backups** (Supabase):
```yaml
Schedule:
  - Full backup: Daily at 02:00 UTC
  - Incremental: Every 6 hours
  - Transaction logs: Real-time (point-in-time recovery)

Retention:
  - Daily backups: 30 days
  - Weekly backups: 12 weeks
  - Monthly backups: 12 months

Storage:
  - Primary: Supabase managed storage
  - Secondary: AWS S3 (cross-region replication)
```

**Manual Backup Script**:
```bash
#!/bin/bash
# scripts/backup_database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql"

# Dump database
pg_dump $SUPABASE_DATABASE_URL > $BACKUP_FILE

# Compress
gzip $BACKUP_FILE

# Upload to S3
aws s3 cp ${BACKUP_FILE}.gz s3://end-stp-backups/database/

# Verify
aws s3 ls s3://end-stp-backups/database/${BACKUP_FILE}.gz

# Cleanup local
rm ${BACKUP_FILE}.gz

echo "✅ Backup complete: ${BACKUP_FILE}.gz"
```

#### Application Backups

```yaml
Code:
  - Git repository (GitHub)
  - Tagged releases (semantic versioning)
  - Branch protection (main, develop)

Environment Variables:
  - Encrypted storage (GitHub Secrets)
  - Backup in 1Password vault
  - Documented in wiki

User-Generated Content:
  - Supabase Storage (automatic replication)
  - Daily sync to S3
  - 90-day retention
```

---

### Monitoring Stack

#### 1️⃣ **Application Monitoring**

**FastAPI Metrics**:
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    request_latency.observe(time.time() - start_time)
    request_count.inc()
    return response
```

**Next.js Analytics**:
```typescript
// Vercel Analytics
import { Analytics } from '@vercel/analytics/react';

export default function App() {
  return (
    <>
      <YourApp />
      <Analytics />
    </>
  );
}
```

#### 2️⃣ **Error Tracking**

**Sentry Integration** (Planned):
```python
# Backend
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT"),
    traces_sample_rate=1.0
)
```

```typescript
// Frontend
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});
```

#### 3️⃣ **Uptime Monitoring**

**Health Check Endpoints**:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": os.getenv("APP_VERSION"),
        "database": await check_database_connection()
    }

@app.get("/readiness")
async def readiness_check():
    # Check all dependencies
    checks = {
        "database": await check_database(),
        "supabase": await check_supabase(),
        "cache": await check_redis()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(
        content={"status": "ready" if all_healthy else "not ready", "checks": checks},
        status_code=status_code
    )
```

**Monitoring Tools**:
- **UptimeRobot**: External monitoring (1-min intervals)
- **PagerDuty**: Incident management + alerting
- **Datadog**: APM + infrastructure monitoring (planned)

#### 4️⃣ **Performance Metrics**

**SLOs (Service Level Objectives)**:
```yaml
Availability: 99.9% uptime
  - Downtime budget: 43 minutes/month

Response Time:
  - p50: < 100ms
  - p95: < 200ms
  - p99: < 500ms

Error Rate:
  - < 0.1% of requests

Database Query Time:
  - p95: < 50ms
```

**Alerting Rules**:
```yaml
Critical Alerts (PagerDuty):
  - API error rate > 1%
  - Response time p95 > 1000ms
  - Database connection failure
  - Payment processing failure

Warning Alerts (Slack):
  - API error rate > 0.5%
  - Response time p95 > 500ms
  - High memory usage (> 80%)
  - Slow query detected (> 1s)

Info Alerts (Email):
  - New deployment
  - Backup completed
  - Traffic spike detected
```

---

### Disaster Recovery Plan

#### RTO & RPO Targets

```yaml
RTO (Recovery Time Objective): 1 hour
  - Maximum acceptable downtime

RPO (Recovery Point Objective): 15 minutes
  - Maximum acceptable data loss

Business Continuity:
  - Critical features: 99.9% uptime
  - Non-critical features: 99% uptime
```

#### Recovery Procedures

**Scenario 1: Database Failure**
```bash
# 1. Switch to read replica (automatic)
# 2. Investigate primary database issue
# 3. Restore from latest backup (if needed)
# 4. Validate data integrity
# 5. Switch back to primary

Estimated Recovery Time: 30 minutes
```

**Scenario 2: Application Crash**
```bash
# 1. Auto-restart (Kubernetes/Railway)
# 2. If restart fails → rollback to previous version
# 3. Investigate crash logs
# 4. Deploy fix

Estimated Recovery Time: 15 minutes
```

**Scenario 3: Data Corruption**
```bash
# 1. Identify affected records
# 2. Restore from point-in-time backup
# 3. Validate restored data
# 4. Communicate to affected users

Estimated Recovery Time: 2 hours
```

---

### Deployment Checklist

**Pre-Deployment**:
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code review approved (2+ reviewers)
- [ ] Security scan passed
- [ ] Performance benchmarks met
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Stakeholder approval (for major releases)

**During Deployment**:
- [ ] Deployment started (timestamp logged)
- [ ] Health checks passing (GREEN environment)
- [ ] Gradual traffic shift (canary deployment)
- [ ] Metrics monitoring (error rates, latency)
- [ ] No critical alerts triggered

**Post-Deployment**:
- [ ] Smoke tests passed
- [ ] Performance metrics normal
- [ ] Error tracking checked (Sentry)
- [ ] User feedback monitored
- [ ] Deployment tagged in Git
- [ ] Changelog updated
- [ ] Team notified (Slack)
```

## 🧪 Testing Strategy

### Backend Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# API tests
pytest tests/api/
```

### Frontend Tests
```bash
# Component tests
npm run test

# E2E tests (Playwright)
npm run test:e2e
```

## 📈 Performance Metrics

### Target KPIs
- **API Response Time**: < 200ms (p95)
- **Dashboard Load**: < 2s (initial load)
- **Database Queries**: < 50ms (p95)
- **Uptime**: 99.9%

### Monitoring
- **Backend**: FastAPI built-in metrics
- **Frontend**: Next.js analytics
- **Database**: Supabase performance insights
- **Errors**: Sentry integration (planned)

## 🤝 Katkıda Bulunma

Bu proje aktif geliştirme aşamasındadır.

### Development Workflow
1. Branch oluştur (`feature/new-feature`)
2. Commit yap (`git commit -m "feat: add new feature"`)
3. Test çalıştır (`npm test` / `pytest`)
4. Push yap (`git push origin feature/new-feature`)
5. Pull Request aç

### Commit Convention
```
feat: Yeni özellik
fix: Bug düzeltme
docs: Dökümantasyon
style: Kod formatı
refactor: Kod iyileştirme
test: Test ekleme/düzeltme
chore: Bakım işleri
```

## 📄 Lisans

Proprietary - End.STP © 2024-2025

---

## 🚀 Geliştirici Notları

### Önemli Kurallar
1. ⚠️ **Her değişiklik öncesi backup al**
2. ⚠️ **Database şema güncellemeleri → Mutlaka dokümante et**
3. ⚠️ **Her feature → Git commit**
4. ⚠️ **Production'a push öncesi → Test yap**

### Teknoloji Kararları
- **TypeScript strict mode** → Tip güvenliği
- **Tailwind CSS** → No @apply, direkt classes
- **Zustand** → Redux karmaşasından kaçış
- **FastAPI** → Python'da en hızlı framework
- **Supabase** → Managed PostgreSQL + Auth

### Debug Tips
```bash
# Backend logs
tail -f backend/logs/app.log

# Frontend console
npm run dev (check browser console)

# Database queries
Supabase Dashboard → Logs → API Logs
```

### Common Issues

**Backend çalışmıyor?**
```bash
# Check port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
# Restart
uvicorn app.main:app --reload --port 8000
```

**Frontend build error?**
```bash
# Clear cache
rm -rf .next
npm install
npm run build
```

**Database connection issue?**
```bash
# Check .env variables
cat .env | grep SUPABASE
# Test connection
curl -H "apikey: YOUR_KEY" YOUR_SUPABASE_URL/rest/v1/
```

---

**Son Güncelleme**: 3 Aralık 2025  
**Sürüm**: v1.5 (Backend + Frontend + DB integrated)  
**Durum**: 🚧 Active Development