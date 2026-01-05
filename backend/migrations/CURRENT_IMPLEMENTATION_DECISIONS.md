# 📋 CURRENT IMPLEMENTATION DECISIONS (MVP Phase)

> **Date**: December 31, 2024  
> **Context**: Physics Context Layer Deployment  
> **Status**: Active decisions for MVP

---

## 🎯 WHY WE'RE NOT CHANGING NOW

### **Principle: "Don't Break Working System"**

We have **35 Physics topics** successfully deployed with:
- ✅ Topics inserted correctly
- ✅ OSYM coverage working
- ✅ Prerequisites linked
- ✅ Format v1.0 proven stable

**Changing schema now would:**
- ❌ Require re-migration of 40 Math + 35 Physics = 75 topics
- ❌ Risk breaking working validation
- ❌ Delay Chemistry + Biology
- ❌ Create technical debt during MVP

**Better approach:**
- ✅ Complete MVP (all subjects)
- ✅ Plan comprehensive Schema v2.0
- ✅ Migrate everything at once (clean, tested)
- ✅ No rush, no mistakes

---

## 📊 CURRENT CONVENTIONS (MVP)

### **1️⃣ grade_level Format**

**Current:**
```sql
grade_level = '10,tyt,ayt'
```

**Interpretation:**
```
- "10" = Grade 10
- "tyt" = TYT exam coverage
- "ayt" = AYT exam coverage
```

**How Affiliates Should Parse:**
```javascript
// Simple parsing for MVP
const [grades, ...exams] = gradeLevel.split(',');
const gradeNumbers = grades.split(',').filter(g => /^\d+$/.test(g));
const examSystems = exams.filter(e => /^[a-z]+$/.test(e));

// Example:
// '10,11,tyt,ayt' → grades: ['10','11'], exams: ['tyt','ayt']
```

**Future:** Will be `grade_metadata` JSONB (Phase 2)

---

### **2️⃣ prerequisite_topics Strategy**

**Current:**
```json
{
  "prerequisite_topics": ["FIZ-BASINC-01"]
}
```

**Implicit Strategy:**
- All prerequisites are "soft" (guidance, not blocker)
- Frontend shows warning: "Recommended: Complete [topic] first"
- Student can proceed anyway

**Rationale:**
- MVP focuses on recommendation, not enforcement
- Free tier = no blocking (good UX)
- Premium tier features come in Phase 2

**Future:** Will have explicit `prerequisite_strategy` field (Phase 2)

---

### **3️⃣ time_estimate Unit**

**Current:**
```json
{
  "time_estimate": {
    "foundation": 240,
    "practice": 300,
    "mastery": 210
  }
}
```

**Implicit Unit:**
- All values in **minutes**
- No explicit unit field

**How Affiliates Should Interpret:**
```javascript
// All values are minutes
const foundationMinutes = timeEstimate.foundation;  // 240
const foundationHours = foundationMinutes / 60;     // 4.0

// Display to users
console.log(`${foundationHours} hours`);  // "4 hours"
```

**Future:** Will have explicit `time_unit: "minutes"` field (Phase 2)

---

## 🔄 BACKWARD COMPATIBILITY PROMISE

When we implement Phase 2 enhancements:

### **grade_level → grade_metadata**
```sql
-- Old field will remain (deprecated)
grade_level TEXT,

-- New field will be added
grade_metadata JSONB
```

**API Response (Phase 2):**
```json
{
  "grade_level": "10,tyt,ayt",  // DEPRECATED (6 months)
  "grade_metadata": {            // NEW
    "grade_levels": ["10"],
    "exam_systems": ["tyt", "ayt"]
  }
}
```

### **prerequisite_topics → prerequisite_strategy**
```json
{
  "prerequisite_topics": ["FIZ-BASINC-01"],  // Existing
  "prerequisite_strategy": "soft"             // NEW (default)
}
```

### **time_estimate → time_unit**
```json
{
  "time_estimate": {
    "foundation": 240,
    "practice": 300,
    "mastery": 210,
    "time_unit": "minutes"  // NEW (explicit)
  }
}
```

**Guarantee:** 6-month deprecation period for old fields

---

## 📝 AFFILIATE INTEGRATION GUIDE (Current MVP)

### **Example: Parsing Topic Data**

```javascript
// Topic from API (current format)
const topic = {
  code: "FIZ-HAREKET-01",
  name_tr: "Düz Çizgisel Hareket",
  grade_level: "9,10,tyt",
  difficulty_level: 5,
  metadata: {
    prerequisite_topics: ["FIZ-BUYUK-01"],
    time_estimate: {
      foundation: 180,
      practice: 240,
      mastery: 150
    }
  }
};

// Parse grade_level
function parseGradeLevel(gradeLevel) {
  const parts = gradeLevel.split(',');
  return {
    grades: parts.filter(p => /^\d+$/.test(p)),      // ["9", "10"]
    exams: parts.filter(p => /^[a-z]+$/.test(p))     // ["tyt"]
  };
}

// Get time in hours
function getTimeInHours(timeEstimate) {
  return {
    foundation: timeEstimate.foundation / 60,  // 3.0 hours
    practice: timeEstimate.practice / 60,      // 4.0 hours
    mastery: timeEstimate.mastery / 60         // 2.5 hours
  };
}

// Check prerequisites
function hasPrerequisites(topic) {
  return topic.metadata?.prerequisite_topics?.length > 0;
}

// Usage
const parsed = parseGradeLevel(topic.grade_level);
console.log(parsed);
// { grades: ["9", "10"], exams: ["tyt"] }

const hours = getTimeInHours(topic.metadata.time_estimate);
console.log(hours);
// { foundation: 3.0, practice: 4.0, mastery: 2.5 }

const needsPrereq = hasPrerequisites(topic);
console.log(needsPrereq);
// true (has FIZ-BUYUK-01 as prerequisite)
```

---

## 🚨 IMPORTANT NOTES FOR AFFILIATES

### **1. grade_level Parsing**
```
⚠️ Current format: "10,tyt,ayt" (comma-separated string)
✅ Split by comma
✅ Numbers = grades, letters = exam systems
⚠️ This will change to JSONB in Phase 2 (Q1 2025)
```

### **2. prerequisite_topics**
```
⚠️ Current: No blocking (soft recommendations only)
✅ Show warning to students
✅ Allow them to proceed
⚠️ Phase 2 will add "strict" mode option
```

### **3. time_estimate**
```
⚠️ Current: Implicit "minutes" unit
✅ All values are in minutes
✅ Divide by 60 for hours
⚠️ Phase 2 will add explicit time_unit field
```

### **4. Migration Timeline**
```
✅ MVP: Current format (stable, working)
⏳ Phase 2: Enhanced schema (Q1 2025)
⏳ Deprecation: Old fields deprecated 6 months after Phase 2
⏳ Removal: Old fields removed 12 months after Phase 2
```

---

## 💬 COMMUNICATION PLAN

### **To Affiliates (When Phase 2 Launches):**

**Email Template:**
```
Subject: Schema Enhancement - Action Required by [6 months from launch]

Dear Partner,

We're enhancing our API schema for better international support!

WHAT'S CHANGING:
✅ grade_level → grade_metadata (structured JSONB)
✅ prerequisite_strategy added (soft/strict options)
✅ time_unit added (explicit "minutes")

TIMELINE:
- Phase 2 Launch: Q1 2025
- Backward Compatibility: 6 months
- Old Fields Deprecated: Q3 2025
- Old Fields Removed: Q1 2026

ACTION REQUIRED:
☐ Update your integration to use new fields
☐ Test with both old and new formats
☐ Deploy before Q3 2025

DOCUMENTATION:
https://docs.end-stp.com/schema-v2

Questions? partnerships@end-stp.com
```

---

## 🎯 KEY TAKEAWAYS

```
1. CURRENT MVP:
   - Simple string formats
   - Implicit conventions
   - Works perfectly for Turkey (OSYM)
   - Easy to parse

2. PHASE 2 (Q1 2025):
   - Structured JSONB
   - Explicit fields
   - International-ready
   - Tier-based features

3. MIGRATION:
   - Backward compatible (6 months)
   - No breaking changes
   - Smooth transition

4. AFFILIATE PROMISE:
   - 6-month warning before changes
   - Clear documentation
   - Support during migration
```

---

**BOTTOM LINE:**
- Current format is INTENTIONAL (MVP simplicity)
- Future enhancements are PLANNED (not oversight)
- Migration will be SMOOTH (backward compatible)
- Affiliates will be SUPPORTED (6-month transition)

---

**END OF CURRENT IMPLEMENTATION DECISIONS**
