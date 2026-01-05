-- =============================================
-- VALIDATION QUERIES FOR MIGRATION 006
-- Mathematics 1st Batch (5 Topics)
-- =============================================

-- =============================================
-- QUERY 1: Check Topics Were Inserted
-- =============================================
-- Expected: 5 rows (MAT-TEMEL-01, MAT-DENK-01, MAT-FONK-01, MAT-USLU-01, MAT-POLI-01)

SELECT 
    code,
    name_tr,
    difficulty_level,
    grade_level,
    is_active,
    created_at
FROM topics
WHERE code IN (
    'MAT-TEMEL-01',
    'MAT-DENK-01',
    'MAT-FONK-01',
    'MAT-USLU-01',
    'MAT-POLI-01'
)
ORDER BY code;

-- =============================================
-- QUERY 2: Check Topic Contexts Were Created
-- =============================================
-- Expected: 5 rows with format_version='1.0'

SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'format_version' as format_version,
    tc.metadata->>'archetype' as archetype,
    jsonb_array_length(tc.metadata->'learning_objectives') as objectives_count,
    tc.created_at
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-TEMEL-01',
    'MAT-DENK-01',
    'MAT-FONK-01',
    'MAT-USLU-01',
    'MAT-POLI-01'
)
ORDER BY t.code;

-- =============================================
-- QUERY 3: Check Archetype Distribution
-- =============================================
-- Expected: foundational=3, synthesis=2

SELECT 
    tc.metadata->>'archetype' as archetype,
    COUNT(*) as count
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-TEMEL-01',
    'MAT-DENK-01',
    'MAT-FONK-01',
    'MAT-USLU-01',
    'MAT-POLI-01'
)
GROUP BY tc.metadata->>'archetype'
ORDER BY archetype;

-- =============================================
-- QUERY 4: Check for Orphaned Contexts
-- =============================================
-- Expected: 0 rows (no contexts without topics)

SELECT 
    tc.id,
    tc.topic_id,
    tc.created_at
FROM topic_contexts tc
LEFT JOIN topics t ON tc.topic_id = t.id
WHERE t.id IS NULL;

-- =============================================
-- QUERY 5: Check Subject Exists
-- =============================================
-- Expected: 1 row (MAT subject)

SELECT 
    code,
    name_tr,
    is_active
FROM subjects
WHERE code = 'MAT';

-- =============================================
-- QUERY 6: Check Curriculum Version Link
-- =============================================
-- Expected: 5 rows, all linked to TR+MEB+2024

SELECT 
    t.code,
    t.name_tr,
    cv.country_code,
    cv.system_code,
    cv.academic_year,
    cv.version_label
FROM topics t
JOIN curriculum_versions cv ON t.curriculum_version_id = cv.id
WHERE t.code IN (
    'MAT-TEMEL-01',
    'MAT-DENK-01',
    'MAT-FONK-01',
    'MAT-USLU-01',
    'MAT-POLI-01'
)
ORDER BY t.code;

-- =============================================
-- QUERY 7: Full Metadata Check
-- =============================================
-- Expected: 5 rows with complete metadata

SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'format_version' as format_version,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->>'cognitive_level' as cognitive_level,
    jsonb_array_length(tc.metadata->'learning_objectives') as objectives_count,
    jsonb_array_length(tc.metadata->'prerequisites') as prerequisites_count,
    jsonb_array_length(tc.metadata->'tags') as tags_count,
    (tc.metadata->'splitting_guidance'->>'recommended')::boolean as splitting_recommended
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-TEMEL-01',
    'MAT-DENK-01',
    'MAT-FONK-01',
    'MAT-USLU-01',
    'MAT-POLI-01'
)
ORDER BY t.code;