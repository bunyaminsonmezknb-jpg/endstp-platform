-- Mevcut tüm policy'leri göster
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename = 'student_topic_tests'
ORDER BY policyname;
