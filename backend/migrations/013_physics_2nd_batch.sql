-- ============================================
-- MIGRATION 013: PHYSICS 2ND BATCH
-- Date: 2024-12-31
-- Topics: 6 (Elektrik, Manyetizma, Basınç + 3 Synthesis)
-- Target: 11/35 topics (31% Physics complete)
-- Archetype: 3F/3S (Balance phase begins!)
-- Velocity: 3x sustained
-- Format: v1.0 (REUSED - no changes!)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (3F + 3S)
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
    
    -- Insert 6 topics (3F + 3S)
    INSERT INTO topics (
        curriculum_version_id,
        subject_id,
        code,
        name_tr,
        difficulty_level,
        grade_level,
        is_active
    ) VALUES
    -- FOUNDATIONAL (3 topics)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-ELEKTRIK-01', 'Elektrostatik ve Elektrik Akımı', 6, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-MANYETIK-01', 'Manyetizma', 6, '11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-BASINC-01', 'Basınç ve Kaldırma Kuvveti', 5, '9,tyt', true),
    
    -- SYNTHESIS (3 topics)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-HAREKET-ILERI-01', 'İleri Hareket Problemleri', 7, '10,tyt,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-KUVVET-ILERI-01', 'İleri Kuvvet ve Denge Problemleri', 8, '10,11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-ENERJI-ILERI-01', 'İleri Enerji Dönüşümleri ve Korunum', 8, '10,11,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '6 Physics topics (3F + 3S) inserted successfully';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (6 contexts)
-- ============================================

DO $$
DECLARE
    v_topic_id UUID;
BEGIN
    -- ==========================================
    -- FOUNDATIONAL TOPICS (3)
    -- ==========================================
    
    -- 1. FIZ-ELEKTRIK-01: Elektrostatik ve Elektrik Akımı (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-ELEKTRIK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Elektrik yükü ve yük korunumu kavramlarını anlama',
            'Coulomb kanunu ve elektrik alanı hesaplamaları',
            'Elektrik potansiyeli ve potansiyel enerji kavramları',
            'Elektrik akımı, gerilim, direnç ilişkilerini bilme (Ohm kanunu)',
            'Seri ve paralel devre analizleri yapma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01',
            'FIZ-KUVVET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Akım ile gerilimi karıştırma (akım yük akışı, gerilim enerji farkı)',
            'Seri devrede akımın azaldığını sanma (sabit kalır!)',
            'Paralel devrede gerilimin bölündüğünü sanma (sabit kalır!)',
            'İletken ile yalıtkan arasındaki farkı sadece madde türü olarak görme',
            'Elektrik alanının yönünü yanlış belirleme (+ → -)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 270,
            'practice', 330,
            'mastery', 240
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Elektrostatik ve akım temelleri, devre kavramları ile 25 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-ELEKTRIK-01';
    
    -- 2. FIZ-MANYETIK-01: Manyetizma (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-MANYETIK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Manyetik alan ve manyetik kuvvet kavramlarını anlama',
            'Akım taşıyan iletkenin manyetik alanını hesaplama',
            'Lorentz kuvveti ve yönünü belirleme (sağ el kuralı)',
            'Elektromanyetik indüksiyon ilkesini bilme',
            'Transformatör çalışma prensibini anlama'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-ELEKTRIK-01'
        ),
        'misconceptions', jsonb_build_array(
            'Manyetik alan ile elektrik alanını karıştırma',
            'Sağ el kuralını yanlış uygulama (parmak yönleri)',
            'Manyetik kuvvetin işin yaptığını sanma (dik bileşen iş yapmaz)',
            'İndüksiyon akımının yönünü Lenz yasasıyla belirleyememe',
            'Transformatörde güç kaybı olmadığını sanma (ideal durum dışında var!)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 210
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Manyetizma temelleri ve indüksiyon, sağ el kuralları ile 20-25 dakikada kavranabilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-MANYETIK-01';
    
    -- 3. FIZ-BASINC-01: Basınç ve Kaldırma Kuvveti (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-BASINC-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Orta'
        ),
        'learning_objectives', jsonb_build_array(
            'Basınç kavramını ve birimlerini anlama',
            'Katı, sıvı ve gaz basıncı hesaplamaları',
            'Pascal prensibi ve hidrolik sistemler',
            'Kaldırma kuvveti (Arşimet prensibi)',
            'Yüzme, batma, askıda kalma koşulları'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-BUYUK-01',
            'FIZ-KUVVET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Basınç ile kuvveti karıştırma (P = F/A)',
            'Sıvı basıncının kabın şekline bağlı olduğunu sanma (sadece derinlik)',
            'Kaldırma kuvvetini sadece su için geçerli sanma (her akışkan!)',
            'Batma koşulunu sadece kütle ile ilişkilendirme (yoğunluk önemli)',
            'Hava basıncını ihmal edilebilir sanma (1 atm = 10^5 Pa büyük!)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 180,
            'practice', 240,
            'mastery', 150
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Basınç ve kaldırma kuvveti temel akışkanlar konusudur, 15-20 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-BASINC-01';
    
    -- ==========================================
    -- SYNTHESIS TOPICS (3)
    -- ==========================================
    
    -- 4. FIZ-HAREKET-ILERI-01: İleri Hareket Problemleri (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-HAREKET-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Parçalı hareket problemlerini çözme',
            'Göreceli hareket analizleri yapma',
            'İki boyutlu hareket (atış, dairesel hareket)',
            'Grafik yorumlama ve grafik çizme becerisi',
            'Kompleks kinematik senaryoları analiz etme'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-HAREKET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Göreceli hızda vektör toplamını yanlış yapma',
            'Parçalı harekette toplam yer değiştirmeyi yol toplamı sanma',
            'İki boyutlu harekette x ve y bileşenlerini karıştırma',
            'Dairesel harekette ivmeyi sıfır sanma (merkezcil ivme var!)',
            'Grafik altı alanı yanlış yorumlama (hız-zaman → yer değiştirme)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 300,
            'practice', 420,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'Kompleks hareket problemleri 4 ana kategoriye ayrılmalı: Parçalı Hareket, Göreceli Hareket, İki Boyutlu Hareket, Grafik Yorumlama'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Göreceli hız problemleri (TYT favori)',
                'Grafik yorumlama (her sınavda çıkar)',
                'Parçalı hareket (ortalama hız tuzakları)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Üç boyutlu hareket (nadir)',
                'Karmaşık parametrik denklemler (zaman alıcı)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-HAREKET-ILERI-01';
    
    -- 5. FIZ-KUVVET-ILERI-01: İleri Kuvvet ve Denge Problemleri (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-KUVVET-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Orta',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Eğik düzlemde kuvvet analizi',
            'İpli sistemler ve makara problemleri',
            'Dönme dengesi ve tork kavramı',
            'Atwood makinesi ve varyasyonları',
            'Kompleks sürtünme senaryoları'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-KUVVET-01',
            'FIZ-HAREKET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Eğik düzlemde normal kuvveti ağırlık sanma (Ncosθ ≠ mg)',
            'İp gerilmesinin her noktada farklı olduğunu sanma (sürtünmesiz makara: aynı)',
            'Tork hesabında kuvvet kolunu yanlış belirleme',
            'Atwood''da ağır cismin ivmesini g sanma (net kuvvete bağlı)',
            'Statik ve kinetik sürtünmeyi karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 480,
            'mastery', 420
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'İleri kuvvet problemleri 4 kategoriye ayrılmalı: Eğik Düzlem, İpli Sistemler, Dönme Dengesi, Sürtünmeli Sistemler'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Eğik düzlem (AYT klasiği)',
                'Basit Atwood (sık çıkar)',
                'Dönme dengesi temelleri (tork)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Çok makaralı karmaşık sistemler (zaman tuzağı)',
                'Üç boyutlu denge problemleri (nadir)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-KUVVET-ILERI-01';
    
    -- 6. FIZ-ENERJI-ILERI-01: İleri Enerji Dönüşümleri ve Korunum (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-ENERJI-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Sürtünmeli yüzeylerde enerji kaybı hesaplama',
            'Yay sistemlerinde enerji dönüşümleri',
            'Eğik düzlem ve enerji korunumu birlikte',
            'Çarpışmalarda enerji ve momentum analizi',
            'Kompleks mekanik sistem problemleri'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-ENERJI-01',
            'FIZ-MOMENTUM-01'
        ),
        'misconceptions', jsonb_build_array(
            'Sürtünmede kaybolan enerjiyi hesaba katmama',
            'Yay enerjisinde x yerine x^2 kullanmayı unutma (E = 1/2 kx^2)',
            'Esnek çarpışmada hem momentum hem enerji korunumunu kontrol etmeme',
            'Potansiyel enerji referans noktasını karıştırma',
            'Dönen cisimlerde sadece öteleme enerjisini hesaplama (dönme + öteleme)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 330,
            'practice', 450,
            'mastery', 390
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'İleri enerji konuları 4 kategoriye ayrılmalı: Sürtünmeli Sistemler, Yay Enerjisi, Çarpışmalar, Kompleks Dönüşümler'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Sürtünmede enerji kaybı (mutlaka çıkar)',
                'Basit yay problemleri (sık)',
                'Esnek çarpışma (klasik soru)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Çok aşamalı karmaşık sistemler',
                'Dönen cisimler (atalet momenti dahil, ileri AYT)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-ENERJI-ILERI-01';
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'PHYSICS 2ND BATCH COMPLETE!';
    RAISE NOTICE '11/35 topics (31%% complete)';
    RAISE NOTICE 'Balance phase: 8F/3S';
    RAISE NOTICE 'First synthesis topics added!';
    RAISE NOTICE '==========================================';
    
END $$;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check all 6 topics inserted
SELECT 
    code,
    name_tr,
    difficulty_level,
    is_active
FROM topics
WHERE code IN (
    'FIZ-ELEKTRIK-01', 'FIZ-MANYETIK-01', 'FIZ-BASINC-01',
    'FIZ-HAREKET-ILERI-01', 'FIZ-KUVVET-ILERI-01', 'FIZ-ENERJI-ILERI-01'
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
    'FIZ-ELEKTRIK-01', 'FIZ-MANYETIK-01', 'FIZ-BASINC-01',
    'FIZ-HAREKET-ILERI-01', 'FIZ-KUVVET-ILERI-01', 'FIZ-ENERJI-ILERI-01'
)
ORDER BY archetype, t.code;

-- Physics cumulative (should show 11 topics, 8F/3S)
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
