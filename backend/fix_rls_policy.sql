-- student_topic_tests RLS Policy
ALTER TABLE student_topic_tests ENABLE ROW LEVEL SECURITY;

-- Service role her şeyi yapabilir
CREATE POLICY "Service role can do everything on student_topic_tests"
ON student_topic_tests
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Authenticated users kendi kayıtlarını görebilir
CREATE POLICY "Users can view their own tests"
ON student_topic_tests
FOR SELECT
TO authenticated
USING (auth.uid()::text = student_id);

-- Authenticated users kendi testlerini ekleyebilir
CREATE POLICY "Users can insert their own tests"
ON student_topic_tests
FOR INSERT
TO authenticated
WITH CHECK (auth.uid()::text = student_id);
