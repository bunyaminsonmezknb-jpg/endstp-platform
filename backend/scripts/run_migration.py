from app.db.session import get_supabase_admin
import os

supabase = get_supabase_admin()

# Migration SQL dosyasını oku
migration_file = "migrations/001_multi_curriculum.sql"

print(f"📖 {migration_file} okunuyor...")

with open(migration_file, 'r', encoding='utf-8') as f:
    sql = f.read()

print("🚀 Migration çalıştırılıyor...")

try:
    # Supabase SQL çalıştırma
    result = supabase.rpc('exec_sql', {'query': sql}).execute()
    print("✅ Migration başarıyla tamamlandı!")
except Exception as e:
    print(f"❌ Hata: {e}")
    print("\n⚠️  Manuel olarak Supabase Dashboard'dan çalıştırabilirsiniz:")
    print("   1. https://supabase.com/dashboard")
    print("   2. SQL Editor'e git")
    print(f"   3. {migration_file} içeriğini kopyala-yapıştır")
    print("   4. Run düğmesine tıkla")

