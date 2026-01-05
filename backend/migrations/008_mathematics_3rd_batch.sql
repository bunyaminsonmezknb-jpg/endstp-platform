-- ============================================
-- MIGRATION 008: Mathematics Context Layer - 3rd Batch (FIXED)
-- Date: 2024-12-30
-- Topics: 7 (İntegral, Analitik Geometri, Kombinatorik, Olasılık, İstatistik, Vektörler, Matrisler)
-- Archetype Distribution: 4 foundational, 3 synthesis
-- Status: READY FOR DEPLOYMENT
-- ============================================

-- FIX: format_version is inside metadata JSONB, not a separate column

-- ============================================
-- TOPIC 1: İntegral (SYNTHESIS)
-- ============================================

INSERT INTO topic_contexts (topic_id, metadata)
SELECT 
    t.id,
    jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'cognitive_level', 'analysis',
        'learning_objectives', jsonb_build_array(
            'Belirsiz integrali anlama ve hesaplama',
            'Belirli integral ile alan hesabı yapabilme',
            'İntegral yöntemlerini (değişken değiştirme, kısmi) uygulama',
            'İntegral-türev ilişkisini kavrama'
        ),
        'prerequisites', jsonb_build_array(
            'MAT-TUREV-01',
            'MAT-FONK-01',
            'MAT-LIMIT-01'
        ),
        'tags', jsonb_build_array(
            'calculus',
            'AYT',
            'integration',
            'area_calculation',
            'antiderivative'
        ),
        'splitting_guidance', jsonb_build_object(
            'recommended', true,
            'reasoning', 'İntegral çok geniş: belirsiz, belirli, yöntemler ayrı ayrı ölçülmeli',
            'suggested_splits', jsonb_build_array(
                'Belirsiz integral (temel formüller)',
                'Belirli integral (alan hesabı)',
                'İntegral yöntemleri (değişken değiştirme, kısmi)',
                'Uygulamalar (hacim, yol)'
            ),
            'roi_notes', jsonb_build_object(
                'high_roi', jsonb_build_array(
                    'Temel belirsiz integral formülleri',
                    'Alan hesabı (belirli integral)'
                ),
                'medium_roi', jsonb_build_array(
                    'Değişken değiştirme yöntemi',
                    'Kısmi integral'
                )
            )
        ),
        'measurement_notes', jsonb_build_object(
            '20min_suitable', false,
            'suitable_for', 'Temel belirsiz integral formülleri',
            'challenging_for', 'Kısmi integral ve karmaşık uygulamalar',
            'time_allocation', 'Belirsiz: 8dk, Belirli: 12dk, Yöntemler: 15dk+'
        ),
        'exam_context', jsonb_build_object(
            'frequency', 'Çok Yüksek',
            'difficulty_range', '6-9',
            'typical_question_count', '3-4 soru (AYT)'
        ),
        'common_mistakes', jsonb_build_array(
            'Sabit c eklemeyi unutma',
            'İntegral sınırlarını ters çevirme',
            'Değişken değiştirmede sınır güncelleme hatası'
        )
    )
FROM topics t
WHERE t.code = 'MAT-INT-01';

-- ============================================
-- TOPIC 2: Analitik Geometri (SYNTHESIS)
-- ============================================

INSERT INTO topic_contexts (topic_id, metadata)
SELECT 
    t.id,
    jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'cognitive_level', 'application',
        'learning_objectives', jsonb_build_array(
            'Koordinat sisteminde doğru ve çember denklemleri yazabilme',
            'İki doğru arasındaki açı ve uzaklık hesabı',
            'Parabol, elips, hiperbol temel özelliklerini bilme',
            'Geometrik problemleri analitik yöntemle çözme'
        ),
        'prerequisites', jsonb_build_array(
            'MAT-FONK-01',
            'MAT-TEMEL-01'
        ),
        'tags', jsonb_build_array(
            'geometry',
            'TYT',
            'AYT',
            'coordinate_system',
            'conic_sections',
            'distance_formula'
        ),
        'splitting_guidance', jsonb_build_object(
            'recommended', true,
            'reasoning', 'Doğru, çember, konikler ayrı konseptler',
            'suggested_splits', jsonb_build_array(
                'Doğru denklemi (y=mx+n, genel form)',
                'Çember denklemi',
                'Uzaklık formülleri (nokta-doğru, nokta-nokta)',
                'Konik kesitler (parabol, elips, hiperbol)'
            ),
            'roi_notes', jsonb_build_object(
                'high_roi', jsonb_build_array(
                    'Doğru denklemi yazma',
                    'Çember merkez ve yarıçap bulma',
                    'Uzaklık formülü'
                ),
                'medium_roi', jsonb_build_array(
                    'İki doğrunun kesişimi',
                    'Parabol özellikleri'
                )
            )
        ),
        'measurement_notes', jsonb_build_object(
            '20min_suitable', false,
            'suitable_for', 'Doğru ve çember denklemi',
            'challenging_for', 'Konik kesitler ve ileri geometri',
            'time_allocation', 'Doğru: 10dk, Çember: 10dk, Konikler: 15dk+'
        ),
        'exam_context', jsonb_build_object(
            'frequency', 'Yüksek',
            'difficulty_range', '5-8',
            'typical_question_count', '2-3 soru (TYT+AYT)'
        ),
        'common_mistakes', jsonb_build_array(
            'Doğru eğimi yanlış hesaplama',
            'Çember denkleminde (x-a)² işareti karıştırma',
            'Uzaklık formülünde karekök unutma'
        )
    )
FROM topics t
WHERE t.code = 'MAT-GEO-01';

-- ============================================
-- TOPIC 3: Kombinatorik (FOUNDATIONAL)
-- ============================================

INSERT INTO topic_contexts (topic_id, metadata)
SELECT 
    t.id,
    jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'cognitive_level', 'application',
        'learning_objectives', jsonb_build_array(
            'Permütasyon ve kombinasyon farkını anlama',
            'Faktöriyel işlemlerini yapabilme',
            'Sayma problemlerini doğru yöntemle çözme',
            'Tekrarlı/tekrarsız durumları ayırt etme'
        ),
        'prerequisites', jsonb_build_array(),
        'tags', jsonb_build_array(
            'counting',
            'TYT',
            'permutation',
            'combination',
            'factorial'
        ),
        'splitting_guidance', jsonb_build_object(
            'recommended', false,
            'reasoning', 'Kombinatorik tek bir konsept: sayma yöntemleri. Bölmek gereksiz.',
            'unified_assessment_preferred', true
        ),
        'measurement_notes', jsonb_build_object(
            '20min_suitable', true,
            'suitable_for', 'Tüm kombinatorik: permütasyon, kombinasyon, faktöriyel',
            'challenging_for', null,
            'time_allocation', '20 dakika yeterli (8-10 soru)'
        ),
        'exam_context', jsonb_build_object(
            'frequency', 'Yüksek',
            'difficulty_range', '4-7',
            'typical_question_count', '2-3 soru (TYT)'
        ),
        'common_mistakes', jsonb_build_array(
            'Permütasyon-kombinasyon karıştırma',
            'Tekrarlı/tekrarsız durumu yanlış belirleme',
            'Faktöriyel sadeleştirmede hata'
        )
    )
FROM topics t
WHERE t.code = 'MAT-KOMB-01';

-- ============================================
-- TOPIC 4: Olasılık (SYNTHESIS)
-- ============================================

INSERT INTO topic_contexts (topic_id, metadata)
SELECT 
    t.id,
    jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'cognitive_level', 'analysis',
        'learning_objectives', jsonb_build_array(
            'Basit ve bileşik olayların olasılığını hesaplama',
            'Bağımlı ve bağımsız olayları ayırt etme',
            'Koşullu olasılık hesabı yapabilme',
            'Kombinatorik bilgisini olasılıkta kullanma'
        ),
        'prerequisites', jsonb_build_array(
            'MAT-KOMB-01'
        ),
        'tags', jsonb_build_array(
            'probability',
            'TYT',
            'AYT',
            'conditional_probability',
            'independent_events'
        ),
        'splitting_guidance', jsonb_build_object(
            'recommended', true,
            'reasoning', 'Basit olasılık vs koşullu olasılık farklı zorluk seviyeleri',
            'suggested_splits', jsonb_build_array(
                'Basit olasılık (P(A), P(B), toplama kuralı)',
                'Bağımsız olaylar (çarpma kuralı)',
                'Koşullu olasılık (P(A|B))',
                'Bayes teoremi (ileri seviye)'
            ),
            'roi_notes', jsonb_build_object(
                'high_roi', jsonb_build_array(
                    'Basit olasılık hesabı',
                    'Bağımsız olaylar çarpma kuralı'
                ),
                'medium_roi', jsonb_build_array(
                    'Koşullu olasılık',
                    'Toplama ve çıkarma kuralları'
                )
            )
        ),
        'measurement_notes', jsonb_build_object(
            '20min_suitable', false,
            'suitable_for', 'Basit olasılık ve bağımsız olaylar',
            'challenging_for', 'Koşullu olasılık ve Bayes',
            'time_allocation', 'Basit: 10dk, Bağımsız: 8dk, Koşullu: 15dk+'
        ),
        'exam_context', jsonb_build_object(
            'frequency', 'Çok Yüksek',
            'difficulty_range', '5-9',
            'typical_question_count', '2-4 soru (TYT+AYT)'
        ),
        'common_mistakes', jsonb_build_array(
            'Bağımlı-bağımsız olay karıştırma',
            'Koşullu olasılıkta pay-payda ters yazma',
            'Kombinatorik ile olasılığı birleştirirken hata'
        )
    )
FROM topics t
WHERE t.code = 'MAT-OLAS-01';

-- ============================================
-- TOPIC 5: İstatistik (FOUNDATIONAL)
-- ============================================

INSERT INTO topic_contexts (topic_id, metadata)
SELECT 
    t.id,
    jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'cognitive_level', 'comprehension',
        'learning_objectives', jsonb_build_array(
            'Ortalama, medyan, mod kavramlarını anlama',
            'Veri setini grafiklerle yorumlama',
            'Standart sapma ve varyans hesabı',
            'Histogram, kutu grafiği okuma'
        ),
        'prerequisites', jsonb_build_array(),
        'tags', jsonb_build_array(
            'statistics',
            'TYT',
            'mean',
            'median',
            'standard_deviation',
            'data_analysis'
        ),
        'splitting_guidance', jsonb_build_object(
            'recommended', false,
            'reasoning', 'İstatistik temel konseptler: ortalama, medyan, sapma. Tek seferde ölçülmeli.',
            'unified_assessment_preferred', true
        ),
        'measurement_notes', jsonb_build_object(
            '20min_suitable', true,
            'suitable_for', 'Tüm istatistik: ortalama, medyan, mod, sapma, grafikler',
            'challenging_for', null,
            'time_allocation', '20 dakika yeterli (8-10 soru)'
        ),
        'exam_context', jsonb_build_object(
            'frequency', 'Orta',
            'difficulty_range', '3-6',
            'typical_question_count', '1-2 soru (TYT)'
        ),
        'common_mistakes', jsonb_build_array(
            'Ortalama hesabında toplam değeri yanlış bulma',
            'Medyan için sıralama yapmayı unutma',
            'Standart sapma formülünde işaret hatası'
        )
    )
FROM topics t
WHERE t.code = 'MAT-IST-01';

-- ============================================
-- TOPIC 6: Vektörler (FOUNDATIONAL)
-- ============================================

INSERT INTO topic_contexts (topic_id, metadata)
SELECT 
    t.id,
    jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'cognitive_level', 'application',
        'learning_objectives', jsonb_build_array(
            'Vektör tanımı ve gösterimi',
            'Vektör toplama ve çıkarma işlemleri',
            'Skaler çarpım ve vektörel çarpım',
            'Birim vektör ve vektör büyüklüğü hesabı'
        ),
        'prerequisites', jsonb_build_array(
            'MAT-GEO-01'
        ),
        'tags', jsonb_build_array(
            'vectors',
            'AYT',
            'dot_product',
            'magnitude',
            'unit_vector'
        ),
        'splitting_guidance', jsonb_build_object(
            'recommended', false,
            'reasoning', 'Vektör işlemleri birbiriyle ilişkili, tek seferde ölçülmeli',
            'unified_assessment_preferred', true
        ),
        'measurement_notes', jsonb_build_object(
            '20min_suitable', true,
            'suitable_for', 'Tüm vektör işlemleri: toplama, çıkarma, skaler çarpım',
            'challenging_for', null,
            'time_allocation', '20 dakika yeterli (6-8 soru)'
        ),
        'exam_context', jsonb_build_object(
            'frequency', 'Orta',
            'difficulty_range', '5-7',
            'typical_question_count', '1-2 soru (AYT)'
        ),
        'common_mistakes', jsonb_build_array(
            'Vektör toplama yön hatası',
            'Skaler çarpım ile vektörel çarpım karıştırma',
            'Birim vektör hesabında büyüklük hatası'
        )
    )
FROM topics t
WHERE t.code = 'MAT-VEK-01';

-- ============================================
-- TOPIC 7: Matrisler (FOUNDATIONAL)
-- ============================================

INSERT INTO topic_contexts (topic_id, metadata)
SELECT 
    t.id,
    jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'cognitive_level', 'application',
        'learning_objectives', jsonb_build_array(
            'Matris tanımı ve gösterimi',
            'Matris toplama ve çıkarma işlemleri',
            'Matris çarpımı kuralları',
            'Determinant ve ters matris hesabı (2x2, 3x3)'
        ),
        'prerequisites', jsonb_build_array(),
        'tags', jsonb_build_array(
            'matrices',
            'AYT',
            'determinant',
            'inverse_matrix',
            'matrix_operations'
        ),
        'splitting_guidance', jsonb_build_object(
            'recommended', false,
            'reasoning', 'Matris işlemleri temel bir bütün, parçalanmaz',
            'unified_assessment_preferred', true
        ),
        'measurement_notes', jsonb_build_object(
            '20min_suitable', true,
            'suitable_for', 'Tüm matris işlemleri: toplama, çarpım, determinant',
            'challenging_for', null,
            'time_allocation', '20 dakika yeterli (6-8 soru)'
        ),
        'exam_context', jsonb_build_object(
            'frequency', 'Orta',
            'difficulty_range', '4-7',
            'typical_question_count', '1-2 soru (AYT)'
        ),
        'common_mistakes', jsonb_build_array(
            'Matris çarpımında satır-sütün kuralını unutma',
            'Determinant hesabında işaret hatası',
            'Ters matris için determinant = 0 kontrolü yapmama'
        )
    )
FROM topics t
WHERE t.code = 'MAT-MATRIS-01';

-- ============================================
-- VERIFICATION (FIXED)
-- ============================================

DO $$
DECLARE
    v_inserted_count INT;
    v_foundational_count INT;
    v_synthesis_count INT;
    v_total_math_topics INT;
BEGIN
    -- Count newly inserted contexts
    SELECT COUNT(*) INTO v_inserted_count
    FROM topic_contexts tc
    JOIN topics t ON tc.topic_id = t.id
    WHERE t.code IN (
        'MAT-INT-01', 'MAT-GEO-01', 'MAT-KOMB-01', 'MAT-OLAS-01',
        'MAT-IST-01', 'MAT-VEK-01', 'MAT-MATRIS-01'
    );
    
    -- Count total math topics with contexts
    SELECT COUNT(*) INTO v_total_math_topics
    FROM topic_contexts tc
    JOIN topics t ON tc.topic_id = t.id
    WHERE t.code LIKE 'MAT-%';
    
    -- Count archetypes (all math topics)
    SELECT COUNT(*) INTO v_foundational_count
    FROM topic_contexts tc
    JOIN topics t ON tc.topic_id = t.id
    WHERE t.code LIKE 'MAT-%'
      AND tc.metadata->>'archetype' = 'foundational';
    
    SELECT COUNT(*) INTO v_synthesis_count
    FROM topic_contexts tc
    JOIN topics t ON tc.topic_id = t.id
    WHERE t.code LIKE 'MAT-%'
      AND tc.metadata->>'archetype' = 'synthesis';
    
    RAISE NOTICE '============================================';
    RAISE NOTICE 'MIGRATION 008: MATHEMATICS 3RD BATCH';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Inserted contexts: %', v_inserted_count;
    RAISE NOTICE 'Total math topics: %', v_total_math_topics;
    RAISE NOTICE 'Foundational: %', v_foundational_count;
    RAISE NOTICE 'Synthesis: %', v_synthesis_count;
    RAISE NOTICE '============================================';
    
    IF v_inserted_count = 7 AND v_total_math_topics = 17 THEN
        RAISE NOTICE '✅ 3RD BATCH: SUCCESS';
        RAISE NOTICE '✅ CUMULATIVE: 17 math topics (42.5%% complete)';
    ELSE
        RAISE NOTICE '⚠️  UNEXPECTED COUNT - CHECK DEPLOYMENT';
    END IF;
    
    RAISE NOTICE '============================================';
END $$;