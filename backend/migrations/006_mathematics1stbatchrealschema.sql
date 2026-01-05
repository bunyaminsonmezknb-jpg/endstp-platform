-- =============================================
-- MIGRATION 006: Mathematics 1st Batch (5 Topics)
-- Context Layer Format v1.0
-- ADAPTED TO REAL DATABASE SCHEMA
-- =============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_subject_id UUID;
    
    -- Topic IDs (will be retrieved after INSERT)
    v_topic_temel UUID;
    v_topic_denk UUID;
    v_topic_fonk UUID;
    v_topic_uslu UUID;
    v_topic_poli UUID;
BEGIN

    -- =============================================
    -- SECTION 1: Get Reference IDs
    -- =============================================
    
    RAISE NOTICE '=== SECTION 1: Getting Reference IDs ===';
    
    -- 1A. Get curriculum_version_id (TR + MEB + 2024)
    SELECT id INTO v_curriculum_version_id
    FROM curriculum_versions
    WHERE country_code = 'TR'
      AND system_code = 'MEB'
      AND academic_year = 2024
      AND is_active = true
    LIMIT 1;
    
    IF v_curriculum_version_id IS NULL THEN
        RAISE EXCEPTION 'curriculum_version not found (TR + MEB + 2024)';
    END IF;
    
    RAISE NOTICE 'Curriculum Version ID: %', v_curriculum_version_id;
    
    -- 1B. Get subject_id (Matematik)
    SELECT id INTO v_subject_id
    FROM subjects
    WHERE code = 'MAT'
    LIMIT 1;
    
    IF v_subject_id IS NULL THEN
        -- Create MAT if doesn't exist
        INSERT INTO subjects (code, name_tr, is_active)
        VALUES ('MAT', 'Matematik', true)
        ON CONFLICT (code) DO NOTHING
        RETURNING id INTO v_subject_id;
        
        RAISE NOTICE 'Created subject: MAT';
    ELSE
        RAISE NOTICE 'Using existing subject: MAT (id: %)', v_subject_id;
    END IF;
    
    -- =============================================
    -- SECTION 2: Insert Topics (5 topics)
    -- =============================================
    
    RAISE NOTICE '=== SECTION 2: Inserting Topics ===';
    
    -- Topic 1: Temel Kavramlar
    INSERT INTO topics (
        subject_id,
        code,
        name_tr,
        curriculum_version_id,
        is_active,
        difficulty_level,
        grade_level
    ) VALUES (
        v_subject_id,
        'MAT-TEMEL-01',
        'Temel Kavramlar ve İşlemler',
        v_curriculum_version_id,
        true,
        3,
        '9'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_temel;
    
    IF v_topic_temel IS NULL THEN
        SELECT id INTO v_topic_temel FROM topics WHERE code = 'MAT-TEMEL-01';
    END IF;
    RAISE NOTICE 'Topic 1: MAT-TEMEL-01 (id: %)', v_topic_temel;
    
    -- Topic 2: Denklemler
    INSERT INTO topics (
        subject_id,
        code,
        name_tr,
        curriculum_version_id,
        is_active,
        difficulty_level,
        grade_level
    ) VALUES (
        v_subject_id,
        'MAT-DENK-01',
        'Denklemler ve Eşitsizlikler',
        v_curriculum_version_id,
        true,
        5,
        '9'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_denk;
    
    IF v_topic_denk IS NULL THEN
        SELECT id INTO v_topic_denk FROM topics WHERE code = 'MAT-DENK-01';
    END IF;
    RAISE NOTICE 'Topic 2: MAT-DENK-01 (id: %)', v_topic_denk;
    
    -- Topic 3: Fonksiyonlar
    INSERT INTO topics (
        subject_id,
        code,
        name_tr,
        curriculum_version_id,
        is_active,
        difficulty_level,
        grade_level
    ) VALUES (
        v_subject_id,
        'MAT-FONK-01',
        'Fonksiyonlar',
        v_curriculum_version_id,
        true,
        6,
        '9,10,tyt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_fonk;
    
    IF v_topic_fonk IS NULL THEN
        SELECT id INTO v_topic_fonk FROM topics WHERE code = 'MAT-FONK-01';
    END IF;
    RAISE NOTICE 'Topic 3: MAT-FONK-01 (id: %)', v_topic_fonk;
    
    -- Topic 4: Üslü-Köklü Sayılar
    INSERT INTO topics (
        subject_id,
        code,
        name_tr,
        curriculum_version_id,
        is_active,
        difficulty_level,
        grade_level
    ) VALUES (
        v_subject_id,
        'MAT-USLU-01',
        'Üslü ve Köklü Sayılar',
        v_curriculum_version_id,
        true,
        4,
        '9,tyt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_uslu;
    
    IF v_topic_uslu IS NULL THEN
        SELECT id INTO v_topic_uslu FROM topics WHERE code = 'MAT-USLU-01';
    END IF;
    RAISE NOTICE 'Topic 4: MAT-USLU-01 (id: %)', v_topic_uslu;
    
    -- Topic 5: Polinomlar
    INSERT INTO topics (
        subject_id,
        code,
        name_tr,
        curriculum_version_id,
        is_active,
        difficulty_level,
        grade_level
    ) VALUES (
        v_subject_id,
        'MAT-POLI-01',
        'Polinomlar',
        v_curriculum_version_id,
        true,
        7,
        '9,10,tyt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_poli;
    
    IF v_topic_poli IS NULL THEN
        SELECT id INTO v_topic_poli FROM topics WHERE code = 'MAT-POLI-01';
    END IF;
    RAISE NOTICE 'Topic 5: MAT-POLI-01 (id: %)', v_topic_poli;
    
    -- =============================================
    -- SECTION 3: Insert topic_contexts (5 contexts)
    -- =============================================
    
    RAISE NOTICE '=== SECTION 3: Inserting Topic Contexts ===';
    
    -- Context 1: Temel Kavramlar
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_temel,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Sayı kümelerini tanımlayabilme',
                'Rasyonel sayılarla işlem yapabilme',
                'Mutlak değer kavramını kullanabilme',
                'Oran-orantı problemlerini çözebilme'
            ),
            'prerequisites', jsonb_build_array(
                'Tam sayılar',
                'Kesirler',
                'Ondalık sayılar'
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('9', 'tyt'),
                'exam_scope', 'school',
                'frequency', 'Çok Yüksek'
            ),
            'cognitive_level', 'comprehension',
            'splitting_guidance', jsonb_build_object(
                'recommended', false,
                'reason', 'Foundational topic, keep unified'
            ),
            'tags', jsonb_build_array('foundational', 'number_systems', 'arithmetic'),
            'archetype', 'foundational',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 1: Temel Kavramlar';
    
    -- Context 2: Denklemler
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_denk,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Birinci derece denklem kurabilme ve çözebilme',
                'Mutlak değerli denklemleri çözebilme',
                'Eşitsizlik çözebilme',
                'Denklem sistemlerini çözebilme'
            ),
            'prerequisites', jsonb_build_array(
                'Temel Kavramlar',
                'Dört işlem',
                'Parantez açma'
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('9', 'tyt'),
                'exam_scope', 'school',
                'frequency', 'Yüksek'
            ),
            'cognitive_level', 'application',
            'splitting_guidance', jsonb_build_object(
                'recommended', true,
                'reason', 'Multiple problem types can be separated',
                'suggested_splits', jsonb_build_array(
                    'Birinci derece denklemler',
                    'Mutlak değerli denklemler',
                    'Eşitsizlikler'
                )
            ),
            'tags', jsonb_build_array('equations', 'problem_solving', 'algebra'),
            'archetype', 'synthesis',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 2: Denklemler';
    
    -- Context 3: Fonksiyonlar
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_fonk,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Fonksiyon kavramını anlayabilme',
                'Fonksiyon türlerini ayırt edebilme',
                'Fonksiyonların grafiklerini çizebilme',
                'Bileşke ve ters fonksiyon bulabilme'
            ),
            'prerequisites', jsonb_build_array(
                'Kartezyen çarpım',
                'İkili bağıntılar',
                'Koordinat sistemi'
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('9', '10', 'tyt'),
                'exam_scope', 'school',
                'frequency', 'Çok Yüksek'
            ),
            'cognitive_level', 'analysis',
            'splitting_guidance', jsonb_build_object(
                'recommended', true,
                'reason', 'Complex topic with distinct subtopics',
                'suggested_splits', jsonb_build_array(
                    'Fonksiyon tanımı ve türleri',
                    'Fonksiyon grafikleri',
                    'Bileşke ve ters fonksiyon'
                )
            ),
            'tags', jsonb_build_array('functions', 'graphs', 'algebra'),
            'archetype', 'synthesis',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 3: Fonksiyonlar';
    
    -- Context 4: Üslü-Köklü Sayılar
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_uslu,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Üslü ifadeleri sadeleştirebilme',
                'Köklü sayılarla işlem yapabilme',
                'Üslü ve köklü sayıları birlikte kullanabilme',
                'Bilimsel gösterim yapabilme'
            ),
            'prerequisites', jsonb_build_array(
                'Tam sayılar',
                'Çarpma-bölme',
                'Üs alma işlemi'
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('9', 'tyt'),
                'exam_scope', 'school',
                'frequency', 'Orta'
            ),
            'cognitive_level', 'application',
            'splitting_guidance', jsonb_build_object(
                'recommended', false,
                'reason', 'Closely related concepts, keep together'
            ),
            'tags', jsonb_build_array('exponents', 'radicals', 'algebra'),
            'archetype', 'foundational',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 4: Üslü-Köklü Sayılar';
    
    -- Context 5: Polinomlar
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_poli,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Polinom kavramını anlayabilme',
                'Polinomlarla işlem yapabilme',
                'Çarpanlara ayırma yapabilme',
                'Polinom denklemlerini çözebilme'
            ),
            'prerequisites', jsonb_build_array(
                'Cebirsel ifadeler',
                'Çarpma-bölme',
                'Parantez açma'
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('9', '10', 'tyt'),
                'exam_scope', 'school',
                'frequency', 'Yüksek'
            ),
            'cognitive_level', 'application',
            'splitting_guidance', jsonb_build_object(
                'recommended', false,
                'reason', 'Single coherent topic'
            ),
            'tags', jsonb_build_array('polynomials', 'factoring', 'algebra'),
            'archetype', 'foundational',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 5: Polinomlar';
    
    -- =============================================
    -- SUCCESS MESSAGE
    -- =============================================
    
    RAISE NOTICE '=== ✅ Migration 006 Completed Successfully ===';
    RAISE NOTICE 'Inserted 5 mathematics topics with Context Layer metadata';
    RAISE NOTICE 'Format Version: 1.0';
    RAISE NOTICE 'Archetypes: 3 foundational, 2 synthesis';

END $$;