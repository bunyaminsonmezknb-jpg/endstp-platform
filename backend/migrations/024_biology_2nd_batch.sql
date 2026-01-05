-- ============================================
-- MIGRATION 024: BIOLOGY 2ND BATCH
-- Date: 2024-12-31
-- Topics: 5 (Sistemler + İleri Genetik/Ekoloji)
-- Target: 10/20 topics (50%% HALFWAY!)
-- Archetype: 3F/2S → Total 7F/3S (70%%/30%%)
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
    -- FOUNDATIONAL (3)
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-SINDIRIM-01', 'Sindirim Sistemi', 6, '10,tyt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-DOLASIM-01', 'Dolaşım Sistemi', 6, '10,tyt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-SOLUNUM-01', 'Solunum Sistemi', 5, '10,tyt', true),
    
    -- SYNTHESIS (2)
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-GENETIK-ILERI-01', 'İleri Genetik ve Mutasyonlar', 8, '11,12,ayt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-EKOLOJI-ILERI-01', 'İleri Ekoloji ve Biyomlar', 7, '11,ayt', true)
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '5 topics (3F+2S) inserted - 50%%%% HALFWAY!';
END $$;

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- FOUNDATIONAL (3)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-SINDIRIM-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Orta'),
        'learning_objectives', jsonb_build_array(
            'Sindirim kanalı organları (ağız, mide, bağırsaklar)',
            'Enzimlerin sindirim sistemi','Karbonhidrat, protein, yağ sindirimi',
            'Besinlerin emilimi',
            'Karaciğer ve pankreas fonksiyonları'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-HUCRE-01'),
        'misconceptions', jsonb_build_array(
            'Sindirim''in sadece midede olduğunu sanma (ağızda başlar)',
            'Karaciğerin sindirim organı olmadığını sanma (safra üretir)',
            'Tüm besinlerin aynı yerde sindirildiğini sanma',
            'İnce bağırsakta emilim olmadığını sanma (en fazla orada)',
            'Enzimlerin her ortamda çalıştığını sanma (pH önemli)'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 210),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Sindirim sistemi temelleri 20-25 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-DOLASIM-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Orta'),
        'learning_objectives', jsonb_build_array(
            'Kalp yapısı ve çalışması',
            'Kan damarları (arter, ven, kılcal)',
            'Kan bileşenleri (plazma, alyuvar, akyuvar, trombosit)',
            'Kan dolaşımı (büyük, küçük dolaşım)',
            'Kan grupları (ABO, Rh)'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-HUCRE-01'),
        'misconceptions', jsonb_build_array(
            'Kalbin sağ tarafında temiz kan olduğunu sanma (sol tarafta)',
            'Arter''in her zaman temiz kan taşıdığını sanma (akciğer arteri kirli)',
            'Akyuvarların oksijen taşıdığını sanma (alyuvarlar taşır)',
            'Tüm damarların aynı yapıda olduğunu sanma',
            'Kan grubunun sadece AB0 olduğunu sanma (Rh de var)'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 210),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Dolaşım sistemi temelleri 20-25 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-SOLUNUM-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Yüksek', 'ayt', 'Orta'),
        'learning_objectives', jsonb_build_array(
            'Solunum yolları (burun, soluk borusu, bronş)',
            'Akciğerler ve alveol yapısı',
            'Gaz alışverişi (O2, CO2)',
            'Hücresel solunum ve ATP üretimi',
            'Solunumun kontrolü'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-HUCRE-01'),
        'misconceptions', jsonb_build_array(
            'Solunum ile hücresel solunumu karıştırma',
            'Akciğerlerin kas olduğunu sanma (diyafram kasılır)',
            'Gaz alışverişinin akciğerde değil kanda olduğunu sanma',
            'Sadece oksijen alıp karbondioksit verdiğimizi sanma (azot da)',
            'ATP''nin sadece solunum sisteminde üretildiğini sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 210, 'practice', 270, 'mastery', 180),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Solunum sistemi temelleri 20 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- SYNTHESIS (2)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-GENETIK-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Mutasyon türleri (gen, kromozom)',
            'Genetik hastalıklar',
            'Kan grupları kalıtımı',
            'Cinsiyet kromozomları ve X''e bağlı kalıtım',
            'Populasyon genetiği temelleri'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-KALITIM-01', 'BIO-DNA-01'),
        'misconceptions', jsonb_build_array(
            'Tüm mutasyonların zararlı olduğunu sanma (nötr veya yararlı da)',
            'Genetik hastalıkların her zaman kalıtsal olduğunu sanma',
            'Kan grubu kalıtımında A''nın her zaman baskın olduğunu sanma',
            'Erkeklerde X kromozomu olmadığını sanma (XY var)',
            'Populasyon genetiğinde frekansların değişmediğini sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 330, 'practice', 420, 'mastery', 360),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri genetik 4 kategoriye: Mutasyonlar, Hastalıklar, Kan Grubu-Cinsiyet, Populasyon'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Basit mutasyon (AYT sık)', 'Kan grubu kalıtımı (klasik)', 'X''e bağlı (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık populasyon genetiği', 'Nadir genetik hastalıklar'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-EKOLOJI-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Orta', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Biyomlar (orman, çöl, tundra, savana)',
            'Biyoçeşitlilik ve korunması',
            'İklim değişikliği ve etkileri',
            'Karbon ve azot döngüleri',
            'Sürdürülebilir ekoloji'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-EKOSISTEM-01'),
        'misconceptions', jsonb_build_array(
            'Tüm biyomların aynı özelliklere sahip olduğunu sanma',
            'Biyoçeşitliliğin sadece hayvan sayısı olduğunu sanma',
            'İklim değişikliğinin sadece sıcaklık artışı olduğunu sanma',
            'Karbon döngüsünün tek yönlü olduğunu sanma',
            'Sürdürülebilirliğin sadece geri dönüşüm olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 390, 'mastery', 330),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri ekoloji 4 kategoriye: Biyomlar, Biyoçeşitlilik, İklim, Döngüler'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Temel biyomlar (AYT sık)', 'Karbon döngüsü (klasik)', 'Basit iklim (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık döngü hesapları', 'Detaylı biyom özellikleri'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE 'BIOLOGY 2ND BATCH COMPLETE! 10/20 (50%%%% - HALFWAY!)';
END $$;
