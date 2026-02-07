# 📘 End.STP Master Context Documentation

> **Version**: 1.1  
> **Last Updated**: December 30, 2024  
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
### Context Layer Migration Status

**Phase 1: Mini Migration (Mathematics)**
- ✅ Format v1.0 LOCKED (2024-12-30)
- ✅ 1st Batch: 5 topics (Temel Kavramlar, Denklemler, Fonksiyonlar, Üslü-Köklü, Polinomlar)
- 🔄 2nd Batch: 5 topics (planned)
- 📅 Target: 15-20 topics/week

**Database:**
- Table: topic_contexts (JSONB)
- Schema: Adapted to real production structure
- Foreign Keys: topics(id) → topic_contexts(topic_id)
---

**🎉 End of Master Context Documentation**

> **Remember:** This document is the **single source of truth** for the End.STP project. Keep it updated, refer to it often, and use it to onboard new team members.

**Target:** Global Top 5 EdTech Analytics Platform by March 14, 2025  
**Status:** 80% MVP Complete, 11 Weeks to Launch  
**Principle:** GLOBAL-FIRST, every code must be internationally ready from day one

---

**"End.STP does not fix learning by rewinding, it fixes learning by revealing where progress slows."**
# End.STP Master Context - Motor v2 Update

## Recent Changes (2025-01-05)

### Motor v2 Context Integration
All v2 motors now use ContextService for enhanced calculations.

#### New Components
1. **ContextService** (`app/core/context_service.py`)
   - Centralized context provider
   - Methods: get_topic_context, get_student_history, get_prerequisites
   - 5-minute cache for performance

2. **Context-Aware Motors**
   - BS-Model v2: Uses archetype, student history
   - Difficulty v2: Uses baseline difficulty, prerequisites
   - Priority v2: Context-enhanced prioritization
   - Time v2: Student pattern analysis

#### Key Fixes
- .env loading at application startup (main.py)
- JWT service_role validation
- Supabase admin client architecture
- Production-ready error handling

#### Testing
All motors tested with real data:
```bash
curl -X POST "http://localhost:8000/api/v1/motors/bs-model/calculate?topic_id=UUID&correct=9&incorrect=2&blank=1&total=12&user_tier=premium"
```
Response includes v2_features with context data.

#### Files Modified
- app/main.py: .env loading
- app/db/session.py: JWT validation
- app/core/context_service.py: Complete implementation
- All v2 motor files: Context integration

#### Git Tag
v2.0.0-context-stable

#### Next Steps
1. Frontend integration (3-5 days)
2. Production deployment preparation
3. Beta testing with real students

---
📜 A4.2 — SIGNAL LIFECYCLE CONTRACT

(Birth → Escalation → Resolution)

Bu doküman, End.STP’de bir sinyalin
nasıl doğduğunu,
nasıl büyüdüğünü,
ne zaman sustuğunu tanımlar.

🎯 AMAÇ

Sonsuz retry döngülerini engellemek

“Bir kere oldu” ile “sistemik problem”i ayırmak

Koçu gereksiz alarmlardan korumak

Kuruma trend, geliştiriciye kök neden vermek

🧬 SIGNAL LIFECYCLE FAZLARI
1️⃣ BIRTH — Doğuş

Bir sinyal ancak şu şartlarla doğar:

Tanımlı bir Event Pattern tetiklenmişse

Threshold resmî registry’de varsa

Event tek başına değil, bağlamla gelmişse

Örnek:

Event:
- error_code = 1004
- mouse_idle = 45s
- active_module = "TestEntry"


➡️ S01_CognitiveLock BIRTH

📌 Kural:

Tekil event = log
Pattern = signal

2️⃣ OBSERVATION — İzleme

Sinyal doğduktan sonra:

UI değişmez

Kullanıcı uyarılmaz

Sistem sadece saymaya başlar

Örnek:

Retry_Count = 1
Retry_Count = 2


📌 Kural:

Observation fazında hiçbir aksiyon yoktur.

3️⃣ ESCALATION — Yükselme

Aşağıdaki durumlardan biri olursa sinyal yükselir:

Aynı sinyal N kez tekrar ederse

Süre eşiği aşılırsa

Başka bir sinyalle çakışırsa

Örnek:

S02_SystemFriction + S07_IdleWarning


➡️ Escalation Level 2

📌 Kural:

Escalation = Visibility artar
Ama owner değişmez

4️⃣ ACTION — Müdahale

Bu noktada kim ne yapar A3 kontratına göre belirlenir.

Owner	Aksiyon
Sistem	Retry / Degrade / Stop
Koç	İletişim / Müdahale
Kurum	İnceleme / Altyapı
Öğrenci	Dolaylı mesaj

📌 Kural:

Aynı sinyal için iki farklı owner aksiyon alamaz

5️⃣ RESOLUTION — Çözülme

Bir sinyal ancak şu şekilde kapanır:

Başarılı aksiyon sonrası

Manuel override (koç / sistem)

Timeout + “non-reproducible” etiketi

Resolution meta’sı:

resolved_by = system | coach | timeout
time_to_resolution = X


📌 Kural:

Kapanmayan sinyal = teknik borç

6️⃣ LEARNING — Öğrenme (Pasif)

Sinyal kapandıktan sonra:

Retry başarısı

Kullanıcı davranış değişimi

Drop-out gerçekleşti mi?

➡️ Model beslenir, UI değişmez.

📌 Kural:

Öğrenme asla kullanıcıyı etkileyemez.

🚫 YASAKLAR (DEĞİŞMEZ)

Signal doğmadan aksiyon alınamaz

Signal çözülmeden UI normale dönemez

Öğrenci teknik terim göremez

Kurum bireysel sinyal göremez

Retry başarısızlığı sessizce yutulamaz

📌 EK — A3 ANAYASA ÖZETİ (BURAYI DA EKLE)

Signal owner değiştirilemez

Visibility genişletilemez

Öğrenci teknik sinyal görmez

Kurum bireysel davranış görmez

Koç, skor değil bağlam görür

✅ A5 — Telemetry Event Taxonomy (Raw Event Contract)

Amaç:
Signal Registry (A1–A4) yorum yapmaz, tahmin etmez, duygu üretmez.
Onu besleyen şey çıplak, tartışmasız, zaman damgalı olaylardır (raw events).

Bu yüzden A5 = sistemin sinir uçlarıdır.
Burada hata yaparsak:

Signal yanlış çıkar

Insight süs olur

Coach Panel “hikâye anlatır” ama aksiyon üretemez

1️⃣ Temel İlke (Anayasa Maddesi)

A5.1 — Raw Event Altın Kuralı
“Bir event, yorum içermez.
Sadece ne oldu, nerede oldu, ne zaman oldu, hangi bağlamda oldu bilgisini taşır.”

❌ Yanlış (yorumlu):

user_frustrated = true

✅ Doğru (ham):

mouse_idle_ms = 45000
retry_count = 3
backend_timeout_ms = 8200

2️⃣ Event Taxonomy v1 — Ana Sınıflar

Bu sınıflar değişmez.
Alt event’ler artar ama bu çatı sabittir.

A5 Event Domains (v1)
├─ SYSTEM_EVENT        (altyapı / backend / network)
├─ UI_EVENT            (tıklama, bekleme, render)
├─ SESSION_EVENT       (başlangıç, bitiş, süre)
├─ INPUT_EVENT         (form, test, veri girişi)
├─ NAVIGATION_EVENT    (sayfa geçişi, geri dönüş)
├─ MOTOR_EVENT         (analiz, retry, fail, success)
└─ COACH_EVENT         (ileride – müdahale, mesaj)


⚠️ Uyarı (senin istediğin türden):
Eğer “duygu” veya “motivasyon” başlığı eklemek istersek → AŞIRI ERKEN.
Duygu event değildir, signal çıktısıdır.
Şimdi eklemek kolon çatlatır.

3️⃣ Event Contract (Zorunlu Alanlar)

Her event aynı iskeleti taşır.
Bu teknik kontrattır.

TelemetryEvent {
  event_id: uuid
  event_type: string        // SYSTEM_TIMEOUT, UI_CLICK, INPUT_SUBMIT
  event_domain: string      // SYSTEM | UI | INPUT | SESSION | MOTOR
  timestamp: iso8601
  user_id?: uuid
  session_id?: uuid
  page?: string
  component?: string
  context: {
    [key: string]: number | string | boolean | null
  }
}


Anayasa Maddesi:
“Context alanı serbesttir ama boş olamaz.”

4️⃣ Örnek Raw Event’ler (v1)
🔧 SYSTEM_EVENT
{
  "event_type": "BACKEND_TIMEOUT",
  "event_domain": "SYSTEM",
  "timestamp": "2026-01-18T10:42:11Z",
  "context": {
    "endpoint": "/student/dashboard",
    "timeout_ms": 8200,
    "retry_count": 2
  }
}

🖱️ UI_EVENT
{
  "event_type": "MOUSE_IDLE",
  "event_domain": "UI",
  "timestamp": "2026-01-18T10:42:30Z",
  "context": {
    "idle_ms": 45000,
    "last_action": "click_submit"
  }
}

🧠 INPUT_EVENT
{
  "event_type": "FORM_SUBMIT",
  "event_domain": "INPUT",
  "timestamp": "2026-01-18T10:43:01Z",
  "context": {
    "form_name": "TestEntry",
    "filled_fields": 9,
    "total_fields": 12
  }
}

🤖 MOTOR_EVENT
{
  "event_type": "MOTOR_RETRY",
  "event_domain": "MOTOR",
  "timestamp": "2026-01-18T10:43:10Z",
  "context": {
    "motor": "BS_MODEL_V2",
    "retry_index": 3,
    "reason": "insufficient_data"
  }
}

5️⃣ Event → Signal Ayrımının Netliği
Katman	Ne yapar	Ne yapmaz
Event (A5)	Ölçer	Yorumlamaz
Signal (A1–A4)	Desen çıkarır	UI mesajı üretmez
Insight (B)	Aksiyon önerir	Ham veri toplamaz

🔒 Bu ayrım bozulursa L5 çöker.

6️⃣ Supabase / DB Konusu (sorduğun kritik soru)

ŞU AN:

❌ Supabase’e yazmıyoruz

❌ Fiziksel tablo açmıyoruz

ŞU AN YAPTIĞIMIZ:

✅ Sözleşme yazıyoruz

✅ Anayasa oluşturuyoruz

✅ .md dokümantasyon üretiyoruz

Neden?
Çünkü:

“Yanlış tasarlanmış bir telemetry tablosu, hiç telemetry olmamasından daha kötüdür.”

DB’ye geçiş:

A6 veya B1.1’de

Retention, sampling, privacy kararlarıyla birlikte

7️⃣ Bu Bölümü MD’ye Nasıl Eklemelisin?

Benim önerim:

docs/
 └─ ENDSTP_TECH_CONSTITUTION.md
     ├─ A1_Error_Severity_Dictionary
     ├─ A4_Signal_Lifecycle
     └─ A5_Telemetry_Event_Taxonomy   👈 buraya birebir yapıştır

     🧠 A6 — Event → Signal Mapping Rules

(Raw Event’ten Anlamlı Sinyale Geçiş Kontratı)

0️⃣ Amaç ve Konum

A6’nın görevi:
Ham event’leri yorumlamadan, kural bazlı, tekrar edilebilir biçimde Signal Registry (A1–A4) ile eşleştirmek.

A6:

UI değildir

Insight değildir

Koçluk dili kullanmaz

A6 = mantık katmanı

1️⃣ Anayasa Maddesi — Mapping’in Altın Kuralı

A6.1 — Deterministik Olma Zorunluluğu
Aynı event dizisi → her zaman aynı signal üretmelidir.

❌ ML, tahmin, olasılık
❌ “Bana göre”
❌ “Kullanıcı sinirli olabilir”

✅ Eşik
✅ Süre
✅ Sayı
✅ Tekrar

2️⃣ Mapping Yapısı (Teknik Kontrat)

Her mapping 4 parçadan oluşur:

EVENT_PATTERN
→ CONDITION
→ SIGNAL_TYPE
→ SEVERITY


Bunlardan biri eksikse mapping geçersizdir.

3️⃣ EVENT_PATTERN (Girdi Tanımı)

Event’ler tekil veya kombinasyon olabilir.

Tek Event Pattern
event_type: BACKEND_TIMEOUT

Kombine Event Pattern
events:
  - BACKEND_TIMEOUT
  - MOTOR_RETRY


⚠️ Uyarı:
Event sırası önemliyse açıkça belirtilmelidir.

4️⃣ CONDITION (Eşik Mantığı)

Condition sayısal ve ölçülebilir olmak zorundadır.

conditions:
  retry_count >= 3
  timeout_ms > 5000


❌ “çok fazla”
❌ “uzun süre”
❌ “sık sık”

5️⃣ SIGNAL_TYPE (A1 Registry’den)

Signal önceden tanımlı olmak zorundadır.

TECHNICAL_BLOCKAGE
FOCUS_DEGRADATION
SYSTEM_INSTABILITY


📌 Yeni signal gerekiyorsa:

Önce A1 Signal Registry güncellenir

Sonra A6’ya eklenir
Tersi yasaktır

6️⃣ SEVERITY (A2 ile birebir)

Severity mapping sırasında atanır, sonradan değişmez.

LOW
MEDIUM
HIGH
CRITICAL

7️⃣ Örnek Mapping Kuralları (v1)
🔴 Teknik Blokaj
rule_id: MAP-001
event_pattern:
  - BACKEND_TIMEOUT
conditions:
  timeout_ms > 7000
signal:
  type: TECHNICAL_BLOCKAGE
  severity: CRITICAL

🟠 Odak Kaybı
rule_id: MAP-002
event_pattern:
  - MOUSE_IDLE
conditions:
  idle_ms >= 45000
signal:
  type: FOCUS_DEGRADATION
  severity: MEDIUM

🔴 Pes Etme Riski (Drop-out Precursor)
rule_id: MAP-003
event_pattern:
  - BACKEND_TIMEOUT
  - MOTOR_RETRY
conditions:
  retry_count >= 3
signal:
  type: DROP_OUT_RISK
  severity: HIGH

8️⃣ Zaman Penceresi (Windowing) Kuralı

A6.4 — Event Zaman Bağlamı Zorunludur

window:
  duration: 10m
  scope: session


Anlamı:

Son 10 dakika

Aynı session içinde

❌ Sınırsız geçmiş
❌ Tüm kullanıcı ömrü

9️⃣ Signal Üretim Sıklığı (Anti-Spam Kuralı)

A6.5 — Aynı signal, aynı session’da yalnızca 1 kez yükseltilir

Ama:

Severity artabilir

Yeni event → yeni değerlendirme

🔒 10️⃣ Yasaklar (Net ve Sert)

🚫 Event olmadan Signal üretmek
🚫 UI mesajına göre Signal üretmek
🚫 Koç yorumuna göre Signal üretmek
🚫 Signal’i retroaktif silmek

11️⃣ A6’nın Sistemdeki Yeri
[ Raw Event ]
      ↓
[ A6 Mapping Rules ]
      ↓
[ Signal Registry (A1–A4) ]
      ↓
[ Insight Pipeline (B) ]


Bu zincirin tek kırılma noktası A6’dır.
🔐 A6.1.1 — Mapping Versioning

(Event → Signal Kurallarının Evrim Kontratı)

Amaç

Mapping kuralları canlı organizmadır, ama asla geçmişi bozamaz.

Bu bölüm:

Geriye dönük analizlerin bozulmasını,

Koç raporlarının “bugün başka, yarın başka” olmasını,

Sistem davranışının izlenemez hale gelmesini
engellemek için zorunludur.

Anayasa Maddesi

A6.1.1.1 — Her Mapping Kuralı Versiyonludur

Hiçbir mapping versiyonsuz tanımlanamaz.

rule_id: MAP-003
version: 1.0.0

Versiyonlama Kuralları (SemVer Benzeri)
MAJOR.MINOR.PATCH

PATCH (1.0.1)

Threshold değişimi

Süre ayarı

Aynı sinyal, aynı mantık

MINOR (1.1.0)

Yeni condition eklendi

Yeni event kombinasyonu

Aynı signal type

MAJOR (2.0.0)

Signal type değişti

Severity anlamı değişti

Mapping mantığı kırıldı

Geçmişe Etki Kuralı

A6.1.1.2 — Mapping Version’ı Signal ile birlikte saklanır

{
  "signal_type": "DROP_OUT_RISK",
  "severity": "HIGH",
  "mapping_rule": "MAP-003",
  "mapping_version": "1.0.0"
}


📌 Bu sayede:

6 ay sonra bile neden o karar verilmiş görülebilir

Sistem kendini savunabilir

Deprecated Mapping Davranışı

A6.1.1.3 — Deprecated Mapping Silinmez

status: deprecated
replaced_by: MAP-007@2.0.0


Eski veriler okunur

Yeni event’ler yeni mapping ile işlenir

⚔️ A6.2 — Conflict Resolution

(Birden Fazla Signal Çakışırsa Ne Olur?)

Problem Tanımı

Aynı zaman penceresinde:

TECHNICAL_BLOCKAGE (HIGH)

FOCUS_DEGRADATION (MEDIUM)

DROP_OUT_RISK (HIGH)

hangisi “gerçek durumdur”?

Anayasa Maddesi

A6.2.1 — Conflict Varsayılanı: Hepsi Geçerlidir

❌ Signal bastırılmaz
❌ Signal silinmez
❌ Signal “önemsiz” sayılmaz

Ama…

1️⃣ Signal Priority Matrix (Zorunlu)
Signal Category	Priority
SYSTEM / TECHNICAL	1 (En Yüksek)
BEHAVIORAL	2
COGNITIVE	3
MOTIVATIONAL	4

A6.2.2 — Yüksek priority, Insight üretiminde önce ele alınır

2️⃣ Severity Tie-Breaker

Aynı priority’de:

CRITICAL > HIGH > MEDIUM > LOW

3️⃣ Root-Cause Locking (ÇOK KRİTİK)

A6.2.3 — Teknik Signal varken Davranışsal Signal “semptom” sayılır

Örnek:

BACKEND_TIMEOUT → TECHNICAL_BLOCKAGE

MOUSE_IDLE → FOCUS_DEGRADATION

➡️ Odak kaybı neden değil, sonuçtur.

Bu bilgi Insight katmanına işaretlenir:

{
  "signal": "FOCUS_DEGRADATION",
  "derived_from": "TECHNICAL_BLOCKAGE"
}

4️⃣ Conflict Resolution ÇIKTISI

A6’nın çıktısı tek signal değildir.

{
  "primary_signal": "TECHNICAL_BLOCKAGE",
  "secondary_signals": ["FOCUS_DEGRADATION"],
  "suppressed": []
}


Suppressed yalnızca UI seviyesinde olabilir, sistem seviyesinde ASLA.

5️⃣ Yasaklar

🚫 “En yükseği al, diğerlerini at”
🚫 UI’daki hataya bakıp conflict çözmek
🚫 Coach yorumuyla signal bastırmak

A6 TAMAMLANDI

Bu noktada sistem artık şunu yapabiliyor:

Event’i tanıyor

Kurala bağlıyor

Versiyonunu biliyor

Çakışmayı çözüyor

Ama hâlâ aksiyon yok.

🚀 B1.1 — Signal → Insight Transformation Rules

(Sinyali Anlamlı Aksiyona Dönüştürme Kontratı)

Amaç

Signal = “Ne oluyor?”
Insight = “Ne yapılmalı?”

B1.1, sistemin koç gibi düşünmeye başladığı ilk noktadır.

Anayasa Maddesi

B1.1.1 — Insight, Signal’den türetilir; asla doğrudan Event’ten değil

Event ❌ → Insight
Signal ✅ → Insight

Insight Tanımı (Zorunlu Alanlar)
{
  "insight_id": "INS-021",
  "signal_type": "DROP_OUT_RISK",
  "audience": "COACH",
  "urgency": "HIGH",
  "action_class": "INTERVENTION_REQUIRED",
  "message_template": "Öğrenci teknik sebeplerle ilerleyemiyor.",
  "expires_in": "48h"
}

Audience Katmanı (Çok Kritik)
Audience	Amaç
STUDENT	Ayna / destek
COACH	Müdahale
INSTITUTION	Trend
SYSTEM	Self-healing

B1.1.2 — Aynı Signal, birden fazla Audience için farklı Insight üretir

Insight Üretim Kuralı
Signal + Context + Policy → Insight


Context yoksa:

Insight ERTELENİR

Uydurulmaz

İlk Örnek
Signal
DROP_OUT_RISK (HIGH)

Insight (COACH)
"Öğrenci son 10 dk içinde 3 kez teknik hata yaşadı ve işlemi yarım bıraktı."

Insight (STUDENT)
"Sistemde kısa bir yavaşlama yaşanıyor. İstersen 5 dk mola verelim."

Bu Aşamada Yapmadıklarımız

❌ UI mesajları
❌ Bildirim gönderme
❌ Koç ekranı

Bunlar B2 ve B3.
🔁 B1.2 — Retry Policy Matrix (Signal-Aware Retry)
Amaç

Retry bir “yama” değildir.
Retry, kontrollü bir sistem refleksidir.

Bu bölüm:

Kör retry’ları yasaklar

Retry’ı Signal bağlamına bağlar

Öğrenciyi yormadan, sistemi kendini iyileştirebilir hale getirir

Observability için neden-sonuç üretir

Anayasa Maddesi

B1.2.1 — Retry kararı Event’e göre değil, Signal’e göre verilir

Event ❌ → Retry
Signal ✅ → Retry

Retry Türleri (Standartlaştırılmış)
Retry Type	Tanım
NONE	Asla retry yapılmaz
SILENT	Kullanıcı fark etmez
BACKOFF	Giderek artan bekleme
ESCALATED	Retry + Insight
CIRCUIT_BREAK	Retry durdurulur
Retry Karar Girdileri (Zorunlu)
signal_type
signal_severity
signal_category
retry_count
time_window
audience

🔢 Retry Policy Matrix (v1)
Signal Type	Severity	Retry Type	Max Retry	Delay Strategy	UI Davranışı
SESSION_NOT_READY	LOW	SILENT	3	500ms → 1s → 2s	Loading
BACKEND_TIMEOUT	MEDIUM	BACKOFF	3	1s → 3s → 6s	Loading
BACKEND_TIMEOUT	HIGH	ESCALATED	2	2s → 5s	Loading → Soft Warn
TECHNICAL_BLOCKAGE	CRITICAL	CIRCUIT_BREAK	0	—	Error + Insight
FOCUS_DEGRADATION	MEDIUM	NONE	0	—	UI Ayna
DROP_OUT_RISK	HIGH	ESCALATED	1	3s	Insight (Coach)
1️⃣ Silent Retry Kuralları

B1.2.2 — Silent Retry sadece sistem bootstrap ve geçici durumlar içindir

Örnek:

SESSION_NOT_READY

TOKEN_REFRESH_PENDING

📌 Kurallar:

UI sadece “Yükleniyor” görür

Retry sayısı loglanır

Öğrenciye hata gösterilmez

2️⃣ Backoff Retry Kuralları

B1.2.3 — Backoff zorunludur (sabit retry yasak)

delay = base * 2^retry_count


Örnek:

1s → 2s → 4s → STOP

3️⃣ Escalated Retry (Kritik Nokta)

B1.2.4 — Retry başarısız olursa Insight üretilir

Yani:

Retry biter

Signal escalate edilir

Coach / System bilgilendirilir

{
  "retry_exhausted": true,
  "signal_escalated": true
}

4️⃣ Circuit Break Rule (Çok Sert)

B1.2.5 — Aynı signal 2 kez CRITICAL olursa retry kapatılır

CRITICAL + CRITICAL → CIRCUIT_OPEN


Sonuç:

Sistem kendini korur

Öğrenci “duvara çarpmaz”

Koç acil bilgilendirilir

5️⃣ UI Kontratı (Senin Önerinle %100 Uyumlu)

B1.2.6 — Öğrenciye gösterilecek akış

Zaman Çizelgesi
Süre	UI
0–2 sn	Loading animasyonu
2–8 sn	Loading + Silent Retry
8–10 sn	Loading + Soft Warning
>10 sn	Error Message

📌 Error mesajı ancak retry bittiğinde gösterilir.

6️⃣ Observability Zorunluluğu

B1.2.7 — Her retry denemesi telemetry üretir

{
  "event": "RETRY_ATTEMPT",
  "signal": "BACKEND_TIMEOUT",
  "retry_index": 2,
  "delay_ms": 3000
}


Bu veri:

Sistem öğrenmesi

Kurum raporu

Altyapı iyileştirme

için altın değerdedir.

7️⃣ Yasaklar

🚫 Retry’ı UI component içinde yazmak
🚫 Hardcoded retry sayıları
🚫 Signal olmadan retry
🚫 Infinite retry

B1.2 SONUÇ

Bu aşamadan sonra sistem:

Kör retry yapmaz

Öğrenciyi yormaz

Kendini gözlemler

Koçu zamanında uyarır

🚨 B1.3 — Insight Escalation & Suppression Rules
Amaç

Her Insight gösterilmez.
Doğru Insight, doğru kişiye, doğru zamanda, doğru dozda gider.

Bu bölüm:

Insight gürültüsünü engeller

Öğrenciyi panikletmez

Koçu aksiyona zorlar

Kurumu stratejik veriyle besler

Anayasa Maddesi

B1.3.1 — Insight üretmek serbesttir, göstermek kontrollüdür

Signal → Insight (her zaman)
Insight → Audience (koşullu)

Insight Türleri (Standart)
Insight Type	Tanım
MIRROR	Öğrenciye yumuşak yansıma
COACH_ALERT	Koç için aksiyon
SYSTEM_ALERT	Teknik ekip
INSTITUTION_REPORT	Kurumsal trend
SILENT_LOG	Sadece sistem
Insight Karar Girdileri (Zorunlu)
signal_type
signal_severity
signal_frequency
audience
time_window
previous_insight_shown

🎯 Audience Matrix (Kim Ne Görür?)
Audience	Görür mü?	Format
Student	Sınırlı	MIRROR
Coach	Evet	ALERT
Institution	Özet	REPORT
System	Tam	LOG
1️⃣ Öğrenciye Insight Gösterme Kuralları

B1.3.2 — Öğrenciye asla teknik hata gösterilmez

🚫 “Backend timeout”
🚫 “Error 500”
🚫 “SQL deadlock”

✅ Doğru format:

“Son birkaç dakikadır hızın düştü. 
İstersen kısa bir mola verelim.”

Öğrenci Insight Şartları
Şart	Gerekçe
Severity ≠ CRITICAL	Panik önlenir
Tekrar < 3	Gürültü engellenir
Aksiyon önerisi var	Koçluk dili
2️⃣ Insight Suppression (Çok Kritik)

B1.3.3 — Aynı insight 1 oturumda yalnızca 1 kez gösterilir

same_insight + same_session → SUPPRESS


Ama:

Sistem loglar

Koç görür

Öğrenci tekrar görmez

3️⃣ Koç Escalation Kuralları

B1.3.4 — Koç, öğrenci fark etmeden önce bilgilendirilir

Koça giden Insight formatı:

{
  "student_id": "X",
  "signal": "TECHNICAL_BLOCKAGE",
  "frequency": 4,
  "dropout_risk": 0.72,
  "suggested_action": "Immediate contact"
}


📌 Koç Insight’ları:

Teknik

Soğuk

Aksiyon odaklı

4️⃣ Kurumsal Suppression & Aggregation

B1.3.5 — Kurum bireyi değil, paterni görür

Individual Insight ❌
Aggregated Trend ✅


Örnek:

“Son 7 günde öğrencilerin %18’i 
aynı teknik darboğazda sistemi terk etti.”

5️⃣ Insight Escalation Zinciri
Signal
  ↓
Retry Exhausted (B1.2)
  ↓
Insight Created
  ↓
Audience Filter
  ↓
Suppression Check
  ↓
Delivery

6️⃣ Insight Cooldown Kuralları

B1.3.6 — Insight sonrası cooldown zorunludur

Audience	Cooldown
Student	10 dk
Coach	5 dk
Institution	24 saat
7️⃣ Observability (Zorunlu)

Her insight için:

{
  "insight_type": "COACH_ALERT",
  "delivered": true,
  "suppressed": false,
  "cooldown_active": false
}


Bu veri:

Gürültü analizi

Koç verimliliği

L5 öğrenme

için kullanılır.

8️⃣ Yasaklar

🚫 Aynı insight’ı spamlemek
🚫 Öğrenciye teknik jargon
🚫 Koçu geç bilgilendirmek
🚫 Kuruma bireysel hata göndermek

B1.3 SONUÇ

Bu aşamadan sonra sistem:

Konuşmayı bilir

Susmayı da bilir

İnsanları yormaz

Müdahaleyi zamanında yapar

🧠 B2 — Telemetry & Observability Contract (L5-Scoped)
B2.0 — Kapsam ve Sınır Tanımı (ZORUNLU)

End.STP bir içerik üretim sistemi değildir.
End.STP bir analiz + yönlendirme + takip sistemidir.

Bu kontrat:

Öğrencinin test girişi

Sistem içi davranış

analiz sonrası etkileşim

eyleme yönelme

yeniden test döngüsü

üzerinden telemetri toplar.

🚫 YAPMAZ:

İçerik öğretmez

Konu anlatmaz

“Şunu öğren” demez

Psikolojik teşhis koymaz

B2.1 — Telemetry’nin Amacı (Anayasa Maddesi)

Telemetry = Hata aramak değil, süreci anlamaktır

Telemetry:

Error üretmek için değil

Signal üretmek için

Insight beslemek için

Retry / Escalation kararlarını desteklemek için

vardır.

B2.2 — Telemetry Kaynakları (Allowed Sources)
1️⃣ Akademik Girdi (PRIMARY)
Event	Kaynak
TEST_SUBMITTED	Öğrenci
correct / wrong / blank	Öğrenci
duration	Öğrenci

📌 Bu tek “bilinçli öğrenme girdisidir”

2️⃣ Sistem İçi Davranış (SECONDARY)
Event	Örnek
PAGE_VIEW	Analiz sayfası
DWELL_TIME	Analizde kalma
BUTTON_CLICK	“Eyleme Geç”
LINK_REDIRECT	Dış kaynak
SCROLL_DEPTH	İnceleme seviyesi

📌 Bunlar öğrenci beyanı değildir, davranışsal izdir

3️⃣ Geri Bildirim (OPTIONAL)
Event	Örnek
LIKE	Faydalı buldu
DISMISS	Öneriyi kapattı
IGNORE	Görüp etkileşmedi

🚫 Zorunlu değildir
🚫 Yokluğu hata değildir

B2.3 — Telemetry Tipleri (SERT AYRIM)
🔹 HARD TELEMETRY (Ölçülebilir)
Test sayısı
Zaman
Tekrar
Tıklama
Bekleme süresi

🔹 SOFT TELEMETRY (Yorumlanabilir)
Eyleme yöneldi mi
Analizi terk etti mi
Tekrar geri geldi mi


📌 Soft telemetry asla tek başına insight üretmez

B2.4 — Pedagojik Güvenlik Kuralı (KRİTİK)

B2.4.1 — Telemetry → pedagojik hüküm üretmez

YASAK ÇIKARIMLAR:

“Öğrenci motivasyonsuz”

“Öğrenci anlamıyor”

“Öğrenci sıkıldı”

İZİN VERİLEN:

“Bu akışta beklenenden erken çıktı”

“Analiz sayfasında kalma süresi düştü”

“Eyleme yönelme tamamlanmadı”

📌 Yorum = Coach’a bırakılır

B2.5 — Error & Telemetry Ayrımı
Kavram	Tanım
Error	Sistemsel başarısızlık
Telemetry	Sistem + kullanıcı etkileşimi
Signal	Error + Telemetry’den türeyen durum

🚫 Telemetry bir error değildir
🚫 Error pedagojik sinyal değildir

B2.6 — Error ile Telemetry’nin Birleştiği Yer

Örnek:

Event:
- BACKEND_TIMEOUT
- ANALYSIS_PAGE_DWELL < 5 sec


Signal:

TECHNICAL_BLOCKAGE_DURING_ANALYSIS


Insight:

“Sistem kaynaklı gecikme nedeniyle analiz tamamlanamadı”


🚫 “Öğrenci anlamadı” denmez

B2.7 — Telemetry → Signal Dönüşüm Şartı

Tek telemetry = sinyal değildir

Minimum 2 veri noktası + zaman ilişkisi gerekir


Örnek:

DWELL ↓ + TEST_ENTRY_DELAY ↑
→ FLOW_DISRUPTION

B2.8 — Öğrenciye Gösterim Kısıtı

Telemetry doğrudan öğrenciye gösterilmez

Öğrenciye gösterilebilecek olan:

Özetlenmiş Insight

Eylem odaklı

Yargısız

🚫 Grafik spam
🚫 Davranış ifşası

B2.9 — Koç & Kurum için Telemetry Seviyesi
Koç:

Bireysel

Zaman çizgili

Aksiyon odaklı

Kurum:

Toplu

Anonim

Trend bazlı

B2.10 — L5 Dayanıklılık İlkesi

Sistem, öğrenci yokken de öğrenir

Telemetry:

Retry başarısını

Insight bastırma oranını

Drop-off noktalarını

öğrenme verisi olarak saklar.

Bu:

Auto-healing

Self-tuning

Coach load reduction

için kullanılır.

B2 SONUÇ (NET)

Bu kontrat sayesinde:

Sistem haddini bilir

Pedagojik sınırı aşmaz

İçerik üretmediğini unutmaz

Ama süreci mükemmel okur

📜 Anayasa — Pedagoji & Navigasyon Ayrımı
Madde 1 — Pedagojik Tarafsızlık

End.STP, öğretim yöntemi dikte etmez.
Hiçbir içerik, yöntem veya kaynak zorunlu olarak sunulamaz.

Madde 2 — Analitik Önceliklendirme Yetkisi

End.STP, analiz sonuçlarına dayanarak:

Öncelikli konuları

Riskli öğrenme alanlarını

Döngü kopmalarını

belirtme yetkisine sahiptir.

Madde 3 — Navigasyon (Yol Gösterme) Yetkisi

End.STP:

İçerik üretmez

Ancak piyasadaki mevcut kaynaklara isteğe bağlı erişim kapıları açabilir

Bu yönlendirmeler:

Opsiyoneldir

Çoklu alternatiftir

Zorunlu değildir

Madde 4 — Dil Kontratı (ZORUNLU)

Affiliate / link sunulan her yerde şu ilke geçerlidir:

“Bu bir öneri değil, bir opsiyon listesidir.
Kullanmak zorunda değilsin.”

Madde 5 — Tek Doğru Yasağı

End.STP hiçbir zaman:

“En iyi yol”

“Doğru yöntem”

“Bunu yapmalısın”

ifadelerini kullanamaz.

🧠 PRATİK DİL ŞABLONLARI (ÇOK ÖNEMLİ)
❌ Yanlış (Pedagojik Diktatörlük)

“Bu konuyu öğrenmek için şu videoyu izle.”

✅ Doğru (Analitik Navigasyon)

“Bu konu şu anda öncelikli görünüyor.
İstersen, bu konuyla ilgili çalışmak için piyasada kullanılan bazı kaynaklara göz atabilirsin.”

❌ Yanlış

“Bu içeriği bitirmeden ilerleyemezsin.”

✅ Doğru

“Bu konu tekrar test edilmeden ilerleme ölçülemez.
Çalışma tercihi sana aittir.”

🔗 Affiliate Sistemi ile %100 Uyum

Affiliate bölümünün rolü:

❌ “Bunu izle”

✅ “Buralarda bulabilirsin”

Bu fark hukuki, etik ve pedagojik olarak seni korur.

Ayrıca:

“Satış baskısı” algısını kırar

Koçluk yaklaşımıyla örtüşür

L5 sistem iddianı güçlendirir

🧠 SERT GERÇEK (Ama Avantajın)

Eğer End.STP bir gün “şunu izlemezsen olmaz” derse
rakiplerinden biri olur.

Ama:

“Analizine göre şu alanlarda boşluk var,
bu boşlukları kapatmak için ekosistemde şu tür araçlar var” derse
kategori yaratır.

✅ SON KARAR (NET)

Affiliate çelişki değil, tamamlayıcı

Kritik olan dil ve zorunluluk seviyesi

Senin tarif ettiğin sistem:
Pedagojik diktatör değil, analitik navigatör

Bu haliyle:

L5 vizyonla uyumlu

Koçluk felsefesiyle uyumlu

Yatırımcıya anlatılabilir

Hukuken ve etik olarak sağlam
1️⃣ B4 — Insight Severity & Escalation Rules

Amaç:
Her Insight’ın ne kadar kritik olduğunu,
kime, ne zaman, nasıl yansıyacağını standartlaştırmak.

Bu bölüm, Coach Panel’in “süs” mü yoksa operasyonel araç mı olacağını belirler.

🎚️ Insight Severity Levels (L1–L5)

Not:
Severity ≠ Error
Severity = Eylem Aciliyeti

L1 — Informational

Tanım:
Durum farkındalığı. Aksiyon gerekmez.

Örnek:

“Bu hafta test sayısı ortalamanın biraz altında”

“Son 3 testte süre uzamış”

Hedef Kitle:

Öğrenci (ayna etkisi)

Sistem Davranışı:

UI banner / küçük bilgi

Log + telemetry kaydı

❌ Coach’a gitmez

L2 — Advisory

Tanım:
İyileştirme fırsatı var, risk düşük.

Örnek:

“Aynı konu 2. kez düşük başarıyla tekrarlandı”

“Odak süresi düşmeye başladı”

Hedef Kitle:

Öğrenci

(Opsiyonel) Koç – pasif

Sistem Davranışı:

Öğrenciye yumuşak ayna mesajı

Coach panelde “soft insight”

❌ Alarm yok

L3 — Warning

Tanım:
Davranışsal veya sistemsel sapma başladı.

Örnek:

“3 oturumdur aynı hatada kalındı”

“Retry + abandon pattern oluştu”

Hedef Kitle:

Koç (aktif)

Öğrenci (kontrollü dil)

Sistem Davranışı:

Coach’a erken uyarı

Öğrenciye motivasyonel ama teknik olmayan mesaj

Trend takibi başlar

L4 — Critical

Tanım:
Kopma riski veya sistemsel engel yüksek.

Örnek:

“Backend timeout → session abandon (3x)”

“Frustration + drop-out sinyali”

Hedef Kitle:

Koç

Kurum (özet)

Sistem Davranışı:

Coach panelde kırmızı durum

Kurum dashboard’unda agregasyon

Otomatik follow-up önerisi

L5 — Emergency / Intervention

Tanım:
Öğrenci veya sistem ilerleyemiyor.

Örnek:

“Teknik hata + davranışsal kopma”

“Sistem kaynaklı tekrar eden blokaj”

Hedef Kitle:

Koç

Kurum (operasyonel)

Sistem (self-healing)

Sistem Davranışı:

Otomatik ticket / task

Coach için “acil müdahale” etiketi

Altyapı / ürün ekibine telemetry snapshot

🔁 Escalation Kuralları (Özet)
Koşul	Davranış
L1 → L2	Trend tekrar ederse
L2 → L3	Aynı sinyal 3 session
L3 → L4	Drop-out veya abandon
L4 → L5	Teknik + davranışsal çakışma
L5	İnsan müdahalesi şart
❗ Altın Kural

Insight hiçbir zaman “öğretmez”
Sadece “durumu ve riski” tanımlar

2️⃣ C1 — Event / Signal / Insight Schema (Supabase)

Amaç:
Artık soyuttan çıkıyoruz.
Bu kontrat DB + sistem + panel için tek gerçek olacak.

📦 1. events Tablosu
create table events (
  id uuid primary key default gen_random_uuid(),

  actor_type text not null, -- student | coach | system
  actor_id uuid,

  event_type text not null, -- error_1004, click, submit_test, timeout
  event_source text not null, -- frontend | backend | db | infra

  context jsonb not null, -- session_id, page, dataset_size, module

  created_at timestamptz default now()
);


🔹 Ham gerçek
🔹 Asla silinmez
🔹 Yorum yok, sadece veri

📦 2. signals Tablosu
create table signals (
  id uuid primary key default gen_random_uuid(),

  signal_code text not null, -- F_SIGNAL, L_SIGNAL, D_SIGNAL
  signal_version int not null,

  derived_from_event_ids uuid[] not null,

  signal_strength numeric, -- 0–1
  signal_metadata jsonb,

  created_at timestamptz default now()
);


🔹 İşlenmiş
🔹 Pattern içerir
🔹 Tek başına kullanıcıya gösterilmez

📦 3. insights Tablosu
create table insights (
  id uuid primary key default gen_random_uuid(),

  insight_type text not null, -- fatigue, blockage, dropout_risk
  severity_level int not null, -- 1–5

  related_signal_ids uuid[] not null,

  target_actor text not null, -- student | coach | institution

  insight_payload jsonb not null, -- UI-safe açıklama
  internal_payload jsonb, -- teknik detay (coach/system)

  status text default 'open', -- open | acknowledged | resolved

  created_at timestamptz default now(),
  resolved_at timestamptz
);


🔹 Sistemin “anlam” ürettiği yer burası
🔹 UI, Coach Panel ve raporlar buradan beslenir

🔐 Güvenlik & Yetki (Özet)

events → sadece sistem

signals → backend / orchestrator

insights:

öğrenci → sadece kendi + L1–L2

koç → L2–L5

kurum → agregasyon

🧠 Neden Bu Yapı Doğru?

Retry ≠ observability

Signal ≠ insight

Insight ≠ pedagojik emir

Bu ayrım:

L5 dayanıklılığı sağlar

“Organizma gibi yaşayan sistem” hedefini mümkün kılar

6 ay sen dokunmasan bile sistem anlam üretmeye devam eder

📌 SON DURUM

✅ B4 tamam
✅ C1 tablo kontratı hazır
✅ Master dokümana yapıştırılabilir
✅ Supabase migration’a hazır

C2 — Signal Registry v1 (Event Taxonomy & Signal Library)

Amaç:
Event’lerden türeyen signal’ların:

tanımını

kapsamını

hangi riskleri temsil ettiğini

hangi katmana ait olduğunu
tek ve değişmez bir referans haline getirmek.

Bu dosya:

Orchestrator’ın

Retry policy’nin

Insight engine’in

Coach Panel’in

tek kaynağıdır (single source of truth).

🧠 Signal Registry Nedir?

Signal = Yorumlanmış teknik/pedagojik durum

Event hamdır
Signal anlamlıdır
Insight aksiyoneldir

Signal Registry:

yeni signal eklenmesini kontrollü yapar

sistemin zamanla sapıtmasını engeller

L5’te “organizma” davranışı için şarttır

🧱 Signal Registry v1 — Tasarım İlkeleri (ANAYASA)

Signal pedagojik emir vermez

Signal içerik önermez

Signal UI metni içermez

Signal versiyonlanır

Signal yalnızca event’ten doğar

Signal tek başına kullanıcıya gösterilmez

Signal insight üretmeden aksiyon doğuramaz

📚 Signal Registry v1 — Kategori Yapısı

v1’de 3 ana signal sınıfı var:

Kod	Adı	Kapsam
L-SIGNAL	Latency / Sistem Tepkisi	Teknik yavaşlık, timeout
F-SIGNAL	Frustration / Davranış	Odak kaybı, tekrar
D-SIGNAL	Drop-out Risk	Kopma, terk etme

⚠️ Motivasyon, pedagoji, içerik signal değildir
Onlar insight layer’da ele alınır

📦 Signal Registry v1 — Tablo (Ana Kayıt)
| signal_code | version | category | description |
|------------|---------|----------|-------------|
| L_SIGNAL_TIMEOUT | 1 | L-SIGNAL | Backend yanıt süresi eşik üstü |
| L_SIGNAL_RETRY_SPIKE | 1 | L-SIGNAL | Kısa sürede tekrar eden retry |
| F_SIGNAL_IDLE | 1 | F-SIGNAL | Kullanıcı etkileşimsiz kaldı |
| F_SIGNAL_REPEAT_ERROR | 1 | F-SIGNAL | Aynı hatada tekrar |
| D_SIGNAL_ABANDON | 1 | D-SIGNAL | Session yarım bırakıldı |
| D_SIGNAL_DROP_TREND | 1 | D-SIGNAL | Tarihsel kopma paterni |

🔍 Signal Detay Tanımları (v1)
🔹 L_SIGNAL_TIMEOUT (v1)

Kaynak Event’ler:

backend_timeout

api_response_time > threshold

Teknik Anlam:

Sistem cevap veremedi

Signal Metadata:

{
  "endpoint": "/student/progress",
  "latency_ms": 8200,
  "retry_count": 2
}

🔹 F_SIGNAL_IDLE (v1)

Kaynak Event’ler:

mouse_idle

no_click_duration > X

Davranışsal Anlam:

Öğrenci dondu / kararsız

Signal Metadata:

{
  "idle_seconds": 45,
  "page": "test-entry"
}

🔹 F_SIGNAL_REPEAT_ERROR (v1)

Kaynak Event’ler:

same_error_code repeated

Davranışsal Anlam:

Öğrenci aynı noktada takılıyor

Signal Metadata:

{
  "error_code": "1004",
  "repeat_count": 3
}

🔹 D_SIGNAL_ABANDON (v1)

Kaynak Event’ler:

session_end without completion

Pedagojik Anlam (yorum değil):

Akış kesildi

Signal Metadata:

{
  "session_duration": 180,
  "last_page": "dashboard"
}

🔁 Signal Versioning Kuralı

Signal değişirse → version artar

Değişiklik	Version
Eşik değişti	+1
Yeni event eklendi	+1
Yorum değişti	❌ (yasak)

Yorum insight layer’dadır.

🧩 Signal → Insight İlişkisi (Ön İzleme)
Signal Kombinasyonu	Olası Insight
L + F	Teknik Blokaj
F + D	Motivasyon Kaybı
L + F + D	Kritik Kopma Riski

Detayı C3’te yapacağız.

❗ Neden C2 Kritik?

Eğer Signal Registry net olmazsa:

Retry kör olur

Coach panel çöp olur

Sistem “hissiyatla” çalışır

L5 hayal olur

Şu an:
✅ Sert
✅ Net
✅ Genişleyebilir
✅ Geriye dönük uyumlu

✅ C2 DURUM

Signal Registry v1 tamam

Anayasaya uygun

Supabase tablolarıyla uyumlu

Orchestrator-ready

C3 — Insight Generation Engine

(Signal → Insight Transformation Contract)

1️⃣ Amaç

Insight Engine’in görevi:

Tekil sinyalleri değil, sinyal kombinasyonlarını
zamansal ve bağlamsal olarak yorumlayıp
aksiyon gerektiren anlamlı çıktılara dönüştürmektir.

Insight:

UI mesajı değildir

içerik önerisi değildir

pedagojik anlatım değildir

karar girdisidir

2️⃣ Insight Nedir? (ANAYASA TANIMI)

Insight = Sistem tarafından algılanan risk / durum / fırsat

Bir insight şu sorulara cevap verir:

Ne oluyor?

Kimin için oluyor?

Ne kadar kritik?

Müdahale gerekir mi?

Kime bildirilmeli?

3️⃣ Insight Engine’in Girdi–Çıktı Kontratı
Girdi

Signal Registry v1’den gelen signal instance’ları

Zaman damgaları

Context (öğrenci, sayfa, session, kurum)

Çıktı

Insight object

Severity

Escalation target

Recommended handling (ama içerik yok)

4️⃣ Insight Türleri (v1)
Kod	Adı	Anlam
INS_TECH_BLOCK	Teknik Blokaj	Sistem kaynaklı ilerleme engeli
INS_COGNITIVE_OVERLOAD	Bilişsel Aşırı Yük	Öğrenci yorulmuş / kilitlenmiş
INS_DROP_RISK	Kopma Riski	Öğrenci sistemi terk etmeye yakın
INS_SYSTEMIC_ISSUE	Sistemik Sorun	Kurum / altyapı düzeyinde problem
5️⃣ Insight Üretim Kuralları (Rule-Based v1)
🔹 Rule 1 — Teknik Blokaj
IF
  L_SIGNAL_TIMEOUT
  AND F_SIGNAL_IDLE (≤ 60sn)
THEN
  INS_TECH_BLOCK


Yorum:

Sistem yavaşladı

Öğrenci dondu

Problem öğrencide değil

🔹 Rule 2 — Bilişsel Aşırı Yük
IF
  F_SIGNAL_REPEAT_ERROR ≥ 3
  AND session_duration > threshold
THEN
  INS_COGNITIVE_OVERLOAD


Yorum:

Öğrenci aynı noktada dönüyor

Teknik hata olmasa bile verim düşmüş

🔹 Rule 3 — Kopma Riski
IF
  D_SIGNAL_ABANDON
  AND recent_history contains F_SIGNAL_IDLE
THEN
  INS_DROP_RISK


Yorum:

Terk bir “anlık” değil

Öncesinde sinyal vermiş

🔹 Rule 4 — Sistemik Sorun
IF
  L_SIGNAL_TIMEOUT
  observed_across > N users
THEN
  INS_SYSTEMIC_ISSUE


Yorum:

Öğrenci problemi değil

Kurum / altyapı problemi

6️⃣ Insight Severity Seviyeleri (Özet)

Detayı B4’te genişlettik, burada engine açısından özet veriyoruz.

Severity	Anlam
LOW	İzle
MEDIUM	Uyar
HIGH	Müdahale
CRITICAL	Acil

Insight severity’siz anlamsızdır.

7️⃣ Insight Nesnesi (Canonical Object)
{
  "insight_code": "INS_TECH_BLOCK",
  "version": 1,
  "severity": "HIGH",
  "signals": [
    "L_SIGNAL_TIMEOUT",
    "F_SIGNAL_IDLE"
  ],
  "subject_type": "student",
  "subject_id": "uuid",
  "context": {
    "page": "test-entry",
    "session_id": "uuid"
  },
  "created_at": "timestamp"
}

8️⃣ Insight ≠ UI Mesajı (KIRMIZI ÇİZGİ)

Insight şunları ASLA içermez:

❌ “Şu konuyu çalış”
❌ “Bu videoyu izle”
❌ “Bu yöntemi dene”
❌ “Başarısızsın”

Insight yalnızca:

“Burada bir durum var.”

der.

9️⃣ Insight → Kime Gider?
Insight	Hedef
INS_TECH_BLOCK	Sistem + Kurum
INS_COGNITIVE_OVERLOAD	Öğrenci (ayna) + Koç
INS_DROP_RISK	Koç
INS_SYSTEMIC_ISSUE	Kurum

Öğrenciye giden insight ayna diline çevrilir,
Koça giden tekniktir,
Kuruma giden trenddir.

🔐 L5 Uyum Notu

Bu yapı sayesinde sistem:

Sensör (event)

Sinir (signal)

Beyin (insight)

katmanlarını net ayırır.

Bu ayrım olmazsa:

affiliate yönlendirme kirlenir

pedagojik diktatörlük başlar

sistem “ne iş yaptığı belli olmayan” bir şeye dönüşür
D — Coach Insight Panel Contract

(Professional Decision Surface)

Amaç:
Koç ekranı bir “dashboard” değil, müdahale panelidir.
Burada öğretim yok, yorum yok, yargı yok — durum + risk + zaman vardır.

1️⃣ Temel İlke (ANAYASA)

Koç Paneli = Karar Verme Alanı

Koç Paneli:

öğrenciye ne öğretileceğini söylemez

içeriği anlatmaz

motivasyon cümlesi kurmaz

“Nerede, ne oluyor, acil mi?” sorusuna cevap verir

2️⃣ Coach Panel’in Sorumluluğu
Yapmalı	Yapmamalı
Riskleri önceliklendirmek	Ders anlatmak
Teknik vs. davranışsal ayrımı yapmak	İçerik önermek
Zamanlama göstermek	Yorum katmak
Müdahale ihtiyacını işaretlemek	Pedagojiye girmek
3️⃣ Panel’e Giren Veri Kaynakları

Coach Panel SADECE şunları alır:

Insight objects (C3)

Severity & escalation bilgisi

Zaman serisi (trend)

❌ Event
❌ Raw telemetry
❌ UI error message
❌ Öğrenciye gösterilen metinler

4️⃣ Coach Panel Görünüm Katmanları
🔹 4.1 — Insight Feed (Zorunlu)

En kritik en üstte

Alan	Açıklama
Insight Code	INS_DROP_RISK vb.
Severity	LOW → CRITICAL
Student	Kim
Context	Nerede
Time	Ne zaman
Status	Açık / ele alındı
🔹 4.2 — Insight Detail (On Click)

Bir insight açıldığında:

INSIGHT: Drop-out Risk
Severity: HIGH

Signals:
- F_SIGNAL_IDLE (120sn)
- D_SIGNAL_ABANDON (2 kez)

Context:
- Page: test-entry
- Session: 45 dk

Interpretation:
→ Öğrenci teknik değil bilişsel sebeple kopuyor

Suggested Handling:
→ Koç müdahalesi gerekebilir


Not: “Suggested Handling” bir aksiyon tipidir, içerik değildir.

5️⃣ Müdahale Tipleri (Action Types)

Coach Panel aksiyon adı verir, aksiyon içeriği vermez.

Kod	Anlam
MONITOR	İzle
CHECK_IN	Temas kur
TECH_ESCALATE	Teknik birime bildir
PRIORITY_FLAG	Öncelik işaretle
NO_ACTION	Bilgi amaçlı
6️⃣ Zaman Boyutu (Çok Kritik)

Her insight şu zaman bilgileriyle gelir:

First seen

Last seen

Frequency

Escalation threshold

Koç şu soruyu görür:
“Bu yeni mi, kronik mi?”

7️⃣ Coach Panel ≠ Öğrenci Paneli
Öğrenci	Koç
Ayna dili	Teknik dil
Duygu yumuşatma	Risk sertliği
“Durum farkındalığı”	“Müdahale kararı”

Aynı insight iki farklı yüzle sunulur.

8️⃣ Affiliate & Navigasyon Çakışması YOK

Coach Panel:

link vermez

video önermez

kitap adı söylemez

Ama şunu yapabilir:

“Bu öğrencinin şu anda analiz sonuçlarına göre aksiyon ihtiyacı var”

Affiliate:

öğrenci panelinde

isteğe bağlı

ayrı kontratla

9️⃣ L5 Dayanıklılık İlkesi

Koç Panel:

sistem çökse bile son insight’ı gösterir

veri gecikse bile sessiz kalır

eksik veride yanlış alarm üretmez

10️⃣ Minimal API Contract (v1)
GET /coach/insights?status=open

{
  "insights": [
    {
      "insight_code": "INS_COGNITIVE_OVERLOAD",
      "severity": "HIGH",
      "student_id": "uuid",
      "context": "test-entry",
      "first_seen": "timestamp",
      "frequency": 3
    }
  ]
}

11️⃣ KIRMIZI ÇİZGİLER (Bir Daha Asla Tartışılmayacak)

❌ “Bu konuyu çalıştır”
❌ “Şu içerik önerilir”
❌ “Bu öğrenci tembel”
❌ “Şu yöntem işe yarar”

✅ D DURUM

Coach Insight Panel kontratı tamam

C3 Insight Engine ile uyumlu

Affiliate & pedagojiden net ayrılmış

Kurum paneline genişletilebilir

E — Institution Insight & System Health Panel

(Strategic Oversight Surface)

Amaç:
Kurum paneli birey değil sistem izler.
Bu panel bir “dashboard” değil, risk haritası + karar radaridir.

1️⃣ Temel İlke (ANAYASA)

Institution Panel = Sistem Sağlığı + Toplu Risk Yönetimi

Kurum paneli:

tekil öğrenciye odaklanmaz

pedagojik içerik konuşmaz

koç gibi müdahale etmez

trendleri, darboğazları, verimlilik kayıplarını gösterir

2️⃣ Kurum Panelinin Sorumluluk Alanı
Gösterir	Göstermez
Toplu risk yoğunlukları	Tek öğrenci detayları
Sistemsel darboğazlar	Öğrenci duygusal yorumları
Zaman içi trendler	Günlük mikro olaylar
Altyapı etkileri	Pedagojik öneriler
3️⃣ Veri Kaynakları (Sıkı Kontrat)

Institution Panel SADECE şunları tüketir:

Aggregated Insights (C3 → roll-up)

System Signals (latency, retry, timeout)

Institutional Metadata (kurum, sınıf, dönem)

❌ Raw events
❌ Mouse telemetry
❌ UI error mesajları
❌ Koç notları

4️⃣ Panel Katmanları
🔹 4.1 — Risk Heatmap (Zorunlu)

“Nerede yoğunlaşıyor?”

Boyut	Açıklama
Time	Gün / hafta / ay
Module	Test-entry, dashboard vb.
Insight Type	Drop-out, latency, overload
Severity	LOW → CRITICAL

📌 Çıktı: Kırmızı alanlar = müdahale gerektiren sistem noktaları

🔹 4.2 — Trend Analysis (Zaman Serisi)

Örnek grafikler:

Drop-out risk oranı (haftalık)

Backend timeout sayısı (aylık)

Retry > 3 oranı

Kurum şunu görür:
“Bu sorun artıyor mu, azalıyor mu?”

🔹 4.3 — System Health Indicators
Gösterge	Anlam
Avg API Latency	Altyapı yükü
Retry Success Rate	Auto-healing başarısı
Silent Fail Count	Sessizce tolere edilen hatalar
Escalation Count	İnsan müdahalesi gereken durumlar
5️⃣ Kurumsal Risk Tipleri

Institution Panel öğrenci değil risk sınıfı konuşur.

Risk Code	Açıklama
SYS_LATENCY_SPIKE	Altyapı yavaşlığı
UX_FRICTION_CLUSTER	Belirli modülde kullanım zorluğu
DROP_CLUSTER	Toplu kopma riski
DATA_INTEGRITY_RISK	Veri tutarsızlığı
6️⃣ Kurumsal Aksiyonlar (YETKİ SINIRI)

Institution Panel aksiyon önermez, aksiyon ihtiyacını işaretler.

İşaret	Anlam
TECH_REVIEW	Teknik inceleme gerekli
PROCESS_REVIEW	Süreç iyileştirme
COACH_BRIEF	Koçlara bilgilendirme
NO_ACTION	Bilgi amaçlı
7️⃣ Koç Paneli ile İlişki
Koç	Kurum
Bireysel risk	Toplu risk
Anlık müdahale	Stratejik karar
Context-rich	Context-aggregated

Aynı insight → iki farklı soyutlama seviyesi

8️⃣ Affiliate & İçerik ile NET AYRIM

Institution Panel:

içerik önermez

link göstermez

anlaşma metni konuşmaz

Ama şunu kanıtlar:

“Belirli noktalarda öğrenciler sistemden kopuyor”

➡️ Bu, kuruma satılan değerin ölçülebilir kanıtıdır

9️⃣ L5 Dayanıklılık Kuralları

Veri gecikirse → eski trendi göster

Eksik veri varsa → sessiz kal

Yanlış pozitif üretme → yasak

Sistem çökerse → son snapshot korunur

10️⃣ Minimal API Contract (v1)
GET /institution/health/summary

{
  "risk_clusters": [
    {
      "type": "DROP_CLUSTER",
      "severity": "HIGH",
      "module": "test-entry",
      "trend": "increasing"
    }
  ],
  "system_health": {
    "avg_latency_ms": 820,
    "retry_success_rate": 0.91
  }
}

11️⃣ KIRMIZI ÇİZGİLER

❌ Öğrenci adı gösterme
❌ Koç aksiyonuna karışma
❌ Pedagojik yorum
❌ İçerik yönlendirme

✅ E DURUM

Kurum Panel kontratı tamam

Coach Panel (D) ile çakışma yok

Affiliate & pedagojiden net ayrım

L5 observability ile uyumlu
F — Auto-Healing & System Learning Loop

(Self-Recovering, Non-Pedagogical, Institution-Aware)

0️⃣ F Bölümünün Konumu (Neden Buradayız?)

F = sistemin refleksi
Retry = kas seğirmesi
Auto-Healing = refleks
Learning Loop = hafıza

Bu katman:

UI değildir

pedagojik değildir

öğrenciye “ne yapacağını” söylemez

sistemin kendi hatalarından öğrenmesini sağlar

1️⃣ Rol & Yetki Haritası (Hatırlatma ile Uyum)

Bu bölüm, senin anlattığın çok-katmanlı yetki yapısını BOZMADAN çalışır.

Rol	F Katmanıyla İlişkisi
End.STP Super Admin (sen)	Kuralları tanımlar, eşikleri belirler
Kurum Admin	Trendleri görür, teknik uyarı alır
Rehberlik Servisi	Sistemsel risk yoğunluğu görür
Koç / Etüt Öğretmeni	Bireysel insight alır (D)
Öğrenci (bireysel)	Sadece stabil sistem görür

⚠️ Auto-Healing hiçbir zaman rol hiyerarşisini delmez.

2️⃣ Auto-Healing NEDİR / NE DEĞİLDİR
✅ Auto-Healing NEDİR

Bilinen hata paterni için önceden tanımlı teknik refleks

Retry + alternatif yol + gecikmeli işlem

Sessiz çalışır

Kayıt altına alınır

❌ Auto-Healing DEĞİLDİR

İçerik sunmak

Öğrenciye “şunu yap” demek

Pedagojik karar vermek

Koçun yerine geçmek

3️⃣ Auto-Healing Lifecycle
Signal oluşur
   ↓
Known Pattern mi?
   ↓ yes                ↓ no
Auto-Heal Attempt       Escalation
   ↓
Success / Fail
   ↓
Learning Log

4️⃣ Auto-Healing Trigger Türleri
Trigger	Örnek
Technical	Backend timeout
UX	Form submit + idle
Data	Incomplete payload
Infra	Latency spike

📌 Pedagojik trigger YOK

5️⃣ Healing Action Types (Sert Sınır)
Action	Açıklama
RETRY_DELAYED	Sessiz retry
FALLBACK_PATH	Alternatif endpoint
DEFERRED_WRITE	Kuyruğa alma
UI_STABILIZE	UI kilitlenmesini önleme
SESSION_EXTEND	Session korunur

❌ “Yeni görev ver”
❌ “Şunu çalış”
❌ “Şu içeriği öner”

6️⃣ Learning Loop (Asıl Değer Burada)

Auto-Healing tek seferlik çözüm değildir.
Her deneme bir öğrenme kaydı üretir.

6.1 Learning Record
{
  "signal_code": "SYS_TIMEOUT",
  "healing_action": "RETRY_DELAYED",
  "attempt_count": 2,
  "success": true,
  "latency_before": 1800,
  "latency_after": 420
}

6.2 Pattern Confidence

Her pattern zamanla güven skoru kazanır.

Confidence	Davranış
LOW	Escalation ağırlıklı
MEDIUM	Heal + log
HIGH	Sessiz auto-heal
7️⃣ İnsan Faktörü ile İlişki (Kritik)

Auto-Healing öğrenciyi kurtarmaz, sistemi kurtarır.

Ama şu etkiyi yaratır:

Öğrenci daha sinirlenmeden sistem toparlanır

Koç “geç kaldım” demez

Kurum “altyapı çöktü” demeden trend görür

8️⃣ Coach / Institution Pipeline ile Entegrasyon
Katman	Ne Alır
Coach Insight (D)	“Sistem kaynaklı blokaj”
Institution Panel (E)	“Bu hafta %12 daha fazla heal”
Super Admin	“Yeni pattern oluştu”
9️⃣ Supabase Tarafı (Konsept – SQL yazmana gerek yok)

Yeni tablo eklenir, mevcutları bozmaz:

auto_heal_attempts

auto_heal_patterns

auto_heal_learning_log

📌 Bunlar Event/Signal/Insight tablolarına bağlanır

🔴 KIRMIZI ÇİZGİLER (Tekrar)

Auto-Healing pedagojik öneri üretmez

Öğrenciyi “yönlendirmez”

Affiliate link tetiklemez

Koç kararının önüne geçmez

10️⃣ L5 Dayanıklılık Garantisi

Sen 6 ay yoksan bile:

Sistem çökerse toparlar

Aynı hatayı ikinci kez daha iyi karşılar

İnsanlara doğru seviyede sinyal gönderir

Bu, organizma davranışıdır, bot değil.

✅ F DURUM

Senin anlattığın rol & kurum yapısıyla %100 uyumlu

Pedagoji / analiz / navigasyon çizgisi korunuyor

Affiliate ile çelişmiyor

L5 hedefi destekliyor
G — Super Admin Control Plane
End.STP Anayasası (L5 Governance Layer)
0️⃣ G Katmanının Misyonu

Super Admin Control Plane, End.STP’nin:

neyi yapabileceğini,

neyi ASLA yapamayacağını,

kimlerin hangi sınırlar içinde hareket edebileceğini
tanımlayan en üst bağlayıcı katmandır.

Bu katman:

UI değildir

API değildir

pedagojik değildir

➡️ Kuralların kurallarıdır

1️⃣ Tek Yetkili: End.STP Super Admin

End.STP Super Admin (sen):

Sistemin etik, teknik ve pedagojik sınırlarını belirler

Yetkiyi dağıtır, ama devretmez

Kurumlara alan açar, ama merkezi kontratı bozmaz

Override eder, ama log bırakır

📌 Hiçbir rol Super Admin’in üstüne çıkamaz

2️⃣ Rol Hiyerarşisi (Bağlayıcı)
End.STP Super Admin
    ↓
Institution Super Admin
    ↓
Institution Admin
    ↓
Coach / Counselor / Teacher
    ↓
Student (Individual or Institutional)

🔒 Kural

Alt rol:

Üst rolün kuralını değiştiremez

Sadece tanımlı parametreler içinde çalışır

3️⃣ Global First İlkesi (Anayasa Maddesi)

Tüm kurallar GLOBAL tanımlanır, LOCAL daraltılır.

Kurum → kural ekleyemez

Kurum → sadece kapama / sınırlandırma yapabilir

Öğrenci → sadece kişisel tercihler yapabilir

4️⃣ Değiştirilemez Kırmızı Çizgiler (Non-Negotiable)
❌ Sistem ASLA şunları yapamaz:

“Bu içeriği izle”

“Şu yöntemle öğren”

“Bunu yapmazsan başaramazsın”

“Bu link zorunludur”

“Şu pedagojik yol tek doğrudur”

📌 Bunlar pedagojik diktatörlük sayılır
📌 Sistem navigatördür, öğretmen değildir

5️⃣ Super Admin Yetki Alanları
5.1 Signal & Insight Governance

Super Admin şunları belirler:

Signal türleri (L, F, D, SYS…)

Signal severity eşikleri

Insight escalation kuralları

Conflict resolution öncelikleri

➡️ Hiçbir kurum yeni Signal tanımı yapamaz

5.2 Retry & Auto-Healing Governance

Max retry count

Retry delay policy

Auto-heal aktif/pasif sınırı

Learning loop açık/kapalı durumu

📌 Kurum sadece görür, değiştiremez

5.3 Observability & Telemetry Scope

Super Admin şunları tanımlar:

Hangi telemetry toplanır

Hangi veri asla toplanmaz

Hangi veriler anonimleşir

Kurum/koç neyi görebilir

🔐 GDPR / KVKK uyumu bu katmanda garanti edilir

6️⃣ Institution Boundary Rules
Kurumlar şunları yapabilir:

Öğrenci, öğretmen, koç tanımlamak

Şube hiyerarşisi kurmak

Toplu test girişi (CSV / Excel)

Kendi öğrencilerini analiz etmek

Kurumlar şunları YAPAMAZ:

Signal üretme kuralı değiştirmek

Insight dilini manipüle etmek

Öğrenciye zorunlu içerik dayatmak

Sistem davranışını override etmek

7️⃣ Coach & Counselor Sınırı

Koç:

Insight görür

Risk görür

Müdahale eder (insan olarak)

Koç:
❌ Algoritma değiştiremez
❌ Signal bastıramaz
❌ Öğrenci adına karar veremez

8️⃣ Öğrenci Hakları (Anayasal)

Öğrenci:

İçeriğe zorlanmaz

Hata ile suçlanmaz

Teknik arızadan sorumlu tutulmaz

“Yetersizsin” diliyle karşılaşmaz

📌 Sistem dili yansıtıcıdır, yargılayıcı değildir

9️⃣ Override Mekanizması (Son Çare)

Super Admin:

Her şeyi override edebilir

AMA her override:

timestamp

neden

etki alanı
ile loglanır

Override = güç değil, sorumluluk

🔟 Anayasa Değişikliği Protokolü

Bu dosya:

Sürüm numarası taşır

Geriye dönük bozulmaz

Değişiklikler changelog ile yapılır

v1.0 — L5 Foundation
v1.1 — Institution Expansion
v1.2 — International Compliance

🧠 Felsefi Çekirdek (Özet)

End.STP:

öğretmez

dayatmaz

manipüle etmez

Ama:

görür

ölçer

yönü gösterir

✅ G DURUMU

Sistem sınırları net

Roller çakışmıyor

Pedagoji ile analiz ayrımı korunuyor

L5 hedefi kilitlendi
H — Decision Transparency & Explainability Layer
“Bu öneri neden üretildi?” Katmanı (L5 Explainability Contract)
0️⃣ H Katmanının Amacı

Decision Transparency Layer, End.STP’nin verdiği hiçbir önerinin:

gizemli,

açıklamasız,

sorgulanamaz
olmamasını garanti eder.

Bu katman sayesinde sistem:

“önerdi”ği için değil,

neden önerdiğini kanıtladığı için güvenilir olur.

1️⃣ Altın Kural (Bağlayıcı)

End.STP’de açıklanamayan hiçbir öneri gösterilemez.

Açıklaması olmayan öneri:

UI’da görünmez

Koça düşmez

Öğrenciye yansımaz

📌 Bu bir opsiyon değil, anayasal zorunluluktur.

2️⃣ Açıklama Seviyeleri (Explainability Levels)

Her Decision / Insight 3 katmanda açıklanır:

2.1 Öğrenci Seviyesi (Human-Readable)

Duygusal yargı yok

Teknik terim yok

Yönlendirici ama zorlayıcı değil

Örnek:

“Son test sonuçlarına göre bu konu uzun süredir tekrar edilmemiş görünüyor.”

2.2 Koç Seviyesi (Analytical)

Signal referansları görünür

Zaman, frekans, eşik bilgisi açık

Müdahale için veri sağlar

Örnek:

“D-SIGNAL:

Last_Test_Days = 14

Remembering_Rate = %52

Retry_Count = 2”

2.3 Sistem Seviyesi (Machine-Traceable)

Event ID’ler

Signal ID’ler

Mapping Version

Engine Version

Timestamp

📌 UI’da görünmez
📌 Log & audit için zorunludur

3️⃣ Decision Trace (Zincir Mantığı)

Her öneri şu zinciri taşır:

Event(s)
  ↓
Signal(s)
  ↓
Rule / Threshold
  ↓
Insight
  ↓
Decision


📌 Zincirin herhangi bir halkası eksikse:
➡️ Decision iptal edilir

4️⃣ Zorunlu Explainability Alanları

Her Decision objesi şu alanları taşımak zorundadır:

{
  "decision_id": "uuid",
  "decision_type": "priority|warning|nudge",
  "explanation": {
    "student": "Basit açıklama",
    "coach": "Analitik gerekçe",
    "system": {
      "events": [],
      "signals": [],
      "mapping_version": "v1.0",
      "engine_version": "bs_model_v2",
      "timestamp": "ISO-8601"
    }
  }
}

5️⃣ Forbidden Explainability (Yasaklı Açıklamalar)

Aşağıdaki türde açıklamalar kesinlikle yasaktır:

❌ “Çünkü sistem böyle dedi”
❌ “Algoritma böyle hesapladı”
❌ “AI önerdi”
❌ “Genel başarı düşüktü”

📌 Bunlar açıklama değildir, kaçıştır.

6️⃣ Explainability ≠ Pedagoji (Kritik Ayrım)

Explainability:

Neyi neden gördüğünü açıklar

Pedagoji:

Nasıl öğrenileceğini öğretir

🔒 H Katmanı ASLA pedagojik alana girmez.

Doğru örnek:

“Bu konuda hata oranı arttı.”

Yanlış örnek:

“Bu konuyu şu yöntemle öğren.”

7️⃣ Affiliate & Navigation Uyumu (Çelişkisiz)

Explainability:

“Eksik olan alanı” açıklar

Navigation:

“Bu alanla ilgili piyasada araçlar var” der

📌 Açıklama → nötr
📌 Link → isteğe bağlı

Örnek doğru kullanım:

“Bu konu için tekrar ihtiyacı görünüyor.
İstersen bu alanda kullanılan bazı kaynaklara göz atabilirsin.”

8️⃣ Explainability Failure Handling

Eğer:

Signal eksikse

Mapping bozuksa

Engine versiyonu uyuşmuyorsa

➡️ Decision:

UI’da gizlenir

Loglanır

Coach’a “Decision withheld” olarak düşer

9️⃣ Audit & Geriye Dönük İzlenebilirlik

Her Decision:

6 ay geriye dönük izlenebilir

“Neden bu gün bu öneri vardı?” sorusu cevaplanabilir

📌 Bu, hukuki ve etik savunma katmanıdır.

🔟 H Katmanı Felsefesi (Özet)

End.STP haklı çıkmak zorunda değildir
Ama anlaşılır olmak zorundadır

✅ H DURUMU

Kara kutu yok

Gizli algoritma yok

“AI dedi” bahanesi yok

Güven inşa edildi

I — Learning Loop & System Self-Evolution Contract
(Sistem Nasıl Öğrenir ama Öğretmen Olmaz?)
0️⃣ I Katmanının Amacı

End.STP öğrenciyi eğitmez,
sistemi eğitir.

Bu katman:

öğrenci davranışlarından

sistem hatalarından

koç müdahalelerinden
ders çıkarır

ama:

öğrenciye yeni öğrenme yöntemi öğretmez

pedagojik içerik üretmez

“nasıl öğrenilir” tarif etmez

1️⃣ Temel İlke (Anayasal)

Learning Loop, yalnızca sistem kararlarının kalitesini artırır.
Öğrenci davranışını doğrudan şekillendirmez.

📌 Bu cümle ihlal edilirse L5 bozulur.

2️⃣ Learning Loop’un Öğrendiği Şeyler (Allowed)

Sistem şunlardan öğrenebilir:

2.1 Teknik Öğrenme

Retry işe yaradı mı?

Timeout sonrası kullanıcı kaçtı mı?

Hangi endpoint darboğaz oluşturdu?

📌 Amaç: altyapıyı iyileştirmek

2.2 Karar Kalitesi Öğrenimi

Üretilen insight uygulanıyor mu?

Uygulandıktan sonra performans arttı mı?

Koç müdahalesi sonucu dropout düştü mü?

📌 Amaç: insight üretimini rafine etmek

2.3 Eşik Ayarı Öğrenimi (Threshold Tuning)

%55 remembering rate eşiği erken mi?

3 retry fazla mı?

10 saniye loading toleransı yeterli mi?

📌 Amaç: daha doğru sinyal üretmek

3️⃣ Learning Loop’un ASLA Öğrenemeyeceği Şeyler (Forbidden)

❌ “Bu öğrenci bu yöntemle daha iyi öğreniyor”
❌ “Şu video türü daha etkili”
❌ “Bu pedagojik yaklaşım daha doğru”
❌ “Şu içerik başarıyı artırıyor”

➡️ Bunlar öğretim bilimidir, End.STP alanı değildir.

4️⃣ Learning Loop Girdi Türleri
Kaynak	Tür	Amaç
Event Logs	Teknik	Sistem sağlığı
Signal History	Analitik	Karar doğruluğu
Insight Outcome	Sonuç	Etki ölçümü
Coach Action	İnsan	Müdahale etkisi
Retry Metrics	Sistem	Dayanıklılık
5️⃣ Öğrenme Döngüsü (Formal Akış)
Decision Üretildi
      ↓
Uygulandı mı?
      ↓
Sonuç Gözlendi
      ↓
Signal Değişti mi?
      ↓
Threshold / Mapping Ayarı


📌 Decision değişmez
📌 Decision üretme koşulları değişir

Bu çok kritik bir ayrımdır.

6️⃣ Self-Evolution Sınırları (Safety Rails)

Sistem:

kendi mapping’ini güncelleyebilir

retry sayısını ayarlayabilir

escalation süresini optimize edebilir

Ama:

yeni signal TANIMLAYAMAZ

taxonomy dışına çıkamaz

insan onayı olmadan contract değiştiremez

7️⃣ İnsan Onayı Gerektiren Evrimler

Aşağıdaki değişiklikler manuel onay ister:

Yeni Signal Type

Insight Severity değişimi

Coach uyarı eşiklerinin kayması

Öğrenciye gösterilen metin formatı

📌 Bunlar Anayasa Değişikliği sayılır.

8️⃣ Öğrenme Kayıtları (Auditability)

Her öğrenme adımı şunu loglar:

{
  "learning_event": "threshold_adjustment",
  "before": 55,
  "after": 60,
  "reason": "false_positive_rate_high",
  "approved_by": "system|human",
  "timestamp": "ISO-8601"
}


📌 Geri alınabilir
📌 İzlenebilir
📌 Savunulabilir

9️⃣ “6 Ay Kimse Yoksa” Senaryosu

Bu katman sayesinde:

sistem çökmez

yanlış öğrenme yapmaz

pedagojik diktaya dönüşmez

sadece daha az hata yapar

➡️ Organizma gibi yaşar ama mutasyona uğramaz

🔟 I Katmanı Özeti

End.STP öğrenir
Ama öğretmez
Uyarlanır
Ama yönlendirmez
Gelişir
Ama haddini bilir

✅ I DURUMU

Self-healing ✔

Self-learning ✔

Pedagoji ihlali ❌

Kara kutu ❌
J — Failure, Abuse & Adversarial Scenarios
(Sistemi Kandırmaya Çalışan Aktörlere Karşı Savunma Kontratı)
0️⃣ J Katmanının Amacı

End.STP yalnızca hatalara dayanıklı değil,
kasıtlı manipülasyona karşı dirençli olmak zorundadır.

Bu katman:

kötü niyetli öğrenci

çıkar çatışması olan koç

metrik manipüle eden kurum
senaryolarını önceden varsayar ve sistematik olarak sınırlar.

1️⃣ Temel İlke (Anayasal)

End.STP kimseye güvenmez; sadece tutarlılığa inanır.

Beyan ≠ Gerçek

Niyet ≠ Davranış

Rol ≠ Masumiyet

2️⃣ Tehdit Aktörleri (Threat Actors)
2.1 Öğrenci (Individual Adversary)

Amaçları:

Daha az çalışıp iyi görünmek

Sistemi “kolay” modda tutmak

Koçu / kurumu yanıltmak

2.2 Koç (Professional Adversary)

Amaçları:

Kendi başarısını yüksek göstermek

Riskli öğrenciyi gizlemek

Müdahale eksikliğini örtmek

2.3 Kurum (Organizational Adversary)

Amaçları:

KPI’ları şişirmek

Sistemsel sorunları gizlemek

Üst yönetime “sorunsuzluk” algısı vermek

3️⃣ Öğrenci Kaynaklı Manipülasyon Senaryoları
J3.1 Bilerek Yanlış Test Girişi

Örnek:

Süreyi kısa girme

Doğru sayısını şişirme

Boşları azaltma

Tespit Mekanizması:

Tarihsel hız / doğruluk tutarsızlığı

Ani performans sıçramaları

Telemetri ↔ test verisi uyumsuzluğu

Sistem Tepkisi:

🔕 Öğrenciye suçlama YOK

⚠️ Koça “Tutarsız Veri Sinyali”

📉 Confidence düşürülür

J3.2 “Sessiz Kaçış” (Dropout Masking)

Örnek:

Sistemi açıp işlem yapmamak

Loading aşamasında bekleyip çıkmak

Tespit:

Idle + session abort pattern

Repeated short sessions

Tepki:

Öğrenciye yumuşak ayna mesajı

Koça erken uyarı

Kuruma trend raporu

4️⃣ Koç Kaynaklı Manipülasyon Senaryoları
J4.1 Müdahale Gizleme

Örnek:

Müdahale yapılmadığı halde “takip ediliyor” işareti

Tespit:

Action log ≠ dashboard beyanı

Zaman / sonuç uyumsuzluğu

Tepki:

Koç görünümünde pasif işaretleme

Kuruma anonim performans sinyali

Süper Admin’e audit flag

J4.2 Aşırı Müdahale (Over-Coaching)

Örnek:

Her düşük sinyalde müdahale

Öğrencinin özerkliğini bozma

Tespit:

Müdahale / sinyal oranı anomalisi

Tepki:

Koça “Over-Intervention Risk”

Öğrenciye yansıtma YOK

5️⃣ Kurum Kaynaklı Manipülasyon Senaryoları
J5.1 Toplu Veri Şişirme

Örnek:

CSV ile toplu yüksek başarı girişi

Tespit:

Dağılım anormalliği

Şube ↔ bireysel sapma

Tepki:

Kurum panelinde “Veri Güvenilirliği Düşük”

Süper Admin audit queue

J5.2 Altyapı Sorununu Gizleme

Örnek:

Sistem yavaş ama rapor “öğrenci kaynaklı” gösteriliyor

Tespit:

Backend latency ↔ dropout korelasyonu

Tepki:

Kuruma altyapı sinyali

Öğrenci / koç suçlanmaz

6️⃣ Adversarial Pattern Registry

Her şüpheli durum:

{
  "pattern_type": "data_manipulation",
  "actor_role": "student|coach|institution",
  "confidence": 0.82,
  "impact_scope": "individual|group|system",
  "recommended_action": "observe|escalate|audit"
}


📌 Hiçbir zaman otomatik ceza YOK
📌 Sadece görünürlük + denge

7️⃣ False Positive Güvencesi

End.STP, yanlış alarm vermekten utanç duyar.

Tekil sinyal → ceza YOK

En az 2 bağımsız kanal

Zaman içinde doğrulama

8️⃣ Etik Güvence

Öğrenci suçlanmaz

Koç teşhir edilmez

Kurum etiketlenmez

➡️ Sistem davranışı düzeltir, insanı damgalamaz.

9️⃣ Süper Admin Yetkileri (J Katmanı)

Süper Admin:

Audit açabilir

Pattern’ı kalıcı hale getirebilir

Threshold resetleyebilir

Kurum / koç / öğrenci seviyesinde inceleme yapabilir

Ama:

Veri manipüle edemez

Sonuçları silemez

🔟 J Katmanı Özeti

End.STP iyi niyete güvenmez
Ama kötü niyeti de cezalandırmaz
Dengesizliği ifşa eder
İnsan onurunu korur

✅ J DURUMU

Manipülasyon Direnci ✔

Etik Güvence ✔

Kara Liste ❌

Otomatik Ceza ❌
K — Legal, Compliance & Liability Shield
(Hukuki Dayanıklılık, Veri Koruma ve Sorumluluk Sınırları)
0️⃣ K Katmanının Amacı

End.STP teknik olarak güçlü olabilir,
ama hukuken savunulamazsa yok hükmündedir.

Bu katman:

GDPR / KVKK uyumu

veri işleme sınırları

öneri kaynaklı zarar iddiaları

rol bazlı sorumluluk ayrımı

konularını anayasal düzeyde tanımlar.

1️⃣ Temel Hukuki İlke (Anayasal)

End.STP bir karar verici değil, bir analiz ve yön bulma (navigation) sistemidir.

Bu cümle:

tüm hukuki savunmaların çekirdeğidir

ürün metinleri, sözleşmeler, UI dili buna göre şekillenir

2️⃣ Rol Bazlı Hukuki Sorumluluk Ayrımı
2.1 Öğrenci

End.STP:

öğretmez

zorlamaz

garanti vermez

Öğrenci:

kendi öğrenme eylemlerinden sorumludur

dış içerikleri kendi iradesiyle kullanır

📌 Hukuki Sonuç:

“Sistem önerdi ama ben yaptım” → sorumluluk öğrencide kalır

2.2 Koç

End.STP:

koça insight verir

karar almasını kolaylaştırır

yerine karar almaz

Koç:

pedagojik / psikolojik yönlendirmeden sorumludur

kuruma karşı profesyonel sorumluluğa sahiptir

📌 Hukuki Sonuç:

Koçun verdiği karar → End.STP’ye yüklenemez

2.3 Kurum

End.STP:

altyapı ve analiz sağlar

trend ve risk raporları sunar

Kurum:

öğrenci politikalarından

rehberlik uygulamalarından

iç yönetmeliklerden sorumludur

📌 Hukuki Sonuç:

Kurumsal kararlar End.STP tarafından “tavsiye edilmiş” sayılmaz

2.4 End.STP (Sistem)

End.STP hiçbir durumda:

eğitim kurumu

öğretmen

koç

terapist

içerik sağlayıcı

olarak konumlanmaz.

3️⃣ GDPR / KVKK Uyumu (Veri Koruma)
3.1 Veri Türleri Ayrımı
Veri Türü	Kapsam	Hukuki Statü
Kimlik (ID)	UUID	Pseudonymous
Akademik veri	Test sonucu	Meşru menfaat
Telemetri	Davranışsal	Açık rıza
Insight	Türetilmiş veri	Profiling (kontrollü)
3.2 Açık Rıza Gerektirenler

Davranışsal telemetri

Frustration / dropout risk sinyalleri

Koç & kurum ekranlarında görünen psikometrik türevler

📌 UI’da açık ve geri alınabilir onay şarttır.

3.3 Profiling Sınırı

End.STP profil çıkarır,
ama otomatik karar almaz.

Otomatik ceza YOK

Otomatik yönlendirme YOK

İnsan müdahalesi her zaman mümkündür

➡️ GDPR Madde 22 uyumu

4️⃣ “Bu Öneri Yüzünden Zarar Gördüm” Senaryosu
4.1 Sistem Savunma Mantığı

End.STP şunu söyler:

“Bu bir öneri değil, analitik tespittir.”

Sistem:

“Şunu yap” DEMEZ

“Bunu öğren” DEMEZ

“Bunu izle” DEMEZ

Sistem:

“Şu alanda risk var”

“Bu eksiklik gözlemlendi”

“Piyasada şu tür araçlar mevcut”

4.2 Affiliate & Linkler ile Çelişmez

Affiliate linkleri:

isteğe bağlıdır

“zorunlu” değildir

“başarı garantisi” içermez

📌 Hukuki Metinlerde:

“Yönlendirmeler bilgilendirme amaçlıdır.”

5️⃣ Veri Saklama & Silme Politikası
5.1 Öğrenci Talebi

KVKK / GDPR kapsamında:

veri indirme

veri silme

profil kapatma

hakları tanımlıdır.

📌 Ancak:

anonimleştirilmiş sistem metrikleri silinmez

aggregate trendler korunur

5.2 Kurumdan Ayrılma

Öğrenci kurumdan ayrılırsa:

bireysel hesabı devam edebilir

kurumsal erişim kesilir

6️⃣ Log, Audit ve Hukuki İz

End.STP her önerinin nedenini saklar.

Insight üretim nedeni

Kullanılan sinyaller

Versiyon bilgisi

Zaman damgası

➡️ Bu kayıtlar:

hukuki savunmada

itirazlarda

denetimlerde kullanılır

7️⃣ Yetki & Sorumluluk Zinciri
End.STP → Analiz üretir
Koç → Karar verir
Öğrenci → Eylemi yapar
Kurum → Politikayı belirler


Bu zincir hiçbir zaman kırılmaz.

8️⃣ Yasaklı Dil (UI / Metin)

Aşağıdaki ifadeler yasaktır:

❌ “Bu şekilde çalışmalısın”
❌ “Bunu yapmazsan başaramazsın”
❌ “Bu içerik zorunlu”
❌ “End.STP sana öğretecek”

9️⃣ Süper Admin (End.STP) Hukuki Yetkileri

Audit başlatabilir

Veri işleme sınırlarını günceller

Kurum sözleşmelerini yönetir

Ama:

bireysel kararlara müdahale edemez

veriyi manipüle edemez

🔟 K Katmanı Özeti

End.STP:

öğretmez

zorlamaz

karar almaz

Ama her kararın nedenini görünür kılar.

✅ K DURUMU

GDPR / KVKK uyumu ✔

Liability Shield ✔

Affiliate uyumu ✔

Hukuki savunulabilirlik ✔
L — Product Language, UI Copy & Legal Tone Guide
(Hangi ekranda hangi kelime asla yazılmayacak?)
0️⃣ L Katmanının Amacı

Yanlış kelime = yanlış vaad = hukuki risk

Bu kılavuz:

UI metinlerini standartlaştırır

pedagojik diktatörlüğü engeller

affiliate / yönlendirme yapısını çelişkisiz kılar

tüm roller için aynı hukuki dili zorunlu kılar

1️⃣ Altın Dil İlkesi (Anayasal)

End.STP öğretmez, zorlamaz, garanti vermez.
End.STP analiz eder, görünür kılar, yön buldurur.

Bu ilke tüm UI, tooltip, toast, modal, e-posta, PDF, rapor için geçerlidir.

2️⃣ Yasaklı Dil – Evrensel Liste (Tüm Sistem)

Aşağıdaki ifadeler hiçbir koşulda kullanılmaz:

❌ “Şunu öğren”
❌ “Bunu çalış”
❌ “Bu yöntemle öğren”
❌ “Bu videoyu izle”
❌ “Bunu yaparsan başarırsın”
❌ “Zorunlu”
❌ “Garantili”
❌ “En doğru yol”
❌ “Tek çözüm”

📌 Gerekçe:

pedagojik yönlendirme

garanti algısı

hukuki sorumluluk devri

3️⃣ İzinli Dil – Evrensel Şablonlar

Aşağıdaki kalıplar her yerde serbesttir:

✅ “Analize göre…”
✅ “Verilere dayanarak…”
✅ “Şu alanda eksiklik gözlemlendi”
✅ “Bu başlık öncelikli görünüyor”
✅ “Piyasada bu ihtiyaca yönelik araçlar bulunuyor”
✅ “İstersen göz atabilirsin”
✅ “Karar sana ait”

4️⃣ Ekran Bazlı Dil Kuralları
4.1 Öğrenci Dashboard

YASAK:

“Bugün şunu çalış”

“Bu konuyu bitir”

“Şu kadar soru çözmelisin”

SERBEST:

“Son test verilerine göre bu konu daha fazla tekrar gerektirebilir”

“İlerlemeni desteklemek için bu başlık öncelikli görünüyor”

4.2 Test Sonucu & Analiz Ekranı

YASAK:

“Yanlış öğrenmişsin”

“Bu konuyu bilmiyorsun”

SERBEST:

“Bu testte hata oranı yükseldi”

“Zaman kullanımında dalgalanma gözlemlendi”

4.3 Insight / Öneri Kartları

YASAK:

“Bunu yap”

“Şu yolu izle”

SERBEST:

“Analiz bu alanda risk işaret ediyor”

“Bu başlık için farklı çalışma araçları bulunuyor”

4.4 Affiliate / Dış Link Alanları

YASAK:

“Bunu izlemeden olmaz”

“Bu içerik zorunlu”

“End.STP öneriyor”

SERBEST:

“Bu başlık için piyasada bulunan isteğe bağlı kaynaklar”

“Harici platform – End.STP içeriği değildir”

📌 Zorunlu Dipnot (küçük puntoda):

“Bu bağlantılar bilgilendirme amaçlıdır. End.STP içerik sağlayıcısı değildir.”

4.5 Koç Paneli

YASAK:

“Öğrenci şunu yapmalı”

“Şu yöntemi uygulat”

SERBEST:

“Öğrencide bu alanda tekrar eden zorlanma sinyali var”

“Müdahale gerektirebilecek bir blokaj gözlemleniyor”

4.6 Kurum & Yönetici Panelleri

YASAK:

“Bu öğrenciler başarısız”

“Bu sınıf öğrenemiyor”

SERBEST:

“Bu grupta risk yoğunluğu artış eğiliminde”

“Sistemsel veya davranışsal darboğaz sinyalleri mevcut”

5️⃣ Modal, Toast, Alert Metinleri
5.1 Hata Mesajları

YASAK:

“Bir şeyler yanlış gitti”

“Sistem hatası”

SERBEST:

“Geçici bir bağlantı sorunu gözlemlendi”

“Veri yüklenirken gecikme oluştu”

5.2 Retry / Loading Metinleri

Standart Metin:

“Yükleniyor… Sistem verileri senin için hazırlıyor.”

Timeout Sonrası:

“Bağlantı şu anda yanıt vermiyor. İstersen tekrar deneyebilirsin.”

6️⃣ Explainability Metinleri (H Katmanı ile Uyum)

Her insight için:

ZORUNLU ŞABLON:

“Bu tespit, son X testteki Y ve Z sinyallerine dayanır.”

❌ “Sistem böyle dedi”
✅ “Şu veriler kullanıldı”

7️⃣ Dil Versiyonlama Kuralı

UI metinleri versiyonlanır

her değişiklik:

tarih

gerekçe

hukuki not

ile kayıt altına alınır.

8️⃣ L Katmanı Denetim Kuralı

Yeni bir ekran → Dil checklist’i zorunlu

Yeni bir metin → yasaklı kelime taraması

Affiliate metni → hukuki dipnot kontrolü

9️⃣ L Katmanı Özeti

End.STP konuşur ama buyurmaz.
Gösterir ama yönlendirmez.
Açıklar ama öğretmez.

✅ L DURUMU

Hukuki dil güvenliği ✔

Pedagojik nötrlük ✔

Affiliate uyumu ✔

Global-first ürün dili ✔
M — Release Governance & Change Control
(Bu anayasa değişirse kim, nasıl, ne zaman değiştirebilir?)
0️⃣ M Katmanının Amacı

Kuralsız değişim = teknik borç + hukuki risk + ürün kimliği erozyonu

M Katmanı:

Anayasanın keyfi değişmesini engeller

Kimlerin hangi kapsamda değişiklik yapabileceğini netleştirir

Sistemi insana bağımlı olmaktan çıkarır

End.STP’nin “organizma” gibi kontrollü evrimini sağlar

1️⃣ Yetki Hiyerarşisi (Bağlayıcı)
1.1 Mutlak Yetkili (Super Admin – End.STP)

📌 Rol: End.STP Süper Üst Admin
📌 Yetki Seviyesi: ROOT

Super Admin:

Anayasanın tüm maddelerini değiştirebilir

Yeni katman ekleyebilir / kaldırabilir

Yetki devri yapabilir

Olağanüstü durumlarda geçici istisna tanımlayabilir

⚠️ Ancak:

Her değişiklik kayıt altına alınmak zorundadır.
Yetki sınırsızdır ama iz bırakmadan kullanılamaz.

1.2 Sınırlı Yetkililer
Rol	Yetki
Lead Engineer	Teknik kontrat & schema önerisi
Legal Advisor	Dil, KVKK, GDPR veto hakkı
Product Owner	UI / UX metni önerisi
Data / AI Lead	Signal, Insight mantığı önerisi

❌ Hiçbiri anayasayı tek başına değiştiremez.

2️⃣ Değişiklik Türleri (Classification)

Her değişiklik aşağıdaki sınıflardan birine girer:

M1 — Dil & UI Değişikliği

Metin güncellemesi

Kelime yasakları

Ton değişimi

📌 Risk: Orta
📌 Onay: Super Admin + Legal

M2 — Teknik Kontrat Değişikliği

Event / Signal / Insight şeması

Retry politikası

Escalation mantığı

📌 Risk: Yüksek
📌 Onay: Super Admin + Lead Engineer

M3 — Yetki & Rol Değişikliği

Koç / kurum / öğrenci yetkileri

Admin sınırları

📌 Risk: Çok Yüksek
📌 Onay: Super Admin (tek başına) + kayıt zorunlu

M4 — Hukuki & Compliance Değişikliği

KVKK / GDPR

Sorumluluk reddi

Veri işleme sınırları

📌 Risk: Kritik
📌 Onay: Legal veto hakkı vardır

3️⃣ Değişiklik Süreci (Zorunlu Akış)

Hiçbir değişiklik şu adımlar atlanarak yapılamaz:

1️⃣ Değişiklik Talebi (Proposal)

Her değişiklik:

Ne değişiyor

Neden

Hangi madde etkileniyor

Risk seviyesi

ile yazılı olarak tanımlanır.

2️⃣ Etki Analizi (Impact Check)

Aşağıdaki sorular cevaplanır:

Öğrenciye yanlış vaade yol açar mı?

Koç veya kuruma pedagojik yük bindirir mi?

Hukuki sorumluluk doğurur mu?

Önceki sinyallerle çelişir mi?

📌 Tek bir “Evet” varsa → ileri gidilmez.

3️⃣ Onay & Versiyonlama

Onaylanan her değişiklik:

Version: vX.Y.Z
Date:
Changed by:
Change Type: M1 / M2 / M3 / M4
Reason:
Backward Compatibility: Yes / No


formatıyla kaydedilir.

4️⃣ Versiyonlama Kuralları (Anayasa)

Major (X): Mantık değişti

Minor (Y): Kapsam genişledi

Patch (Z): Açıklama / dil düzeltmesi

📌 Major değişiklikler geriye dönük uyumsuz olabilir.

5️⃣ Geri Alma (Rollback) Kuralı

Her değişiklik için:

Önceki sürüm saklanır

24–72 saat izleme süresi vardır

Beklenmeyen sonuçta anında geri alınır

6️⃣ Olağanüstü Durum Yetkisi (Emergency Override)

Sadece şu durumlarda:

Hukuki risk

Veri ihlali

Yanlış yönlendirme zinciri

Sistem bütünlüğü riski

📌 Super Admin:

Geçici karar alabilir

Ancak sonradan gerekçelendirmek zorundadır

7️⃣ İnsan Faktörüne Karşı Güvence

Anayasa, iyi niyetli hatalara karşı da korumalıdır.

Bu yüzden:

“Bence böyle daha iyi” gerekçe değildir

“Kullanıcı istedi” tek başına yeterli değildir

“Rakip yapıyor” geçerli sebep değildir

8️⃣ M Katmanı Özeti

End.STP kendini geliştirir ama rastgele evrimleşmez.
Değişir ama kimliğini kaybetmez.
Güç vardır ama disiplinle kullanılır.

✅ M DURUMU

Yetki sınırları net ✔

Keyfi değişim engellendi ✔

Hukuki & teknik güvence ✔

Organizma-vari ama kontrollü evrim ✔

N — Auditability & External Review Protocol
(Bağımsız denetçi / yatırımcı / kamu otoritesi bu sistemi nasıl inceler?)
0️⃣ N Katmanının Amacı

“Güven” iddia edilmez, ispatlanır.

N Katmanı:

End.STP’nin iç mantığını dış gözlere açar

“Kara kutu” algısını bilinçli olarak kırar

Hukuki, etik ve teknik denetimlere hazır olma halini tanımlar

Yatırımcı, kamu ve kurumlar için tekil doğrulama noktası oluşturur

1️⃣ Denetçi Tipleri & Bakış Açıları
1.1 Bağımsız Teknik Denetçi (Audit / Security / Data)

Sorduğu Sorular:

Sistem hangi veriyi topluyor?

Bu veriler nasıl işleniyor?

Karar üretim zinciri izlenebilir mi?

Hata ve riskler nasıl ele alınıyor?

End.STP’nin Cevabı:

Event → Signal → Insight zinciri tam loglanır

Her Insight için:

kaynak event’ler

mapping versiyonu

karar gerekçesi

kullanıcıya gösterilen dil
kayıt altındadır

1.2 Kamu Otoritesi (KVKK / GDPR / Regülatör)

Sorduğu Sorular:

Kişisel veri var mı?

Profil çıkarma yapılıyor mu?

Otomatik kararlar zarara yol açabilir mi?

Kullanıcı itiraz edebilir mi?

End.STP’nin Cevabı:

Kişisel veri → minimize edilmiş

Pedagojik karar → üretilmez

Otomatik öneriler → bağlayıcı değildir

Her kullanıcı için:

“Bu öneri neden üretildi?” açıklaması vardır

itiraz ve geri bildirim mekanizması mevcuttur

1.3 Yatırımcı / Kurumsal Alıcı

Sorduğu Sorular:

Sistem ölçeklenebilir mi?

Tek kişiye bağımlı mı?

Riskler kontrol altında mı?

Yanlış karar üretirse ne olur?

End.STP’nin Cevabı:

Tüm kararlar kontrata bağlıdır

İnsan bağımlılığı yoktur

Yanlış karar:

bağlayıcı değildir

geri alınabilir

öğrenme verisine dönüşür

Governance (M) + Audit (N) birlikte çalışır

2️⃣ Denetim Yüzeyleri (Audit Surfaces)

Denetim tek noktadan değil, katmanlı yapılır.

2.1 Veri Yüzeyi (Data Surface)

Event kayıtları

Telemetri (anonimleştirilmiş)

Feedback logları

📌 Denetçi şunu görür:

“Bu veri neden toplanmış, nerede kullanılmış, ne zaman silinecek?”

2.2 Karar Yüzeyi (Decision Surface)

Her Insight için:

Insight_ID
Triggered_By: [Event_IDs]
Signal_Version
Mapping_Version
Severity
Escalation_Path
Shown_To_User: Yes / No


📌 Denetçi şunu görür:

“Bu çıktı hangi mantıkla üretildi?”

2.3 Dil & Sunum Yüzeyi (UI / Copy)

Yasaklı kelime listesi (L Katmanı)

Gösterilen metin ile iç karar ayrıdır

Öğrenciye gösterilen ifade:

yönlendirici değil

bağlayıcı değil

pedagojik iddia içermez

3️⃣ Denetim Modları
N1 — Read-Only Audit Mode

Hiçbir veri değiştirilemez

Sadece:

loglar

kontratlar

versiyonlar
görülebilir

📌 Kamu & yatırımcı için varsayılan mod

N2 — Scenario Replay Mode

Seçili bir olay zinciri alınır

Event → Signal → Insight tekrar çalıştırılır

Aynı sonucu üretip üretmediği gözlemlenir

📌 Teknik denetimler için kritik

N3 — Stress & Edge Case Review

Aykırı senaryolar

Yanlış veri

Kötü niyetli kullanım

📌 J Katmanı ile entegredir

4️⃣ Denetim Kayıtları (Audit Logs)

Her denetim:

Audit_ID
Auditor_Type
Scope
Start_Date
End_Date
Findings
Risk_Level
Actions_Taken


şeklinde kaydedilir.

📌 Denetim kendisi de denetlenebilir olmalıdır.

5️⃣ Şeffaflık Seviyeleri (Disclosure Levels)
Seviye	Kim Görür	Kapsam
L1	Öğrenci	Kendi verisi + açıklama
L2	Koç	Öğrenci sinyalleri
L3	Kurum	Trend & risk
L4	Denetçi	Tüm sistem mantığı
L5	Super Admin	Tam erişim
6️⃣ “Black Box” Reddi (Temel İlke)

End.STP bir AI motoru değildir.
Analitik navigasyon sistemidir.

Bu yüzden:

“Model böyle dedi” yok

“Algoritma öyle uygun gördü” yok

Her çıktının yazılı gerekçesi vardır

7️⃣ N Katmanı Özeti

Denetlenebilirlik varsayılan ✔

Karar zinciri izlenebilir ✔

Hukuki & yatırımcı uyumu ✔

Kara kutu yok ✔

🔒 STRATEJİK NOT

Bu katman sayesinde End.STP:

kamuya açılabilir

kurumsal satın almaya uygundur

yatırımcı due-diligence’ı geçebilir

“etik teknoloji” iddiasını kanıtlayabilir
O — External API & Partner Audit Contract

(API satan End.STP nasıl denetlenir?)

Amaç:
End.STP’nin başka platformlara, kurumlara, üniversitelere veya yayıncılara API verdiği durumda
→ güvenlik, yetki, sorumluluk ve denetlenebilirliği anayasal düzeyde garanti altına almak.

Bu bölüm de master.md’ye birebir yapıştırılabilir.

0️⃣ Neden O Katmanı Ayrı?

Çünkü API satışı, sistemin en riskli noktasıdır:

Kontrol senin UI’ında değildir

Yanlış kullanım sana fatura edilebilir

“Bu öneri yüzünden zarar gördüm” iddiası API üzerinden gelir

👉 O Katmanı yoksa:

L5 mimari kurumsal satışa hazır değildir

Yatırımcı “scale risk” der

1️⃣ External Consumer Tipleri
1.1 API Client Türleri
Client Tipi	Örnek
EdTech Platform	LMS, ölçme sistemi
Kurum / Üniversite	Kendi paneline gömme
Yayıncı	Analitik + yönlendirme
Araştırma Kurumu	Anonim analiz

Her biri farklı yetki ve sorumluluk taşır.

2️⃣ API Audit Contract (Zorunlu Şartlar)

Bir dış sistem End.STP API’sini kullanıyorsa şu kontratı kabul eder:

2.1 Zorunlu Kabul Maddeleri

End.STP pedagojik içerik üretmez

Üretilen çıktılar:

bağlayıcı değildir

öneri niteliğindedir

Son karar:

kullanıcıya

koça

kuruma aittir

📌 Bu madde API response header’ına bile yazılabilir.

3️⃣ API Event & Insight Sınırları
3.1 API’nin Görebileceği

✅ Event (anonimleştirilmiş)
✅ Signal (tip + seviye)
✅ Insight (metinsel açıklama)

3.2 API’nin Asla Göremeyeceği

❌ Ham telemetri (mouse, dwell time raw)
❌ Psikolojik etiketler
❌ Öğrenciye gösterilen UI metni
❌ Koç içgörüleri

API navigasyonu verir,
insanı ifşa etmez.

4️⃣ Partner Audit Mode

API client’ları için zorunlu audit modu vardır.

O1 — API Replay Audit

Belirli request’ler seçilir

Aynı Event → Signal → Insight zinciri

Tekrar çalıştırılır

📌 “Aynı girdiye aynı çıktı mı?” sorusu test edilir.

O2 — Rate & Abuse Audit

Aşırı çağrı

Pattern abuse

Data scraping

Tespit edilirse:

otomatik throttle

gerekirse anahtar iptali

5️⃣ Versiyon & Geriye Dönük Uyumluluk

Her API response:

signal_registry_version

mapping_version

insight_contract_version
içerir

📌 Dış sistem:

“Bu kararı hangi anayasa üretmiş?”
sorusuna cevap alır.

6️⃣ Hukuki Sorumluluk Çerçevesi

API üzerinden gelen bir şikayette:

End.STP logları sunar

Kararın bağlayıcı olmadığı gösterilir

İçerik sunulmadığı ispatlanır

UI dili End.STP tarafından kontrol edilmediği belirtilir

📌 Sorumluluk paylaşımlıdır, tek taraflı değildir.

7️⃣ O Katmanı Özeti

API kara kutu değildir ✔

Yetki & sınır nettir ✔

Denetlenebilirlik korunur ✔

Kurumsal satış güvenlidir ✔

ŞİMDİ GEÇİYORUZ 👇
I — Learning Loop & System Self-Evolution Contract

(Sistem nasıl öğrenir, neyi öğrenmez?)

Bu katman kritik.
Çünkü yanlış yapılırsa sistem pedagojik diktatörlüğe dönüşür.

0️⃣ Temel İlke (ÇİVİ)

End.STP öğrenir ama öğretmez.
Davranışı analiz eder ama yönlendirme dikte etmez.

1️⃣ Sistem Ne Öğrenir?
1.1 Öğrenebileceği Şeyler (SERBEST)

✅ Hangi insight işe yaradı
✅ Hangi sinyal yanlış alarm üretti
✅ Retry başarılı mı oldu
✅ Kullanıcı öneriyi görüp harekete geçti mi
✅ Koç müdahalesi sonrası kopma azaldı mı

📌 Bunlar sistem performansıdır, pedagojik bilgi değildir.

1.2 Asla Öğrenmeyeceği Şeyler (YASAK)

❌ “Bu yöntemle daha iyi öğrenir”
❌ “Bu video en etkilisi”
❌ “Bu öğrenci şu tiptir”
❌ Öğrenciye psikolojik etiketleme

2️⃣ Learning Loop Aşamaları
I1 — Observation

Event, Signal, Insight sonuçları izlenir

Sonuçlar etiketlenmez, sadece ölçülür

I2 — Outcome Tracking

Insight sonrası:

yeni test girişi oldu mu?

sistem terk edildi mi?

koç müdahalesi geldi mi?

I3 — Policy Adjustment (Sınırlı)

Sistem sadece şunu yapabilir:

eşik değerlerini ayarlamak

retry sayılarını optimize etmek

escalation zamanlamasını düzeltmek

📌 İçerik, yöntem, öğrenme biçimi yok.

3️⃣ Human-in-the-Loop Zorunluluğu

Bazı şeyler asla otomatikleşmez:

Kritik motivasyon düşüşü

Drop-out riski

Etik sınır ihlali

➡️ Bu noktada:

Koç

Kurum

Super Admin

insan müdahalesi şarttır

4️⃣ Öğrenmenin Kayıt Altına Alınması

Her “öğrenme”:

Learning_Event_ID
Triggered_By
Change_Type
Before_State
After_State
Approval_Type (auto / human)


şeklinde loglanır.

📌 Sistem kendi evrimini bile denetler.

5️⃣ “Altı Ay Yoksak Bile” Prensibi

Bu kontrat sayesinde:

Sistem çalışmaya devam eder

Ama sınırları genişlemez

Yeni davranış icat etmez

Sadece optimize eder

Organizma yaşar ama karakter değiştirmez.

6️⃣ I Katmanı Özeti

Öğrenme var ✔

Pedagoji yok ✔

Otonomi sınırlı ✔

İnsan her zaman üstte ✔

🔐 KAPANIŞ NOTU

Buraya kadar kurduğumuz yapı şunu garanti eder:

End.STP akıllı ama alçakgönüllü,
güçlü ama haddini bilen bir sistemdir.
Q — Ethical Red Lines & Kill-Switch Protocol

(“Bir gün durmak gerekirse, sistem nasıl DURUR?”)

Amaç:
End.STP’nin yanlış yöne evrilmesini, etik sınır aşımını, hukuki/itibar riskini ve algoritmik zorbalığı önceden ve kesin şekilde engellemek.

Q0 — Değişmez İlke (Çivi)

End.STP, sonuç üretmeyi bırakabilir;
etik sınırı aşmayı asla sürdürmez.

Q1 — Ethical Red Lines (Aşılması Yasak Kırmızı Çizgiler)

Aşağıdaki ihlallerden herhangi biri tespit edilirse Kill-Switch tetiklenir.

Q1.1 Pedagojik Diktatörlük (YASAK)

“Şunu öğrenmelisin”

“Bunu izlemeden ilerleyemezsin”

“Bu yöntemi uygula”

İçerik/öğretim zorunluluğu

➡️ İhlal Tipi: Etik + Pedagojik
➡️ Aksiyon: Otomatik durdurma

Q1.2 Psikolojik Etiketleme (YASAK)

“Bu öğrenci tembel”

“Zihinsel kapasitesi düşük”

Kalıcı kişilik/zeka etiketleri

➡️ İhlal Tipi: Etik + Hukuki
➡️ Aksiyon: Otomatik durdurma + audit

Q1.3 Karar Bağlayıcılığı (YASAK)

Önerinin tek doğru gibi sunulması

Alternatifsiz yönlendirme

➡️ İhlal Tipi: Hukuki
➡️ Aksiyon: Otomatik durdurma

Q1.4 Yetkisiz Öğrenme (YASAK)

Sistem kendi başına:

yeni pedagojik kural üretirse

kapsam genişletirse

davranış icat ederse

➡️ İhlal Tipi: Sistemsel
➡️ Aksiyon: Kill-Switch + rollback

Q2 — Kill-Switch Türleri
Q2.1 Soft Kill (Kademeli Durdurma)

Ne zaman?

Şüpheli sinyal artışı

Belirsiz etik risk

Ne yapar?

Yeni insight üretimini durdurur

Mevcut analizleri “read-only” yapar

Loglamaya devam eder

Q2.2 Hard Kill (Acil Durdurma)

Ne zaman?

Kırmızı çizgi ihlali kesinleştiyse

Ne yapar?

Event → Signal → Insight zinciri durur

API cevapları “degraded safe mode” olur

UI sadece geçmiş veriyi gösterir

Q2.3 Scoped Kill (Alan Bazlı)

Ne zaman?

Sadece belirli bir modül riskliyse

Ne yapar?

Örn. “Motivation inference” kapatılır

Diğer modüller çalışır

Q3 — Kill-Switch Tetikleyiciler
Tetikleyici	Kaynak
Red Line ihlali	Otomatik
Anormal model drift	Otomatik
Hukuki bildirim	Manual
Super Admin	Manual
Regülatör talebi	Manual
Q4 — Kill-Switch Sonrası Zorunlu Süreç

Root Cause Analysis

Etki Analizi (kim etkilendi?)

Düzeltme planı

Super Admin onayı

Controlled restart

📌 Restart asla otomatik değildir.

Q5 — Kayıt & Denetlenebilirlik

Her kill-switch olayı:

Kill_Switch_ID
Trigger_Type
Scope
Reason
Timestamp
Approved_By
Restart_Conditions


şeklinde değiştirilemez log olarak tutulur.

Q Özeti

Etik sınırlar kod seviyesinde ✔

“Dur” deme mekanizması net ✔

İnsan kontrolü en üstte ✔

R — Public Trust Manifesto

(Kamuya Açık “Biz Ne Yaparız / Ne Yapmayız” Belgesi)

Amaç:
Öğrenci, veli, koç, kurum, yatırımcı ve kamu otoritelerine
tek sayfalık, net, dürüst bir güven sözleşmesi sunmak.

📌 Bu belge web sitesinde, sözleşmelerde ve pitch’lerde aynen kullanılabilir.

R0 — Biz Kimiz?

End.STP,
öğrencinin girdiği test sonuçlarını analiz eden,
öğrenme sürecini ölçen,
riskleri erken fark eden
bir Analitik Navigasyon Sistemidir.

R1 — Biz Ne Yaparız?

✅ Test sonuçlarını analiz ederiz
✅ Öğrenme sürecindeki riskleri gösteririz
✅ Öncelik ve zamanlama önerileri üretiriz
✅ Koç ve kurumlar için erken uyarılar sağlarırız
✅ Kararların nedenini açıklarız

R2 — Biz Ne Yapmayız? (KIRMIZI LİSTE)

❌ İçerik üretmeyiz
❌ “Şunu öğren” demeyiz
❌ Tek doğru dayatmayız
❌ Psikolojik etiketleme yapmayız
❌ Öğrenci yerine karar vermeyiz

R3 — Önerilerimizin Doğası

Bağlayıcı değildir

Zorunlu değildir

Alternatiflidir

İnsan kararıyla tamamlanır

R4 — Veriye Yaklaşımımız

Gerektiği kadar veri

Amacı dışında kullanım yok

Ham telemetri gizlidir

Anonimleştirme esastır

R5 — Affiliate & Dış Kaynaklar

End.STP içerik satmaz

Piyasadaki araçlara isteğe bağlı yönlendirme yapabilir

Bu yönlendirmeler:

alternatiflidir

bağlayıcı değildir

şeffaftır

R6 — Hata ve Sorumluluk

Sistemsel hatalar izlenir

Etik ihlallerde sistem durdurulur

Nihai karar insana aittir

R7 — Şeffaflık Taahhüdü

“Bu öneri neden üretildi?”
sorusuna her zaman cevap veririz.

R8 — Güven Sözümüz

End.STP,
öğrencinin yerine düşünmez,
öğrencinin önünü aydınlatır.

R Özeti

Kamuya açık ✔

Hukuki uyumlu ✔

Pedagojik sınırları net ✔

Güven inşa eder ✔

🔒 KAPANIŞ

Bu iki bölümle birlikte:

Sistem etik olarak kilitlendi

“Dur” deme yeteneği kazandı

Kamuya yüzü ak bir manifesto oluşturuldu