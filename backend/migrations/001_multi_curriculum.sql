-- =============================================
-- MULTI-CURRICULUM SUPPORT
-- Mevcut veriyi BOZMADAN yeni yapı ekliyoruz
-- =============================================

-- 1. Curriculum Systems (Müfredat Sistemleri)
CREATE TABLE IF NOT EXISTS curriculum_systems (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    country_code VARCHAR(2),
    language VARCHAR(10) DEFAULT 'en',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Exam Types (Sınav Tipleri)
CREATE TABLE IF NOT EXISTS exam_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    curriculum_system_id UUID REFERENCES curriculum_systems(id),
    code VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(curriculum_system_id, code)
);

-- 3. Grade Levels (Sınıf Seviyeleri)
CREATE TABLE IF NOT EXISTS grade_levels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    curriculum_system_id UUID REFERENCES curriculum_systems(id),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(curriculum_system_id, code)
);

-- 4. Subjects tablosuna YENİ KOLON ekle (mevcut veriler bozulmaz!)
ALTER TABLE subjects 
ADD COLUMN IF NOT EXISTS curriculum_system_id UUID REFERENCES curriculum_systems(id);

-- 5. Subject-ExamType ilişkisi (Many-to-Many)
CREATE TABLE IF NOT EXISTS subject_exam_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID REFERENCES subjects(id) ON DELETE CASCADE,
    exam_type_id UUID REFERENCES exam_types(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(subject_id, exam_type_id)
);

-- 6. Subject-GradeLevel ilişkisi (Many-to-Many)
CREATE TABLE IF NOT EXISTS subject_grade_levels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID REFERENCES subjects(id) ON DELETE CASCADE,
    grade_level_id UUID REFERENCES grade_levels(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(subject_id, grade_level_id)
);

-- 7. Indexes (performance)
CREATE INDEX IF NOT EXISTS idx_subjects_curriculum ON subjects(curriculum_system_id);
CREATE INDEX IF NOT EXISTS idx_exam_types_curriculum ON exam_types(curriculum_system_id);
CREATE INDEX IF NOT EXISTS idx_grade_levels_curriculum ON grade_levels(curriculum_system_id);

COMMENT ON TABLE curriculum_systems IS 'Global müfredat sistemleri (Türkiye, ABD, Hindistan, vb.)';
COMMENT ON TABLE exam_types IS 'Sınav tipleri (TYT, AYT, SAT, JEE, vb.)';
COMMENT ON TABLE grade_levels IS 'Sınıf/derece seviyeleri (country-specific)';
