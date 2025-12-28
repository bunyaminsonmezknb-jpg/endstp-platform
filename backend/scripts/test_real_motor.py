"""
Real Motor Test
Gerçek öğrenci verileriyle motor hesaplaması
"""
import sys
sys.path.insert(0, '/home/endstp/endstp-platform/backend')

from app.db.session import get_supabase_admin
from app.core.motor_wrapper import MotorWrapper
from app.core.motor_registry import MotorType, SubscriptionTier
import asyncio


async def test_real_student():
    """Gerçek öğrenci verileriyle test"""
    supabase = get_supabase_admin()
    
    print("=" * 60)
    print("REAL MOTOR TEST - Gerçek Öğrenci Verisi")
    print("=" * 60)
    
    # 1. Random öğrenci bul
    students = supabase.table("user_profiles").select(
        "id, first_name, last_name, subscription_tier"
    ).eq("role", "student").limit(1).execute()
    
    if not students.data:
        print("❌ Hiç öğrenci bulunamadı!")
        return
    
    student = students.data[0]
    print(f"\n✅ Öğrenci: {student['first_name']} {student['last_name']}")
    print(f"   ID: {student['id']}")
    print(f"   Tier: {student.get('subscription_tier', 'free')}")
    
    # 2. Öğrencinin test sonuçlarını bul
    test_results = supabase.table("topic_test_results").select(
        "*, topics(name_tr, subject:subjects(name_tr))"
    ).eq("user_id", student['id']).limit(5).execute()
    
    if not test_results.data:
        print("❌ Öğrencinin test sonucu yok!")
        return
    
    print(f"\n📊 Test Sonuçları: {len(test_results.data)} adet bulundu")
    
    # 3. İlk konuyu seç ve motor hesapla
    first_test = test_results.data[0]
    topic = first_test['topics']
    
    print(f"\n🎯 Seçilen Konu:")
    print(f"   Ders: {topic['subject']['name_tr']}")
    print(f"   Konu: {topic['name_tr']}")
    print(f"   Doğru: {first_test['questions_correct']}/{first_test['questions_total']}")
    print(f"   Yanlış: {first_test['questions_wrong']}")
    print(f"   Boş: {first_test['questions_blank']}")
    
    # 4. Motor hesaplama
    print("\n⚙️  Motor Hesaplaması Başlıyor...")
    
    wrapper = MotorWrapper(MotorType.DIFFICULTY)
    
    tier = SubscriptionTier(student.get('subscription_tier', 'free'))
    
    result = await wrapper.execute(
        user_id=student['id'],
        user_tier=tier,
        student_id=student['id'],
        topic_id=first_test['topic_id']
    )
    
    # 5. Sonuçları göster
    print("\n" + "=" * 60)
    print("MOTOR SONUÇLARI")
    print("=" * 60)
    print(f"Zorluk Yüzdesi: {result.get('difficulty_percentage', 0):.1f}%")
    print(f"Zorluk Seviyesi: {result.get('difficulty_level', 0)}/5")
    print(f"Öğrenci Segmenti: {result.get('student_segment', 'N/A')}")
    print(f"Öğrenci Mesajı: {result.get('student_message', 'N/A')}")
    print(f"\nMotor Metadata:")
    print(f"  Version: {result.get('motor_metadata', {}).get('motor_version', 'N/A')}")
    print(f"  Features: {result.get('motor_metadata', {}).get('features_used', 0)}")
    print(f"  Fallback: {result.get('motor_metadata', {}).get('fallback_used', False)}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_real_student())
