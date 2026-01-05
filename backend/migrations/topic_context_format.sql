-- =============================================
-- TOPIC CONTEXTS TABLE
-- Topics tablosuna bağlı, Context Layer metadata
-- =============================================

CREATE TABLE IF NOT EXISTS topic_contexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    
    -- Metadata (JSONB)
    metadata JSONB NOT NULL DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(topic_id)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_topic_contexts_topic_id ON topic_contexts(topic_id);

-- Index for JSONB queries (format_version)
CREATE INDEX IF NOT EXISTS idx_topic_contexts_format_version ON topic_contexts USING gin ((metadata->'format_version'));

-- Index for JSONB queries (archetype)
CREATE INDEX IF NOT EXISTS idx_topic_contexts_archetype ON topic_contexts USING gin ((metadata->'archetype'));

-- Comments
COMMENT ON TABLE topic_contexts IS 'Context Layer metadata for topics (Format v1.0)';
COMMENT ON COLUMN topic_contexts.metadata IS 'JSONB containing: learning_objectives, prerequisites, exam_context, cognitive_level, splitting_guidance, tags, archetype, format_version';

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_topic_contexts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_topic_contexts_updated_at
    BEFORE UPDATE ON topic_contexts
    FOR EACH ROW
    EXECUTE FUNCTION update_topic_contexts_updated_at();