-- ============================================
-- MIGRATION 018: CHEMISTRY 1ST BATCH
-- Date: 2024-12-31
-- Topics: 6 (Atom, Bağlar, Madde, Mol, Tepkime, Karışım)
-- Target: 6/30 topics (20%% Chemistry kickoff!)
-- Archetype: 5F/1S (83%%/17%% - Foundation phase)
-- Velocity: 3.7x+ expected (Format v1.0 proven!)
-- Format: v1.0 (REUSED from Math/Physics - bulletproof!)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (5F + 1S)
-- ============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_chemistry_subject_id UUID;
BEGIN
    SELECT id INTO v_curriculum_version_id
    FROM curriculum_versions
    WHERE country_code = 'TR' AND system_code = 'MEB' AND academic_year = 2024
    LIMIT 1;
    
    SELECT id INTO v_chemistry_subject_id
    FROM subjects WHERE code = 'KIM' LIMIT 1;
    
    INSERT INTO topics (
        curriculum_version_id, subject_id, code, name_tr,
        difficulty_level, grade_level, is_active
    ) VALUES
    -- FOUNDATIONAL (5)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ATOM-01', 'Atom Yapısı ve Periyodik Sistem', 5, '9,tyt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-BAG-01', 'Kimyasal Bağlar', 5, '9,10,tyt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-MADDE-01', 'Maddenin Halleri', 4, '9,tyt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-MOL-01', 'Mol Kavramı ve Hesaplamalar', 6, '9,10,tyt,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-TEPKIME-01', 'Kimyasal Tepkimeler ve Denklemler', 5, '9,10,tyt', true),
    
    -- SYNTHESIS (1)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-KARISIM-01', 'Karışımlar ve Ayırma Yöntemleri', 6, '9,tyt,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '6 Chemistry topics (5F + 1S) inserted - KICKOFF!';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (6 contexts)
-- ============================================

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- ==========================================
    -- FOUNDATIONAL TOPICS (5)
    -- ==========================================
    
    -- 1. KIM-ATOM-01: Atom Yapısı (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ATOM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Atom modelleri (Dalton, Thomson, Rutherford, Bohr)',
            'Atom numarası, kütle numarası, izotoplar',
            'Periyodik tablonun yapısı (grup, periyot)',
            'Elektronların enerji seviyeleri ve dağılımı',
            'Periyodik özellikler (atom yarıçapı, iyonlaşma enerjisi)'
        ),
        'prerequisite_topics', jsonb_build_array(),
        'misconceptions', jsonb_build_array(
            'Atomun en küçük parçacık olduğunu sanma (proton, nötron, elektron var)',
            'Periyodik tabloda sütunları periyot sanma (grup doğru)',
            'İzotopların kimyasal özelliklerinin farklı olduğunu sanma (aynı)',
            'Elektronların rastgele dağıldığını sanma (enerji seviyelerine göre)',
            'Atom yarıçapının periyotta sağa gidildikçe arttığını sanma (azalır)'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 180),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Atom yapısı ve periyodik sistem temelleri 20-25 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 2. KIM-BAG-01: Kimyasal Bağlar (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-BAG-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'İyonik bağ oluşumu ve özellikleri',
            'Kovalent bağ ve elektron paylaşımı',
            'Metalik bağ ve özellikleri',
            'Polar ve apolar moleküller',
            'Lewis nokta yapıları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-ATOM-01'),
        'misconceptions', jsonb_build_array(
            'İyonik bağı elektron paylaşımı sanma (elektron alışverişi)',
            'Kovalent bağda elektronların kaybolduğunu sanma (paylaşılır)',
            'Tüm kovalent bağların polar olduğunu sanma (apolar da var)',
            'Metalik bağı sadece elektron denizi olarak görme (örgü yapısı da önemli)',
            'Lewis yapısında okteti her zaman doldurma zorunluluğu (istisnalar var)'
        ),
        'time_estimate', jsonb_build_object('foundation', 210, 'practice', 270, 'mastery', 180),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Kimyasal bağlar temelleri 20 dakikada kavranabilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 3. KIM-MADDE-01: Maddenin Halleri (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-MADDE-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Yüksek', 'ayt', 'Orta'),
        'learning_objectives', jsonb_build_array(
            'Katı, sıvı, gaz hallerinin özellikleri',
            'Hal değişimleri ve enerji',
            'Moleküller arası kuvvetler (Van der Waals, hidrojen bağı)',
            'Faz diyagramları',
            'Buharlaşma, kaynama, donma, süblimleşme'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-BAG-01'),
        'misconceptions', jsonb_build_array(
            'Hal değişiminde sıcaklığın sürekli değiştiğini sanma (sabit kalır)',
            'Buharlaşma ile kaynama''yı karıştırma (farklı sıcaklıklar)',
            'Hidrojen bağının kimyasal bağ olduğunu sanma (moleküller arası)',
            'Gazların hacminin sıfır olduğunu sanma (çok büyük)',
            'Süblimleşmenin sadece soğuk koşullarda olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 180, 'practice', 240, 'mastery', 150),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Maddenin halleri temelleri 15-20 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 4. KIM-MOL-01: Mol Kavramı (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-MOL-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Mol kavramı ve Avogadro sayısı',
            'Molekül kütlesi ve mol kütlesi',
            'Mol-kütle-hacim dönüşümleri',
            'Molekül formülü ve ampirik formül',
            'Bileşiklerde kütle oranları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-ATOM-01'),
        'misconceptions', jsonb_build_array(
            'Mol''ü kütle birimi sanma (madde miktarı birimi)',
            'Avogadro sayısını sadece moleküller için geçerli sanma (her parçacık)',
            'Ampirik formülü molekül formülü sanma (en basit oran)',
            'Mol kütlesinin elementin kütlesi olduğunu sanma (1 mol''ün kütlesi)',
            'Gazların mol hacmini her koşulda 22.4L sanma (STP''de geçerli)'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 360, 'mastery', 240),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Mol kavramı temel hesaplamalarla 25-30 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 5. KIM-TEPKIME-01: Kimyasal Tepkimeler (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-TEPKIME-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Kimyasal denklem yazma ve denkleştirme',
            'Tepkime türleri (birleşme, ayrışma, yer değiştirme)',
            'Reaktif ve ürün kavramları',
            'Kütlenin korunumu yasası',
            'Basit tepkime hesaplamaları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-MOL-01'),
        'misconceptions', jsonb_build_array(
            'Tepkimede kütlenin değiştiğini sanma (korunur)',
            'Denkleştirilmemiş denklemi kabul etme',
            'İndisleri değiştirerek denkleştirmeye çalışma (katsayılar)',
            'Her tepkimenin geri dönüşümlü olduğunu sanma (tek yönlü de var)',
            'Ürünlerin toplamının reaktiflerden fazla olabileceğini sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 210),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Kimyasal tepkimeler temelleri ve denkleştirme 20-25 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- ==========================================
    -- SYNTHESIS TOPIC (1)
    -- ==========================================
    
    -- 6. KIM-KARISIM-01: Karışımlar (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-KARISIM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Yüksek', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Homojen ve heterojen karışımlar',
            'Ayırma yöntemleri (filtrasyon, distilasyon, kristalizasyon)',
            'Çözelti, süspansiyon, koloit ayrımı',
            'Kromatografi teknikleri',
            'Laboratuvar uygulamaları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-MADDE-01'),
        'misconceptions', jsonb_build_array(
            'Homojen karışımın sadece sıvı olduğunu sanma (alaşımlar katı)',
            'Filtrasyon ile damıtmayı karıştırma (farklı prensipler)',
            'Koloidin çözelti olduğunu sanma (daha büyük parçacıklar)',
            'Kromatografiyi sadece renkliler için sanma (renksiz de)',
            'Ayırma yöntemlerinin kimyasal değişim yaptığını sanma (fiziksel)'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 330, 'mastery', 240),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'Karışımlar 4 kategoriye ayrılmalı: Karışım Türleri, Fiziksel Ayırma, Kromatografi, Laboratuvar Uygulamaları'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Homojen-heterojen ayrımı (TYT klasik)', 'Basit ayırma yöntemleri (mutlaka)', 'Filtrasyon-damıtma (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık kromatografi', 'Çok aşamalı ayırma prosesleri')
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'CHEMISTRY 1ST BATCH COMPLETE!';
    RAISE NOTICE '6/30 topics (20%%%% - Foundation phase!)';
    RAISE NOTICE 'Balance: 5F/1S (83%%%%/17%%%%)';
    RAISE NOTICE 'Format v1.0 REUSED - 3.7x velocity expected!';
    RAISE NOTICE '==========================================';
    
END $$;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check all 6 topics inserted
SELECT 
    code, name_tr, difficulty_level, grade_level, is_active
FROM topics
WHERE code IN (
    'KIM-ATOM-01', 'KIM-BAG-01', 'KIM-MADDE-01',
    'KIM-MOL-01', 'KIM-TEPKIME-01', 'KIM-KARISIM-01'
)
ORDER BY code;

-- Check contexts and archetypes
SELECT 
    t.code,
    t.name_tr,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->'splitting'->>'recommended' as needs_splitting
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'KIM-ATOM-01', 'KIM-BAG-01', 'KIM-MADDE-01',
    'KIM-MOL-01', 'KIM-TEPKIME-01', 'KIM-KARISIM-01'
)
ORDER BY archetype, t.code;

-- Chemistry cumulative (should show 6 topics, 5F/1S)
SELECT 
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT tc.id) as with_context,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END) as foundational,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'synthesis' THEN 1 ELSE 0 END) as synthesis,
    ROUND(100.0 * SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END)::numeric / 
          NULLIF(COUNT(DISTINCT tc.id), 0), 1) || '%%' as foundational_pct,
    ROUND(100.0 * COUNT(DISTINCT tc.id) / 30.0, 1) || '%%' as completion_vs_target
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'KIM';
-- Expected: 6 topics, 5F, 1S, 83%% foundational, 20%% completion
