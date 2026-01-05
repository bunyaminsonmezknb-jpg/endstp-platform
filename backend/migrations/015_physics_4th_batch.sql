-- ============================================
-- MIGRATION 015: PHYSICS 4TH BATCH
-- Date: 2024-12-31
-- Topics: 6 (Denge, Çekirdek + 4 Synthesis)
-- Target: 24/35 topics (69% Physics complete - ALMOST 3/4!)
-- Archetype: 2F/4S → Total 14F/10S (58%/42%)
-- Velocity: 3.5x+ sustained (PEAK MOMENTUM!)
-- Format: v1.0 (REUSED - ultra stable!)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (2F + 4S)
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
    
    -- Insert 6 topics (2F + 4S)
    INSERT INTO topics (
        curriculum_version_id,
        subject_id,
        code,
        name_tr,
        difficulty_level,
        grade_level,
        is_active
    ) VALUES
    -- FOUNDATIONAL (2 topics)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-DENGE-01', 'Statik Denge ve Tork', 6, '9,10,tyt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-CEKIRDEK-01', 'Çekirdek Fiziği', 7, '12,ayt', true),
    
    -- SYNTHESIS (4 topics)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-MOMENTUM-ILERI-01', 'İleri Momentum ve Çarpışmalar', 8, '10,11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-DAIRESEL-01', 'Dairesel Hareket ve Merkezcil Kuvvet', 7, '10,tyt,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-HARMONIC-01', 'Basit Harmonik Hareket', 8, '11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-MODERN-ILERI-01', 'İleri Modern Fizik', 9, '12,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '6 Physics topics (2F + 4S) inserted - 69%% ALMOST 3/4!';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (6 contexts)
-- ============================================

DO $$
DECLARE
    v_topic_id UUID;
BEGIN
    -- ==========================================
    -- FOUNDATIONAL TOPICS (2)
    -- ==========================================
    
    -- 1. FIZ-DENGE-01: Statik Denge ve Tork (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-DENGE-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Orta'
        ),
        'learning_objectives', jsonb_build_array(
            'Tork (moment) kavramını ve hesaplamasını anlama',
            'Statik denge koşullarını bilme (ΣF=0, Στ=0)',
            'Kaldıraç prensibi ve uygulamaları',
            'Ağırlık merkezi kavramı',
            'Cisim dengesi problemleri'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-KUVVET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Tork ile kuvveti karıştırma (τ = F × r, kol önemli)',
            'Kuvvet kolu belirleme hatası (dik mesafe)',
            'Ağırlık merkezini geometrik merkez sanma (kütleye bağlı)',
            'Denge için sadece net kuvvetin sıfır olması gerektiğini sanma (net tork da sıfır)',
            'Tork yönünü (saat-saat karşı) yanlış belirleme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 210,
            'practice', 270,
            'mastery', 180
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Statik denge ve tork temel mekanik kavramlardır, kaldıraç ile 20 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-DENGE-01';
    
    -- 2. FIZ-CEKIRDEK-01: Çekirdek Fiziği (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-CEKIRDEK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Nükleer kuvvetler ve bağlanma enerjisi',
            'Kütle açığı ve Einstein denklemi (E=mc²)',
            'Nükleer fisyon ve füzyon',
            'Nükleer reaktörler ve enerji üretimi',
            'Radyasyondan korunma yöntemleri'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-ATOM-01'
        ),
        'misconceptions', jsonb_build_array(
            'Kütle açığını kütle kaybı olarak yorumlama (enerjiye dönüşüm)',
            'Fisyon ile füzyonu karıştırma (fisyon parçalanma, füzyon birleşme)',
            'Bağlanma enerjisini atomdan elektron koparmak için gereken enerji sanma',
            'Her elementin füzyon yapabileceğini sanma (hafif elementler)',
            'Radyasyon ile radyoaktiviteyi karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 210
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Çekirdek fiziği temelleri, fisyon-füzyon ve bağlanma enerjisi 20-25 dakikada kavranabilir'
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-CEKIRDEK-01';
    
    -- ==========================================
    -- SYNTHESIS TOPICS (4)
    -- ==========================================
    
    -- 3. FIZ-MOMENTUM-ILERI-01: İleri Momentum ve Çarpışmalar (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-MOMENTUM-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Orta',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Kompleks çarpışma problemleri (2D çarpışma)',
            'Esnek ve esnek olmayan çarpışma analizi',
            'Patlama ve geri tepme olayları',
            'Momentum ve enerji korunumu birlikte',
            'Değişken kütleli sistemler (roket problemi)'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-MOMENTUM-01',
            'FIZ-ENERJI-01'
        ),
        'misconceptions', jsonb_build_array(
            'İki boyutlu çarpışmada vektörel momentum korunumunu ihmal etme',
            'Esnek çarpışmada sadece momentum korunumunu kontrol etme (enerji de)',
            'Tam esnek olmayan çarpışmada momentum korunmaz sanma (korunur!)',
            'Patlamada momentum korunmaz sanma (dış kuvvet yoksa korunur)',
            'Roket probleminde kütle kaybını ihmal etme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 480,
            'mastery', 420
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'İleri momentum 4 kategoriye ayrılmalı: Esnek Çarpışma, Esnek Olmayan Çarpışma, Patlama-Geri Tepme, 2D ve Kompleks Sistemler'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Esnek çarpışma (AYT klasik)',
                'Tam esnek olmayan (mutlaka)',
                'Basit patlama problemleri (sık)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Roket denklemi (çok nadir)',
                'Çok karmaşık 2D çarpışma (zaman alıcı)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-MOMENTUM-ILERI-01';
    
    -- 4. FIZ-DAIRESEL-01: Dairesel Hareket (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-DAIRESEL-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Düzgün dairesel hareket parametreleri (ω, T, f)',
            'Merkezcil ivme ve merkezcil kuvvet',
            'Dönen sistemler (viraj, dönme dolap, salıncak)',
            'Açısal momentum ve korunumu',
            'Uydu hareketi ve Kepler yasaları'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-HAREKET-01',
            'FIZ-KUVVET-01'
        ),
        'misconceptions', jsonb_build_array(
            'Merkezcil kuvveti ayrı bir kuvvet sanma (net kuvvetin bileşeni)',
            'Merkezkaç kuvvetinin gerçek olduğunu sanma (görünür kuvvet)',
            'Düzgün dairesel harekette ivme olmadığını sanma (merkezcil ivme var)',
            'Açısal hızı doğrusal hızla karıştırma (ω ≠ v)',
            'Uydu hızının yükseklikten bağımsız olduğunu sanma (yakın olana hızlı)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 330,
            'practice', 420,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'Dairesel hareket 4 kategoriye ayrılmalı: Düzgün Dairesel Hareket, Merkezcil Kuvvet Problemleri, Açısal Momentum, Uydu ve Gezegen Hareketi'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Merkezcil kuvvet (TYT-AYT mutlaka)',
                'Viraj problemleri (klasik)',
                'Basit uydu hareketi (sık)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Kepler yasaları detay (nadir)',
                'Karmaşık açısal momentum (ileri)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-DAIRESEL-01';
    
    -- 5. FIZ-HARMONIC-01: Basit Harmonik Hareket (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-HARMONIC-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Basit harmonik hareket (BHH) özellikleri',
            'Yay-kütle sistemi ve periyot',
            'Sarkaç hareketi (basit ve fiziksel)',
            'BHH''de enerji dönüşümleri',
            'Rezonans ve uygulamaları'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-HAREKET-01',
            'FIZ-ENERJI-01'
        ),
        'misconceptions', jsonb_build_array(
            'BHH''de hızın her noktada aynı olduğunu sanma (değişir)',
            'Yay sabitinin kütleye bağlı olduğunu sanma (yaya bağlı)',
            'Sarkaç periyodunun kütleye bağlı olduğunu sanma (bağlı değil)',
            'BHH''de toplam enerjinin değiştiğini sanma (korunur, sürtünmesiz)',
            'Rezonansı sadece salıncakla sınırlama (köprüler, moleküller)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 330,
            'practice', 420,
            'mastery', 390
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'BHH 4 kategoriye ayrılmalı: Yay-Kütle Sistemi, Sarkaç Hareketi, Enerji Analizi, Rezonans ve Uygulamalar'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Yay-kütle periyodu (AYT klasik)',
                'Sarkaç periyodu (sık)',
                'BHH enerji korunumu (mutlaka)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Fiziksel sarkaç (nadir)',
                'Karmaşık rezonans hesaplamaları (ileri)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-HARMONIC-01';
    
    -- 6. FIZ-MODERN-ILERI-01: İleri Modern Fizik (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-MODERN-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Kuantum mekaniği temelleri (dalga-parçacık)',
            'Fotoelektrik olay ve Einstein denklemi',
            'Compton saçılması',
            'De Broglie dalga boyu',
            'Heisenberg belirsizlik ilkesi'
        ),
        'prerequisite_topics', jsonb_build_array(
            'FIZ-ATOM-01',
            'FIZ-CEKIRDEK-01'
        ),
        'misconceptions', jsonb_build_array(
            'Fotonun kütlesi olduğunu sanma (kütlesiz, momentum var)',
            'Fotoelektrikte ışık şiddeti ile elektron enerjisini ilişkilendirme (frekans)',
            'Compton saçılmasında foton enerjisinin değişmediğini sanma (azalır)',
            'De Broglie dalga boyunu sadece elektronlar için geçerli sanma (her parçacık)',
            'Belirsizlik ilkesini ölçüm hatası olarak yorumlama (doğanın kuralı)'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 450,
            'mastery', 390
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'İleri modern fizik 4 kategoriye ayrılmalı: Kuantum Temelleri, Fotoelektrik Olay, Compton ve De Broglie, Belirsizlik ve Uygulamalar'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array(
                'Fotoelektrik olay (AYT klasik)',
                'Einstein denklemi (mutlaka)',
                'De Broglie basit hesaplar (sık)'
            ),
            'low_roi_subtopics', jsonb_build_array(
                'Compton detaylı hesaplar (nadir)',
                'Belirsizlik ilkesi uygulamaları (ileri)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for FIZ-MODERN-ILERI-01';
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'PHYSICS 4TH BATCH COMPLETE!';
    RAISE NOTICE '24/35 topics (69%% - ALMOST 3/4!)';
    RAISE NOTICE 'Balance: 14F/10S (58%%/42%%)';
    RAISE NOTICE '3.5x+ velocity sustained!';
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
    'FIZ-DENGE-01', 'FIZ-CEKIRDEK-01',
    'FIZ-MOMENTUM-ILERI-01', 'FIZ-DAIRESEL-01',
    'FIZ-HARMONIC-01', 'FIZ-MODERN-ILERI-01'
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
    'FIZ-DENGE-01', 'FIZ-CEKIRDEK-01',
    'FIZ-MOMENTUM-ILERI-01', 'FIZ-DAIRESEL-01',
    'FIZ-HARMONIC-01', 'FIZ-MODERN-ILERI-01'
)
ORDER BY archetype, t.code;

-- Physics cumulative (should show 24 topics, 14F/10S)
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
-- Expected: 24 topics, 14F, 10S, 58% foundational, ~69% completion
