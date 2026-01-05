-- ============================================
-- MIGRATION 023: BIOLOGY 1ST BATCH
-- Date: 2024-12-31
-- Topics: 5 (Hücre, Bölünme, Kalıtım, DNA, Ekosistem)
-- Target: 5/20 topics (25%% Biology kickoff!)
-- Archetype: 4F/1S (80%%/20%% - Foundation phase)
-- Velocity: 3.7x sustained (3 subjects proven!)
-- Format: v1.0 (REUSED - bulletproof!)
-- ============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_biology_subject_id UUID;
BEGIN
    SELECT id INTO v_curriculum_version_id
    FROM curriculum_versions
    WHERE country_code = 'TR' AND system_code = 'MEB' AND academic_year = 2024
    LIMIT 1;
    
    SELECT id INTO v_biology_subject_id
    FROM subjects WHERE code = 'BIO' LIMIT 1;
    
    INSERT INTO topics (
        curriculum_version_id, subject_id, code, name_tr,
        difficulty_level, grade_level, is_active
    ) VALUES
    -- FOUNDATIONAL (4)
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-HUCRE-01', 'Hücre Yapısı ve Organeller', 5, '9,tyt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-BOLUNME-01', 'Hücre Bölünmesi (Mitoz-Mayoz)', 6, '9,10,tyt,ayt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-KALITIM-01', 'Kalıtım ve Mendel Yasaları', 6, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-DNA-01', 'DNA, RNA ve Protein Sentezi', 7, '11,ayt', true),
    
    -- SYNTHESIS (1)
    (v_curriculum_version_id, v_biology_subject_id, 'BIO-EKOSISTEM-01', 'Ekosistem ve Ekoloji', 6, '9,10,tyt,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '5 Biology topics (4F + 1S) inserted - KICKOFF!';
END $$;

DO $$
DECLARE v_topic_id UUID;
BEGIN
    -- ==========================================
    -- FOUNDATIONAL TOPICS (4)
    -- ==========================================
    
    -- 1. BIO-HUCRE-01: Hücre Yapısı
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-HUCRE-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Prokariot ve ökariot hücre farkları',
            'Hücre organelleri (çekirdek, mitokondri, ribozom, ER, golgi)',
            'Hücre zarı ve geçirgenlik',
            'Osmoz ve difüzyon',
            'Hücresel solunum temelleri'
        ),
        'prerequisite_topics', jsonb_build_array(),
        'misconceptions', jsonb_build_array(
            'Tüm hücrelerin çekirdeği olduğunu sanma (prokaryotlarda yok)',
            'Bitki hücresiyle hayvan hücresinin aynı olduğunu sanma (kloroplast, hücre duvarı)',
            'Mitokondrinin sadece enerji depoladığını sanma (üretir)',
            'Hücre zarının geçirgenliğinin her madde için aynı olduğunu sanma',
            'Osmozun sadece suda olduğunu sanma (çözeltilerde de)'
        ),
        'time_estimate', jsonb_build_object('foundation', 240, 'practice', 300, 'mastery', 180),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Hücre yapısı temelleri 20-25 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 2. BIO-BOLUNME-01: Hücre Bölünmesi
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-BOLUNME-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Mitoz bölünme evreleri (profaz, metafaz, anafaz, telofaz)',
            'Mayoz bölünme ve eşey hücresi oluşumu',
            'Mitoz ile mayoz arasındaki farklar',
            'Kromozom, kromatit, homolog kromozom kavramları',
            'Krossing-over ve genetik çeşitlilik'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-HUCRE-01'),
        'misconceptions', jsonb_build_array(
            'Mitoz ile mayozun aynı olduğunu sanma (farklı amaçlar)',
            'Mayozda kromozom sayısının yarıya inmediğini sanma (iner)',
            'Krossing-over''ın mitozda olduğunu sanma (sadece mayoz)',
            'Hücre bölünmesinin sadece üreme için olduğunu sanma (büyüme, onarım)',
            'Profaz-metafaz-anafaz-telofaz sırasını karıştırma'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 330, 'mastery', 240),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Mitoz ve mayoz temelleri 25-30 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 3. BIO-KALITIM-01: Kalıtım
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-KALITIM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Çok Yüksek', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Mendel yasaları (baskınlık, ayrılma, bağımsız dağılım)',
            'Genotip ve fenotip kavramları',
            'Homozigot ve heterozigot',
            'Punnet karesi kullanımı',
            'Monohibrit ve dihibrit çaprazlamalar'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-BOLUNME-01'),
        'misconceptions', jsonb_build_array(
            'Baskın karakterin her zaman çoğunlukta olduğunu sanma (frekans farklı)',
            'Genotiple fenotipin aynı olduğunu sanma',
            'Çekinik karakterin kaybolduğunu sanma (gizli kalır)',
            'Tüm özelliklerin Mendel yasalarına uyduğunu sanma (istisnalar var)',
            'Dihibrit çaprazlamada 9:3:3:1 oranının her zaman çıktığını sanma'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 360, 'mastery', 270),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Mendel kalıtımı ve çaprazlamalar 25-30 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- 4. BIO-DNA-01: DNA ve Protein Sentezi
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-DNA-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Orta', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'DNA yapısı (çift sarmal, nükleotit)',
            'DNA replikasyonu',
            'RNA türleri (mRNA, tRNA, rRNA)',
            'Transkripsiyon (DNA → RNA)',
            'Translasyon (RNA → Protein)'
        ),
        'prerequisite_topics', jsonb_build_array('BIO-HUCRE-01'),
        'misconceptions', jsonb_build_array(
            'DNA ile RNA''nın aynı olduğunu sanma (timinin yerine urasil)',
            'Protein sentezinin sadece çekirdekte olduğunu sanma (ribozomda)',
            'Her hücrenin aynı proteinleri ürettiğini sanma (farklılaşma)',
            'Transkripsiyon ile translasyonu karıştırma',
            'Kodon ile antikodon''u karıştırma'
        ),
        'time_estimate', jsonb_build_object('foundation', 300, 'practice', 360, 'mastery', 270),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'DNA yapısı ve protein sentezi temelleri 25-30 dakikada öğretilebilir'
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    -- ==========================================
    -- SYNTHESIS TOPIC (1)
    -- ==========================================
    
    -- 5. BIO-EKOSISTEM-01: Ekosistem
    SELECT id INTO v_topic_id FROM topics WHERE code = 'BIO-EKOSISTEM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object('tyt', 'Yüksek', 'ayt', 'Çok Yüksek'),
        'learning_objectives', jsonb_build_array(
            'Ekosistemin bileşenleri (biyotik, abiyotik)',
            'Besin zincirleri ve besin ağları',
            'Enerji piramidi ve madde döngüsü',
            'Populasyon dinamikleri',
            'Habitat ve niş kavramları'
        ),
        'prerequisite_topics', jsonb_build_array(),
        'misconceptions', jsonb_build_array(
            'Besin zincirinin tek yönlü olduğunu sanma (ağ yapısı)',
            'Enerjinin döngü yaptığını sanma (tek yönlü akış)',
            'Maddenin kaybolduğunu sanma (döngü yapar)',
            'Piramit''in her zaman eşit büyüdüğünü sanma (küçülür)',
            'Habitat ile nişi karıştırma (yer vs görev)'
        ),
        'time_estimate', jsonb_build_object('foundation', 270, 'practice', 360, 'mastery', 270),
        'splitting', jsonb_build_object(
            'recommended', true,
            'parts', 4,
            'rationale', 'Ekosistem 4 kategoriye: Bileşenler, Besin İlişkileri, Enerji-Madde, Populasyon'
        ),
        'roi_guidance', jsonb_build_object(
            'high_roi_subtopics', jsonb_build_array('Besin zinciri (TYT klasik)', 'Enerji piramidi (mutlaka)', 'Basit populasyon (sık)'),
            'low_roi_subtopics', jsonb_build_array('Karmaşık besin ağı', 'Detaylı populasyon dinamikleri')
        )
    ))
    ON CONFLICT (topic_id) DO UPDATE SET metadata = EXCLUDED.metadata;
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'BIOLOGY 1ST BATCH COMPLETE!';
    RAISE NOTICE '5/20 topics (25%%%% - Foundation phase!)';
    RAISE NOTICE 'Balance: 4F/1S (80%%%%/20%%%%)';
    RAISE NOTICE 'Format v1.0 REUSED - 3 subjects proven!';
    RAISE NOTICE '==========================================';
    
END $$;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check all 5 topics inserted
SELECT 
    code, name_tr, difficulty_level, grade_level, is_active
FROM topics
WHERE code IN (
    'BIO-HUCRE-01', 'BIO-BOLUNME-01', 'BIO-KALITIM-01',
    'BIO-DNA-01', 'BIO-EKOSISTEM-01'
)
ORDER BY code;

-- Biology cumulative (should show 5 topics, 4F/1S)
SELECT 
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT tc.id) as with_context,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END) as foundational,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'synthesis' THEN 1 ELSE 0 END) as synthesis,
    ROUND(100.0 * SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END)::numeric / 
          NULLIF(COUNT(DISTINCT tc.id), 0), 1) || '%%' as foundational_pct,
    ROUND(100.0 * COUNT(DISTINCT tc.id) / 20.0, 1) || '%%' as completion_vs_target
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'BIO';
-- Expected: 5 topics, 4F, 1S, 80%% foundational, 25%% completion
