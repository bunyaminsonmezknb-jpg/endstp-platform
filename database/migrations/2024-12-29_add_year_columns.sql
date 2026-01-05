-- ============================================
-- ADD YEAR COLUMNS TO TOPICS TABLE
-- ============================================
-- Purpose: Store yearly question counts (2018-2025)
-- Updates: exam_frequency calculation
-- Duration: ~2 minutes to apply
-- ============================================

-- 1. ADD YEAR COLUMNS
-- ============================================
ALTER TABLE topics
ADD COLUMN IF NOT EXISTS q_2018 DECIMAL(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS q_2019 DECIMAL(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS q_2020 DECIMAL(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS q_2021 DECIMAL(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS q_2022 DECIMAL(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS q_2023 DECIMAL(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS q_2024 DECIMAL(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS q_2025 DECIMAL(4,2) DEFAULT 0;

-- Add comment
COMMENT ON COLUMN topics.q_2018 IS 'Number of questions in 2018 exams (TYT/AYT)';
COMMENT ON COLUMN topics.q_2019 IS 'Number of questions in 2019 exams (TYT/AYT)';
COMMENT ON COLUMN topics.q_2020 IS 'Number of questions in 2020 exams (TYT/AYT)';
COMMENT ON COLUMN topics.q_2021 IS 'Number of questions in 2021 exams (TYT/AYT)';
COMMENT ON COLUMN topics.q_2022 IS 'Number of questions in 2022 exams (TYT/AYT)';
COMMENT ON COLUMN topics.q_2023 IS 'Number of questions in 2023 exams (TYT/AYT)';
COMMENT ON COLUMN topics.q_2024 IS 'Number of questions in 2024 exams (TYT/AYT)';
COMMENT ON COLUMN topics.q_2025 IS 'Number of questions in 2025 exams (TYT/AYT)';

-- ============================================
-- 2. CREATE FREQUENCY CALCULATION FUNCTION
-- ============================================
CREATE OR REPLACE FUNCTION calculate_topic_frequency(
  p_topic_id UUID,
  p_years_back INT DEFAULT 5
) RETURNS DECIMAL(5,2) AS $$
DECLARE
  topic_total DECIMAL(10,2);
  subject_total DECIMAL(10,2);
  frequency_ratio DECIMAL(10,5);
  normalized_score DECIMAL(5,2);
BEGIN
  -- Get topic's total questions in last N years
  SELECT 
    CASE 
      WHEN p_years_back = 8 THEN 
        COALESCE(q_2018, 0) + COALESCE(q_2019, 0) + COALESCE(q_2020, 0) + 
        COALESCE(q_2021, 0) + COALESCE(q_2022, 0) + COALESCE(q_2023, 0) + 
        COALESCE(q_2024, 0) + COALESCE(q_2025, 0)
      WHEN p_years_back = 5 THEN 
        COALESCE(q_2020, 0) + COALESCE(q_2021, 0) + COALESCE(q_2022, 0) + 
        COALESCE(q_2023, 0) + COALESCE(q_2024, 0)
      WHEN p_years_back = 3 THEN 
        COALESCE(q_2022, 0) + COALESCE(q_2023, 0) + COALESCE(q_2024, 0)
      ELSE 
        COALESCE(q_2023, 0) + COALESCE(q_2024, 0)  -- Default 2 years
    END
  INTO topic_total
  FROM topics
  WHERE id = p_topic_id;
  
  -- Get subject's total questions in last N years
  SELECT 
    SUM(
      CASE 
        WHEN p_years_back = 8 THEN 
          COALESCE(q_2018, 0) + COALESCE(q_2019, 0) + COALESCE(q_2020, 0) + 
          COALESCE(q_2021, 0) + COALESCE(q_2022, 0) + COALESCE(q_2023, 0) + 
          COALESCE(q_2024, 0) + COALESCE(q_2025, 0)
        WHEN p_years_back = 5 THEN 
          COALESCE(q_2020, 0) + COALESCE(q_2021, 0) + COALESCE(q_2022, 0) + 
          COALESCE(q_2023, 0) + COALESCE(q_2024, 0)
        WHEN p_years_back = 3 THEN 
          COALESCE(q_2022, 0) + COALESCE(q_2023, 0) + COALESCE(q_2024, 0)
        ELSE 
          COALESCE(q_2023, 0) + COALESCE(q_2024, 0)
      END
    )
  INTO subject_total
  FROM topics
  WHERE subject_id = (SELECT subject_id FROM topics WHERE id = p_topic_id)
    AND grade_level = (SELECT grade_level FROM topics WHERE id = p_topic_id);
  
  -- Avoid division by zero
  IF subject_total = 0 OR subject_total IS NULL THEN
    RETURN 1.0;
  END IF;
  
  -- Calculate frequency ratio
  frequency_ratio := topic_total / subject_total;
  
  -- Normalize to 0.6 - 1.4 range
  -- Low frequency: < 0.05 → 0.6-0.8
  -- Medium: 0.05 - 0.15 → 0.8-1.0
  -- High: > 0.15 → 1.0-1.4
  
  IF frequency_ratio < 0.05 THEN
    normalized_score := 0.6 + (frequency_ratio / 0.05) * 0.2;
  ELSIF frequency_ratio < 0.15 THEN
    normalized_score := 0.8 + ((frequency_ratio - 0.05) / 0.10) * 0.2;
  ELSE
    normalized_score := 1.0 + LEAST((frequency_ratio - 0.15) / 0.15, 0.4);
  END IF;
  
  RETURN normalized_score;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION calculate_topic_frequency IS 
'Calculates exam frequency score (0.6-1.4) based on topic question count vs subject total';

-- ============================================
-- 3. CREATE UPDATE TRIGGER (Optional)
-- ============================================
-- Automatically update exam_frequency when year columns change

CREATE OR REPLACE FUNCTION update_exam_frequency_trigger()
RETURNS TRIGGER AS $$
BEGIN
  -- Calculate and update exam_frequency (5 years default)
  NEW.exam_frequency := calculate_topic_frequency(NEW.id, 5);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop if exists
DROP TRIGGER IF EXISTS trigger_update_exam_frequency ON topics;

-- Create trigger
CREATE TRIGGER trigger_update_exam_frequency
  BEFORE INSERT OR UPDATE OF q_2018, q_2019, q_2020, q_2021, q_2022, q_2023, q_2024, q_2025
  ON topics
  FOR EACH ROW
  EXECUTE FUNCTION update_exam_frequency_trigger();

COMMENT ON TRIGGER trigger_update_exam_frequency ON topics IS 
'Auto-updates exam_frequency when year columns change';

-- ============================================
-- 4. CREATE HELPER FUNCTION (Batch Update)
-- ============================================
CREATE OR REPLACE FUNCTION update_all_exam_frequencies(
  p_years_back INT DEFAULT 5
) RETURNS TABLE(
  updated_count INT,
  avg_frequency DECIMAL(5,2),
  max_frequency DECIMAL(5,2),
  min_frequency DECIMAL(5,2)
) AS $$
DECLARE
  v_updated_count INT := 0;
BEGIN
  -- Update all topics
  UPDATE topics
  SET exam_frequency = calculate_topic_frequency(id, p_years_back)
  WHERE id IS NOT NULL;
  
  GET DIAGNOSTICS v_updated_count = ROW_COUNT;
  
  -- Return statistics
  RETURN QUERY
  SELECT 
    v_updated_count,
    ROUND(AVG(exam_frequency)::NUMERIC, 2),
    ROUND(MAX(exam_frequency)::NUMERIC, 2),
    ROUND(MIN(exam_frequency)::NUMERIC, 2)
  FROM topics
  WHERE exam_frequency IS NOT NULL;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION update_all_exam_frequencies IS 
'Batch update exam_frequency for all topics. Returns statistics.';

-- ============================================
-- 5. CREATE INDEX FOR PERFORMANCE
-- ============================================
-- Index for fast year-based filtering
CREATE INDEX IF NOT EXISTS idx_topics_year_totals 
ON topics (
  (COALESCE(q_2020, 0) + COALESCE(q_2021, 0) + COALESCE(q_2022, 0) + 
   COALESCE(q_2023, 0) + COALESCE(q_2024, 0))
);

CREATE INDEX IF NOT EXISTS idx_topics_exam_frequency 
ON topics(exam_frequency) 
WHERE exam_frequency IS NOT NULL;

COMMENT ON INDEX idx_topics_year_totals IS 'Fast filtering by 5-year question total';
COMMENT ON INDEX idx_topics_exam_frequency IS 'Fast sorting by exam frequency';

-- ============================================
-- 6. VERIFICATION QUERIES
-- ============================================

-- Check if columns added
SELECT 
    column_name, 
    data_type,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'topics'
  AND column_name LIKE 'q_20%'
ORDER BY column_name;

-- Count topics with year data
SELECT 
    COUNT(*) as total_topics,
    COUNT(*) FILTER (WHERE q_2024 > 0) as topics_2024,
    COUNT(*) FILTER (WHERE q_2023 > 0) as topics_2023,
    COUNT(*) FILTER (WHERE exam_frequency IS NOT NULL) as with_frequency
FROM topics;

-- Test frequency calculation
SELECT 
    name_tr,
    grade_level,
    q_2020, q_2021, q_2022, q_2023, q_2024,
    calculate_topic_frequency(id, 5) as freq_score
FROM topics
WHERE q_2024 > 0 OR q_2023 > 0
LIMIT 5;

-- ============================================
-- DONE! Ready for Excel seed
-- ============================================
-- Next steps:
-- 1. Run Excel seed script (updates q_2018-q_2025)
-- 2. Run: SELECT update_all_exam_frequencies(5);
-- 3. Verify: SELECT COUNT(*) FROM topics WHERE exam_frequency IS NOT NULL;
