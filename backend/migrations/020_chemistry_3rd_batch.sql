-- ============================================
-- MIGRATION 020: CHEMISTRY 3RD BATCH
-- Date: 2024-12-31
-- Topics: 6 (Kinetik, Denge, Termo + 3 Synthesis)
-- Target: 18/30 topics (60%% Chemistry - HALFWAY!)
-- Archetype: 3F/3S → Total 11F/7S (61%%/39%%)
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
    -- FOUNDATIONAL (3)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-KINETIK-01', 'Kimyasal Kinetik ve Hız', 6, '11,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-DENGE-01', 'Kimyasal Denge', 7, '11,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-TERMO-01', 'Termokimya ve Enerji', 6, '11,ayt', true),
    
    -- SYNTHESIS (3)
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-KINETIK-ILERI-01', 'İleri Kimyasal Kinetik', 8, '11,12,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-DENGE-ILERI-01', 'İleri Kimyasal Denge', 8, '11,12,ayt', true),
    (v_curriculum_version_id, v_chemistry_subject_id, 'KIM-TERMO-ILERI-01', 'İleri Termokimya', 8, '11,12,ayt', true)
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '6 topics (3F+3S) inserted - 60%%%% HALFWAY!';
END $$;

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- FOUNDATIONAL (3)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-KINETIK-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Tepkime hızı ve hesaplanması',
            'Hız sabiti ve tepkime mertebesi',
            'Sıcaklık ve katalizörün hıza etkisi',
            'Arrhenius denklemi',
            'Tepkime mekanizmaları ve hız belirleyici adım'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-TEPKIME-01'),
        'misconceptions', jsonb_build_array(
            'Hız sabitinin sabit olduğunu sanma (sıcaklığa bağlı)',
            'Tepkime mertebesinin katsayılardan bulunduğunu sanma (deneysel)',
            'Katalizörün dengeyi kaydırdığını sanma (sadece hız)',
            'Aktivasyon enerjisinin tepkime ısısı olduğunu sanma',
            'Hız belirleyici adımın en hızlı adım olduğunu sanma (en yavaş)'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 330, 'mastery', 240),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Kimyasal kinetik temelleri 25-30 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-DENGE-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Denge kavramı ve dinamik denge',
            'Denge sabiti (Kc, Kp)',
            'Le Chatelier prensibi',
            'Derişim, basınç, sıcaklığın dengeye etkisi',
            'Heterojen dengeler'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-KINETIK-01'),
        'misconceptions', jsonb_build_array(
            'Dengenin statik olduğunu sanma (dinamik)',
            'Denge sabitinin koşullara bağlı olduğunu sanma (sadece sıcaklığa)',
            'Katalizörün dengeyi kaydırdığını sanma (sadece hızlandırır)',
            'Le Chatelier''de katı/sıvının etkili olduğunu sanma',
            'Kc ile Kp''yi karıştırma (farklı birimler)'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 360, 'mastery', 270),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Kimyasal denge ve Le Chatelier 25-30 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-TERMO-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Orta', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Endotermik ve ekzotermik tepkimeler',
            'Entalpi (ΔH) ve hesaplanması',
            'Hess yasası',
            'Standart oluşum entalpisi',
            'Bağ enerjisi hesaplamaları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-TEPKIME-01'),
        'misconceptions', jsonb_build_array(
            'Endotermik tepkimenin kendiliğinden olmadığını sanma (ΔG önemli)',
            'Entalpi ile sıcaklığı karıştırma (farklı)',
            'Hess yasasında yönün önemsiz olduğunu sanma (ΔH işaret değiştirir)',
            'Bağ enerjisinin tepkime ısısı olduğunu sanma',
            'Standart koşulların STP olduğunu sanma (298K, 1atm)'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 210),
        'splitting', jsonb_build_object('recommended', false,
            'rationale', 'Termokimya temelleri ve Hess yasası 20-25 dakikada öğretilebilir')
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- SYNTHESIS (3)
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-KINETIK-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Birinci ve ikinci mertebe tepkimeler',
            'Yarı ömür hesaplamaları',
            'Entegre hız denklemleri',
            'Karmaşık tepkime mekanizmaları',
            'Enzim kinetiği temelleri'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-KINETIK-01'),
        'misconceptions', jsonb_build_array(
            'Yarı ömrün her tepkimede sabit olduğunu sanma (sadece 1. mertebe)',
            'Mertebe toplamının molekülerliliğe eşit olduğunu sanma',
            'Hız denkleminin katsayılardan yazılabileceğini sanma',
            'Enzim kinetiğinde Michaelis-Menten''i her zaman uygulamak',
            'Ara ürünlerin kararlı olduğunu varsayma'
        ),
        'time_estimate', jsonb_build_object('foundation', 360, 'practice', 450, 'mastery', 390),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri kinetik 4 kategoriye: Mertebe Analizi, Yarı Ömür, Entegre Denklemler, Mekanizmalar'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('1. mertebe yarı ömür (AYT klasik)', 'Basit mekanizma (sık)', 'Arrhenius basit (mutlaka)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık entegre denklemler', 'Enzim kinetiği detay'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-DENGE-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Çözünürlük dengesi ve Ksp',
            'Ortak iyon etkisi',
            'Çökelme hesaplamaları',
            'Kompleks iyon dengeleri',
            'Çoklu denge sistemleri'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-DENGE-01'),
        'misconceptions', jsonb_build_array(
            'Ksp''nin çözünürlükle aynı olduğunu sanma',
            'Ortak iyon''un çözünürlüğü artırdığını sanma (azaltır)',
            'Tüm tuzların çözündüğünü sanma (Ksp çok küçük olanlar)',
            'Kompleks iyonların daima kararlı olduğunu sanma',
            'Çoklu dengelerde herbir dengenin bağımsız olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 360, 'practice', 450, 'mastery', 390),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri denge 4 kategoriye: Çözünürlük Ksp, Ortak İyon, Çökelme, Kompleks İyonlar'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Basit Ksp (AYT klasik)', 'Ortak iyon (mutlaka)', 'Çökelme Q vs Ksp (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık kompleks iyonlar', 'Çoklu denge hesaplar'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    SELECT id INTO v_topic_id FROM topics WHERE code = 'KIM-TERMO-ILERI-01';
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0', 'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Düşük', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Entropi (ΔS) ve düzensizlik',
            'Gibbs serbest enerjisi (ΔG)',
            'Kendiliğindenlik kriterleri',
            'ΔG ile denge sabiti ilişkisi',
            'Termodinamik yasaları'
        ),
        'prerequisite_topics', jsonb_build_array('KIM-TERMO-01', 'KIM-DENGE-01'),
        'misconceptions', jsonb_build_array(
            'Entropi''nin sadece ısıyla ilgili olduğunu sanma (düzensizlik)',
            'ΔG < 0''ın hızlı tepkime anlamına geldiğini sanma (termodinamik vs kinetik)',
            'Kendiliğindenliğin sadece ekzotermikle olduğunu sanma (ΔG önemli)',
            'Standart koşullarda ΔG°''nin ΔG olduğunu sanma',
            '2. yasanın sadece izole sistemlerde geçerli olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 360, 'practice', 450, 'mastery', 390),
        'splitting', jsonb_build_object('recommended', true, 'parts', 4,
            'rationale', 'İleri termo 4 kategoriye: Entropi, Gibbs Enerjisi, Kendiliğindenlik, ΔG-K İlişkisi'),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('ΔG hesabı (AYT klasik)', 'ΔG = ΔH - TΔS (mutlaka)', 'Kendiliğindenlik (sık)'),
            'low_roi_subtopics', jsonb_build_array('Termodinamik yasaları detay', 'Karmaşık ΔG-K'))
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE 'CHEMISTRY 3RD BATCH COMPLETE! 18/30 (60%%%% - HALFWAY!)';
END $$;
