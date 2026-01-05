-- ============================================
-- Migration: 001_create_missing_tables
-- Description: Create missing core tables
-- Date: 2025-01-04
-- ============================================

-- 1. user_profiles (CORE)
CREATE TABLE IF NOT EXISTS public.user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT CHECK (role IN ('student', 'coach', 'admin', 'institution')),
  first_name TEXT,
  last_name TEXT,
  subscription_tier TEXT CHECK (subscription_tier IN ('free', 'basic', 'medium', 'premium')) DEFAULT 'free',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. test_records (TEST SYSTEM)
CREATE TABLE IF NOT EXISTS public.test_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  test_name TEXT,
  test_date DATE NOT NULL,
  test_type TEXT CHECK (test_type IN ('mock_exam', 'practice', 'daily_quiz')),
  total_questions INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. topic_test_results (MOTOR CONTEXT - CRITICAL!)
CREATE TABLE IF NOT EXISTS public.topic_test_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  test_record_id UUID REFERENCES public.test_records(id) ON DELETE CASCADE,
  topic_id UUID REFERENCES public.topics(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Performance metrics
  questions_total INT NOT NULL,
  questions_correct INT NOT NULL,
  questions_wrong INT NOT NULL,
  questions_blank INT NOT NULL,
  
  -- Timing data (crucial for BS-Model)
  time_spent_seconds INT NOT NULL,
  entry_timestamp TIMESTAMPTZ DEFAULT NOW(),
  
  -- Derived metrics
  success_rate DECIMAL(5,2),
  speed_score DECIMAL(5,2),
  
  -- Motor outputs
  bs_model_score DECIMAL(5,2),
  remembering_rate DECIMAL(5,2),
  priority_score DECIMAL(5,2),
  
  CONSTRAINT unique_user_topic_test UNIQUE(user_id, topic_id, test_record_id)
);

-- 4. prerequisites (PREREQUISITE SYSTEM)
CREATE TABLE IF NOT EXISTS public.prerequisites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_id UUID REFERENCES public.topics(id) ON DELETE CASCADE,
  prerequisite_topic_id UUID REFERENCES public.topics(id) ON DELETE CASCADE,
  strength DECIMAL(3,2) CHECK (strength BETWEEN 0 AND 1) DEFAULT 0.5,
  is_mandatory BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES auth.users(id)
);

-- ============================================
-- RLS POLICIES (Enable but allow service role)
-- ============================================

-- Enable RLS
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.test_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.topic_test_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prerequisites ENABLE ROW LEVEL SECURITY;

-- Allow service_role full access
CREATE POLICY "service_role_all_user_profiles" ON public.user_profiles FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_test_records" ON public.test_records FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_topic_test_results" ON public.topic_test_results FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_prerequisites" ON public.prerequisites FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Students can view own data
CREATE POLICY "students_view_own_profiles" ON public.user_profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "students_view_own_tests" ON public.test_records FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "students_view_own_results" ON public.topic_test_results FOR SELECT USING (auth.uid() = user_id);

-- ============================================
-- INDEXES for Performance
-- ============================================

CREATE INDEX IF NOT EXISTS idx_test_records_user_id ON public.test_records(user_id);
CREATE INDEX IF NOT EXISTS idx_test_records_test_date ON public.test_records(test_date);
CREATE INDEX IF NOT EXISTS idx_topic_test_results_user_topic ON public.topic_test_results(user_id, topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_test_results_test_id ON public.topic_test_results(test_record_id);
CREATE INDEX IF NOT EXISTS idx_prerequisites_topic ON public.prerequisites(topic_id);

-- ============================================
-- VERIFICATION
-- ============================================

-- Check created tables
SELECT 'user_profiles' as table_name, COUNT(*) as count FROM public.user_profiles
UNION ALL
SELECT 'test_records', COUNT(*) FROM public.test_records
UNION ALL
SELECT 'topic_test_results', COUNT(*) FROM public.topic_test_results
UNION ALL
SELECT 'prerequisites', COUNT(*) FROM public.prerequisites;

-- Done!
