-- Feature flags table
CREATE TABLE IF NOT EXISTS feature_flags (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  flag_key TEXT UNIQUE NOT NULL,
  is_enabled BOOLEAN DEFAULT true,
  description TEXT,
  phase TEXT DEFAULT 'mvp',
  health_score INTEGER DEFAULT 100,
  error_count INTEGER DEFAULT 0,
  last_error_at TIMESTAMPTZ,
  disabled_reason TEXT,
  disabled_by TEXT,
  disabled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Navigation & Diagnostics
  component_path TEXT,
  backend_endpoint TEXT,
  related_files TEXT[],
  fix_guide TEXT,
  docs_link TEXT,
  
  -- Error Severity & Impact
  error_severity TEXT DEFAULT 'low',
  user_impact_level TEXT DEFAULT 'none',
  last_deploy_at TIMESTAMPTZ,
  affected_users_count INTEGER DEFAULT 0,
  
  -- Auto-Recovery
  auto_recovery_enabled BOOLEAN DEFAULT false,
  recovery_attempts INTEGER DEFAULT 0,
  last_recovery_attempt_at TIMESTAMPTZ,
  
  -- Performance Metrics
  avg_response_time_ms INTEGER,
  p95_response_time_ms INTEGER,
  rows_processed INTEGER,
  cache_hit_rate DECIMAL(5,2),
  error_rate_percent DECIMAL(5,2) DEFAULT 0,
  last_success_at TIMESTAMPTZ,
  
  -- Health Breakdown
  latency_score INTEGER DEFAULT 100,
  error_score INTEGER DEFAULT 100,
  freshness_score INTEGER DEFAULT 100,
  data_volume_score INTEGER DEFAULT 100,
  
  -- Error Details
  last_error_message TEXT,
  last_error_trace TEXT,
  last_error_function TEXT,
  error_timeline JSONB DEFAULT '[]'::jsonb,
  
  -- Dependencies
  depends_on TEXT[],
  blocks TEXT[],
  deploy_timestamp TIMESTAMPTZ
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_feature_flags_key ON feature_flags(flag_key);
CREATE INDEX IF NOT EXISTS idx_feature_flags_enabled ON feature_flags(is_enabled);
CREATE INDEX IF NOT EXISTS idx_error_severity ON feature_flags(error_severity);
CREATE INDEX IF NOT EXISTS idx_user_impact ON feature_flags(user_impact_level);
CREATE INDEX IF NOT EXISTS idx_health_score ON feature_flags(health_score);

-- Disable RLS
ALTER TABLE feature_flags DISABLE ROW LEVEL SECURITY;

-- Permissions
GRANT ALL ON feature_flags TO authenticated;
GRANT ALL ON feature_flags TO service_role;
GRANT ALL ON feature_flags TO anon;
