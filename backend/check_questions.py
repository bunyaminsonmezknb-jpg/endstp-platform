import os
from supabase import create_client

url = "https://runbsfxytxmtzweuaufr.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1bmJzZnh5dHhtdHp3ZXVhdWZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzODc0NDgsImV4cCI6MjA3ODk2MzQ0OH0.6ja6PZTRqUMBHL9A3HoRgFUjYFiaysyXAVVeJg_b6ow"

supabase = create_client(url, key)

# Check tables
tables_to_check = [
    "questions",
    "question_sub_components", 
    "topic_exam_history",
    "user_goals",
    "exam_types",
    "osym_topics"
]

print("=" * 60)
print("📊 SUPABASE TABLE CHECK")
print("=" * 60)

for table in tables_to_check:
    try:
        result = supabase.table(table).select("*", count="exact").limit(0).execute()
        count = result.count if hasattr(result, 'count') else "?"
        print(f"✅ {table:30} → {count} rows")
    except Exception as e:
        print(f"❌ {table:30} → NOT FOUND")

print("=" * 60)
