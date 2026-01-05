-- ============================================
-- MIGRATION 016: PHYSICS 5TH BATCH
-- Date: 2024-12-31
-- Topics: 6 (Akışkan, Gravitasyon + 4 Synthesis)
-- Target: 30/35 topics (86% Physics complete!)
-- Archetype: 2F/4S → Total 16F/14S (53%/47%)
-- Velocity: 3.7x+ sustained (ULTRA MOMENTUM!)
-- Format: v1.0 (REUSED - rock solid!)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (2F + 4S)
-- ============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_physics_subject_id UUID;
BEGIN
    SELECT id INTO v_curriculum_version_id
    FROM curriculum_versions
    WHERE country_code = 'TR' AND system_code = 'MEB' AND academic_year = 2024
    LIMIT 1;
    
    SELECT id INTO v_physics_subject_id
    FROM subjects WHERE code = 'FIZ' LIMIT 1;
    
    INSERT INTO topics (
        curriculum_version_id, subject_id, code, name_tr,
        difficulty_level, grade_level, is_active
    ) VALUES
    -- FOUNDATIONAL (2)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-AKISKAN-01', 'Akışkanlar Dinamiği', 6, '10,tyt,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-GRAVITE-01', 'Evrensel Çekim ve Gravitasyon', 7, '11,ayt', true),
    
    -- SYNTHESIS (4)
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-BASINC-ILERI-01', 'İleri Akışkan Problemleri', 8, '11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-MANYETIK-ILERI-01', 'İleri Manyetizma ve İndüksiyon', 8, '11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-DALGA-ILERI-01', 'İleri Dalga Problemleri', 8, '11,ayt', true),
    (v_curriculum_version_id, v_physics_subject_id, 'FIZ-DENGE-ILERI-01', 'İleri Denge ve Dönme Hareketi', 8, '11,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '6 Physics topics (2F + 4S) inserted - 86%%%% milestone!';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (6 contexts)
-- ============================================

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- 1. FIZ-AKISKAN-01: Akışkanlar Dinamiği (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-AKISKAN-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Orta', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Akışkan akışı ve süreklilik denklemi',
            'Bernoulli prensibi ve uygulamaları',
            'Viskozite ve laminer akış',
            'Akış hızı ve debi hesaplamaları',
            'Venturi etkisi ve pratik uygulamalar'
        ),
        'prerequisite_topics', jsonb_build_array('FIZ-BASINC-01', 'FIZ-ENERJI-01'),
        'misconceptions', jsonb_build_array(
            'Süreklilik denkleminde kütle yerine hacim korunumunu sanma',
            'Bernoulli''de basınç artarken hızın arttığını sanma (ters orantılı)',
            'Viskoziteyi sadece sıvılar için geçerli sanma (gazlar da)',
            'Laminer ile türbülanslı akışı karıştırma',
            'Venturi''de basınç düşmesinin yanlış yorumu'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 210),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Akışkan dinamiği temelleri, Bernoulli ve süreklilik ile 20-25 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 2. FIZ-GRAVITE-01: Evrensel Çekim (FOUNDATIONAL)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-GRAVITE-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Newton''un evrensel çekim yasası',
            'Gravitasyonel alan ve potansiyel',
            'Yerçekimi ivmesi ve değişimi',
            'Ağırlık ve kütle farkı',
            'Serbest düşüş ve fırlatma hareketleri'
        ),
        'prerequisite_topics', jsonb_build_array('FIZ-KUVVET-01', 'FIZ-HAREKET-01'),
        'misconceptions', jsonb_build_array(
            'Kütle ile ağırlığı karıştırma (kütle değişmez, ağırlık değişir)',
            'Gravitasyon kuvvetinin sadece Dünya için geçerli olduğunu sanma',
            'Yükseklikte yerçekimi ivmesinin sabit kaldığını sanma (azalır)',
            'Gravitasyonel potansiyel enerjiyi sadece yüzeye yakın için bilme',
            'Serbest düşüşte ağırlıksızlık olmadığını unutma (g varken de)'
        ),
        'time_estimate', jsonb_build_object('foundation', 210, 'practice', 270, 'mastery', 180),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Evrensel çekim temelleri ve gravitasyonel alan 20 dakikada kavranabilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 3. FIZ-BASINC-ILERI-01: İleri Akışkan (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-BASINC-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Kompleks Bernoulli problemleri',
            'Toriçelli teoremi ve uygulamaları',
            'Hidrolik sistemler ileri analiz',
            'Batma-yüzme dengesi problemleri',
            'Akışkan akış hızı optimizasyonu'
        ),
        'prerequisite_topics', jsonb_build_array('FIZ-BASINC-01', 'FIZ-AKISKAN-01'),
        'misconceptions', jsonb_build_array(
            'Toriçelli''de delik yüksekliğinin önemsiz olduğunu sanma',
            'Hidrolik preste basınç çarpanını güç çarpanı sanma',
            'Batma koşulunda sadece yoğunluğu kontrol etme (hacim de önemli)',
            'Bernoulli''de sürtünme kayıplarını ihmal etme',
            'Akış hızının sadece basınca bağlı olduğunu sanma (alan da)'
        ),
        'time_estimate', jsonb_build_object('foundation', 330, 'practice', 420, 'mastery', 360),
        'splitting', jsonb_build_object(
            'recommended', true, 'parts', 4,
            'rationale', 'İleri akışkan 4 kategoriye ayrılmalı: Bernoulli İleri, Toriçelli ve Akış, Hidrolik Sistemler, Batma-Yüzme Dengesi'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Toriçelli teoremi (AYT klasik)', 'Basit Bernoulli (sık)', 'Kaldırma kuvveti dengesi (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Çok karmaşık akış sistemleri', 'Viskozite detaylı hesaplar')
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 4. FIZ-MANYETIK-ILERI-01: İleri Manyetizma (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-MANYETIK-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Faraday indüksiyon yasası ileri uygulamalar',
            'Lenz yasası ve yön belirleme',
            'Transformatör detaylı analiz',
            'Öz-indüksiyon ve bobinler',
            'AC devrelerinde indüktans'
        ),
        'prerequisite_topics', jsonb_build_array('FIZ-MANYETIK-01', 'FIZ-ELEKTRIK-01'),
        'misconceptions', jsonb_build_array(
            'Faraday''de alan değişimi yerine akı değişimini unutma',
            'Lenz yasasında indüksiyon akımı yönünü yanlış belirleme',
            'Transformatörde güç korunumunu ihmal etme (ideal durum)',
            'Öz-indüksiyonda akımın anında değiştiğini sanma (L etkisi)',
            'AC devresinde indüktansın dirençle aynı davrandığını sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 360, 'practice', 450, 'mastery', 390),
        'splitting', jsonb_build_object(
            'recommended', true, 'parts', 4,
            'rationale', 'İleri manyetizma 4 kategoriye ayrılmalı: Faraday İleri, Lenz ve Yön, Transformatör Analizi, Öz-indüksiyon ve AC'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Faraday temel (AYT mutlaka)', 'Transformatör ideal (klasik)', 'Lenz yön (sık)'),
            'low_roi_subtopics', jsonb_build_array('AC devre empedans (nadir)', 'Karmaşık öz-indüksiyon')
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 5. FIZ-DALGA-ILERI-01: İleri Dalga (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-DALGA-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Dalga girişimi ve süperpozisyon',
            'Duran dalgalar ve harmonikler',
            'Doppler etkisi ileri problemler',
            'Rezonans koşulları ve uygulamalar',
            'Ses şiddeti ve desibel'
        ),
        'prerequisite_topics', jsonb_build_array('FIZ-DALGA-01'),
        'misconceptions', jsonb_build_array(
            'Yapıcı girişimde amplitüdlerin toplanmadığını sanma (süperpozisyon)',
            'Duran dalgada düğüm sayısını yanlış hesaplama',
            'Doppler''de sadece kaynak hareketini düşünme (gözlemci de)',
            'Rezonansı sadece mekanik sistemlerle sınırlama (EM de var)',
            'Desibel''in doğrusal ölçek olduğunu sanma (logaritmik)'
        ),
        'time_estimate', jsonb_build_object('foundation', 330, 'practice', 420, 'mastery', 360),
        'splitting', jsonb_build_object(
            'recommended', true, 'parts', 4,
            'rationale', 'İleri dalga 4 kategoriye ayrılmalı: Girişim ve Süperpozisyon, Duran Dalgalar, Doppler İleri, Ses ve Rezonans'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Doppler temel (AYT mutlaka)', 'Duran dalga (klasik)', 'Basit girişim (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık süperpozisyon', 'Desibel hesaplamaları detay')
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 6. FIZ-DENGE-ILERI-01: İleri Denge ve Dönme (SYNTHESIS)
    SELECT id INTO v_topic_id FROM topics WHERE code = 'FIZ-DENGE-ILERI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Dönme hareketi kinematiği (açısal hız, ivme)',
            'Atalet momenti hesaplamaları',
            'Açısal momentum ve korunumu',
            'Dönme enerjisi ve toplam enerji',
            'Kompleks denge problemleri'
        ),
        'prerequisite_topics', jsonb_build_array('FIZ-DENGE-01', 'FIZ-HAREKET-01'),
        'misconceptions', jsonb_build_array(
            'Açısal hızı doğrusal hızla karıştırma (v = rω ilişkisi)',
            'Atalet momentinin sadece kütleye bağlı olduğunu sanma (dağılım da)',
            'Açısal momentum korunumunda dış tork yokluğunu unutma',
            'Yuvarlanmada sadece öteleme enerjisini hesaplama (dönme de)',
            'Tork ile açısal momentumu karıştırma'
        ),
        'time_estimate', jsonb_build_object('foundation', 360, 'practice', 480, 'mastery', 420),
        'splitting', jsonb_build_object(
            'recommended', true, 'parts', 4,
            'rationale', 'İleri denge 4 kategoriye ayrılmalı: Dönme Kinematiği, Atalet Momenti, Açısal Momentum, Dönme Enerjisi ve Yuvarlanma'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Atalet momenti temel (AYT klasik)', 'Açısal momentum korunumu (mutlaka)', 'Yuvarlanma enerjisi (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık atalet momenti hesapları', 'Jiroskop etkileri')
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'PHYSICS 5TH BATCH COMPLETE!';
    RAISE NOTICE '30/35 topics (86%%%% complete!)';
    RAISE NOTICE 'Balance: 16F/14S (53%%%%/47%%%%)';
    RAISE NOTICE '==========================================';
END $$;
