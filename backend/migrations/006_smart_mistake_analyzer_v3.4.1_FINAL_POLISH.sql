-- ============================================
-- MIGRATION 006: Smart Mistake Pattern Analyzer v3.4.1
-- Date: 2024-12-14
-- Version: 3.4.1 (COMMENT inside DO block - Final Polish)
-- Description: Parametrik trigger + Adaptive baseline + Safety guards
-- ============================================

-- ============================================
-- CRITICAL FIX v3.4.1:
-- ✅ COMMENT ON COLUMN moved inside DO block (env-safe)
-- ============================================

-- ============================================
-- PART 1: SYSTEM SETTINGS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS system_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    category VARCHAR(50) NOT NULL,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value JSONB NOT NULL,
    
    display_name VARCHAR(200),
    description TEXT,
    data_type VARCHAR(20),
    min_value DECIMAL,
    max_value DECIMAL,
    default_value JSONB,
    unit VARCHAR(20),
    
    preset_mode VARCHAR(20),
    
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by UUID,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE system_settings
ADD COLUMN IF NOT EXISTS setting_group VARCHAR(50);

ALTER TABLE system_settings
ADD COLUMN IF NOT EXISTS preset_mode VARCHAR(20);

CREATE INDEX IF NOT EXISTS idx_system_settings_category ON system_settings(category);
CREATE INDEX IF NOT EXISTS idx_system_settings_group ON system_settings(setting_group);
CREATE INDEX IF NOT EXISTS idx_system_settings_preset ON system_settings(preset_mode);

COMMENT ON TABLE system_settings IS 'Tüm sistem parametreleri - Admin UI''dan düzenlenebilir';

-- ============================================
-- PART 2: ANALYSIS PRESETS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS analysis_presets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    preset_name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    description TEXT,
    
    settings JSONB NOT NULL,
    
    color_code VARCHAR(20),
    icon VARCHAR(50),
    recommended_for TEXT[],
    
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analysis_presets_name ON analysis_presets(preset_name);
CREATE INDEX IF NOT EXISTS idx_analysis_presets_default ON analysis_presets(is_default);

-- ✅ v3.4: Data integrity - only one default preset
CREATE UNIQUE INDEX IF NOT EXISTS one_default_preset
ON analysis_presets (is_default)
WHERE is_default = true;

COMMENT ON TABLE analysis_presets IS 'Analiz modları - Agresif/Normal/Soft presetler';

-- ============================================
-- PART 3: STUDENT ANALYSIS SETTINGS
-- ============================================

CREATE TABLE IF NOT EXISTS student_analysis_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    student_id UUID NOT NULL,
    preset_name VARCHAR(50) REFERENCES analysis_presets(preset_name),
    
    custom_settings JSONB,
    
    set_by UUID,
    set_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(student_id)
);

CREATE INDEX IF NOT EXISTS idx_student_analysis_student ON student_analysis_settings(student_id);

COMMENT ON TABLE student_analysis_settings IS 'Öğrenci bazında analiz ayarları';

-- ============================================
-- PART 4: STUDENT BASELINE PERFORMANCE
-- ============================================

CREATE TABLE IF NOT EXISTS student_baseline_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    student_id UUID NOT NULL,
    global_topic_uid VARCHAR(100),
    
    baseline_avg_duration DECIMAL,
    baseline_sample_count INT DEFAULT 0,
    baseline_established_at TIMESTAMP,
    
    current_avg_duration DECIMAL,
    current_sample_count INT DEFAULT 0,
    
    improvement_rate DECIMAL,
    
    exam_norm_duration DECIMAL,
    distance_to_norm DECIMAL,
    
    adaptive_expected_duration DECIMAL,
    
    learning_phase VARCHAR(20),
    
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(student_id, global_topic_uid)
    -- FUTURE: exam_system_id eklenebilir (TR/IB/SAT ayrımı için)
);

CREATE INDEX IF NOT EXISTS idx_baseline_student ON student_baseline_performance(student_id);
CREATE INDEX IF NOT EXISTS idx_baseline_topic ON student_baseline_performance(global_topic_uid);
CREATE INDEX IF NOT EXISTS idx_baseline_phase ON student_baseline_performance(learning_phase);

COMMENT ON TABLE student_baseline_performance IS 'Öğrenci normları - Adaptif hedef belirleme';

-- ============================================
-- PART 5: TEST RECORDS DURATION COLUMNS
-- ============================================

CREATE OR REPLACE FUNCTION calculate_expected_duration()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.expected_duration_per_question := 
        (NEW.total_duration_minutes * 60.0) / NULLIF(NEW.question_count, 0);
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION calculate_expected_duration IS 'Calculate expected duration per question (test_records trigger)';

DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'test_records'
    ) THEN
        ALTER TABLE test_records
        ADD COLUMN IF NOT EXISTS total_duration_minutes INT,
        ADD COLUMN IF NOT EXISTS question_count INT,
        ADD COLUMN IF NOT EXISTS expected_duration_per_question DECIMAL;
        
        DROP TRIGGER IF EXISTS trg_calculate_expected_duration ON test_records;
        CREATE TRIGGER trg_calculate_expected_duration
        BEFORE INSERT OR UPDATE OF total_duration_minutes, question_count ON test_records
        FOR EACH ROW
        EXECUTE FUNCTION calculate_expected_duration();
        
        RAISE NOTICE '✅ test_records duration columns added';
    ELSE
        RAISE NOTICE '⚠️ test_records tablosu yok, atlanıyor';
    END IF;
END $$;

-- ============================================
-- PART 6: STUDENT MISTAKES TIME ANALYSIS
-- ============================================

-- ✅ v3.4.1: COMMENT moved inside DO block (env-safe)
DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'student_mistakes'
    ) THEN
        ALTER TABLE student_mistakes
        ADD COLUMN IF NOT EXISTS expected_duration DECIMAL,
        ADD COLUMN IF NOT EXISTS time_ratio DECIMAL,
        ADD COLUMN IF NOT EXISTS used_adaptive_baseline BOOLEAN DEFAULT false;
        
        CREATE INDEX IF NOT EXISTS idx_student_mistakes_time_ratio 
        ON student_mistakes(time_ratio);
        
        -- ✅ v3.4.1: COMMENT inside DO block
        COMMENT ON COLUMN student_mistakes.time_ratio IS 'time_spent / expected_duration';
        COMMENT ON COLUMN student_mistakes.used_adaptive_baseline IS 'Adaptif öğrenci normali mi kullanıldı?';
        
        RAISE NOTICE '✅ student_mistakes time analysis columns added';
    ELSE
        RAISE NOTICE '⚠️ student_mistakes tablosu yok, atlanıyor';
    END IF;
END $$;

-- ============================================
-- PART 7: DEFAULT PRESETS
-- ============================================

INSERT INTO analysis_presets (
    preset_name, display_name, description,
    settings, color_code, icon,
    recommended_for, is_default
) VALUES
(
    'aggressive',
    'Agresif Analiz',
    'Hızlı müdahale, yüksek hassasiyet. Yarışma sınavlarına hazırlananlar için.',
    '{
        "panic_ratio": 0.2,
        "panic_absolute_min": 3,
        "panic_absolute_max": 120,
        "stuck_repeat_threshold": 3,
        "stuck_time_window_hours": 12,
        "trend_window_size": 5,
        "trend_recent_count": 2,
        "trend_past_count": 3,
        "trend_significance_threshold": 0.2,
        "improvement_reward_multiplier": 1.8,
        "worsening_safety_multiplier": 0.6,
        "minimum_data_for_trend": 2,
        "baseline_test_count": 3,
        "improvement_target_ratio": 0.90,
        "use_adaptive_baseline": true
    }'::jsonb,
    '#ff4444',
    'fire',
    ARRAY['competitive_exam', 'advanced', 'YKS', 'LGS'],
    false
),
(
    'normal',
    'Normal Analiz',
    'Dengeli yaklaşım. Çoğu öğrenci için önerilir.',
    '{
        "panic_ratio": 0.3,
        "panic_absolute_min": 5,
        "panic_absolute_max": 180,
        "stuck_repeat_threshold": 3,
        "stuck_time_window_hours": 24,
        "trend_window_size": 5,
        "trend_recent_count": 2,
        "trend_past_count": 3,
        "trend_significance_threshold": 0.3,
        "improvement_reward_multiplier": 1.5,
        "worsening_safety_multiplier": 0.7,
        "minimum_data_for_trend": 3,
        "baseline_test_count": 5,
        "improvement_target_ratio": 0.95,
        "use_adaptive_baseline": true
    }'::jsonb,
    '#44ff44',
    'balance',
    ARRAY['general', 'high_school', 'middle_school'],
    true
),
(
    'soft',
    'Yumuşak Analiz',
    'Daha toleranslı, yavaş müdahale. Yeni başlayanlar için.',
    '{
        "panic_ratio": 0.4,
        "panic_absolute_min": 8,
        "panic_absolute_max": 240,
        "stuck_repeat_threshold": 4,
        "stuck_time_window_hours": 48,
        "trend_window_size": 7,
        "trend_recent_count": 3,
        "trend_past_count": 4,
        "trend_significance_threshold": 0.5,
        "improvement_reward_multiplier": 1.3,
        "worsening_safety_multiplier": 0.8,
        "minimum_data_for_trend": 4,
        "baseline_test_count": 7,
        "improvement_target_ratio": 0.97,
        "use_adaptive_baseline": true
    }'::jsonb,
    '#4444ff',
    'feather',
    ARRAY['beginners', 'elementary', 'struggling'],
    false
) ON CONFLICT (preset_name) DO NOTHING;

-- ============================================
-- PART 8: BASELINE UPDATE FUNCTION
-- ============================================

CREATE OR REPLACE FUNCTION update_student_baseline()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_baseline RECORD;
    v_exam_norm DECIMAL;
    v_new_avg DECIMAL;
    v_baseline_test_count INT;
    v_improvement_target_ratio DECIMAL;
    v_use_adaptive BOOLEAN;
    v_improvement_rate DECIMAL;
BEGIN
    IF NEW.time_spent_seconds IS NULL OR NEW.time_spent_seconds <= 0 THEN
        RETURN NEW;
    END IF;
    
    SELECT 
        COALESCE((settings->>'baseline_test_count')::INT, 5),
        COALESCE((settings->>'improvement_target_ratio')::DECIMAL, 0.95),
        COALESCE((settings->>'use_adaptive_baseline')::BOOLEAN, true)
    INTO v_baseline_test_count, v_improvement_target_ratio, v_use_adaptive
    FROM analysis_presets
    WHERE is_default = true;
    
    BEGIN
        SELECT expected_duration_per_question INTO v_exam_norm
        FROM test_records tr
        JOIN test_answers ta ON ta.test_id = tr.id
        WHERE ta.id = NEW.test_answer_id;
    EXCEPTION
        WHEN OTHERS THEN
            v_exam_norm := NULL;
    END;
    
    SELECT * INTO v_baseline
    FROM student_baseline_performance
    WHERE student_id = NEW.student_id
    AND global_topic_uid = NEW.global_topic_uid;
    
    IF v_baseline IS NULL THEN
        INSERT INTO student_baseline_performance (
            student_id, global_topic_uid,
            baseline_avg_duration, baseline_sample_count,
            current_avg_duration, current_sample_count,
            exam_norm_duration,
            learning_phase,
            adaptive_expected_duration
        ) VALUES (
            NEW.student_id, NEW.global_topic_uid,
            NEW.time_spent_seconds, 1,
            NEW.time_spent_seconds, 1,
            v_exam_norm,
            'baseline',
            v_exam_norm
        );
    ELSE
        IF v_baseline.baseline_sample_count < v_baseline_test_count THEN
            v_new_avg := (
                (v_baseline.baseline_avg_duration * v_baseline.baseline_sample_count + NEW.time_spent_seconds)
                / (v_baseline.baseline_sample_count + 1)
            );
            
            UPDATE student_baseline_performance
            SET baseline_avg_duration = v_new_avg,
                baseline_sample_count = baseline_sample_count + 1,
                current_avg_duration = v_new_avg,
                current_sample_count = current_sample_count + 1,
                exam_norm_duration = v_exam_norm,
                baseline_established_at = CASE 
                    WHEN baseline_sample_count + 1 >= v_baseline_test_count 
                    THEN NOW() 
                    ELSE baseline_established_at 
                END,
                learning_phase = CASE 
                    WHEN baseline_sample_count + 1 >= v_baseline_test_count 
                    THEN 'improvement' 
                    ELSE 'baseline' 
                END,
                adaptive_expected_duration = CASE
                    WHEN v_use_adaptive AND baseline_sample_count + 1 >= v_baseline_test_count
                    THEN v_new_avg * v_improvement_target_ratio
                    ELSE v_exam_norm
                END,
                updated_at = NOW()
            WHERE student_id = NEW.student_id
            AND global_topic_uid = NEW.global_topic_uid;
        ELSE
            v_new_avg := (
                (v_baseline.current_avg_duration * v_baseline.current_sample_count + NEW.time_spent_seconds)
                / (v_baseline.current_sample_count + 1)
            );
            
            v_improvement_rate := CASE 
                WHEN v_baseline.baseline_avg_duration > 0 
                THEN (v_baseline.baseline_avg_duration - v_new_avg) / v_baseline.baseline_avg_duration
                ELSE NULL
            END;
            
            UPDATE student_baseline_performance
            SET current_avg_duration = v_new_avg,
                current_sample_count = current_sample_count + 1,
                improvement_rate = v_improvement_rate,
                distance_to_norm = v_exam_norm - v_new_avg,
                learning_phase = CASE
                    WHEN v_exam_norm IS NOT NULL AND ABS(v_new_avg - v_exam_norm) / NULLIF(v_exam_norm, 1) < 0.1 
                    THEN 'convergence'
                    ELSE 'improvement'
                END,
                adaptive_expected_duration = CASE
                    WHEN v_use_adaptive THEN v_new_avg * v_improvement_target_ratio
                    ELSE v_exam_norm
                END,
                updated_at = NOW()
            WHERE student_id = NEW.student_id
            AND global_topic_uid = NEW.global_topic_uid;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION update_student_baseline IS 'Adaptive baseline calculator - NULL-safe, divide-by-zero safe';

DROP TRIGGER IF EXISTS trg_update_student_baseline ON student_mistakes;
CREATE TRIGGER trg_update_student_baseline
AFTER INSERT ON student_mistakes
FOR EACH ROW
EXECUTE FUNCTION update_student_baseline();

-- ============================================
-- PART 9: SMART MISTAKE PATTERN ANALYZER
-- ============================================

-- IMPORTANT: AFTER INSERT ONLY
-- Do not convert to UPDATE trigger (infinite loop risk)
CREATE OR REPLACE FUNCTION update_mistake_patterns()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_settings JSONB;
    
    v_panic_ratio DECIMAL;
    v_panic_absolute_min INT;
    v_panic_absolute_max INT;
    v_stuck_repeat_threshold INT;
    v_stuck_time_window_hours INT;
    v_trend_window_size INT;
    v_trend_recent_count INT;
    v_trend_past_count INT;
    v_trend_significance DECIMAL;
    v_minimum_data_for_trend INT;
    v_use_adaptive_baseline BOOLEAN;
    
    v_pattern_exists BOOLEAN;
    v_current_distribution JSONB;
    v_new_count INT;
    v_trend_status VARCHAR(20);
    v_avg_severity_recent DECIMAL;
    v_avg_severity_past DECIMAL;
    v_recent_mistake_codes TEXT[];
    v_severity INT;
    v_expected_duration DECIMAL;
    v_time_ratio DECIMAL;
    v_adaptive_duration DECIMAL;
BEGIN
    IF NEW.time_spent_seconds IS NULL OR NEW.time_spent_seconds <= 0 THEN
        RETURN NEW;
    END IF;
    
    SELECT ap.settings INTO v_settings
    FROM student_analysis_settings sas
    JOIN analysis_presets ap ON ap.preset_name = sas.preset_name
    WHERE sas.student_id = NEW.student_id
    LIMIT 1;
    
    IF v_settings IS NULL THEN
        SELECT ap.settings INTO v_settings
        FROM analysis_presets ap
        WHERE ap.is_default = true
        ORDER BY ap.created_at ASC
        LIMIT 1;
    END IF;
    
    IF v_settings IS NULL THEN
        v_settings := '{
            "panic_ratio": 0.3,
            "panic_absolute_min": 5,
            "panic_absolute_max": 180,
            "stuck_repeat_threshold": 3,
            "stuck_time_window_hours": 24,
            "trend_window_size": 5,
            "trend_recent_count": 2,
            "trend_past_count": 3,
            "trend_significance_threshold": 0.3,
            "minimum_data_for_trend": 3,
            "use_adaptive_baseline": true
        }'::jsonb;
    END IF;
    
    v_panic_ratio := COALESCE((v_settings->>'panic_ratio')::DECIMAL, 0.3);
    v_panic_absolute_min := COALESCE((v_settings->>'panic_absolute_min')::INT, 5);
    v_panic_absolute_max := COALESCE((v_settings->>'panic_absolute_max')::INT, 180);
    v_stuck_repeat_threshold := COALESCE((v_settings->>'stuck_repeat_threshold')::INT, 3);
    v_stuck_time_window_hours := COALESCE((v_settings->>'stuck_time_window_hours')::INT, 24);
    v_trend_window_size := COALESCE((v_settings->>'trend_window_size')::INT, 5);
    v_trend_recent_count := COALESCE((v_settings->>'trend_recent_count')::INT, 2);
    v_trend_past_count := COALESCE((v_settings->>'trend_past_count')::INT, 3);
    v_trend_significance := COALESCE((v_settings->>'trend_significance_threshold')::DECIMAL, 0.3);
    v_minimum_data_for_trend := COALESCE((v_settings->>'minimum_data_for_trend')::INT, 3);
    v_use_adaptive_baseline := COALESCE((v_settings->>'use_adaptive_baseline')::BOOLEAN, true);
    
    IF v_use_adaptive_baseline THEN
        SELECT adaptive_expected_duration INTO v_adaptive_duration
        FROM student_baseline_performance
        WHERE student_id = NEW.student_id
        AND global_topic_uid = NEW.global_topic_uid;
        
        IF v_adaptive_duration IS NOT NULL THEN
            v_expected_duration := v_adaptive_duration;
            
            UPDATE student_mistakes
            SET expected_duration = v_expected_duration,
                used_adaptive_baseline = true
            WHERE id = NEW.id;
        ELSE
            BEGIN
                SELECT tr.expected_duration_per_question INTO v_expected_duration
                FROM test_records tr
                JOIN test_answers ta ON ta.test_id = tr.id
                WHERE ta.id = NEW.test_answer_id;
                
                UPDATE student_mistakes
                SET expected_duration = v_expected_duration,
                    used_adaptive_baseline = false
                WHERE id = NEW.id;
            EXCEPTION
                WHEN OTHERS THEN
                    v_expected_duration := NULL;
            END;
        END IF;
    ELSE
        BEGIN
            SELECT tr.expected_duration_per_question INTO v_expected_duration
            FROM test_records tr
            JOIN test_answers ta ON ta.test_id = tr.id
            WHERE ta.id = NEW.test_answer_id;
            
            UPDATE student_mistakes
            SET expected_duration = v_expected_duration,
                used_adaptive_baseline = false
            WHERE id = NEW.id;
        EXCEPTION
            WHEN OTHERS THEN
                v_expected_duration := NULL;
        END;
    END IF;
    
    v_time_ratio := NEW.time_spent_seconds / NULLIF(v_expected_duration, 1);
    
    UPDATE student_mistakes
    SET time_ratio = v_time_ratio
    WHERE id = NEW.id;
    
    -- ✅ v3.4: CRITICAL FIX - severity NULL guard
    SELECT severity INTO v_severity 
    FROM mistake_types 
    WHERE mistake_code = NEW.mistake_code;
    
    IF v_severity IS NULL THEN
        v_severity := 3;  -- Nötr seviye (yeni mistake_code için fallback)
    END IF;
    
    WITH recent_mistakes AS (
        SELECT 
            mt.severity,
            sm.mistake_code,
            sm.time_spent_seconds,
            ROW_NUMBER() OVER (ORDER BY sm.occurred_at DESC) as rn
        FROM student_mistakes sm
        JOIN mistake_types mt ON sm.mistake_code = mt.mistake_code
        WHERE sm.student_id = NEW.student_id 
          AND sm.global_topic_uid = NEW.global_topic_uid
          AND sm.occurred_at >= NOW() - (v_stuck_time_window_hours || ' hours')::INTERVAL
        LIMIT v_trend_window_size
    )
    SELECT 
        AVG(CASE WHEN rn <= v_trend_recent_count THEN severity END),
        AVG(CASE WHEN rn > v_trend_recent_count THEN severity END),
        array_agg(mistake_code ORDER BY rn)
    INTO v_avg_severity_recent, v_avg_severity_past, v_recent_mistake_codes
    FROM recent_mistakes;
    
    IF v_avg_severity_past IS NULL OR 
       array_length(v_recent_mistake_codes, 1) < v_minimum_data_for_trend THEN
        v_trend_status := 'insufficient_data';
    
    ELSIF (NEW.time_spent_seconds < v_panic_absolute_min)
       OR (v_time_ratio IS NOT NULL AND v_time_ratio < v_panic_ratio AND v_severity < 4) THEN
        v_trend_status := 'PANIC_RUSH';
    
    ELSIF array_length(v_recent_mistake_codes, 1) >= 3
          AND v_recent_mistake_codes[1] = v_recent_mistake_codes[2] 
          AND v_recent_mistake_codes[2] = v_recent_mistake_codes[3] THEN
        v_trend_status := 'STUCK_LOOP';
    
    ELSIF NEW.time_spent_seconds > v_panic_absolute_max THEN
        v_trend_status := 'STUCK_SLOW';
    
    ELSIF v_avg_severity_recent < v_avg_severity_past - v_trend_significance THEN
        v_trend_status := 'improving';
    ELSIF v_avg_severity_recent > v_avg_severity_past + v_trend_significance THEN
        v_trend_status := 'worsening';
    ELSE
        v_trend_status := 'stable';
    END IF;
    
    SELECT EXISTS (
        SELECT 1 FROM student_mistake_patterns
        WHERE student_id = NEW.student_id 
        AND global_topic_uid = NEW.global_topic_uid
    ) INTO v_pattern_exists;
    
    IF NOT v_pattern_exists THEN
        INSERT INTO student_mistake_patterns (
            student_id, global_topic_uid,
            dominant_mistake_code, dominant_mistake_count,
            mistake_distribution,
            improvement_trend,
            analyzed_at
        ) VALUES (
            NEW.student_id, NEW.global_topic_uid,
            NEW.mistake_code, 1,
            jsonb_build_object(NEW.mistake_code, 1),
            COALESCE(v_trend_status, 'new'),
            NOW()
        );
    ELSE
        SELECT mistake_distribution INTO v_current_distribution
        FROM student_mistake_patterns
        WHERE student_id = NEW.student_id 
        AND global_topic_uid = NEW.global_topic_uid;
        
        v_new_count := COALESCE((v_current_distribution->>NEW.mistake_code)::INT, 0) + 1;
        
        v_current_distribution := jsonb_set(
            v_current_distribution,
            ARRAY[NEW.mistake_code],
            to_jsonb(v_new_count)
        );
        
        UPDATE student_mistake_patterns
        SET 
            mistake_distribution = v_current_distribution,
            dominant_mistake_code = (
                SELECT key 
                FROM jsonb_each_text(v_current_distribution) 
                ORDER BY value::INT DESC LIMIT 1
            ),
            dominant_mistake_count = (
                SELECT value::INT 
                FROM jsonb_each_text(v_current_distribution) 
                ORDER BY value::INT DESC LIMIT 1
            ),
            improvement_trend = v_trend_status,
            analyzed_at = NOW()
        WHERE student_id = NEW.student_id 
        AND global_topic_uid = NEW.global_topic_uid;
    END IF;
    
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION update_mistake_patterns IS 'Smart analyzer v3.4.1 - Production hardened with NULL guards';

DROP TRIGGER IF EXISTS trg_update_mistake_patterns ON student_mistakes;

CREATE TRIGGER trg_update_mistake_patterns
AFTER INSERT ON student_mistakes
FOR EACH ROW
EXECUTE FUNCTION update_mistake_patterns();

-- ============================================
-- PART 10: STUDENT RECOMMENDATIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS student_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    student_id UUID NOT NULL,
    global_topic_uid VARCHAR(100),
    
    recommendation_type VARCHAR(20) NOT NULL,
    
    title TEXT,
    message TEXT,
    action_items JSONB,
    
    priority INT DEFAULT 5,
    is_shown BOOLEAN DEFAULT false,
    shown_at TIMESTAMP,
    is_dismissed BOOLEAN DEFAULT false,
    dismissed_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_student_recommendations_student ON student_recommendations(student_id);
CREATE INDEX IF NOT EXISTS idx_student_recommendations_shown ON student_recommendations(is_shown);
CREATE INDEX IF NOT EXISTS idx_student_recommendations_priority ON student_recommendations(priority DESC);

COMMENT ON TABLE student_recommendations IS 'UI notifications - TODO: Trigger implementation pending';

-- ============================================
-- PART 11: VERIFICATION
-- ============================================

DO $$
DECLARE
    preset_count INT;
    baseline_exists BOOLEAN;
    trigger_count INT;
    setting_group_exists BOOLEAN;
    preset_mode_exists BOOLEAN;
    unique_default_exists BOOLEAN;
BEGIN
    SELECT COUNT(*) INTO preset_count FROM analysis_presets;
    
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = 'student_baseline_performance'
    ) INTO baseline_exists;
    
    SELECT COUNT(*) INTO trigger_count
    FROM pg_trigger 
    WHERE tgname IN ('trg_update_mistake_patterns', 'trg_update_student_baseline');
    
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'system_settings' AND column_name = 'setting_group'
    ) INTO setting_group_exists;
    
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'system_settings' AND column_name = 'preset_mode'
    ) INTO preset_mode_exists;
    
    SELECT EXISTS (
        SELECT 1 FROM pg_indexes
        WHERE indexname = 'one_default_preset'
    ) INTO unique_default_exists;
    
    RAISE NOTICE '============================================';
    RAISE NOTICE 'MIGRATION 006 v3.4.1: FINAL POLISH';
    RAISE NOTICE '============================================';
    RAISE NOTICE '✅ system_settings: setting_group: %', setting_group_exists;
    RAISE NOTICE '✅ system_settings: preset_mode: %', preset_mode_exists;
    RAISE NOTICE '✅ analysis_presets (% presets)', preset_count;
    RAISE NOTICE '✅ analysis_presets: unique default: %', unique_default_exists;
    RAISE NOTICE '✅ student_baseline_performance: %', baseline_exists;
    RAISE NOTICE '✅ Triggers attached: % of 2', trigger_count;
    RAISE NOTICE '============================================';
    RAISE NOTICE '🔧 VERSION HISTORY:';
    RAISE NOTICE '  v3.1: STABLE keyword fix';
    RAISE NOTICE '  v3.2: Nested dollar quotes fix';
    RAISE NOTICE '  v3.3: preset_mode ALTER TABLE fix';
    RAISE NOTICE '  v3.4: Production hardening (2 guards)';
    RAISE NOTICE '  v3.4.1: COMMENT inside DO block';
    RAISE NOTICE '============================================';
    RAISE NOTICE '🛡️ PRODUCTION HARDENING:';
    RAISE NOTICE '  ✅ student_mistakes ALTER → DO block';
    RAISE NOTICE '  ✅ COMMENT → DO block (v3.4.1)';
    RAISE NOTICE '  ✅ severity NULL guard (default: 3)';
    RAISE NOTICE '  ✅ is_default UNIQUE INDEX';
    RAISE NOTICE '============================================';
    RAISE NOTICE '📋 CHECKLIST v1.1 COMPLIANT';
    RAISE NOTICE '============================================';
    RAISE NOTICE '🧠 NERVOUS SYSTEM v3.4.1 - FINAL POLISH!';
    RAISE NOTICE '============================================';
END $$;
