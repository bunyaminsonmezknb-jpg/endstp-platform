-- ============================================
-- VALIDATION QUERIES: PHYSICS 1ST BATCH
-- Migration: 012
-- Topics: 5 foundational (Büyüklükler, Hareket, Kuvvet, Enerji, Momentum)
-- Target: 5/35 (14% Physics complete)
-- ============================================

-- Query 1: Quick check - 5 topics inserted
SELECT 
    'Physics 1st Batch' as batch_name,
    COUNT(*) as topics_inserted
FROM topics
WHERE code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
);
-- Expected: 5

-- Query 2: Quick check - 5 contexts created
SELECT 
    'Physics Contexts' as batch_name,
    COUNT(*) as contexts_created
FROM topic_contexts tc
JOIN topics t ON tc.topic_id = t.id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
);
-- Expected: 5

-- Query 3: Physics cumulative status
SELECT 
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT tc.id) as with_context,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END) as foundational,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'synthesis' THEN 1 ELSE 0 END) as synthesis,
    ROUND(100.0 * COUNT(DISTINCT tc.id) / NULLIF(COUNT(DISTINCT t.id), 0), 1) || '%' as completion
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'FIZ';
-- Expected: 5 topics, 5 contexts, 5F, 0S, ~14-20% completion

-- Query 4: Topic details with context status
SELECT 
    t.code,
    t.name_tr,
    t.difficulty_level,
    CASE WHEN tc.id IS NULL THEN 'MISSING' ELSE 'OK' END as context_status,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->'osym_exam_relevance'->>'tyt' as tyt_relevance
FROM topics t
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY t.code;
-- All should have status = 'OK' and archetype = 'foundational'

-- Query 5: Prerequisites check
SELECT 
    t.code,
    t.name_tr,
    jsonb_array_length(COALESCE(tc.metadata->'prerequisite_topics', '[]'::jsonb)) as prereq_count
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY prereq_count, t.code;
-- FIZ-BUYUK-01: 0 prereqs (base)
-- FIZ-HAREKET-01: 1 prereq (Büyüklükler)
-- Others: 2 prereqs (Büyüklükler + Hareket)

-- Query 6: Format version consistency
SELECT 
    tc.metadata->>'format_version' as format_version,
    COUNT(*) as topic_count
FROM topic_contexts tc
JOIN topics t ON tc.topic_id = t.id
JOIN subjects s ON t.subject_id = s.id
WHERE s.code = 'FIZ'
GROUP BY tc.metadata->>'format_version';
-- Expected: v1.0 for all 5 topics

-- Query 7: Time estimates check
SELECT 
    t.code,
    (tc.metadata->'time_estimate'->>'foundation')::int as foundation_mins,
    (tc.metadata->'time_estimate'->>'practice')::int as practice_mins,
    (tc.metadata->'time_estimate'->>'mastery')::int as mastery_mins,
    (tc.metadata->'time_estimate'->>'foundation')::int + 
    (tc.metadata->'time_estimate'->>'practice')::int + 
    (tc.metadata->'time_estimate'->>'mastery')::int as total_mins
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY total_mins;
-- All should be ~450-750 minutes (7-12 hours study time per topic)

-- Query 8: Misconceptions check
SELECT 
    t.code,
    jsonb_array_length(tc.metadata->'misconceptions') as misconception_count
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY t.code;
-- Each should have 5 misconceptions

-- Query 9: OSYM relevance check
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->'osym_exam_relevance'->>'tyt' as tyt,
    tc.metadata->'osym_exam_relevance'->>'ayt' as ayt
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY t.code;
-- All should have 'Yüksek' or 'Çok Yüksek' for TYT

-- Query 10: 20min suitability check (foundational topics)
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->'splitting'->>'recommended' as split_recommended,
    CASE 
        WHEN tc.metadata->'splitting'->>'recommended' = 'false' THEN '20min OK'
        ELSE 'NEEDS SPLIT'
    END as suitability
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY t.code;
-- All foundational topics should be '20min OK' (splitting = false)

-- Query 11: PHYSICS vs MATHEMATICS comparison
SELECT 
    s.code as subject_code,
    s.name_tr as subject_name,
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT tc.id) as with_context,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END) as foundational,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'synthesis' THEN 1 ELSE 0 END) as synthesis,
    ROUND(100.0 * COUNT(DISTINCT tc.id) / NULLIF(COUNT(DISTINCT t.id), 0), 1) as completion_pct
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code IN ('MAT', 'FIZ')
GROUP BY s.code, s.name_tr
ORDER BY s.code;
-- MAT: 40 topics (100% complete)
-- FIZ: 5 topics (14% complete, just started!)

-- ============================================
-- QUICK SUMMARY
-- ============================================

SELECT 
    '1ST BATCH COMPLETE' as status,
    '5F / 0S' as archetype_split,
    '5 / 35 topics' as progress,
    '14%% Physics complete' as completion,
    'Format v1.0 REUSED' as format_status,
    '3x velocity expected' as velocity_target;
