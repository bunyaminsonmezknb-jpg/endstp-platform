-- ============================================
-- ANALYTICS & MONITORING TABLES
-- Date: 2025-11-18
-- Description: User behavior tracking and analytics
-- ============================================

-- 1. Analytics Events
CREATE TABLE analytics_events (
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

-- 2. User Sessions
CREATE TABLE user_sessions (
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

-- 3. Daily Analytics Summary
CREATE TABLE daily_analytics_summary (
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

-- 4. User Behavior Patterns
CREATE TABLE user_behavior_patterns (
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

-- 5. Teacher Feedback
CREATE TABLE teacher_feedback (
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

-- 6. Student Mood Logs
CREATE TABLE student_mood_logs (
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

-- 7. Churn Risk Signals
CREATE TABLE churn_risk_signals (
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

-- Indexes
CREATE INDEX idx_events_user ON analytics_events(user_id);
CREATE INDEX idx_events_type ON analytics_events(event_type);
CREATE INDEX idx_events_session ON analytics_events(session_id);
CREATE INDEX idx_events_category ON analytics_events(event_category);
CREATE INDEX idx_events_created ON analytics_events(created_at DESC);

CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_started ON user_sessions(started_at DESC);

CREATE INDEX idx_feedback_student ON teacher_feedback(student_id);
CREATE INDEX idx_feedback_teacher ON teacher_feedback(teacher_id);
CREATE INDEX idx_feedback_created ON teacher_feedback(created_at DESC);

CREATE INDEX idx_mood_student ON student_mood_logs(student_id);
CREATE INDEX idx_mood_created ON student_mood_logs(created_at DESC);

CREATE INDEX idx_churn_user ON churn_risk_signals(user_id);
CREATE INDEX idx_churn_severity ON churn_risk_signals(severity);
CREATE INDEX idx_churn_resolved ON churn_risk_signals(is_resolved);

-- RLS Disable
ALTER TABLE analytics_events DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE daily_analytics_summary DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_behavior_patterns DISABLE ROW LEVEL SECURITY;
ALTER TABLE teacher_feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE student_mood_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE churn_risk_signals DISABLE ROW LEVEL SECURITY;