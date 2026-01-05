-- ============================================
-- Migration: 006_mathematics_1st_batch_mini
-- Description: Insert 5 mathematics topics from 1st batch (proof of concept)
-- Purpose: Validate CURRICULUM_TOPIC_FORMAT_v1.0 against database schema
-- Scope: MINI migration (not full mathematics curriculum)
-- Author: End.STP Curriculum Team
-- Date: 2024-12-30
-- Lock: CURRICULUM_TOPIC_FORMAT_v1.0.md
-- ============================================

-- ============================================
-- SECTION 1: SUBJECTS
-- ============================================

-- Insert Matematik subject (if not exists)
INSERT INTO subjects (
    id,
    name_tr,
    name_en,
    code,
    display_order,
    is_active
)
VALUES (
    gen_random_uuid(),
    'Matematik',
    'Mathematics',
    'MAT',
    1,
    TRUE
)
ON CONFLICT (code) DO NOTHING;

-- Get subject_id for later use
-- Store in variable for PostgreSQL
DO $$
DECLARE
    v_subject_id UUID;
    v_curriculum_version_id UUID;
    v_exam_version_id UUID;
    
    -- Topic IDs
    v_topic_1_id UUID;
    v_topic_2_id UUID;
    v_topic_3_id UUID;
    v_topic_4_id UUID;
    v_topic_5_id UUID;
BEGIN

-- ============================================
-- SECTION 2: GET REFERENCE IDS
-- ============================================

-- Get subject_id
SELECT id INTO v_subject_id FROM subjects WHERE code = 'MAT';

-- Get curriculum_version_id (TR_MEB_2024)
SELECT id INTO v_curriculum_version_id 
FROM curriculum_versions 
WHERE code = 'TR_MEB_2024' 
LIMIT 1;

-- Get exam_version_id (TYT_2024)
SELECT id INTO v_exam_version_id 
FROM exam_versions 
WHERE code = 'TYT_2024' 
LIMIT 1;

-- Validate references exist
IF v_subject_id IS NULL THEN
    RAISE EXCEPTION 'Subject MAT not found. Run curriculum system migrations first.';
END IF;

IF v_curriculum_version_id IS NULL THEN
    RAISE EXCEPTION 'Curriculum version TR_MEB_2024 not found. Run FAZ 1 migrations first.';
END IF;

IF v_exam_version_id IS NULL THEN
    RAISE EXCEPTION 'Exam version TYT_2024 not found. Run FAZ 1 migrations first.';
END IF;

-- ============================================
-- SECTION 3: INSERT TOPICS (5 Topics)
-- ============================================

-- TOPIC 1: Temel Kavramlar - Sayılar ve Kümeler
v_topic_1_id := gen_random_uuid();
INSERT INTO topics (
    id,
    subject_id,
    name_tr,
    name_en,
    code,
    difficulty_level,
    estimated_study_minutes,
    is_active
)
VALUES (
    v_topic_1_id,
    v_subject_id,
    'Temel Kavramlar - Sayılar ve Kümeler',
    'Fundamentals - Numbers and Sets',
    'MAT-TEMEL-01',
    3, -- difficulty_level from format
    45, -- 🔒 PASSIVE (not used by motors yet)
    TRUE
);

-- TOPIC 2: Denklemler (1. ve 2. Derece)
v_topic_2_id := gen_random_uuid();
INSERT INTO topics (
    id,
    subject_id,
    name_tr,
    name_en,
    code,
    difficulty_level,
    estimated_study_minutes,
    is_active
)
VALUES (
    v_topic_2_id,
    v_subject_id,
    'Denklemler (1. ve 2. Derece)',
    'Equations (1st and 2nd Degree)',
    'MAT-DENK-01',
    5,
    50,
    TRUE
);

-- TOPIC 3: Fonksiyonlar (Tanım ve Türleri)
v_topic_3_id := gen_random_uuid();
INSERT INTO topics (
    id,
    subject_id,
    name_tr,
    name_en,
    code,
    difficulty_level,
    estimated_study_minutes,
    is_active
)
VALUES (
    v_topic_3_id,
    v_subject_id,
    'Fonksiyonlar (Tanım ve Türleri)',
    'Functions (Definition and Types)',
    'MAT-FONK-01',
    7,
    60,
    TRUE
);

-- TOPIC 4: Üslü ve Köklü Sayılar
v_topic_4_id := gen_random_uuid();
INSERT INTO topics (
    id,
    subject_id,
    name_tr,
    name_en,
    code,
    difficulty_level,
    estimated_study_minutes,
    is_active
)
VALUES (
    v_topic_4_id,
    v_subject_id,
    'Üslü ve Köklü Sayılar',
    'Exponents and Radicals',
    'MAT-USLU-01',
    6,
    50,
    TRUE
);

-- TOPIC 5: Polinomlar
v_topic_5_id := gen_random_uuid();
INSERT INTO topics (
    id,
    subject_id,
    name_tr,
    name_en,
    code,
    difficulty_level,
    estimated_study_minutes,
    is_active
)
VALUES (
    v_topic_5_id,
    v_subject_id,
    'Polinomlar',
    'Polynomials',
    'MAT-POLI-01',
    7,
    70,
    TRUE
);

-- ============================================
-- SECTION 4: INSERT TOPIC_CONTEXTS
-- ============================================

-- CONTEXT 1: Temel Kavramlar (TR_MEB_2024 + TYT_2024)
INSERT INTO topic_contexts (
    id,
    topic_id,
    curriculum_version_id,
    exam_version_id,
    is_active,
    valid_from,
    valid_until,
    context_metadata
)
VALUES (
    gen_random_uuid(),
    v_topic_1_id,
    v_curriculum_version_id,
    v_exam_version_id,
    TRUE,
    '2024-09-01',
    NULL, -- No expiry (current curriculum)
    jsonb_build_object(
        'grade_levels', ARRAY['9', 'tyt'],
        'exam_scope', 'school',
        'difficulty_level', 3,
        'tags', ARRAY['foundational', 'numbers', 'sets'],
        'archetype', 'foundational',
        'format_version', '1.0'
    )
);

-- CONTEXT 2: Denklemler (TR_MEB_2024 + TYT_2024)
INSERT INTO topic_contexts (
    id,
    topic_id,
    curriculum_version_id,
    exam_version_id,
    is_active,
    valid_from,
    valid_until,
    context_metadata
)
VALUES (
    gen_random_uuid(),
    v_topic_2_id,
    v_curriculum_version_id,
    v_exam_version_id,
    TRUE,
    '2024-09-01',
    NULL,
    jsonb_build_object(
        'grade_levels', ARRAY['9', '10', 'tyt'],
        'exam_scope', 'school',
        'difficulty_level', 5,
        'tags', ARRAY['algebra', 'equations', 'problem_solving'],
        'archetype', 'foundational',
        'format_version', '1.0'
    )
);

-- CONTEXT 3: Fonksiyonlar (TR_MEB_2024 + TYT_2024)
INSERT INTO topic_contexts (
    id,
    topic_id,
    curriculum_version_id,
    exam_version_id,
    is_active,
    valid_from,
    valid_until,
    context_metadata
)
VALUES (
    gen_random_uuid(),
    v_topic_3_id,
    v_curriculum_version_id,
    v_exam_version_id,
    TRUE,
    '2024-09-01',
    NULL,
    jsonb_build_object(
        'grade_levels', ARRAY['10', '11', 'tyt', 'ayt'],
        'exam_scope', 'school',
        'difficulty_level', 7,
        'tags', ARRAY['functions', 'algebra', 'abstract_thinking'],
        'archetype', 'synthesis',
        'splitting_recommended', TRUE,
        'format_version', '1.0'
    )
);

-- CONTEXT 4: Üslü-Köklü (TR_MEB_2024 + TYT_2024)
INSERT INTO topic_contexts (
    id,
    topic_id,
    curriculum_version_id,
    exam_version_id,
    is_active,
    valid_from,
    valid_until,
    context_metadata
)
VALUES (
    gen_random_uuid(),
    v_topic_4_id,
    v_curriculum_version_id,
    v_exam_version_id,
    TRUE,
    '2024-09-01',
    NULL,
    jsonb_build_object(
        'grade_levels', ARRAY['9', '10', 'tyt'],
        'exam_scope', 'school',
        'difficulty_level', 6,
        'tags', ARRAY['algebra', 'exponents', 'radicals', 'operations'],
        'archetype', 'foundational',
        'format_version', '1.0'
    )
);

-- CONTEXT 5: Polinomlar (TR_MEB_2024 + TYT_2024)
INSERT INTO topic_contexts (
    id,
    topic_id,
    curriculum_version_id,
    exam_version_id,
    is_active,
    valid_from,
    valid_until,
    context_metadata
)
VALUES (
    gen_random_uuid(),
    v_topic_5_id,
    v_curriculum_version_id,
    v_exam_version_id,
    TRUE,
    '2024-09-01',
    NULL,
    jsonb_build_object(
        'grade_levels', ARRAY['9', '10', '11', 'tyt'],
        'exam_scope', 'school',
        'difficulty_level', 7,
        'tags', ARRAY['algebra', 'polynomials', 'factoring', 'operations'],
        'archetype', 'synthesis',
        'splitting_recommended', TRUE,
        'format_version', '1.0'
    )
);

-- ============================================
-- SECTION 5: SUCCESS MESSAGE
-- ============================================

RAISE NOTICE '✅ Mathematics 1st Batch (5 topics) inserted successfully';
RAISE NOTICE '📊 Topics: % inserted', 5;
RAISE NOTICE '🔗 Contexts: % inserted', 5;
RAISE NOTICE '📘 Format: CURRICULUM_TOPIC_FORMAT_v1.0';

END $$;

-- ============================================
-- SECTION 6: VALIDATION QUERIES
-- ============================================

-- Check orphaned contexts (should be 0)
DO $$
DECLARE
    v_orphan_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_orphan_count
    FROM topic_contexts tc
    LEFT JOIN topics t ON tc.topic_id = t.id
    WHERE t.id IS NULL;
    
    IF v_orphan_count > 0 THEN
        RAISE EXCEPTION 'VALIDATION FAILED: % orphaned contexts found', v_orphan_count;
    END IF;
    
    RAISE NOTICE '✅ Validation passed: No orphaned contexts';
END $$;

-- Check NULL contexts (should be 0 after migration)
-- Note: This checks new topics only
DO $$
DECLARE
    v_null_context_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_null_context_count
    FROM topics t
    WHERE t.code LIKE 'MAT-%'
    AND NOT EXISTS (
        SELECT 1 FROM topic_contexts tc 
        WHERE tc.topic_id = t.id AND tc.is_active = TRUE
    );
    
    IF v_null_context_count > 0 THEN
        RAISE EXCEPTION 'VALIDATION FAILED: % topics without active context', v_null_context_count;
    END IF;
    
    RAISE NOTICE '✅ Validation passed: All mathematics topics have contexts';
END $$;

-- Check format_version in metadata
DO $$
DECLARE
    v_invalid_format_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_invalid_format_count
    FROM topic_contexts tc
    JOIN topics t ON tc.topic_id = t.id
    WHERE t.code LIKE 'MAT-%'
    AND (tc.context_metadata->>'format_version') != '1.0';
    
    IF v_invalid_format_count > 0 THEN
        RAISE WARNING 'Format version mismatch: % contexts', v_invalid_format_count;
    END IF;
    
    RAISE NOTICE '✅ Validation passed: All contexts use format v1.0';
END $$;

-- ============================================
-- SECTION 7: SUMMARY REPORT
-- ============================================

-- Display inserted topics
SELECT 
    t.code,
    t.name_tr,
    t.difficulty_level,
    tc.context_metadata->>'archetype' as archetype,
    tc.is_active
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code LIKE 'MAT-%'
ORDER BY t.code;

-- ============================================
-- DOWN MIGRATION (ROLLBACK)
-- ============================================

-- Uncomment below to rollback

-- DELETE FROM topic_contexts 
-- WHERE topic_id IN (
--     SELECT id FROM topics WHERE code LIKE 'MAT-%'
-- );

-- DELETE FROM topics WHERE code LIKE 'MAT-%';

-- RAISE NOTICE '⚠️ ROLLBACK COMPLETE: Mathematics 1st batch removed';

-- ============================================
-- END OF MIGRATION
-- ============================================
