-- ============================================
-- VALIDATION QUERIES FOR MIGRATION 010
-- Mathematics 5th Batch: 8 Topics
-- Expected: 33 total topics, 17F/16S balance
-- ============================================

-- ============================================
-- QUICK CHECKS (Run these first!)
-- ============================================

-- Query 1: Verify all 8 new topics exist
SELECT 
    code,
    name_tr,
    difficulty_level,
    grade_level
FROM topics
WHERE code IN (
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY code;
-- Expected: 8 rows

-- Query 2: Verify all 8 contexts created
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->>'format_version' as format
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY t.code;
-- Expected: 8 rows, all with format_version=1.0

-- Query 3: Cumulative totals (should be 33 topics, 17F/16S)
SELECT 
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT tc.id) as with_context,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END) as foundational,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'synthesis' THEN 1 ELSE 0 END) as synthesis,
    ROUND(100.0 * COUNT(DISTINCT tc.id) / NULLIF(COUNT(DISTINCT t.id), 0), 1) || '%' as completion_pct
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT';
-- Expected: total=33, context=33, foundational=17, synthesis=16, completion=100%

-- ============================================
-- DETAILED VALIDATION
-- ============================================

-- Query 4: Check prerequisite relationships (5th batch)
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    jsonb_array_length(COALESCE(tc.metadata->'prerequisite_topics', '[]'::jsonb)) as prereq_count,
    tc.metadata->'prerequisite_topics' as prerequisites
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY prereq_count DESC, t.code;
-- Expected: 
--   MAT-ESITSIZ-01: 2 prereqs
--   MAT-CARPAN-01: 2 prereqs
--   MAT-FONK-GRAF-01: 2 prereqs
--   MAT-ORAN-01: 1 prereq
--   MAT-MUTLAK-01: 1 prereq
--   MAT-BASAM-01: 1 prereq
--   MAT-MODUL-01: 1 prereq
--   MAT-KOKLU-01: 1 prereq

-- Query 5: Difficulty distribution (5th batch)
SELECT 
    tc.metadata->>'archetype' as archetype,
    t.difficulty_level,
    COUNT(*) as count,
    string_agg(t.code, ', ' ORDER BY t.code) as topics
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
GROUP BY tc.metadata->>'archetype', t.difficulty_level
ORDER BY archetype, difficulty_level;
-- Expected distribution:
--   Foundational: difficulty 5-7
--   Synthesis: difficulty 6-8

-- Query 6: Check splitting recommendations (synthesis topics only)
SELECT 
    t.code,
    t.name_tr,
    (tc.metadata->'splitting'->>'recommended')::boolean as split_recommended,
    jsonb_array_length(COALESCE(tc.metadata->'splitting'->'parts', '[]'::jsonb)) as part_count,
    tc.metadata->'splitting'->>'rationale' as rationale
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY t.code;
-- Expected: All 4 synthesis topics should have split_recommended=true

-- Query 7: Check ROI guidance (synthesis topics only)
SELECT 
    t.code,
    t.name_tr,
    jsonb_array_length(tc.metadata->'roi_guidance'->'high_yield_subtopics') as high_yield_count,
    jsonb_array_length(tc.metadata->'roi_guidance'->'low_yield_subtopics') as low_yield_count,
    jsonb_array_length(tc.metadata->'roi_guidance'->'skip_if_time_limited') as skip_count
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY t.code;
-- Expected: All 4 should have high_yield, low_yield, skip arrays

-- Query 8: Check 20min suitability (foundational topics only)
SELECT 
    t.code,
    t.name_tr,
    (tc.metadata->'splitting'->>'recommended')::boolean as needs_splitting,
    tc.metadata->'splitting'->>'rationale' as rationale
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01'
)
ORDER BY t.code;
-- Expected: All 4 foundational should have needs_splitting=false

-- Query 9: OSYM exam frequency check (5th batch)
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->'osym_exam_relevance'->>'tyt' as tyt_relevance,
    tc.metadata->'osym_exam_relevance'->>'ayt' as ayt_relevance
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY t.code;
-- Expected: Mix of TYT and AYT relevance

-- Query 10: Learning objectives count (5th batch)
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    jsonb_array_length(tc.metadata->'learning_objectives') as objective_count
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY objective_count DESC, t.code;
-- Expected: All should have 4-6 learning objectives

-- ============================================
-- FINAL HEALTH CHECK
-- ============================================

-- Query 11: Complete Mathematics Status
SELECT 
    'Mathematics 5th Batch Health Check' as metric,
    '=========================' as separator
UNION ALL
SELECT 'Total Topics', COUNT(DISTINCT t.id)::text
FROM topics t
JOIN subjects s ON t.subject_id = s.id
WHERE s.code = 'MAT'
UNION ALL
SELECT 'With Context', COUNT(DISTINCT tc.id)::text
FROM topics t
JOIN subjects s ON t.subject_id = s.id
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT'
UNION ALL
SELECT 'Foundational', COUNT(*)::text
FROM topics t
JOIN subjects s ON t.subject_id = s.id
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT' AND tc.metadata->>'archetype' = 'foundational'
UNION ALL
SELECT 'Synthesis', COUNT(*)::text
FROM topics t
JOIN subjects s ON t.subject_id = s.id
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT' AND tc.metadata->>'archetype' = 'synthesis'
UNION ALL
SELECT 'With Prerequisites', COUNT(*)::text
FROM topics t
JOIN subjects s ON t.subject_id = s.id
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT' 
  AND jsonb_array_length(COALESCE(tc.metadata->'prerequisite_topics', '[]'::jsonb)) > 0
UNION ALL
SELECT 'Target Progress', '33/40 (82.5%)'
UNION ALL
SELECT 'Completion %', 
    ROUND(100.0 * COUNT(DISTINCT tc.id) / NULLIF(COUNT(DISTINCT t.id), 0), 1)::text || '%'
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT';
-- Expected:
--   Total: 33-37 (some old topics may exist)
--   With Context: 33
--   Foundational: 17
--   Synthesis: 16
--   With Prerequisites: ~22
--   Target Progress: 33/40 (82.5%)
--   Completion: ~90%+

-- ============================================
-- PREREQUISITE CHAIN VALIDATION
-- ============================================

-- Query 12: New prerequisite chains formed in 5th batch
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->'prerequisite_topics' as prerequisites
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-MODUL-01', 'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 
    'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
AND jsonb_array_length(tc.metadata->'prerequisite_topics') > 0
ORDER BY t.code;
-- Expected: Shows new chains:
--   Bölünebilme → Modüler Aritmetik
--   Temel + Fonksiyon → Eşitsizlikler
--   Temel + Polinom → Çarpanlara Ayırma
--   Üslü → Köklü İfadeler
--   Fonksiyon + Limit → Fonksiyon Grafikleri

-- ============================================
-- ARCHETYPE BALANCE CHECK
-- ============================================

-- Query 13: Cumulative archetype distribution
SELECT 
    tc.metadata->>'archetype' as archetype,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as percentage
FROM topics t
JOIN subjects s ON t.subject_id = s.id
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT'
GROUP BY tc.metadata->>'archetype'
ORDER BY count DESC;
-- Expected: 
--   foundational: 17 (51.5%)
--   synthesis: 16 (48.5%)
--   Perfect balance maintained!

-- ============================================
-- PROGRESS TRACKING
-- ============================================

-- Query 14: Batch-by-batch progress
WITH batch_info AS (
    SELECT 
        'Batch 1' as batch_name,
        5 as topics_added,
        5 as cumulative_total
    UNION ALL SELECT 'Batch 2', 5, 10
    UNION ALL SELECT 'Batch 3', 7, 17
    UNION ALL SELECT 'Batch 4', 8, 25
    UNION ALL SELECT 'Batch 5', 8, 33
)
SELECT 
    batch_name,
    topics_added,
    cumulative_total,
    ROUND(100.0 * cumulative_total / 40, 1) || '%' as progress_pct
FROM batch_info
ORDER BY cumulative_total;
-- Shows progression: 12.5% → 25% → 42.5% → 62.5% → 82.5%
