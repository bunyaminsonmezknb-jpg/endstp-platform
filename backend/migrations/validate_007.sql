-- =============================================
-- MIGRATION 007: Mathematics 2nd Batch (5 Topics)
-- Context Layer Format v1.0
-- Topics: Trigonometri, Logaritma, Diziler, Limit, Türev
-- =============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_subject_id UUID;
    
    -- Topic IDs (will be retrieved after INSERT)
    v_topic_trig UUID;
    v_topic_loga UUID;
    v_topic_dizi UUID;
    v_topic_limit UUID;
    v_topic_turev UUID;
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
      AND is_active = true
    LIMIT 1;
    
    IF v_subject_id IS NULL THEN
        RAISE EXCEPTION 'Subject MAT not found or inactive';
    END IF;
    
    RAISE NOTICE 'Using subject: MAT (id: %)', v_subject_id;
    
    -- =============================================
    -- SECTION 2: Insert Topics (5 topics)
    -- =============================================
    
    RAISE NOTICE '=== SECTION 2: Inserting Topics ===';
    
    -- Topic 1: Trigonometri
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
        'MAT-TRIG-01',
        'Trigonometri (Temel)',
        v_curriculum_version_id,
        true,
        7,
        '10,11,tyt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_trig;
    
    IF v_topic_trig IS NULL THEN
        SELECT id INTO v_topic_trig FROM topics WHERE code = 'MAT-TRIG-01';
    END IF;
    RAISE NOTICE 'Topic 1: MAT-TRIG-01 (id: %)', v_topic_trig;
    
    -- Topic 2: Logaritma
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
        'MAT-LOGA-01',
        'Logaritma',
        v_curriculum_version_id,
        true,
        6,
        '10,11,tyt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_loga;
    
    IF v_topic_loga IS NULL THEN
        SELECT id INTO v_topic_loga FROM topics WHERE code = 'MAT-LOGA-01';
    END IF;
    RAISE NOTICE 'Topic 2: MAT-LOGA-01 (id: %)', v_topic_loga;
    
    -- Topic 3: Diziler
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
        'MAT-DIZI-01',
        'Diziler',
        v_curriculum_version_id,
        true,
        7,
        '11,tyt,ayt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_dizi;
    
    IF v_topic_dizi IS NULL THEN
        SELECT id INTO v_topic_dizi FROM topics WHERE code = 'MAT-DIZI-01';
    END IF;
    RAISE NOTICE 'Topic 3: MAT-DIZI-01 (id: %)', v_topic_dizi;
    
    -- Topic 4: Limit
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
        'MAT-LIMIT-01',
        'Limit',
        v_curriculum_version_id,
        true,
        6,
        '11,12,ayt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_limit;
    
    IF v_topic_limit IS NULL THEN
        SELECT id INTO v_topic_limit FROM topics WHERE code = 'MAT-LIMIT-01';
    END IF;
    RAISE NOTICE 'Topic 4: MAT-LIMIT-01 (id: %)', v_topic_limit;
    
    -- Topic 5: Türev
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
        'MAT-TUREV-01',
        'Türev',
        v_curriculum_version_id,
        true,
        8,
        '12,ayt'
    )
    ON CONFLICT (code) DO NOTHING
    RETURNING id INTO v_topic_turev;
    
    IF v_topic_turev IS NULL THEN
        SELECT id INTO v_topic_turev FROM topics WHERE code = 'MAT-TUREV-01';
    END IF;
    RAISE NOTICE 'Topic 5: MAT-TUREV-01 (id: %)', v_topic_turev;
    
    -- =============================================
    -- SECTION 3: Insert topic_contexts (5 contexts)
    -- =============================================
    
    RAISE NOTICE '=== SECTION 3: Inserting Topic Contexts ===';
    
    -- Context 1: Trigonometri (SYNTHESIS)
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_trig,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Açı ölçülerini (derece-radyan) dönüştürebilme',
                'Trigonometrik oranları (sin, cos, tan) kullanabilme',
                'Birim çember üzerinde değer okuyabilme',
                'Özel açıların değerlerini bilme',
                'Temel trigonometrik özdeşlikleri uygulayabilme'
            ),
            'prerequisites', jsonb_build_array(
                'MAT-USLU-01',  -- Üslü ve Köklü Sayılar (zorunlu)
                'MAT-FONK-01'   -- Fonksiyonlar (önerilen)
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('10', '11', 'tyt'),
                'exam_scope', 'school',
                'frequency', 'Yüksek'
            ),
            'cognitive_level', 'application',
            'splitting_guidance', jsonb_build_object(
                'recommended', true,
                'reason', 'Ezber (özel açılar) ve mantık (özdeşlikler) ayrımı kritik',
                'suggested_splits', jsonb_build_array(
                    'Birim çember ve özel açılar (High ROI)',
                    'Trigonometrik oranlar',
                    'Temel özdeşlikler'
                ),
                'roi_notes', jsonb_build_object(
                    'high_roi', jsonb_build_array('Birim çember', 'Özel açılar'),
                    'medium_roi', jsonb_build_array('Özdeşlik dönüşümleri')
                )
            ),
            'measurement_notes', jsonb_build_object(
                '20min_suitable', false,
                'suitable_for', 'Özel açılar',
                'challenging_for', 'Özdeşlik dönüşümleri'
            ),
            'tags', jsonb_build_array('trigonometry', 'unit_circle', 'functions', 'synthesis'),
            'archetype', 'synthesis',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 1: Trigonometri (synthesis)';
    
    -- Context 2: Logaritma (FOUNDATIONAL)
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_loga,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Logaritma tanımını anlayabilme',
                'Logaritma kurallarını uygulayabilme',
                'Üstel-logaritmik dönüşüm yapabilme',
                'Basit logaritmik denklemleri çözebilme'
            ),
            'prerequisites', jsonb_build_array(
                'MAT-USLU-01',  -- Üslü Sayılar (zorunlu)
                'MAT-DENK-01'   -- Denklemler (önerilen)
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('10', '11', 'tyt'),
                'exam_scope', 'school',
                'frequency', 'Orta'
            ),
            'cognitive_level', 'comprehension',
            'splitting_guidance', jsonb_build_object(
                'recommended', false,
                'reason', 'Hata tipleri net, gelişim çizgisi açık, unified topic'
            ),
            'measurement_notes', jsonb_build_object(
                '20min_suitable', true,
                'suitable_for', 'Tüm alt konular',
                'group_study_effective', true
            ),
            'tags', jsonb_build_array('logarithms', 'exponents', 'algebra', 'foundational'),
            'archetype', 'foundational',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 2: Logaritma (foundational)';
    
    -- Context 3: Diziler (SYNTHESIS)
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_dizi,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Dizi kavramını anlayabilme',
                'Aritmetik dizi genel terimi bulabilme',
                'Geometrik dizi genel terimi bulabilme',
                'Dizi toplamı formüllerini kullanabilme'
            ),
            'prerequisites', jsonb_build_array(
                'MAT-DENK-01',  -- Denklemler (zorunlu)
                'MAT-FONK-01'   -- Fonksiyonlar (önerilen)
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('11', 'tyt', 'ayt'),
                'exam_scope', 'school',
                'frequency', 'Yüksek'
            ),
            'cognitive_level', 'application',
            'splitting_guidance', jsonb_build_object(
                'recommended', true,
                'reason', 'Formül bilgisi + problem çözme karışımı, alt tür bazlı çalışma gerekli',
                'suggested_splits', jsonb_build_array(
                    'Aritmetik diziler (High ROI)',
                    'Geometrik diziler (Medium ROI)'
                ),
                'roi_notes', jsonb_build_object(
                    'high_roi', jsonb_build_array('Aritmetik dizi'),
                    'medium_roi', jsonb_build_array('Geometrik dizi')
                )
            ),
            'measurement_notes', jsonb_build_object(
                '20min_suitable', false,
                'reason', 'Alt tür bazlı çalışma gerekli'
            ),
            'tags', jsonb_build_array('sequences', 'series', 'algebra', 'synthesis'),
            'archetype', 'synthesis',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 3: Diziler (synthesis)';
    
    -- Context 4: Limit (FOUNDATIONAL)
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_limit,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Limit kavramını anlayabilme',
                'Sağ-sol limit hesaplayabilme',
                'Süreklilik kavramına giriş yapabilme',
                'Basit limit hesapları yapabilme'
            ),
            'prerequisites', jsonb_build_array(
                'MAT-FONK-01',  -- Fonksiyonlar (zorunlu)
                'MAT-POLI-01'   -- Polinomlar (önerilen)
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('11', '12', 'ayt'),
                'exam_scope', 'school',
                'frequency', 'Çok Yüksek'
            ),
            'cognitive_level', 'comprehension',
            'splitting_guidance', jsonb_build_object(
                'recommended', false,
                'reason', 'Gelişim ölçülebilir, konu sınırı uygun, unified topic'
            ),
            'measurement_notes', jsonb_build_object(
                '20min_suitable', true,
                'suitable_for', 'Tüm alt konular',
                'group_study_effective', true
            ),
            'tags', jsonb_build_array('limits', 'functions', 'calculus', 'foundational'),
            'archetype', 'foundational',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 4: Limit (foundational)';
    
    -- Context 5: Türev (SYNTHESIS)
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (
        v_topic_turev,
        jsonb_build_object(
            'learning_objectives', jsonb_build_array(
                'Türev tanımını anlayabilme',
                'Temel türev kurallarını uygulayabilme',
                'Grafik yorumu yapabilme',
                'Artan-azalan analizi yapabilme'
            ),
            'prerequisites', jsonb_build_array(
                'MAT-LIMIT-01',  -- Limit (zorunlu)
                'MAT-FONK-01'    -- Fonksiyonlar (önerilen)
            ),
            'exam_context', jsonb_build_object(
                'grade_levels', jsonb_build_array('12', 'ayt'),
                'exam_scope', 'school',
                'frequency', 'Çok Yüksek'
            ),
            'cognitive_level', 'analysis',
            'splitting_guidance', jsonb_build_object(
                'recommended', true,
                'reason', 'Konu sınırı geniş, hata tipi ayrımı kritik',
                'suggested_splits', jsonb_build_array(
                    'Grafik yorumu (High ROI)',
                    'Temel türev kuralları (Medium ROI)',
                    'Artan-azalan analizi'
                ),
                'roi_notes', jsonb_build_object(
                    'high_roi', jsonb_build_array('Grafik yorumu'),
                    'medium_roi', jsonb_build_array('Kural ezberi')
                )
            ),
            'measurement_notes', jsonb_build_object(
                '20min_suitable', false,
                'reason', 'Alt konu odaklı çalışma gerekli'
            ),
            'tags', jsonb_build_array('derivatives', 'calculus', 'functions', 'synthesis'),
            'archetype', 'synthesis',
            'format_version', '1.0'
        )
    )
    ON CONFLICT (topic_id) DO NOTHING;
    RAISE NOTICE 'Context 5: Türev (synthesis)';
    
    -- =============================================
    -- SUCCESS MESSAGE
    -- =============================================
    
    RAISE NOTICE '=== ✅ Migration 007 Completed Successfully ===';
    RAISE NOTICE 'Inserted 5 mathematics topics with Context Layer metadata';
    RAISE NOTICE 'Topics: Trigonometri, Logaritma, Diziler, Limit, Türev';
    RAISE NOTICE 'Format Version: 1.0';
    RAISE NOTICE 'Archetypes: 2 foundational, 3 synthesis';
    RAISE NOTICE 'Prerequisite chain: Limit → Türev';

END $$;