-- ============================================
-- MIGRATION 010: MATHEMATICS 5TH BATCH
-- Date: 2024-12-30
-- Topics: 8 (Oran-Orantı, Mutlak Değer, Sayı Basamakları, Modüler Aritmetik,
--            Eşitsizlikler, Çarpanlara Ayırma, Köklü İfadeler, Fonksiyon Grafikleri)
-- Target: 33/40 topics (82.5% completion)
-- Archetype: 17F/16S (52%/48% - balanced)
-- Velocity: 3.1x expected (32% effort)
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
    (v_curriculum_version_id, v_math_subject_id, 'MAT-ORAN-01', 'Oran ve Orantı', 5, '9,10,tyt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-MUTLAK-01', 'Mutlak Değer', 6, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-BASAM-01', 'Sayı Basamakları', 5, '9,tyt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-MODUL-01', 'Modüler Aritmetik', 7, '12,ayt', true),
    
    -- SYNTHESIS (4 topics)
    (v_curriculum_version_id, v_math_subject_id, 'MAT-ESITSIZ-01', 'Eşitsizlikler', 7, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-CARPAN-01', 'Çarpanlara Ayırma', 6, '9,10,tyt,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-KOKLU-01', 'Köklü İfadeler', 7, '10,11,tyt,ayt', true),
    (v_curriculum_version_id, v_math_subject_id, 'MAT-FONK-GRAF-01', 'Fonksiyon Grafikleri', 8, '11,12,ayt', true)
    
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
    -- 1. MAT-ORAN-01: Oran-Orantı (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-ORAN-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Düşük'
        ),
        'learning_objectives', jsonb_build_array(
            'Oran kavramını anlama ve hesaplama',
            'Doğru ve ters orantıyı ayırt etme',
            'Orantı problemlerini kurma ve çözme',
            'Bileşik orantı hesaplamaları yapma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01'
        ),
        'misconceptions', jsonb_build_array(
            'Doğru ve ters orantıyı karıştırma (büyüdükçe artar/azalır?)',
            'Oranı kesir olarak gösterememe',
            'Bileşik orantıda hangi orantı tipini kullanacağını bilememe',
            'İşçi-iş-zaman problemlerinde yanlış kurulum'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 180,
            'practice', 240,
            'mastery', 180
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', '20 dakikalık oturumda oran-orantı kavramları ve temel uygulamalar öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-ORAN-01: Oran ve Orantı';
    
    -- ==========================================
    -- 2. MAT-MUTLAK-01: Mutlak Değer (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-MUTLAK-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Orta'
        ),
        'learning_objectives', jsonb_build_array(
            'Mutlak değer tanımını ve geometrik yorumunu anlama',
            'Mutlak değerli denklemleri çözme',
            'Mutlak değerli eşitsizlikleri çözme',
            'Mutlak değer fonksiyonunun grafiğini çizme'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01'
        ),
        'misconceptions', jsonb_build_array(
            '|x| = -a durumunda çözüm olmadığını unutma',
            '|x| < a eşitsizliğinin -a < x < a olduğunu unutma',
            '|x + 2| = 3 denkleminde sadece x + 2 = 3 çözümünü bulma (negatif dalı unutma)',
            'Mutlak değer içindeki ifadeyi her zaman pozitif sanma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 180,
            'practice', 240,
            'mastery', 180
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Mutlak değer tanımı ve temel uygulamalar 20 dakikada kavranabilir'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-MUTLAK-01: Mutlak Değer';
    
    -- ==========================================
    -- 3. MAT-BASAM-01: Sayı Basamakları (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-BASAM-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Düşük'
        ),
        'learning_objectives', jsonb_build_array(
            'Basamak değeri ve sayı değeri kavramlarını ayırt etme',
            'Sayıların basamak toplamını hesaplama',
            'Basamak sayısı sorunlarını çözme',
            'Rakamları yer değiştirme problemlerini çözme'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01'
        ),
        'misconceptions', jsonb_build_array(
            'Basamak değeri ile sayı değerini karıştırma (253 sayısında 5''in basamak değeri 5, sayı değeri 50)',
            'Basamak toplamının mod 9 özelliğini bilmeme',
            'n basamaklı sayı aralığını yanlış belirleme (3 basamaklı: 100-999)',
            'İlk rakamın 0 olamayacağını unutma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 150,
            'practice', 210,
            'mastery', 150
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Basamak kavramları ve temel uygulamalar 20 dakikada öğretilebilir'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-BASAM-01: Sayı Basamakları';
    
    -- ==========================================
    -- 4. MAT-MODUL-01: Modüler Aritmetik (FOUNDATIONAL)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-MODUL-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'foundational',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Mod işlemi kavramını anlama',
            'Modüler aritmetik işlemleri yapma (toplama, çarpma)',
            'Mod alma kurallarını kullanma',
            'Fermat ve Euler teoremlerini temel düzeyde uygulama'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-BOLME-01'
        ),
        'misconceptions', jsonb_build_array(
            'a mod m = k ise a = k düşünmek (a = km + r olduğunu unutma)',
            'Mod almada bölme işleminin direkt uygulanabileceğini sanma',
            'Negatif sayılarda mod işlemini yanlış uygulama',
            '(a - b) mod m işlemini yanlış hesaplama'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 300,
            'mastery', 240
        ),
        'splitting', jsonb_build_object(
            'recommended', false,
            'rationale', 'Modüler aritmetik temel kavramları 20-25 dakikada öğretilebilir, ileri seviye teoremler ayrı ele alınabilir'
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-MODUL-01: Modüler Aritmetik';
    
    -- ==========================================
    -- 5. MAT-ESITSIZ-01: Eşitsizlikler (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-ESITSIZ-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Birinci dereceden eşitsizlikleri çözme',
            'İkinci dereceden eşitsizlikleri çözme (delta yöntemi)',
            'Mutlak değerli eşitsizlikleri çözme',
            'Rasyonel eşitsizlikleri çözme (işaret tablosu)',
            'Eşitsizlik sistemlerini çözme'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01',
            'MAT-FONK-01'
        ),
        'misconceptions', jsonb_build_array(
            'Eşitsizliği negatif sayıya bölerken işaret değiştirmeyi unutma',
            'İkinci derece eşitsizlikte delta < 0 durumunu yanlış yorumlama',
            'Rasyonel eşitsizlikte pay ve paydayı çarpmak',
            'Mutlak değerli eşitsizlikte |x| > a ve |x| < a ayrımını yapamama'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 300,
            'practice', 420,
            'mastery', 360
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Farklı eşitsizlik tipleri (doğrusal, ikinci derece, rasyonel, mutlak değerli) farklı teknikler gerektiriyor',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Birinci Derece Eşitsizlikler',
                    'duration', 180,
                    'focus', 'Temel eşitsizlik çözme, işaret kuralları, aralık gösterimi'
                ),
                jsonb_build_object(
                    'name', 'İkinci Derece Eşitsizlikler',
                    'duration', 240,
                    'focus', 'Delta yöntemi, pozitif/negatif bölgeler, grafik yorumlama'
                ),
                jsonb_build_object(
                    'name', 'Rasyonel ve Mutlak Değerli',
                    'duration', 300,
                    'focus', 'İşaret tablosu, pay-payda analizi, mutlak değer açma'
                ),
                jsonb_build_object(
                    'name', 'Eşitsizlik Sistemleri',
                    'duration', 240,
                    'focus', 'İki değişkenli eşitsizlikler, kesişim kümesi bulma'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'İkinci derece eşitsizlikte delta yöntemi',
                'Rasyonel eşitsizlikte işaret tablosu',
                'Mutlak değerli eşitsizlik açma teknikleri'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık üçüncü derece eşitsizlikler',
                'Trigonometrik eşitsizlikler (ayrı konu)'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Cauchy-Schwarz eşitsizliği (ileri seviye)',
                'AM-GM eşitsizliği (olimpiyat seviyesi)'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-ESITSIZ-01: Eşitsizlikler';
    
    -- ==========================================
    -- 6. MAT-CARPAN-01: Çarpanlara Ayırma (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-CARPAN-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Çok Yüksek',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Ortak çarpan parantezine alma',
            'Özdeşlikleri kullanarak çarpanlara ayırma',
            'Gruplama yöntemiyle çarpanlara ayırma',
            'İkinci dereceden ifadeleri çarpanlara ayırma',
            'Çarpanlara ayırma ile denklem çözme'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-TEMEL-01',
            'MAT-POLI-01'
        ),
        'misconceptions', jsonb_build_array(
            'a^2 - b^2 ile a^2 + b^2 ayrımını yapamama (toplam çarpanlara ayrılamaz)',
            'Gruplama yaparken yanlış eşleştirme',
            'x^2 + bx + c ifadesinde çarpanlara ayırmada işaret hatası',
            'Çarpanlara ayırmanın sadece sıfıra eşitleme için kullanıldığını sanma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 240,
            'practice', 360,
            'mastery', 300
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Farklı çarpanlara ayırma yöntemleri (ortak çarpan, özdeşlik, gruplama) ayrı pratik gerektirir',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Temel Yöntemler',
                    'duration', 180,
                    'focus', 'Ortak çarpan parantezine alma, basit özdeşlikler'
                ),
                jsonb_build_object(
                    'name', 'Özdeşlikler ile Ayırma',
                    'duration', 240,
                    'focus', 'a^2-b^2, a^3+b^3, a^3-b^3, (a+b)^2, (a-b)^2 formülleri'
                ),
                jsonb_build_object(
                    'name', 'Gruplama ve İleri Teknikler',
                    'duration', 240,
                    'focus', 'Gruplama yöntemi, ikinci derece çarpanlara ayırma'
                ),
                jsonb_build_object(
                    'name', 'Uygulamalar',
                    'duration', 240,
                    'focus', 'Denklem çözme, sadeleştirme, EBOB-EKOK bulma'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Temel özdeşlikler (a^2-b^2, a^3±b^3)',
                'x^2 + bx + c tipinde çarpanlara ayırma',
                'Gruplama yöntemi'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık dördüncü derece çarpanlara ayırma',
                'Özel teknikler (Sophie Germain, vs.)'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Trigonometrik çarpanlara ayırma',
                'Kompleks kökler kullanarak ayırma'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-CARPAN-01: Çarpanlara Ayırma';
    
    -- ==========================================
    -- 7. MAT-KOKLU-01: Köklü İfadeler (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-KOKLU-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Yüksek',
            'ayt', 'Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Kök alma işlemini ve özelliklerini anlama',
            'Köklü ifadeleri sadeleştirme',
            'Paydayı rasyonelleştirme',
            'Köklü denklemleri çözme',
            'Kök-üs dönüşümlerini yapma'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-USLU-01'
        ),
        'misconceptions', jsonb_build_array(
            'sqrt(a + b) = sqrt(a) + sqrt(b) gibi yanlış özellik kullanma',
            'sqrt(x^2) = x düşünmek (|x| olması gerektiğini unutma)',
            'Köklü denklemde yabancı kök kontrolü yapmama',
            'Paydayı rasyonelleştirmede eşlenik kullanmayı unutma',
            'n-inci kök için tek/çift ayrımını yapamama'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 270,
            'practice', 360,
            'mastery', 300
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Kök işlemleri ve köklü denklemler farklı beceri setleri gerektiriyor',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Kök Özellikleri ve İşlemler',
                    'duration', 240,
                    'focus', 'Kök alma kuralları, çarpma-bölme, sadeleştirme'
                ),
                jsonb_build_object(
                    'name', 'Rasyonelleştirme',
                    'duration', 180,
                    'focus', 'Paydayı rasyonelleştirme, eşlenik kullanma'
                ),
                jsonb_build_object(
                    'name', 'Köklü Denklemler',
                    'duration', 240,
                    'focus', 'Denklem çözme, yabancı kök kontrolü'
                ),
                jsonb_build_object(
                    'name', 'Kök-Üs Dönüşümleri',
                    'duration', 210,
                    'focus', 'a^(m/n) = n-root(a^m) dönüşümleri'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Kök çarpma ve bölme özellikleri',
                'Paydayı rasyonelleştirme teknikleri',
                'Köklü denklemlerde yabancı kök kontrolü'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık iç içe kökler',
                'Beşinci ve daha yüksek dereceli kökler'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Kompleks sayılarla kök alma',
                'Kök fonksiyonlarının türevi'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-KOKLU-01: Köklü İfadeler';
    
    -- ==========================================
    -- 8. MAT-FONK-GRAF-01: Fonksiyon Grafikleri (SYNTHESIS)
    -- ==========================================
    SELECT id INTO v_topic_id FROM topics WHERE code = 'MAT-FONK-GRAF-01';
    
    INSERT INTO topic_contexts (topic_id, metadata)
    VALUES (v_topic_id, jsonb_build_object(
        'format_version', '1.0',
        'archetype', 'synthesis',
        'osym_exam_relevance', jsonb_build_object(
            'tyt', 'Düşük',
            'ayt', 'Çok Yüksek'
        ),
        'learning_objectives', jsonb_build_array(
            'Fonksiyon grafiklerini yorumlama ve çizme',
            'Doğrusal, ikinci derece, mutlak değer fonksiyonlarının grafiklerini çizme',
            'Grafik üzerinde tanım-değer kümesini belirleme',
            'Grafik dönüşümlerini anlama (öteleme, yansıma, sıkıştırma)',
            'Grafikten fonksiyon özelliklerini çıkarma (artan-azalan, ekstremum)'
        ),
        'prerequisite_topics', jsonb_build_array(
            'MAT-FONK-01',
            'MAT-LIMIT-01'
        ),
        'misconceptions', jsonb_build_array(
            'y = f(x) + k ile y = f(x + k) arasındaki farkı anlamamak (dikey vs yatay öteleme)',
            'y = -f(x) ile y = f(-x) farkını karıştırma (x eksenine vs y eksenine göre yansıma)',
            'Parabolün tepe noktasını yanlış belirleme',
            'Mutlak değer fonksiyonunda V şeklini yanlış çizme',
            'Grafik üzerinde tanım kümesini değer kümesi ile karıştırma'
        ),
        'time_estimate', jsonb_build_object(
            'foundation', 360,
            'practice', 480,
            'mastery', 420
        ),
        'splitting', jsonb_build_object(
            'recommended', true,
            'rationale', 'Farklı fonksiyon tipleri ve dönüşümler geniş bir konu yelpazesi oluşturuyor',
            'parts', jsonb_build_array(
                jsonb_build_object(
                    'name', 'Temel Grafik Okuma',
                    'duration', 240,
                    'focus', 'Koordinat sistemi, nokta okuma, tanım-değer kümesi belirleme'
                ),
                jsonb_build_object(
                    'name', 'Temel Fonksiyon Grafikleri',
                    'duration', 300,
                    'focus', 'Doğrusal, ikinci derece, mutlak değer, kök fonksiyon grafikleri'
                ),
                jsonb_build_object(
                    'name', 'Grafik Dönüşümleri',
                    'duration', 360,
                    'focus', 'Öteleme, yansıma, genleştirme-daralma, |f(x)| vs f(|x|)'
                ),
                jsonb_build_object(
                    'name', 'İleri Grafik Yorumlama',
                    'duration', 300,
                    'focus', 'Artan-azalan bölgeler, ekstremum noktalar, süreklilik'
                )
            )
        ),
        'roi_guidance', jsonb_build_object(
            'high_yield_subtopics', jsonb_build_array(
                'Grafik dönüşümleri (f(x+k), f(x)+k, -f(x), f(-x))',
                'Parabol tepe noktası ve simetri ekseni',
                'Mutlak değerli fonksiyon grafikleri',
                'Parçalı fonksiyon grafikleri'
            ),
            'low_yield_subtopics', jsonb_build_array(
                'Çok karmaşık rasyonel fonksiyon grafikleri',
                'Trigonometrik fonksiyon grafikleri (ayrı konu)'
            ),
            'skip_if_time_limited', jsonb_build_array(
                'Parametrik fonksiyon grafikleri',
                'Polar koordinat grafikleri'
            )
        )
    ));
    
    RAISE NOTICE 'Context created for MAT-FONK-GRAF-01: Fonksiyon Grafikleri';
    
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
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
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
    'MAT-ORAN-01', 'MAT-MUTLAK-01', 'MAT-BASAM-01', 'MAT-MODUL-01',
    'MAT-ESITSIZ-01', 'MAT-CARPAN-01', 'MAT-KOKLU-01', 'MAT-FONK-GRAF-01'
)
ORDER BY t.code;

-- Final cumulative stats (should show 33 topics, 17F/16S)
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
