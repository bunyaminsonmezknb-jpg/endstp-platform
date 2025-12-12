from app.db.session import get_supabase_admin

supabase = get_supabase_admin()

print("🌍 Multi-Curriculum Seed başlıyor...\n")

# ====================
# 1. CURRICULUM SYSTEMS
# ====================
print("📚 Curriculum Systems ekleniyor...")

curriculum_systems = [
    {"code": "tr_osym", "name": "Türkiye ÖSYM (YKS)", "country_code": "TR", "language": "tr"},
    {"code": "us_sat", "name": "United States (SAT/ACT)", "country_code": "US", "language": "en"},
    {"code": "in_jee", "name": "India (JEE)", "country_code": "IN", "language": "en"},
    {"code": "de_abitur", "name": "Germany (Abitur)", "country_code": "DE", "language": "de"},
    {"code": "kr_csat", "name": "South Korea (CSAT)", "country_code": "KR", "language": "ko"},
]

curriculum_ids = {}
for cs in curriculum_systems:
    try:
        result = supabase.table("curriculum_systems").insert(cs).execute()
        curriculum_ids[cs['code']] = result.data[0]['id']
        print(f"  ✅ {cs['name']}")
    except Exception as e:
        print(f"  ⚠️  {cs['name']} (zaten var olabilir)")
        # Varsa ID'yi çek
        result = supabase.table("curriculum_systems").select("id").eq("code", cs['code']).execute()
        if result.data:
            curriculum_ids[cs['code']] = result.data[0]['id']

print()

# ====================
# 2. EXAM TYPES
# ====================
print("📝 Exam Types ekleniyor...")

exam_types_data = [
    # Türkiye
    {"curriculum_code": "tr_osym", "code": "tyt", "name": "Temel Yeterlilik Testi (TYT)", "display_order": 1},
    {"curriculum_code": "tr_osym", "code": "ayt", "name": "Alan Yeterlilik Testi (AYT)", "display_order": 2},
    
    # USA
    {"curriculum_code": "us_sat", "code": "sat_math", "name": "SAT Mathematics", "display_order": 1},
    {"curriculum_code": "us_sat", "code": "sat_reading", "name": "SAT Reading & Writing", "display_order": 2},
    {"curriculum_code": "us_sat", "code": "act", "name": "ACT", "display_order": 3},
    
    # India
    {"curriculum_code": "in_jee", "code": "jee_main", "name": "JEE Main", "display_order": 1},
    {"curriculum_code": "in_jee", "code": "jee_advanced", "name": "JEE Advanced", "display_order": 2},
    
    # Germany
    {"curriculum_code": "de_abitur", "code": "abitur", "name": "Abitur", "display_order": 1},
    
    # Korea
    {"curriculum_code": "kr_csat", "code": "csat", "name": "College Scholastic Ability Test", "display_order": 1},
]

exam_type_ids = {}
for et in exam_types_data:
    data = {
        "curriculum_system_id": curriculum_ids[et['curriculum_code']],
        "code": et['code'],
        "name": et['name'],
        "display_order": et['display_order']
    }
    try:
        result = supabase.table("curriculum_exam_types").insert(data).execute()
        exam_type_ids[et['code']] = result.data[0]['id']
        print(f"  ✅ {et['name']}")
    except Exception as e:
        print(f"  ⚠️  {et['name']} (zaten var olabilir)")

print()

# ====================
# 3. GRADE LEVELS
# ====================
print("🎓 Grade Levels ekleniyor...")

grade_levels_data = [
    # Türkiye
    {"curriculum_code": "tr_osym", "code": "9", "name": "9. Sınıf", "display_order": 1},
    {"curriculum_code": "tr_osym", "code": "10", "name": "10. Sınıf", "display_order": 2},
    {"curriculum_code": "tr_osym", "code": "11", "name": "11. Sınıf", "display_order": 3},
    {"curriculum_code": "tr_osym", "code": "12", "name": "12. Sınıf", "display_order": 4},
    {"curriculum_code": "tr_osym", "code": "graduate", "name": "Mezun", "display_order": 5},
    
    # USA
    {"curriculum_code": "us_sat", "code": "9", "name": "Grade 9 (Freshman)", "display_order": 1},
    {"curriculum_code": "us_sat", "code": "10", "name": "Grade 10 (Sophomore)", "display_order": 2},
    {"curriculum_code": "us_sat", "code": "11", "name": "Grade 11 (Junior)", "display_order": 3},
    {"curriculum_code": "us_sat", "code": "12", "name": "Grade 12 (Senior)", "display_order": 4},
    
    # India
    {"curriculum_code": "in_jee", "code": "11", "name": "Class 11", "display_order": 1},
    {"curriculum_code": "in_jee", "code": "12", "name": "Class 12", "display_order": 2},
    {"curriculum_code": "in_jee", "code": "dropper", "name": "Dropper (Gap Year)", "display_order": 3},
    
    # Germany
    {"curriculum_code": "de_abitur", "code": "10", "name": "Klasse 10", "display_order": 1},
    {"curriculum_code": "de_abitur", "code": "11", "name": "Klasse 11", "display_order": 2},
    {"curriculum_code": "de_abitur", "code": "12", "name": "Klasse 12", "display_order": 3},
    {"curriculum_code": "de_abitur", "code": "13", "name": "Klasse 13", "display_order": 4},
    
    # Korea
    {"curriculum_code": "kr_csat", "code": "10", "name": "고등학교 1학년", "display_order": 1},
    {"curriculum_code": "kr_csat", "code": "11", "name": "고등학교 2학년", "display_order": 2},
    {"curriculum_code": "kr_csat", "code": "12", "name": "고등학교 3학년", "display_order": 3},
]

grade_level_ids = {}
for gl in grade_levels_data:
    data = {
        "curriculum_system_id": curriculum_ids[gl['curriculum_code']],
        "code": gl['code'],
        "name": gl['name'],
        "display_order": gl['display_order']
    }
    try:
        result = supabase.table("curriculum_grade_levels").insert(data).execute()
        key = f"{gl['curriculum_code']}_{gl['code']}"
        grade_level_ids[key] = result.data[0]['id']
        print(f"  ✅ {gl['name']}")
    except Exception as e:
        print(f"  ⚠️  {gl['name']} (zaten var olabilir)")

print()

# ====================
# 4. TÜRKİYE SUBJECTS
# ====================
print("📚 Türkiye Dersleri ekleniyor...")

tr_curriculum_id = curriculum_ids['tr_osym']

subjects_tr = [
    # TYT Dersleri
    {"name_tr": "Türkçe", "name_en": "Turkish", "code": "turkish"},
    {"name_tr": "Matematik (Temel)", "name_en": "Mathematics (Basic)", "code": "math_basic"},
    {"name_tr": "Geometri (Temel)", "name_en": "Geometry (Basic)", "code": "geometry_basic"},
    {"name_tr": "Tarih", "name_en": "History", "code": "history"},
    {"name_tr": "Coğrafya", "name_en": "Geography", "code": "geography"},
    {"name_tr": "Felsefe", "name_en": "Philosophy", "code": "philosophy"},
    {"name_tr": "Din Kültürü", "name_en": "Religious Culture", "code": "religion"},
    {"name_tr": "Fizik (Temel)", "name_en": "Physics (Basic)", "code": "physics_basic"},
    {"name_tr": "Kimya (Temel)", "name_en": "Chemistry (Basic)", "code": "chemistry_basic"},
    {"name_tr": "Biyoloji (Temel)", "name_en": "Biology (Basic)", "code": "biology_basic"},
    
    # AYT Sayısal
    {"name_tr": "Matematik (İleri)", "name_en": "Mathematics (Advanced)", "code": "math_advanced"},
    {"name_tr": "Geometri (İleri)", "name_en": "Geometry (Advanced)", "code": "geometry_advanced"},
    {"name_tr": "Fizik", "name_en": "Physics", "code": "physics"},
    {"name_tr": "Kimya", "name_en": "Chemistry", "code": "chemistry"},
    {"name_tr": "Biyoloji", "name_en": "Biology", "code": "biology"},
    
    # AYT Sözel
    {"name_tr": "Edebiyat", "name_en": "Literature", "code": "literature"},
    {"name_tr": "Tarih (İleri)", "name_en": "History (Advanced)", "code": "history_advanced"},
    {"name_tr": "Coğrafya (İleri)", "name_en": "Geography (Advanced)", "code": "geography_advanced"},
]

subject_ids = {}
for subj in subjects_tr:
    data = {
        "name_tr": subj['name_tr'],
        "code": subj['code'],
        "curriculum_system_id": tr_curriculum_id,
        "is_active": True
    }
    try:
        result = supabase.table("subjects").insert(data).execute()
        subject_ids[subj['code']] = result.data[0]['id']
        print(f"  ✅ {subj['name_tr']}")
    except Exception as e:
        print(f"  ⚠️  {subj['name_tr']} (zaten var olabilir)")

print("\n🎉 Seed tamamlandı!")
print(f"\n📊 Özet:")
print(f"  - {len(curriculum_systems)} Curriculum System")
print(f"  - {len(exam_types_data)} Exam Type")
print(f"  - {len(grade_levels_data)} Grade Level")
print(f"  - {len(subjects_tr)} Subject (Türkiye)")
