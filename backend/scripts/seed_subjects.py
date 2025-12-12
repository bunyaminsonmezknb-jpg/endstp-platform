from app.db.session import get_supabase_admin
import json

supabase = get_supabase_admin()

# TYT + AYT Dersleri
subjects_data = [
    # TYT Dersleri
    {"name_tr": "Türkçe", "name_en": "Turkish", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10", "11", "12"])},
    {"name_tr": "Matematik (Temel)", "name_en": "Mathematics (Basic)", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10", "11", "12"])},
    {"name_tr": "Geometri (Temel)", "name_en": "Geometry (Basic)", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10", "11", "12"])},
    {"name_tr": "Tarih", "name_en": "History", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10", "11", "12"])},
    {"name_tr": "Coğrafya", "name_en": "Geography", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10", "11", "12"])},
    {"name_tr": "Felsefe", "name_en": "Philosophy", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10", "11", "12"])},
    {"name_tr": "Din Kültürü", "name_en": "Religious Culture", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10", "11", "12"])},
    {"name_tr": "Fizik (Temel)", "name_en": "Physics (Basic)", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10"])},
    {"name_tr": "Kimya (Temel)", "name_en": "Chemistry (Basic)", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10"])},
    {"name_tr": "Biyoloji (Temel)", "name_en": "Biology (Basic)", "exam_type": "tyt", "grade_levels": json.dumps(["9", "10"])},
    
    # AYT Sayısal
    {"name_tr": "Matematik (İleri)", "name_en": "Mathematics (Advanced)", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
    {"name_tr": "Geometri (İleri)", "name_en": "Geometry (Advanced)", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
    {"name_tr": "Fizik", "name_en": "Physics", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
    {"name_tr": "Kimya", "name_en": "Chemistry", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
    {"name_tr": "Biyoloji", "name_en": "Biology", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
    
    # AYT Sözel
    {"name_tr": "Edebiyat", "name_en": "Literature", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
    {"name_tr": "Tarih (İleri)", "name_en": "History (Advanced)", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
    {"name_tr": "Coğrafya (İleri)", "name_en": "Geography (Advanced)", "exam_type": "ayt", "grade_levels": json.dumps(["11", "12"])},
]

print("🌱 Subjects seed başlıyor...")

for subject in subjects_data:
    try:
        result = supabase.table("subjects").insert(subject).execute()
        print(f"✅ {subject['name_tr']} eklendi")
    except Exception as e:
        print(f"❌ {subject['name_tr']} eklenemedi: {e}")

print(f"\n🎉 Toplam {len(subjects_data)} ders eklendi!")
