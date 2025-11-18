-- ============================================
-- DEMO DATA - Initial Dataset
-- ============================================

-- 1. Türkiye
INSERT INTO countries (id, code, name_en, name_local, language, currency, timezone, order_index) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'TR', 'Turkey', 'Türkiye', 'tr', 'TRY', 'Europe/Istanbul', 1);

-- 2. MEB Eğitim Sistemi
INSERT INTO education_systems (id, country_id, code, name_en, name_local) VALUES
('550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', 'MEB', 'Turkish Ministry of Education', 'Millî Eğitim Bakanlığı');

-- 3. Eğitim Seviyeleri
INSERT INTO education_levels (id, education_system_id, code, name_en, name_tr, grade_range, order_index) VALUES
('550e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440002', 'MIDDLE', 'Middle School', 'Ortaokul', '5-8', 1),
('550e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', 'HIGH', 'High School', 'Lise', '9-12', 2);

-- 4. Sınıf Seviyeleri (Lise)
INSERT INTO class_levels (id, education_level_id, code, name_en, name_tr, grade_number, order_index) VALUES
('550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440004', 'GRADE_9', '9th Grade', '9. Sınıf', 9, 1),
('550e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440004', 'GRADE_10', '10th Grade', '10. Sınıf', 10, 2),
('550e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440004', 'GRADE_11', '11th Grade', '11. Sınıf', 11, 3),
('550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440004', 'GRADE_12', '12th Grade', '12. Sınıf', 12, 4);

-- 5. Sınav Sistemleri
INSERT INTO exam_systems (id, education_system_id, code, name_en, name_tr, description, total_duration_minutes) VALUES
('550e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440002', 'YKS', 'Higher Education Institutions Exam', 'Yükseköğretim Kurumları Sınavı', 'TYT + AYT', 240),
('550e8400-e29b-41d4-a716-44665544000a', '550e8400-e29b-41d4-a716-446655440002', 'LGS', 'High School Entrance Exam', 'Liselere Giriş Sınavı', '8. sınıf sınavı', 180);

-- 6. Dersler (Lise - TYT/AYT)
INSERT INTO subjects (id, education_system_id, class_level_id, code, name_en, name_tr, exam_system_id, total_questions, icon, color, order_index) VALUES
-- TYT Dersleri
('550e8400-e29b-41d4-a716-44665544000b', '550e8400-e29b-41d4-a716-446655440002', NULL, 'MATH', 'Mathematics', 'Matematik', '550e8400-e29b-41d4-a716-446655440009', 40, '📐', '#3B82F6', 1),
('550e8400-e29b-41d4-a716-44665544000c', '550e8400-e29b-41d4-a716-446655440002', NULL, 'PHYS', 'Physics', 'Fizik', '550e8400-e29b-41d4-a716-446655440009', 14, '⚛️', '#8B5CF6', 2),
('550e8400-e29b-41d4-a716-44665544000d', '550e8400-e29b-41d4-a716-446655440002', NULL, 'CHEM', 'Chemistry', 'Kimya', '550e8400-e29b-41d4-a716-446655440009', 13, '⚗️', '#10B981', 3),
('550e8400-e29b-41d4-a716-44665544000e', '550e8400-e29b-41d4-a716-446655440002', NULL, 'BIO', 'Biology', 'Biyoloji', '550e8400-e29b-41d4-a716-446655440009', 13, '🧬', '#059669', 4),
('550e8400-e29b-41d4-a716-44665544000f', '550e8400-e29b-41d4-a716-446655440002', NULL, 'TURK', 'Turkish', 'Türkçe', '550e8400-e29b-41d4-a716-446655440009', 40, '📚', '#EF4444', 5),
('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440002', NULL, 'HIST', 'History', 'Tarih', '550e8400-e29b-41d4-a716-446655440009', 10, '🏛️', '#F59E0B', 6),
('550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440002', NULL, 'GEO', 'Geography', 'Coğrafya', '550e8400-e29b-41d4-a716-446655440009', 10, '🗺️', '#06B6D4', 7),
('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440002', NULL, 'ENG', 'English', 'İngilizce', '550e8400-e29b-41d4-a716-446655440009', 20, '🇬🇧', '#6366F1', 8);

-- 7. Matematik Konuları (Demo)
INSERT INTO topics (id, subject_id, code, name_en, name_tr, achievement_code, difficulty_level, exam_weight, exam_avg_questions, bloom_level, order_index) VALUES
-- 11. Sınıf Matematik
('550e8400-e29b-41d4-a716-446655440013', '550e8400-e29b-41d4-a716-44665544000b', 'LIMIT', 'Limit', 'Limit', 'MAT.11.1.1', 4, 8.5, 3.4, 'apply', 1),
('550e8400-e29b-41d4-a716-446655440014', '550e8400-e29b-41d4-a716-44665544000b', 'DERIVATIVE', 'Derivative', 'Türev', 'MAT.11.1.2', 4, 9.2, 3.7, 'apply', 2),
('550e8400-e29b-41d4-a716-446655440015', '550e8400-e29b-41d4-a716-44665544000b', 'INTEGRAL', 'Integral', 'İntegral', 'MAT.12.1.1', 5, 10.5, 4.2, 'analyze', 3),
('550e8400-e29b-41d4-a716-446655440016', '550e8400-e29b-41d4-a716-44665544000b', 'LOGARITHM', 'Logarithm', 'Logaritma', 'MAT.11.2.1', 3, 6.5, 2.6, 'apply', 4),
('550e8400-e29b-41d4-a716-446655440017', '550e8400-e29b-41d4-a716-44665544000b', 'EXPONENTIAL', 'Exponential Functions', 'Üstel Fonksiyonlar', 'MAT.11.2.2', 3, 5.8, 2.3, 'understand', 5),
('550e8400-e29b-41d4-a716-446655440018', '550e8400-e29b-41d4-a716-44665544000b', 'TRIGONOMETRY', 'Trigonometry', 'Trigonometri', 'MAT.10.3.1', 4, 7.5, 3.0, 'apply', 6),
('550e8400-e29b-41d4-a716-446655440019', '550e8400-e29b-41d4-a716-44665544000b', 'PROBABILITY', 'Probability', 'Olasılık', 'MAT.11.4.1', 3, 6.0, 2.4, 'apply', 7),
('550e8400-e29b-41d4-a716-44665544001a', '550e8400-e29b-41d4-a716-44665544000b', 'SEQUENCES', 'Sequences', 'Diziler', 'MAT.11.3.1', 4, 7.2, 2.9, 'analyze', 8);

-- 8. Fizik Konuları (Demo)
INSERT INTO topics (id, subject_id, code, name_en, name_tr, achievement_code, difficulty_level, exam_weight, exam_avg_questions, bloom_level, order_index) VALUES
('550e8400-e29b-41d4-a716-44665544001b', '550e8400-e29b-41d4-a716-44665544000c', 'MOTION', 'Motion', 'Hareket', 'FIZ.9.1.1', 3, 8.5, 1.2, 'apply', 1),
('550e8400-e29b-41d4-a716-44665544001c', '550e8400-e29b-41d4-a716-44665544000c', 'FORCE', 'Force and Motion', 'Kuvvet ve Hareket', 'FIZ.9.2.1', 4, 9.2, 1.3, 'apply', 2),
('550e8400-e29b-41d4-a716-44665544001d', '550e8400-e29b-41d4-a716-44665544000c', 'ENERGY', 'Energy', 'Enerji', 'FIZ.9.3.1', 3, 7.8, 1.1, 'understand', 3),
('550e8400-e29b-41d4-a716-44665544001e', '550e8400-e29b-41d4-a716-44665544000c', 'MAGNETISM', 'Magnetism', 'Manyetizma', 'FIZ.11.4.1', 5, 10.5, 1.5, 'analyze', 4),
('550e8400-e29b-41d4-a716-44665544001f', '550e8400-e29b-41d4-a716-44665544000c', 'ELECTRICITY', 'Electricity', 'Elektrik', 'FIZ.11.3.1', 4, 9.8, 1.4, 'apply', 5);

-- 9. Kimya Konuları (Demo)
INSERT INTO topics (id, subject_id, code, name_en, name_tr, achievement_code, difficulty_level, exam_weight, exam_avg_questions, bloom_level, order_index) VALUES
('550e8400-e29b-41d4-a716-446655440020', '550e8400-e29b-41d4-a716-44665544000d', 'ATOM', 'Atom', 'Atom', 'KIM.9.1.1', 3, 7.5, 1.0, 'understand', 1),
('550e8400-e29b-41d4-a716-446655440021', '550e8400-e29b-41d4-a716-44665544000d', 'PERIODIC_TABLE', 'Periodic Table', 'Periyodik Tablo', 'KIM.9.2.1', 3, 6.8, 0.9, 'remember', 2),
('550e8400-e29b-41d4-a716-446655440022', '550e8400-e29b-41d4-a716-44665544000d', 'CHEMICAL_BONDS', 'Chemical Bonds', 'Kimyasal Bağlar', 'KIM.10.1.1', 4, 8.5, 1.1, 'apply', 3),
('550e8400-e29b-41d4-a716-446655440023', '550e8400-e29b-41d4-a716-44665544000d', 'CHEMICAL_EQUILIBRIUM', 'Chemical Equilibrium', 'Kimyasal Denge', 'KIM.11.3.1', 5, 10.2, 1.3, 'analyze', 4),
('550e8400-e29b-41d4-a716-446655440024', '550e8400-e29b-41d4-a716-44665544000d', 'ACID_BASE', 'Acid and Base', 'Asit-Baz', 'KIM.11.4.1', 4, 9.0, 1.2, 'apply', 5);

-- 10. Soru Tipleri
INSERT INTO question_types (code, name_en, name_tr, scoring_method) VALUES
('MULTIPLE_CHOICE', 'Multiple Choice', 'Çoktan Seçmeli', 'DS_YS_BS'),
('OPEN_ENDED', 'Open Ended', 'Açık Uçlu', 'POINTS'),
('FILL_BLANK', 'Fill in the Blank', 'Boşluk Doldurma', 'POINTS'),
('TRUE_FALSE', 'True/False', 'Doğru/Yanlış', 'DS_YS_BS'),
('MATCHING', 'Matching', 'Eşleştirme', 'POINTS');