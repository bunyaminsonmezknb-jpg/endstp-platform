"""
Inspect existing tables
"""
import sys
sys.path.insert(0, '/home/endstp/endstp-platform/backend')

from app.db.session import get_supabase_admin
import json

supabase = get_supabase_admin()

print("=" * 60)
print("TABLO İNCELEMESİ")
print("=" * 60)

# users tablosu
print("\n1. USERS TABLE:")
users = supabase.table("users").select("*").limit(3).execute()
for user in users.data:
    print(f"   {json.dumps(user, indent=2)}")

# topics tablosu
print("\n2. TOPICS TABLE:")
topics = supabase.table("topics").select("*").limit(3).execute()
for topic in topics.data:
    print(f"   {json.dumps(topic, indent=2)}")

# subjects tablosu
print("\n3. SUBJECTS TABLE:")
subjects = supabase.table("subjects").select("*").limit(3).execute()
for subject in subjects.data:
    print(f"   {json.dumps(subject, indent=2)}")

print("=" * 60)
