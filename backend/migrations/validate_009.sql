-- ============================================
-- VALIDATION QUERIES FOR MIGRATION 009
-- Mathematics 4th Batch: 8 Topics
-- Expected: 25 total topics, 13F/12S balance
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
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
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
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
)
ORDER BY t.code;
-- Expected: 8 rows, all with format_version=1.0

-- Query 3: Cumulative totals (should be 25 topics, 13F/12S)
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
-- Expected: total=25, context=25, foundational=13, synthesis=12, completion=100%

-- ============================================
-- DETAILED VALIDATION
-- ============================================

-- Query 4: Check prerequisite relationships (4th batch)
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    jsonb_array_length(COALESCE(tc.metadata->'prerequisite_topics', '[]'::jsonb)) as prereq_count,
    tc.metadata->'prerequisite_topics' as prerequisites
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
)
ORDER BY prereq_count DESC, t.code;
-- Expected: 
--   MAT-USLU-LOGA-01: 3 prereqs
--   MAT-TUMEVARIM-01: 2 prereqs
--   MAT-OLASILIK-DAGIL-01: 2 prereqs
--   MAT-KARMASIK-01: 2 prereqs
--   MAT-PERM-01: 1 prereq
--   MAT-BOLME-01: 1 prereq
--   MAT-MANTIK-01: 0 prereqs
--   MAT-KUME-01: 0 prereqs

-- Query 5: Difficulty distribution (4th batch)
SELECT 
    tc.metadata->>'archetype' as archetype,
    t.difficulty_level,
    COUNT(*) as count,
    string_agg(t.code, ', ' ORDER BY t.code) as topics
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
)
GROUP BY tc.metadata->>'archetype', t.difficulty_level
ORDER BY archetype, difficulty_level;
-- Expected distribution:
--   Foundational: difficulty 4-6
--   Synthesis: difficulty 7-8

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
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
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
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
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
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01'
)
ORDER BY t.code;
-- Expected: All 4 foundational should have needs_splitting=false

-- Query 9: OSYM exam frequency check (4th batch)
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->'osym_exam_relevance'->>'tyt' as tyt_relevance,
    tc.metadata->'osym_exam_relevance'->>'ayt' as ayt_relevance
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
)
ORDER BY t.code;
-- Expected: TYT-heavy for foundational, AYT-heavy for synthesis

-- Query 10: Learning objectives count (4th batch)
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    jsonb_array_length(tc.metadata->'learning_objectives') as objective_count
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
)
ORDER BY objective_count DESC, t.code;
-- Expected: All should have 4-6 learning objectives

-- ============================================
-- FINAL HEALTH CHECK
-- ============================================

-- Query 11: Complete Mathematics Status
SELECT 
    'Mathematics 4th Batch Health Check' as metric,
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
SELECT 'Completion %', 
    ROUND(100.0 * COUNT(DISTINCT tc.id) / NULLIF(COUNT(DISTINCT t.id), 0), 1)::text || '%'
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT';
-- Expected:
--   Total: 25
--   With Context: 25
--   Foundational: 13
--   Synthesis: 12
--   With Prerequisites: ~18
--   Completion: 62.5%

-- ============================================
-- PREREQUISITE CHAIN VALIDATION
-- ============================================

-- Query 12: New prerequisite chains formed in 4th batch
WITH RECURSIVE prereq_chain AS (
    -- Base: Topics from 4th batch
    SELECT 
        t.code,
        t.name_tr,
        tc.metadata->'prerequisite_topics' as prereqs,
        1 as level
    FROM topics t
    JOIN topic_contexts tc ON t.id = tc.topic_id
    WHERE t.code IN (
        'MAT-PERM-01', 'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 
        'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
    )
    AND jsonb_array_length(tc.metadata->'prerequisite_topics') > 0
)
SELECT 
    code,
    name_tr,
    level,
    prereqs
FROM prereq_chain
ORDER BY level DESC, code;
-- Expected: Shows new chains:
--   Kombinatorik → Permütasyon
--   Kombinatorik → Olasılık → Olasılık Dağılımları
--   Mantık + Diziler → Tümevarım
--   Fonksiyon → Karmaşık Sayılar

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
--   foundational: 13 (52%)
--   synthesis: 12 (48%)
--   Perfect balance maintained!
