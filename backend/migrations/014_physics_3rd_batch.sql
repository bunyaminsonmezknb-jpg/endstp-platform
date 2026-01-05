-- ============================================
-- MIGRATION 014: PHYSICS 3RD BATCH
-- Date: 2024-12-31
-- Topics: 7 (Isı, Optik, Dalga, Atom + 3 Synthesis)
-- Target: 18/35 topics (51% Physics complete - MILESTONE!)
-- Archetype: 4F/3S → Total 12F/6S (67%/33%)
-- Velocity: 3x sustained (MOMENTUM MODE!)
-- Format: v1.0 (REUSED - proven stable!)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (4F + 3S)
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
    
    -- Insert 7 topics (4F + 3S)
    INSERT INTO topics (
        curriculum_version_id,
        subject_id,
        code,
        name_tr,
        difficulty_level,
        grade_level,
        is_active
    ) VALUES
    -- FOUNDATIONAL (4 topics)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-ISI-01', 'Isı ve Sıcaklık', 5, '9,tyt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-OPTIK-01', 'Işık ve Optik', 6, '10,tyt,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-DALGA-01', 'Dalgalar', 6, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-ATOM-01', 'Atom Fiziği ve Radyoaktivite', 7, '12,ayt', true),
    
    -- SYNTHESIS (3 topics)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-ELEKTRIK-ILERI-01', 'İleri Elektrik Devreleri', 8, '11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-OPTIK-ILERI-01', 'İleri Optik Problemleri', 8, '11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-TERMAL-ILERI-01', 'İleri Termodinamik', 8, '11,12,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '7 Physics topics (4F + 3S) inserted - 51%% MILESTONE!';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (7 contexts)
-- ============================================

DO $$
DECLARE
    v_topic_id UUID;
BEGIN
    -- ==========================================
    -- FOUNDATIONAL TOPICS (4)
    -- ==========================================
    
    -- 1. FIZ-ISI-01: Isı ve Sıcaklık (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-ISI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Orta'
        ),
        'learning_objectives', jsonb_build_array(
            'Sıcaklık ve ısı kavramlarını ayırt etme',
            'Sıcaklık ölçekleri arası dönüşüm (Celsius, Kelvin, Fahrenheit)',
            'Isı alışverişi ve kalorimetri hesaplamaları',
            'Hal değişimi ve öz ısı kavramları',
            'Isı geçişi yöntemleri (iletim, taşınım, ışınım)'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01',
            'FIZ-ENERJI-01'
        ),
        'misconceptions', jsonb_build_array(
            'Sıcaklık ile ısıyı karıştırma (sıcaklık ölçü, ısı enerji)',
            'Öz ısı ile ısı kapasitesini karıştırma',
            'Hal değişiminde sıcaklığın değiştiğini sanma (sabit kalır!)',
            'Isı geçişinde sadece iletimi düşünme (3 yöntem var)',
            'Negatif sıcaklıkta ısı olmadığını sanma (mutlak sıfır dışında var)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 180,
            'practice', 240,
            'mastery', 150
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Isı ve sıcaklık temel termodinamik kavramlardır, 15-20 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-ISI-01';
    
    -- 2. FIZ-OPTIK-01: Işık ve Optik (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-OPTIK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Işık özelliklerini anlama (dalga-parçacık ikiliği)',
            'Yansıma ve kırılma yasalarını uygulama',
            'Düz aynada görüntü oluşumu',
            'Mercek denklemini kullanma',
            'Işık hızı ve kırılma indisi kavramları'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01',
            'FIZ-DALGA-01'
        ),
        'misconceptions', jsonb_build_array(
            'Yansıma açısı ile gelme açısını farklı sanma (eşittir)',
            'Kırılmada her zaman ışının kırıldığını sanma (tam yansıma var)',
            'Merceklerde odak uzaklığı ile görüntü uzaklığını karıştırma',
            'Sanal görüntünün gerçek olmadığını sanma (görülebilir ama perdede değil)',
            'Işık hızının her ortamda aynı olduğunu sanma (ortama bağlı)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 210
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Geometrik optik temelleri, ayna ve mercek ile 20-25 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-OPTIK-01';
    
    -- 3. FIZ-DALGA-01: Dalgalar (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-DALGA-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Dalga kavramı ve türlerini anlama (enine, boyuna)',
            'Dalga parametreleri (frekans, dalga boyu, hız)',
            'Ses dalgaları ve özellikleri',
            'Doppler olayını açıklama',
            'Elektromanyetik spektrum'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01',
            'FIZ-HAREKET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Frekans ile dalga boyunu karıştırma (ters orantılı)',
            'Ses dalgasının boşlukta yayıldığını sanma (ortam gerekir)',
            'Doppler olayında sadece kaynak hareketini düşünme (gözlemci de)',
            'Elektromanyetik dalgaların ortam gerektirdiğini sanma (boşlukta da yayılır)',
            'Dalga hızının frekanstan bağımsız olduğunu unutma (v = f×λ)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 240
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Dalga kavramları ve türleri, Doppler ile 20-25 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-DALGA-01';
    
    -- 4. FIZ-ATOM-01: Atom Fiziği ve Radyoaktivite (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-ATOM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Atom modelleri ve tarihi gelişim',
            'Çekirdek yapısı (proton, nötron, elektron)',
            'Radyoaktif bozunma türleri (alfa, beta, gama)',
            'Yarı ömür kavramı ve hesaplamaları',
            'Nükleer reaksiyonlar ve enerji'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01'
        ),
        'misconceptions', jsonb_build_array(
            'Elektronun çekirdeğin etrafında yörünge izlediğini sanma (kuantum bulut)',
            'Radyoaktivite ile radyasyonu karıştırma',
            'Yarı ömürde tüm atomların aynı anda bozunduğunu sanma (istatistiksel)',
            'Nükleer füzyon ile fisyonu karıştırma (füzyon birleşme, fisyon parçalanma)',
            'Kütle numarası ile atom numarasını karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 210,
            'practice', 270,
            'mastery', 180
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Modern fizik temelleri, atom ve radyoaktivite 20 dakikada kavranabilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-ATOM-01';
    
    -- ==========================================
    -- SYNTHESIS TOPICS (3)
    -- ==========================================
    
    -- 5. FIZ-ELEKTRIK-ILERI-01: İleri Elektrik Devreleri (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-ELEKTRIK-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Kirchhoff yasalarını uygulama',
            'RC devrelerinde yük-deşarj analizi',
            'Kapasitör ve kapasitans hesaplamaları',
            'Kompleks devre problemleri',
            'Galvanometre ve köprü devreleri'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-ELEKTRIK-01'
        ),
        'misconceptions', jsonb_build_array(
            'Kirchhoff akım yasasında işaret yönünü yanlış belirleme',
            'RC devresinde kararlı durum zamanını yanlış hesaplama (5τ)',
            'Paralel kapasitörlerde toplam kapasitansı seri gibi hesaplama',
            'Köprü dengesinde sadece direnç oranını kontrol etme (gerilim de)',
            'Galvanometrenin direncini ihmal etme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 480,
            'mastery', 420
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'İleri elektrik devreleri 4 kategoriye ayrılmalı: Kirchhoff Yasaları, RC Devreleri, Kapasitör Sistemleri, Kompleks Devreler'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Kirchhoff yasaları (AYT mutlaka çıkar)',
                'RC devre yük-deşarj (klasik)',
                'Seri-paralel kapasitör (sık)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Wheatstone köprüsü (nadir)',
                'Çok karmaşık mesh analizi (zaman alıcı)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-ELEKTRIK-ILERI-01';
    
    -- 6. FIZ-OPTIK-ILERI-01: İleri Optik Problemleri (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-OPTIK-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Küresel aynalarda görüntü problemleri',
            'İnce ve kalın mercek sistemleri',
            'Prizma ve dispersiyon',
            'Girişim ve kırınım olayları',
            'Optik alet tasarımı (mikroskop, teleskop)'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-OPTIK-01',
            'FIZ-DALGA-01'
        ),
        'misconceptions', jsonb_build_array(
            'Ayna denkleminde işaret kurallarını yanlış uygulama',
            'Toplam büyütmede m1 × m2 yerine m1 + m2 yapma',
            'Prizmada sapma açısının dalga boyundan bağımsız olduğunu sanma',
            'Girişimde yıkıcı için yol farkını λ/2 yerine λ sanma',
            'Kırınımda tek yarık ile çift yarığı karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 450,
            'mastery', 390
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'İleri optik 4 kategoriye ayrılmalı: Küresel Aynalar-Mercekler, Mercek Sistemleri, Prizma-Dispersiyon, Girişim-Kırınım'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Küresel ayna problemleri (AYT klasik)',
                'İnce mercek denklemi (mutlaka)',
                'Prizma sapma açısı (sık)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Kalın mercek (nadir)',
                'Karmaşık girişim desenleri (ileri seviye)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-OPTIK-ILERI-01';
    
    -- 7. FIZ-TERMAL-ILERI-01: İleri Termodinamik (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-TERMAL-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'İdeal gaz yasası ve uygulamaları (PV=nRT)',
            'Termodinamik süreçler (izobarik, izokorik, izotermal, adyabatik)',
            'İç enerji ve birinci yasa',
            'Entropi ve ikinci yasa',
            'Isı makineleri ve verim'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-ISI-01',
            'FIZ-ENERJI-01'
        ),
        'misconceptions', jsonb_build_array(
            'İdeal gaz yasasında birim uyumsuzluğu (P atm, V L, n mol, T K)',
            'İzotermal süreçte iç enerji değişimini sıfırdan farklı sanma (ΔU=0)',
            'Adyabatik süreçte ısı alışverişi olduğunu sanma (Q=0)',
            'Entropi ile düzensizliği karıştırma (entropi enerji dağılımı)',
            'Carnot veriminin %100 olabileceğini sanma (imkansız)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 330,
            'practice', 420,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'İleri termodinamik 4 kategoriye ayrılmalı: İdeal Gaz Yasaları, Termodinamik Süreçler, İç Enerji ve Entropi, Isı Makineleri'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'İdeal gaz yasası (AYT mutlaka)',
                'Termodinamik süreçler (sık)',
                'Birinci yasa uygulamaları (klasik)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'İkinci yasa entropi detayları (nadir)',
                'Carnot çevrimi hesaplamaları (ileri)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-TERMAL-ILERI-01';
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'PHYSICS 3RD BATCH COMPLETE!';
    RAISE NOTICE '18/35 topics (51%% - HALFWAY MILESTONE!)';
    RAISE NOTICE 'Balance: 12F/6S (67%%/33%%)';
    RAISE NOTICE '3x velocity sustained!';
    RAISE NOTICE '==========================================';
    
END $$;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check all 7 topics inserted
SELECT 
    code,
    name_tr,
    difficulty_level,
    is_active
FROM topics
WHERE code IN (
    'FIZ-ISI-01', 'FIZ-OPTIK-01', 'FIZ-DALGA-01', 'FIZ-ATOM-01',
    'FIZ-ELEKTRIK-ILERI-01', 'FIZ-OPTIK-ILERI-01', 'FIZ-TERMAL-ILERI-01'
)
ORDER BY code;

-- Check contexts and archetypes
SELECT 
    t.code,
    tc.metadata->>'archetype' as archetype,
    tc.metadata->'splitting'->>'recommended' as needs_splitting
FROM topics t
JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'FIZ-ISI-01', 'FIZ-OPTIK-01', 'FIZ-DALGA-01', 'FIZ-ATOM-01',
    'FIZ-ELEKTRIK-ILERI-01', 'FIZ-OPTIK-ILERI-01', 'FIZ-TERMAL-ILERI-01'
)
ORDER BY archetype, t.code;

-- Physics cumulative (should show 18 topics, 12F/6S)
SELECT 
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT tc.id) as with_context,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END) as foundational,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'synthesis' THEN 1 ELSE 0 END) as synthesis,
    ROUND(100.0 * SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END)::numeric / 
          NULLIF(COUNT(DISTINCT tc.id), 0), 1) || '%' as foundational_pct,
    ROUND(100.0 * COUNT(DISTINCT tc.id) / NULLIF(COUNT(DISTINCT t.id), 0), 1) || '%' as completion
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'FIZ';
-- Expected: 18 topics, 12F, 6S, 67% foundational, ~51% completion
