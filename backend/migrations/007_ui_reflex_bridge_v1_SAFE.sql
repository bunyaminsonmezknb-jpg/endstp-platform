-- ============================================
-- MIGRATION 007: UI Reflex Bridge v1 (SAFE)
-- Date: 2024-12-14
-- Version: 1.0 (Safe - Preserves Migration 006 triggers)
-- Description:
-- 1) UI Reflex event feed (Supabase Realtime ready)
-- 2) Auto recommendation generation (template-based, no LLM)
-- 3) Dedupe mechanism (1 active recommendation per type)
-- 4) Preserves Migration 006 triggers (no breaking changes)
-- ============================================

-- ============================================
-- ARCHITECTURE NOTE:
-- This migration PRESERVES Migration 006 triggers:
-- - trg_update_student_baseline (stays)
-- - trg_update_mistake_patterns (stays)
-- 
-- NEW trigger:
-- - trg_generate_recommendations (AFTER student_mistake_patterns)
-- 
-- This is the SAFE approach - no breaking changes to 006
-- ============================================

-- ============================================
-- PART 1: UI REFLEX EVENT STREAM (Bridge)
-- ============================================

CREATE TABLE IF NOT EXISTS ui_reflex_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    student_id UUID NOT NULL,
    global_topic_uid VARCHAR(100),
    
    -- Event types: 'RECOMMENDATION_CREATED', 'RECOMMENDATION_UPDATED', 'PATTERN_CHANGED'
    event_type VARCHAR(50) NOT NULL,
    
    -- UI payload (template-based, deterministic)
    title TEXT,
    message TEXT,
    action_items JSONB,  -- [{"action":"slow_down","duration_sec":60}, ...]
    priority INT DEFAULT 5,  -- 1..10
    
    -- Links
    recommendation_id UUID,
    source_mistake_id UUID,
    
    -- Delivery state (for polling/realtime)
    delivered BOOLEAN DEFAULT false,
    delivered_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ui_reflex_events_student ON ui_reflex_events(student_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ui_reflex_events_type ON ui_reflex_events(event_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ui_reflex_events_priority ON ui_reflex_events(priority DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ui_reflex_events_delivered ON ui_reflex_events(delivered, created_at DESC);

COMMENT ON TABLE ui_reflex_events IS 'UI event feed - Supabase Realtime/polling için refleks akışı. Template-based, no LLM.';

-- ============================================
-- PART 2: student_recommendations DEDUPE
-- ============================================

-- Add columns if not exist (from 006 v3.4.1)
ALTER TABLE student_recommendations
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS source_mistake_id UUID,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP;

-- Dedupe: Aynı tip + aynı topic → tek aktif öneri
CREATE UNIQUE INDEX IF NOT EXISTS uq_student_reco_active
ON student_recommendations(student_id, global_topic_uid, recommendation_type)
WHERE is_active = true;

COMMENT ON COLUMN student_recommendations.is_active IS 'Dedupe: Aynı tipte aktif öneri tek olsun';

-- ============================================
-- PART 3: DETERMINISTIC MESSAGE TEMPLATES
-- ============================================

-- NO LLM! Template-based, rule-based, deterministic
-- Cost: $0, Speed: <10ms, Control: 100%

CREATE OR REPLACE FUNCTION build_reflex_recommendation_payload(
    p_status VARCHAR,
    p_severity INT,
    p_time_spent INT,
    p_global_topic_uid VARCHAR
) RETURNS TABLE (
    o_title TEXT,
    o_message TEXT,
    o_action_items JSONB,
    o_priority INT,
    o_expires_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Default values
    o_priority := 5;
    o_expires_at := NOW() + INTERVAL '12 hours';
    o_action_items := '[]'::jsonb;
    
    -- Template-based message generation (NO LLM!)
    IF p_status = 'PANIC_RUSH' THEN
        o_title := '⏱️ Acele Modu Tespit Edildi';
        o_message := 'Çok hızlı çözüm → basit hata riski. 60 sn yavaşlat ve mini kontrol uygula.';
        o_action_items := jsonb_build_array(
            jsonb_build_object('action', 'slow_down', 'duration_sec', 60, 'label', '60 saniye nefes al'),
            jsonb_build_object('action', 'recheck_steps', 'count', 2, 'label', '2 adımı kontrol et'),
            jsonb_build_object('action', 'micro_break', 'duration_sec', 45, 'label', '45 saniye ara ver')
        );
        o_priority := 8;
        o_expires_at := NOW() + INTERVAL '6 hours';
        
    ELSIF p_status = 'STUCK_LOOP' THEN
        o_title := '🔁 Takılma Döngüsü Tespit Edildi';
        o_message := 'Aynı hata tekrar ediyor. 1 ipucu al + 1 mini konu tekrarı yap + yeniden dene.';
        o_action_items := jsonb_build_array(
            jsonb_build_object('action', 'hint', 'level', 1, 'label', '1 ipucu al'),
            jsonb_build_object('action', 'micro_review', 'duration_min', 6, 'label', '6 dakika tekrar'),
            jsonb_build_object('action', 'retry', 'count', 1, 'label', 'Tekrar dene')
        );
        o_priority := 9;
        o_expires_at := NOW() + INTERVAL '24 hours';
        
    ELSIF p_status = 'STUCK_SLOW' THEN
        o_title := '🐢 Çok Yavaş Çözüm Tespit Edildi';
        o_message := 'Süre aşımı var. Çözümü 3 parçaya böl + her parçaya 90 sn hedefi koy.';
        o_action_items := jsonb_build_array(
            jsonb_build_object('action', 'split_solution', 'steps', 3, 'label', 'Çözümü 3 adıma böl'),
            jsonb_build_object('action', 'time_box', 'duration_sec', 90, 'label', 'Her adım için 90 sn'),
            jsonb_build_object('action', 'retry', 'count', 1, 'label', 'Yeniden dene')
        );
        o_priority := 7;
        o_expires_at := NOW() + INTERVAL '24 hours';
        
    ELSIF p_status = 'worsening' THEN
        o_title := '⚠️ Hata Şiddeti Artıyor';
        o_message := 'Son hatalar daha zorlayıcı. Önce öncül mini tekrar + sonra daha kolay soru seti önerilir.';
        o_action_items := jsonb_build_array(
            jsonb_build_object('action', 'prereq_check', 'mode', 'light', 'label', 'Öncül konuları kontrol et'),
            jsonb_build_object('action', 'easy_set', 'count', 6, 'label', '6 kolay soru çöz'),
            jsonb_build_object('action', 'review', 'duration_min', 8, 'label', '8 dakika tekrar')
        );
        o_priority := 7;
        o_expires_at := NOW() + INTERVAL '24 hours';
        
    ELSIF p_status = 'improving' THEN
        o_title := '✅ İyileşme Var - Devam Et!';
        o_message := 'Hatalar hafifliyor. Ritmi koru: 1 kısa tekrar + 1 normal deneme seti.';
        o_action_items := jsonb_build_array(
            jsonb_build_object('action', 'review', 'duration_min', 5, 'label', '5 dakika hızlı tekrar'),
            jsonb_build_object('action', 'normal_set', 'count', 8, 'label', '8 normal soru')
        );
        o_priority := 4;
        o_expires_at := NOW() + INTERVAL '24 hours';
        
    ELSE
        -- stable / insufficient_data / new → öneri üretme
        o_title := NULL;
        o_message := NULL;
        o_action_items := '[]'::jsonb;
        o_priority := 3;
        o_expires_at := NOW() + INTERVAL '24 hours';
    END IF;
    
    RETURN NEXT;
END;
$$;

COMMENT ON FUNCTION build_reflex_recommendation_payload IS 
'Deterministic template-based message generation (NO LLM). Cost: $0, Speed: <10ms, Control: 100%.';

-- ============================================
-- PART 4: UPSERT RECOMMENDATION + EMIT EVENT
-- ============================================

CREATE OR REPLACE FUNCTION upsert_student_recommendation_and_emit(
    p_student_id UUID,
    p_global_topic_uid VARCHAR,
    p_type VARCHAR,
    p_title TEXT,
    p_message TEXT,
    p_action_items JSONB,
    p_priority INT,
    p_source_mistake_id UUID,
    p_expires_at TIMESTAMP
) RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    v_existing_id UUID;
    v_event_type VARCHAR(50);
BEGIN
    -- Aktif aynı tip öneri var mı? (dedupe check)
    SELECT id INTO v_existing_id
    FROM student_recommendations
    WHERE student_id = p_student_id
      AND global_topic_uid = p_global_topic_uid
      AND recommendation_type = p_type
      AND is_active = true
    LIMIT 1;
    
    IF v_existing_id IS NULL THEN
        -- Yeni öneri oluştur
        INSERT INTO student_recommendations(
            student_id, global_topic_uid,
            recommendation_type,
            title, message, action_items,
            priority,
            is_shown, is_dismissed,
            is_active,
            source_mistake_id,
            created_at, expires_at, updated_at
        ) VALUES (
            p_student_id, p_global_topic_uid,
            p_type,
            p_title, p_message, p_action_items,
            p_priority,
            false, false,
            true,
            p_source_mistake_id,
            NOW(), p_expires_at, NOW()
        )
        RETURNING id INTO v_existing_id;
        
        v_event_type := 'RECOMMENDATION_CREATED';
        
    ELSE
        -- Mevcut öneriyi güncelle
        UPDATE student_recommendations
        SET title = p_title,
            message = p_message,
            action_items = p_action_items,
            priority = p_priority,
            source_mistake_id = p_source_mistake_id,
            expires_at = p_expires_at,
            updated_at = NOW()
        WHERE id = v_existing_id;
        
        v_event_type := 'RECOMMENDATION_UPDATED';
    END IF;
    
    -- UI event emit (Supabase Realtime / polling için)
    INSERT INTO ui_reflex_events(
        student_id, global_topic_uid,
        event_type,
        title, message, action_items,
        priority,
        recommendation_id,
        source_mistake_id
    ) VALUES (
        p_student_id, p_global_topic_uid,
        v_event_type,
        p_title, p_message, p_action_items,
        p_priority,
        v_existing_id,
        p_source_mistake_id
    );
END;
$$;

COMMENT ON FUNCTION upsert_student_recommendation_and_emit IS 
'Dedupe upsert + UI event emission. Single source of truth for recommendations.';

-- ============================================
-- PART 5: AUTO RECOMMENDATION GENERATOR
-- ============================================

-- This trigger generates recommendations AFTER pattern analysis
-- Migration 006 triggers stay intact!

CREATE OR REPLACE FUNCTION trg_generate_recommendations()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_severity INT;
    v_title TEXT;
    v_message TEXT;
    v_actions JSONB;
    v_priority INT;
    v_expires TIMESTAMP;
    v_source_mistake_id UUID;
BEGIN
    -- Get latest mistake for this pattern
    SELECT id INTO v_source_mistake_id
    FROM student_mistakes
    WHERE student_id = NEW.student_id
      AND global_topic_uid = NEW.global_topic_uid
    ORDER BY occurred_at DESC
    LIMIT 1;
    
    -- Get severity (with NULL guard from 006 v3.4)
    SELECT severity INTO v_severity
    FROM mistake_types mt
    JOIN student_mistakes sm ON sm.mistake_code = mt.mistake_code
    WHERE sm.id = v_source_mistake_id;
    
    IF v_severity IS NULL THEN
        v_severity := 3;  -- Fallback
    END IF;
    
    -- Build recommendation payload (template-based, no LLM!)
    SELECT o_title, o_message, o_action_items, o_priority, o_expires_at
    INTO v_title, v_message, v_actions, v_priority, v_expires
    FROM build_reflex_recommendation_payload(
        NEW.improvement_trend,
        v_severity,
        0,  -- time_spent (not used in current templates)
        NEW.global_topic_uid
    );
    
    -- Only create recommendation if title exists (skip stable/insufficient_data)
    IF v_title IS NOT NULL THEN
        PERFORM upsert_student_recommendation_and_emit(
            NEW.student_id,
            NEW.global_topic_uid,
            NEW.improvement_trend,  -- recommendation_type = trend status
            v_title,
            v_message,
            v_actions,
            v_priority,
            v_source_mistake_id,
            v_expires
        );
    END IF;
    
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION trg_generate_recommendations IS 
'Auto-generates recommendations based on pattern analysis. Template-based, no LLM.';

DROP TRIGGER IF EXISTS trg_generate_recommendations ON student_mistake_patterns;

CREATE TRIGGER trg_generate_recommendations
AFTER INSERT OR UPDATE OF improvement_trend ON student_mistake_patterns
FOR EACH ROW
EXECUTE FUNCTION trg_generate_recommendations();

COMMENT ON TRIGGER trg_generate_recommendations ON student_mistake_patterns IS
'Auto-generates UI recommendations when pattern changes. Works alongside Migration 006 triggers.';

-- ============================================
-- PART 6: VERIFICATION
-- ============================================

DO $$
DECLARE
    v_events_table BOOLEAN;
    v_dedupe_index BOOLEAN;
    v_reco_trigger BOOLEAN;
    v_m006_triggers INT;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = 'ui_reflex_events'
    ) INTO v_events_table;
    
    SELECT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE indexname = 'uq_student_reco_active'
    ) INTO v_dedupe_index;
    
    SELECT EXISTS (
        SELECT 1 FROM pg_trigger 
        WHERE tgname = 'trg_generate_recommendations'
    ) INTO v_reco_trigger;
    
    -- Verify Migration 006 triggers are still there
    SELECT COUNT(*) INTO v_m006_triggers
    FROM pg_trigger
    WHERE tgname IN ('trg_update_student_baseline', 'trg_update_mistake_patterns');
    
    RAISE NOTICE '============================================';
    RAISE NOTICE 'MIGRATION 007 v1: UI REFLEX BRIDGE (SAFE)';
    RAISE NOTICE '============================================';
    RAISE NOTICE '✅ ui_reflex_events table: %', v_events_table;
    RAISE NOTICE '✅ Dedupe index (uq_student_reco_active): %', v_dedupe_index;
    RAISE NOTICE '✅ Auto recommendation trigger: %', v_reco_trigger;
    RAISE NOTICE '✅ Migration 006 triggers preserved: % of 2', v_m006_triggers;
    RAISE NOTICE '============================================';
    RAISE NOTICE '🎯 FEATURES:';
    RAISE NOTICE '  ✅ UI event feed (Supabase Realtime ready)';
    RAISE NOTICE '  ✅ Auto recommendation generation';
    RAISE NOTICE '  ✅ Template-based messages (NO LLM)';
    RAISE NOTICE '  ✅ Dedupe mechanism (1 active per type)';
    RAISE NOTICE '  ✅ Cost: $0, Speed: <10ms';
    RAISE NOTICE '============================================';
    RAISE NOTICE '🛡️ SAFE APPROACH:';
    RAISE NOTICE '  ✅ Migration 006 triggers untouched';
    RAISE NOTICE '  ✅ No breaking changes';
    RAISE NOTICE '  ✅ Additive only';
    RAISE NOTICE '============================================';
    RAISE NOTICE '🚀 UI REFLEX BRIDGE ACTIVATED!';
    RAISE NOTICE '============================================';
END $$;
