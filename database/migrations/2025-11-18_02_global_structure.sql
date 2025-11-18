-- ============================================
-- GLOBAL STRUCTURE - Multi-country Support
-- Date: 2025-11-18
-- Description: Countries, education systems, subjects, topics
-- ============================================

-- 1. Countries
CREATE TABLE countries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT UNIQUE NOT NULL,
  name_en TEXT NOT NULL,
  name_local TEXT NOT NULL,
  language TEXT DEFAULT 'tr',
  currency TEXT DEFAULT 'TRY',
  timezone TEXT DEFAULT 'Europe/Istanbul',
  date_format TEXT DEFAULT 'DD/MM/YYYY',
  number_format TEXT DEFAULT 'comma',
  is_active BOOLEAN DEFAULT true,
  order_index INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Education Systems
CREATE TABLE education_systems (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_id UUID REFERENCES countries(id),
  code TEXT UNIQUE NOT NULL,
  name_en TEXT NOT NULL,
  name_local TEXT NOT NULL,
  description TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Education Levels
CREATE TABLE education_levels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  education_system_id UUID REFERENCES education_systems(id),
  code TEXT NOT NULL,
  name_en TEXT NOT NULL,
  name_tr TEXT,
  name_local TEXT,
  grade_range TEXT,
  is_active BOOLEAN DEFAULT true,
  order_index INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Class Levels
CREATE TABLE class_levels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  education_level_id UUID REFERENCES education_levels(id),
  code TEXT NOT NULL,
  name_en TEXT NOT NULL,
  name_tr TEXT,
  name_local TEXT,
  grade_number INTEGER,
  is_active BOOLEAN DEFAULT true,
  order_index INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Exam Systems
CREATE TABLE exam_systems (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  education_system_id UUID REFERENCES education_systems(id),
  code TEXT UNIQUE NOT NULL,
  name_en TEXT NOT NULL,
  name_tr TEXT,
  name_local TEXT,
  description TEXT,
  total_duration_minutes INTEGER,
  sections JSONB,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Subjects
CREATE TABLE subjects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  education_system_id UUID REFERENCES education_systems(id),
  class_level_id UUID REFERENCES class_levels(id),
  code TEXT NOT NULL,
  name_en TEXT NOT NULL,
  name_tr TEXT,
  name_local TEXT,
  exam_system_id UUID REFERENCES exam_systems(id),
  total_questions INTEGER,
  question_weight DECIMAL(5,2),
  icon TEXT,
  color TEXT,
  is_active BOOLEAN DEFAULT true,
  order_index INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Topics
DROP TABLE IF EXISTS topics CASCADE;

CREATE TABLE topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id UUID REFERENCES subjects(id),
  code TEXT,
  name_en TEXT NOT NULL,
  name_tr TEXT,
  name_local TEXT,
  achievement_code TEXT,
  difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5) DEFAULT 3,
  exam_weight DECIMAL(5,2),
  exam_avg_questions DECIMAL(5,2),
  prerequisite_topics UUID[],
  bloom_level TEXT,
  description TEXT,
  learning_outcomes TEXT[],
  video_urls TEXT[],
  resource_urls TEXT[],
  is_active BOOLEAN DEFAULT true,
  order_index INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8. Sub Topics
CREATE TABLE sub_topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_id UUID REFERENCES topics(id),
  code TEXT,
  name_en TEXT NOT NULL,
  name_tr TEXT,
  name_local TEXT,
  achievement_code TEXT,
  is_active BOOLEAN DEFAULT true,
  order_index INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. Question Types
CREATE TABLE question_types (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT UNIQUE NOT NULL,
  name_en TEXT NOT NULL,
  name_tr TEXT,
  name_local TEXT,
  scoring_method TEXT,
  description TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_countries_code ON countries(code);
CREATE INDEX idx_education_systems_country ON education_systems(country_id);
CREATE INDEX idx_education_levels_system ON education_levels(education_system_id);
CREATE INDEX idx_class_levels_education ON class_levels(education_level_id);
CREATE INDEX idx_exam_systems_education ON exam_systems(education_system_id);
CREATE INDEX idx_subjects_system ON subjects(education_system_id);
CREATE INDEX idx_subjects_class ON subjects(class_level_id);
CREATE INDEX idx_topics_subject ON topics(subject_id);
CREATE INDEX idx_sub_topics_topic ON sub_topics(topic_id);

-- RLS Disable
ALTER TABLE countries DISABLE ROW LEVEL SECURITY;
ALTER TABLE education_systems DISABLE ROW LEVEL SECURITY;
ALTER TABLE education_levels DISABLE ROW LEVEL SECURITY;
ALTER TABLE class_levels DISABLE ROW LEVEL SECURITY;
ALTER TABLE exam_systems DISABLE ROW LEVEL SECURITY;
ALTER TABLE subjects DISABLE ROW LEVEL SECURITY;
ALTER TABLE topics DISABLE ROW LEVEL SECURITY;
ALTER TABLE sub_topics DISABLE ROW LEVEL SECURITY;
ALTER TABLE question_types DISABLE ROW LEVEL SECURITY;