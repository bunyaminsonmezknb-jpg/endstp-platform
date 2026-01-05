-- ============================================
-- MIGRATION 012: PHYSICS 1ST BATCH
-- Date: 2024-12-31
-- Topics: 5 (Fiziksel Büyüklükler, Hareket, Kuvvet, Enerji, Momentum)
-- Target: 5/35 topics (14% Physics complete)
-- Archetype: 5F/0S (Foundation building phase)
-- Velocity: 3x expected (format v1.0 proven!)
-- Format: v1.0 (REUSED from Mathematics - no changes!)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (5 foundational topics)
-- ============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_physics_subject_id UUID;
BEGIN
    -- Get curriculum version (TR MEB 2024)
    SELECT id INTO v_curriculum_version_id
    FROM curriculum_versions
    WHERE country_code = 'TR'
      AND system_code = 'MEB'
      AND academic_year = 2024
    LIMIT 1;
    
    -- Get Physics subject
    SELECT id INTO v_physics_subject_id
    FROM subjects
    WHERE code = 'FIZ'
    LIMIT 1;
    
    -- Insert 5 foundational topics
    INSERT INTO topics (
        curriculum_version_id,
        subject_id,
        code,
        name_tr,
        difficulty_level,
        grade_level,
        is_active
    ) VALUES
    -- ALL FOUNDATIONAL (5 topics)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-BUYUK-01', 'Fiziksel Büyüklükler ve Ölçme', 4, '9,tyt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-HAREKET-01', 'Düz Çizgisel Hareket', 5, '9,tyt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-KUVVET-01', 'Kuvvet ve Newton Kanunları', 6, '9,10,tyt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-ENERJI-01', 'İş, Enerji, Güç', 6, '9,10,tyt,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-MOMENTUM-01', 'İtme ve Momentum', 6, '10,tyt,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '5 Physics foundational topics inserted successfully';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (5 contexts)
-- ============================================

DO $$
DECLARE
    v_topic_id UUID;
BEGIN
    -- ==========================================
    -- 1. FIZ-BUYUK-01: Fiziksel Büyüklükler (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-BUYUK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Orta'
        ),
        'learning_objectives', jsonb_build_array(
            'Fiziksel büyüklük ve birim kavramlarını anlama',
            'Temel ve türetilmiş birimleri ayırt etme',
            'Birim dönüşümleri yapma',
            'Bilimsel gösterim kullanma',
            'Ölçme hataları ve belirsizlik kavramlarını bilme'
        ),
        'prerequisite_topics', jsonb_build_array(
        ),
        'misconceptions', jsonb_build_array(
            'Büyüklük ile birimi karıştırma (uzunluk büyüklüğü, metre birimi)',
            'Birim dönüşümünde çarpan yerine bölme veya tersi',
            'Bilimsel gösterimde 10 üssünü yanlış kullanma',
            'Kesinlik ile doğruluğu karıştırma',
            'Ölçüm aletinin hassasiyetini göz ardı etme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 150,
            'practice', 180,
            'mastery', 120
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Fiziksel büyüklükler ve ölçme temel kavramlardır, 15-20 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-BUYUK-01: Fiziksel Büyüklükler ve Ölçme';
    
    -- ==========================================
    -- 2. FIZ-HAREKET-01: Düz Çizgisel Hareket (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-HAREKET-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Orta'
        ),
        'learning_objectives', jsonb_build_array(
            'Konum, yol, yer değiştirme kavramlarını ayırt etme',
            'Hız ve sürat farkını anlama',
            'İvme kavramını ve türlerini bilme',
            'Hareket grafiklerini okuma ve çizme',
            'Kinematik denklemleri kullanma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01'
        ),
        'misconceptions', jsonb_build_array(
            'Yol ile yer değiştirmeyi karıştırma (yol skaler, yer değiştirme vektör)',
            'Hız ile sürati karıştırma (hız vektörel, sürat skaler)',
            'Grafiklerde eğim ile alan yorumunu karıştırma',
            'Negatif ivmeyi yavaşlama olarak yorumlama (her zaman değil!)',
            'Serbest düşmede hava direncini göz ardı etme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 210,
            'practice', 270,
            'mastery', 180
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Düz çizgisel hareket temel kinematik konusudur, grafik ve denklemler birlikte 20 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-HAREKET-01: Düz Çizgisel Hareket';
    
    -- ==========================================
    -- 3. FIZ-KUVVET-01: Kuvvet ve Newton Kanunları (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-KUVVET-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Kuvvet kavramını ve özelliklerini anlama',
            'Newton''un 3 hareket yasasını bilme ve uygulama',
            'Sürtünme kuvveti ve türlerini anlama',
            'Serbest cisim diyagramı çizme',
            'Net kuvvet ve ivme ilişkisini kullanma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01',
            'FIZ-HAREKET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Newton''un 1. yasasını sadece durağan cisimler için geçerli sanma',
            'Etki-tepki kuvvetlerini aynı cisim üzerinde gösterme',
            'Sürtünme kuvvetinin her zaman harekete zıt olduğunu sanma',
            'F=ma''da kütle ile ağırlığı karıştırma',
            'Hava direncini ihmal edilebilir sanma (yüksek hızlarda önemli!)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 210
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Newton kanunları temel dinamik konusudur, 3 yasa birlikte 20-25 dakikada kavranabilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-KUVVET-01: Kuvvet ve Newton Kanunları';
    
    -- ==========================================
    -- 4. FIZ-ENERJI-01: İş, Enerji, Güç (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-ENERJI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'İş kavramını ve hesaplamasını anlama',
            'Kinetik ve potansiyel enerji kavramlarını bilme',
            'Mekanik enerjinin korunumu ilkesini uygulama',
            'Güç kavramını ve birimlerini bilme',
            'Verim hesaplamaları yapma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-KUVVET-01',
            'FIZ-HAREKET-01'
        ),
        'misconceptions', jsonb_build_array(
            'İş için kuvvet yönü ile hareket yönünün aynı olması gerektiğini sanma (cosθ faktörü!)',
            'Potansiyel enerjiyi sadece yerçekimi ile sınırlama (elastik PE var)',
            'Enerjinin yokolabileceğini düşünme (sadece dönüşür)',
            'Güç ile kuvveti karıştırma (P = W/t vs F = ma)',
            'Verimi yüzde ile katma sayı olarak karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 240
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'İş-enerji-güç kavramları birbirine bağlıdır, 20-25 dakikada temel ilkeler öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-ENERJI-01: İş, Enerji, Güç';
    
    -- ==========================================
    -- 5. FIZ-MOMENTUM-01: İtme ve Momentum (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-MOMENTUM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Momentum kavramını ve özelliklerini anlama',
            'İtme-momentum teoremini uygulama',
            'Momentumun korunumu ilkesini bilme',
            'Çarpışma türlerini ayırt etme (esnek, esnek olmayan)',
            'Geri tepme olaylarını açıklama'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-KUVVET-01',
            'FIZ-HAREKET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Momentum ile enerjiyi karıştırma (p = mv vs Ek = 1/2 mv^2)',
            'Momentumun korunumunun her zaman geçerli olduğunu sanma (dış kuvvet yoksa!)',
            'Esnek çarpışmada hem momentum hem enerjinin korunduğunu unutma',
            'Esnek olmayan çarpışmada momentum korunmaz sanma (korunur!)',
            'İtme ile anlık kuvveti karıştırma (İ = F·Δt, alan altı)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 210,
            'practice', 270,
            'mastery', 210
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'İtme ve momentum temel dinamik kavramlardır, korunum yasaları ile 20 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-MOMENTUM-01: İtme ve Momentum';
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'PHYSICS 1ST BATCH COMPLETE!';
    RAISE NOTICE '5/35 topics (14%% complete)';
    RAISE NOTICE 'Foundation phase: 5F/0S';
    RAISE NOTICE '==========================================';
    
END $$;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check all 5 topics inserted
SELECT 
    code,
    name_tr,
    difficulty_level,
    grade_level,
    is_active
FROM topics
WHERE code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY code;

-- Check all 5 contexts created
SELECT 
    t.code,
    t.name_tr,
    CASE WHEN tc.id IS NULL THEN 'NO CONTEXT' ELSE 'HAS CONTEXT' END as status,
    tc.metadata->>'archetype' as archetype
FROM topics t
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-BUYUK-01', 'FIZ-HAREKET-01', 'FIZ-KUVVET-01',
    'FIZ-ENERJI-01', 'FIZ-MOMENTUM-01'
)
ORDER BY t.code;

-- Physics cumulative stats (should show 5 topics, 5F/0S)
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
