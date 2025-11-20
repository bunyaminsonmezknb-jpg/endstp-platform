# End.STP Platform - Development Roadmap

## 🎯 IRT (Item Response Theory) Entegrasyonu

### Tetikleyiciler:
- [ ] Öğrenci başına 50+ test çözüldüğünde
- [ ] Toplam 500+ test verisi biriktiğinde  
- [ ] Kullanıcı "daha hassas analiz" talep ettiğinde

### Yapılacaklar:
1. [ ] Öğrenci theta hesaplama algoritması
2. [ ] IRT difficulty score hesaplama
3. [ ] Hibrit sistem geçişi (simple + IRT)
4. [ ] Makine öğrenmesi ile iyileştirme

### Hazır Olan Altyapı:
✅ `question_bank` tablosu (IRT parametreleri için)
✅ `student_ability` tablosu (theta değerleri için)
✅ `student_topic_difficulty` tablosu (hibrit skorlar için)
✅ `test_question_responses` tablosu (detaylı veri için)

### Tahmini Süre: 2-4 hafta
### Öncelik: Orta (Veri biriktikten sonra)

---

## 📊 Sınav Ağırlığı Sistemi

### Durum: ✅ Tamamlandı (2025-11-19)

### Özellikler:
✅ Son 5 yıl sınav verisi analizi
✅ Otomatik ağırlık hesaplama
✅ Trend analizi
✅ Sıklık kategorileri

### Kullanım:
```python
calculate_exam_weight(topic_id, exam_system_id, years=5)
```

---

## 🔄 Güncellenecek:
- 2025-11-19: IRT altyapısı hazır, hesaplama ertelendi
- Son güncelleme: 2025-11-19
## 🌍 Global Expansion Plan

### Phase 1: Turkey MVP (Current)
- [x] Turkish language
- [x] YKS exam system
- [x] TYT/AYT structure
- [ ] English UI (basic)

### Phase 2: Pilot Expansion (3-6 months)
- [ ] i18n infrastructure (next-intl)
- [ ] South Korea market entry
  - [ ] Suneung exam system
  - [ ] Korean language support
  - [ ] Local partnerships
- [ ] Full English support

### Phase 3: Regional Expansion (6-12 months)
- [ ] Japan (Center Test)
- [ ] India (JEE, NEET)
- [ ] Iran (Konkur)

### Phase 4: Wide Expansion (12+ months)
- [ ] MENA region
- [ ] Southeast Asia
- [ ] Eastern Europe

### Target Countries Analysis

| Country | Education Stress | Market Size | Competition | Priority |
|---------|------------------|-------------|-------------|----------|
| 🇰🇷 South Korea | ⭐⭐⭐⭐⭐ | High | Medium | 🥇 1 |
| 🇯🇵 Japan | ⭐⭐⭐⭐⭐ | High | Medium | 🥈 2 |
| 🇮🇳 India | ⭐⭐⭐⭐⭐ | Very High | High | 🥉 3 |
| 🇨🇳 China | ⭐⭐⭐⭐⭐ | Very High | Very High | ⚠️ 4 |
| 🇮🇷 Iran | ⭐⭐⭐⭐ | Medium | Low | 🎯 5 |
```

**Kaydet**

---

## ✅ ÖZET

### **Durum:**
```
✅ Mimari ZATEN global ölçeklenmeye hazır
✅ name_local kolonları mevcut
✅ Ülke/sınav sistemi tabloları esnek
✅ Sadece i18n (çeviri) altyapısı lazım
```

### **Öncelik:**
```
1. ŞİMDİ: Türkiye MVP'sini bitir
2. SONRA: İngilizce ekle (demo için)
3. ÇOK SONRA: Diğer ülkeler
```

### **Sonraki Oturumda:**
```
✅ ÖSYM konularını toplu ekleme
✅ Dashboard'da ÖSYM bağlamı gösterme
✅ MVP'yi tamamlama

İleride (4-6 ay sonra):
⏳ i18n kurulumu
⏳ Güney Kore pilot