-- ============================================
-- MIGRATION 021: CHEMISTRY 4TH BATCH
-- Date: 2024-12-31
-- Topics: 6 (Elektrokimya, Organik + 4 Synthesis)
-- Target: 24/30 topics (80%% Chemistry)
-- Archetype: 2F/4S → Total 13F/11S (54%%/46%%)
-- Velocity: 3.7x sustained!
-- ============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_chemistry_subject_id UUID;
BEGIN
    SELECT id INTO v_curriculum_version_id FROM curriculum_versions
    WHERE country_code = 'TR' AND system_code = 'MEB' AND academic_year = 2024 LIMIT 1;
    
    SELECT id INTO v_chemistry_subject_id FROM subjects WHERE code = 'KIM' LIMIT 1;
    
    INSERT INTO topics (curriculum_version_id, subject_id, code, name_tr, difficulty_level, grade_level, is_active)
    VALUES
    -- FOUNDATIONAL (2)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ELEKTRO-01', 'Elektrokimya ve Piller', 7, '11,12,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ORGANIK-01', 'Organik Kimya Temelleri', 6, '11,ayt', true),
    
    -- SYNTHESIS (4)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ELEKTRO-ILERI-01', 'İleri Elektrokimya', 9, '12,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ORGANIK-ILERI-01', 'Organik Reaksiyonlar ve Mekanizmalar', 8, '11,12,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-REDOKS-01', 'İleri Redoks ve Denkleştirme', 8, '11,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ANALITIK-01', 'Analitik Kimya ve Titrasyonlar', 8, '12,ayt', true)
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '6 topics (2F+4S) inserted - 80%%%% milestone!';
END $$;

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- FOUNDATIONAL (2)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ELEKTRO-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Redoks tepkimeleri ve elektron transferi',
            'Galvanik piller ve Daniell pili',
            'Standart elektrot potansiyelleri',
            'Elektrolitik hücreler ve elektroliz',
            'Faraday yasaları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-TEPKIME-01'),
        'misconceptions', jsonb_build_array(
            'Oksidasyonu oksijen almak sanma (elektron kaybı)',
            'Anodun her zaman negatif olduğunu sanma (galvanikte -, elektrolitikte +)',
            'Standart potansiyelin mutlak değer olduğunu sanma (göreceli)',
            'Elektrolizde kütlenin akımın karesiyle arttığını sanma (doğrusal)',
            'Faraday sabitini evrensel gaz sabiti sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 360, 'mastery', 270),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Elektrokimya temelleri ve piller 25-30 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ORGANIK-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Orta', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Hidrokarbon türleri (alkan, alken, alkin)',
            'Fonksiyonel gruplar (alkol, aldehit, keton, asit)',
            'İzomerlik (yapısal, geometrik)',
            'IUPAC adlandırma kuralları',
            'Basit organik tepkimeler'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-BAG-01'),
        'misconceptions', jsonb_build_array(
            'Organik kimyanın sadece canlılarla ilgili olduğunu sanma',
            'Tüm hidrokarbonların doymamış olduğunu sanma',
            'İzomerlerin aynı özelliklere sahip olduğunu sanma',
            'IUPAC''ta en uzun zinciri rastgele seçme (dal sayısı önemli)',
            'Fonksiyonel grubun molekülün her yerinde olabileceğini sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 360, 'mastery', 270),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Organik kimya temelleri ve adlandırma 25-30 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- SYNTHESIS (4)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ELEKTRO-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Nernst denklemi ve konsantrasyon hücreleri',
            'Korozyon ve önleme yöntemleri',
            'Akümülatörler ve yakıt pilleri',
            'Elektrokimyasal seri',
            'Endüstriyel elektroliz uygulamaları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-ELEKTRO-01'),
        'misconceptions', jsonb_build_array(
            'Nernst denkleminde Q yerine K kullanma',
            'Korozyonun sadece demirde olduğunu sanma',
            'Yakıt pilinin şarj edilebilir olduğunu sanma',
            'Konsantrasyon hücresinde E°''nin sıfır olmadığını sanma',
            'Elektrokimyasal serinin evrensel olduğunu sanma (çözeltiye bağlı)'
        ),
        'time_estimate', jsonb_build_object('foundation', 390, 'practice', 480, 'mastery', 420),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri elektrokimya 4 kategoriye: Nernst ve Konsantrasyon, Korozyon, Piller İleri, Endüstriyel'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Basit Nernst (AYT klasik)', 'Korozyon basit (sık)', 'Pil türleri (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık konsantrasyon hücreleri', 'Endüstriyel detay'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ORGANIK-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Eliminasyon ve yerine koyma reaksiyonları',
            'Esterleşme ve sabunlaşma',
            'Polimerizasyon tepkimeleri',
            'Aromatik bileşikler',
            'Optik izomerlik ve kiral merkezler'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-ORGANIK-01'),
        'misconceptions', jsonb_build_array(
            'SN1 ile SN2''yi karıştırma',
            'Esterleşmenin geri dönüşümsüz olduğunu sanma',
            'Tüm polimerlerin plastik olduğunu sanma',
            'Benzenin doymamış olduğu için kolay tepkime verdiğini sanma (kararlı)',
            'Optik aktivitenin her zaman 4 farklı grup gerektirdiğini sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 360, 'practice', 480, 'mastery', 420),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'Organik reaksiyonlar 4 kategoriye: Yerine Koyma-Eliminasyon, Ester-Sabun, Polimer, Aromatik-Optik'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Esterleşme (AYT klasik)', 'Basit polimer (mutlaka)', 'Sabunlaşma (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık SN1/SN2 mekanizma', 'Optik izomerlik detay'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-REDOKS-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Yükseltgenme sayısı hesaplama',
            'Redoks denkleştirme (yarı tepkime yöntemi)',
            'Asidik ve bazik ortamda denkleştirme',
            'Disproporsiyonasyon tepkimeleri',
            'Redoks titrasyon hesaplamaları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-ELEKTRO-01'),
        'misconceptions', jsonb_build_array(
            'Yükseltgenme sayısının elektron sayısı olduğunu sanma',
            'Her redoks tepkimesinin elektrokimyasal olduğunu sanma',
            'Bazik ortamda H+ kullanma (OH- kullan)',
            'Disproporsiyonasyonda aynı elementin sadece yükseltgendiğini sanma',
            'Redoks titrasyonunda eşdeğerliliği mol oranı sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 330, 'practice', 420, 'mastery', 360),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'Redoks 4 kategoriye: Yük. Sayısı, Yarı Tepkime, Asit-Baz Ortam, Titrasyon'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Yükseltgenme sayısı (AYT mutlaka)', 'Basit denkleştirme (klasik)', 'Asidik ortam (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık disproporsiyonasyon', 'Çok aşamalı redoks'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ANALITIK-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Gravimetrik analiz',
            'Volumetrik analiz ve standart çözeltiler',
            'Asit-baz, redoks, çöktürme titrasyonları',
            'Kompleksometrik titrasyonlar',
            'Spektroskopi temelleri'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-ASIT-ILERI-01', 'KIM-REDOKS-01'),
        'misconceptions', jsonb_build_array(
            'Gravimetrik analizin her zaman tartım gerektirdiğini sanma',
            'Standart çözeltinin derişik çözelti olduğunu sanma',
            'Tüm titrasyonların asit-baz olduğunu sanma',
            'Kompleksometride sadece EDTA kullanıldığını sanma',
            'Spektroskopinin sadece UV-Vis olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 330, 'practice', 420, 'mastery', 360),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'Analitik kimya 4 kategoriye: Gravimetri, Volumetri, Titrasyonlar, Spektroskopi'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Asit-baz titrasyon (AYT klasik)', 'Basit gravimetri (sık)', 'Standart çözelti (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Kompleksometri detay', 'Spektroskopi ileri'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE 'CHEMISTRY 4TH BATCH COMPLETE! 24/30 (80%%%%)';
END $$;
