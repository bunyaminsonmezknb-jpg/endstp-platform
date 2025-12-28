-- ==========================================
-- 🏛️ END.STP TABLO OLUŞTURMA ANAYASASI
-- ==========================================
-- Her yeni tablo bu şablona göre oluşturulmalıdır!
-- Versiyon: 1.0
-- Tarih: 2025-11-25
-- ==========================================

-- 1️⃣ TABLOYU OLUŞTUR
CREATE TABLE public.TABLE_NAME (
    -- 🔑 Otomatik UUID primary key (HER ZAMAN OLMALI)
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- 👤 Student ilişkisi (student tabloları için)
    student_id uuid,  -- REFERENCES eklemeyiz (döngüsel bağımlılık önlemi)
    
    -- 📊 VERİ KOLONLARI
    -- Buraya kendi kolonlarını ekle
    -- Örnek:
    -- subject_id uuid,
    -- topic_id uuid,
    -- test_date timestamptz,
    -- correct_count int,
    -- net_score numeric(10,2),
    
    -- 💰 TİCARİ API KOLONLARI (Her tabloda ZORUNLU)
    client_id uuid,                              -- Hangi firma/müşteri
    api_version varchar(10) DEFAULT 'v1',        -- API versiyonu
    request_id uuid,                             -- Request tracking
    billing_period_id uuid,                      -- Faturalama dönemi
    api_call_cost numeric(10,2) DEFAULT 0.00,    -- İşlem maliyeti
    created_via varchar(50) DEFAULT 'internal',  -- Kaynak (web_form, api_client, vb.)
    ip_address inet,                             -- Security/audit
    user_agent text,                             -- Client bilgisi
    api_metadata jsonb,                          -- Esnek metadata
    
    -- 🔄 İŞLEM DURUMU (Pipeline için)
    is_processed boolean DEFAULT false,
    processing_status varchar(20) DEFAULT 'pending',
    processing_metadata jsonb,
    
    -- 📅 TIMESTAMP'LER (Her tabloda ZORUNLU)
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now(),
    deleted_at timestamptz                       -- Soft delete için
);

-- 2️⃣ RLS AKTİF ET (GÜVENLİK ZORUNLU)
ALTER TABLE public.TABLE_NAME ENABLE ROW LEVEL SECURITY;

-- 3️⃣ SERVICE ROLE POLİCY (Backend için - ZORUNLU)
CREATE POLICY "backend_full_access"
ON public.TABLE_NAME
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- 4️⃣ AUTHENTICATED USER POLİCY (Kullanıcı erişimi için)
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

-- 5️⃣ ANON USERS BLOCK (Güvenlik)
CREATE POLICY "anon_no_access"
ON public.TABLE_NAME
FOR ALL
TO anon
USING (false);

-- 6️⃣ GRANT YETKİLERİ (ÇOK ÇOK ÖNEMLİ! - ZORUNLU)
GRANT ALL ON TABLE public.TABLE_NAME TO service_role;
GRANT ALL ON TABLE public.TABLE_NAME TO postgres;
GRANT ALL ON TABLE public.TABLE_NAME TO authenticated;

-- 7️⃣ INDEX'LER (Performance optimizasyonu)
CREATE INDEX idx_TABLE_NAME_student_id 
    ON public.TABLE_NAME(student_id);
    
CREATE INDEX idx_TABLE_NAME_client_id 
    ON public.TABLE_NAME(client_id) 
    WHERE client_id IS NOT NULL;
    
CREATE INDEX idx_TABLE_NAME_is_processed 
    ON public.TABLE_NAME(is_processed) 
    WHERE is_processed = false;
    
CREATE INDEX idx_TABLE_NAME_deleted 
    ON public.TABLE_NAME(deleted_at) 
    WHERE deleted_at IS NULL;
    
CREATE INDEX idx_TABLE_NAME_created_at 
    ON public.TABLE_NAME(created_at DESC);

-- 8️⃣ CONSTRAINTS (Veri bütünlüğü)
ALTER TABLE public.TABLE_NAME
ADD CONSTRAINT check_processing_status 
CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed'));

ALTER TABLE public.TABLE_NAME
ADD CONSTRAINT check_created_via
CHECK (created_via IN ('internal', 'web_form', 'api_client', 'excel_import', 'mobile_app', 'coach_panel'));

-- 9️⃣ COMMENTS (Dökümantasyon - ÖNERİLİR)
COMMENT ON TABLE public.TABLE_NAME IS 'Tablo açıklaması buraya';
COMMENT ON COLUMN public.TABLE_NAME.client_id IS 'API müşteri/firma ID - faturalama için';
COMMENT ON COLUMN public.TABLE_NAME.api_version IS 'Kullanılan API versiyonu (v1, v2)';
COMMENT ON COLUMN public.TABLE_NAME.is_processed IS 'Pipeline tarafından işlendi mi?';
COMMENT ON COLUMN public.TABLE_NAME.created_via IS 'Veri kaynağı';

-- 🔟 KONTROL (İzinleri doğrula)
SELECT 
    grantee, 
    privilege_type,
    is_grantable
FROM information_schema.role_table_grants 
WHERE table_name = 'TABLE_NAME'
ORDER BY grantee, privilege_type;

-- ==========================================
-- ✅ ANAYASA BİTTİ
-- ==========================================
-- Kullanım:
-- 1. TABLE_NAME'i değiştir (örnek: exam_results)
-- 2. Veri kolonlarını ekle (-- 📊 VERİ KOLONLARI altına)
-- 3. Tüm SQL'i Supabase SQL Editor'da çalıştır
-- 4. Kontrol sorgusunu çalıştır
-- ==========================================
