-- student_topic_tests RLS Policy (Type cast düzeltmesi)

-- Önce mevcut policy'leri sil
DROP POLICY IF EXISTS "Service role can do everything on student_topic_tests" ON student_topic_tests;
DROP POLICY IF EXISTS "Users can view their own tests" ON student_topic_tests;
DROP POLICY IF EXISTS "Users can insert their own tests" ON student_topic_tests;

-- RLS aktif et
ALTER TABLE student_topic_tests ENABLE ROW LEVEL SECURITY;

-- Service role her şeyi yapabilir (Backend için)
CREATE POLICY "Service role full access"
ON student_topic_tests
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Authenticated users kendi kayıtlarını görebilir (UUID cast)
CREATE POLICY "Users view own tests"
ON student_topic_tests
FOR SELECT
TO authenticated
USING (auth.uid() = student_id::uuid);

-- Authenticated users kendi testlerini ekleyebilir (UUID cast)
CREATE POLICY "Users insert own tests"
ON student_topic_tests
FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = student_id::uuid);

-- Anon users hiçbir şey yapamaz (güvenlik)
CREATE POLICY "Anon users no access"
ON student_topic_tests
FOR ALL
TO anon
USING (false);

