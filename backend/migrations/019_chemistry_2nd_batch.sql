-- ============================================
-- MIGRATION 019: CHEMISTRY 2ND BATCH
-- Date: 2024-12-31
-- Topics: 6 (Çözeltiler, Asit-Baz, Gazlar + 3 Synthesis)
-- Target: 12/30 topics (40%% Chemistry)
-- Archetype: 3F/3S → Total 8F/4S (67%%/33%%)
-- Velocity: 3.7x sustained!
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
    -- FOUNDATIONAL (3)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-COZELTI-01', 'Çözeltiler ve Derişim', 5, '9,10,tyt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ASIT-01', 'Asitler ve Bazlar', 6, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-GAZ-01', 'Gazlar ve Gaz Yasaları', 5, '10,tyt,ayt', true),
    
    -- SYNTHESIS (3)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-COZELTI-ILERI-01', 'İleri Çözelti Hesaplamaları', 8, '11,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-ASIT-ILERI-01', 'İleri Asit-Baz Dengesi', 8, '11,12,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-GAZ-ILERI-01', 'İleri Gaz Problemleri', 7, '11,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '6 topics (3F+3S) inserted - 40%%%% milestone!';
END $$;

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- FOUNDATIONAL (3)
    
    -- 1. KIM-COZELTI-01
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-COZELTI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Çözücü, çözünen, çözelti kavramları',
            'Derişim birimleri (%%, ppm, molarite, molalite)',
            'Seyreltme ve karıştırma hesaplamaları',
            'Çözünürlük ve doymuş çözelti',
            'Sıcaklık ve basıncın çözünürlüğe etkisi'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-MOL-01'),
        'misconceptions', jsonb_build_array(
            'Molarite ile molaliteyi karıştırma (hacim vs kütle)',
            'Seyreltmede mol sayısının değiştiğini sanma (sabit)',
            'Tüm maddelerin çözünürlüğünün sıcaklıkla arttığını sanma (gazlar azalır)',
            'Derişimi sadece %% olarak bilme (M, m, ppm var)',
            'Doymuş çözeltiye daha fazla çözünen eklenebileceğini sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 210),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Çözeltiler ve derişim hesaplamaları 20-25 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 2. KIM-ASIT-01
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ASIT-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Asit ve baz tanımları (Arrhenius, Brönsted-Lowry)',
            'pH ve pOH kavramları',
            'Kuvvetli ve zayıf asit-baz ayrımı',
            'Nötrleşme tepkimeleri',
            'İndikatörler ve pH ölçümü'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-COZELTI-01'),
        'misconceptions', jsonb_build_array(
            'pH''ın doğrusal ölçek olduğunu sanma (logaritmik)',
            'Kuvvetli asidi derişik asit sanma (farklı kavramlar)',
            'Zayıf asidin hiç iyonlaşmadığını sanma (az iyonlaşır)',
            'pH + pOH''ın her zaman 14 olduğunu sanma (25°C''de)',
            'Nötrleşmede her zaman pH=7 olduğunu sanma (tuz hidrolizi)'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 330, 'mastery', 240),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Asit-baz temelleri ve pH kavramı 25-30 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 3. KIM-GAZ-01
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-GAZ-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Yüksek', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'İdeal gaz denklemi (PV=nRT)',
            'Boyle, Charles, Gay-Lussac yasaları',
            'Dalton''un kısmi basınç yasası',
            'Gaz karışımları ve mol kesri',
            'Gerçek gazlar ve Van der Waals denklemi'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-MOL-01', 'KIM-MADDE-01'),
        'misconceptions', jsonb_build_array(
            'İdeal gaz yasasının her koşulda geçerli olduğunu sanma (yüksek P, düşük T''de değil)',
            'Kısmi basıncı toplam basınçla karıştırma',
            'Gaz karışımında her gazın ayrı hacmi olduğunu sanma (aynı)',
            'STP koşullarını standart koşul sanma (273K, 1atm)',
            'R sabitinin değerinin birimden bağımsız olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 210),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Gaz yasaları ve ideal gaz denklemi 20-25 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- SYNTHESIS (3)
    
    -- 4. KIM-COZELTI-ILERI-01
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-COZELTI-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Orta', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Koligatif özellikler (buhar basıncı düşmesi, kaynama noktası yükselmesi)',
            'Donma noktası alçalması',
            'Osmotik basınç',
            'Raoult yasası uygulamaları',
            'Elektrolit çözeltilerinde Van''t Hoff faktörü'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-COZELTI-01'),
        'misconceptions', jsonb_build_array(
            'Koligatif özelliklerin çözünen cinsine bağlı olduğunu sanma (sadece mol sayısına)',
            'İ faktörünü her zaman 1 sanma (elektrolitlerde >1)',
            'Raoult yasasının her çözeltide geçerli olduğunu sanma (ideal çözeltiler)',
            'Osmotik basıncı sadece biyolojik sistemlerde önemli sanma',
            'Donma noktası alçalmasının çözünürle doğru orantılı olmadığını düşünme'
        ),
        'time_estimate', jsonb_build_object('foundation', 330, 'practice', 420, 'mastery', 360),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri çözelti 4 kategoriye: Buhar Basıncı, Kaynama-Donma, Osmotik Basınç, Raoult ve i Faktörü'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Buhar basıncı düşmesi (AYT klasik)', 'ΔTk ve ΔTd hesapları (mutlaka)', 'i faktörü (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık Raoult', 'Çok bileşenli sistemler'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 5. KIM-ASIT-ILERI-01
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-ASIT-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Tampon çözeltiler ve Henderson-Hasselbalch',
            'Titrasyon eğrileri ve eşdeğerlik noktası',
            'Tuz hidrolizi ve pH hesaplamaları',
            'Çok protonlu asitler',
            'Asit-baz indikatörü seçimi'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-ASIT-01'),
        'misconceptions', jsonb_build_array(
            'Tamponun pH''ı hiç değiştirmediğini sanma (az değiştirir)',
            'Eşdeğerlik noktasının her zaman pH=7 olduğunu sanma',
            'Tuz çözeltilerinin nötr olduğunu sanma (hidroliz)',
            'İndikatörün dönüm noktasının eşdeğerlik noktası olduğunu sanma',
            'Çok protonlu asitlerde tüm protonların aynı anda koptuğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 360, 'practice', 450, 'mastery', 390),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri asit-baz 4 kategoriye: Tampon Sistemler, Titrasyon, Tuz Hidrolizi, Çok Protonlu Asitler'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Tampon pH hesabı (AYT mutlaka)', 'Basit titrasyon (klasik)', 'Tuz hidrolizi pH (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık titrasyon eğrileri', 'Çok protonlu asit detay'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 6. KIM-GAZ-ILERI-01
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-GAZ-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Kinetik moleküler teori',
            'Graham''ın yayılma yasası',
            'Gerçek gaz davranışı ve sıkıştırılabilirlik',
            'Van der Waals sabitleri',
            'Ortalama kinetik enerji ve sıcaklık ilişkisi'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-GAZ-01'),
        'misconceptions', jsonb_build_array(
            'Yayılma hızının molekül kütlesiyle doğru orantılı olduğunu sanma (ters kareköklü)',
            'Gerçek gazın ideal gazdan her zaman sapma gösterdiğini sanma (yüksek T, düşük P''de yakın)',
            'Van der Waals sabitlerinin evrensel olduğunu sanma (gaza özgü)',
            'Kinetik enerjinin sadece hıza bağlı olduğunu sanma (sıcaklık da)',
            'Sıkıştırılabilirlik faktörünün her zaman 1''den küçük olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 390, 'mastery', 330),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri gaz 4 kategoriye: Kinetik Teori, Graham Yasası, Gerçek Gazlar, Van der Waals'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Graham yayılma (AYT klasik)', 'Basit gerçek gaz (sık)', 'Kinetik enerji (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Van der Waals detay hesaplar', 'Sıkıştırılabilirlik karmaşık'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE 'CHEMISTRY 2ND BATCH COMPLETE! 12/30 (40%%%%)';
END $$;
