"""
List all tables in Supabase
"""
import sys
sys.path.insert(0, '/home/endstp/endstp-platform/backend')

from app.db.session import get_supabase_admin

supabase = get_supabase_admin()

print("=" * 60)
print("SUPABASE TABLOLARI")
print("=" * 60)

# Bazı önemli tabloları test et
tables_to_check = [
    "user_roles",
    "user_profiles", 
    "students",
    "users",
    "topic_test_results",
    "topics",
    "subjects",
    "test_records"
]

for table in tables_to_check:
    try:
        result = supabase.table(table).select("*").limit(1).execute()
        count = len(result.data)
        print(f"✅ {table:30} - {count} row(s)")
    except Exception as e:
        print(f"❌ {table:30} - {str(e)[:50]}")

print("=" * 60)
