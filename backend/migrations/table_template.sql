-- ==========================================
-- STANDART END.STP TABLO ŞABLONU
-- Her yeni tablo için bu adımları takip et!
-- ==========================================

-- 1️⃣ TABLOYU OLUŞTUR
CREATE TABLE public.TABLE_NAME (
    -- Otomatik UUID primary key
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- İlişkiler
    student_id uuid REFERENCES public.students(id),
    
    -- Veri kolonları
    -- ... buraya kendi kolonlarını ekle
    
    -- TİCARİ API KOLONLARI (her tabloda olmalı)
    client_id uuid,
    api_version varchar(10) DEFAULT 'v1',
    request_id uuid,
    billing_period_id uuid,
    api_call_cost numeric(10,2) DEFAULT 0.00,
    created_via varchar(50) DEFAULT 'internal',
    ip_address inet,
    user_agent text,
    api_metadata jsonb,
    
    -- İşlem durumu
    is_processed boolean DEFAULT false,
    processing_status varchar(20) DEFAULT 'pending',
    
    -- Timestamp'ler
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now(),
    deleted_at timestamptz
);

-- 2️⃣ RLS AKTİF ET
ALTER TABLE public.TABLE_NAME ENABLE ROW LEVEL SECURITY;

-- 3️⃣ SERVICE ROLE POLİCY (Backend için)
CREATE POLICY "backend_full_access"
ON public.TABLE_NAME
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- 4️⃣ AUTHENTICATED USER POLİCY (Opsiyonel)
CREATE POLICY "users_read_own"
ON public.TABLE_NAME
FOR SELECT
TO authenticated
USING (student_id::text = auth.uid()::text);

CREATE POLICY "users_insert_own"
ON public.TABLE_NAME
FOR INSERT
TO authenticated
WITH CHECK (student_id::text = auth.uid()::text);

-- 5️⃣ ANON USERS BLOCK
CREATE POLICY "anon_no_access"
ON public.TABLE_NAME
FOR ALL
TO anon
USING (false);

-- 6️⃣ GRANT YETKİLERİ (ÇOK ÖNEMLİ!)
GRANT ALL ON TABLE public.TABLE_NAME TO service_role;
GRANT ALL ON TABLE public.TABLE_NAME TO postgres;
GRANT ALL ON TABLE public.TABLE_NAME TO authenticated;

-- 7️⃣ INDEX'LER (Performance)
CREATE INDEX idx_TABLE_NAME_student_id ON public.TABLE_NAME(student_id);
CREATE INDEX idx_TABLE_NAME_client_id ON public.TABLE_NAME(client_id) WHERE client_id IS NOT NULL;
CREATE INDEX idx_TABLE_NAME_is_processed ON public.TABLE_NAME(is_processed) WHERE is_processed = false;
CREATE INDEX idx_TABLE_NAME_deleted ON public.TABLE_NAME(deleted_at) WHERE deleted_at IS NULL;

-- 8️⃣ CONSTRAINTS
ALTER TABLE public.TABLE_NAME
ADD CONSTRAINT check_processing_status 
CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed'));

-- 9️⃣ COMMENTS (Dökümantasyon)
COMMENT ON TABLE public.TABLE_NAME IS 'Açıklama buraya';
COMMENT ON COLUMN public.TABLE_NAME.client_id IS 'API müşteri firma ID';
COMMENT ON COLUMN public.TABLE_NAME.is_processed IS 'Pipeline tarafından işlendi mi?';

-- 🔟 KONTROL
SELECT grantee, privilege_type 
FROM information_schema.role_table_grants 
WHERE table_name = 'TABLE_NAME';
