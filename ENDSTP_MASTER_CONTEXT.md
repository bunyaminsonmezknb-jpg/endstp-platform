# 📘 End.STP Master Context Documentation

> **Version**: 1.1  
> **Last Updated**: December 24, 2024  
> **Status**: MVP Phase (80% Complete)  
> **Target**: Global Top 5 EdTech Analytics Platform by March 14, 2025

---

## 📑 Table of Contents

1. [Ürün Tanımı](#1-ürün-tanımı)
2. [Mimari Özet](#2-mimari-özet)
3. [Repo Tree](#3-repo-tree)
4. [Veri Modeli](#4-veri-modeli)
5. [API Sözleşmesi](#5-api-sözleşmesi)
6. [UI Akışları](#6-ui-akışları)
7. [Project Constitution / Altın Kurallar](#7-project-constitution--altın-kurallar)
8. [Faz Planı](#8-faz-planı)
9. [Known Issues / Gotchas](#9-known-issues--gotchas)
10. [Çalıştırma Rehberi](#10-çalıştırma-rehberi)

---

## 1. Ürün Tanımı

### 🎯 Problem Statement

**End.STP does not fix learning by rewinding, it fixes learning by revealing where progress slows.**

Geleneksel eğitim sistemleri öğrencilerin sadece doğru/yanlış yaptıklarını gösterir, ancak **bilgi boşluklarının nereden kaynaklandığını** ve **hangi konularda unutma sürecinin başladığını** göstermez.

### 💡 Çözüm

End.STP, AI-powered educational analytics platform olarak:
- **Unutma eğrisi tahminleri** ile proaktif müdahale
- **Prerequisite governance** ile bilgi ağacındaki zayıf noktaları tespit
- **7+1 Motor** ile çok boyutlu analiz
- **Smart Curator** modeli: Orijinal içerik üretmek yerine, partner içeriklerine yönlendirme

### 👥 Hedef Kitle

1. **Bireysel Öğrenciler**: OSYM-YKS hazırlananlar (ilk pazar), sonra global genişleme
2. **Koçlar/Öğretmenler**: Dershane ve özel ders veren eğitmenler
3. **Eğitim Kurumları**: Yüzlerce kurum, yüz binlerce kullanıcı hedefi

### 🎬 Ana Ekranlar

| Ekran | Kullanıcı | Amaç |
|-------|-----------|------|
| **Student Dashboard** | Öğrenci | Kritik uyarılar, bugünün görevleri, sağlık barları |
| **Test Entry** | Öğrenci | Deneme/soru girişi, timing kaydı |
| **Past Tests** | Öğrenci | Geçmiş denemeler, trend grafikleri |
| **Admin Dashboard** | Yönetici | Curriculum mapping, prerequisite yönetimi |
| **Coach Dashboard** | Koç | Öğrenci grupları, kolektif analiz |
| **Feature Control Panel** | Admin | Motor açma/kapama, tier yönetimi |

### 📊 Kritik Metrikler

**Öğrenci Bazlı:**
- **Remembering Rate (R%)**: Her konu için hatırlama yüzdesi (0-100%)
- **Critical Topics Count**: R% < 40 olan konular (kırmızı bölge)
- **Frozen Topics**: 30+ gün test girilmemiş konular
- **Streak Days**: Ardışık giriş yapılan günler
- **BS-Model Score**: Unutma eğrisi tahmini (0-100)

**Platform Bazlı:**
- **DAU/MAU**: Daily/Monthly Active Users
- **Retention Rate**: 7-day, 30-day retention
- **Partner Click-through Rate**: Smart curator başarı oranı
- **Subscription Conversion**: Free → Basic → Medium → Premium
- **API Usage**: External calls (future revenue stream)

---

## 2. Mimari Özet

### 🗃️ System Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    GLOBAL-FIRST ARCHITECTURE                 │
│     (Single Source, Multiple Markets, Affiliate-Ready)       │
└───────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │      Frontend Layer (Next.js 14)    │
        │  - App Router (TypeScript)          │
        │  - Tailwind CSS + Zustand           │
        │  - JWT Token Management             │
        │  - Centralized API Client           │
        └──────────────┬──────────────────────┘
                       │ HTTPS/REST
                       ▼
        ┌─────────────────────────────────────┐
        │     Backend Layer (FastAPI)         │
        │  - Python 3.10+                     │
        │  - Pydantic validation              │
        │  - JWT Authentication               │
        │  - Swagger/OpenAPI docs             │
        │  - Rate limiting                    │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │    Database Layer (Supabase)        │
        │  - PostgreSQL 15+                   │
        │  - Row Level Security (RLS)         │
        │  - Real-time subscriptions          │
        │  - Automated backups                │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │      Analytics Engines (7+1)        │
        │  1. BS-Model (Spaced Repetition)    │
        │  2. Priority Engine                 │
        │  3. Difficulty Engine               │
        │  4. Time Analyzer                   │
        │  5. Prerequisite Analyzer (planned) │
        │  6. Goal Tracker (planned)          │
        │  7. Trend Predictor (planned)       │
        │  +1. Master Orchestrator            │
        └─────────────────────────────────────┘
```

### 🔐 Authentication Flow

```
Client (Next.js)
    │
    ├─→ Login Request (email/password)
    │
    ▼
Backend (FastAPI)
    │
    ├─→ Supabase Auth Check
    │
    ▼
Supabase
    │
    ├─→ JWT Token (access + refresh)
    │
    ▼
Client stores tokens
    │
    ├─→ Every API call includes: Authorization: Bearer <token>
    │
    ▼
Backend validates JWT
    │
    ├─→ RLS policies enforce data access
```

### 🌐 Deployment Architecture

```
Production:
  - Frontend: Vercel/Netlify (CDN)
  - Backend: Railway/Render (Auto-scaling)
  - Database: Supabase (Multi-region)
  - Storage: Supabase Storage (S3-compatible)
  - Monitoring: Sentry + Datadog

Staging:
  - Isolated environments for each major feature
  - Shared Supabase staging database
  - Feature flags for gradual rollout

Local Development:
  - Frontend: localhost:3000
  - Backend: localhost:8000
  - Database: Local Supabase or Remote staging
```

---

## 3. Repo Tree

### 📁 Current Structure (MVP Phase)

```
end-stp-project/
│
├── backend/                              # ⚠️ TO BE INITIALIZED
│   ├── app/
│   │   ├── main.py                       # FastAPI entry point
│   │   ├── config.py                     # Environment configs
│   │   ├── database.py                   # Supabase connection
│   │   │
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py           # Login/logout/refresh
│   │   │   │   │   ├── students.py       # Student CRUD
│   │   │   │   │   ├── tests.py          # Test entry/retrieval
│   │   │   │   │   ├── dashboard.py      # Dashboard data
│   │   │   │   │   ├── motors.py         # Engine calculations
│   │   │   │   │   └── admin.py          # Admin operations
│   │   │   │   └── router.py
│   │   │   └── deps.py                   # Common dependencies
│   │   │
│   │   ├── models/                       # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── test.py
│   │   │   ├── topic.py
│   │   │   └── dashboard.py
│   │   │
│   │   ├── schemas/                      # Request/Response schemas
│   │   │   ├── auth.py
│   │   │   ├── student.py
│   │   │   └── test.py
│   │   │
│   │   ├── services/                     # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── student_service.py
│   │   │   ├── test_service.py
│   │   │   └── motors/
│   │   │       ├── bs_model.py           # Spaced repetition
│   │   │       ├── priority_engine.py
│   │   │       ├── difficulty_engine.py
│   │   │       └── time_analyzer.py
│   │   │
│   │   ├── utils/                        # Helper functions
│   │   │   ├── jwt.py
│   │   │   ├── validators.py
│   │   │   └── formatters.py
│   │   │
│   │   └── tests/                        # Unit/integration tests
│   │       ├── test_auth.py
│   │       ├── test_motors.py
│   │       └── test_endpoints.py
│   │
│   ├── migrations/                       # Database migrations
│   │   ├── versions/
│   │   │   ├── 001_initial_schema.sql
│   │   │   ├── 002_add_rls_policies.sql
│   │   │   └── 003_prerequisite_system.sql
│   │   └── README.md
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/                             # ✅ MVP COMPLETE
│   ├── app/
│   │   ├── layout.tsx                    # Root layout
│   │   ├── page.tsx                      # Landing page
│   │   ├── globals.css
│   │   │
│   │   ├── student/
│   │   │   └── dashboard/
│   │   │       ├── page.tsx              # Main dashboard
│   │   │       └── components/
│   │   │           ├── CriticalAlert.tsx
│   │   │           ├── HeroStats.tsx
│   │   │           ├── ActionCards.tsx
│   │   │           ├── TopicHealthBar.tsx
│   │   │           ├── RecoveryModal.tsx
│   │   │           └── DashboardHeader.tsx
│   │   │
│   │   ├── admin/                        # ⚠️ TO BE BUILT
│   │   │   ├── dashboard/
│   │   │   ├── curriculum/
│   │   │   ├── prerequisites/
│   │   │   └── feature-control/
│   │   │
│   │   └── coach/                        # ⚠️ TO BE BUILT
│   │       └── dashboard/
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts                 # Centralized API client
│   │   │   └── endpoints/
│   │   │       ├── auth.ts
│   │   │       ├── student.ts
│   │   │       └── test.ts
│   │   │
│   │   ├── store/
│   │   │   ├── studentDashboardStore.ts  # Zustand store
│   │   │   ├── authStore.ts
│   │   │   └── globalStore.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useDashboard.ts
│   │   │   └── usePolling.ts
│   │   │
│   │   └── utils/
│   │       ├── formatters.ts
│   │       ├── validators.ts
│   │       └── constants.ts
│   │
│   ├── public/
│   │   ├── images/
│   │   └── icons/
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── .env.local.example
│
├── docs/                                 # Documentation
│   ├── API.md                            # API documentation
│   ├── DATABASE.md                       # Schema documentation
│   ├── DEPLOYMENT.md                     # Deployment guide
│   ├── CONTRIBUTING.md                   # Contribution guide
│   └── ARCHITECTURE.md                   # Architecture decisions
│
├── scripts/                              # Automation scripts
│   ├── seed_demo_data.py                 # Demo data seeding
│   ├── backup_database.sh                # Backup automation
│   └── deploy.sh                         # Deployment script
│
├── .github/
│   └── workflows/
│       ├── ci.yml                        # CI pipeline
│       └── deploy.yml                    # CD pipeline
│
├── README.md                             # ✅ CURRENT
├── ENDSTP_MASTER_CONTEXT.md             # ✅ THIS FILE
├── PROGRESS_LOG.md                       # ✅ DAILY UPDATES
├── .gitignore
└── LICENSE
```

### 🔑 Kritik Dosyalar

| Dosya | Amaç | Durum |
|-------|------|-------|
| `backend/app/main.py` | FastAPI entry point | ⚠️ Kurulacak |
| `backend/app/services/motors/bs_model.py` | Unutma eğrisi motoru | ⚠️ Kurulacak |
| `frontend/app/student/dashboard/page.tsx` | Öğrenci dashboard | ✅ Tamamlandı |
| `frontend/lib/api/client.ts` | Centralized API client | ✅ Tamamlandı |
| `frontend/lib/store/studentDashboardStore.ts` | Zustand state | ✅ Tamamlandı |
| `migrations/001_initial_schema.sql` | İlk DB şeması | ⚠️ Yazılacak |

---

## 4. Veri Modeli

### 🗄️ Database Schema (38 Tables)

#### **Core Tables (User & Auth)**

```sql
-- users (Supabase Auth managed)
CREATE TABLE auth.users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- user_profiles
CREATE TABLE public.user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  role TEXT CHECK (role IN ('student', 'coach', 'admin', 'institution')),
  first_name TEXT,
  last_name TEXT,
  subscription_tier TEXT CHECK (tier IN ('free', 'basic', 'medium', 'premium')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### **Curriculum Tables**

```sql
-- subjects (Ders)
CREATE TABLE subjects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name_tr TEXT NOT NULL,
  name_en TEXT,
  code TEXT UNIQUE NOT NULL,
  display_order INT,
  is_active BOOLEAN DEFAULT TRUE
);

-- topics (Konu)
CREATE TABLE topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id UUID REFERENCES subjects(id),
  name_tr TEXT NOT NULL,
  name_en TEXT,
  code TEXT UNIQUE NOT NULL,
  difficulty_level INT CHECK (difficulty_level BETWEEN 1 AND 10),
  estimated_study_minutes INT,
  is_active BOOLEAN DEFAULT TRUE
);

-- prerequisites (Ön Koşul İlişkileri)
CREATE TABLE prerequisites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_id UUID REFERENCES topics(id),          -- Ana konu
  prerequisite_topic_id UUID REFERENCES topics(id),  -- Ön koşul konu
  strength DECIMAL(3,2) CHECK (strength BETWEEN 0 AND 1),  -- 0.1 = weak, 1.0 = strong
  is_mandatory BOOLEAN DEFAULT FALSE,           -- Guidance, not blocker
  created_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES auth.users(id)
);
```

#### **Exam Weight Tables**

```sql
-- exam_types (Sınav Tipleri)
CREATE TABLE exam_types (
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name TEXT NOT NULL,
  system_id INTEGER REFERENCES exam_systems(id),
  total_questions INTEGER NOT NULL,
  total_duration INTEGER,  -- dakika
  description TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- subject_exam_weights (Ders Ağırlıkları)
CREATE TABLE subject_exam_weights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id UUID REFERENCES subjects(id) ON DELETE CASCADE,
  exam_type_id INTEGER REFERENCES exam_types(id) ON DELETE CASCADE,
  question_count INT NOT NULL,
  time_minutes INT,
  weight_multiplier DECIMAL(4,2) DEFAULT 1.0,
  display_order INT DEFAULT 0,
  
  -- Alternative subject logic
  is_alternative BOOLEAN DEFAULT FALSE,
  alternative_group VARCHAR(50),
  alternative_note TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(subject_id, exam_type_id)
);
```

#### **Test & Performance Tables**

```sql
-- test_records (Deneme Kaydı)
CREATE TABLE test_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  test_name TEXT,
  test_date DATE NOT NULL,
  test_type TEXT CHECK (test_type IN ('mock_exam', 'practice', 'daily_quiz')),
  total_questions INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- topic_test_results (Konu Bazlı Sonuçlar)
CREATE TABLE topic_test_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  test_record_id UUID REFERENCES test_records(id),
  topic_id UUID REFERENCES topics(id),
  user_id UUID REFERENCES auth.users(id),
  
  -- Performance metrics
  questions_total INT NOT NULL,
  questions_correct INT NOT NULL,
  questions_wrong INT NOT NULL,
  questions_blank INT NOT NULL,
  
  -- Timing data (crucial for BS-Model)
  time_spent_seconds INT NOT NULL,
  entry_timestamp TIMESTAMPTZ DEFAULT NOW(),  -- Must be within 24h of test_date
  
  -- Derived metrics (calculated by backend)
  success_rate DECIMAL(5,2),  -- (correct / total) * 100
  speed_score DECIMAL(5,2),   -- time_spent / questions_total
  
  -- Motor outputs
  bs_model_score DECIMAL(5,2),
  remembering_rate DECIMAL(5,2),
  priority_score DECIMAL(5,2),
  
  CONSTRAINT unique_user_topic_test UNIQUE(user_id, topic_id, test_record_id)
);
```

#### **Motor-Specific Tables**

```sql
-- bs_model_history (Unutma Eğrisi Geçmişi)
CREATE TABLE bs_model_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  topic_id UUID REFERENCES topics(id),
  
  -- Algorithm parameters
  s_effective DECIMAL(10,5),  -- Effective spacing factor
  last_review_date DATE NOT NULL,
  next_review_date DATE NOT NULL,
  
  -- Decay prediction
  decay_rate DECIMAL(5,2),
  predicted_remembering_rate DECIMAL(5,2),
  
  calculated_at TIMESTAMPTZ DEFAULT NOW()
);

-- priority_calculations (Öncelik Skoru)
CREATE TABLE priority_calculations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  topic_id UUID REFERENCES topics(id),
  
  -- Factors
  recency_score DECIMAL(5,2),
  difficulty_score DECIMAL(5,2),
  prerequisite_impact DECIMAL(5,2),
  goal_alignment_score DECIMAL(5,2),
  
  -- Final score
  final_priority_score DECIMAL(5,2),
  calculated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### **University Goals Tables**

```sql
-- university_tiers (5-Tier System)
CREATE TABLE university_tiers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tier_number INT CHECK (tier_number BETWEEN 1 AND 5),
  name_tr TEXT NOT NULL,
  min_rank INT,
  max_rank INT,
  weight DECIMAL(3,2)  -- Progress calculation weight
);

-- user_university_goals
CREATE TABLE user_university_goals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  tier_id UUID REFERENCES university_tiers(id),
  target_date DATE,
  progress_percentage DECIMAL(5,2),  -- Weighted calculation
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 🔐 Row Level Security (RLS) Strategy

```sql
-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE topic_test_results ENABLE ROW LEVEL SECURITY;

-- Example: Students can only see their own data
CREATE POLICY "Students view own data" 
  ON test_records
  FOR SELECT
  USING (auth.uid() = user_id);

-- Example: Coaches can see their assigned students
CREATE POLICY "Coaches view assigned students"
  ON test_records
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM coach_student_assignments
      WHERE coach_id = auth.uid() AND student_id = test_records.user_id
    )
  );

-- Example: Admins can see everything
CREATE POLICY "Admins view all"
  ON test_records
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );
```

---

## 5. API Sözleşmesi

### 🌐 Base URL

```
Production:  https://api.end-stp.com/api/v1
Staging:     https://staging-api.end-stp.com/api/v1
Local:       http://localhost:8000/api/v1
```

### 🔑 Authentication

**All endpoints require JWT token except:**
- `POST /auth/login`
- `POST /auth/register`
- `POST /auth/forgot-password`

**Header Format:**
```
Authorization: Bearer <access_token>
```

**Token Lifecycle:**
- Access token: 60 minutes
- Refresh token: 7 days
- Auto-refresh when <5 min remaining

---

### 📋 Endpoint List

#### **Authentication Endpoints**

##### `POST /auth/login`
```json
// Request
{
  "email": "student@example.com",
  "password": "SecurePass123"
}

// Response (200 OK)
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid-here",
    "email": "student@example.com",
    "role": "student",
    "subscription_tier": "basic"
  }
}
```

---

## 6. UI Akışları

### 🎨 Öğrenci Dashboard Flow

```
┌───────────────────────────────────────────────────────────┐
│                    STUDENT DASHBOARD                         │
│                   (5 Second Rule)                            │
└───────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌────────────────┐ ┌──────────┐ ┌──────────────┐
     │ Critical Alert │ │ Streak   │ │ Quick Actions│
     │ (RED BOX)      │ │ Badge    │ │ (3 Cards)    │
     └────────────────┘ └──────────┘ └──────────────┘
              │               │               │
              │    What to do FIRST?          │
              └───────────────┼───────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌──────────────────┐  ┌─────────────────┐
        │ TODAY'S TASKS    │  │ TOPIC HEALTH    │
        │ (Prioritized)    │  │ BARS            │
        └──────────────────┘  └─────────────────┘
                    │                   │
                    ▼                   ▼
        ┌─────────────────────────────────────┐
        │     Click Topic → Recovery Modal      │
        │  (Partner Links + Study Resources)    │
        └─────────────────────────────────────┘
```

---

## 7. Project Constitution / Altın Kurallar

### 🌐 GLOBAL-FIRST Prensipler

```
┌───────────────────────────────────────────────────────────┐
│                  GLOBAL-FIRST ARCHITECTURE                   │
│     Every code, API, feature must be globally compatible     │
│              and affiliate-ready from day one                │
└───────────────────────────────────────────────────────────┘
```

**Mandatory Rules:**

1. **Database Naming**
   - Use `_tr` and `_en` suffixes for localized columns
   - Example: `topics.name_tr`, `topics.name_en`
   - NEVER hardcode Turkish-only names

2. **API Responses**
   - Always return both `name_tr` and `name_en`
   - Frontend decides which to display based on user locale

3. **Date/Time Handling**
   - ALL timestamps in UTC in database
   - Convert to user timezone in frontend only
   - Use ISO 8601 format: `2024-12-19T10:30:00Z`

4. **Currency**
   - Store prices in USD as base
   - Display in user's local currency (conversion in frontend)
   - Column naming: `price_usd`, `price_try`, `price_eur`

5. **Affiliate Links**
   - Partner URLs must have `?affiliate_id=` parameter
   - Track clicks in separate table for revenue sharing
   - Never hardcode partner URLs (store in database)

---

### 🔐 Güvenlik Kuralları

**Authentication:**
- NEVER store passwords in plaintext
- Use Supabase Auth (bcrypt hashing)
- JWT tokens with 60-minute expiry
- Refresh tokens with 7-day expiry
- Auto-logout on token expiry

**Authorization:**
- Row Level Security (RLS) enabled on ALL tables
- Role-based access control (RBAC)
- Students: Own data only
- Coaches: Assigned students only
- Admins: Full access with audit logs

**Data Protection:**
- Encrypt sensitive fields (e.g., university goals)
- GDPR compliance: Right to deletion
- Anonymize data after account deletion (keep aggregated stats)
- No PII in log files

**API Security:**
- Rate limiting per tier
- CORS: Whitelist only allowed domains
- SQL injection prevention (Pydantic validation)
- XSS prevention (sanitize all inputs)

---

### ⚡ Performans Kuralları

**Database Optimization:**
- Index on foreign keys automatically (Supabase)
- Add composite indexes for common queries
- Example: `CREATE INDEX idx_user_topic_test ON topic_test_results(user_id, topic_id);`
- Use views for complex joins
- Pagination: ALWAYS use `LIMIT` and `OFFSET`

**API Response Time:**
- Target: <200ms for simple queries
- Target: <500ms for complex dashboard queries
- Use caching for static data (subjects, topics)
- Redis caching for motor calculations (5-minute TTL)

**Frontend Optimization:**
- Lazy load heavy components
- Use Next.js Image component (automatic optimization)
- Debounce search inputs (300ms)
- Polling interval: 30 seconds (not 5 seconds!)
- Zustand for state (avoid prop drilling)

---

### 🌍 Internationalization (i18n) Kuralları

**Code Structure:**
```
frontend/
├── locales/
│   ├── tr/
│   │   ├── common.json
│   │   ├── dashboard.json
│   │   └── errors.json
│   └── en/
│       ├── common.json
│       ├── dashboard.json
│       └── errors.json
```

**Translation Keys:**
```json
// ✅ GOOD: Hierarchical and descriptive
{
  "dashboard": {
    "critical_alert": {
      "title": "Acil Dikkat!",
      "description": "{topicName} konusunu {days} gün içinde unutacaksınız!"
    }
  }
}

// ❌ BAD: Flat and generic
{
  "alert_title": "Uyarı",
  "message": "Bir sorun var"
}
```

---

### 📊 Migration Kuralları

**File Naming Convention:**
```
migrations/
└── versions/
    ├── 001_initial_schema.sql
    ├── 002_add_rls_policies.sql
    ├── 003_prerequisite_system.sql
    ├── 004_add_university_goals.sql
    └── 005_add_motor_history_tables.sql
```

**Migration Template:**
```sql
-- Migration: 003_prerequisite_system
-- Description: Add prerequisite relationships table
-- Author: Team
-- Date: 2024-12-19

-- ============================================
-- UP Migration
-- ============================================

CREATE TABLE prerequisites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
  prerequisite_topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
  strength DECIMAL(3,2) CHECK (strength BETWEEN 0 AND 1),
  is_mandatory BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES auth.users(id)
);

-- ============================================
-- DOWN Migration (Rollback)
-- ============================================

-- DROP TABLE prerequisites;
-- (Commented out for safety, uncomment if needed)

-- ============================================
-- Verification Query
-- ============================================

-- SELECT COUNT(*) FROM prerequisites;
-- Expected: 0 (empty table initially)
```

---

### 🛠 Hata Yönetimi Kuralları

**Error Logging:**
```python
# Use structured logging
import logging
import json

logger = logging.getLogger(__name__)

def log_error(error_type, message, context):
    logger.error(json.dumps({
        "error_type": error_type,
        "message": message,
        "context": context,
        "timestamp": datetime.utcnow().isoformat()
    }))
```

---

### 📝 Kod Yazım Kuralları

**Python (Backend):**
```python
# ✅ GOOD: Type hints, docstrings, clear naming
from typing import Optional, List
from pydantic import BaseModel

async def calculate_remembering_rate(
    user_id: str,
    topic_id: str,
    test_date: date
) -> Optional[float]:
    """
    Calculate remembering rate for a topic using BS-Model.
    
    Args:
        user_id: UUID of the student
        topic_id: UUID of the topic
        test_date: Date of the test
        
    Returns:
        Remembering rate (0-100) or None if insufficient data
    """
    pass
```

---

### 🧪 Testing Kuralları

**Backend Tests:**
```python
# tests/test_bs_model.py

import pytest
from app.services.motors.bs_model import calculate_remembering_rate

@pytest.mark.asyncio
async def test_remembering_rate_calculation():
    """Test BS-Model calculation with known inputs"""
    user_id = "test-user-uuid"
    topic_id = "test-topic-uuid"
    test_date = date(2024, 12, 19)
    
    result = await calculate_remembering_rate(user_id, topic_id, test_date)
    
    assert result is not None
    assert 0 <= result <= 100
    assert isinstance(result, float)
```

---

### ⚖️ Exam Weight System Rules (Sınav Ağırlık Sistemi)

#### **RULE 1: Single Source of Truth - Merkezi Toplam**

```
KAYNAK                      AMAÇ                    ÖRNEK
────────────────────────────────────────────────────────────────
exam_types.total_questions  Gerçek soru sayısı      TYT = 120
subject_exam_weights        Dağılım/analiz          Matematik: 40
topics/test_records         Öğrenci performans      Test sonuçları
```

**KRİTİK KURAL:**
```sql
-- ❌ YANLIŞ (asla yapma)
SELECT SUM(question_count) FROM subject_exam_weights WHERE exam_type_id = 1;
-- Bu 120 olmayabilir! (seçmeli dersler yüzünden)

-- ✅ DOĞRU (her zaman)
SELECT total_questions FROM exam_types WHERE code = 'TYT';
-- Bu her zaman 120'dir (merkezi kaynak)
```

**Sebep:**
- Seçmeli dersler → SUM(question_count) > total_questions
- Merkezi otorite (ÖSYM) toplam soru sayısını belirler
- Dersler sadece dağılım gösterir

---

#### **RULE 2: Alternative Subjects (Seçmeli Dersler)**

**Gerçek Hayat Örneği - ÖSYM TYT Sosyal (20 soru):**

```
┌─────────────────────────────────────────────┐
│ ZORUNLU (15 soru)                           │
├─────────────────────────────────────────────┤
│ Tarih:     5 soru                           │
│ Coğrafya:  5 soru                           │
│ Felsefe:   5 soru                           │
├─────────────────────────────────────────────┤
│ SEÇMELİ (5 soru) - Birini seç              │
├─────────────────────────────────────────────┤
│ ○ Din Kültürü:  5 soru                      │
│ ○ Ek Felsefe:   5 soru                      │
└─────────────────────────────────────────────┘
Toplam: 20 soru (SABİT)
```

**Database Model:**

```sql
-- subject_exam_weights tablosu
ALTER TABLE subject_exam_weights
ADD COLUMN is_alternative BOOLEAN DEFAULT FALSE,
ADD COLUMN alternative_group VARCHAR(50),
ADD COLUMN alternative_note TEXT;

-- Örnek kayıt
UPDATE subject_exam_weights
SET 
  is_alternative = TRUE,
  alternative_group = 'TYT_SOCIAL_OPTIONAL',
  alternative_note = 'Öğrenci Felsefe veya Din Kültürü soruları çözer'
WHERE subject_id = (SELECT id FROM subjects WHERE code = 'DIN')
  AND exam_type_id = (SELECT id FROM exam_types WHERE code = 'TYT');
```

**Global-First Examples:**

| Sınav Sistemi | Seçmeli Ders | Alternative Group |
|---------------|--------------|-------------------|
| ÖSYM TYT | Din Kültürü | TYT_SOCIAL_OPTIONAL |
| ÖSYM TYT | Ek Felsefe | TYT_SOCIAL_OPTIONAL |
| SAT | Math Level 2 | SAT_MATH_OPTIONAL |
| SAT | Math Level 1 | SAT_MATH_OPTIONAL |
| A-Level | Further Maths | ALEVEL_MATH_OPTIONAL |
| A-Level | Statistics | ALEVEL_MATH_OPTIONAL |
| IB | HL History | IB_GROUP3_OPTIONAL |
| IB | HL Economics | IB_GROUP3_OPTIONAL |

**Aynı gruptaki dersler birbirinin alternatifidir!**

---

#### **RULE 3: Admin Panel Management (Phase 4)**

**Current State (MVP):**
- SQL ile manuel set edilir
- Supabase SQL Editor kullanılır
- Hızlı çözüm, production-ready değil

**Future State (Phase 4 - Admin Panel):**

```
Admin Dashboard
└─ Exam Weight Management
   ├─ Subject Weight Editor (visual, grid-based)
   │   ├─ Question count (editable)
   │   ├─ is_alternative (checkbox)
   │   └─ alternative_group (dropdown)
   │
   ├─ Approval Workflow (Two-Person Rule)
   │   ├─ Pending changes queue
   │   ├─ Diff view (old vs new)
   │   └─ Approve/Reject buttons
   │
   ├─ Audit Log
   │   ├─ Who changed what
   │   ├─ When
   │   └─ Rollback capability
   │
   └─ Global Templates
       ├─ ÖSYM (Turkey)
       ├─ SAT (USA)
       ├─ A-Level (UK)
       └─ IB (International)
```

**Why Admin Panel?**

1. **Global-First Requirement:**
   - 100+ ülke, her birinin farklı sınav sistemi
   - ÖSYM kuralları politika kararıyla değişebilir
   - Scalability: SQL bilgisi gerektirmemeli

2. **Security:**
   - Two-Person Rule (Güneş Security Protocol)
   - Comprehensive audit log
   - Emergency rollback

3. **Operational Excellence:**
   - Curriculum team SQL bilmeden yönetebilir
   - Değişiklikler anında production'a yansır
   - A/B testing için farklı konfigürasyonlar

---

#### **RULE 4: Priority Score Integration (Future)**

**Exam weight multiplier:**

```python
# Backend: progress.py
for subject in subjects:
    # ... mevcut priority_score hesaplama
    
    # Exam weight multiplier
    weight_result = supabase.table("subject_exam_weights").select(
        "question_count"
    ).eq("subject_id", subject['subject_id']).execute()
    
    exam_multiplier = 1.0
    if weight_result.data:
        total_weight = sum(w['question_count'] for w in weight_result.data)
        # Normalize: 5-80 soru arası → 0.5x-2.0x çarpan
        exam_multiplier = min(2.0, max(0.5, total_weight / 40.0))
    
    subject['priority_score'] *= exam_multiplier
```

**Örnek:**
- Matematik (TYT:40 + AYT:40 = 80 soru) → 2.0x çarpan
- Tarih (TYT:5 soru) → 0.5x çarpan
- Fizik (TYT:7 + AYT:14 = 21 soru) → 1.05x çarpan

---

#### **RULE 5: Data Integrity (Analytics Integrity Triangle)**

```
┌─────────────────────────────────────────────┐
│     ANALYTICS INTEGRITY TRIANGLE            │
├─────────────────────────────────────────────┤
│                                             │
│         exam_types.total_questions          │
│         (Merkezi kaynak, değişmez)          │
│                    △                        │
│                   ╱ ╲                       │
│                  ╱   ╲                      │
│                 ╱     ╲                     │
│                ╱       ╲                    │
│   subject_exam_weights   test_records      │
│   (Dağılım tanımı)       (Gerçek veri)     │
│                                             │
└─────────────────────────────────────────────┘
```

**3 Kontrol Noktası:**

1. **exam_types kontrolü:**
```sql
-- Her sınav tipinin total_questions değeri tanımlı olmalı
SELECT code, total_questions 
FROM exam_types 
WHERE total_questions IS NULL;
-- Beklenen: 0 satır
```

2. **subject_exam_weights kontrolü:**
```sql
-- Seçmeliler hariç, toplam mantıklı olmalı
SELECT 
  et.code,
  et.total_questions as merkezi,
  SUM(sew.question_count) as dersler
FROM exam_types et
LEFT JOIN subject_exam_weights sew ON et.id = sew.exam_type_id
GROUP BY et.code, et.total_questions;
-- Not: dersler >= merkezi (seçmeliler yüzünden)
```

3. **test_records kontrolü:**
```sql
-- Öğrenci girişleri mantıklı mı?
SELECT 
  COUNT(*) as anomaly_count
FROM test_records tr
JOIN exam_types et ON tr.exam_type_id = et.id
WHERE tr.total_questions_answered > et.total_questions;
-- Beklenen: 0 (öğrenci sınav toplamından fazla soru çözemez)
```

---

#### **CRITICAL NOTES**

**⚠️ DO:**
- exam_types.total_questions'ı merkezi kaynak olarak kullan
- Seçmeli dersler için is_alternative kullan
- Admin Panel değişiklikleri için Two-Person Rule uygula
- Audit log'u mutlaka tut

**❌ DON'T:**
- SUM(question_count) = total_questions eşitliği bekleme
- Manuel SQL ile production'da değişiklik yapma (MVP hariç)
- Seçmeli mantığı subject sayısı ile belirlemeye çalışma
- Alternative group'ları hardcode etme (database'de tut)

**🌍 GLOBAL-FIRST:**
Her ülke/sınav sistemi için:
- exam_types → Kendi sınav tiplerini tanımlar
- subject_exam_weights → Kendi ders dağılımını belirler
- is_alternative → Kendi seçmeli mantığını kurar

---

## 8. Faz Planı

### 🚀 Faz 1: MVP (Weeks 1-4) - **80% Complete**

**Week 1: ✅ COMPLETED**
- [x] Frontend setup (Next.js 14, Tailwind, Zustand)
- [x] Student Dashboard UI (full design)
- [x] Mock data integration
- [x] Responsive design
- [x] Gamification elements (streak, badges)

**Week 2: Current Focus**
- [ ] Backend initialization (FastAPI)
- [ ] Database migrations (initial schema)
- [ ] Supabase setup + RLS policies
- [ ] Authentication endpoints (login/logout/refresh)
- [ ] Student dashboard API endpoint
- [ ] Test entry endpoint

**Week 3: Integration**
- [ ] Connect frontend to real API
- [ ] Replace mock data with database queries
- [ ] Implement JWT token management
- [ ] Real-time dashboard polling
- [ ] Error handling and loading states
- [ ] Form validation

**Week 4: Testing & Deployment**
- [ ] Unit tests (backend)
- [ ] Integration tests (API)
- [ ] E2E tests (critical user flows)
- [ ] Performance testing (load testing)
- [ ] Deploy to staging
- [ ] UAT (User Acceptance Testing)
- [ ] Deploy to production

---

## 9. Known Issues / Gotchas

### 🛠 Recent Fixes (2024-12-24)

#### **ISSUE-001: Fizik Subject Duplicates (RESOLVED)**
**Status**: ✅ RESOLVED  
**Date**: Dec 24, 2024

**Problem:**
- 3 Fizik subjects existed (physics_basics, physics, FIZ)
- TYT total showed 127 questions (should be 120)
- NULL subject in exam weights caused silent error

**Solution:**
- Merged all topics under single FIZ subject
- Removed NULL subject_id from exam weights
- Verified all exam totals: TYT=120, AYT=80

---

## 10. Çalıştırma Rehberi

### 🖥️ Local Development Setup

#### **Prerequisites:**
- **Node.js**: v20.19.5+
- **Python**: 3.10.12+
- **PostgreSQL**: 15+ (or use Supabase)
- **Git**

---

### 📦 Frontend Setup

```bash
# 1. Clone repository
git clone https://github.com/your-org/end-stp-project.git
cd end-stp-project/frontend

# 2. Install dependencies
npm install

# 3. Setup environment variables
cp .env.local.example .env.local

# Edit .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key

# 4. Run development server
npm run dev

# Frontend now running at: http://localhost:3000
```

---

### ⚙️ Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env

# Edit .env:
DATABASE_URL=postgresql://postgres:password@localhost:5432/endstp
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# 5. Run development server
uvicorn app.main:app --reload --port 8000

# Backend now running at: http://localhost:8000
```

---

## 📄 Document Maintenance

**This document should be updated when:**
- New features are added
- Architecture changes
- New gotchas discovered
- Migration issues encountered
- API endpoints modified

**Version History:**
- v1.1 (Dec 24, 2024): Added Exam Weight System Rules
- v1.0 (Dec 19, 2024): Initial comprehensive documentation

**Maintainers:**
- Lead Dev: [Name]
- Backend: [Name]
- Frontend: [Name]
- DevOps: [Name]

---

## 🎯 Quick Reference

### **One-Line Commands:**

```bash
# Start everything (run in separate terminals)
cd frontend && npm run dev                          # Terminal 1
cd backend && uvicorn app.main:app --reload         # Terminal 2

# Build for production
cd frontend && npm run build && npm start           # Terminal 1
cd backend && gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker  # Terminal 2

# Run tests
cd frontend && npm run test                         # Frontend
cd backend && pytest                                # Backend

# Deploy
vercel --prod                                       # Frontend
git push origin main                                # Backend (auto-deploy)
```

---

**🎉 End of Master Context Documentation**

> **Remember:** This document is the **single source of truth** for the End.STP project. Keep it updated, refer to it often, and use it to onboard new team members.

**Target:** Global Top 5 EdTech Analytics Platform by March 14, 2025  
**Status:** 80% MVP Complete, 11 Weeks to Launch  
**Principle:** GLOBAL-FIRST, every code must be internationally ready from day one

---

**"End.STP does not fix learning by rewinding, it fixes learning by revealing where progress slows."**
