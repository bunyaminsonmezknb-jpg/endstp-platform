-- ============================================
-- ENDSTP PLATFORM - FULL DATABASE BACKUP
-- Date: 2025-11-18
-- Description: Complete schema with all tables
-- ============================================

-- ============================================
-- 1. AUTH & USER TABLES
-- ============================================

-- profiles (Supabase Auth tarafından oluşturuldu)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- students
CREATE TABLE IF NOT EXISTS students (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  name TEXT NOT NULL,
  class TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 2. TEST TABLES
-- ============================================

-- tests
CREATE TABLE IF NOT EXISTS tests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  subject TEXT NOT NULL,
  total_questions INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- test_results
CREATE TABLE IF NOT EXISTS test_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES students(id),
  user_id UUID REFERENCES profiles(id),
  entry_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
  subject TEXT NOT NULL,
  topic TEXT NOT NULL,
  correct_count INTEGER NOT NULL,
  wrong_count INTEGER NOT NULL,
  empty_count INTEGER NOT NULL,
  net DECIMAL(5,2) NOT NULL,
  success_rate DECIMAL(5,2),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 3. ANALYTICS TABLES
-- ============================================

-- analytics_events
CREATE TABLE IF NOT EXISTS analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  session_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  event_category TEXT,
  event_data JSONB,
  page_url TEXT,
  page_title TEXT,
  referrer TEXT,
  device_type TEXT,
  browser TEXT,
  os TEXT,
  screen_resolution TEXT,
  ip_address INET,
  country TEXT,
  city TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- user_sessions
CREATE TABLE IF NOT EXISTS user_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  session_id TEXT UNIQUE NOT NULL,
  started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  ended_at TIMESTAMP WITH TIME ZONE,
  duration_seconds INTEGER,
  page_views INTEGER DEFAULT 0,
  events_count INTEGER DEFAULT 0,
  device_type TEXT,
  browser TEXT,
  ip_address INET,
  country TEXT
);

-- daily_analytics_summary
CREATE TABLE IF NOT EXISTS daily_analytics_summary (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL UNIQUE,
  total_users INTEGER DEFAULT 0,
  new_users INTEGER DEFAULT 0,
  active_users INTEGER DEFAULT 0,
  returning_users INTEGER DEFAULT 0,
  total_sessions INTEGER DEFAULT 0,
  total_page_views INTEGER DEFAULT 0,
  avg_session_duration INTEGER DEFAULT 0,
  tests_submitted INTEGER DEFAULT 0,
  total_questions_answered INTEGER DEFAULT 0,
  avg_test_duration INTEGER DEFAULT 0,
  most_popular_subject TEXT,
  most_popular_topic TEXT,
  most_visited_page TEXT,
  calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- user_behavior_patterns
CREATE TABLE IF NOT EXISTS user_behavior_patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) UNIQUE,
  preferred_time_slot TEXT,
  most_active_days TEXT[],
  avg_session_duration INTEGER,
  favorite_subjects TEXT[],
  study_consistency_score INTEGER,
  best_performance_time TEXT,
  avg_daily_tests DECIMAL(5,2),
  last_active_at TIMESTAMP WITH TIME ZONE,
  total_tests INTEGER DEFAULT 0,
  total_study_hours INTEGER DEFAULT 0,
  churn_risk_score INTEGER DEFAULT 0,
  engagement_score INTEGER DEFAULT 50,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- teacher_feedback
CREATE TABLE IF NOT EXISTS teacher_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES students(id),
  teacher_id UUID REFERENCES profiles(id),
  test_result_id UUID REFERENCES test_results(id),
  tags TEXT[],
  difficulty_rating INTEGER CHECK (difficulty_rating BETWEEN 1 AND 5),
  focus_rating INTEGER CHECK (focus_rating BETWEEN 1 AND 5),
  comment TEXT,
  recommendations TEXT,
  student_mood TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- student_mood_logs
CREATE TABLE IF NOT EXISTS student_mood_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES students(id),
  test_result_id UUID REFERENCES test_results(id),
  mood_emoji TEXT,
  difficulty_perception TEXT,
  focus_level INTEGER CHECK (focus_level BETWEEN 1 AND 5),
  motivation_level INTEGER CHECK (motivation_level BETWEEN 1 AND 5),
  note TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- churn_risk_signals
CREATE TABLE IF NOT EXISTS churn_risk_signals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  signal_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  description TEXT,
  metadata JSONB,
  is_resolved BOOLEAN DEFAULT false,
  resolved_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 4. GLOBAL STRUCTURE TABLES
-- ============================================

-- countries
CREATE TABLE IF NOT EXISTS countries (
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

-- education_systems
CREATE TABLE IF NOT EXISTS education_systems (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_id UUID REFERENCES countries(id),
  code TEXT UNIQUE NOT NULL,
  name_en TEXT NOT NULL,
  name_local TEXT NOT NULL,
  description TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- education_levels
CREATE TABLE IF NOT EXISTS education_levels (
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

-- class_levels
CREATE TABLE IF NOT EXISTS class_levels (
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

-- exam_systems
CREATE TABLE IF NOT EXISTS exam_systems (
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

-- subjects
CREATE TABLE IF NOT EXISTS subjects (
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

-- topics
CREATE TABLE IF NOT EXISTS topics (
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

-- sub_topics
CREATE TABLE IF NOT EXISTS sub_topics (
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

-- question_types
CREATE TABLE IF NOT EXISTS question_types (
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

-- ============================================
-- 5. INDEXES
-- ============================================

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_events_user ON analytics_events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_session ON analytics_events(session_id);
CREATE INDEX IF NOT EXISTS idx_events_category ON analytics_events(event_category);
CREATE INDEX IF NOT EXISTS idx_events_created ON analytics_events(created_at DESC);

-- Session indexes
CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_started ON user_sessions(started_at DESC);

-- Feedback indexes
CREATE INDEX IF NOT EXISTS idx_feedback_student ON teacher_feedback(student_id);
CREATE INDEX IF NOT EXISTS idx_feedback_teacher ON teacher_feedback(teacher_id);
CREATE INDEX IF NOT EXISTS idx_feedback_created ON teacher_feedback(created_at DESC);

-- Mood indexes
CREATE INDEX IF NOT EXISTS idx_mood_student ON student_mood_logs(student_id);
CREATE INDEX IF NOT EXISTS idx_mood_created ON student_mood_logs(created_at DESC);

-- Churn indexes
CREATE INDEX IF NOT EXISTS idx_churn_user ON churn_risk_signals(user_id);
CREATE INDEX IF NOT EXISTS idx_churn_severity ON churn_risk_signals(severity);
CREATE INDEX IF NOT EXISTS idx_churn_resolved ON churn_risk_signals(is_resolved);

-- Global structure indexes
CREATE INDEX IF NOT EXISTS idx_countries_code ON countries(code);
CREATE INDEX IF NOT EXISTS idx_education_systems_country ON education_systems(country_id);
CREATE INDEX IF NOT EXISTS idx_education_levels_system ON education_levels(education_system_id);
CREATE INDEX IF NOT EXISTS idx_class_levels_education ON class_levels(education_level_id);
CREATE INDEX IF NOT EXISTS idx_exam_systems_education ON exam_systems(education_system_id);
CREATE INDEX IF NOT EXISTS idx_subjects_system ON subjects(education_system_id);
CREATE INDEX IF NOT EXISTS idx_subjects_class ON subjects(class_level_id);
CREATE INDEX IF NOT EXISTS idx_topics_subject ON topics(subject_id);
CREATE INDEX IF NOT EXISTS idx_sub_topics_topic ON sub_topics(topic_id);

-- ============================================
-- 6. RLS POLICIES (Currently Disabled)
-- ============================================

-- Note: All tables have RLS disabled for development
-- Enable in production with proper policies

-- ============================================
-- END OF BACKUP
-- ============================================