# 🎯 BACKEND-FIRST PRENSİBİ

**Kılavuz Cümle:**
> "Backend endpoint yazılmadan frontend konuşulmaz."

**Neden?**
1. Frontend HAZIR ve bekliyor
2. Response structure AÇIK ve belli
3. Mock data YOK, real API çağrısı yapıyor
4. Backend yazmadan frontend incelemek zaman kaybı

**Yaklaşım:**
1. ✅ Backend endpoint yaz
2. ✅ Test et (Swagger/curl)
3. ✅ Frontend'de dene
4. ✅ Sonra component'e bak (gerekirse)

**Frontend İnceleme:**
- SADECE response structure anlamak için
- SADECE hangi data beklediğini görmek için
- Component nasıl çalışıyor diye BAKMA
- Backend yazınca kendiliğinden çalışacak

**Exceptions:**
- Accordion UI (yeni feature, backend yok)
- Design patterns (öğrenme amaçlı)

---

## 🚨 YENİ ALTINA KURAL

**"Yeni eklemeden önce mevcut yapıya bak!"**

### ZORUNLU KONTROL SÜRECİ:

**Yeni dosya/endpoint eklemeden ÖNCE:**

1. ✅ Klasör yapısını kontrol et: `ls -la app/api/v1/endpoints/student/`
2. ✅ İlgili dosyayı TAM görüntüle: `cat dashboard.py`
3. ✅ Endpoint'leri listele: `grep "@router" dashboard.py`
4. ✅ Fonksiyonları listele: `grep "^def " utils.py`
5. ✅ Zaten VARSA → GÜNCELLE
6. ✅ YOKSA → EKLE

**NEDEN GEREKLİ?**
- Duplicate dosyalar önlenir
- Kod çöplüğü oluşmaz
- Mevcut yapı korunur
- Modüler mimari bozulmaz

**KURAL:**
> "Claude, yeni bir şey ekleyeceğin zaman 'ZATEN VAR MI?' diye sor!"

**ÖRNEKLERLe:**

❌ **YANLIŞ YAKLAŞIM:**
```bash
# Direkt dosya oluştur
cat > app/api/v1/endpoints/student.py << 'EOF'
...

---

## 🚨 YENİ ALTINA KURAL

**"Yeni eklemeden önce mevcut yapıya bak!"**

### ZORUNLU KONTROL SÜRECİ:

**Yeni dosya/endpoint eklemeden ÖNCE:**

1. ✅ Klasör yapısını kontrol et: `ls -la app/api/v1/endpoints/student/`
2. ✅ İlgili dosyayı TAM görüntüle: `cat dashboard.py`
3. ✅ Endpoint'leri listele: `grep "@router" dashboard.py`
4. ✅ Fonksiyonları listele: `grep "^def " utils.py`
5. ✅ Zaten VARSA → GÜNCELLE
6. ✅ YOKSA → EKLE

**NEDEN GEREKLİ?**
- Duplicate dosyalar önlenir
- Kod çöplüğü oluşmaz
- Mevcut yapı korunur
- Modüler mimari bozulmaz

**KURAL:**
> "Claude, yeni bir şey ekleyeceğin zaman 'ZATEN VAR MI?' diye sor!"

**ÖRNEKLERLe:**

❌ **YANLIŞ YAKLAŞIM:**
```bash
# Direkt dosya oluştur
cat > app/api/v1/endpoints/student.py << 'EOF'
...

---

## 🚨 YENİ ALTINA KURAL

**"Yeni eklemeden önce mevcut yapıya bak!"**

### ZORUNLU KONTROL SÜRECİ:

**Yeni dosya/endpoint eklemeden ÖNCE:**

1. ✅ Klasör yapısını kontrol et: `ls -la app/api/v1/endpoints/student/`
2. ✅ İlgili dosyayı TAM görüntüle: `cat dashboard.py`
3. ✅ Endpoint'leri listele: `grep "@router" dashboard.py`
4. ✅ Fonksiyonları listele: `grep "^def " utils.py`
5. ✅ Zaten VARSA → GÜNCELLE
6. ✅ YOKSA → EKLE

**NEDEN GEREKLİ?**
- Duplicate dosyalar önlenir
- Kod çöplüğü oluşmaz
- Mevcut yapı korunur
- Modüler mimari bozulmaz

**KURAL:**
> "Claude, yeni bir şey ekleyeceğin zaman 'ZATEN VAR MI?' diye sor!"

**ÖRNEKLERLe:**

❌ **YANLIŞ YAKLAŞIM:**
```bash
# Direkt dosya oluştur
cat > app/api/v1/endpoints/student.py << 'EOF'
...
