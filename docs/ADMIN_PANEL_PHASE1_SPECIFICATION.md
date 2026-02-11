# 🛠️ End.STP Admin Panel - Phase 1 Specification
**Version:** 1.0  
**Date:** February 9, 2026  
**Author:** End.STP Team  
**Status:** Planning Phase  
**Target:** Before Phase 2 (TYT/AYT tracking)

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Why Admin Panel First](#why-admin-panel-first)
3. [Architecture Principles](#architecture-principles)
4. [Database Schema (Admin-Relevant)](#database-schema)
5. [Authentication & Authorization](#authentication--authorization)
6. [Feature Modules](#feature-modules)
7. [UI/UX Patterns](#uiux-patterns)
8. [Security & Compliance](#security--compliance)
9. [Implementation Roadmap](#implementation-roadmap)
10. [Success Criteria](#success-criteria)

---

## 1. EXECUTIVE SUMMARY

### Current Problem
End.STP is "working but unmanaged":
- ✅ Progress system functional (5 endpoints)
- ✅ Dashboard stable (SSR migration complete)
- ✅ Compliance 38/38 files
- ❌ Kill switch exists but no UI
- ❌ Card visibility decisions hardcoded
- ❌ Goal management impossible
- ❌ Exam weights uncontrollable

### Solution
Admin Panel MVP with 4 core modules:
1. **Dashboard Control** - Card visibility toggles
2. **Kill Switch UI** - Feature flags & emergency shutdown
3. **Exam Weight Viewer** - Read-only validation
4. **Goal Management** - Basic CRUD for student goals

### Why Now?
Cannot start Phase 2 (TYT/AYT tracking) without control plane.

---

## 2. WHY ADMIN PANEL FIRST

### The Control Problem
```
CURRENT STATE (No Admin Panel)
├─ Want to hide UniversityGoalCard? → Edit code
├─ Want to disable motor? → Edit database
├─ Want to assign goal? → Manual SQL
└─ Want to validate exam weights? → Query console

AFTER ADMIN PANEL
├─ Toggle cards → Click button
├─ Disable motor → Click switch
├─ Assign goal → Form submit
└─ Validate weights → View dashboard
```

### Risk Without Admin Panel

**Scenario:** Phase 2 başlarken UniversityGoalCard'da bug bulundu.
```
WITHOUT ADMIN PANEL:
1. Code'a gir
2. Kodu kapat
3. Deploy et
4. Test et
5. Geri aç
6. Tekrar deploy
→ 30 dakika downtime

WITH ADMIN PANEL:
1. Admin panele gir
2. Toggle'a bas
→ 10 saniye downtime
```

---

## 3. ARCHITECTURE PRINCIPLES

### 🌍 GLOBAL-FIRST (Mandatory)

**Every admin feature must follow:**
```python
# ❌ WRONG
settings = {
  "card_name": "Projection Card",
  "enabled": True
}

# ✅ CORRECT
settings = {
  "card_name_tr": "Projeksiyon Kartı",
  "card_name_en": "Projection Card",
  "enabled": True,
  "updated_at": datetime.now(timezone.utc)  # UTC!
}
```

**Admin panel metinleri:**
- Türkçe: Ana dil
- İngilizce: Gelecek için hazır
- Suffix pattern: `_tr` / `_en`

---

### 🔒 L5 Non-Invasive Principle

**CRITICAL:** Admin panel NEVER deletes existing code.
```
❌ FORBIDDEN:
- Remove dashboard components
- Delete database tables
- Modify core logic

✅ ALLOWED:
- Add visibility flags
- Create new tables
- Extend functionality
```

**Example:**
```typescript
// ❌ WRONG: Removing component
// return null; // UniversityGoalCard removed

// ✅ CORRECT: Conditional render
{showGoalCard && <UniversityGoalCard />}
```

---

### 🛡️ Two-Person Rule (Critical Operations)

**Applies to:**
1. Exam weight modifications
2. Kill switch activation (master)
3. Goal tier changes
4. RLS policy updates

**Implementation:**
```
Action Flow:
1. Admin A: Request change
2. System: Create pending approval
3. Admin B: Review diff
4. Admin B: Approve/Reject
5. System: Execute + Audit log
```

**Database Schema:**
```sql
CREATE TABLE admin_approvals (
  id UUID PRIMARY KEY,
  action_type TEXT NOT NULL,
  requested_by UUID REFERENCES auth.users(id),
  request_data JSONB NOT NULL,
  status TEXT CHECK (status IN ('pending', 'approved', 'rejected')),
  approved_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  resolved_at TIMESTAMPTZ
);
```

---

### 📊 Analytics Integrity Triangle

**Three interconnected decisions:**
```
         exam_types.total_questions
         (Merkezi kaynak, değişmez)
                    △
                   ╱ ╲
                  ╱   ╲
                 ╱     ╲
   subject_exam_weights   test_records
   (Dağılım tanımı)       (Gerçek veri)
```

**Admin Panel Validations:**

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
-- Beklenen: 0
```

**Admin Panel Exam Weight Viewer:**
- Read-only in Phase 1
- Show validation status (✅/❌)
- Display anomalies if any
- Two-Person Rule for edits (Phase 2)

---

## 4. DATABASE SCHEMA (ADMIN-RELEVANT)

### New Tables for Admin Panel

#### 4.1 Dashboard Settings
```sql
CREATE TABLE dashboard_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Card visibility
  show_projection_card BOOLEAN DEFAULT TRUE,
  show_university_goal_card BOOLEAN DEFAULT TRUE,
  show_critical_alert BOOLEAN DEFAULT TRUE,
  show_trend_chart BOOLEAN DEFAULT TRUE,
  
  -- Card behavior
  hide_goal_card_when_empty BOOLEAN DEFAULT FALSE,
  hide_projection_when_no_data BOOLEAN DEFAULT FALSE,
  
  -- Global settings
  is_active BOOLEAN DEFAULT TRUE,
  
  -- Metadata
  updated_by UUID REFERENCES auth.users(id),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  CONSTRAINT one_settings_row CHECK (id = gen_random_uuid())
);

-- Insert default settings
INSERT INTO dashboard_settings (id) 
VALUES (gen_random_uuid())
ON CONFLICT DO NOTHING;
```

#### 4.2 Feature Flags (Kill Switch)
```sql
CREATE TABLE feature_flags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  flag_key TEXT UNIQUE NOT NULL,
  flag_name_tr TEXT NOT NULL,
  flag_name_en TEXT NOT NULL,
  description_tr TEXT,
  description_en TEXT,
  
  -- Status
  is_enabled BOOLEAN DEFAULT TRUE,
  
  -- Categories
  category TEXT CHECK (category IN ('motor', 'ui', 'analytics', 'system')),
  criticality TEXT CHECK (criticality IN ('low', 'medium', 'high', 'critical')),
  
  -- Metadata
  updated_by UUID REFERENCES auth.users(id),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed data
INSERT INTO feature_flags (flag_key, flag_name_tr, flag_name_en, category, criticality) VALUES
('motor_bs_model', 'BS-Model Motor', 'BS-Model Motor', 'motor', 'high'),
('motor_priority', 'Öncelik Motoru', 'Priority Engine', 'motor', 'high'),
('motor_difficulty', 'Zorluk Motoru', 'Difficulty Engine', 'motor', 'medium'),
('motor_time', 'Zaman Analizi', 'Time Analyzer', 'motor', 'medium'),
('ui_dashboard', 'Dashboard', 'Dashboard', 'ui', 'critical'),
('ui_progress', 'İlerleme Sayfası', 'Progress Page', 'ui', 'critical'),
('analytics_trend', 'Trend Grafiği', 'Trend Chart', 'analytics', 'medium'),
('analytics_prediction', 'Tahmin Sistemi', 'Prediction System', 'analytics', 'low');
```

#### 4.3 Admin Audit Log
```sql
CREATE TABLE admin_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  admin_id UUID REFERENCES auth.users(id),
  action_type TEXT NOT NULL,
  action_category TEXT CHECK (action_category IN (
    'dashboard_settings', 'feature_flags', 'goal_management', 
    'exam_weights', 'user_management', 'system'
  )),
  
  -- Change details
  before_state JSONB,
  after_state JSONB,
  
  -- Context
  ip_address INET,
  user_agent TEXT,
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for performance
CREATE INDEX idx_audit_admin ON admin_audit_log(admin_id, created_at DESC);
CREATE INDEX idx_audit_category ON admin_audit_log(action_category, created_at DESC);
```

---

### Existing Tables (Important for Admin)

#### 4.4 student_goals (NOT user_university_goals!)

**CRITICAL:** Table name is `student_goals` not `user_university_goals`
```sql
-- Actual table structure
CREATE TABLE student_goals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  tier_id UUID REFERENCES university_tiers(id),
  target_date DATE,
  progress_percentage DECIMAL(5,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Admin Panel Actions:**
- View all goals
- Assign goal to student
- Update target date
- Delete goal
- View progress (read-only)

---

#### 4.5 university_tiers (5-Tier System)
```sql
CREATE TABLE university_tiers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tier_number INT CHECK (tier_number BETWEEN 1 AND 5),
  name_tr TEXT NOT NULL,
  name_en TEXT,
  min_rank INT,
  max_rank INT,
  weight DECIMAL(3,2),
  is_active BOOLEAN DEFAULT TRUE
);
```

**Admin Panel Display:**
- Read-only view
- Show tier distribution
- Highlight which students target which tier

---

#### 4.6 subject_exam_weights (Critical for Validation)
```sql
CREATE TABLE subject_exam_weights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id UUID REFERENCES subjects(id),
  exam_type_id INTEGER REFERENCES exam_types(id),
  question_count INT NOT NULL,
  
  -- Alternative subject logic
  is_alternative BOOLEAN DEFAULT FALSE,
  alternative_group VARCHAR(50),
  alternative_note TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Admin Panel Phase 1:** Read-only viewer  
**Admin Panel Phase 2:** Two-Person Rule editor

---

## 5. AUTHENTICATION & AUTHORIZATION

### RLS Policies (Admin Access)
```sql
-- Admins can see everything
CREATE POLICY "Admins view all dashboard_settings"
  ON dashboard_settings
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- Admins can modify feature flags
CREATE POLICY "Admins manage feature_flags"
  ON feature_flags
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- Audit log: Insert for admins, read-only for all
CREATE POLICY "Admins write audit_log"
  ON admin_audit_log
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

CREATE POLICY "Admins read audit_log"
  ON admin_audit_log
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );
```

---

### Admin Role Check (Backend)
```python
# backend/app/core/auth.py

async def get_current_admin(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Verify user is admin
    Raises 403 if not admin
    """
    user_id = current_user.get("id")
    
    # Check role in user_profiles
    supabase = get_supabase_admin()
    profile = supabase.table("user_profiles").select(
        "role"
    ).eq("id", user_id).single().execute()
    
    if not profile.data or profile.data.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    
    return current_user
```

---

### Frontend Admin Route Protection
```typescript
// frontend/middleware.ts

export async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;
  
  // Admin routes
  if (path.startsWith('/admin')) {
    const supabase = createServerClient(/* ... */);
    const { data: { session } } = await supabase.auth.getSession();
    
    if (!session) {
      return NextResponse.redirect(new URL('/login', req.url));
    }
    
    // Check admin role
    const { data: profile } = await supabase
      .from('user_profiles')
      .select('role')
      .eq('id', session.user.id)
      .single();
    
    if (profile?.role !== 'admin') {
      return NextResponse.redirect(new URL('/student/dashboard', req.url));
    }
  }
  
  return NextResponse.next();
}
```

---

## 6. FEATURE MODULES

### Module 1: Dashboard Control

**Purpose:** Manage dashboard card visibility

**UI Components:**
```
Admin Panel → Settings → Dashboard Management

┌─────────────────────────────────────────────────┐
│  📊 Dashboard Card Management                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  Projection Card                                │
│  [●] Show when no data   [Toggle: ON]          │
│                                                 │
│  University Goal Card                           │
│  [○] Hide when no goal   [Toggle: ON]          │
│                                                 │
│  Critical Alert                                 │
│  [●] Always show         [Toggle: ON]          │
│                                                 │
│  Trend Chart                                    │
│  [●] Show predictions    [Toggle: ON]          │
│                                                 │
│  [Save Changes]                                 │
└─────────────────────────────────────────────────┘
```

**Backend Endpoints:**
```python
# GET /admin/dashboard/settings
@router.get("/dashboard/settings")
async def get_dashboard_settings(
    current_admin: dict = Depends(get_current_admin)
):
    """Get current dashboard settings"""
    # Query dashboard_settings table
    pass

# PUT /admin/dashboard/settings
@router.put("/dashboard/settings")
async def update_dashboard_settings(
    settings: DashboardSettingsUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Update dashboard settings
    Creates audit log entry
    """
    # Update dashboard_settings
    # Log to admin_audit_log
    pass
```

**Frontend Integration:**
```typescript
// frontend/app/student/dashboard/page.tsx

const [settings, setSettings] = useState<DashboardSettings | null>(null);

useEffect(() => {
  const fetchSettings = async () => {
    const response = await api.get('/admin/dashboard/settings');
    setSettings(response.data);
  };
  fetchSettings();
}, []);

// Conditional rendering
{settings?.show_projection_card && <ProjectionCard />}
{(settings?.show_university_goal_card && 
  !(settings?.hide_goal_card_when_empty && !goalData)) && 
  <UniversityGoalCard />}
```

---

### Module 2: Kill Switch UI

**Purpose:** Control feature flags and emergency shutdown

**UI Components:**
```
Admin Panel → System → Feature Flags

┌─────────────────────────────────────────────────┐
│  🚨 Feature Flags & Kill Switch                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  🔴 MASTER KILL SWITCH          [OFF]          │
│  └─ Disables ALL non-critical features         │
│                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                 │
│  Motors (High Priority)                         │
│  ├─ BS-Model          [ON]  ⚠️ High           │
│  ├─ Priority Engine   [ON]  ⚠️ High           │
│  ├─ Difficulty        [ON]  ⚙️ Medium         │
│  └─ Time Analyzer     [ON]  ⚙️ Medium         │
│                                                 │
│  UI Features (Critical)                         │
│  ├─ Dashboard         [ON]  🔴 Critical       │
│  ├─ Progress Page     [ON]  🔴 Critical       │
│  └─ Test Entry        [ON]  🔴 Critical       │
│                                                 │
│  Analytics (Low Priority)                       │
│  ├─ Trend Chart       [ON]  ⚙️ Medium         │
│  └─ Predictions       [ON]  ⚪ Low            │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Backend Endpoints:**
```python
# GET /admin/feature-flags
@router.get("/feature-flags")
async def get_feature_flags(
    current_admin: dict = Depends(get_current_admin)
):
    """Get all feature flags with status"""
    pass

# PUT /admin/feature-flags/{flag_key}
@router.put("/feature-flags/{flag_key}")
async def toggle_feature_flag(
    flag_key: str,
    enabled: bool,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Toggle single feature flag
    Two-Person Rule for critical flags
    """
    pass

# POST /admin/kill-switch
@router.post("/kill-switch")
async def activate_master_kill_switch(
    reason: str,
    current_admin: dict = Depends(get_current_admin)
):
    """
    EMERGENCY: Disable all non-critical features
    Requires Two-Person Rule
    """
    pass
```

**Kill Switch Logic:**
```python
# backend/kill_switch/guard.py

def is_feature_enabled(flag_key: str) -> bool:
    """
    Check if feature is enabled
    Respects master kill switch
    """
    # Check master kill switch
    master = get_master_kill_switch_status()
    if master and flag_key not in CRITICAL_FEATURES:
        return False
    
    # Check individual flag
    flag = get_feature_flag(flag_key)
    return flag.is_enabled if flag else False

CRITICAL_FEATURES = [
    'ui_dashboard',
    'ui_test_entry',
    'ui_auth'
]
```

---

### Module 3: Exam Weight Viewer

**Purpose:** Validate exam weight integrity (read-only in Phase 1)

**UI Components:**
```
Admin Panel → Curriculum → Exam Weights

┌─────────────────────────────────────────────────┐
│  📚 Exam Weight Validation                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  Exam Type: TYT (Turkish University Entrance)   │
│  Total Questions: 120 (Official)                │
│                                                 │
│  Subject Breakdown:                             │
│  ├─ Matematik       40 questions                │
│  ├─ Fizik           7 questions                 │
│  ├─ Kimya           7 questions                 │
│  ├─ Biyoloji        6 questions                 │
│  ├─ Türkçe          40 questions                │
│  ├─ Tarih           5 questions                 │
│  ├─ Coğrafya        5 questions                 │
│  ├─ Felsefe         5 questions                 │
│  └─ [Seçmeli: Din KÜltürü/Ek Felsefe] 5 q     │
│                                                 │
│  ✅ Total Declared: 120 questions               │
│  ✅ Validation: PASSED                          │
│  ℹ️  Alternative subjects handled correctly    │
│                                                 │
│  [View AYT] [View Other Exams]                 │
└─────────────────────────────────────────────────┘
```

**Backend Endpoints:**
```python
# GET /admin/exam-weights/validate
@router.get("/exam-weights/validate")
async def validate_exam_weights(
    current_admin: dict = Depends(get_current_admin)
):
    """
    Run Analytics Integrity Triangle checks
    Returns validation status
    """
    pass

# GET /admin/exam-weights/{exam_type_id}
@router.get("/exam-weights/{exam_type_id}")
async def get_exam_weight_breakdown(
    exam_type_id: int,
    current_admin: dict = Depends(get_current_admin)
):
    """Get subject breakdown for exam type"""
    pass
```

---

### Module 4: Goal Management

**Purpose:** Assign university goals to students

**UI Components:**
```
Admin Panel → Students → Goal Management

┌─────────────────────────────────────────────────┐
│  🎯 Student Goal Management                     │
├─────────────────────────────────────────────────┤
│                                                 │
│  Search Student: [test2@test.com        ] 🔍   │
│                                                 │
│  Student: Demo Öğrenci (test2@test.com)        │
│  Current Goal: No goal assigned                 │
│                                                 │
│  ┌───────────────────────────────────────┐     │
│  │  Assign New Goal                      │     │
│  │                                       │     │
│  │  University Tier:                     │     │
│  │  [Dropdown: Tier 1-5            ▼]   │     │
│  │                                       │     │
│  │  Target Date:                         │     │
│  │  [2025-06-15                    📅]   │     │
│  │                                       │     │
│  │  [Assign Goal]                        │     │
│  └───────────────────────────────────────┘     │
│                                                 │
│  Recent Goals:                                  │
│  ├─ 2 students targeting Tier 1                │
│  ├─ 5 students targeting Tier 2                │
│  └─ 3 students targeting Tier 3                │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Backend Endpoints:**
```python
# POST /admin/goals/assign
@router.post("/goals/assign")
async def assign_student_goal(
    user_id: str,
    tier_id: str,
    target_date: date,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Assign university goal to student
    Creates entry in student_goals table
    """
    pass

# GET /admin/goals/{user_id}
@router.get("/goals/{user_id}")
async def get_student_goal(
    user_id: str,
    current_admin: dict = Depends(get_current_admin)
):
    """Get student's current goal"""
    pass

# DELETE /admin/goals/{goal_id}
@router.delete("/goals/{goal_id}")
async def delete_student_goal(
    goal_id: str,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Delete student goal
    Requires confirmation
    """
    pass

# GET /admin/goals/statistics
@router.get("/goals/statistics")
async def get_goal_statistics(
    current_admin: dict = Depends(get_current_admin)
):
    """Get goal distribution by tier"""
    pass
```

---

## 7. UI/UX PATTERNS

### Color Scheme (Admin Panel)
```css
/* Admin Theme (Professional) */
:root {
  --admin-primary: #6366f1;      /* Indigo */
  --admin-secondary: #8b5cf6;    /* Purple */
  --admin-success: #10b981;      /* Green */
  --admin-warning: #f59e0b;      /* Amber */
  --admin-danger: #ef4444;       /* Red */
  --admin-bg: #f9fafb;           /* Gray 50 */
  --admin-card: #ffffff;         /* White */
  --admin-border: #e5e7eb;       /* Gray 200 */
  --admin-text: #111827;         /* Gray 900 */
  --admin-text-muted: #6b7280;   /* Gray 500 */
}
```

### Layout Structure
```
┌────────────────────────────────────────────────────────────┐
│  [Logo] End.STP Admin       [Notifications] [Profile ▼]   │
├────────────┬───────────────────────────────────────────────┤
│            │                                               │
│  📊 Home   │                                               │
│            │                                               │
│  ⚙️ System  │           MAIN CONTENT AREA                  │
│  └─ Feature│                                               │
│     Flags  │                                               │
│            │                                               │
│  🎨 UI      │                                               │
│  └─ Dashboard                                              │
│     Settings│                                              │
│            │                                               │
│  🎯 Students│                                              │
│  └─ Goals  │                                               │
│            │                                               │
│  📚 Curriculum                                             │
│  └─ Exam   │                                               │
│     Weights│                                               │
│            │                                               │
│  📊 Analytics                                              │
│  📝 Audit  │                                               │
│     Log    │                                               │
│            │                                               │
└────────────┴───────────────────────────────────────────────┘
```

### Component Standards

**Toggle Switch:**
```tsx
// Standard toggle component
<Toggle
  enabled={value}
  onChange={handleChange}
  label="Feature Name"
  description="What this does"
  criticality="high"  // low | medium | high | critical
/>
```

**Confirmation Modal:**
```tsx
// For destructive actions
<ConfirmModal
  title="Delete Student Goal?"
  message="This action cannot be undone."
  confirmText="Delete"
  cancelText="Cancel"
  danger={true}
  onConfirm={handleDelete}
  onCancel={handleCancel}
/>
```

**Audit Trail Display:**
```tsx
// Show who changed what
<AuditEntry
  admin="admin@end-stp.com"
  action="Updated dashboard settings"
  timestamp="2026-02-09T10:30:00Z"
  changes={{
    before: { show_goal_card: true },
    after: { show_goal_card: false }
  }}
/>
```

---

## 8. SECURITY & COMPLIANCE

### Audit Logging (Mandatory)

**Every admin action MUST be logged:**
```python
async def log_admin_action(
    admin_id: str,
    action_type: str,
    action_category: str,
    before_state: dict = None,
    after_state: dict = None
):
    """
    Log admin action to audit trail
    """
    supabase = get_supabase_admin()
    
    supabase.table("admin_audit_log").insert({
        "admin_id": admin_id,
        "action_type": action_type,
        "action_category": action_category,
        "before_state": before_state,
        "after_state": after_state,
        "created_at": datetime.now(timezone.utc).isoformat()
    }).execute()
```

**Usage:**
```python
@router.put("/dashboard/settings")
async def update_dashboard_settings(
    settings: DashboardSettingsUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    # Get current state
    before = get_current_settings()
    
    # Update
    after = update_settings(settings)
    
    # Log
    await log_admin_action(
        admin_id=current_admin["id"],
        action_type="update_dashboard_settings",
        action_category="dashboard_settings",
        before_state=before,
        after_state=after
    )
    
    return after
```

---

### RBAC (Role-Based Access Control)

**Roles:**
```
admin       → Full access
coach       → Students assigned to them
student     → Own data only
institution → Aggregate data only
```

**Permission Matrix:**

| Action | Admin | Coach | Student | Institution |
|--------|-------|-------|---------|-------------|
| View own dashboard | ✅ | ✅ | ✅ | ✅ |
| View other dashboards | ✅ | ✅* | ❌ | ✅** |
| Modify dashboard settings | ✅ | ❌ | ❌ | ❌ |
| Toggle feature flags | ✅ | ❌ | ❌ | ❌ |
| Assign goals | ✅ | ✅* | ❌ | ❌ |
| View exam weights | ✅ | ✅ | ❌ | ✅ |
| Edit exam weights | ✅*** | ❌ | ❌ | ❌ |
| View audit log | ✅ | ❌ | ❌ | ❌ |

\* Only assigned students  
\** Aggregate only, no PII  
\*** Two-Person Rule

---

### Rate Limiting (Admin Actions)
```python
# backend/app/core/rate_limit.py

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.put("/dashboard/settings")
@limiter.limit("10/minute")  # Max 10 changes per minute
async def update_dashboard_settings(
    request: Request,
    settings: DashboardSettingsUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    pass

@router.post("/kill-switch")
@limiter.limit("1/hour")  # Max 1 kill switch per hour
async def activate_master_kill_switch(
    request: Request,
    reason: str,
    current_admin: dict = Depends(get_current_admin)
):
    pass
```

---

### CSRF Protection
```typescript
// frontend/lib/api/client.ts

// All admin POST/PUT/DELETE requests include CSRF token
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  ?.getAttribute('content');

api.defaults.headers.common['X-CSRF-Token'] = csrfToken;
```

---

## 9. IMPLEMENTATION ROADMAP

### Week 1: Foundation (3-4 days)

**Backend:**
- [ ] Database migrations (3 new tables)
- [ ] Admin auth middleware
- [ ] Audit logging system
- [ ] Base admin router setup

**Frontend:**
- [ ] Admin layout component
- [ ] Sidebar navigation
- [ ] Auth guard for /admin routes
- [ ] Basic dashboard (placeholder)

**Testing:**
- [ ] Admin auth flow
- [ ] RLS policies verification
- [ ] Route protection

**Deliverables:**
- Admin panel accessible at `/admin`
- Audit log capturing actions
- Only admins can access

---

### Week 2: Module 1 & 2 (4-5 days)

**Module 1: Dashboard Control**
- [ ] Dashboard settings table UI
- [ ] Toggle switches for cards
- [ ] Backend endpoint integration
- [ ] Frontend conditional rendering
- [ ] Audit logging

**Module 2: Kill Switch UI**
- [ ] Feature flags table seeding
- [ ] Kill switch dashboard UI
- [ ] Master kill switch logic
- [ ] Individual flag toggles
- [ ] Two-Person Rule setup (basic)

**Testing:**
- [ ] Toggle cards on/off
- [ ] Master kill switch disables non-critical
- [ ] Audit log complete

**Deliverables:**
- Dashboard cards controllable
- Kill switch functional
- Changes logged

---

### Week 3: Module 3 & 4 (4-5 days)

**Module 3: Exam Weight Viewer**
- [ ] Validation dashboard UI
- [ ] Analytics Integrity Triangle checks
- [ ] Subject breakdown view
- [ ] Alternative subjects display
- [ ] Anomaly detection alerts

**Module 4: Goal Management**
- [ ] Student search UI
- [ ] Goal assignment form
- [ ] Goal listing & deletion
- [ ] Statistics dashboard
- [ ] Integration with UniversityGoalCard

**Testing:**
- [ ] Exam weight validation correct
- [ ] Goals assigned successfully
- [ ] UniversityGoalCard shows real data

**Deliverables:**
- Exam weights viewable & validated
- Goals manageable via UI
- Phase 2 (TYT/AYT) ready

---

### Week 4: Polish & Testing (2-3 days)

**Polish:**
- [ ] UI/UX refinements
- [ ] Error handling improvements
- [ ] Loading states
- [ ] Empty states
- [ ] Help tooltips

**Testing:**
- [ ] E2E admin workflows
- [ ] Security testing (penetration)
- [ ] Performance testing
- [ ] Cross-browser testing

**Documentation:**
- [ ] Admin user guide
- [ ] API documentation update
- [ ] Video tutorial (optional)

**Deliverables:**
- Production-ready admin panel
- Complete documentation
- Security audit passed

---

## 10. SUCCESS CRITERIA

### Functional Requirements

✅ **Dashboard Control:**
- [ ] Cards can be toggled on/off
- [ ] Changes reflect immediately on student dashboard
- [ ] Settings persist across sessions

✅ **Kill Switch:**
- [ ] Master kill switch disables non-critical features
- [ ] Individual flags can be toggled
- [ ] Critical features remain active during kill switch

✅ **Exam Weights:**
- [ ] Analytics Integrity Triangle validates correctly
- [ ] Anomalies detected and displayed
- [ ] Read-only view complete

✅ **Goal Management:**
- [ ] Goals can be assigned to students
- [ ] Goals can be deleted
- [ ] UniversityGoalCard reflects real data
- [ ] Statistics dashboard accurate

---

### Non-Functional Requirements

✅ **Security:**
- [ ] Only admins can access /admin
- [ ] All actions logged to audit trail
- [ ] CSRF protection enabled
- [ ] Rate limiting enforced

✅ **Performance:**
- [ ] Admin panel loads < 2 seconds
- [ ] Toggle actions respond < 500ms
- [ ] Audit log queries optimized (indexed)

✅ **Compliance:**
- [ ] GLOBAL-FIRST: All text _tr/_en
- [ ] UTC timestamps throughout
- [ ] L5 non-invasive: No code deletion

✅ **Usability:**
- [ ] Intuitive navigation
- [ ] Clear confirmation dialogs
- [ ] Help tooltips where needed
- [ ] Mobile-friendly (basic)

---

## 11. PHASE 2 PREPARATION

### What Admin Panel Enables

**After Admin Panel MVP:**
```
✅ READY FOR:
├─ TYT/AYT Net Tracking
│  └─ Goals manageable → Real data flow
│
├─ Action Hint Layer
│  └─ Kill switch → Gradual rollout
│
├─ Advanced Analytics
│  └─ Feature flags → A/B testing
│
└─ Multi-tenant (Future)
   └─ Dashboard settings → Per-institution config
```

**Not Ready Without Admin Panel:**
```
❌ BLOCKED:
├─ TYT/AYT tracking → No goal management
├─ Action hints → No control mechanism
├─ Advanced features → No kill switch
└─ Scale → Manual database edits
```

---

## 12. APPENDIX

### A. Database ERD (Admin Tables)
```
dashboard_settings (1)
├─ id
├─ show_projection_card
├─ show_university_goal_card
├─ hide_goal_card_when_empty
└─ updated_by → user_profiles(id)

feature_flags (*)
├─ flag_key (UNIQUE)
├─ is_enabled
├─ category
└─ updated_by → user_profiles(id)

admin_audit_log (*)
├─ admin_id → user_profiles(id)
├─ action_type
├─ before_state (JSONB)
├─ after_state (JSONB)
└─ created_at

admin_approvals (*) [Two-Person Rule]
├─ action_type
├─ requested_by → user_profiles(id)
├─ approved_by → user_profiles(id)
├─ status
└─ request_data (JSONB)
```

---

### B. API Endpoint Summary

**Dashboard Control:**
```
GET    /admin/dashboard/settings
PUT    /admin/dashboard/settings
```

**Feature Flags:**
```
GET    /admin/feature-flags
PUT    /admin/feature-flags/{flag_key}
POST   /admin/kill-switch
GET    /admin/kill-switch/status
```

**Exam Weights:**
```
GET    /admin/exam-weights/validate
GET    /admin/exam-weights/{exam_type_id}
GET    /admin/exam-weights/anomalies
```

**Goal Management:**
```
GET    /admin/goals/statistics
GET    /admin/goals/{user_id}
POST   /admin/goals/assign
DELETE /admin/goals/{goal_id}
```

**Audit Log:**
```
GET    /admin/audit-log
GET    /admin/audit-log/{admin_id}
GET    /admin/audit-log/category/{category}
```

---

### C. Environment Variables
```bash
# .env (Backend)

# Admin Panel
ADMIN_PANEL_ENABLED=true
ADMIN_TWO_PERSON_RULE_ENABLED=true
ADMIN_RATE_LIMIT_PER_MINUTE=10

# Kill Switch
MASTER_KILL_SWITCH_ENABLED=false
KILL_SWITCH_CRITICAL_FEATURES=ui_dashboard,ui_test_entry,ui_auth

# Audit
AUDIT_LOG_RETENTION_DAYS=365
AUDIT_LOG_COMPRESSION_ENABLED=true
```

---

### D. Testing Credentials
```bash
# Admin User (Test)
Email: admin@end-stp.com
Password: Admin123!Test
Role: admin

# Regular User (Test)
Email: test2@test.com
Password: test123test
Role: student

# Coach User (Test)
Email: coach@end-stp.com
Password: Coach123!Test
Role: coach
```

---

## 13. GLOSSARY

| Term | Definition |
|------|------------|
| **Analytics Integrity Triangle** | Three-way validation: exam_types ↔ subject_exam_weights ↔ test_records |
| **Kill Switch** | Emergency mechanism to disable non-critical features |
| **Two-Person Rule** | Critical changes require approval from second admin |
| **L5 Non-Invasive** | Never delete code, only add/extend |
| **GLOBAL-FIRST** | All features must be internationally ready from day one |
| **RLS** | Row Level Security (Supabase database security) |
| **Audit Trail** | Complete log of all admin actions |
| **Feature Flag** | Toggle to enable/disable features without deployment |

---

**END OF SPECIFICATION**

**Next Steps:**
1. Review this document with team
2. Create GitHub issues for each module
3. Set up project board (Kanban)
4. Begin Week 1 implementation

**Questions?** See: `docs/SESSION_SUMMARY_2026_02_08_09.md`

