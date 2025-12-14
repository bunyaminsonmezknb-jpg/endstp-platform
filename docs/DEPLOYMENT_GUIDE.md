# 🚀 DEPLOYMENT GUIDE - Migrations 006 & 007

## 📋 PREREQUISITES

### **Environment:**
- Supabase PostgreSQL database
- Database access (admin privileges)
- SQL Editor or psql client

### **Pre-Deployment Checklist:**
```
✅ Backup database
✅ Test environment ready (staging)
✅ Rollback plan prepared
✅ Supabase SQL Editor access
✅ Database schema documented
```

---

## 📦 MIGRATION 006 v3.4.1 - SMART MISTAKE ANALYZER

### **File:**
```
/mnt/user-data/outputs/006_smart_mistake_analyzer_v3.4.1_FINAL_POLISH.sql
```

### **Deployment Steps:**

**1. Pre-Deployment Check:**
```sql
-- Check if tables already exist
SELECT table_name FROM information_schema.tables
WHERE table_name IN (
    'system_settings',
    'analysis_presets',
    'student_analysis_settings',
    'student_baseline_performance',
    'student_mistake_patterns'
);
-- If any exist, review before proceeding
```

**2. Deploy Migration:**
```sql
-- Copy entire 006_smart_mistake_analyzer_v3.4.1_FINAL_POLISH.sql
-- Paste into Supabase SQL Editor
-- Click "Run"
-- Wait for completion (~10-15 seconds)
```

**3. Verify Deployment:**
```sql
-- Check tables created
SELECT table_name FROM information_schema.tables
WHERE table_name IN (
    'system_settings',
    'analysis_presets',
    'student_analysis_settings',
    'student_baseline_performance',
    'student_mistake_patterns'
);
-- Expected: 5 rows

-- Check triggers attached
SELECT tgname FROM pg_trigger
WHERE tgname IN (
    'trg_update_student_baseline',
    'trg_update_mistake_patterns'
);
-- Expected: 2 rows

-- Check functions exist
SELECT proname FROM pg_proc
WHERE proname IN (
    'update_student_baseline',
    'update_mistake_patterns'
);
-- Expected: 2 rows

-- Check presets seeded
SELECT COUNT(*) FROM analysis_presets;
-- Expected: 3 rows (aggressive, normal, soft)

-- Check default settings
SELECT COUNT(*) FROM system_settings WHERE is_default = true;
-- Expected: 1 row
```

**4. Success Indicators:**
```
✅ All 5 tables created
✅ All 2 triggers attached
✅ All 2 functions created
✅ 3 presets seeded
✅ 1 default setting
✅ No errors in output
```

---

## 🗣️ MIGRATION 007 v1 - UI REFLEX BRIDGE

### **File:**
```
/mnt/user-data/outputs/007_ui_reflex_bridge_v1_SAFE.sql
```

### **Prerequisites:**
```
⚠️ Migration 006 must be deployed first!
⚠️ student_mistakes table must exist
⚠️ student_mistake_patterns table must exist
```

### **Deployment Steps:**

**1. Pre-Deployment Check:**
```sql
-- Verify Migration 006 deployed
SELECT COUNT(*) FROM pg_trigger
WHERE tgname IN (
    'trg_update_student_baseline',
    'trg_update_mistake_patterns'
);
-- Expected: 2 rows

-- Check if Migration 007 tables exist
SELECT table_name FROM information_schema.tables
WHERE table_name IN (
    'student_recommendations',
    'ui_reflex_events'
);
-- If any exist, review before proceeding
```

**2. Deploy Migration:**
```sql
-- Copy entire 007_ui_reflex_bridge_v1_SAFE.sql
-- Paste into Supabase SQL Editor
-- Click "Run"
-- Wait for completion (~5-10 seconds)
```

**3. Verify Deployment:**
```sql
-- Check tables created
SELECT table_name FROM information_schema.tables
WHERE table_name IN (
    'student_recommendations',
    'ui_reflex_events'
);
-- Expected: 2 rows

-- Check trigger attached
SELECT tgname FROM pg_trigger
WHERE tgname = 'trg_generate_recommendations';
-- Expected: 1 row

-- Check functions exist
SELECT proname FROM pg_proc
WHERE proname IN (
    'build_reflex_recommendation_payload',
    'upsert_student_recommendation_and_emit',
    'trg_generate_recommendations'
);
-- Expected: 3 rows

-- Check dedupe index
SELECT indexname FROM pg_indexes
WHERE indexname = 'uq_student_reco_active';
-- Expected: 1 row

-- Verify Migration 006 triggers still exist
SELECT COUNT(*) FROM pg_trigger
WHERE tgname IN (
    'trg_update_student_baseline',
    'trg_update_mistake_patterns'
);
-- Expected: 2 rows (PRESERVED!)
```

**4. Success Indicators:**
```
✅ All 2 tables created
✅ 1 new trigger attached
✅ 3 functions created
✅ Dedupe index created
✅ Migration 006 triggers preserved
✅ No errors in output
```

---

## 🧪 POST-DEPLOYMENT TESTING

### **Quick Functional Test:**

```sql
-- ============================================
-- POST-DEPLOYMENT FUNCTIONAL TEST
-- ============================================

DO $$
DECLARE
    v_student_id UUID := gen_random_uuid();
BEGIN
    -- Insert 3 fast mistakes (PANIC_RUSH)
    FOR i IN 1..3 LOOP
        INSERT INTO student_mistakes (
            student_id,
            global_topic_uid,
            mistake_code,
            test_answer_id,
            time_spent_seconds,
            occurred_at
        ) VALUES (
            v_student_id,
            'TR.MAT.ALG.001',
            'CALCULATION_ERROR',
            NULL,
            3,
            NOW() + (i || ' seconds')::INTERVAL
        );
    END LOOP;
    
    RAISE NOTICE 'Test student: %', v_student_id;
END $$;

-- Check results
SELECT 
    (SELECT COUNT(*) FROM student_mistake_patterns) as patterns,
    (SELECT COUNT(*) FROM student_recommendations) as recommendations,
    (SELECT COUNT(*) FROM ui_reflex_events) as events;

-- Expected (after 3 runs):
-- patterns: 3
-- recommendations: 1-3 (depending on data)
-- events: 1-3

-- Cleanup test data
-- DELETE FROM ui_reflex_events;
-- DELETE FROM student_recommendations;
-- DELETE FROM student_mistake_patterns;
-- DELETE FROM student_mistakes;
```

---

## 🔄 ROLLBACK PROCEDURES

### **Migration 007 Rollback:**

```sql
-- ============================================
-- ROLLBACK MIGRATION 007 (if needed)
-- ============================================

-- 1. Drop trigger
DROP TRIGGER IF EXISTS trg_generate_recommendations ON student_mistake_patterns;

-- 2. Drop functions
DROP FUNCTION IF EXISTS trg_generate_recommendations();
DROP FUNCTION IF EXISTS upsert_student_recommendation_and_emit(UUID, VARCHAR, VARCHAR, TEXT, TEXT, JSONB, INT, UUID, TIMESTAMP);
DROP FUNCTION IF EXISTS build_reflex_recommendation_payload(VARCHAR, INT, INT, VARCHAR);

-- 3. Drop tables (CAREFUL - data will be lost!)
DROP TABLE IF EXISTS ui_reflex_events CASCADE;
DROP TABLE IF EXISTS student_recommendations CASCADE;

-- Verify rollback
SELECT tgname FROM pg_trigger WHERE tgname = 'trg_generate_recommendations';
-- Expected: 0 rows

SELECT table_name FROM information_schema.tables
WHERE table_name IN ('student_recommendations', 'ui_reflex_events');
-- Expected: 0 rows
```

### **Migration 006 Rollback:**

```sql
-- ============================================
-- ROLLBACK MIGRATION 006 (if needed)
-- ============================================

⚠️ WARNING: This will also break Migration 007!
⚠️ Rollback 007 first before rolling back 006!

-- 1. Drop triggers
DROP TRIGGER IF EXISTS trg_update_mistake_patterns ON student_mistakes;
DROP TRIGGER IF EXISTS trg_update_student_baseline ON student_mistakes;

-- 2. Drop functions
DROP FUNCTION IF EXISTS update_mistake_patterns();
DROP FUNCTION IF EXISTS update_student_baseline();

-- 3. Drop tables (CAREFUL - data will be lost!)
DROP TABLE IF EXISTS student_mistake_patterns CASCADE;
DROP TABLE IF EXISTS student_baseline_performance CASCADE;
DROP TABLE IF EXISTS student_analysis_settings CASCADE;
DROP TABLE IF EXISTS analysis_presets CASCADE;
DROP TABLE IF EXISTS system_settings CASCADE;

-- Verify rollback
SELECT tgname FROM pg_trigger
WHERE tgname IN ('trg_update_student_baseline', 'trg_update_mistake_patterns');
-- Expected: 0 rows

SELECT table_name FROM information_schema.tables
WHERE table_name IN (
    'system_settings', 'analysis_presets', 'student_analysis_settings',
    'student_baseline_performance', 'student_mistake_patterns'
);
-- Expected: 0 rows
```

---

## 📊 DEPLOYMENT SCENARIOS

### **Scenario A: Fresh Database**
```
1. Deploy Migration 006 ✅
2. Verify ✅
3. Deploy Migration 007 ✅
4. Verify ✅
5. Test ✅
→ Clean deployment
```

### **Scenario B: Existing Analytics Data**
```
1. Backup database ✅
2. Check for conflicts ✅
3. Deploy Migration 006 ✅
4. Verify existing data ✅
5. Deploy Migration 007 ✅
6. Verify ✅
7. Test ✅
→ Careful deployment
```

### **Scenario C: Staging → Production**
```
1. Deploy to staging ✅
2. Test thoroughly ✅
3. Document any issues ✅
4. Schedule production window ✅
5. Deploy to production ✅
6. Monitor performance ✅
7. Verify production data ✅
→ Professional deployment
```

---

## ⚠️ COMMON ISSUES & SOLUTIONS

### **Issue 1: "relation does not exist"**
```
Error: relation "test_records" does not exist

Solution:
✅ This is EXPECTED if test engine not deployed
✅ Migration 006 handles this gracefully
✅ System works in FK-free mode
✅ No action needed
```

### **Issue 2: FK constraint violation**
```
Error: violates foreign key constraint "student_mistakes_test_answer_id_fkey"

Solution:
✅ This is CORRECT behavior (data integrity protection)
✅ Either:
   a) Deploy test engine first, OR
   b) Use NULL for test_answer_id in tests
```

### **Issue 3: Trigger not firing**
```
Symptoms: Mistakes inserted, but patterns not analyzed

Diagnosis:
SELECT tgname, tgenabled FROM pg_trigger
WHERE tgname LIKE 'trg_%';

Solution:
-- Re-run migration SQL
-- Or manually enable trigger:
ALTER TABLE student_mistakes ENABLE TRIGGER trg_update_student_baseline;
ALTER TABLE student_mistakes ENABLE TRIGGER trg_update_mistake_patterns;
```

### **Issue 4: Duplicate recommendations**
```
Symptoms: Multiple active recommendations for same type

Diagnosis:
SELECT student_id, global_topic_uid, recommendation_type, COUNT(*)
FROM student_recommendations
WHERE is_active = true
GROUP BY student_id, global_topic_uid, recommendation_type
HAVING COUNT(*) > 1;

Solution:
-- Unique index should prevent this
-- If it happens, re-create index:
DROP INDEX IF EXISTS uq_student_reco_active;
CREATE UNIQUE INDEX uq_student_reco_active
ON student_recommendations(student_id, global_topic_uid, recommendation_type)
WHERE is_active = true;
```

---

## 📈 MONITORING

### **Health Checks (Run Daily):**

```sql
-- Check trigger health
SELECT 
    tgname,
    tgrelid::regclass AS table_name,
    tgenabled,
    CASE tgenabled
        WHEN 'O' THEN 'ENABLED ✅'
        WHEN 'D' THEN 'DISABLED ❌'
        ELSE 'UNKNOWN ⚠️'
    END AS status
FROM pg_trigger
WHERE tgname LIKE 'trg_%';

-- Check recommendation generation rate
SELECT 
    DATE(created_at) as date,
    COUNT(*) as recommendations_created
FROM student_recommendations
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Check UI event delivery rate
SELECT 
    DATE(created_at) as date,
    COUNT(*) as events_created,
    COUNT(CASE WHEN delivered = true THEN 1 END) as events_delivered,
    ROUND(100.0 * COUNT(CASE WHEN delivered = true THEN 1 END) / COUNT(*), 2) as delivery_rate
FROM ui_reflex_events
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## ✅ SUCCESS CRITERIA

### **Deployment Successful When:**
```
✅ All tables created
✅ All triggers attached and enabled
✅ All functions created
✅ Test data processes correctly
✅ Recommendations generated
✅ UI events emitted
✅ No errors in logs
✅ Performance acceptable (<50ms per trigger chain)
```

---

## 🎯 NEXT STEPS AFTER DEPLOYMENT

**1. Documentation:**
```
✅ Update README.md
✅ Create CHANGELOG.md
✅ Git commit with proper message
```

**2. UI Integration:**
```
⏭️ Frontend notification component
⏭️ Supabase Realtime subscription
⏭️ Test with real students
```

**3. Monitoring:**
```
⏭️ Set up daily health checks
⏭️ Monitor trigger performance
⏭️ Track recommendation effectiveness
```

---

**Status:** ✅ DEPLOYMENT GUIDE COMPLETE  
**Last Updated:** December 14, 2024  
**Migrations:** 006 v3.4.1 + 007 v1  
**Environment:** Production-Ready  

---

**Prepared by:** End.STP Team  
**For Support:** See MIGRATIONS_COMPLETE_SUMMARY.md
