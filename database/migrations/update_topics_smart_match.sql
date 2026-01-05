-- ============================================
-- UPDATE TOPICS WITH YEAR DATA
-- Smart name-based matching
-- ============================================

BEGIN;

-- Create temp table for excel data
CREATE TEMP TABLE excel_topic_data (
    excel_id INT,
    subject_code TEXT,
    grade_level TEXT,
    topic_name TEXT,
    q_2018 DECIMAL(4,2),
    q_2019 DECIMAL(4,2),
    q_2020 DECIMAL(4,2),
    q_2021 DECIMAL(4,2),
    q_2022 DECIMAL(4,2),
    q_2023 DECIMAL(4,2),
    q_2024 DECIMAL(4,2),
    q_2025 DECIMAL(4,2)
);

INSERT INTO excel_topic_data VALUES (
    1,
    'MAT',
    '9',
    'Matematik:Sayılar-Gerçek Sayıların Üslü ve Köklü Gösterimleri ile Yapılan İşlemler',
    2.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    2,
    'MAT',
    '9',
    'Matematik:Sayılar-Gerçek Sayı Aralıklarının Gösteriminde ve Aralıklarla İlgili İşlemlerde Küme, Sembol ve İşlemleri',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    3,
    'MAT',
    '9',
    'Matematik:Sayılar-Sayı Kümelerinin Özellikleri',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    4,
    'MAT',
    '9',
    'Matematik:Sayılar-Gerçek Sayıların İşlem Özellikleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    5,
    'MAT',
    '9',
    'Matematik:Nicelikler ve Değişimler-Gerçek Sayılarda Tanımlı Doğrusal Fonksiyonlar ve Nitel Özellikleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    6,
    'MAT',
    '9',
    'Matematik:Nicelikler ve Değişimler-Gerçek Sayılarda Mutlak Değer Fonksiyonları ve Nitel Özellikleri',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    7,
    'MAT',
    '9',
    'Matematik:Nicelikler ve Değişimler-Doğrusal Fonksiyonlarla İfade Edilebilen Denklem ve Eşitsizlikler İçeren Problemler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    8,
    'MAT',
    '9',
    'Matematik:Geometrik Şekiller-Üçgenle Açı ve Kenarlarla İlgili Özellikler',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    9,
    'MAT',
    '9',
    'Matematik:Eşlik ve Benzerlik-Geometrik Dönüşümler',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    10,
    'MAT',
    '9',
    'Matematik:Eşlik ve Benzerlik-İki Üçgenin Eş veya Benzer Olması İçin Gerekli Olan Asgari Koşullar',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    11,
    'MAT',
    '9',
    'Matematik:Eşlik ve Benzerlik-Bir Üçgenden Hareketle Ona Benzer ÜçgenlerOluşturma',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    12,
    'MAT',
    '9',
    'Matematik:Eşlik ve Benzerlik-Tales, Öklid ve Pisagor Teoremleri',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    13,
    'MAT',
    '9',
    'Matematik:Eşlik ve Benzerlik-Eşlik ve Benzerlikle İlgili Problemler',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    14,
    'MAT',
    '9',
    'Matematik:Algoritma ve Bilişim-Algoritma Temelli Yaklaşımlarla Problem Çözme',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    15,
    'MAT',
    '9',
    'Matematik:Algoritma ve Bilişim-Algoritmik Yapılar İçerisindeki Mantık Bağlaçları ve Niceleyicileri',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    16,
    'MAT',
    '9',
    'Matematik:Algoritma ve Bilişim-Algoritmalarda ve Matematiksel İspatlarda Mantık Bağlaçları ve Niceleyiciler',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    17,
    'MAT',
    '9',
    'Matematik:İstatistiksel Araştırma Süreci-Tek Nicel Değişkenli Veri Dağılımları ile Çalışma ve Veriye Dayalı Karar Verme',
    0.0, 0.0, 1.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    18,
    'MAT',
    '9',
    'Matematik:İstatistiksel Araştırma Süreci-Başkalır Tarafından Oluşturulan Tek Nicel değişkenli Veri Dağılımlarına Dayalı Sonuç veya Yorumları Tartışabilme',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    19,
    'MAT',
    '9',
    'Matematik:Veriden Olasılığa-Olayların Olasılığını Gözleme Dayalı Tahmin Etme',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    20,
    'MAT',
    '9',
    'Matematik:Veriden Olasılığa-Olayların Olasılığına İlişkin Tümevarımsal Akıl Yürütme',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    21,
    'FIZ',
    '9',
    'Fizik:Fizik Bilimi ve Kariyer Keşfi-Fizik Bilimi, Alt Dalları',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    22,
    'FIZ',
    '9',
    'Fizik:Fizik Bilimi ve Kariyer Keşfi-Fizik Bilimine Yön Verenler, Kariyer Keşfi',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    23,
    'FIZ',
    '9',
    'Fizik:Kuvvet ve Hareket-Temel ve Türetilmiş Nicelikler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    24,
    'FIZ',
    '9',
    'Fizik:Kuvvet ve Hareket-Skaler ve Vektörel Nicelikler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    25,
    'FIZ',
    '9',
    'Fizik:Kuvvet ve Hareket-Vektörler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    26,
    'FIZ',
    '9',
    'Fizik:Kuvvet ve Hareket-Doğadaki Temel Kuvvetler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    27,
    'FIZ',
    '9',
    'Fizik:Kuvvet ve Hareket-Hareket ve Hareket Türleri',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    28,
    'FIZ',
    '9',
    'Fizik:Akışkanlar-Basınç',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    29,
    'FIZ',
    '9',
    'Fizik:Akışkanlar-Sıvılarda Basınç',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    30,
    'FIZ',
    '9',
    'Fizik:Akışkanlar-Açık Hava Basınıcı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    31,
    'FIZ',
    '9',
    'Fizik:Akışkanlar-Kaldırma Kuvveti',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    32,
    'FIZ',
    '9',
    'Fizik:Akışkanlar-Bernoulli İlkesi',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    33,
    'FIZ',
    '9',
    'Fizik:Enerji-İç Enerji, Isı',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    34,
    'FIZ',
    '9',
    'Fizik:Enerji-Isı, öz Isı, Isı Sığası ve Sıcaklık Farkı arasındaki İlişki',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    35,
    'FIZ',
    '9',
    'Fizik:Enerji-Hal Değişimi',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    36,
    'FIZ',
    '9',
    'Fizik:Enerji-Isıl Denge',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    37,
    'FIZ',
    '9',
    'Fizik:Enerji-Isı Aktarım Yolları',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    38,
    'FIZ',
    '9',
    'Fizik:Enerji-Isı İletim Hızı',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    39,
    'KIM',
    '9',
    'Kimya:Etkileşim-Kimya Hayattır',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    40,
    'KIM',
    '9',
    'Kimya:Etkileşim-Atomdan Periyodik Tabloya, Atom Teorileri (Bohr Atom Teorisi, Modern Atom Teorisi) ve Atomun Yapısı',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    41,
    'KIM',
    '9',
    'Kimya:Etkileşim-Atomdan Periyodik Tabloya, Atom Orbitalleri ve Elektron Dizilimi',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    42,
    'KIM',
    '9',
    'Kimya:Etkileşim-Atomdan Periyodik Tabloya, Periyodik Tabloda Yer Bulma',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    43,
    'KIM',
    '9',
    'Kimya:Etkileşim-Atomdan Periyodik Tabloya, Periyodik Özellikler',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    44,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Metalik Bağ',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    45,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, İyonik Bağ',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    46,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Kovalent Bağ',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    47,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Lewis Nokta Yapısı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    48,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Molekül Polarlığı, Apolarlığı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    49,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Bileşiklerin Adlandırılması',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    50,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Etkileşimden Maddeye, Moleküller Arası Etkileşimler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    51,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Etkileşimden Maddeye, Katılar ve Özellikleri (Amorf ve Kristal)',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    52,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Etkileşimden Maddeye, Sıvılar ve Özellikleri, Buharlaşma ve Denge Buhar Basıncı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    53,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Etkileşimden Maddeye, Sıvılar ve Özellikleri, Kaynama Sıcaklığı, Viskozite',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    54,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Etkileşimden Maddeye, Sıvılar ve Özellikleri, Adezyon ve Kohezyon Kuvvetleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    55,
    'KIM',
    '9',
    'Kimya:Çeşitlilik-Etkileşimler, Etkileşimden Maddeye, Sıvılar ve Özellikleri, Sıvıların Yüzey Gerilimini Etkileyen Kuvvetler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    56,
    'KIM',
    '9',
    'Kimya:Sürdürülebilirlik-Nanoparçacıklar ve Ekolojik Sürdürülebilirlik, Metal Nanoparçacıklar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    57,
    'KIM',
    '9',
    'Kimya:Sürdürülebilirlik-Nanoparçacıklar ve Ekolojik Sürdürülebilirlik, Yeşil Kimyanın Atık Önleme İlkesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    58,
    'KIM',
    '9',
    'Kimya:Sürdürülebilirlik-Nanoparçacıklar ve Ekolojik Sürdürülebilirlik, Metal, Alaşım ve Metal Nanoparçacıkların Çevresel Etkileri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    59,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Biyolojideki Dönüm Noktalarının İnsan Hayatına Katkıları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    60,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Bilim, Bilimin Doğası ve Bilimsel Araştırma Süreçleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    61,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Bilimsel Araştırmaların Bilim Etiğine Uygunluğu',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    62,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Canlıların Ortak Özellikleri, Hücresel Yapı, Organizasyon',
    0.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    63,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Canlıların Ortak Özellikleri, Beslenme, enerji Üretimi ve Tüketimi',
    0.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    64,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Canlıların Ortak Özellikleri, Metabolizma, Boşaltım, Büyüme ve Gelişme, Üreme',
    0.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    65,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Canlıların Ortak Özellikleri, Uyaranlara Tepki, Homeostazi, Varyasyon ve Adaptasyon, Virüsler',
    0.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    66,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Sınıflandırmada Temel Yaklaşımlar ve Modern Sınıflandırma',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    67,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Sınıflandırmada Üç Üst Alem(Domain) Sistemi, Bakteriler, Arkeler, Ökaryotlar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    68,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Sınıflandırmada Üç Üst Alem(Domain) Sistemi, Ökaryot Canlıların Sınıflandırılması',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    69,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Sınıflandırmada Üç Üst Alem(Domain) Sistemi, Canlıların Biyolojik ve ekonomik Önemi',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    70,
    'BIO',
    '9',
    'Biyoloji:Yaşam-Biyoçeşitlilik',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    71,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-İnorganik Moleküller',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    72,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-Organik Moleküller, Karbonhidratlar, Lipitler, Proteinler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    73,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-Organik Moleküller, Enzim Aktivitesini Etkileyen Koşullar, Nükleik Asitler, Vitaminler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    74,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-Organik Moleküllerin Tayininde Kullanılan Ayıraçlar',
    0.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    75,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-Enzim Aktivitesini Etkileyen Koşullar',
    0.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    76,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-Hücre ve Alt Birimleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    77,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-Hücre Zarından Madde Geçişleri',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    78,
    'BIO',
    '9',
    'Biyoloji:Organizasyon-Küçük Moleküllerin Hareketi,Difüzyon ve Ozmoz',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    79,
    'TAR',
    '9',
    'Tarih:Geçmişin İnşa Sürecinde Tarih -Tarih Öğrenmenin Faydaları, Tarihin Doğası',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    80,
    'TAR',
    '9',
    'Tarih:Geçmişin İnşa Sürecinde Tarih -Tarihsel Bilginin Üretim Süreci',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    81,
    'TAR',
    '9',
    'Tarih:Geçmişin İnşa Sürecinde Tarih -Tarih Araştırma ve Yazımında Dijital Dönüşüm',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    82,
    'TAR',
    '9',
    'Tarih:Eski Çağ Medeniyetleri -Tarım Devrimi''nin Eski Çağ''a Etkileri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    83,
    'TAR',
    '9',
    'Tarih:Eski Çağ Medeniyetleri -Eski Çağ''da Yönetenler ve Savaşanlar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    84,
    'TAR',
    '9',
    'Tarih:Eski Çağ Medeniyetleri -Eski Çağ''da Hukuk',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    85,
    'TAR',
    '9',
    'Tarih:Eski Çağ Medeniyetleri -Eski Çağ''da İnanç, Bilim ve Sanat',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    86,
    'TAR',
    '9',
    'Tarih:Eski Çağ Medeniyetleri -Türklerde Konargöçer Yaşam',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    87,
    'TAR',
    '9',
    'Tarih:Orta Çağ Medeniyetleri -Orta Çağ''da Kitlesen Göçler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    88,
    'TAR',
    '9',
    'Tarih:Orta Çağ Medeniyetleri -Orta Çağ''daki Siyasi ve Askeri Gelişmeler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    89,
    'TAR',
    '9',
    'Tarih:Orta Çağ Medeniyetleri -Orta Çağ''da Ticaret Yolları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    90,
    'TAR',
    '9',
    'Tarih:Orta Çağ Medeniyetleri -Orta Çağ''da Bilim, Kültür ve Sanat',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    91,
    'COG',
    '9',
    'Coğrafya:Coğrafyanın Doğası -Doğa ve İnsan, Coğrafya Bilimi',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    92,
    'COG',
    '9',
    'Coğrafya:Mekansal Bilgi Teknolojileri -Harita Bilgisi, Harita Okuryazarlığı',
    1.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    93,
    'COG',
    '9',
    'Coğrafya:Mekansal Bilgi Teknolojileri -Türkiye''nin Coğrafi Konumu',
    1.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    94,
    'COG',
    '9',
    'Coğrafya:Doğal Sistemler ve Süreçler -İklim Bilgisi',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    95,
    'COG',
    '9',
    'Coğrafya:Doğal Sistemler ve Süreçler -İklim Bilgisi Hava Olayları, İklim Sistemi',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    96,
    'COG',
    '9',
    'Coğrafya:Doğal Sistemler ve Süreçler -İklim Bilgisi İklim Türleri, İklim Sisteminde Yaşanan Değişiklikler',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    97,
    'COG',
    '9',
    'Coğrafya:Beşeri sistemler ve Süreçler -Nüfus ve Yerleşme',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    98,
    'COG',
    '9',
    'Coğrafya:Beşeri sistemler ve Süreçler -Nüfus Dinamikleri, Dağılımı ve Hareketleri',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    99,
    'COG',
    '9',
    'Coğrafya:Beşeri sistemler ve Süreçler -Demografik Döşünüm Süreci ve Nüfus Piramitleri, Nüfus Politikaları',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    100,
    'COG',
    '9',
    'Coğrafya:Ekonomik Faaliyetler ve Etkileri',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    101,
    'COG',
    '9',
    'Coğrafya:Afetler ve Sürdürülebilir Çevre -Doğal Afetler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    102,
    'COG',
    '9',
    'Coğrafya:Bölgeler, Ülkeler ve Küresel Bağlantılar -Bölgeler',
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    103,
    'MAT',
    '10',
    'Matematik:Sayma ve Olasılık-Sıralama ve Seçme, Sayma Yöntemleri',
    2.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    104,
    'MAT',
    '10',
    'Matematik:Sayma ve Olasılık-Sıralama ve Seçme, Permütasyon (Diziliş)',
    1.0, 1.0, 2.0, 0.0,
    0.0, 1.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    105,
    'MAT',
    '10',
    'Matematik:Sayma ve Olasılık-Sıralama ve Seçme, Tekrarlı Permütasyon',
    1.0, 1.0, 2.0, 0.0,
    1.0, 1.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    106,
    'MAT',
    '10',
    'Matematik:Sayma ve Olasılık-Sıralama ve Seçme, Kombinasyon',
    1.0, 1.0, 2.0, 0.0,
    0.0, 1.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    107,
    'MAT',
    '10',
    'Matematik:Sayma ve Olasılık-Sıralama ve Seçme, Pascal Üçgeni',
    2.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    108,
    'MAT',
    '10',
    'Matematik:Sayma ve Olasılık-Sıralama ve Seçme, Binom Açılımı',
    2.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    109,
    'MAT',
    '10',
    'Matematik:Sayma ve Olasılık-Basit Olayların Olasılıkları',
    2.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    110,
    'MAT',
    '10',
    'Matematik:Fonksiyonlar-Fonksiyon Kavramı ve Gösterimi',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    111,
    'MAT',
    '10',
    'Matematik:Fonksiyonlar-Fonksiyon Kavramı ve Gösterimi, Fonksiyonlarda Grafik Çizimi',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    112,
    'MAT',
    '10',
    'Matematik:Fonksiyonlar-Fonksiyon Kavramı ve Gösterimi, Fonksiyonlarda Grafik Yorumlama',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    113,
    'MAT',
    '10',
    'Matematik:Fonksiyonlar-Fonksiyon Kavramı ve Gösterimi, Doğrusal Fonksiyonlarda Güncel Uygulamalar',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    114,
    'MAT',
    '10',
    'Matematik:Fonksiyonlar-İki Fonksiyonun Bileşkesi ve Bir Fonksiyonun Tersi, Bire Bir ve Örtenlik',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    115,
    'MAT',
    '10',
    'Matematik:Fonksiyonlar-Bileşke Fonksiyon',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    116,
    'MAT',
    '10',
    'Matematik:Fonksiyonlar-Bir Fonksiyonun Tersi',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    117,
    'MAT',
    '10',
    'Matematik:Polinomlar-Polinom Kavramı',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    118,
    'MAT',
    '10',
    'Matematik:Polinomlar-Polinomlarla İşlemler',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    119,
    'MAT',
    '10',
    'Matematik:Polinomlar-Polinomların Çarpanlara Ayrılması',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    120,
    'MAT',
    '10',
    'Matematik:Polinomlar-Rasyonel İfadelerin Sadeleştirmesi',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    121,
    'MAT',
    '10',
    'Matematik:İkinci Dereceden Denklemler-İkinci Derecen Bir Bilinmeyenli Denklemlerin Çözümü',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    122,
    'MAT',
    '10',
    'Matematik:İkinci Dereceden Denklemler-Karmaşık Sayılar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    123,
    'MAT',
    '10',
    'Matematik:İkinci Dereceden Denklemler-İkinci Dereceden Bir Bilinmeyenleri Denklemlerin Kökleri ve Katsayıları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    124,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Çokgenler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    125,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Dörtgenler ve Özellikleri, Temel Elemanlar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    126,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Özel Dörtgenler, Yamuk',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    127,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Özel Dörtgenler, Paralel Kenar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    128,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Özel Dörtgenler, Eşkenar Dörtgen',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    129,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Özel Dörtgenler, Dikdörtgen',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    130,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Özel Dörtgenler, Kare',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    131,
    'MAT',
    '10',
    'Matematik:Dörtgenler ve Çokgenler-Özel Dörtgenler, Deltoid',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    132,
    'MAT',
    '10',
    'Matematik:Uzay Geometri-Dik Piramitler Uzunluk, Alan ve Hacim Bağıntıları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    133,
    'MAT',
    '10',
    'Matematik:Uzay Geometri-Dik Prizmalar Uzunluk, Alan ve Hacim Bağıntıları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    134,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Elektrik Akımı',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    135,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Potansiyel Farkı',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    136,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Direnç',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    137,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Elektrik Devreleri',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    138,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Elektrik Devreleri, Direnç, Potansiyel Farkı ve Akım İlişkisi',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    139,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Elektrik Devreleri, Dirençlerin Bağlanması, üreteçler',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    140,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Elektrik Enerjisi ve Elektriksel Güç',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    141,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Elektrik Akımının Oluşturabileceği Tehlikeler ve Önleme Yöntemleri',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    142,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Mıknatıs ve Manyetik Alan',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    143,
    'FIZ',
    '10',
    'Fizik:Elektrik ve Manyetizma-Akım ve Manyetik Alan',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    144,
    'FIZ',
    '10',
    'Fizik:Basınç ve Kaldırma Kuvveti-Basınç',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    145,
    'FIZ',
    '10',
    'Fizik:Basınç-Katı Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    146,
    'FIZ',
    '10',
    'Fizik:Basınç-Sıvı (Durgun Sıvıların) Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    147,
    'FIZ',
    '10',
    'Fizik:Basınç-Gaz Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    148,
    'FIZ',
    '10',
    'Fizik:Basınç-Basıncın Hal Değişimine Etkisi',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    149,
    'FIZ',
    '10',
    'Fizik:Basınç-Açık Hava Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    150,
    'FIZ',
    '10',
    'Fizik:Basınç-Akışkanlarda Akış Sürati ile Akışkan Basıncı Arasındaki İlişki',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    151,
    'FIZ',
    '10',
    'Fizik:Basınç ve Kaldırma Kuvveti-Kaldırma Kuvveti',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    152,
    'FIZ',
    '10',
    'Fizik:  Dalgalar',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    153,
    'FIZ',
    '10',
    'Fizik:  Dalgalar-Yay Dalgası, Yaylarda Atma ve Periyodik Dalga',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    154,
    'FIZ',
    '10',
    'Fizik:  Dalgalar-Su Dalgası, Doğrusal ve Dairesel Dalgaların Yansıması',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    155,
    'FIZ',
    '10',
    'Fizik:  Dalgalar-Su Dalgası, Ortam Derinliği Su Dalgalarının Yayılma Hızına Etkisi, Kırılma',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    156,
    'FIZ',
    '10',
    'Fizik:  Dalgalar-Ses Dalgası',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    157,
    'FIZ',
    '10',
    'Fizik:  Dalgalar-Deprem Dalgası',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    158,
    'FIZ',
    '10',
    'Fizik:Optik-Aydınlanma, Işığın Davranış Modelleri, Işık Şiddeti, Akısı, Aydınlanma Şiddeti',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    159,
    'FIZ',
    '10',
    'Fizik:Optik-Gölge, Yansıma, Düzlem Ayna',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    160,
    'FIZ',
    '10',
    'Fizik:Optik-Küresel Aynalar, Çukur Ayna ve Tümsek Ayna',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    161,
    'FIZ',
    '10',
    'Fizik:Optik-Kırılma',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    162,
    'FIZ',
    '10',
    'Fizik:Optik-Mercekler, İnce ve Kalın Kenarlı Mercekler',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    163,
    'FIZ',
    '10',
    'Fizik:Optik-Prizmalar',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    164,
    'FIZ',
    '10',
    'Fizik:Optik-Işık ve Boya Renkleri',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    165,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları ve Kimyasal Hesaplamalar-Kimyanın Temel Kanunları, Kütlenin Korunumu Kanunu',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    166,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları ve Kimyasal Hesaplamalar-Kimyanın Temel Kanunları, Sabit Oranlar Kanunu',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    167,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları ve Kimyasal Hesaplamalar-Kimyanın Temel Kanunları, Katlı Oranlar Kanunu',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    168,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları-Mol Kavramı ve Hesaplamaları, Atom Kütlesinin Belirlenmesi',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    169,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları-Mol Kavramı ve Hesaplamaları, Mol Kavramı',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    170,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları-Mol Kavramı ve Hesaplamaları, Mol Kavramı ile İlgili Hesaplamalar',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    171,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları-Kimyasal Tepkimelerde Hesaplamalar, Denklemli Miktar Geçiş Hesaplamaları',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    172,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları-Kimyasal Tepkimelerde Hesaplamalar, Sınırlayıcı Bileşen Hesaplamaları',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    173,
    'KIM',
    '10',
    'Kimya:Kimyanın Temel Kanunları-Kimyasal Tepkimelerde Hesaplamalar, Yüzde Verim Hesaplamaları',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    174,
    'KIM',
    '10',
    'Kimya:Karışımlar-Homojin ve Heterojin Karışımlar, Karışımların Sınıflandırılması, Çözünme Olayı',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    175,
    'KIM',
    '10',
    'Kimya:Karışımlar-Ayırma ve Saflaştırma Teknikleri',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    176,
    'KIM',
    '10',
    'Kimya:Asitler, Bazlar ve Tuzlar-Asitler ve Bazlar',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    177,
    'KIM',
    '10',
    'Kimya:Asitler, Bazlar ve Tuzlar-Asitler ve Bazların Özellikleri',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    178,
    'KIM',
    '10',
    'Kimya:Asitler, Bazlar ve Tuzlar-Asitlerin ve Bazların Tepkimeleri',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    179,
    'KIM',
    '10',
    'Kimya:Asitler, Bazlar ve Tuzlar-Hayatımızda Asitler ve Bazlar',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    180,
    'KIM',
    '10',
    'Kimya:Asitler, Bazlar ve Tuzlar-Tuzlar',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    181,
    'KIM',
    '10',
    'Kimya:Kimya Her Yerde-Yaygın Günlük Hayat Kimyasalları',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    182,
    'KIM',
    '10',
    'Kimya:Kimya Her Yerde-Gıdalar',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    183,
    'BIO',
    '10',
    'Biyoloji:Hücre Bölünmeleri-Mitoz ve Eşeysiz Üreme, Hücre Bölünmeleri, Hücre Döngüsü',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    184,
    'BIO',
    '10',
    'Biyoloji:Hücre Bölünmeleri-Mitoz ve Eşeysiz Üreme, Eşeysiz Üreme',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    185,
    'BIO',
    '10',
    'Biyoloji:Hücre Bölünmeleri-Mayoz ve Eşeyli Üreme, Mayoz',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    186,
    'BIO',
    '10',
    'Biyoloji:Hücre Bölünmeleri-Mayoz ve Eşeyli Üreme, Eşeyli Üreme',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    187,
    'BIO',
    '10',
    'Biyoloji:Kalıtımın Genel İlkeleri-Biyolojik Çeşitlilik, Mendel İlkeleri, Monohibrit, Dihibrit, Kontrol Çaprazlama',
    0.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    188,
    'BIO',
    '10',
    'Biyoloji:Kalıtımın Genel İlkeleri-Biyolojik Çeşitlilik, Mendel İlkeleri, Eş Baskınlık, Çok Alellilik, Eşeye Bağlı Kalıtım',
    0.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    189,
    'BIO',
    '10',
    'Biyoloji:Kalıtımın Genel İlkeleri-Biyolojik Çeşitlilik, Mendel İlkeleri, Soyağacı Analizi, Akraba Evliliği ve Kalıtsal Hastalıklar, Genetik Varyasyonlar',
    0.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    190,
    'BIO',
    '10',
    'Biyoloji:Ekosistem Ekolojisi ve Güncel Çevre Sorunları-Güncel Çevre Sorunları ve İnsan',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    191,
    'BIO',
    '10',
    'Biyoloji:Ekosistem Ekolojisi ve Güncel Çevre Sorunları-Doğal Kaynaklar ve Biyolojik Çeşitlilik',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    192,
    'TAR',
    '10',
    'Tarih:Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi-Anadolu Siyasi Tarihi (1072-1308)',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    193,
    'TAR',
    '10',
    'Tarih:Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi-Anadolu''nun Türkleşmesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    194,
    'TAR',
    '10',
    'Tarih:Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi-Anadolu''daki İlk Türk Siyasi Teşekkülleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    195,
    'TAR',
    '10',
    'Tarih:Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi-Haçlı Seferleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    196,
    'TAR',
    '10',
    'Tarih:Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi-Moğol İstilası ve Sonuçları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    197,
    'TAR',
    '10',
    'Tarih:Beylikten Devlete Osmanlı Siyaseti-1299-1453 Osmanlı Siyasi Faaliyetleri, Beyliğin Devletmeşme Süreci',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    198,
    'TAR',
    '10',
    'Tarih:Beylikten Devlete Osmanlı Siyaseti-Rumeli''deki Fetihler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    199,
    'TAR',
    '10',
    'Tarih:Beylikten Devlete Osmanlı Siyaseti-Anadolu''da Türk Siyasi Birliğini Sağlamaya Yönelik Faaliyetler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    200,
    'TAR',
    '10',
    'Tarih:Devletleşme Sürecinde Savaşçılar ve Askerler-Devletleşme Sürecinde Osmanlı Ordusu',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    201,
    'TAR',
    '10',
    'Tarih:Devletleşme Sürecinde Savaşçılar ve Askerler-Tımar Sistemi ve Tımarlı Sipahiler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    202,
    'TAR',
    '10',
    'Tarih:Devletleşme Sürecinde Savaşçılar ve Askerler-Pencik, Devşirme Sistemi ve Yeniçeriler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    203,
    'TAR',
    '10',
    'Tarih:Beylikten Devlete Osmanlı Medeniyeti-Anadolu''nun İslamlaşmasına Sufi ve Alimlerin Katkıları',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    204,
    'TAR',
    '10',
    'Tarih:Beylikten Devlete Osmanlı Medeniyeti-Osmanlı Devletinin İdari Yapısı',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    205,
    'TAR',
    '10',
    'Tarih:Beylikten Devlete Osmanlı Medeniyeti-Osmanlı Coğrafyasında Bilim, Kültür, Sanat ve Zanaat',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    206,
    'TAR',
    '10',
    'Tarih:Dünya Gücü Osmanlı (1453-1595)-1453-1520 Yılları Arası Osmanlı Siyasi Faaliyetleri, İstanbul''un Fethi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    207,
    'TAR',
    '10',
    'Tarih:Dünya Gücü Osmanlı (1453-1595)-İslam Dünyasında Hakimiyet Kurulması, 1520-1595 Arası Osmanlı Siyasi Faaliyetleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    208,
    'TAR',
    '10',
    'Tarih:Dünya Gücü Osmanlı (1453-1595)-Osmanlı Devleti Zirvede, Dünya Gücü Osmanlı ve Stratejik Rakipleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    209,
    'TAR',
    '10',
    'Tarih:Dünya Gücü Osmanlı (1453-1595)-Kara ve Denizlere Nüfuz Etme Çabaları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    210,
    'TAR',
    '10',
    'Tarih:Sultan ve Osmanlı Merkez Teşkilatı-Osmanlı Merkez Teşkilatı, Merkez Yapısının Güçlendirilmesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    211,
    'TAR',
    '10',
    'Tarih:Klasik Çağda Osmanlı Toplum Düzeni-Osmanlı Toplum Yapısı, Fethedilen Bölgelerde Toplumsal ve Kültürel Değişimler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    212,
    'TAR',
    '10',
    'Tarih:Klasik Çağda Osmanlı Toplum Düzeni-Osmanlı Toprak Sistemi ve Tarımsal Üretim, Lonca Teşkilatı ve Osmanlı Ekonomisindeki Etkileri, Vakıf Sistemi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    213,
    'TUR',
    '10',
    'Türkçe:Anlatım Bozukluğu',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    214,
    'TUR',
    '10',
    'Türkçe:Cümlede Anlam',
    7.0, 3.0, 6.0, 3.0,
    3.0, 4.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    215,
    'TUR',
    '10',
    'Türkçe:Cümle Türleri',
    7.0, 3.0, 6.0, 3.0,
    3.0, 4.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    216,
    'TUR',
    '10',
    'Türkçe:Cümlenin Öğeleri',
    7.0, 3.0, 6.0, 3.0,
    3.0, 4.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    217,
    'TUR',
    '10',
    'Türkçe:Dil Bilgisi',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    218,
    'TUR',
    '10',
    'Türkçe:Sözcük Türleri',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    219,
    'TUR',
    '10',
    'Türkçe:Sözcük Türleri – Fiiller',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    220,
    'TUR',
    '10',
    'Türkçe:Sözcük Türleri – İsimler',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    221,
    'TUR',
    '10',
    'Türkçe:Sözcük Türleri– Edat – Bağlaç – Ünlem',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    222,
    'TUR',
    '10',
    'Türkçe:Sözcük Türleri– Sıfatlar',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    223,
    'TUR',
    '10',
    'Türkçe:Sözcük Türleri– Zamirler',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    224,
    'TUR',
    '10',
    'Türkçe:Sözcük Türleri– Zarflar',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    225,
    'TUR',
    '10',
    'Türkçe:Sözcükte Yapı',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    226,
    'TUR',
    '10',
    'Türkçe:Noktalama İşaretleri',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    227,
    'TUR',
    '10',
    'Türkçe:Paragraf',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    228,
    'TUR',
    '10',
    'Türkçe:Paragraf– Paragrafta Anlatım Teknikleri',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    229,
    'TUR',
    '10',
    'Türkçe:Paragraf– Paragrafta Düşünceyi Geliştirme Yolları',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    230,
    'TUR',
    '10',
    'Türkçe:Paragraf– Paragrafta Konu-Ana Düşünce',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    231,
    'TUR',
    '10',
    'Türkçe:Paragraf– Paragrafta Yapı',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    232,
    'TUR',
    '10',
    'Türkçe:Paragraf– Paragrafta Yardımcı Düşünce',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    233,
    'TUR',
    '10',
    'Türkçe:Ses Bilgisi',
    3.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    234,
    'TUR',
    '10',
    'Türkçe:Sözcükte Anlam',
    3.0, 4.0, 1.0, 5.0,
    4.0, 3.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    235,
    'TUR',
    '10',
    'Türkçe:Yazım Kuralları',
    2.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    236,
    'DIN',
    '10',
    'Din:Bilgi ve İnanç',
    1.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    237,
    'DIN',
    '10',
    'Din:Din ve İslam',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    238,
    'DIN',
    '10',
    'Din:İslam ve İbadet',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    239,
    'DIN',
    '10',
    'Din:Gençlik ve Değerler',
    1.0, 1.0, 1.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    240,
    'DIN',
    '10',
    'Din:Allah İnsan İlişkisi',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    241,
    'DIN',
    '10',
    'Din:Hz. Muhammed (S.A.V.)',
    1.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    242,
    'DIN',
    '10',
    'Din:Vahiy ve Akıl',
    1.0, 0.0, 2.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    243,
    'DIN',
    '10',
    'Din:İslam Düşüncesinde Yorumlar, Mezhepler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    244,
    'DIN',
    '10',
    'Din:İslam Medeniyeti ve Özellikleri',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    245,
    'COG',
    '10',
    'Coğrafya:Doğal Sistemler-Doğal Sistemler, Dünyanın Tektonik Oluşumu ve Gelişimi, Dünya''nın Teknonik Gelişimi, Yerin Katmanları',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    246,
    'COG',
    '10',
    'Coğrafya:Doğal Sistemler-Doğal Sistemler, Dünyanın Tektonik Oluşumu ve Gelişimi, Kıtaların Kayması ve Levha Tektoniği, Jeolojik Zamanlar',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    247,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-İç Kuvvetler',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    248,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Topoğrafya ve Kayaçlar',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    249,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Dış Kuvvetler-Doğal Değişim, Akarsular, Rüzgarlar, Buzullar ve Oluşturduğu Yer Şekilleri',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    250,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Dış Kuvvetler-Yer Altı Suları, Dalga ve Akıntılar ve Oluşturduğu Yer Şekilleri, Türkiye''de Dış Kuvvetlerin Yer Şekillerine Etkisi',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    251,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Dış Kuvvetler-Türkiye''de Akarsuların, Rüzgarların, Buzulların Oluşturduğu Yer Şekilleri ve Karstik Şekiller',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    252,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Dış Kuvvetler-Türkiye''de Dalga ve Akıntıların Oluşturduğu Yer Şekilleri, Kıyı tipleri, Heyelan ve Erozyon, Başlıca Yer Şekilleri',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    253,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Dünyanın Su Zenginliği',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    254,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Dünyanın Toprak Zenginliği',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    255,
    'COG',
    '10',
    'Coğrafya: Doğal Sistemler-Dünyanın Bitki Zenginliği',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    256,
    'COG',
    '10',
    'Coğrafya:Beşeri Sistemler-Nüfusun Özellikleri ve Dağılışı',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    257,
    'COG',
    '10',
    'Coğrafya:Beşeri Sistemler-Türkiye''nin Nüfus özellikleri',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    258,
    'COG',
    '10',
    'Coğrafya:Beşeri Sistemler-Nüsuf Hareketleri, Göçler',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    259,
    'COG',
    '10',
    'Coğrafya:Beşeri Sistemler-Temel Ekonomik Faaliyetler',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    260,
    'COG',
    '10',
    'Coğrafya:Küresel Ortam: Bölgeler ve Ülkeler, Ulaşım Sistemleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    261,
    'COG',
    '10',
    'Coğrafya:Çevre ve Toplum-Afetler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    262,
    'MAT',
    '11',
    'Matematik:Trigonometri-Yönlü Açılar',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    263,
    'MAT',
    '11',
    'Matematik:Trigonometri-Trigonometrik Fonksiyonlar ve Grafikleri',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    264,
    'MAT',
    '11',
    'Matematik:Trigonometri-Trigonometrik Fonksiyonlar Üçgende Kosinüs',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    265,
    'MAT',
    '11',
    'Matematik:Trigonometri-Trigonometrik Fonksiyonlar Üçgende Sinüs',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    266,
    'MAT',
    '11',
    'Matematik:Trigonometri-Trigonometrik Fonksiyonlar Kosinüs, Sinüs Grafikleri',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    267,
    'MAT',
    '11',
    'Matematik:Trigonometri-Trigonometrik Fonksiyonlar Ters Trigonometrik Fonksiyonlar',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    268,
    'MAT',
    '11',
    'Matematik:Analitik Geometri-Doğrunun Analitik İncelenmesi, Analitik Düzlem ve Analitik Düzlemde İki Nokta Arasındaki Uzaklık',
    3.0, 0.0, 1.0, 2.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    269,
    'MAT',
    '11',
    'Matematik:Analitik Geometri-Doğrunun Analitik İncelenmesi, Bir Doğru Parçasını Belli Bir Oranda (İçten/Dıştan) Bölen Noktanın Koordinatları',
    3.0, 0.0, 1.0, 2.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    270,
    'MAT',
    '11',
    'Matematik:Analitik Geometri-Doğrunun Analitik İncelenmesi, Analitik Düzlemde Doğrular',
    3.0, 0.0, 1.0, 2.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    271,
    'MAT',
    '11',
    'Matematik:Analitik Geometri-Doğrunun Analitik İncelenmesi, Bir Noktanın Bir Doğruya Uzaklığı',
    3.0, 0.0, 1.0, 2.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    272,
    'MAT',
    '11',
    'Matematik:Fonksiyonlarda Uygulamalar-Fonksiyonlarla İlgili Uygulamalar',
    3.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    273,
    'MAT',
    '11',
    'Matematik:Fonksiyonlarda Uygulamalar-İkinci Dereceden Fonksiyonlar ve Grafikleri',
    3.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    274,
    'MAT',
    '11',
    'Matematik:Fonksiyonlarda Uygulamalar-Fonksiyonların Dönüşümleri',
    3.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    275,
    'MAT',
    '11',
    'Matematik:Denklem ve Eşitsizlik Sistemleri-İkinci Dereceden İki Bilinmeyenli Denklem Sistemleri',
    0.0, 0.0, 1.0, 1.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    276,
    'MAT',
    '11',
    'Matematik:Denklem ve Eşitsizlik Sistemleri-İkinci Dereceden Bir Bilinmeyenli Eşitsizlikler ve Eşitsizlik Sistemleri',
    0.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    277,
    'MAT',
    '11',
    'Matematik:Çember ve Daire-Çemberin Temel Elemanları Teğet, Kiriş, Çap, Yay ve Kesen',
    2.0, 2.0, 2.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    278,
    'MAT',
    '11',
    'Matematik:Çember ve Daire-Çemberde Açılar',
    2.0, 2.0, 2.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    279,
    'MAT',
    '11',
    'Matematik:Çember ve Daire-Çemberde Teğet',
    2.0, 2.0, 2.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    280,
    'MAT',
    '11',
    'Matematik:Çember ve Daire-Dairenin Çevresi ve Alanı',
    2.0, 2.0, 2.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    281,
    'MAT',
    '11',
    'Matematik:Katı Cisimler Dik Dairesel Silindir Alan ve Hacim Bağıntıları',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    282,
    'MAT',
    '11',
    'Matematik:Katı Cisimler Dik Dairesel Koni-Kürenin Alan ve Hacim Bağıntıları',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    283,
    'MAT',
    '11',
    'Matematik:Olasılık-Koşullu Olasılık',
    2.0, 2.0, 3.0, 2.0,
    3.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    284,
    'MAT',
    '11',
    'Matematik:Olasılık-Deneysel ve Teorik Olasılık',
    2.0, 2.0, 3.0, 2.0,
    3.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    285,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-Vektörler',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    286,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-Bağıl Hareket',
    0.0, 0.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    287,
    'FIZ',
    '11',
    'Fizik:Newton’un Hareket Yasaları',
    1.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    288,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-Bir Boyutta Sabit İvmeli Hareket',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    289,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-İki Boyutta Hareket',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    290,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-Enerji ve Hareket',
    0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    291,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-İtme ve Çizgisel Momentum',
    1.0, 1.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    292,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-Tork',
    1.0, 1.0, 1.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    293,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-Denge ve Denge Şartları',
    1.0, 1.0, 1.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    294,
    'FIZ',
    '11',
    'Fizik:Kuvvet ve Hareket-Basit Makineler',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    295,
    'FIZ',
    '11',
    'Fizik:Elektrik ve Manyetizma-Elektriksel Kuvvet ve Elektrik Alan',
    1.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    296,
    'FIZ',
    '11',
    'Fizik:Elektrik ve Manyetizma-Elektriksel Potansiyel',
    1.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    297,
    'FIZ',
    '11',
    'Fizik:Elektrik ve Manyetizma-Düzgün Elektrik Alan ve Sığa',
    1.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    298,
    'FIZ',
    '11',
    'Fizik:Elektrik ve Manyetizma-Manyetizma ve Elektromanyetik İndüklenme',
    1.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    299,
    'FIZ',
    '11',
    'Fizik:Elektrik ve Manyetizma-Alternatif Akım',
    1.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    300,
    'FIZ',
    '11',
    'Fizik:Elektrik ve Manyetizma-Transformatörler',
    1.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    301,
    'KIM',
    '11',
    'Kimya:Modern Atom Teorisi-Atomun Kuantum Modeli',
    0.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    302,
    'KIM',
    '11',
    'Kimya:Modern Atom Teorisi-Periyodik Sistem ve Elektron Dizilimleri',
    0.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    303,
    'KIM',
    '11',
    'Kimya:Modern Atom Teorisi-Periyodik Özellikler',
    0.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    304,
    'KIM',
    '11',
    'Kimya:Modern Atom Teorisi-Elementler',
    0.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    305,
    'KIM',
    '11',
    'Kimya:Modern Atom Teorisi-Yükseltgenme Basamakları',
    0.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    306,
    'KIM',
    '11',
    'Kimya:Gazlar-Gazların Özellikleri ve Gaz Yasaları',
    1.0, 1.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    307,
    'KIM',
    '11',
    'Kimya:Gazlar-İdeal Gaz Yasası',
    1.0, 1.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    308,
    'KIM',
    '11',
    'Kimya:Gazlar-Gazlara Kinetik Teori',
    1.0, 1.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    309,
    'KIM',
    '11',
    'Kimya:Gazlar-Gaz Karışımları',
    1.0, 1.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    310,
    'KIM',
    '11',
    'Kimya:Gazlar-Gerçek Gazlar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    311,
    'KIM',
    '11',
    'Kimya:Sıvı Çözeltiler ve Çözünürlük-Çözücü ve Çözünen Etkileşimleri',
    1.0, 1.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    312,
    'KIM',
    '11',
    'Kimya:Sıvı Çözeltiler ve Çözünürlük-Derişim Birimleri',
    1.0, 1.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    313,
    'KIM',
    '11',
    'Kimya:Sıvı Çözeltiler ve Çözünürlük-Koligatif Özellikler',
    1.0, 1.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    314,
    'KIM',
    '11',
    'Kimya:Sıvı Çözeltiler ve Çözünürlük-Çözünürlük',
    1.0, 1.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    315,
    'KIM',
    '11',
    'Kimya:Sıvı Çözeltiler ve Çözünürlük-Çözünürlüğe Etki Eden Faktörler',
    1.0, 1.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    316,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Enerji-Tepkimelerde Isı Değişimi',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    317,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Enerji-Oluşumu Entalpisi',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    318,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Enerji-Bağ Enerjileri',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    319,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Enerji-Tepkime Isılarının Toplanabilirliği',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    320,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Hız-Tepkime Hızları, Tepkime Hızını Etkileyen Faktörler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    321,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Denge-Kimyasal Denge',
    1.0, 2.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    322,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Denge-Dengeyi Etkileyen Faktörler',
    1.0, 2.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    323,
    'KIM',
    '11',
    'Kimya:Kimyasal Tepkimelerde Denge-Sulu Çözelti Dengeleri',
    1.0, 2.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    324,
    'BIO',
    '11',
    'Biyoloji:Denetleyici ve Düzenleyici Sistem, Duyu Organları-Sinir Sisteminin Yapı, Görev ve İşleyişi',
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    325,
    'BIO',
    '11',
    'Biyoloji:Denetleyici ve Düzenleyici Sistem, Duyu Organları-Duyu Organlarının Sağlıklı Yapısının Korunması',
    0.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    326,
    'BIO',
    '11',
    'Biyoloji:Denetleyici ve Düzenleyici Sistem, Duyu Organları-Duyu Organlarının Yapısı ve İşleyişi',
    0.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    327,
    'BIO',
    '11',
    'Biyoloji:Denetleyici ve Düzenleyici Sistem, Duyu Organları-Endokrin Bezler ve Salgıladıkları Hormonlar',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    328,
    'BIO',
    '11',
    'Biyoloji:Destek ve Hareket Sistemi-Destek ve Hareket Sisteminin Yapısı, Görevi ve İşleyişi',
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    329,
    'BIO',
    '11',
    'Biyoloji:Destek ve Hareket Sistemi-Destek ve Hareket Sistemi Rahatsızlıkları',
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    330,
    'BIO',
    '11',
    'Biyoloji:Destek ve Hareket Sistemi-Destek ve Hareket Sisteminin Sağlıklı Yapısının Korunması',
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    331,
    'BIO',
    '11',
    'Biyoloji:Sindirim Sistemi-Sindirim Sisteminin Yapısı, Görevi ve İşleyişi',
    0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    332,
    'BIO',
    '11',
    'Biyoloji:Sindirim Sistemi-Sindirim Sistemi Rahatsızlıkları',
    0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    333,
    'BIO',
    '11',
    'Biyoloji:Sindirim Sistemi-Sindirim Sisteminin Sağlıklı Yapısının Korunması',
    0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    334,
    'BIO',
    '11',
    'Biyoloji:Dolaşım Sistemleri-Kan ve Lenf Dolaşımı',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    335,
    'BIO',
    '11',
    'Biyoloji:Dolaşım Sistemleri-Dolaşım Sistemi Rahatsızlıkları',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    336,
    'BIO',
    '11',
    'Biyoloji:Dolaşım Sistemleri-Dolaşım Sisteminin Sağlıklı Yapısının Korunması',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    337,
    'BIO',
    '11',
    'Biyoloji:Dolaşım ve Bağışıklık Sistemi',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    338,
    'BIO',
    '11',
    'Biyoloji:Solunum Sistemi-Solunum Sisteminin Yapısı, Görevi ve İşleyişi',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    339,
    'BIO',
    '11',
    'Biyoloji:Solunum Sistemi-Alveollerden Dokulara ve Dokulardan Alveollere Gaz Taşınması',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    340,
    'BIO',
    '11',
    'Biyoloji:Solunum Sistemi-Solunum Sistemi Rahatsızlıkları ve Sağlıklı Yapısının Korunması',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    341,
    'BIO',
    '11',
    'Biyoloji:Üriner Sistem-Üriner Sistemin Yapısı, Görevi ve İşleyişi',
    0.0, 0.0, 1.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    342,
    'BIO',
    '11',
    'Biyoloji:Üriner Sistem-Homeostasinin Sağlanmasında Böbreklerin Rolü',
    0.0, 0.0, 1.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    343,
    'BIO',
    '11',
    'Biyoloji:Üriner Sistem-Üriner Sistem Rahatsızlıkları ve Sağlıklı Yapısının Korunması',
    0.0, 0.0, 1.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    344,
    'BIO',
    '11',
    'Biyoloji:Üreme Sistemi ve Embriyonik Gelişim-Üreme Sisteminin Yapısı, Görevi ve İşleyişi',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    345,
    'BIO',
    '11',
    'Biyoloji:Üreme Sistemi ve Embriyonik Gelişim-Üreme Sisteminin Sağlıklı Yapısının Korunması',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    346,
    'BIO',
    '11',
    'Biyoloji:Üreme Sistemi ve Embriyonik Gelişim-İnsanda Embriyonik Gelişim Süreci',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    347,
    'BIO',
    '11',
    'Biyoloji:Komünite ve Popülasyon Ekolojisi-Komünitenin Yapısına Etki Eden Faktörler',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    348,
    'BIO',
    '11',
    'Biyoloji:Komünite ve Popülasyon Ekolojisi-Komünitede Tür İçi ve Türler Arasındaki Rekabet',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    349,
    'BIO',
    '11',
    'Biyoloji:Komünite ve Popülasyon Ekolojisi-Komünitede Türler Arasında Simbiyotik İlişkiler',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    350,
    'BIO',
    '11',
    'Biyoloji:Komünite ve Popülasyon Ekolojisi-Popülasyonun Yapısı ve Dinamikleri',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    351,
    'BIO',
    '11',
    'Biyoloji:Komünite ve Popülasyon Ekolojisi-Popülasyon Ekolojisi',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    352,
    'EDB',
    '11',
    'Edebiyat:Giriş-Cumhuriyet Dönemi’nde Hikâye (1923-1940)',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    353,
    'EDB',
    '11',
    'Edebiyat:Giriş-Cumhuriyet Dönemi’nde Hikâye (1940-1960)',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    354,
    'EDB',
    '11',
    'Edebiyat:Giriş-Edebiyat ve Toplum İlişkisi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    355,
    'EDB',
    '11',
    'Edebiyat:Giriş-Edebiyatın Sanat Akımları ile İlişkisi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    356,
    'EDB',
    '11',
    'Edebiyat:Giriş-Hikâye',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    357,
    'EDB',
    '11',
    'Edebiyat:Giriş-Toplumcu Gerçekçilik',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    358,
    'EDB',
    '11',
    'Edebiyat:Şiir Bilgisi',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    359,
    'EDB',
    '11',
    'Edebiyat:Şiir-Cumhuriyet Dönemi’nin İlk Yıllarında Şiir',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    360,
    'EDB',
    '11',
    'Edebiyat:Şiir-Milli Edebiyat Dönemi Şiiri',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    361,
    'EDB',
    '11',
    'Edebiyat:Şiir-Saf Şiir',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    362,
    'EDB',
    '11',
    'Edebiyat:Şiir-Servetifünun Dönemi Şiiri',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    363,
    'EDB',
    '11',
    'Edebiyat:Şiir-Tanzimat Dönemi Şiiri',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    364,
    'EDB',
    '11',
    'Edebiyat:Şiir-Türkiye Dışındaki Çağdaş Türk Şiiri',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    365,
    'EDB',
    '11',
    'Edebiyat:Edebi Metinler',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    366,
    'EDB',
    '11',
    'Edebiyat:Makale-Araştırmaya Dayalı Metin Yazma Aşamaları',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    367,
    'EDB',
    '11',
    'Edebiyat:Makale-Makale',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    368,
    'EDB',
    '11',
    'Edebiyat:Makale-Münazara',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    369,
    'EDB',
    '11',
    'Edebiyat:Makale-Münazaranın Aşamaları',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    370,
    'EDB',
    '11',
    'Edebiyat:Tiyatro',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    371,
    'EDB',
    '11',
    'Edebiyat:Tiyatro-Cumhuriyet Dönemi’nde Tiyatro (1923-1950)',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    372,
    'EDB',
    '11',
    'Edebiyat:Tiyatro-Cumhuriyet Dönemi’nde Tiyatro (1950-1980)',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    373,
    'EDB',
    '11',
    'Edebiyat:Tiyatro-Dünya Edebiyatında Tiyatro',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    374,
    'EDB',
    '11',
    'Edebiyat:Tiyatro-Temel Tiyatro Terimleri',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    375,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    376,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Cumhuriyet Dönemi’nde Fıkra',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    377,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Cumhuriyet Dönemi’nde Sohbet',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    378,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Cumhuriyet Öncesinde Fıkra',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    379,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Cumhuriyet Öncesinde Sohbet',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    380,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Fıkra',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    381,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Sohbet',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    382,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Sohbet ve Fıkra Yazma Aşamaları',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    383,
    'EDB',
    '11',
    'Edebiyat:Sohbet ve Fıkra-Türklerde Sohbet Kültürü',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    384,
    'EDB',
    '11',
    'Edebiyat:Eleştiri',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    385,
    'EDB',
    '11',
    'Edebiyat:Eleştiri-Cumhuriyet Dönemi’nde Eleştiri',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    386,
    'EDB',
    '11',
    'Edebiyat:Eleştiri-Cumhuriyet Öncesinde Eleştiri',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    387,
    'EDB',
    '11',
    'Edebiyat:Eleştiri-Eleştiri',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    388,
    'EDB',
    '11',
    'Edebiyat:Eleştiri-Eleştiri Yazma Aşamaları',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    389,
    'EDB',
    '11',
    'Edebiyat:Mülakat ve Röportaj',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    390,
    'EDB',
    '11',
    'Edebiyat:Mülakat ve Röportaj-Cumhuriyet Dönemi’nde Mülakat',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    391,
    'EDB',
    '11',
    'Edebiyat:Mülakat ve Röportaj-Cumhuriyet Dönemi’nde Röportaj',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    392,
    'EDB',
    '11',
    'Edebiyat:Mülakat ve Röportaj-Cumhuriyet Öncesinde Mülakat',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    393,
    'EDB',
    '11',
    'Edebiyat:Mülakat ve Röportaj-Mülakat',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    394,
    'EDB',
    '11',
    'Edebiyat:Mülakat ve Röportaj-Mülakat Yazma Aşamaları',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    395,
    'EDB',
    '11',
    'Edebiyat:Mülakat ve Röportaj-Röportaj',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    396,
    'EDB',
    '11',
    'Edebiyat:Roman',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    397,
    'EDB',
    '11',
    'Edebiyat:Roman-Cumhuriyet Dönemi’nde Roman (1923-1950)',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    398,
    'EDB',
    '11',
    'Edebiyat:Roman-Cumhuriyet Dönemi’nde Roman (1950-1980)',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    399,
    'EDB',
    '11',
    'Edebiyat:Roman-Dünya Edebiyatında Roman',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    400,
    'EDB',
    '11',
    'Edebiyat:Roman-Modernizm Akımı',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    401,
    'TAR',
    '11',
    'Tarih:Değişen Dünya Dengeleri Karşısında Osmanlı Siyaseti (1595 – 1774)-1595 – 1700 Yılları Arasındaki Siyasi Gelişmeler, Uzun Savaşlardan Diplomasiye',
    0.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    402,
    'TAR',
    '11',
    'Tarih:Değişen Dünya Dengeleri Karşısında Osmanlı Siyaseti (1595 – 1774)-Fetihlerden Savunmaya',
    0.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    403,
    'TAR',
    '11',
    'Tarih:Değişen Dünya Dengeleri Karşısında Osmanlı Siyaseti (1595 – 1774)-Uzun Savaşlardan Diplomasiye',
    0.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    404,
    'TAR',
    '11',
    'Tarih:Değişen Dünya Dengeleri Karşısında Osmanlı Siyaseti (1595 – 1774)-XVII ve XVIII. Yüzyıllarda Osmanlı Devleti’nde ve Avrupa’da Denizcilik Faaliyetleri',
    0.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    405,
    'TAR',
    '11',
    'Tarih:Değişim Çağında Avrupa ve Osmanlı-Avrupa’da Değişim Çağı',
    0.0, 2.0, 2.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    406,
    'TAR',
    '11',
    'Tarih:Değişim Çağında Avrupa ve Osmanlı-Osmanlı Devleti’nde Değişim',
    0.0, 2.0, 2.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    407,
    'TAR',
    '11',
    'Tarih:Değişim Çağında Avrupa ve Osmanlı-Osmanlı Devleti’nde İsyanlar ve Düzeni Koruma Çabaları',
    0.0, 2.0, 2.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    408,
    'TAR',
    '11',
    'Tarih:Uluslararası İlişkilerde Denge Stratejisi (1774 – 1914)-XVIII – XX. Yüzyıl Siyasi Gelişmeleri (1774 – 1914)',
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    409,
    'TAR',
    '11',
    'Tarih:Uluslararası İlişkilerde Denge Stratejisi (1774 – 1914)-Osmanlı Topraklarını Paylaşma Mücadelesi',
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    410,
    'TAR',
    '11',
    'Tarih:Uluslararası İlişkilerde Denge Stratejisi (1774 – 1914)-Mehmet Ali Paşa’nın Güç Kazanması',
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    411,
    'TAR',
    '11',
    'Tarih:Uluslararası İlişkilerde Denge Stratejisi (1774 – 1914)-Osmanlı ve Rusya Rekabeti (1768 – 1914)',
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    412,
    'TAR',
    '11',
    'Tarih:Devrimler Çağında Değişen Devlet – Toplum İlişkileri-İhtilaller Çağı',
    0.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    413,
    'TAR',
    '11',
    'Tarih:Devrimler Çağında Değişen Devlet – Toplum İlişkileri-Osmanlı Devleti’nde Modern Orduya Geçiş',
    0.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    414,
    'TAR',
    '11',
    'Tarih:Devrimler Çağında Değişen Devlet – Toplum İlişkileri-XIX. Yüzyılda Sosyal Hayattaki Değişimler',
    0.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    415,
    'TAR',
    '11',
    'Tarih:Devrimler Çağında Değişen Devlet – Toplum İlişkileri-Osmanlı Devleti’nde Demokratikleşme Hareketleri',
    0.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    416,
    'TAR',
    '11',
    'Tarih:Devrimler Çağında Değişen Devlet – Toplum İlişkileri-Osmanlı Devleti’nde Darbeler',
    0.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    417,
    'TAR',
    '11',
    'Tarih:Sermaye ve Emek-El Emeğinden Makineleşmeye',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    418,
    'TAR',
    '11',
    'Tarih:Sermaye ve Emek-Osmanlı Devleti’nde Sanayileşme Çabaları',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    419,
    'TAR',
    '11',
    'Tarih:Sermaye ve Emek-Ekonomiyi Düzeltme Çabaları',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    420,
    'TAR',
    '11',
    'Tarih:XIX ve XX. Yüzyılda Değişen Gündelik Hayat-Ulus Devlete Giden Süreçte Nüfus',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    421,
    'TAR',
    '11',
    'Tarih:XIX ve XX. Yüzyılda Değişen Gündelik Hayat-Modern Hayattaki Sosyal Değişim',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    422,
    'COG',
    '11',
    'Coğrafya:Doğal Sistemler-Yeryüzünde Biyoçeşitlilik',
    0.0, 3.0, 3.0, 3.0,
    4.0, 4.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    423,
    'COG',
    '11',
    'Coğrafya:Doğal Sistemler-Enerji Akışı ve Madde Döngüleri',
    0.0, 3.0, 3.0, 3.0,
    4.0, 4.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    424,
    'COG',
    '11',
    'Coğrafya:Doğal Sistemler-Su Ekosistemlerinin İşleyişi',
    0.0, 3.0, 3.0, 3.0,
    4.0, 4.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    425,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Nüfus Politikaları',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    426,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Türkiye’nin Nüfus Politikaları ve Nüfus Projeksiyonları',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    427,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Şehirlerin Gelişimi ve Fonksiyonları ve Etki Alanları',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    428,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Türkiye’de Fonksiyonlarına Göre Şehirler ve Kır Yerleşmeleri',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    429,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Üretim, Doğal ve Beşeri Unsurların Dağıtım ve Tüketime Etkisi',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    430,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Doğal Kaynaklar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    431,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Türkiye''de Uygulaman Ekonomi Politikaları ve Ekonomisinin Sektörel Dağılımı',
    4.0, 2.0, 1.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    432,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Tarım ve Hayvancılığın Türkiye Ekonomisindeki Yeri',
    4.0, 2.0, 1.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    433,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Türkiye’de Madencilik ve Enerji Kaynakları',
    4.0, 2.0, 1.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    434,
    'COG',
    '11',
    'Coğrafya:Beşeri Sistemleri-Türkiye’de Sanayi',
    4.0, 2.0, 1.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    435,
    'COG',
    '11',
    'Coğrafya:Bölgeler ve Ülkeler-İlk Uygarlıklar, Kültür Merkezleri',
    1.0, 1.0, 2.0, 2.0,
    4.0, 4.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    436,
    'COG',
    '11',
    'Coğrafya:Bölgeler ve Ülkeler-Türk Kültürü',
    1.0, 1.0, 2.0, 2.0,
    4.0, 4.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    437,
    'COG',
    '11',
    'Coğrafya:Bölgeler ve Ülkeler-Uygarlıkların Merkezi: Anadolu',
    1.0, 1.0, 2.0, 2.0,
    4.0, 4.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    438,
    'COG',
    '11',
    'Coğrafya:Bölgeler ve Ülkeler-Ham Madde, Üretim, Pazar',
    1.0, 1.0, 2.0, 2.0,
    4.0, 4.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    439,
    'COG',
    '11',
    'Coğrafya:Bölgeler ve Ülkeler-Uluslararası Turizm',
    1.0, 1.0, 2.0, 2.0,
    4.0, 4.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    440,
    'COG',
    '11',
    'Coğrafya:Bölgeler ve Ülkeler-Küresel ve Bölgesel Örgütler',
    1.0, 1.0, 2.0, 2.0,
    4.0, 4.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    441,
    'COG',
    '11',
    'Coğrafya:Çevre ve Toplum-Çevre Sorunlarının Sebepleri',
    0.0, 1.0, 3.0, 3.0,
    1.0, 1.0, 4.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    442,
    'COG',
    '11',
    'Coğrafya:Çevre ve Toplum-Madenlerin ve Enerji Kaynaklarını Kullanımı, Yenilenemeyen Kaynakların Kullanımı',
    0.0, 1.0, 3.0, 3.0,
    1.0, 1.0, 4.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    443,
    'COG',
    '11',
    'Coğrafya:Çevre ve Toplum-Doğal Kaynakların Kullanımı ve Arazi Kullanım Şeklinin Çevreye Etkisi',
    0.0, 1.0, 3.0, 3.0,
    1.0, 1.0, 4.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    444,
    'COG',
    '11',
    'Coğrafya:Çevre ve Toplum-Küresel Çevre Sorunlarının Ortaya Çıkması ve Yayılması',
    0.0, 1.0, 3.0, 3.0,
    1.0, 1.0, 4.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    445,
    'COG',
    '11',
    'Coğrafya:Çevre ve Toplum-Doğal Kaynakların Kullanımı ve Geri Dönüşüm',
    0.0, 1.0, 3.0, 3.0,
    1.0, 1.0, 4.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    446,
    'DIN',
    '11',
    'Din:Dünya ve Ahiret',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    447,
    'DIN',
    '11',
    'Din:Dünya ve Ahiret-Ahiret Âlemi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    448,
    'DIN',
    '11',
    'Din:Dünya ve Ahiret-Ahirete Uğurlama',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    449,
    'DIN',
    '11',
    'Din:Dünya ve Ahiret-Kur’an’dan Mesajlar: Bakara Suresi 153-157. Ayetler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    450,
    'DIN',
    '11',
    'Din:Dünya ve Ahiret-Varoluşun ve Hayatın Anlamı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    451,
    'DIN',
    '11',
    'Din:Kur’an’a Göre Hz. Muhammed',
    2.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    452,
    'DIN',
    '11',
    'Din:Kur’an’a Göre Hz. Muhammed-Hz. Muhammed’e Bağlılık ve İtaat',
    2.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    453,
    'DIN',
    '11',
    'Din:Kur’an’a Göre Hz. Muhammed-Hz. Muhammed’in Peygamberlik Yönü',
    2.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    454,
    'DIN',
    '11',
    'Din:Kur’an’a Göre Hz. Muhammed-Hz. Muhammed’in Şahsiyeti',
    2.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    455,
    'DIN',
    '11',
    'Din:Kur’an’a Göre Hz. Muhammed-Kur’an’dan Mesajlar: Ahzâb Suresi 25, 45 ve 46. Ayetler',
    2.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    456,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    457,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-Allah İçin Samimiyet: İhlas',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    458,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-Allah Yolunda Mücahede: Cihat',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    459,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-Allah’ı Görüyormuşçasına Yaşamak: İhsan',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    460,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-Allah’ın Emir ve Yasaklarına Riayet: Takva',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    461,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-Dosdoğru Yol: Sırat-ı Mustakim',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    462,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-İslam’ın Aydınlık Yolu: Hidayet',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    463,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-İyi, Doğru ve Güzel Davranış: Salih Amel',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    464,
    'DIN',
    '11',
    'Din:Kur’an’da Bazı Kavramlar-Kur’an’dan Mesajlar: Kehf Suresi 107-110. Ayetler',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    465,
    'DIN',
    '11',
    'Din:İnançla İlgili Meseleler',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    466,
    'DIN',
    '11',
    'Din:İnançla İlgili Meseleler-İnançla İlgili Felsefi Yaklaşımlar',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    467,
    'DIN',
    '11',
    'Din:İnançla İlgili Meseleler-Kur’an’dan Mesajlar: En’âm Suresi 59. Ayet ve Lokmân Suresi 27. Ayet',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    468,
    'DIN',
    '11',
    'Din:İnançla İlgili Meseleler-Yeni Dinî Hareketler',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    469,
    'DIN',
    '11',
    'Din:Yaşayan Dinler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    470,
    'DIN',
    '11',
    'Din:Yahudilik ve Hristiyanlık',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    471,
    'DIN',
    '11',
    'Din:Yahudilik ve Hristiyanlık-Hristiyanlık',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    472,
    'DIN',
    '11',
    'Din:Yahudilik ve Hristiyanlık-Yahudilik',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    473,
    'MAT',
    '12',
    'matematik:Üstel ve Logaritmik Fonksiyonlar-Üstel Fonksiyon',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    474,
    'MAT',
    '12',
    'matematik:Üstel ve Logaritmik Fonksiyonlar-Logaritma Fonksiyonu',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    475,
    'MAT',
    '12',
    'matematik:Üstel ve Logaritmik Fonksiyonlar-Üstel Denklemler',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    476,
    'MAT',
    '12',
    'matematik:Üstel ve Logaritmik Fonksiyonlar-Logaritmik Denklemler ve Eşitsizlikler',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    477,
    'MAT',
    '12',
    'matematik:Üstel ve Logaritmik Fonksiyonlar-Üstel Eşitsizlikler',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    478,
    'MAT',
    '12',
    'matematik:Üstel ve Logaritmik Fonksiyonlar-Logaritmik Eşitsizlikler',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    479,
    'MAT',
    '12',
    'matematik:Üstel ve Logaritmik Fonksiyonlar-Üstel ve Logaritmik Fonksiyonlarla Modelleme',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    480,
    'MAT',
    '12',
    'matematik:Diziler-Gerçek Sayı Dizileri, Dizi, Sabit Dizi',
    1.0, 1.0, 2.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    481,
    'MAT',
    '12',
    'matematik:Diziler-Gerçek Sayı Dizileri, Aritmetik Diziler ve Özellikleri',
    1.0, 1.0, 2.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    482,
    'MAT',
    '12',
    'matematik:Diziler-Gerçek Sayı Dizileri, Geometrik Diziler ve Özellikleri',
    1.0, 1.0, 2.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    483,
    'MAT',
    '12',
    'matematik:Diziler-Gerçek Sayı Dizileri, Fibonacci Dizisi',
    1.0, 1.0, 2.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    484,
    'MAT',
    '12',
    'Matematik:Trigonometri-Toplam,Fark Formülleri',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    485,
    'MAT',
    '12',
    'Matematik:Trigonometri-Toplam,Fark Formülleri, Kosinüs İçin',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    486,
    'MAT',
    '12',
    'Matematik:Trigonometri-Toplam,Fark Formülleri, Sinüs İçin',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    487,
    'MAT',
    '12',
    'Matematik:Trigonometri-Toplam,Fark Formülleri, Tanjant ve Kotanjant İçin',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    488,
    'MAT',
    '12',
    'Matematik:Trigonometri-İki Kat Açı Formülleri, Kosinüs İçin',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    489,
    'MAT',
    '12',
    'Matematik:Trigonometri-İki Kat Açı Formülleri, Sinüs İçin',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    490,
    'MAT',
    '12',
    'Matematik:Trigonometri-İki Kat Açı Formülleri, Tanjant ve Kotanjant İçin',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    491,
    'MAT',
    '12',
    'Matematik:Trigonometri-Trigonometrik Denklemler',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    492,
    'MAT',
    '12',
    'Matematik:Trigonometri-Trigonometrik Denklemler, Çarpanlara Ayırarak Çözümü',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    493,
    'MAT',
    '12',
    'Matematik:Trigonometri-Trigonometrik Denklemler, Özdeşlikler Yardımı ile Denklem Çözümü',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    494,
    'MAT',
    '12',
    'Matematik:Dönüşümler-Analitik Düzlemde Temel Dönüşümler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    495,
    'MAT',
    '12',
    'matematik:Türev-Limit ve Süreklilik',
    1.0, 4.0, 0.0, 3.0,
    4.0, 0.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    496,
    'MAT',
    '12',
    'matematik:Türev-Anlık Değişim Oranı ve Türev',
    1.0, 4.0, 0.0, 3.0,
    4.0, 0.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    497,
    'MAT',
    '12',
    'matematik:Türev-Türevin Uygulamaları',
    1.0, 4.0, 0.0, 3.0,
    4.0, 0.0, 3.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    498,
    'MAT',
    '12',
    'matematik:İntegral-Belirsiz İntegral',
    3.0, 4.0, 0.0, 4.0,
    4.0, 0.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    499,
    'MAT',
    '12',
    'matematik:İntegral-Belirli İntegral ve Uygulamaları',
    3.0, 4.0, 0.0, 4.0,
    4.0, 0.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    500,
    'MAT',
    '12',
    'matematik:Analitik Geometri-Çemberin Analitik İncelenmesi',
    1.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    501,
    'FIZ',
    '12',
    'Fizik:Çembersel Hareket, Düzgün Çembersel Hareket, Merkezcil Kuvvet ve Bağlı Olduğu Değişkenler',
    2.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    502,
    'FIZ',
    '12',
    'Fizik:Çembersel Hareket, Düzgün Çembersel Hareket, Hareket Analizi ve Araçların Emniyetli Dönüş Şartları',
    2.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    503,
    'FIZ',
    '12',
    'Fizik: Çembersel Hareket-Dönerek Öteleme Hareketi',
    2.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    504,
    'FIZ',
    '12',
    'Fizik: Çembersel Hareket-Açısal Momentum',
    0.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    505,
    'FIZ',
    '12',
    'Fizik: Çembersel Hareket-Kütle Çekim Kuvveti',
    2.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    506,
    'FIZ',
    '12',
    'Fizik: Çembersel Hareket-Kepler Kanunları',
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    507,
    'FIZ',
    '12',
    'Fizik:Basit Harmonik Hareket',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    508,
    'FIZ',
    '12',
    'Fizik: Dalga Mekaniği-Dalgalarda Kırınım, Girişim ve Doppler Olayı',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    509,
    'FIZ',
    '12',
    'Fizik:Dalga Mekaniği-Elektromanyetik Dalgalar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    510,
    'FIZ',
    '12',
    'Fizik: Atom Fiziğine Giriş ve Radyoaktivite-Atom Kavramının Tarihsel Gelişimi, Uyarılma Yolları, Modern Atom Teorisi',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    511,
    'FIZ',
    '12',
    'Fizik: Atom Fiziğine Giriş ve Radyoaktivite-Büyük Patlama ve Evrenin Oluşumu',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    512,
    'FIZ',
    '12',
    'Fizik: Atom Fiziğine Giriş ve Radyoaktivite-Radyoaktivite',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    513,
    'FIZ',
    '12',
    'Fizik:Modern Fizik-Özel Görelillik',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    514,
    'FIZ',
    '12',
    'Fizik: Modern Fizik-Kuantum Fiziğine Giriş',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    515,
    'FIZ',
    '12',
    'Fizik: Modern Fizik-Fotoelektrik Olayı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    516,
    'FIZ',
    '12',
    'Fizik: Modern Fizik-Compton Saçılması ve De Broglie Dalga Boyu',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    517,
    'KIM',
    '12',
    'Kimya: Kimya ve Elektrik-İndirgenme ve Yükseltgenme Tepkimelerinde Elektrik Akımı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    518,
    'KIM',
    '12',
    'Kimya: Kimya ve Elektrik-Elektrotlar ve Elektrokimyasal Hücreler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    519,
    'KIM',
    '12',
    'Kimya: Kimya ve Elektrik-Elektrot Potansiyelleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    520,
    'KIM',
    '12',
    'Kimya: Kimya ve Elektrik-Kimyasallardan Elektrik Üretimi, Elektroliz ve Korozyon',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    521,
    'KIM',
    '12',
    'Kimya: Karbon Kimyasına Giriş-Anorganik ve Organik Bileşikler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    522,
    'KIM',
    '12',
    'Kimya: Karbon Kimyasına Giriş-Basit Formül ve Molekül Formülü, Doğada Karbon',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    523,
    'KIM',
    '12',
    'Kimya: Karbon Kimyasına Giriş-Lewis Formülleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    524,
    'KIM',
    '12',
    'Kimya: Karbon Kimyasına Giriş-Hibritleşme, Molekül Geometrileri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    525,
    'KIM',
    '12',
    'Kimya: Organik Bileşikler-Hidrokarbonlar, Sınıflandırma, Alkanlar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    526,
    'KIM',
    '12',
    'Kimya: Organik Bileşikler-Hidrokarbonlar, Sınıflandırma, Alkenler, Alkinler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    527,
    'KIM',
    '12',
    'Kimya: Organik Bileşikler-Fonksiyonel Gruplar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    528,
    'KIM',
    '12',
    'Kimya: Organik Bileşikler-Alkoller',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    529,
    'KIM',
    '12',
    'Kimya: Organik Bileşikler-Eterler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    530,
    'KIM',
    '12',
    'Kimya: Organik Bileşikler-Karbonil Bileşikler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    531,
    'KIM',
    '12',
    'Kimya: Organik Bileşikler-Karboksilik Asitler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    532,
    'BIO',
    '12',
    'Kimya: Organik Bileşikler-Esterler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    533,
    'BIO',
    '12',
    'Biyoloji: Genden Proteine-Nükleik Asitlerin Keşfi ve Önemi',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    534,
    'BIO',
    '12',
    'Biyoloji: Genden Proteine-Nükleik Asitlerin Çeşitleri ve Görevleri (DNA,RNA)',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    535,
    'BIO',
    '12',
    'Biyoloji: Genden Proteine-Hücredeki Genetik materyalin Organizasyonu, DNA''nın Eşlenmesi',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    536,
    'BIO',
    '12',
    'Biyoloji: Genden Proteine-Genetik Şifre ve Protein Sentezi, Protein Sentezi Mekanizması',
    3.0, 1.0, 2.0, 2.0,
    2.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    537,
    'BIO',
    '12',
    'Biyoloji: Genden Proteine-Genetik Şifre ve Protein Sentezi',
    3.0, 1.0, 2.0, 2.0,
    2.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    538,
    'BIO',
    '12',
    'Biyoloji: Genden Proteine-Genetik Mühendisliği ve Biyoteknoloji Uygulamaları',
    3.0, 1.0, 2.0, 2.0,
    2.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    539,
    'BIO',
    '12',
    'Biyoloji: Genden Proteine-Genetik Mühendisliği ve Biyoteknoloji Uygulamalarının İnsan Hayatına Etkisi',
    3.0, 1.0, 2.0, 2.0,
    2.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    540,
    'BIO',
    '12',
    'Biyoloji: Canlılarda Enerji Dönüşümleri-Canlılık ve Enerji',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    541,
    'BIO',
    '12',
    'Biyoloji: Canlılarda Enerji Dönüşümleri-Fotosentez',
    1.0, 1.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    542,
    'BIO',
    '12',
    'Biyoloji: Canlılarda Enerji Dönüşümleri-Kemosentez',
    1.0, 1.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    543,
    'BIO',
    '12',
    'Biyoloji: Canlılarda Enerji Dönüşümleri-Hücresel Solunum',
    0.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    544,
    'BIO',
    '12',
    'Biyoloji: Bitki Biyolojisi-Bitkilerin Yapısı, Çiçekli Bitkilerin Temel Kısımları',
    2.0, 3.0, 0.0, 2.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    545,
    'BIO',
    '12',
    'Biyoloji: Bitki Biyolojisi-Bitkilerin Yapısı, Bitki Gelişiminde Hormonların Etkisi',
    2.0, 3.0, 0.0, 2.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    546,
    'BIO',
    '12',
    'Biyoloji: Bitki Biyolojisi-Bitkilerin Yapısı, Bitkilerde Gözlenebilen Hareketler',
    2.0, 3.0, 0.0, 2.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    547,
    'BIO',
    '12',
    'Biyoloji: Bitki Biyolojisi-Bitkilerde Madde Taşınması',
    2.0, 3.0, 0.0, 2.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    548,
    'BIO',
    '12',
    'Biyoloji: Bitki Biyolojisi-Bitkilerde Eşeyli Üreme',
    2.0, 3.0, 0.0, 2.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    549,
    'COG',
    '12',
    'Biyoloji:Canlılar ve Çevre',
    1.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    550,
    'COG',
    '12',
    'Coğrafya:Doğal Sistemler-Ekstrem Doğa Olayları ve Doğa Olaylarının Geleceği',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    551,
    'COG',
    '12',
    'Coğrafya:Beşeri Sistemler-Ekonomi Şehirleşme ve Göç',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    552,
    'COG',
    '12',
    'Coğrafya:Beşeri Sistemler-Türkiye''nin İşlevsel Bölgeleri ve Kalkınma Projeleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    553,
    'COG',
    '12',
    'Coğrafya:Beşeri Sistemler-Küresel Ticaret',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    554,
    'COG',
    '12',
    'Coğrafya:Beşeri Sistemler-Türkiye''de Turizm',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    555,
    'COG',
    '12',
    'Coğrafya:Küresel Ortam-Bölgeler ve Ülkeler, Jeopolitik Konum',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    556,
    'COG',
    '12',
    'Coğrafya:Küresel Ortam-Bölgeler ve Ülkeler, Ülkeler Arası Etkileşim',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    557,
    'COG',
    '12',
    'Coğrafya:Küresel Ortam-TÜM',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    558,
    'COG',
    '12',
    'Coğrafya:Çevre ve Toplum-Çevre Sorunlarının Çözümüne Yönelik Yaklaşımlar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    559,
    'DIN',
    '12',
    'Din:İslam ve Bilim',
    0.0, 1.0, 2.0, 1.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    560,
    'DIN',
    '12',
    'Din:Anadolu’da İslam',
    0.0, 0.0, 0.0, 1.0,
    0.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    561,
    'DIN',
    '12',
    'Din:İslam Düşüncesinde Tasavvufi Yorumlar ve Mezhepler',
    0.0, 2.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    562,
    'DIN',
    '12',
    'Din:Güncel Dini Meseleler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    563,
    'DIN',
    '12',
    'Din:Yaşayan Dinler-Hint Çin Dinleri',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    564,
    'FEL',
    '12',
    'Felsefe:Felsefe ve Bilim',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    565,
    'FEL',
    '12',
    'Felsefe:Bilgi Felsefesi',
    1.0, 2.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    566,
    'FEL',
    '12',
    'Felsefe:Varlık Felsefesi',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    567,
    'FEL',
    '12',
    'Felsefe:Ahlak Felsefesi',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    568,
    'FEL',
    '12',
    'Felsefe:Sanat Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    569,
    'FEL',
    '12',
    'Felsefe:Din Felsefesi',
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    570,
    'FEL',
    '12',
    'Felsefe:20. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    571,
    'FEL',
    '12',
    'Felsefe:15. Yüzyıl – 17. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    572,
    'FEL',
    '12',
    'Felsefe:18. Yüzyıl – 19. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    573,
    'FEL',
    '12',
    'Felsefe:Felsefe’nin Konusu',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    574,
    'FEL',
    '12',
    'Felsefe:İlk Çağ Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    575,
    'FEL',
    '12',
    'Felsefe:MÖ 6. Yüzyıl – MS 2. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    576,
    'FEL',
    '12',
    'Felsefe:MS 2. Yüzyıl – MS 15. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    577,
    'FEL',
    '12',
    'Felsefe:Siyaset Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    578,
    'MAN',
    '12',
    'Mantık: -Mantığa Giriş',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    579,
    'MAN',
    '12',
    'Mantık: -Mantığa Giriş-Doğru Düşünme',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    580,
    'MAN',
    '12',
    'Mantık: -Mantığa Giriş-Mantığın Uygulama Alanı',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    581,
    'MAN',
    '12',
    'Mantık: -Klasik Mantık',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    582,
    'MAN',
    '12',
    'Mantık: -Klasik Mantık-Kavram ve Terim',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    583,
    'MAN',
    '12',
    'Mantık: -Klasik Mantık-Tanım',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    584,
    'MAN',
    '12',
    'Mantık: -Klasik Mantık-Önerme',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    585,
    'MAN',
    '12',
    'Mantık: -Klasik Mantık-Çıkarım',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    586,
    'MAN',
    '12',
    'Mantık: -Mantık ve Dil',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    587,
    'MAN',
    '12',
    'Mantık: -Mantık ve Dil-Dilin Farklı Görevleri',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    588,
    'MAN',
    '12',
    'Mantık: -Mantık ve Dil-Anlama ve Tanımlama',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    589,
    'MAN',
    '12',
    'Mantık: -Sembolik Mantık',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    590,
    'MAN',
    '12',
    'Mantık: -Sembolik Mantık-Önermeler Mantığı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    591,
    'MAN',
    '12',
    'Mantık: -Sembolik Mantık-Niceleme Mantığı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    592,
    'MAN',
    '12',
    'Mantık: -Sembolik Mantık-Çok değerli Mantık',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    593,
    'PSI',
    '12',
    'Psikoloji -Psikoloji Bilimini Tanıyalım',
    0.0, 1.0, 3.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    594,
    'PSI',
    '12',
    'Psikoloji -Psikolojinin Temel Süreçleri',
    0.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    595,
    'PSI',
    '12',
    'Psikoloji -Öğrenme Bellek Düşünme',
    2.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    596,
    'PSI',
    '12',
    'Psikoloji -Ruh Sağlığının Temelleri',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    597,
    'SOS',
    '12',
    'Sosyoloji:Sosyolojiye Giriş',
    0.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    598,
    'SOS',
    '12',
    'Sosyoloji:Birey ve Toplum',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    599,
    'SOS',
    '12',
    'Sosyoloji:Toplumsal Yapı',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    600,
    'SOS',
    '12',
    'Sosyoloji:Toplumsal Değişme ve Gelişme',
    1.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    601,
    'SOS',
    '12',
    'Sosyoloji:Toplum ve Kültür',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    602,
    'SOS',
    '12',
    'Sosyoloji:Toplumsal Kurumlar',
    1.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    603,
    'MAT',
    'tyt',
    'Matematik:Olasılık',
    2.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    604,
    'MAT',
    'tyt',
    'Matematik:Permütasyon ve Kombinasyon',
    1.0, 1.0, 2.0, 0.0,
    0.0, 1.0, 3.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    605,
    'MAT',
    'tyt',
    'Matematik:Oran Orantı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    606,
    'MAT',
    'tyt',
    'Matematik:Mutlak Değer',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    607,
    'MAT',
    'tyt',
    'Matematik:Modüler Aritmetik',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    608,
    'MAT',
    'tyt',
    'Matematik:Problemler',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    609,
    'MAT',
    'tyt',
    'Matematik:Problemler– Hareket Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    610,
    'MAT',
    'tyt',
    'Matematik:Problemler– İşçi Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    611,
    'MAT',
    'tyt',
    'Matematik:Problemler– Kar Zarar Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    612,
    'MAT',
    'tyt',
    'Matematik:Problemler– Karışım Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    613,
    'MAT',
    'tyt',
    'Matematik:Problemler– Kesir Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    614,
    'MAT',
    'tyt',
    'Matematik:Problemler– Rutin Olmayan Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    615,
    'MAT',
    'tyt',
    'Matematik:Problemler– Sayı Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    616,
    'MAT',
    'tyt',
    'Matematik:Problemler– Tablo-Grafik Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    617,
    'MAT',
    'tyt',
    'Matematik:Problemler– Yaş Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    618,
    'MAT',
    'tyt',
    'Matematik:Problemler– Yüzde Problemleri',
    11.0, 12.0, 13.0, 13.0,
    13.0, 10.0, 11.0, 11.0
);

INSERT INTO excel_topic_data VALUES (
    619,
    'MAT',
    'tyt',
    'Matematik:Temel Kavramlar',
    4.0, 1.0, 1.0, 3.0,
    3.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    620,
    'MAT',
    'tyt',
    'Matematik:Sayı Basamakları',
    1.0, 2.0, 1.0, 2.0,
    1.0, 1.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    621,
    'MAT',
    'tyt',
    'Matematik:İşlem',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    622,
    'MAT',
    'tyt',
    'Matematik:Kümeler-Kartezyen Çarpım',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    623,
    'MAT',
    'tyt',
    'Matematik:Mantık',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    624,
    'MAT',
    'tyt',
    'Matematik:Fonskiyonlar',
    1.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    625,
    'MAT',
    'tyt',
    'Matematik:Bölme ve Bölünebilme',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    626,
    'MAT',
    'tyt',
    'Matematik:Basit Eşitsizlikler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 3.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    627,
    'MAT',
    'tyt',
    'Matematik:Denklem Çözme',
    0.0, 2.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    628,
    'MAT',
    'tyt',
    'Matematik:Üslü Sayılar',
    2.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    629,
    'MAT',
    'tyt',
    'Matematik:Çarpanlara Ayırma',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    630,
    'MAT',
    'tyt',
    'Matematik:Köklü Sayılar',
    2.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    631,
    'MAT',
    'tyt',
    'Matematik:EBOB – EKOK',
    0.0, 0.0, 2.0, 0.0,
    0.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    632,
    'MAT',
    'tyt',
    'Matematik:Rasyonel Sayılar',
    1.0, 0.0, 3.0, 3.0,
    1.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    633,
    'MAT',
    'tyt',
    'Matematik:Polinomlar',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    634,
    'MAT',
    'tyt',
    'Matematik:Veri – İstatistik',
    0.0, 0.0, 1.0, 0.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    635,
    'MAT',
    'tyt',
    'Matematik:Grafik Okuma',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    636,
    'MAT',
    'tyt',
    'Matematik:Faktöriyel',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    637,
    'MAT',
    'tyt',
    'Matematik:Analitik Geometri',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    638,
    'MAT',
    'tyt',
    'Matematik:Analitik Geometri-Doğrunun Analitiği',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    639,
    'MAT',
    'tyt',
    'Matematik:Analitik Geometri-Noktanın Analitiği',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    640,
    'MAT',
    'tyt',
    'Matematik:Çember ve Daire',
    1.0, 2.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    641,
    'MAT',
    'tyt',
    'Matematik:Çember ve Daire-Çemberde Açı',
    1.0, 2.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    642,
    'MAT',
    'tyt',
    'Matematik:Çember ve Daire-Çemberde Uzunluk',
    1.0, 2.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    643,
    'MAT',
    'tyt',
    'Matematik:Çember ve Daire-Dairede Alan',
    1.0, 2.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    644,
    'MAT',
    'tyt',
    'Matematik:Katı Cisimler',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    645,
    'MAT',
    'tyt',
    'Matematik:Katı Cisimler-Koni',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    646,
    'MAT',
    'tyt',
    'Matematik:Katı Cisimler-Küp',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    647,
    'MAT',
    'tyt',
    'Matematik:Katı Cisimler-Küre',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    648,
    'MAT',
    'tyt',
    'Matematik:Katı Cisimler-Piramit',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    649,
    'MAT',
    'tyt',
    'Matematik:Katı Cisimler-Prizmalar',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    650,
    'MAT',
    'tyt',
    'Matematik:Katı Cisimler-Silindir',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    651,
    'MAT',
    'tyt',
    'Matematik:Yamuk',
    1.0, 0.0, 2.0, 0.0,
    0.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    652,
    'MAT',
    'tyt',
    'Matematik:Çokgenler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    653,
    'MAT',
    'tyt',
    'Matematik:Üçgende Açı',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    654,
    'MAT',
    'tyt',
    'Matematik:Üçgende Açı-Eşkenar Üçgende Açı',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    655,
    'MAT',
    'tyt',
    'Matematik:Üçgende Açı-İkizkenar Üçgende Açı',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    656,
    'MAT',
    'tyt',
    'Matematik:Üçgende Alan',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    657,
    'MAT',
    'tyt',
    'Matematik:Üçgende Çevre',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    658,
    'MAT',
    'tyt',
    'Matematik:Üçgende Eşlik – Benzerlik',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    659,
    'MAT',
    'tyt',
    'Matematik:Üçgende Merkezler',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    660,
    'MAT',
    'tyt',
    'Matematik:Özel Üçgenler',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    661,
    'MAT',
    'tyt',
    'Matematik:Özel Üçgenler– Dik Üçgen',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    662,
    'MAT',
    'tyt',
    'Matematik:Özel Üçgenler– Eşkenar Üçgen',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    663,
    'MAT',
    'tyt',
    'Matematik:Özel Üçgenler– İkizkenar Üçgen',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    664,
    'MAT',
    'tyt',
    'Matematik:Kenarortay',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    665,
    'MAT',
    'tyt',
    'Matematik:Açı – Kenar Bağıntıları',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    666,
    'MAT',
    'tyt',
    'Matematik:Açıortay',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    667,
    'MAT',
    'tyt',
    'Matematik:Doğruda Açı',
    3.0, 1.0, 2.0, 4.0,
    4.0, 5.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    668,
    'MAT',
    'tyt',
    'Matematik:Eşkenar Dörtgen',
    0.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    669,
    'MAT',
    'tyt',
    'Matematik:Kare',
    1.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    670,
    'MAT',
    'tyt',
    'Matematik:Dikdörtgen',
    2.0, 2.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    671,
    'MAT',
    'tyt',
    'Matematik:Deltoid',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    672,
    'MAT',
    'tyt',
    'Matematik:Dörtgenler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    673,
    'MAT',
    'tyt',
    'Matematik:Ek Çizimler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    674,
    'MAT',
    'tyt',
    'Matematik:Paralelkenar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    675,
    'FIZ',
    'tyt',
    'Fizik:Fizik Bilimine Giriş',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    676,
    'FIZ',
    'tyt',
    'Fizik:Madde ve Özellikleri',
    0.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    677,
    'FIZ',
    'tyt',
    'Fizik:Hareket ve Kuvvet',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    678,
    'FIZ',
    'tyt',
    'Fizik:İş, Güç ve Enerji',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    679,
    'FIZ',
    'tyt',
    'Fizik:Isı ve Sıcaklık',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    680,
    'FIZ',
    'tyt',
    'Fizik:Isı, Sıcaklık ve Genleşme',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    681,
    'FIZ',
    'tyt',
    'Fizik:Elektrostatik',
    1.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    682,
    'FIZ',
    'tyt',
    'Fizik:Elektrik',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    683,
    'FIZ',
    'tyt',
    'Fizik:Manyetizma',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    684,
    'FIZ',
    'tyt',
    'Fizik:Elektrik Akımı',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    685,
    'FIZ',
    'tyt',
    'Fizik:Elektrik ve Manyetizma',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    686,
    'FIZ',
    'tyt',
    'Fizik:Basınç',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    687,
    'FIZ',
    'tyt',
    'Fizik:Basınç-Açık Hava Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    688,
    'FIZ',
    'tyt',
    'Fizik:Basınç-Gaz Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    689,
    'FIZ',
    'tyt',
    'Fizik:Basınç-Katı Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    690,
    'FIZ',
    'tyt',
    'Fizik:Basınç-Sıvı Basıncı',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    691,
    'FIZ',
    'tyt',
    'Fizik:Kaldırma Kuvveti',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    692,
    'FIZ',
    'tyt',
    'Fizik:Dalgalar',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    693,
    'FIZ',
    'tyt',
    'Fizik:Ses ve Deprem Dalgası',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    694,
    'FIZ',
    'tyt',
    'Fizik:Su Dalgaları',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    695,
    'FIZ',
    'tyt',
    'Fizik:Optik',
    2.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    696,
    'FIZ',
    'tyt',
    'Fizik:Işık Akışı, Aydınlatma, Gölge',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    697,
    'FIZ',
    'tyt',
    'Fizik:Yansıma ve Düzlem Aynalar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    698,
    'KIM',
    'tyt',
    'Kimya:Kimya Bilimi',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    699,
    'KIM',
    'tyt',
    'Kimya: Atom ve Yapısı',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    700,
    'KIM',
    'tyt',
    'Kimya:Atom ve Periyodik Sistem',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    701,
    'KIM',
    'tyt',
    'Kimya: Periyodik Sistem',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    702,
    'KIM',
    'tyt',
    'Kimya: Periyodik Sistem ve Değişen Özellikleri',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    703,
    'KIM',
    'tyt',
    'Kimya: Periyodik Sistem ve Özellikleri',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    704,
    'KIM',
    'tyt',
    'Kimya:Kimyasal Türler Arası Etkileşimler',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    705,
    'KIM',
    'tyt',
    'Kimya:Kimyasal Hesaplamalar',
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    706,
    'KIM',
    'tyt',
    'Kimya:Kimyanın Temel Kanunları',
    1.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    707,
    'KIM',
    'tyt',
    'Kimya:Asit, Baz ve Tuz',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    708,
    'KIM',
    'tyt',
    'Kimya:Karışımlar',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    709,
    'KIM',
    'tyt',
    'Kimya:Kimya Her Yerde',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    710,
    'KIM',
    'tyt',
    'Kimya:Atmosfer ve Bağıl Nem',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    711,
    'KIM',
    'tyt',
    'Kimya:Doğa ve Kimya',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    712,
    'KIM',
    'tyt',
    'Kimya:Fiziksel ve Kimyasal Özellikler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    713,
    'KIM',
    'tyt',
    'Kimya:Maddenin Halleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    714,
    'KIM',
    'tyt',
    'Kimya:Maddenin Halleri-Plazma',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    715,
    'KIM',
    'tyt',
    'Kimya:Maddenin Halleri-Su Döngüsü',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    716,
    'BIO',
    'tyt',
    'Biyoloji:Canlıların Ortak Özellikleri',
    0.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    717,
    'BIO',
    'tyt',
    'Biyoloji:Canlıların Temel Bileşenleri',
    1.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    718,
    'BIO',
    'tyt',
    'Biyoloji:Hücre ve Organelleri',
    0.0, 0.0, 1.0, 2.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    719,
    'BIO',
    'tyt',
    'Biyoloji:Hücre Zarından Madde Geçişi',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    720,
    'BIO',
    'tyt',
    'Biyoloji:Canlıların Sınıflandırılması',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    721,
    'BIO',
    'tyt',
    'Biyoloji:Mayoz ve Eşeyli Üreme',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    722,
    'BIO',
    'tyt',
    'Biyoloji:Mitoz ve Eşeysiz Üreme',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    723,
    'BIO',
    'tyt',
    'Biyoloji:Ekosistem Ekolojisi',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    724,
    'BIO',
    'tyt',
    'Biyoloji:Bitkiler Biyolojisi',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    725,
    'BIO',
    'tyt',
    'Biyoloji:Kalıtım',
    0.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    726,
    'BIO',
    'tyt',
    'Biyoloji:Canlıların Temel Bileşenleri-Organik Temel Bileşenler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    727,
    'BIO',
    'tyt',
    'Biyoloji:Güncel Çevre Sorunları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    728,
    'BIO',
    'tyt',
    'Biyoloji:İnorganik Maddeler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    729,
    'BIO',
    'tyt',
    'Biyoloji:Organik Maddeler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    730,
    'TUR',
    'tyt',
    'Türkçe:Anlatım Bozukluğu',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    731,
    'TUR',
    'tyt',
    'Türkçe:Cümlede Anlam',
    7.0, 3.0, 6.0, 3.0,
    3.0, 4.0, 5.0, 4.0
);

INSERT INTO excel_topic_data VALUES (
    732,
    'TUR',
    'tyt',
    'Türkçe:Cümle Türleri',
    7.0, 3.0, 6.0, 3.0,
    3.0, 4.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    733,
    'TUR',
    'tyt',
    'Türkçe:Cümlenin Öğeleri',
    7.0, 3.0, 6.0, 3.0,
    3.0, 4.0, 5.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    734,
    'TUR',
    'tyt',
    'Türkçe:Dil Bilgisi',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    735,
    'TUR',
    'tyt',
    'Türkçe:Sözcük Türleri',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    736,
    'TUR',
    'tyt',
    'Türkçe:Sözcük Türleri – Fiiller',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    737,
    'TUR',
    'tyt',
    'Türkçe:Sözcük Türleri – İsimler',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    738,
    'TUR',
    'tyt',
    'Türkçe:Sözcük Türleri– Edat – Bağlaç – Ünlem',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    739,
    'TUR',
    'tyt',
    'Türkçe:Sözcük Türleri– Sıfatlar',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    740,
    'TUR',
    'tyt',
    'Türkçe:Sözcük Türleri– Zamirler',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    741,
    'TUR',
    'tyt',
    'Türkçe:Sözcük Türleri– Zarflar',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    742,
    'TUR',
    'tyt',
    'Türkçe:Sözcükte Yapı',
    1.0, 7.0, 3.0, 2.0,
    3.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    743,
    'TUR',
    'tyt',
    'Türkçe:Noktalama İşaretleri',
    1.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    744,
    'TUR',
    'tyt',
    'Türkçe:Paragraf',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 26.0
);

INSERT INTO excel_topic_data VALUES (
    745,
    'TUR',
    'tyt',
    'Türkçe:Paragraf– Paragrafta Anlatım Teknikleri',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 26.0
);

INSERT INTO excel_topic_data VALUES (
    746,
    'TUR',
    'tyt',
    'Türkçe:Paragraf– Paragrafta Düşünceyi Geliştirme Yolları',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 26.0
);

INSERT INTO excel_topic_data VALUES (
    747,
    'TUR',
    'tyt',
    'Türkçe:Paragraf– Paragrafta Konu-Ana Düşünce',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 26.0
);

INSERT INTO excel_topic_data VALUES (
    748,
    'TUR',
    'tyt',
    'Türkçe:Paragraf– Paragrafta Yapı',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 26.0
);

INSERT INTO excel_topic_data VALUES (
    749,
    'TUR',
    'tyt',
    'Türkçe:Paragraf– Paragrafta Yardımcı Düşünce',
    22.0, 21.0, 26.0, 25.0,
    26.0, 26.0, 26.0, 26.0
);

INSERT INTO excel_topic_data VALUES (
    750,
    'TUR',
    'tyt',
    'Türkçe:Ses Bilgisi',
    3.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    751,
    'TUR',
    'tyt',
    'Türkçe:Sözcükte Anlam',
    3.0, 4.0, 1.0, 5.0,
    4.0, 3.0, 5.0, 4.0
);

INSERT INTO excel_topic_data VALUES (
    752,
    'TUR',
    'tyt',
    'Türkçe:Yazım Kuralları',
    2.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    753,
    'TAR',
    'tyt',
    'Tarih:Değişen Dünya Dengeleri Karşısında Osmanlı Siyaseti',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    754,
    'TAR',
    'tyt',
    'Tarih:Değişim Çağında Avrupa ve Osmanlı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    755,
    'TAR',
    'tyt',
    'Tarih:Devletleşme Sürecinde Savaşçılar ve Askerler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    756,
    'TAR',
    'tyt',
    'Tarih:Devrimler Çağında Değişen Devlet-Toplum İlişkileri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    757,
    'TAR',
    'tyt',
    'Tarih:İnsanlığın İlk Dönemleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    758,
    'TAR',
    'tyt',
    'Tarih:Klasik Çağda Osmanlı Toplum Düzeni',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    759,
    'TAR',
    'tyt',
    'Tarih:Orta Çağ’da Dünya',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    760,
    'TAR',
    'tyt',
    'Tarih:Sermaye ve Emek',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    761,
    'TAR',
    'tyt',
    'Tarih:Sultan ve Osmanlı Merkez Teşkilatı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    762,
    'TAR',
    'tyt',
    'Tarih:XIX. ve XX. Yüzyılda Değişen Gündelik Hayat',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    763,
    'TAR',
    'tyt',
    'Tarih:Tarih ve Zaman',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    764,
    'TAR',
    'tyt',
    'Tarih:İlk ve Orta Çağlarda Türk Dünyası',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    765,
    'TAR',
    'tyt',
    'Tarih:İslam Medeniyetinin Doğuşu ve İlk İslam Devletleri',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    766,
    'TAR',
    'tyt',
    'Tarih:Türklerin İslamiyet’i Kabulü ve İlk Türk İslam Devletleri',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    767,
    'TAR',
    'tyt',
    'Tarih:Beylikten Devlete Osmanlı',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    768,
    'TAR',
    'tyt',
    'Tarih:Dünya Gücü Osmanlı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    769,
    'TAR',
    'tyt',
    'Tarih:Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    770,
    'TAR',
    'tyt',
    'Tarih:Uluslararası İlişkilerde Denge Stratejisi (1774-1914)',
    1.0, 0.0, 1.0, 1.0,
    0.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    771,
    'TAR',
    'tyt',
    'Tarih:XX. Yüzyıl Başlarında Osmanlı Devleti ve Dünya',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    772,
    'TAR',
    'tyt',
    'Tarih:Milli Mücadele',
    0.0, 1.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    773,
    'TAR',
    'tyt',
    'Tarih:Atatürkçülük ve Türk İnkılabı',
    0.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    774,
    'DIN',
    'tyt',
    'Din:Bilgi ve İnanç',
    1.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    775,
    'DIN',
    'tyt',
    'Din:Din ve İslam',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    776,
    'DIN',
    'tyt',
    'Din:İslam ve İbadet',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    777,
    'DIN',
    'tyt',
    'Din:Gençlik ve Değerler',
    1.0, 1.0, 1.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    778,
    'DIN',
    'tyt',
    'Din:Allah İnsan İlişkisi',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    779,
    'DIN',
    'tyt',
    'Din:Hz. Muhammed (S.A.V.)',
    1.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    780,
    'DIN',
    'tyt',
    'Din:Vahiy ve Akıl',
    1.0, 0.0, 2.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    781,
    'DIN',
    'tyt',
    'Din:İslam Düşüncesinde Yorumlar, Mezhepler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    782,
    'DIN',
    'tyt',
    'Din:İslam Medeniyeti ve Özellikleri',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    783,
    'COG',
    'tyt',
    'Coğrafya:Doğa ve İnsan',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    784,
    'COG',
    'tyt',
    'Coğrafya:Dünya’nın Şekli ve Hareketleri',
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    785,
    'COG',
    'tyt',
    'Coğrafya:Coğrafi Konum',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    786,
    'COG',
    'tyt',
    'Coğrafya:Harita Bilgisi',
    1.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    787,
    'COG',
    'tyt',
    'Coğrafya:Atmosfer ve Sıcaklık',
    0.0, 0.0, 1.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    788,
    'COG',
    'tyt',
    'Coğrafya:İklim Bilgisi',
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    789,
    'COG',
    'tyt',
    'Coğrafya:İç Kuvvetler / Dış Kuvvetler',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    790,
    'COG',
    'tyt',
    'Coğrafya:Nüfus ve Yerleşme',
    1.0, 2.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    791,
    'COG',
    'tyt',
    'Coğrafya:Türkiye’nin Yer Şekilleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    792,
    'COG',
    'tyt',
    'Coğrafya:Ekonomik Faaliyetler',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    793,
    'COG',
    'tyt',
    'Coğrafya:Bölgeler',
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    794,
    'COG',
    'tyt',
    'Coğrafya:Uluslararası Ulaşım Hatları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    795,
    'COG',
    'tyt',
    'Coğrafya:Doğal Afetler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    796,
    'COG',
    'tyt',
    'Coğrafya:Çevre ve Toplum',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    797,
    'COG',
    'tyt',
    'Coğrafya:Dünya’nın Tektonik Oluşumu',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    798,
    'COG',
    'tyt',
    'Coğrafya:Göç',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    799,
    'COG',
    'tyt',
    'Coğrafya:Jeolojik Zamanlar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    800,
    'COG',
    'tyt',
    'Coğrafya:Kayaçlar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    801,
    'COG',
    'tyt',
    'Coğrafya:Su – Toprak ve Bitkiler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    802,
    'COG',
    'tyt',
    'Felsefe:Felsefenin Alanı',
    0.0, 1.0, 0.0, 2.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    803,
    'COG',
    'tyt',
    'Felsefe:Felsefe’nin Konusu',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    804,
    'COG',
    'tyt',
    'Felsefe:Bilgi Felsefesi',
    2.0, 1.0, 1.0, 0.0,
    2.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    805,
    'COG',
    'tyt',
    'Felsefe:Bilim Felsefesi',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    806,
    'COG',
    'tyt',
    'Felsefe:Varlık Felsefesi',
    1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    807,
    'COG',
    'tyt',
    'Felsefe:Ahlak Felsefesi',
    1.0, 1.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    808,
    'COG',
    'tyt',
    'Felsefe:Siyaset Felsefesi',
    0.0, 1.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    809,
    'COG',
    'tyt',
    'Felsefe:Din Felsefesi',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    810,
    'COG',
    'tyt',
    'Felsefe:Sanat Felsefesi',
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    811,
    'COG',
    'tyt',
    'Felsefe:İlk Çağ Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    812,
    'COG',
    'tyt',
    'Felsefe:15. Yüzyıl ve 17. Yüzyıl Felsefeleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    813,
    'COG',
    'tyt',
    'Felsefe:18. Yüzyıl ve 19. Yüzyıl Felsefeleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    814,
    'COG',
    'tyt',
    'Felsefe:2. Yüzyıl ve 15. Yüzyıl Felsefeleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    815,
    'COG',
    'tyt',
    'Felsefe:20. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    816,
    'MAT',
    'ayt',
    'Matematik:Temel Kavramlar-Denklem Çözme-Sayılar',
    4.0, 2.0, 2.0, 3.0,
    2.0, 4.0, 2.0, 6.0
);

INSERT INTO excel_topic_data VALUES (
    817,
    'MAT',
    'ayt',
    'Matematik:Sayı Basamakları',
    0.0, 0.0, 3.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    818,
    'MAT',
    'ayt',
    'Matematik:Üslü Sayılar',
    0.0, 0.0, 1.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    819,
    'MAT',
    'ayt',
    'Matematik:Bölme ve Bölünebilme',
    0.0, 1.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    820,
    'MAT',
    'ayt',
    'Matematik:Fonskiyonlar',
    3.0, 2.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    821,
    'MAT',
    'ayt',
    'Matematik:2.Dereceden Denklemler',
    0.0, 0.0, 1.0, 1.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    822,
    'MAT',
    'ayt',
    'Matematik:Mantık',
    2.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    823,
    'MAT',
    'ayt',
    'Matematik:Parabol',
    0.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    824,
    'MAT',
    'ayt',
    'Matematik:Trigonometri',
    3.0, 3.0, 4.0, 5.0,
    4.0, 5.0, 5.0, 4.0
);

INSERT INTO excel_topic_data VALUES (
    825,
    'MAT',
    'ayt',
    'Matematik:Karmaşık Sayılar',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    826,
    'MAT',
    'ayt',
    'Matematik:Polinomlar',
    2.0, 2.0, 2.0, 1.0,
    1.0, 2.0, 0.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    827,
    'MAT',
    'ayt',
    'Matematik:Logaritma',
    2.0, 3.0, 3.0, 1.0,
    2.0, 3.0, 1.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    828,
    'MAT',
    'ayt',
    'Matematik:Denklem Çözme',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    829,
    'MAT',
    'ayt',
    'Matematik:Diziler',
    1.0, 1.0, 2.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    830,
    'MAT',
    'ayt',
    'Matematik:Permütasyon-Kombinasyon-Olasılık',
    2.0, 2.0, 3.0, 2.0,
    3.0, 3.0, 3.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    831,
    'MAT',
    'ayt',
    'Matematik:Kombinasyon',
    2.0, 2.0, 3.0, 2.0,
    3.0, 3.0, 3.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    832,
    'MAT',
    'ayt',
    'Matematik:Permütasyon',
    2.0, 2.0, 3.0, 2.0,
    3.0, 3.0, 3.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    833,
    'MAT',
    'ayt',
    'Matematik:Olasılık',
    2.0, 2.0, 3.0, 2.0,
    3.0, 3.0, 3.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    834,
    'MAT',
    'ayt',
    'Matematik:Limit',
    1.0, 2.0, 0.0, 2.0,
    2.0, 0.0, 2.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    835,
    'MAT',
    'ayt',
    'Matematik:Türev',
    1.0, 4.0, 0.0, 3.0,
    4.0, 0.0, 3.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    836,
    'MAT',
    'ayt',
    'Matematik:İntegral',
    3.0, 4.0, 0.0, 4.0,
    4.0, 0.0, 5.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    837,
    'MAT',
    'ayt',
    'Matematik:Vektörler',
    2.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    838,
    'MAT',
    'ayt',
    'Matematik:Köklü Sayılar',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    839,
    'MAT',
    'ayt',
    'Matematik:Kümeler ve Kartezyen Çarpım',
    0.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    840,
    'MAT',
    'ayt',
    'Matematik:Kümeler',
    0.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    841,
    'MAT',
    'ayt',
    'Matematik:Kartezyen Çarpım',
    0.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    842,
    'MAT',
    'ayt',
    'Matematik:Basit Eşitsizlikler',
    0.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    843,
    'MAT',
    'ayt',
    'Matematik:Mutlak Değer',
    0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    844,
    'MAT',
    'ayt',
    'Matematik:EBOB EKOK',
    0.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    845,
    'MAT',
    'ayt',
    'Matematik:Çarpanlara Ayırma',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    846,
    'MAT',
    'ayt',
    'Matematik:Oran Orantı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    847,
    'MAT',
    'ayt',
    'Matematik:Problemler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 8.0
);

INSERT INTO excel_topic_data VALUES (
    848,
    'MAT',
    'ayt',
    'Matematik:Rasyonel Sayılar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    849,
    'MAT',
    'ayt',
    'Matematik:2.Dereceden Eşitsizlikler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    850,
    'MAT',
    'ayt',
    'Matematik:Denklemler ve Eşitsizlikler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    851,
    'MAT',
    'ayt',
    'Matematik:Veri – İstatistik',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    852,
    'MAT',
    'ayt',
    'Matematik:Doğruda ve Üçgende Açı',
    1.0, 3.0, 1.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    853,
    'MAT',
    'ayt',
    'Matematik:Doğruda Açı',
    1.0, 3.0, 1.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    854,
    'MAT',
    'ayt',
    'Matematik:Üçgende Açı',
    1.0, 3.0, 1.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    855,
    'MAT',
    'ayt',
    'Matematik:Özel Üçgenler',
    0.0, 0.0, 0.0, 0.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    856,
    'MAT',
    'ayt',
    'Matematik:Özel Üçgenler-Dik Üçgen',
    0.0, 0.0, 0.0, 0.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    857,
    'MAT',
    'ayt',
    'Matematik:Özel Üçgenler-Eşkenar Üçgen',
    0.0, 0.0, 0.0, 0.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    858,
    'MAT',
    'ayt',
    'Matematik:Özel Üçgenler-İkizkenar Üçgen',
    0.0, 0.0, 0.0, 0.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    859,
    'MAT',
    'ayt',
    'Matematik:Üçgende Merkezler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    860,
    'MAT',
    'ayt',
    'Matematik:Açıortay-Kenarortay',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    861,
    'MAT',
    'ayt',
    'Matematik:Açıortay',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    862,
    'MAT',
    'ayt',
    'Matematik:Kenarortay',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    863,
    'MAT',
    'ayt',
    'Matematik:Üçgende Alan-Benzerlik',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    864,
    'MAT',
    'ayt',
    'Matematik:Üçgende Alan',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    865,
    'MAT',
    'ayt',
    'Matematik:Üçgende Eşlik – Benzerlik',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    866,
    'MAT',
    'ayt',
    'Matematik:Açı – Kenar Bağıntıları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    867,
    'MAT',
    'ayt',
    'Matematik:Çokgenler',
    0.0, 0.0, 0.0, 0.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    868,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    869,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-Deltoid',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    870,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-Dikdörtgen',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    871,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-Dörtgenler',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    872,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-Eşkenar Dörtgen',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    873,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-İkizkenar',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    874,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-Kare',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    875,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-Paralelkenar',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    876,
    'MAT',
    'ayt',
    'Matematik:Özel Dörtgenler-Yamuk',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    877,
    'MAT',
    'ayt',
    'Matematik:Çember ve Daire',
    2.0, 2.0, 2.0, 3.0,
    2.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    878,
    'MAT',
    'ayt',
    'Matematik:Analitik Geometri-Noktanın Analitiği',
    1.0, 1.0, 1.0, 2.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    879,
    'MAT',
    'ayt',
    'Matematik:Analitik Geometri-Doğrunun Analitiği',
    3.0, 0.0, 1.0, 2.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    880,
    'MAT',
    'ayt',
    'Matematik:Analitik Geometri-Dönüşüm Geometrisi',
    0.0, 1.0, 1.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    881,
    'MAT',
    'ayt',
    'Matematik:Katı Cisimler (Uzay Geometri)',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    882,
    'MAT',
    'ayt',
    'Matematik:Katı Cisimler (Uzay Geometri)-Koni',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    883,
    'MAT',
    'ayt',
    'Matematik:Katı Cisimler (Uzay Geometri)-Küp',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    884,
    'MAT',
    'ayt',
    'Matematik:Katı Cisimler (Uzay Geometri)-Küre',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    885,
    'MAT',
    'ayt',
    'Matematik:Katı Cisimler (Uzay Geometri)-Piramit',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    886,
    'MAT',
    'ayt',
    'Matematik:Katı Cisimler (Uzay Geometri)-Prizmalar',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    887,
    'MAT',
    'ayt',
    'Matematik:Katı Cisimler (Uzay Geometri)-Silindir',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    888,
    'MAT',
    'ayt',
    'Matematik:Analitik Geometri-Çemberin Analitiği',
    1.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    889,
    'FIZ',
    'ayt',
    'Fizik:Vektörler',
    0.0, 0.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    890,
    'FIZ',
    'ayt',
    'Fizik:Hareket',
    0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    891,
    'FIZ',
    'ayt',
    'Fizik:Newton’un Hareket Yasaları',
    1.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    892,
    'FIZ',
    'ayt',
    'Fizik:Bir Boyutta Sabit İvmeli Hareket',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    893,
    'FIZ',
    'ayt',
    'Fizik:Atışlar',
    0.0, 1.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    894,
    'FIZ',
    'ayt',
    'Fizik:İş, Güç ve Enerji II',
    0.0, 0.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    895,
    'FIZ',
    'ayt',
    'Fizik:İtme ve Momentum',
    1.0, 1.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    896,
    'FIZ',
    'ayt',
    'Fizik:Kuvvet, Tork ve Denge',
    1.0, 1.0, 1.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    897,
    'FIZ',
    'ayt',
    'Fizik:Basit Makineler',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    898,
    'FIZ',
    'ayt',
    'Fizik:Elektrik Alan ve Potansiyel',
    1.0, 1.0, 1.0, 2.0,
    0.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    899,
    'FIZ',
    'ayt',
    'Fizik:Paralel Levhalar ve Sığa',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    900,
    'FIZ',
    'ayt',
    'Fizik:Manyetik Alan ve Manyetik Kuvvet',
    1.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    901,
    'FIZ',
    'ayt',
    'Fizik:İndüksiyon, Alternatif Akım ve Transformatörler',
    1.0, 2.0, 1.0, 1.0,
    1.0, 2.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    902,
    'FIZ',
    'ayt',
    'Fizik:Çembersel Hareket',
    2.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    903,
    'FIZ',
    'ayt',
    'Fizik:Dönme, Yuvarlanma ve Açısal Momentum',
    0.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    904,
    'FIZ',
    'ayt',
    'Fizik:Kütle Çekim ve Kepler Yasaları',
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    905,
    'FIZ',
    'ayt',
    'Fizik:Basit Harmonik Hareket',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    906,
    'FIZ',
    'ayt',
    'Fizik:Dalga Mekaniği ve Elektromanyetik Dalgalar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    907,
    'FIZ',
    'ayt',
    'Fizik:Atom Fiziğine Giriş ve Radyoaktivite',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    908,
    'FIZ',
    'ayt',
    'Fizik:Fotoelektrik Olay ve Compton Olayı',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    909,
    'FIZ',
    'ayt',
    'Fizik:Modern Fiziğin Teknolojideki Uygulamaları',
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    910,
    'FIZ',
    'ayt',
    'Fizik:Özel Görelillik',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    911,
    'FIZ',
    'ayt',
    'Fizik:Kütle Merkezi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    912,
    'KIM',
    'ayt',
    'Kimya:Kimya Bilimi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    913,
    'KIM',
    'ayt',
    'Kimya:Atom ve Yapısı',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    914,
    'KIM',
    'ayt',
    'Kimya:Periyodik Sistem',
    1.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    915,
    'KIM',
    'ayt',
    'Kimya:Kimyasal Türler Arası Etkileşimler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    916,
    'KIM',
    'ayt',
    'Kimya:Kimyasal Hesaplamalar',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    917,
    'KIM',
    'ayt',
    'Kimya:Modern Atom Teorisi',
    0.0, 0.0, 2.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    918,
    'KIM',
    'ayt',
    'Kimya:Gazlar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    919,
    'KIM',
    'ayt',
    'Kimya:Çözeltiler',
    1.0, 1.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    920,
    'KIM',
    'ayt',
    'Kimya:Kimyasal Tepkimelerde Enerji',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    921,
    'KIM',
    'ayt',
    'Kimya:Kimyasal Tepkimelerde Hız',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    922,
    'KIM',
    'ayt',
    'Kimya:Kimyasal Tepkimelerde Denge',
    0.0, 0.0, 1.0, 1.0,
    1.0, 2.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    923,
    'KIM',
    'ayt',
    'Kimya:Asit-Baz Dengesi',
    1.0, 2.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    924,
    'KIM',
    'ayt',
    'Kimya:Çözünürlük Dengesi',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    925,
    'KIM',
    'ayt',
    'Kimya:Kimya ve Elektrik',
    2.0, 2.0, 3.0, 2.0,
    2.0, 3.0, 2.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    926,
    'KIM',
    'ayt',
    'Kimya:Organik Kimya',
    4.0, 3.0, 1.0, 3.0,
    3.0, 1.0, 3.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    927,
    'KIM',
    'ayt',
    'Kimya:Asit, Baz ve Tuz',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    928,
    'KIM',
    'ayt',
    'Kimya:Maddenin Halleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    929,
    'KIM',
    'ayt',
    'Kimya:Karışımlar',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    930,
    'KIM',
    'ayt',
    'Kimya:Doğa ve Kimya',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    931,
    'KIM',
    'ayt',
    'Kimya:Kimya Her Yerde',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    932,
    'KIM',
    'ayt',
    'Kimya:Kimyanın Temel Kanunları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    933,
    'BIO',
    'ayt',
    'Biyoloji:Sinir Sistemi',
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    934,
    'BIO',
    'ayt',
    'Biyoloji:Endokrin Sistem',
    0.0, 1.0, 1.0, 1.0,
    0.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    935,
    'BIO',
    'ayt',
    'Biyoloji:Duyu Organları',
    0.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    936,
    'BIO',
    'ayt',
    'Biyoloji:Destek ve Hareket Sistemi',
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    937,
    'BIO',
    'ayt',
    'Biyoloji:Sindirim Sistemi',
    0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    938,
    'BIO',
    'ayt',
    'Biyoloji:Dolaşım ve Bağışıklık Sistemi',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    939,
    'BIO',
    'ayt',
    'Biyoloji:Solunum Sistemi',
    0.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    940,
    'BIO',
    'ayt',
    'Biyoloji:Boşaltım Sistemi',
    1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    941,
    'BIO',
    'ayt',
    'Biyoloji:Üriner Sistem',
    0.0, 0.0, 1.0, 0.0,
    0.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    942,
    'BIO',
    'ayt',
    'Biyoloji:Üreme Sistemi ve Embriyonik Gelişim',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    943,
    'BIO',
    'ayt',
    'Biyoloji:Komünite ve Popülasyon Ekolojisi',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    944,
    'BIO',
    'ayt',
    'Biyoloji:Komünite Ekolojisi',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    945,
    'BIO',
    'ayt',
    'Biyoloji:Popülasyon Ekolojisi',
    2.0, 0.0, 2.0, 2.0,
    2.0, 2.0, 2.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    946,
    'BIO',
    'ayt',
    'Biyoloji:Genden Proteine-Nükleik Asitler',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    947,
    'BIO',
    'ayt',
    'Biyoloji:Genden Proteine-Genetik Şifre ve Protein Sentezi',
    3.0, 1.0, 2.0, 2.0,
    2.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    948,
    'BIO',
    'ayt',
    'Biyoloji:Canlılarda Enerji Dönüşümleri-Canlılık ve Enerji',
    0.0, 0.0, 0.0, 0.0,
    1.0, 0.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    949,
    'BIO',
    'ayt',
    'Biyoloji:Canlılarda Enerji Dönüşümleri-Fotosentez ve Kemosentez',
    1.0, 1.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    950,
    'BIO',
    'ayt',
    'Biyoloji:Canlılarda Enerji Dönüşümleri-Fotosentez',
    1.0, 1.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    951,
    'BIO',
    'ayt',
    'Biyoloji:Canlılarda Enerji Dönüşümleri-Kemosentez',
    1.0, 1.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    952,
    'BIO',
    'ayt',
    'Biyoloji:Canlılarda Enerji Dönüşümleri-Hücresel Solunum',
    0.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 0.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    953,
    'BIO',
    'ayt',
    'Biyoloji:Bitkiler Biyolojisi',
    2.0, 3.0, 0.0, 2.0,
    2.0, 0.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    954,
    'BIO',
    'ayt',
    'Biyoloji:Canlılar ve Çevre',
    1.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    955,
    'EDB',
    'ayt',
    'Edebiyat:Dünya Edebiyatı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    956,
    'EDB',
    'ayt',
    'Edebiyat:Fecr-i Ati Edebiyatı',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    957,
    'EDB',
    'ayt',
    'Edebiyat:Güzel Sanatlar ve Edebiyat',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    958,
    'EDB',
    'ayt',
    'Edebiyat:Anlam Bilgisi',
    4.0, 4.0, 6.0, 3.0,
    6.0, 6.0, 6.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    959,
    'EDB',
    'ayt',
    'Edebiyat:Dil Bilgisi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    960,
    'EDB',
    'ayt',
    'Edebiyat:Şiir Bilgisi',
    3.0, 3.0, 3.0, 2.0,
    3.0, 1.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    961,
    'EDB',
    'ayt',
    'Edebiyat:Edebi Sanatlar',
    1.0, 1.0, 1.0, 2.0,
    2.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    962,
    'EDB',
    'ayt',
    'Edebiyat:Edebi Metinler',
    1.0, 0.0, 0.0, 0.0,
    0.0, 3.0, 3.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    963,
    'EDB',
    'ayt',
    'Edebiyat:Tiyatro',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    964,
    'EDB',
    'ayt',
    'Edebiyat:İslamiyet Öncesi Türk Edebiyatı ve Geçiş Dönemi',
    0.0, 1.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    965,
    'EDB',
    'ayt',
    'Edebiyat:Halk Edebiyatı',
    1.0, 2.0, 2.0, 2.0,
    1.0, 2.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    966,
    'EDB',
    'ayt',
    'Edebiyat:Divan Edebiyatı',
    5.0, 3.0, 5.0, 6.0,
    4.0, 5.0, 5.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    967,
    'EDB',
    'ayt',
    'Edebiyat:Edebi Akımlar',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    968,
    'EDB',
    'ayt',
    'Edebiyat:Tanzimat Edebiyatı',
    3.0, 2.0, 1.0, 2.0,
    1.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    969,
    'EDB',
    'ayt',
    'Edebiyat:Servet-i Fünun Edebiyatı',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    970,
    'EDB',
    'ayt',
    'Edebiyat:Milli Edebiyat',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 2.0
);

INSERT INTO excel_topic_data VALUES (
    971,
    'EDB',
    'ayt',
    'Edebiyat:Cumhuriyet Dönemi Edebiyatı',
    4.0, 5.0, 2.0, 3.0,
    3.0, 2.0, 2.0, 3.0
);

INSERT INTO excel_topic_data VALUES (
    972,
    'TAR',
    'ayt',
    'Tarih:Tarih ve Zaman',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    973,
    'TAR',
    'ayt',
    'Tarih:İnsanlığın İlk Dönemleri',
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    974,
    'TAR',
    'ayt',
    'Tarih:Orta Çağ’da Dünya',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    975,
    'TAR',
    'ayt',
    'Tarih:İlk ve Orta Çağlarda Türk Dünyası',
    3.0, 2.0, 2.0, 1.0,
    2.0, 2.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    976,
    'TAR',
    'ayt',
    'Tarih:İslam Medeniyetinin Doğuşu ve İlk İslam Devletleri',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    977,
    'TAR',
    'ayt',
    'Tarih:Türklerin İslamiyet’i Kabulü ve İlk Türk İslam Devletleri',
    1.0, 1.0, 1.0, 3.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    978,
    'TAR',
    'ayt',
    'Tarih:Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi',
    0.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    979,
    'TAR',
    'ayt',
    'Tarih:Beylikten Devlete Osmanlı',
    2.0, 1.0, 1.0, 0.0,
    3.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    980,
    'TAR',
    'ayt',
    'Tarih:Beylikten Devlete Osmanlı Medeniyeti',
    2.0, 1.0, 1.0, 0.0,
    3.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    981,
    'TAR',
    'ayt',
    'Tarih:Beylikten Devlete Osmanlı Siyaseti',
    2.0, 1.0, 1.0, 0.0,
    3.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    982,
    'TAR',
    'ayt',
    'Tarih:Devletleşme Sürecinde Savaşçılar ve Askerler',
    0.0, 0.0, 1.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    983,
    'TAR',
    'ayt',
    'Tarih:Dünya Gücü Osmanlı',
    2.0, 1.0, 0.0, 1.0,
    0.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    984,
    'TAR',
    'ayt',
    'Tarih:Sultan ve Osmanlı Merkez Teşkilatı',
    0.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    985,
    'TAR',
    'ayt',
    'Tarih:Değişen Dünya Dengeleri Karşısında Osmanlı Siyaseti',
    0.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    986,
    'TAR',
    'ayt',
    'Tarih:Değişim Çağında Avrupa ve Osmanlı',
    0.0, 2.0, 2.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    987,
    'TAR',
    'ayt',
    'Tarih:Uluslararası İlişkilerde Denge Stratejisi (1774-1914)',
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    988,
    'TAR',
    'ayt',
    'Tarih:Devrimler Çağında Değişen Devlet-Toplum İlişkileri',
    0.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    989,
    'TAR',
    'ayt',
    'Tarih:Sermaye ve Emek',
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    990,
    'TAR',
    'ayt',
    'Tarih:XX. Yüzyıl Başlarında Osmanlı Devleti ve Dünya',
    3.0, 4.0, 2.0, 1.0,
    0.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    991,
    'TAR',
    'ayt',
    'Tarih:Milli Mücadele',
    1.0, 3.0, 4.0, 4.0,
    5.0, 6.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    992,
    'TAR',
    'ayt',
    'Tarih:Atatürkçülük ve Türk İnkılabı',
    2.0, 2.0, 2.0, 3.0,
    1.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    993,
    'TAR',
    'ayt',
    'Tarih:İki Savaş Arasındaki Dönemde Türkiye ve Dünya',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    994,
    'TAR',
    'ayt',
    'Tarih:II. Dünya Savaşı Sürecinde 0 Sonrasında Türkiye ve Dünya',
    1.0, 0.0, 0.0, 0.0,
    2.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    995,
    'TAR',
    'ayt',
    'Tarih:XXI. Yüzyılın Eşiğinde Türkiye ve Dünya',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    996,
    'COG',
    'ayt',
    'Coğrafya:İklim ve Yer Şekilleri',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    997,
    'COG',
    'ayt',
    'Coğrafya:Coğrafi Konum',
    2.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    998,
    'COG',
    'ayt',
    'Coğrafya:Dünya’nın Şekli ve Hareketleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    999,
    'COG',
    'ayt',
    'Coğrafya:Harita Bilgisi',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1000,
    'COG',
    'ayt',
    'Coğrafya:İç ve Dış Kuvvetler',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1001,
    'COG',
    'ayt',
    'Coğrafya:Ekosistem',
    0.0, 3.0, 3.0, 3.0,
    4.0, 4.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1002,
    'COG',
    'ayt',
    'Coğrafya:Nüfus Politikaları',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1003,
    'COG',
    'ayt',
    'Coğrafya:Türkiye’de Nüfus ve Yerleşme',
    4.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1004,
    'COG',
    'ayt',
    'Coğrafya:Ekonomik Faaliyetler ve Doğal Kaynaklar',
    1.0, 1.0, 1.0, 1.0,
    2.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1005,
    'COG',
    'ayt',
    'Coğrafya:Göç ve Şehirleşme',
    0.0, 1.0, 1.0, 0.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1006,
    'COG',
    'ayt',
    'Coğrafya:Türkiye Ekonomisi',
    4.0, 2.0, 1.0, 3.0,
    2.0, 2.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1007,
    'COG',
    'ayt',
    'Coğrafya:Türkiye’nin İşlevsel Bölgeleri ve Kalkınma Projeleri',
    1.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1008,
    'COG',
    'ayt',
    'Coğrafya:Küresel Ticaret',
    0.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1009,
    'COG',
    'ayt',
    'Coğrafya:Kültür Bölgeleri',
    0.0, 2.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1010,
    'COG',
    'ayt',
    'Coğrafya:Küresel ve Bölgesel Örgütler',
    0.0, 2.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1011,
    'COG',
    'ayt',
    'Coğrafya:Ülkeler Arası Etkileşimler',
    0.0, 1.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1012,
    'COG',
    'ayt',
    'Coğrafya:Bölgeler ve Ülkeler',
    1.0, 1.0, 2.0, 2.0,
    4.0, 4.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1013,
    'COG',
    'ayt',
    'Coğrafya:Çevre ve Toplum',
    0.0, 1.0, 3.0, 3.0,
    1.0, 1.0, 4.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1014,
    'COG',
    'ayt',
    'Coğrafya:Ekstrem Doğa Olayları',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1015,
    'COG',
    'ayt',
    'Coğrafya:Geçmişten Geleceğe Şehir ve Ekonomi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1016,
    'COG',
    'ayt',
    'Coğrafya:Hizmet Sektörünün Ekonomideki Yeri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1017,
    'COG',
    'ayt',
    'Coğrafya:Küresel İklim Değişimi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1018,
    'COG',
    'ayt',
    'Coğrafya:Türkiye Turizmi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1019,
    'COG',
    'ayt',
    'Coğrafya:Yerleşmelerin Özellikleri',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1020,
    'DIN',
    'ayt',
    'Din:İslamda İbadet',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1021,
    'DIN',
    'ayt',
    'Din:Allah, İnsan İlişkisi',
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1022,
    'DIN',
    'ayt',
    'Din:Kur’an’a Göre Hz. Muhammed',
    2.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 2.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1023,
    'DIN',
    'ayt',
    'Din:Kur’an’da Bazı Kavramlar',
    2.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1024,
    'DIN',
    'ayt',
    'Din:Kur’an’dan Mesajlar',
    1.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1025,
    'DIN',
    'ayt',
    'Din:İnançla İlgili Meseleler',
    0.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1026,
    'DIN',
    'ayt',
    'Din:İslam ve Bilim',
    0.0, 1.0, 2.0, 1.0,
    3.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1027,
    'DIN',
    'ayt',
    'Din:Anadolu’da İslam',
    0.0, 0.0, 0.0, 1.0,
    0.0, 2.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1028,
    'DIN',
    'ayt',
    'Din:İslam Düşüncesinde Tasavvufi Yorumlar ve Mezhepler',
    0.0, 2.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1029,
    'DIN',
    'ayt',
    'Din:Güncel Dini Meseleler',
    0.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 1.0
);

INSERT INTO excel_topic_data VALUES (
    1030,
    'DIN',
    'ayt',
    'Din:Yaşayan Dinler',
    1.0, 1.0, 0.0, 0.0,
    1.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1031,
    'FEL',
    'ayt',
    'Felsefe:Felsefe ve Bilim',
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1032,
    'FEL',
    'ayt',
    'Felsefe:Bilgi Felsefesi',
    1.0, 2.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1033,
    'FEL',
    'ayt',
    'Felsefe:Varlık Felsefesi',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1034,
    'FEL',
    'ayt',
    'Felsefe:Ahlak Felsefesi',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1035,
    'FEL',
    'ayt',
    'Felsefe:Sanat Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1036,
    'FEL',
    'ayt',
    'Felsefe:Din Felsefesi',
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1037,
    'FEL',
    'ayt',
    'Felsefe:20. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1038,
    'FEL',
    'ayt',
    'Felsefe:15. Yüzyıl – 17. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1039,
    'FEL',
    'ayt',
    'Felsefe:18. Yüzyıl – 19. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1040,
    'FEL',
    'ayt',
    'Felsefe:Felsefe’nin Konusu',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1041,
    'FEL',
    'ayt',
    'Felsefe:İlk Çağ Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1042,
    'FEL',
    'ayt',
    'Felsefe:MÖ 6. Yüzyıl – MS 2. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1043,
    'FEL',
    'ayt',
    'Felsefe:MS 2. Yüzyıl – MS 15. Yüzyıl Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1044,
    'FEL',
    'ayt',
    'Felsefe:Siyaset Felsefesi',
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1045,
    'FEL',
    'ayt',
    'Mantık: -Mantığa Giriş',
    1.0, 1.0, 2.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1046,
    'FEL',
    'ayt',
    'Mantık: -Klasik Mantık',
    2.0, 2.0, 1.0, 1.0,
    1.0, 1.0, 2.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1047,
    'FEL',
    'ayt',
    'Mantık: -Mantık ve Dil',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1048,
    'FEL',
    'ayt',
    'Psikoloji -Psikoloji Bilimini Tanıyalım',
    0.0, 1.0, 3.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1049,
    'FEL',
    'ayt',
    'Psikoloji -Psikolojinin Temel Süreçleri',
    0.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1050,
    'FEL',
    'ayt',
    'Psikoloji -Öğrenme Bellek Düşünme',
    2.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1051,
    'FEL',
    'ayt',
    'Psikoloji -Ruh Sağlığının Temelleri',
    0.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1052,
    'FEL',
    'ayt',
    'Sosyoloji:Sosyolojiye Giriş',
    0.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1053,
    'FEL',
    'ayt',
    'Sosyoloji:Birey ve Toplum',
    1.0, 1.0, 2.0, 0.0,
    0.0, 0.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1054,
    'FEL',
    'ayt',
    'Sosyoloji:Toplumsal Yapı',
    1.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1055,
    'FEL',
    'ayt',
    'Sosyoloji:Toplumsal Değişme ve Gelişme',
    1.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1056,
    'FEL',
    'ayt',
    'Sosyoloji:Toplum ve Kültür',
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0
);

INSERT INTO excel_topic_data VALUES (
    1057,
    'FEL',
    'ayt',
    'Sosyoloji:Toplumsal Kurumlar',
    1.0, 0.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 0.0
);


-- ============================================
-- MATCHING STRATEGIES
-- ============================================

-- Strategy 1: Exact match (name + subject + grade)

UPDATE topics t
SET 
    q_2018 = e.q_2018,
    q_2019 = e.q_2019,
    q_2020 = e.q_2020,
    q_2021 = e.q_2021,
    q_2022 = e.q_2022,
    q_2023 = e.q_2023,
    q_2024 = e.q_2024,
    q_2025 = e.q_2025
FROM excel_topic_data e
JOIN subjects s ON s.code = e.subject_code
WHERE t.name_tr = e.topic_name
  AND t.subject_id = s.id
  AND (t.grade_level ILIKE '%' || e.grade_level || '%' OR e.grade_level ILIKE '%' || t.grade_level || '%');


-- Strategy 2: Partial match (first 30 characters)

UPDATE topics t
SET 
    q_2018 = COALESCE(t.q_2018, 0) + e.q_2018,
    q_2019 = COALESCE(t.q_2019, 0) + e.q_2019,
    q_2020 = COALESCE(t.q_2020, 0) + e.q_2020,
    q_2021 = COALESCE(t.q_2021, 0) + e.q_2021,
    q_2022 = COALESCE(t.q_2022, 0) + e.q_2022,
    q_2023 = COALESCE(t.q_2023, 0) + e.q_2023,
    q_2024 = COALESCE(t.q_2024, 0) + e.q_2024,
    q_2025 = COALESCE(t.q_2025, 0) + e.q_2025
FROM excel_topic_data e
JOIN subjects s ON s.code = e.subject_code
WHERE LEFT(t.name_tr, 30) = LEFT(e.topic_name, 30)
  AND t.subject_id = s.id
  AND t.q_2024 = 0  -- Only update if not already matched
  AND (t.grade_level ILIKE '%' || e.grade_level || '%' OR e.grade_level ILIKE '%' || t.grade_level || '%');


-- Strategy 3: Display name match (if available)

UPDATE topics t
SET 
    q_2018 = COALESCE(t.q_2018, 0) + e.q_2018,
    q_2019 = COALESCE(t.q_2019, 0) + e.q_2019,
    q_2020 = COALESCE(t.q_2020, 0) + e.q_2020,
    q_2021 = COALESCE(t.q_2021, 0) + e.q_2021,
    q_2022 = COALESCE(t.q_2022, 0) + e.q_2022,
    q_2023 = COALESCE(t.q_2023, 0) + e.q_2023,
    q_2024 = COALESCE(t.q_2024, 0) + e.q_2024,
    q_2025 = COALESCE(t.q_2025, 0) + e.q_2025
FROM excel_topic_data e
JOIN subjects s ON s.code = e.subject_code
WHERE t.display_name = e.topic_name
  AND t.subject_id = s.id
  AND t.q_2024 = 0  -- Only update if not already matched
  AND (t.grade_level ILIKE '%' || e.grade_level || '%' OR e.grade_level ILIKE '%' || t.grade_level || '%');


-- ============================================
-- UPDATE EXAM FREQUENCY
-- ============================================

-- Calculate frequency for all updated topics
SELECT update_all_exam_frequencies(5);

-- Cleanup temp table
DROP TABLE excel_topic_data;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================

SELECT 
    COUNT(*) as total_topics,
    COUNT(*) FILTER (WHERE q_2024 > 0) as matched_2024,
    COUNT(*) FILTER (WHERE q_2023 > 0) as matched_2023,
    COUNT(*) FILTER (WHERE exam_frequency > 1.0) as with_frequency,
    ROUND(AVG(exam_frequency), 2) as avg_frequency
FROM topics;

-- Top 10 high frequency topics
SELECT name_tr, grade_level, q_2023, q_2024, exam_frequency
FROM topics
WHERE exam_frequency > 1.0
ORDER BY exam_frequency DESC
LIMIT 10;