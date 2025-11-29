-- ============================================
-- END.STP - 5 Motor Sistemi Migration
-- Tarih: 28 Kasım 2024
-- Versiyon: 1.0
-- ============================================

-- 1. BS-MODEL + DIFFICULTY + TIME + PRIORITY için alanlar
ALTER TABLE student_topic_tests ADD COLUMN IF NOT EXISTS
  ease_factor DECIMAL(3,2) DEFAULT 2.5 CHECK (ease_factor BETWEEN 1.3 AND 2.5),
  interval INTEGER DEFAULT 1 CHECK (interval >= 0),
  actual_gap INTEGER DEFAULT 0 CHECK (actual_gap >= 0),
  repetitions INTEGER DEFAULT 0 CHECK (repetitions >= 0),
  status VARCHAR(20) DEFAULT 'NEW' CHECK (status IN ('NEW', 'NORMAL', 'HERO', 'RESET', 'RECOVERY')),
  total_duration_minutes DECIMAL(5,2) NULL CHECK (total_duration_minutes > 0),
  pace_ratio DECIMAL(3,2) NULL,
  time_modifier DECIMAL(3,2) DEFAULT 1.0 CHECK (time_modifier BETWEEN 0.5 AND 2.0),
  difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
  priority_score DECIMAL(5,2) NULL CHECK (priority_score BETWEEN 0 AND 100),
  priority_level VARCHAR(20) NULL CHECK (priority_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'));

-- 2. Topics tablosu - Stratejik ağırlıklar
ALTER TABLE topics ADD COLUMN IF NOT EXISTS
  difficulty INTEGER DEFAULT 3 CHECK (difficulty BETWEEN 1 AND 5),
  ideal_time_per_question DECIMAL(3,1) DEFAULT 1.5 CHECK (ideal_time_per_question > 0),
  topic_weight DECIMAL(4,3) DEFAULT 0.025 CHECK (topic_weight BETWEEN 0 AND 1),
  exam_frequency DECIMAL(3,2) NULL CHECK (exam_frequency BETWEEN 0 AND 1);

-- 3. Courses tablosu - Importance
ALTER TABLE courses ADD COLUMN IF NOT EXISTS
  total_questions INTEGER DEFAULT 40 CHECK (total_questions > 0),
  coefficient DECIMAL(3,2) DEFAULT 1.0 CHECK (coefficient > 0);

-- 4. Course Stats Cache (Performans için)
CREATE TABLE IF NOT EXISTS course_stats_cache (
  student_id UUID NOT NULL,
  course_id INTEGER NOT NULL,
  total_correct INTEGER DEFAULT 0 CHECK (total_correct >= 0),
  total_incorrect INTEGER DEFAULT 0 CHECK (total_incorrect >= 0),
  total_blank INTEGER DEFAULT 0 CHECK (total_blank >= 0),
  total_questions INTEGER DEFAULT 0 CHECK (total_questions >= 0),
  last_updated TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- 5. Partner Resources (Ticari linkler)
CREATE TABLE IF NOT EXISTS partner_resources (
  id SERIAL PRIMARY KEY,
  topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  resource_type VARCHAR(20) NOT NULL CHECK (resource_type IN ('VIDEO', 'TEST', 'BOOK', 'COURSE', 'ARTICLE')),
  provider VARCHAR(100) NOT NULL,
  title VARCHAR(200) NOT NULL,
  url TEXT NOT NULL,
  affiliate_link TEXT,
  difficulty_match INTEGER CHECK (difficulty_match BETWEEN 1 AND 5),
  priority_match VARCHAR(20) CHECK (priority_match IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
  is_free BOOLEAN DEFAULT false,
  price DECIMAL(10,2) NULL CHECK (price >= 0),
  rating DECIMAL(2,1) CHECK (rating BETWEEN 0 AND 5),
  view_count INTEGER DEFAULT 0 CHECK (view_count >= 0),
  click_count INTEGER DEFAULT 0 CHECK (click_count >= 0),
  created_at TIMESTAMP DEFAULT NOW()
);

-- 6. İndeksler (Performans)
CREATE INDEX IF NOT EXISTS idx_student_topic_status ON student_topic_tests(student_id, topic_id, status);
CREATE INDEX IF NOT EXISTS idx_student_topic_repetitions ON student_topic_tests(student_id, topic_id, repetitions);
CREATE INDEX IF NOT EXISTS idx_course_stats_student ON course_stats_cache(student_id);
CREATE INDEX IF NOT EXISTS idx_partner_topic ON partner_resources(topic_id, difficulty_match);

-- 7. Yorum ekle (Dokümantasyon)
COMMENT ON COLUMN student_topic_tests.ease_factor IS 'BS-Model: Kolay faktörü (1.3-2.5)';
COMMENT ON COLUMN student_topic_tests.status IS 'BS-Model: NEW/NORMAL/HERO/RESET/RECOVERY';
COMMENT ON COLUMN student_topic_tests.difficulty_level IS 'Difficulty Engine: Konu zorluğu (1-5)';
COMMENT ON COLUMN student_topic_tests.priority_score IS 'Priority Engine: Öncelik puanı (0-100)';
COMMENT ON TABLE course_stats_cache IS 'Performans cache - Course context hesaplamaları için';
COMMENT ON TABLE partner_resources IS 'Ticari linkler ve affiliate kaynaklar';
