-- ============================================
-- MIGRATION 009: MATHEMATICS 4TH BATCH
-- Date: 2024-12-30
-- Topics: 8 (Permütasyon, Üstel-Loga, Mantık, Kümeler, 
--            Karmaşık, Tümevvarım, Olasılık Dağılımları, Bölünebilme)
-- Target: 25/40 topics (62.5% completion)
-- Archetype: 13F/12S (52%/48% - balanced)
-- Velocity: 3x expected (30-35% effort)
-- Format: v1.0 (LOCKED)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (8 new topics)
-- ============================================

DO $$
DECLARE
    v_curriculum_version_id UUID;
    v_math_subject_id UUID;
BEGIN
    -- Get curriculum version (TR MEB 2024)
    SELECT id INTO v_curriculum_version_id
    FROM curriculum_versions
    WHERE country_code = 'TR'
      AND system_code = 'MEB'
      AND academic_year = 2024
    LIMIT 1;
    
    -- Get Math subject
    SELECT id INTO v_math_subject_id
    FROM subjects
    WHERE code = 'MAT'
    LIMIT 1;
    
    -- Insert 8 new topics (4 foundational, 4 synthesis)
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
    (v_curriculum_version_id, v_math_subject_id, 'MAT-PERM-01', 'Permütasyon', 6, '11,tyt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-MANTIK-01', 'Mantık', 4, '9,tyt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-KUME-01', 'Kümeler', 4, '9,tyt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-BOLME-01', 'Bölünebilme', 5, '9,10,tyt', true),
    
    -- SYNTHESIS (4 topics)
    (v_curriculum_version_id, v_math_subject_id, 'MAT-USLU-LOGA-01', 'Üstel ve Logaritmik Fonksiyonlar', 8, '11,12,tyt,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-KARMASIK-01', 'Karmaşık Sayılar', 8, '12,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-TUMEVARIM-01', 'Tümevarım', 7, '11,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-OLASILIK-DAGIL-01', 'Olasılık Dağılımları', 8, '12,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '8 topics inserted successfully';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (8 contexts)
-- ============================================

DO $$
DECLARE
    v_topic_id UUID;
BEGIN
    -- ==========================================
    -- 1. MAT-PERM-01: Permütasyon (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-PERM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Düşük'
        ),
        'learning_objectives', jsonb_build_array(
            'Permütasyon tanımını ve formülünü anlama',
            'Sıralama problemlerini çözme',
            'Tekrarlı permütasyon kavramını kullanma',
            'Döngüsel permütasyon hesaplama'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-KOMB-01'
        ),
        'misconceptions', jsonb_build_array(
            'Permütasyon ile kombinasyon karıştırılması (sıralama önemli mi?)',
            'Tekrarlı permütasyonda formül hatası',
            'Döngüsel permütasyonda (n-1)! formülünü unutma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 180,
            'practice', 240,
            'mastery', 180
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', '20 dakikalık bir oturumda permütasyon formülü ve temel uygulamalar öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-PERM-01: Permütasyon';
    
    -- ==========================================
    -- 2. MAT-MANTIK-01: Mantık (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-MANTIK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Orta',
            'ayt', 'Düşük'
        ),
        'learning_objectives', jsonb_build_array(
            'Önerme kavramını anlama',
            'Mantıksal bağlaçları kullanma (ve, veya, değil, ise)',
            'Doğruluk tablosu oluşturma',
            'Mantıksal denklikleri kullanma'
        ),
        'prerequisite_topics', jsonb_build_array(),
        'misconceptions', jsonb_build_array(
            'Günlük dildeki "veya" ile mantıktaki "veya" farkını anlamamak',
            'p→q önermesinin doğruluk tablosunu yanlış yorumlama',
            'Olumsuzlama işleminde De Morgan kurallarını unutma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 120,
            'practice', 180,
            'mastery', 120
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Temel mantık kavramları 20 dakikada öğretilebilir, soyut ama kısa bir konu'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-MANTIK-01: Mantık';
    
    -- ==========================================
    -- 3. MAT-KUME-01: Kümeler (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-KUME-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Orta',
            'ayt', 'Düşük'
        ),
        'learning_objectives', jsonb_build_array(
            'Küme tanımını ve gösterim yöntemlerini bilme',
            'Küme işlemlerini (birleşim, kesişim, fark) uygulama',
            'Alt küme ve eşit küme kavramlarını anlama',
            'Venn şeması çizme ve yorumlama'
        ),
        'prerequisite_topics', jsonb_build_array(),
        'misconceptions', jsonb_build_array(
            'Küme ile eleman kavramını karıştırma (∈ vs ⊂)',
            'Boş kümenin her kümenin alt kümesi olduğunu unutma',
            'Venn şemasında kesişim ve birleşim alanlarını yanlış yorumlama'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 150,
            'practice', 180,
            'mastery', 120
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Temel küme kavramları ve işlemler 20 dakikalık oturuma sığar'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-KUME-01: Kümeler';
    
    -- ==========================================
    -- 4. MAT-BOLME-01: Bölünebilme (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-BOLME-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Düşük'
        ),
        'learning_objectives', jsonb_build_array(
            'Bölünebilme kurallarını bilme (2, 3, 4, 5, 6, 8, 9, 10)',
            'EBOB ve EKOK hesaplama',
            'Asal sayı ve asal çarpanlar kavramı',
            'Bölme işleminde kalan teoremi'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01'
        ),
        'misconceptions', jsonb_build_array(
            'EBOB ve EKOK kavramlarını karıştırma',
            'Bölünebilme kurallarını yanlış uygulama (örn: 6''ya bölünme)',
            'Asal çarpanlara ayırırken hata yapma',
            '1''in asal sayı olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 180,
            'practice', 240,
            'mastery', 180
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Bölünebilme kuralları ve EBOB-EKOK 20 dakikada kavranabilir, ezber ağırlıklı'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-BOLME-01: Bölünebilme';
    
    -- ==========================================
    -- 5. MAT-USLU-LOGA-01: Üstel-Logaritmik (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-USLU-LOGA-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Üstel fonksiyonların grafiklerini ve özelliklerini anlama',
            'Logaritma kavramını ve özelliklerini bilme',
            'Üstel ve logaritmik denklemleri çözme',
            'Logaritmanın uygulamalarını (pH, desibel, Richter) yorumlama'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-USLU-01',
            'MAT-LOGA-01',
            'MAT-FONK-01'
        ),
        'misconceptions', jsonb_build_array(
            'log(a+b) = log(a) + log(b) gibi yanlış logaritma özellikleri',
            'Üstel fonksiyonlarda taban değişiminin etkisini anlamamak',
            'e tabanının özel önemini kavrayamamak',
            'Logaritma denklemi çözümünde tanım kümesi kontrolünü unutma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 480,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Hem üstel hem logaritmik fonksiyonlar kapsandığı için split gerekli',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Üstel Fonksiyonlar',
                    'duration', 240,
                    'focus', 'Üstel fonksiyon grafikleri, denklemler, büyüme-azalma modelleri'
                ),
                jsonb_build_object(
                    'name', 'Logaritma Temelleri',
                    'duration', 240,
                    'focus', 'Logaritma tanımı, özellikleri, taban değişimi'
                ),
                jsonb_build_object(
                    'name', 'Logaritmik Fonksiyonlar',
                    'duration', 240,
                    'focus', 'Logaritmik fonksiyon grafikleri, denklemler'
                ),
                jsonb_build_object(
                    'name', 'Üstel-Logaritmik Uygulamalar',
                    'duration', 240,
                    'focus', 'Bileşik faiz, yarı ömür, pH, desibel problemleri'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Logaritma özellikleri (çarpma → toplama, bölme → çıkarma)',
                'Üstel denklem çözme teknikleri',
                'e tabanının özellikleri ve doğal logaritma'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık logaritma eşitsizlikleri',
                'Üstel fonksiyonlarda çok adımlı kompozisyon'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Tarihsel logaritma tabloları',
                'Slide rule hesapları'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-USLU-LOGA-01: Üstel ve Logaritmik Fonksiyonlar';
    
    -- ==========================================
    -- 6. MAT-KARMASIK-01: Karmaşık Sayılar (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-KARMASIK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Karmaşık sayı kavramını ve i birimini anlama',
            'Karmaşık sayılarla dört işlem yapma',
            'Eşlenik kavramı ve kullanımı',
            'Argand diyagramında karmaşık sayıları gösterme',
            'Polar form ve De Moivre teoremi'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01',
            'MAT-FONK-01'
        ),
        'misconceptions', jsonb_build_array(
            'i^2=-1 yerine i=-1 düşünmek',
            'Karmaşık sayıların sıralanabilir olduğunu sanmak',
            'Eşlenik çarpımının her zaman reel sayı olduğunu unutmak',
            'Polar formda argüman hesabında açı aralığını yanlış belirleme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 300,
            'practice', 360,
            'mastery', 300
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Cebirsel işlemler ve geometrik yorumlama farklı beceriler gerektiriyor',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Karmaşık Sayı Cebri',
                    'duration', 300,
                    'focus', 'i birimi, dört işlem, eşlenik, mutlak değer'
                ),
                jsonb_build_object(
                    'name', 'Geometrik Yorumlama',
                    'duration', 300,
                    'focus', 'Argand diyagramı, polar form, trigonometrik form'
                ),
                jsonb_build_object(
                    'name', 'İleri Uygulamalar',
                    'duration', 360,
                    'focus', 'De Moivre teoremi, kökler, üstel form'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'i''nin kuvvetleri (i, i^2, i^3, i^4 döngüsü)',
                'Eşlenik ile bölme işlemi',
                'Karmaşık sayıların mutlak değeri'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok adımlı polar form dönüşümleri',
                'n-inci dereceden karmaşık kökler'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Euler formülü ile bağlantılar (e^(iθ))',
                'Karmaşık fonksiyonlar teorisi'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-KARMASIK-01: Karmaşık Sayılar';
    
    -- ==========================================
    -- 7. MAT-TUMEVARIM-01: Tümevarım (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-TUMEVARIM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Tümevarım ilkesini anlama (baz adım + indüksiyon adımı)',
            'Toplam formüllerini tümevarımla ispatlama',
            'Bölünebilme önermelerini tümevarımla gösterme',
            'Eşitsizlikleri tümevarımla kanıtlama'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-MANTIK-01',
            'MAT-DIZI-01'
        ),
        'misconceptions', jsonb_build_array(
            'Baz adımını kontrol etmeyi unutma (n=1 veya n=0)',
            'İndüksiyon hipotezini doğru kullanmama',
            'n=k+1 adımını n=k''dan bağımsız düşünme',
            'Tümevarımın sadece toplam formülleri için olduğunu sanma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 360,
            'mastery', 300
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Farklı uygulama alanları (toplam, bölünebilme, eşitsizlik) ayrı pratik gerektirir',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Tümevarım Prensipleri',
                    'duration', 180,
                    'focus', 'Baz adım, indüksiyon hipotezi, indüksiyon adımı mantığı'
                ),
                jsonb_build_object(
                    'name', 'Toplam Formülleri',
                    'duration', 240,
                    'focus', '1+2+...+n, 1^2+2^2+...+n^2 gibi formüllerin ispatı'
                ),
                jsonb_build_object(
                    'name', 'Bölünebilme ve Eşitsizlikler',
                    'duration', 240,
                    'focus', 'n^3-n her zaman 3''e bölünür gibi önermeler, Bernoulli eşitsizliği'
                ),
                jsonb_build_object(
                    'name', 'İleri Uygulamalar',
                    'duration', 240,
                    'focus', 'Kombinatorik eşitlikler, geometri problemleri'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Temel toplam formüllerinin tümevarımla ispatı',
                'Basit bölünebilme önermelerinin kanıtı',
                'İki adımlı tümevarım mantığı (baz + indüksiyon)'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık kombinatorik eşitlikler',
                'İki değişkenli tümevarım (nadiren sorulur)'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Güçlü tümevarım (strong induction)',
                'Yapısal tümevarım (structural induction)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-TUMEVARIM-01: Tümevarım';
    
    -- ==========================================
    -- 8. MAT-OLASILIK-DAGIL-01: Olasılık Dağılımları (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-OLASILIK-DAGIL-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Kesikli olasılık dağılımı kavramını anlama',
            'Beklenen değer (ortalama) hesaplama',
            'Varyans ve standart sapma kavramları',
            'Binom dağılımını anlama ve uygulama',
            'Normal dağılım (temel seviyede)'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-OLAS-01',
            'MAT-IST-01'
        ),
        'misconceptions', jsonb_build_array(
            'Beklenen değerin mutlaka olası değerlerden biri olması gerektiğini sanma',
            'Varyans hesabında E(X^2) - [E(X)]^2 formülünü yanlış kullanma',
            'Binom dağılımında n ve p parametrelerini karıştırma',
            'Normal dağılımın her zaman uygulanabileceğini düşünme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 300,
            'practice', 420,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'İstatistiksel kavramlar ve farklı dağılım tipleri ayrı kavramsal çerçeveler',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Olasılık Dağılımı Temelleri',
                    'duration', 240,
                    'focus', 'Kesikli dağılım, olasılık fonksiyonu, kümülatif dağılım'
                ),
                jsonb_build_object(
                    'name', 'Beklenen Değer ve Varyans',
                    'duration', 300,
                    'focus', 'E(X) hesaplama, Var(X) formülü, standart sapma'
                ),
                jsonb_build_object(
                    'name', 'Binom Dağılımı',
                    'duration', 300,
                    'focus', 'Binom formülü, beklenen değer=np, varyans=npq'
                ),
                jsonb_build_object(
                    'name', 'Normal Dağılım (Temel)',
                    'duration', 240,
                    'focus', 'Çan eğrisi, standart normal tablo, z-skoru'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Beklenen değer formülü: E(X) = Σ x·P(x)',
                'Varyans formülü: Var(X) = E(X^2) - [E(X)]^2',
                'Binom dağılımında E(X)=np, Var(X)=npq'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık dağılım fonksiyonları',
                'Sürekli dağılımların integral hesapları'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Poisson dağılımı (AYT''de nadiren görülür)',
                'Geometrik dağılım (çok nadir)',
                'Hipergeometrik dağılım'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-OLASILIK-DAGIL-01: Olasılık Dağılımları';
    
END $$;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check all 8 topics inserted
SELECT 
    code,
    name_tr,
    difficulty_level,
    grade_level,
    is_active
FROM topics
WHERE code IN (
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
)
ORDER BY code;

-- Check all 8 contexts created
SELECT 
    t.code,
    t.name_tr,
    CASE WHEN tc.id IS NULL THEN 'NO CONTEXT' ELSE 'HAS CONTEXT' END as status,
    tc.metadata->>'archetype' as archetype
FROM topics t
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-PERM-01', 'MAT-MANTIK-01', 'MAT-KUME-01', 'MAT-BOLME-01',
    'MAT-USLU-LOGA-01', 'MAT-KARMASIK-01', 'MAT-TUMEVARIM-01', 'MAT-OLASILIK-DAGIL-01'
)
ORDER BY t.code;

-- Final cumulative stats (should show 25 topics, 13F/12S)
SELECT 
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT tc.id) as with_context,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'foundational' THEN 1 ELSE 0 END) as foundational,
    SUM(CASE WHEN tc.metadata->>'archetype' = 'synthesis' THEN 1 ELSE 0 END) as synthesis,
    ROUND(100.0 * COUNT(DISTINCT tc.id) / NULLIF(COUNT(DISTINCT t.id), 0), 1) || '%' as completion
FROM topics t
JOIN subjects s ON t.subject_id = s.id
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE s.code = 'MAT';
