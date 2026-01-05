# 📋 PHASE 2: SCHEMA ENHANCEMENTS (Post-MVP)

> **Status**: Planned  
> **Priority**: High (Enterprise Polish)  
> **Timeline**: After Chemistry + Biology completion  
> **Impact**: GLOBAL-FIRST alignment

---

## 🎯 OVERVIEW

These enhancements improve our schema for international scalability, affiliate partnerships, and tier-based features. They are NOT bugs - they are enterprise-level polish identified during Physics deployment.

**Credit:** Identified during Physics Context Layer deployment (Dec 31, 2024)

---

## 1️⃣ GRADE_LEVEL → Structured Format

### **Current State:**
```sql
CREATE TABLE topics (
  ...
  grade_level TEXT,  -- e.g. '10,tyt,ayt'
  ...
);
```

**Problem:**
- Mixed concepts (grade vs exam system)
- Requires string parsing
- Not globally scalable (TYT/AYT is Turkey-only)

### **Enhanced Schema:**
```sql
CREATE TABLE topics (
  ...
  grade_level TEXT,  -- DEPRECATED (keep for backward compat)
  grade_metadata JSONB,  -- NEW!
  ...
);
```

**grade_metadata Structure:**
```json
{
  "grade_levels": ["10", "11"],        // Universal (9-12, K-12, etc.)
  "exam_systems": ["tyt", "ayt"],      // Country-specific
  "curriculum_year": 2024,             // When applicable
  "semester": null                     // When applicable
}
```

**Global Examples:**
```json
// Turkey (OSYM)
{
  "grade_levels": ["10"],
  "exam_systems": ["tyt", "ayt"]
}

// USA (SAT)
{
  "grade_levels": ["11", "12"],
  "exam_systems": ["sat"]
}

// UK (A-Level)
{
  "grade_levels": ["12", "13"],  // Year 12-13
  "exam_systems": ["a-level"]
}

// International Baccalaureate
{
  "grade_levels": ["11", "12"],
  "exam_systems": ["ib-dp"],  // IB Diploma Programme
  "curriculum_year": 2024
}
```

**Migration SQL:**
```sql
-- Step 1: Add new column
ALTER TABLE topics ADD COLUMN grade_metadata JSONB;

-- Step 2: Migrate existing data
UPDATE topics 
SET grade_metadata = jsonb_build_object(
  'grade_levels', ARRAY[
    unnest(string_to_array(
      regexp_replace(grade_level, ',(tyt|ayt|sat)', '', 'g'),
      ','
    ))
  ],
  'exam_systems', ARRAY[
    unnest(regexp_matches(grade_level, '(tyt|ayt|sat)', 'g'))
  ]
)
WHERE grade_level IS NOT NULL;

-- Step 3: Create index
CREATE INDEX idx_topics_grade_metadata ON topics USING GIN (grade_metadata);

-- Step 4: Update API responses to use grade_metadata
-- Step 5: Deprecate grade_level (keep for 6 months backward compat)
```

**Benefits:**
- ✅ Universal grade levels (work in any country)
- ✅ Exam systems as separate concept
- ✅ Affiliates map exam_systems to their own
- ✅ No parsing needed (native JSONB)
- ✅ Queryable: `WHERE grade_metadata->'exam_systems' ? 'tyt'`

---

## 2️⃣ PREREQUISITE_STRATEGY

### **Current State:**
```json
// In topic_contexts.metadata
{
  "prerequisite_topics": ["FIZ-BASINC-01"]
  // Implicit: always "soft" (guidance, not blocker)
}
```

**Problem:**
- No way to enforce strict prerequisites
- Institutions want pedagogical control
- Can't A/B test strict vs soft

### **Enhanced Schema:**
```json
// In topic_contexts.metadata
{
  "prerequisite_topics": ["FIZ-BASINC-01"],
  "prerequisite_strategy": "soft",  // NEW!
  "prerequisite_config": {          // NEW! (optional)
    "blocking_message_tr": "Bu konuyu çalışmadan önce Basınç konusunu tamamlamanız önerilir.",
    "blocking_message_en": "It is recommended to complete Pressure before this topic.",
    "completion_threshold": 70  // % score needed to "complete" prerequisite
  }
}
```

**Strategy Types:**
```
"soft"      → Warning shown, can proceed
"strict"    → Cannot proceed without completion
"recommended" → Just FYI, no warning
"adaptive"  → Based on user tier/performance
```

**Tier-Based Rules:**
```json
// Free Tier: Always soft (no blocking)
{
  "prerequisite_strategy": "soft"
}

// Premium Tier: Institution can choose
{
  "prerequisite_strategy": "strict",  // Enforced!
  "prerequisite_config": {
    "completion_threshold": 80  // Must score 80%+
  }
}
```

**Migration SQL:**
```sql
-- Add prerequisite_strategy to all existing topics
UPDATE topics t
SET metadata = jsonb_set(
  metadata,
  '{prerequisite_strategy}',
  '"soft"'::jsonb
)
WHERE metadata->'prerequisite_topics' IS NOT NULL;
```

**Benefits:**
- ✅ Tier-based features (Free vs Premium)
- ✅ Institution customization
- ✅ A/B testing learning outcomes
- ✅ Adaptive learning paths
- ✅ Clear user messaging

---

## 3️⃣ TIME_UNIT Clarity

### **Current State:**
```json
// In topic_contexts.metadata
{
  "time_estimate": {
    "foundation": 240  // Implicit: minutes
  }
}
```

**Problem:**
- Unit not explicit (assumes minutes)
- International API consumers may assume hours
- Some curricula use "sessions" (45-min blocks)

### **Enhanced Schema:**
```json
{
  "time_estimate": {
    "foundation": 240,
    "practice": 300,
    "mastery": 210,
    "time_unit": "minutes"  // NEW! Explicit unit
  }
}
```

**Supported Units:**
```
"minutes"   → Standard (international)
"hours"     → When > 120 minutes
"sessions"  → Curriculum-based (e.g. 45-min blocks)
```

**Conversion Helper (API):**
```json
// API can return multiple units
{
  "time_estimate": {
    "minutes": 240,
    "hours": 4.0,
    "sessions": 5.33  // If 45-min sessions
  }
}
```

**Migration SQL:**
```sql
-- Add time_unit to all existing topics
UPDATE topics t
SET metadata = jsonb_set(
  metadata,
  '{time_estimate,time_unit}',
  '"minutes"'::jsonb
)
WHERE metadata->'time_estimate' IS NOT NULL;
```

**Benefits:**
- ✅ International clarity
- ✅ No assumptions
- ✅ API can convert units automatically
- ✅ Curriculum flexibility

---

## 📊 MIGRATION CHECKLIST

### **Phase 2.1: Schema Updates**
```
☐ Add grade_metadata column to topics
☐ Migrate existing grade_level data
☐ Add prerequisite_strategy to topic_contexts
☐ Add time_unit to time_estimate
☐ Create GIN indexes for JSONB queries
☐ Update validation rules
```

### **Phase 2.2: API Updates**
```
☐ Update topic serializers (include new fields)
☐ Add backward compatibility (keep old fields)
☐ Update Swagger/OpenAPI docs
☐ Add conversion helpers (time units)
☐ Add tier-based prerequisite logic
```

### **Phase 2.3: Frontend Updates**
```
☐ Update TypeScript interfaces
☐ Handle grade_metadata in UI
☐ Show prerequisite warnings/blocks
☐ Display time estimates with units
☐ Test tier-based features
```

### **Phase 2.4: Testing**
```
☐ Unit tests (schema migrations)
☐ Integration tests (API)
☐ E2E tests (Frontend)
☐ Performance tests (JSONB queries)
☐ Backward compatibility tests
```

---

## 🌍 GLOBAL-FIRST EXAMPLES

### **Turkey (OSYM - Current)**
```json
{
  "grade_metadata": {
    "grade_levels": ["10"],
    "exam_systems": ["tyt", "ayt"]
  },
  "prerequisite_strategy": "soft",
  "time_estimate": {
    "foundation": 240,
    "time_unit": "minutes"
  }
}
```

### **USA (SAT)**
```json
{
  "grade_metadata": {
    "grade_levels": ["11", "12"],
    "exam_systems": ["sat"]
  },
  "prerequisite_strategy": "recommended",
  "time_estimate": {
    "foundation": 4,
    "time_unit": "hours"
  }
}
```

### **UK (A-Level)**
```json
{
  "grade_metadata": {
    "grade_levels": ["12", "13"],
    "exam_systems": ["a-level"],
    "curriculum_year": 2024
  },
  "prerequisite_strategy": "strict",
  "prerequisite_config": {
    "completion_threshold": 75
  },
  "time_estimate": {
    "foundation": 6,
    "time_unit": "sessions"
  }
}
```

### **International Baccalaureate**
```json
{
  "grade_metadata": {
    "grade_levels": ["11", "12"],
    "exam_systems": ["ib-dp"],
    "curriculum_year": 2024
  },
  "prerequisite_strategy": "adaptive",
  "time_estimate": {
    "foundation": 240,
    "practice": 360,
    "time_unit": "minutes"
  }
}
```

---

## 💰 ROI ANALYSIS

### **Business Value:**
```
Tier-Based Features:
- Free: Soft prerequisites → Good UX
- Premium: Strict prerequisites → Better learning outcomes (+15% retention)
- Institution: Custom thresholds → Pedagogical control

Affiliate Partnerships:
- grade_metadata → Easy mapping to local systems
- time_unit → International clarity
- prerequisite_strategy → Institutional flexibility

A/B Testing:
- Test strict vs soft prerequisites
- Measure completion rates
- Optimize learning paths
```

### **Development Cost:**
```
Estimated Time: 1-2 weeks
- Schema migration: 2 days
- API updates: 3 days
- Frontend: 3 days
- Testing: 2-3 days
```

### **Expected Impact:**
```
✅ Premium conversion: +10% (strict prerequisites appeal)
✅ Affiliate signup: +25% (easy integration)
✅ International expansion: +50% (localization ready)
✅ Student retention: +15% (better guidance)
```

---

## 📅 TIMELINE

**After MVP:**
- Week 1-2: Complete Chemistry + Biology
- Week 3: Phase 2 Schema Planning
- Week 4-5: Implementation
- Week 6: Testing + Deployment

**ETA:** January 2025 (post-MVP)

---

## 🎯 SUCCESS METRICS

```
✅ All topics have grade_metadata
✅ Zero API errors (backward compat)
✅ Tier-based features working
✅ International affiliates can integrate
✅ Time estimates have explicit units
✅ A/B tests running (strict vs soft)
```

---

## 📝 NOTES

- **Priority:** High (but not blocking MVP)
- **Type:** Enhancement (not bug fix)
- **Impact:** GLOBAL-FIRST alignment
- **Complexity:** Medium (JSONB migrations)
- **Risk:** Low (backward compatible)

**Credit:** Enterprise-level thinking during Physics deployment! 🎯

---

**END OF PHASE 2 ENHANCEMENT PLAN**
