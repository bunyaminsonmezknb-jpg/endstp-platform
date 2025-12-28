-- ================================================
-- TİCARİ API MİMARİSİ - ORTAK KOLONLAR
-- Tüm API-kullanılan tablolara eklenecek
-- ================================================

-- FONKSIYON: Ortak kolonları ekle
CREATE OR REPLACE FUNCTION add_commercial_api_columns(table_name text)
RETURNS void AS $$
BEGIN
  EXECUTE format('
    ALTER TABLE %I
    ADD COLUMN IF NOT EXISTS client_id uuid,
    ADD COLUMN IF NOT EXISTS api_version varchar(10) DEFAULT ''v1'',
    ADD COLUMN IF NOT EXISTS request_id uuid,
    ADD COLUMN IF NOT EXISTS billing_period_id uuid,
    ADD COLUMN IF NOT EXISTS api_call_cost numeric(10,2) DEFAULT 0.00,
    ADD COLUMN IF NOT EXISTS created_via varchar(50) DEFAULT ''internal'',
    ADD COLUMN IF NOT EXISTS ip_address inet,
    ADD COLUMN IF NOT EXISTS user_agent text,
    ADD COLUMN IF NOT EXISTS api_metadata jsonb;
  ', table_name);
  
  -- Index'ler
  EXECUTE format('
    CREATE INDEX IF NOT EXISTS idx_%I_client_id ON %I(client_id) WHERE client_id IS NOT NULL;
  ', table_name, table_name);
  
  EXECUTE format('
    CREATE INDEX IF NOT EXISTS idx_%I_billing_period ON %I(billing_period_id) WHERE billing_period_id IS NOT NULL;
  ', table_name, table_name);
  
  RAISE NOTICE 'Commercial API columns added to: %', table_name;
END;
$$ LANGUAGE plpgsql;

-- GRUP 1: Test & Performance tablolarına ekle
SELECT add_commercial_api_columns('student_topic_tests');
SELECT add_commercial_api_columns('test_answers');
SELECT add_commercial_api_columns('student_topic_performance');
SELECT add_commercial_api_columns('forgetting_curve_tracking');

-- GRUP 2: Analytics tablolarına ekle
SELECT add_commercial_api_columns('student_learning_stats');
SELECT add_commercial_api_columns('topic_recommendations');

-- Constraint'ler
ALTER TABLE student_topic_tests
ADD CONSTRAINT check_created_via_student_topic_tests
CHECK (created_via IN ('internal', 'web_form', 'api_client', 'excel_import', 'mobile_app', 'coach_panel'));

-- Comments (dökümantasyon)
COMMENT ON COLUMN student_topic_tests.client_id IS 'API müşteri firma ID - faturalama için';
COMMENT ON COLUMN student_topic_tests.api_version IS 'Kullanılan API versiyonu (v1, v2)';
COMMENT ON COLUMN student_topic_tests.request_id IS 'Unique request tracking - hata ayıklama için';
COMMENT ON COLUMN student_topic_tests.billing_period_id IS 'Fatura dönemi ID';
COMMENT ON COLUMN student_topic_tests.api_call_cost IS 'Bu işlemin maliyeti (TL)';
COMMENT ON COLUMN student_topic_tests.created_via IS 'Veri kaynağı';

-- Fonksiyonu temizle (opsiyonel)
-- DROP FUNCTION IF EXISTS add_commercial_api_columns(text);

