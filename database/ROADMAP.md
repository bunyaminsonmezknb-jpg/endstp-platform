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