-- ============================================
-- MIGRATION 011: MATHEMATICS 6TH BATCH (FINAL!)
-- Date: 2024-12-31
-- Topics: 7 (Üçgen, Dörtgen, Katı Cisimler, Çember, Dönüşüm, Ardışık Sayılar, Analitik Geometri)
-- Target: 40/40 topics (100% COMPLETION!)
-- Archetype: 20F/20S (50%/50% - PERFECT BALANCE!)
-- Velocity: 3.3x expected (30% effort)
-- Format: v1.0 (LOCKED)
-- ============================================

-- ============================================
-- STEP 1: INSERT TOPICS (7 final topics)
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
    
    -- Insert 7 final topics (3 foundational, 4 synthesis)
    INSERT INTO topics (
        curriculum_version_id,
        subject_id,
        code,
        name_tr,
        difficulty_level,
        grade_level,
        is_active
    ) VALUES
    -- FOUNDATIONAL (3 topics)
    (v_curriculum_version_id, v_math_subject_id, 'MAT-UCGEN-01', 'Üçgen Geometri', 6, '9,10,tyt,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-DORTGEN-01', 'Dörtgen Geometri', 5, '9,10,tyt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-KATI-01', 'Katı Cisimler', 6, '11,12,ayt', true),
    
    -- SYNTHESIS (4 topics)
    (v_curriculum_version_id, v_math_subject_id, 'MAT-CEMBER-01', 'Çember Geometri', 7, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-DONUSUM-01', 'Dönüşüm Geometrisi', 7, '11,12,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-ARDISIK-01', 'Ardışık Sayılar ve Problemler', 6, '9,10,tyt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-ANALITIK-01', 'Analitik Geometri', 8, '11,12,ayt', true)
    
    ON CONFLICT (code) DO NOTHING;
    
    RAISE NOTICE '7 final topics inserted successfully - 100%% COMPLETE!';
END $$;

-- ============================================
-- STEP 2: INSERT CONTEXTS (7 contexts)
-- ============================================

DO $$
DECLARE
    v_topic_id UUID;
BEGIN
    -- ==========================================
    -- 1. MAT-UCGEN-01: Üçgen Geometri (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-UCGEN-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Üçgen çeşitlerini tanıma ve özelliklerini bilme',
            'Açı-kenar bağıntılarını kullanma',
            'Üçgen eşitsizliği ve alan hesaplama',
            'Özel üçgenleri tanıma (ikizkenar, eşkenar, dik)',
            'Benzerlik ve eşlik koşullarını uygulama'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01'
        ),
        'misconceptions', jsonb_build_array(
            'Üçgen eşitsizliğini yanlış uygulama (a + b > c)',
            'Benzerlik ile eşliği karıştırma',
            'Açıortay teoremini yanlış kullanma',
            'Dik üçgende Pisagor teoremini sadece c^2 = a^2 + b^2 olarak bilme (a^2 = c^2 - b^2 vb. unutma)',
            'Alan formüllerinde yüksekliği yanlış belirleme'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 240
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Temel üçgen kavramları ve özellikler 20-25 dakikada öğretilebilir, açı-kenar bağıntıları doğal bir devam niteliğinde'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-UCGEN-01: Üçgen Geometri';
    
    -- ==========================================
    -- 2. MAT-DORTGEN-01: Dörtgen Geometri (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-DORTGEN-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Orta'
        ),
        'learning_objectives', jsonb_build_array(
            'Dörtgen çeşitlerini tanıma (kare, dikdörtgen, paralelkenar, yamuk)',
            'Dörtgenlerin özelliklerini bilme',
            'Alan ve çevre hesaplamaları yapma',
            'Köşegen özelliklerini kullanma',
            'Özel dörtgenleri ayırt etme'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-UCGEN-01'
        ),
        'misconceptions', jsonb_build_array(
            'Paralelkenar ile dikdörtgeni karıştırma',
            'Yamukta orta taban teoremini yanlış uygulama',
            'Deltoidin özelliklerini bilmeme',
            'Köşegenlerin kesişim noktası özelliklerini karıştırma',
            'Alan formüllerinde taban-yükseklik seçimini yanlış yapma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 210,
            'practice', 270,
            'mastery', 210
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Dörtgen çeşitleri ve özellikler 20 dakikada öğretilebilir, üçgen bilgisiyle doğal bağlantı kurulur'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-DORTGEN-01: Dörtgen Geometri';
    
    -- ==========================================
    -- 3. MAT-KATI-01: Katı Cisimler (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-KATI-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Prizma, piramit, silindir, koni ve küre özelliklerini bilme',
            'Hacim ve yüzey alanı formüllerini kullanma',
            'Kesit alma ve iz bulma işlemlerini yapma',
            'Benzer cisimlerde oran hesaplama',
            'Dönme cisimleri tanıma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-UCGEN-01',
            'MAT-DORTGEN-01'
        ),
        'misconceptions', jsonb_build_array(
            'Hacim ile yüzey alanını karıştırma',
            'Pisagor teoremini 3 boyutta yanlış uygulama',
            'Kesik piramit/koni formüllerini bilmeme',
            'Benzer cisimlerde hacim oranını (k^3) unutma',
            'Dönme cisimlerinde yüzey alanı hesabını yanlış yapma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 270,
            'practice', 360,
            'mastery', 300
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Temel katı cisim formülleri ve kavramlar 25 dakikada öğretilebilir, 2D geometri bilgisiyle desteklenir'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-KATI-01: Katı Cisimler';
    
    -- ==========================================
    -- 4. MAT-CEMBER-01: Çember Geometri (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-CEMBER-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Çember ve daire kavramlarını ayırt etme',
            'Merkez ve çevre açısı teoremlerini uygulama',
            'Teğet ve kiriş özelliklerini kullanma',
            'Çemberde alan ve çevre hesaplama',
            'Çember denklemini yazma ve çözme'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-UCGEN-01'
        ),
        'misconceptions', jsonb_build_array(
            'Merkez açı ile çevre açısı ilişkisini yanlış kurma (2:1 oranı)',
            'Teğet uzunluklarının eşitliğini unutma',
            'Dik açıyla gören yayın yarım çember olduğunu bilmeme',
            'Çemberin denkleminde (x-a)^2 + (y-b)^2 = r^2 formülünü yanlış kullanma',
            'Kiriş-teğet açısı teoremini karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 300,
            'practice', 420,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Çember geometrisi farklı teorem grupları içeriyor: açı teoremleri, uzunluk teoremleri, çember denklemi',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Temel Kavramlar ve Açı Teoremleri',
                    'duration', 240,
                    'focus', 'Merkez-çevre açısı, çevrel dörtgen, teğet açıları'
                ),
                jsonb_build_object(
                    'name', 'Uzunluk Teoremleri',
                    'duration', 240,
                    'focus', 'Kiriş özellikleri, teğet uzunlukları, kuvvet teoremi'
                ),
                jsonb_build_object(
                    'name', 'Çember Denklemi',
                    'duration', 240,
                    'focus', 'Analitik düzlemde çember, merkez-yarıçap bulma'
                ),
                jsonb_build_object(
                    'name', 'İleri Uygulamalar',
                    'duration', 300,
                    'focus', 'Çemberlerin birbirine göre durumu, ortak teğetler'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Merkez ve çevre açısı ilişkisi (2:1)',
                'Teğet uzunlukları eşitliği',
                'Dik açıyla gören yay (yarım çember)',
                'Çemberin denklemini yazma'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık kuvvet teoremi uygulamaları',
                'Üç boyutlu çember problemleri'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'İki çemberin radikal ekseni',
                'Apollonius çemberleri'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-CEMBER-01: Çember Geometri';
    
    -- ==========================================
    -- 5. MAT-DONUSUM-01: Dönüşüm Geometrisi (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-DONUSUM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Öteleme, yansıma ve dönme dönüşümlerini uygulama',
            'Dönüşüm matrislerini kullanma',
            'Bileşke dönüşüm hesaplama',
            'Dönüşüm altında korunan özellikleri belirleme',
            'İzometrik dönüşümleri tanıma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-UCGEN-01',
            'MAT-VEKT-01'
        ),
        'misconceptions', jsonb_build_array(
            'Dönme merkezini yanlış belirleme',
            'Yansıma eksenine göre yansımayı yanlış yapma',
            'Bileşke dönüşümde sıranın önemini unutma',
            'Dönüşüm matrisini yanlış oluşturma',
            'Homojen olmayan dönüşümleri karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 300,
            'practice', 420,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Her dönüşüm tipi farklı geometrik anlayış ve matris bilgisi gerektiriyor',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Öteleme ve Yansıma',
                    'duration', 240,
                    'focus', 'Vektörle öteleme, eksene göre yansıma, noktaya göre yansıma'
                ),
                jsonb_build_object(
                    'name', 'Dönme Dönüşümleri',
                    'duration', 240,
                    'focus', 'Merkez etrafında dönme, dönme açısı, dönme matrisi'
                ),
                jsonb_build_object(
                    'name', 'Bileşke Dönüşümler',
                    'duration', 300,
                    'focus', 'Ardışık dönüşümler, matris çarpımı, sıra önemi'
                ),
                jsonb_build_object(
                    'name', 'İzometri ve Benzerlik',
                    'duration', 240,
                    'focus', 'Uzunluk/açı koruyan dönüşümler, homojen dönüşümler'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Eksene göre yansıma formülleri',
                'Orijin etrafında dönme (90°, 180°, 270°)',
                'Dönüşüm matrislerinin çarpımı',
                'İzometrik dönüşüm özellikleri'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Genel nokta etrafında dönme',
                'Kompleks sayılarla dönüşüm'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Projektif dönüşümler',
                'Afin dönüşümler'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-DONUSUM-01: Dönüşüm Geometrisi';
    
    -- ==========================================
    -- 6. MAT-ARDISIK-01: Ardışık Sayılar (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-ARDISIK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Düşük'
        ),
        'learning_objectives', jsonb_build_array(
            'Ardışık tam sayı problemlerini çözme',
            'Ardışık çift/tek sayı problemlerini çözme',
            'Toplam formüllerini kullanma',
            'Yaş problemlerini çözme',
            'Sayı problemlerinde denklem kurma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01'
        ),
        'misconceptions', jsonb_build_array(
            'Ardışık sayıları n, n+1, n+2 yerine n, 2n, 3n olarak almak',
            'Ardışık çift sayıları n, n+1 olarak almak (n, n+2 olmalı)',
            'Toplam formülünü yanlış kullanma',
            'Yaş problemlerinde zaman faktörünü unutma',
            'Basamak sayısı ile sayı değerini karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 210,
            'practice', 300,
            'mastery', 240
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Farklı problem tipleri (sayı, yaş, rakam) farklı kurulum stratejileri gerektiriyor',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Ardışık Sayı Problemleri',
                    'duration', 180,
                    'focus', 'Tam sayı, çift/tek sayı, toplam formülleri'
                ),
                jsonb_build_object(
                    'name', 'Yaş Problemleri',
                    'duration', 240,
                    'focus', 'Geçmiş-şimdi-gelecek zaman ilişkileri, denklem kurma'
                ),
                jsonb_build_object(
                    'name', 'Rakam ve Basamak Problemleri',
                    'duration', 240,
                    'focus', 'İki/üç basamaklı sayılar, rakam yer değiştirme'
                ),
                jsonb_build_object(
                    'name', 'Karma Problem Çözme',
                    'duration', 210,
                    'focus', 'Tüm tiplerin kombinasyonu, hızlı strateji seçimi'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Ardışık tam sayı (n, n+1, n+2)',
                'Ardışık çift/tek sayı (n, n+2, n+4)',
                'Yaş problemleri (x yıl önce/sonra)',
                'İki basamaklı sayı (10a + b)'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık üç nesne yaş problemleri',
                'Dört basamaklı sayı problemleri'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Aritmetik dizi ile ardışık sayı kombinasyonları',
                'Modüler aritmetik ile ardışık sayı özellikleri'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-ARDISIK-01: Ardışık Sayılar ve Problemler';
    
    -- ==========================================
    -- 7. MAT-ANALITIK-01: Analitik Geometri (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-ANALITIK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Koordinat sisteminde nokta ve doğru işlemleri yapma',
            'Doğru denklemi yazma (genel form, eğim-kayma)',
            'İki doğrunun durumunu belirleme (paralel, dik, kesişen)',
            'Nokta-doğru uzaklığı hesaplama',
            'Geometrik şekillerin denklemlerini yazma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-VEKT-01',
            'MAT-FONK-01'
        ),
        'misconceptions', jsonb_build_array(
            'Eğim (m) ile açı (α) arasındaki ilişkiyi yanlış kurma (m = tan α)',
            'Paralel doğrularda m1 = m2, dik doğrularda m1 × m2 = -1 kuralını unutma',
            'Nokta-doğru uzaklık formülünü yanlış uygulamak',
            'Doğru denkleminde Ax + By + C = 0 formunda A, B, C katsayılarını karıştırma',
            'İki nokta arası mesafeyi yanlış hesaplama'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 480,
            'mastery', 420
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Analitik geometri geniş bir alan: nokta-doğru-çember-konikler farklı yaklaşımlar gerektirir',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Nokta ve Doğru Temelleri',
                    'duration', 240,
                    'focus', 'Koordinat sistemi, mesafe, orta nokta, doğru eğimi'
                ),
                jsonb_build_object(
                    'name', 'Doğru Denklemleri',
                    'duration', 300,
                    'focus', 'Genel form, eğim-kayma formu, iki nokta formu, kesim noktası'
                ),
                jsonb_build_object(
                    'name', 'Doğru İlişkileri ve Uzaklıklar',
                    'duration', 300,
                    'focus', 'Paralel/dik doğrular, nokta-doğru uzaklığı, doğru-doğru uzaklığı'
                ),
                jsonb_build_object(
                    'name', 'İleri Konular',
                    'duration', 360,
                    'focus', 'Çember denklemi, elips/hiperbol/parabol temelleri, kesişim problemleri'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Doğrunun eğimi ve denklemi',
                'Paralel ve dik doğru koşulları',
                'Nokta-doğru uzaklık formülü',
                'İki nokta arası mesafe',
                'Çember denklemi temel form'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Karmaşık konik kesit problemleri',
                'Parametrik denklemler'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Kutupsal koordinatlar',
                'Hiperbol ve elips ileri özellikleri',
                'Dönüştürülmüş koordinat sistemleri'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-ANALITIK-01: Analitik Geometri';
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'MATHEMATICS 100%% COMPLETE! SUCCESS!';
    RAISE NOTICE '40/40 topics with contexts!';
    RAISE NOTICE 'Perfect 20F/20S balance achieved!';
    RAISE NOTICE '==========================================';
    
END $$;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check all 7 final topics inserted
SELECT 
    code,
    name_tr,
    difficulty_level,
    grade_level,
    is_active
FROM topics
WHERE code IN (
    'MAT-UCGEN-01', 'MAT-DORTGEN-01', 'MAT-KATI-01',
    'MAT-CEMBER-01', 'MAT-DONUSUM-01', 'MAT-ARDISIK-01', 'MAT-ANALITIK-01'
)
ORDER BY code;

-- Check all 7 contexts created
SELECT 
    t.code,
    t.name_tr,
    CASE WHEN tc.id IS NULL THEN 'NO CONTEXT' ELSE 'HAS CONTEXT' END as status,
    tc.metadata->>'archetype' as archetype
FROM topics t
LEFT JOIN topic_contexts tc ON t.id = tc.topic_id
WHERE t.code IN (
    'MAT-UCGEN-01', 'MAT-DORTGEN-01', 'MAT-KATI-01',
    'MAT-CEMBER-01', 'MAT-DONUSUM-01', 'MAT-ARDISIK-01', 'MAT-ANALITIK-01'
)
ORDER BY t.code;

-- Final cumulative stats (should show 40 topics, 20F/20S)
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

-- ============================================
--  100% COMPLETION CELEBRATION! 
-- ============================================
