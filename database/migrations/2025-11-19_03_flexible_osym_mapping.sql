-- ============================================
-- END.STP PLATFORM - COMPLETE FLEXIBLE ARCHITECTURE
-- Date: 2025-11-19
-- Description: ÖSYM mapping + Flexible exam context
-- ============================================

-- ============================================
-- PART 1: EXAM TYPES (Sınav Türleri)
-- ============================================

CREATE TABLE IF NOT EXISTS exam_types (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  exam_system_id UUID REFERENCES exam_systems(id),
  
  code TEXT NOT NULL,
  name_tr TEXT NOT NULL,
  name_en TEXT,
  short_name TEXT,
  
  duration_minutes INTEGER,
  total_questions INTEGER,
  subject_distribution JSONB,
  scoring_type TEXT,
  description TEXT,
  
  is_active BOOLEAN DEFAULT true,
  order_index INTEGER,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(exam_system_id, code)
);

-- ============================================
-- PART 2: ÖSYM OFFICIAL TOPICS (ÖSYM Resmi Konular)
-- ============================================

CREATE TABLE IF NOT EXISTS osym_topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  exam_type_id UUID REFERENCES exam_types(id),
  
  official_name TEXT NOT NULL,
  code TEXT,
  subject_name TEXT,
  
  description TEXT,
  notes TEXT,
  
  published_year INTEGER,
  related_grade_levels INTEGER[],
  
  is_active BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- PART 3: MEB-ÖSYM MAPPING (Konu Eşleştirme)
-- ============================================

CREATE TABLE IF NOT EXISTS topic_osym_mapping (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  meb_topic_id UUID REFERENCES topics(id),
  osym_topic_id UUID REFERENCES osym_topics(id),
  
  match_type TEXT,
  match_percentage INTEGER,
  
  mapping_notes TEXT,
  
  created_by TEXT,
  verified BOOLEAN DEFAULT false,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(meb_topic_id, osym_topic_id)
);

-- ============================================
-- PART 4: GRADE-EXAM MAPPING (Sınıf-Sınav İlişkisi)
-- ============================================

CREATE TABLE IF NOT EXISTS grade_exam_mapping (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  class_level_id UUID REFERENCES class_levels(id),
  exam_type_id UUID REFERENCES exam_types(id),
  
  relevance TEXT,
  notes TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(class_level_id, exam_type_id)
);

-- ============================================
-- PART 5: STUDENT EXAM GOALS (Öğrenci Sınav Hedefi)
-- ============================================

CREATE TABLE IF NOT EXISTS student_exam_goals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES students(id),
  exam_type_id UUID REFERENCES exam_types(id),
  
  target_year INTEGER,
  target_date DATE,
  
  status TEXT DEFAULT 'active',
  
  focus_subjects UUID[],
  weak_topics UUID[],
  
  notes TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- PART 6: TOPIC EXAM RELEVANCE (Konu-Sınav İlişkisi)
-- ============================================

CREATE TABLE IF NOT EXISTS topic_exam_relevance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_id UUID REFERENCES topics(id),
  exam_type_id UUID REFERENCES exam_types(id),
  
  is_relevant BOOLEAN DEFAULT true,
  importance_level TEXT,
  
  notes TEXT,
  
  first_appeared_year INTEGER,
  last_appeared_year INTEGER,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(topic_id, exam_type_id)
);

-- ============================================
-- PART 7: EXISTING TABLES UPDATE
-- ============================================

-- Subjects tablosuna exam_type_id ekle (eğer yoksa)
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'subjects' AND column_name = 'exam_type_id'
  ) THEN
    ALTER TABLE subjects ADD COLUMN exam_type_id UUID REFERENCES exam_types(id);
  END IF;
END $$;

-- Student_topic_difficulty güncellemeleri
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'student_topic_difficulty' AND column_name = 'exam_context_used'
  ) THEN
    ALTER TABLE student_topic_difficulty ADD COLUMN exam_context_used BOOLEAN DEFAULT false;
  END IF;
  
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'student_topic_difficulty' AND column_name = 'exam_weight_bonus'
  ) THEN
    ALTER TABLE student_topic_difficulty ADD COLUMN exam_weight_bonus INTEGER DEFAULT 0;
  END IF;
END $$;

-- Topic_exam_weights güncellemeleri
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'topic_exam_weights' AND column_name = 'osym_official_name'
  ) THEN
    ALTER TABLE topic_exam_weights ADD COLUMN osym_official_name TEXT;
  END IF;
  
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'topic_exam_weights' AND column_name = 'grade_levels'
  ) THEN
    ALTER TABLE topic_exam_weights ADD COLUMN grade_levels INTEGER[];
  END IF;
  
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'topic_exam_weights' AND column_name = 'exam_type_id'
  ) THEN
    ALTER TABLE topic_exam_weights ADD COLUMN exam_type_id UUID REFERENCES exam_types(id);
  END IF;
END $$;

-- Topic_yearly_stats güncellemeleri
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'topic_yearly_stats' AND column_name = 'exam_type_id'
  ) THEN
    ALTER TABLE topic_yearly_stats ADD COLUMN exam_type_id UUID REFERENCES exam_types(id);
  END IF;
END $$;

-- ============================================
-- PART 8: INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_exam_types_system ON exam_types(exam_system_id);
CREATE INDEX IF NOT EXISTS idx_exam_types_code ON exam_types(code);

CREATE INDEX IF NOT EXISTS idx_osym_topics_exam_type ON osym_topics(exam_type_id);
CREATE INDEX IF NOT EXISTS idx_osym_topics_published_year ON osym_topics(published_year);

CREATE INDEX IF NOT EXISTS idx_topic_osym_mapping_meb ON topic_osym_mapping(meb_topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_osym_mapping_osym ON topic_osym_mapping(osym_topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_osym_mapping_match ON topic_osym_mapping(match_type);

CREATE INDEX IF NOT EXISTS idx_grade_exam_mapping_grade ON grade_exam_mapping(class_level_id);
CREATE INDEX IF NOT EXISTS idx_grade_exam_mapping_exam ON grade_exam_mapping(exam_type_id);

CREATE INDEX IF NOT EXISTS idx_student_exam_goals_student ON student_exam_goals(student_id);
CREATE INDEX IF NOT EXISTS idx_student_exam_goals_exam ON student_exam_goals(exam_type_id);
CREATE INDEX IF NOT EXISTS idx_student_exam_goals_status ON student_exam_goals(status);

CREATE INDEX IF NOT EXISTS idx_topic_exam_relevance_topic ON topic_exam_relevance(topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_exam_relevance_exam ON topic_exam_relevance(exam_type_id);

CREATE INDEX IF NOT EXISTS idx_subjects_exam_type ON subjects(exam_type_id);

-- ============================================
-- PART 9: RLS DISABLE
-- ============================================

ALTER TABLE exam_types DISABLE ROW LEVEL SECURITY;
ALTER TABLE osym_topics DISABLE ROW LEVEL SECURITY;
ALTER TABLE topic_osym_mapping DISABLE ROW LEVEL SECURITY;
ALTER TABLE grade_exam_mapping DISABLE ROW LEVEL SECURITY;
ALTER TABLE student_exam_goals DISABLE ROW LEVEL SECURITY;
ALTER TABLE topic_exam_relevance DISABLE ROW LEVEL SECURITY;

-- ============================================
-- PART 10: SAMPLE DATA (Örnek Veriler)
-- ============================================

-- TYT ve AYT exam types
INSERT INTO exam_types (id, exam_system_id, code, name_tr, short_name, total_questions, order_index)
VALUES 
(
  '660e8400-e29b-41d4-a716-446655440001',
  '550e8400-e29b-41d4-a716-446655440009',
  'TYT',
  'Temel Yeterlilik Testi',
  'TYT',
  120,
  1
),
(
  '660e8400-e29b-41d4-a716-446655440002',
  '550e8400-e29b-41d4-a716-446655440009',
  'AYT',
  'Alan Yeterlilik Testi',
  'AYT',
  80,
  2
)
ON CONFLICT (exam_system_id, code) DO UPDATE SET
  name_tr = EXCLUDED.name_tr,
  total_questions = EXCLUDED.total_questions;

-- LGS exam type
INSERT INTO exam_types (id, exam_system_id, code, name_tr, short_name, total_questions, order_index)
SELECT 
  '660e8400-e29b-41d4-a716-446655440003',
  es.id,
  'LGS_MAIN',
  'Liselere Giriş Sınavı',
  'LGS',
  90,
  1
FROM exam_systems es
WHERE es.code = 'LGS'
ON CONFLICT (exam_system_id, code) DO UPDATE SET
  name_tr = EXCLUDED.name_tr;

-- Sınıf-Sınav eşleştirmeleri (9-10. sınıf → TYT)
INSERT INTO grade_exam_mapping (class_level_id, exam_type_id, relevance, notes)
SELECT 
  cl.id,
  '660e8400-e29b-41d4-a716-446655440001',
  'primary',
  '9. ve 10. sınıf konuları TYT kapsamındadır'
FROM class_levels cl
WHERE cl.grade_number IN (9, 10)
ON CONFLICT (class_level_id, exam_type_id) DO NOTHING;

-- 11-12. sınıf → AYT
INSERT INTO grade_exam_mapping (class_level_id, exam_type_id, relevance, notes)
SELECT 
  cl.id,
  '660e8400-e29b-41d4-a716-446655440002',
  'primary',
  '11. ve 12. sınıf konuları AYT kapsamındadır'
FROM class_levels cl
WHERE cl.grade_number IN (11, 12)
ON CONFLICT (class_level_id, exam_type_id) DO NOTHING;

-- 8. sınıf → LGS
INSERT INTO grade_exam_mapping (class_level_id, exam_type_id, relevance, notes)
SELECT 
  cl.id,
  '660e8400-e29b-41d4-a716-446655440003',
  'primary',
  '8. sınıf konuları LGS kapsamındadır'
FROM class_levels cl
WHERE cl.grade_number = 8
ON CONFLICT (class_level_id, exam_type_id) DO NOTHING;

-- Örnek ÖSYM konuları (TYT Matematik)
INSERT INTO osym_topics (id, exam_type_id, official_name, subject_name, related_grade_levels, published_year)
VALUES 
(
  '770e8400-e29b-41d4-a716-446655440001',
  '660e8400-e29b-41d4-a716-446655440001',
  'Kümeler, Kartezyen Çarpım',
  'TYT Matematik',
  ARRAY[9, 10],
  2024
),
(
  '770e8400-e29b-41d4-a716-446655440002',
  '660e8400-e29b-41d4-a716-446655440001',
  'Denklemler ve Eşitsizlikler',
  'TYT Matematik',
  ARRAY[9, 10],
  2024
),
(
  '770e8400-e29b-41d4-a716-446655440003',
  '660e8400-e29b-41d4-a716-446655440001',
  'Fonksiyonlar',
  'TYT Matematik',
  ARRAY[9, 10],
  2024
)
ON CONFLICT DO NOTHING;

-- Örnek ÖSYM konuları (AYT Matematik)
INSERT INTO osym_topics (id, exam_type_id, official_name, subject_name, related_grade_levels, published_year)
VALUES 
(
  '770e8400-e29b-41d4-a716-446655440010',
  '660e8400-e29b-41d4-a716-446655440002',
  'Limit ve Süreklilik',
  'AYT Matematik',
  ARRAY[11, 12],
  2024
),
(
  '770e8400-e29b-41d4-a716-446655440011',
  '660e8400-e29b-41d4-a716-446655440002',
  'Türev',
  'AYT Matematik',
  ARRAY[11, 12],
  2024
),
(
  '770e8400-e29b-41d4-a716-446655440012',
  '660e8400-e29b-41d4-a716-446655440002',
  'İntegral',
  'AYT Matematik',
  ARRAY[11, 12],
  2024
)
ON CONFLICT DO NOTHING;

-- ============================================
-- COMPLETED!
-- ============================================

-- Tablo sayısını göster
SELECT 
  'exam_types' as table_name, COUNT(*) as row_count FROM exam_types
UNION ALL
SELECT 'osym_topics', COUNT(*) FROM osym_topics
UNION ALL
SELECT 'topic_osym_mapping', COUNT(*) FROM topic_osym_mapping
UNION ALL
SELECT 'grade_exam_mapping', COUNT(*) FROM grade_exam_mapping
UNION ALL
SELECT 'student_exam_goals', COUNT(*) FROM student_exam_goals
UNION ALL
SELECT 'topic_exam_relevance', COUNT(*) FROM topic_exam_relevance;