-- ============================================
-- MIGRATION 025: BIOLOGY 3RD BATCH
-- Date: 2024-12-31
-- Topics: 5 (Boşaltım, Sinir + İleri konular)
-- Target: 15/20 topics (75%%)
-- Archetype: 2F/3S → Total 9F/6S (60%%/40%%)
-- Velocity: 3.7x sustained!
-- ============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_biology_subject_id UUID;
BEGIN
    SELECT id INTO v_curriculum_version_id FROM curriculum_versions
    WHERE country_code = 'TR' AND system_code = 'MEB' AND academic_year = 2024 LIMIT 1;
    
    SELECT id INTO v_biology_subject_id FROM subjects WHERE code = 'BIO' LIMIT 1;
    
    INSERT INTO topics (curriculum_version_id, subject_id, code, name_tr, difficulty_level, grade_level, is_active)
    VALUES
    -- FOUNDATIONAL (2)
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-BOSALTIM-01', 'Boşaltım Sistemi', 5, '10,tyt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-SINIR-01', 'Sinir Sistemi ve Duyu Organları', 7, '11,ayt', true),
    
    -- SYNTHESIS (3)
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-EVRIM-01', 'Evrim Teorisi ve Kanıtları', 7, '11,12,ayt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-IMMUN-01', 'İmmün Sistem ve Bağışıklık', 7, '11,ayt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-HORMON-01', 'Hormonlar ve Endokrin Sistem', 7, '11,ayt', true)
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '5 topics (2F+3S) inserted - 75%%%%!';
END $$;

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- FOUNDATIONAL (2)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-BOSALTIM-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Yüksek', 'ayt', 'Orta'),
        'learning_objectives', jsonb_build_array(
            'Böbrek yapısı ve nefron',
            'İdrar oluşumu (süzülme, geri emilim, salgılama)',
            'Su ve tuz dengesi',
            'Boşaltım ürünleri (üre, ürik asit, amonyak)',
            'Ter ve akciğer yoluyla atık'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-HUCRE-01'),
        'misconceptions', jsonb_build_array(
            'Boşaltımın sadece böbrek olduğunu sanma (ter, akciğer de)',
            'Tüm suyun geri emildiğini sanma (bir kısmı)',
            'İdrar oluşumunun tek aşamalı olduğunu sanma',
            'Böbreğin sadece atık temizlediğini sanma (denge de)',
            'Ter bezlerinin boşaltım organı olmadığını sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 210, 'practice', 270, 'mastery', 180),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Boşaltım sistemi temelleri 20 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-SINIR-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Orta', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Nöron yapısı ve sinir iletimi',
            'Merkezi sinir sistemi (beyin, omurilik)',
            'Periferik sinir sistemi',
            'Refleks yayı',
            'Duyu organları (göz, kulak, dil, burun, deri)'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-HUCRE-01'),
        'misconceptions', jsonb_build_array(
            'Sinir iletiminin elektrik akımı olduğunu sanma (kimyasal+elektrik)',
            'Beynin %10''unu kullandığımızı sanma (tamamını)',
            'Refleksin beyin kontrolünde olduğunu sanma (omurilik)',
            'Tüm duyu organlarının aynı çalıştığını sanma',
            'Sinir hücrelerinin yenilendiğini sanma (yenilenmiyor)'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 360, 'mastery', 270),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Sinir sistemi temelleri 25-30 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- SYNTHESIS (3)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-EVRIM-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Darwin''in doğal seçilim teorisi',
            'Evrim kanıtları (fosil, anatomi, embriyoloji, moleküler)',
            'Adaptasyon ve spesiyasyon',
            'Lamarck ve Darwin karşılaştırması',
            'Modern sentez teorisi'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-KALITIM-01'),
        'misconceptions', jsonb_build_array(
            'Evrim''in amaçlı olduğunu sanma (rastgele)',
            'Bireysel evrimin olduğunu sanma (populasyon)',
            'Lamarck''ın tamamen yanlış olduğunu sanma',
            'Evrim teorisinin kanıtlanmamış olduğunu sanma',
            'İnsan maymundan geldiğini sanma (ortak ata)'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 390, 'mastery', 330),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'Evrim 4 kategoriye: Darwin Teorisi, Kanıtlar, Adaptasyon-Spesiyasyon, Tarihsel Gelişim'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Doğal seçilim (AYT klasik)', 'Fosil kanıtları (sık)', 'Adaptasyon (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Detaylı moleküler evrim', 'Karmaşık spesiyasyon'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-IMMUN-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Doğuştan ve kazanılmış bağışıklık',
            'Antijen ve antikor',
            'Lenfositler (B ve T hücreleri)',
            'Aşı ve serum',
            'Bağışıklık hastalıkları (otoimmün, allerji, AIDS)'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-DOLASIM-01'),
        'misconceptions', jsonb_build_array(
            'Aşı ile serumun aynı olduğunu sanma',
            'Antikorların virüsleri öldürdüğünü sanma (işaretler)',
            'T hücrelerinin antikor ürettiğini sanma (B hücreleri)',
            'Doğuştan bağışıklığın öğrenildiğini sanma',
            'AIDS''in hava yoluyla bulaştığını sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 390, 'mastery', 330),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İmmun 4 kategoriye: Bağışıklık Türleri, Antijen-Antikor, Lenfositler, Hastalıklar'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Aşı-serum farkı (AYT klasik)', 'Basit antikor (sık)', 'B-T ayrımı (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık otoimmün', 'Detaylı AIDS mekanizması'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-HORMON-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Endokrin bezler (hipofiz, tiroid, adrenal, pankreas)',
            'Hormon türleri ve etkileri',
            'Geri bildirim mekanizması',
            'İnsülin ve glukagon',
            'Büyüme hormonu ve tiroksin'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-DOLASIM-01'),
        'misconceptions', jsonb_build_array(
            'Hormonların hemen etki gösterdiğini sanma (yavaş)',
            'İnsülin ile glukagonun aynı işi yaptığını sanma (zıt)',
            'Endokrin ile ekzokrin bezi karıştırma',
            'Hipofizin sadece büyüme hormonu salgıladığını sanma',
            'Geri bildirimin sadece negatif olduğunu sanma (pozitif de)'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 390, 'mastery', 330),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'Hormon 4 kategoriye: Bezler, Hormon Türleri, Geri Bildirim, Örnek Hormonlar'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('İnsülin-glukagon (AYT klasik)', 'Bezler (sık)', 'Geri bildirim (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık hormon etkileşimleri', 'Nadir bezler'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE 'BIOLOGY 3RD BATCH COMPLETE! 15/20 (75%%%%)';
END $$;
