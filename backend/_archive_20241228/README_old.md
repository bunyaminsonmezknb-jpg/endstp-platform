# 🚀 End.STP Backend API

FastAPI tabanlı, satılabilir analytics API.

## 📁 Proje Yapısı

```
backend/
├── main.py                 # Ana FastAPI uygulaması
├── requirements.txt        # Python bağımlılıkları
├── .env                    # Environment variables
├── api/
│   └── v1/
│       └── student.py      # Student analytics endpoints
├── models/
│   └── schemas.py          # Pydantic models (data validation)
├── services/
│   └── analytics_service.py # İş mantığı ve hesaplamalar
└── core/
    └── config.py           # Configuration yönetimi
```

## 🔧 Kurulum

### 1. Virtual Environment Oluştur

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 2. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

`.env` dosyası zaten var. İsterseniz düzenleyebilirsiniz.

### 4. API'yi Çalıştır

```bash
uvicorn main:app --reload --port 8000
```

Veya:

```bash
python main.py
```

## 📊 API Endpoints

### Base URL: `http://localhost:8000`

### Swagger UI (Otomatik Dokümantasyon)
```
http://localhost:8000/docs
```

### ReDoc (Alternatif Dokümantasyon)
```
http://localhost:8000/redoc
```

### Endpoints:

#### 1. Health Check
```
GET /
GET /health
```

#### 2. Öğrenci Dashboard
```
GET /api/v1/student/{student_id}/dashboard
```

**Response:**
```json
{
  "student_name": "Ahmet Yılmaz",
  "streak": 7,
  "daily_goal": { "current": 5, "target": 12 },
  "weekly_success": 72,
  "topics": [...]
}
```

#### 3. Kurtarma Planı (Partner Links)
```
GET /api/v1/student/{student_id}/topic/{topic_id}/recovery-plan
```

**Response:**
```json
{
  "topic_id": 1,
  "topic_name": "Türev",
  "partner_links": [
    {
      "id": "video",
      "partner_type": "video",
      "partner_name": "Dr. Biyoloji",
      "title": "Türev Özet Video",
      "url": "https://youtube.com/example"
    }
  ]
}
```

#### 4. Konu Durumu Güncelle
```
POST /api/v1/student/{student_id}/topic/update
```

**Request Body:**
```json
{
  "topic_id": 1,
  "new_remembering_rate": 45,
  "study_completed": true
}
```

## 🎯 Özellikler

### ✅ Tamamlanan
- FastAPI kurulumu
- Otomatik API dokümantasyonu (Swagger/ReDoc)
- CORS desteği (Frontend bağlantısı için)
- Mock data endpoints
- Pydantic validation
- Environment configuration

### 🔜 Gelecek
- Database entegrasyonu (Supabase)
- Unutma eğrisi algoritması
- API Key authentication
- Rate limiting
- Caching (Redis)
- WebSocket (real-time notifications)

## 💡 API Satış Modeli

Bu API standalone çalışır ve başka EduTech şirketlerine satılabilir:

1. **API Key** verirsiniz
2. Müşteri kendi frontend'inden çağırır
3. Analytics sonuçlarını kendi uygulamasında gösterir

**Swagger'da test yapabilirler:**
```
https://api.end-stp.com/docs
```

## 🧪 Test

### Manuel Test (Swagger UI)
```
http://localhost:8000/docs
```

### cURL ile Test
```bash
curl http://localhost:8000/api/v1/student/1/dashboard
```

### Python ile Test
```python
import requests

response = requests.get("http://localhost:8000/api/v1/student/1/dashboard")
print(response.json())
```

## 📝 Notlar

- Şu anda **mock data** kullanılıyor
- Database bağlantısı henüz yok
- API Key authentication henüz aktif değil
- Tüm endpoints çalışır durumda ve test edilebilir

---

**Geliştirici:** End.STP Team
**Lisans:** Proprietary

---

## ��️ Veritabanı Anayasası

### Yeni Tablo Oluşturma Kuralları

**Her yeni tablo `TABLE_CREATION_ANAYASA.sql` şablonuna göre oluşturulmalıdır!**

#### Zorunlu Bileşenler:
1. ✅ UUID primary key (otomatik)
2. ✅ Ticari API kolonları (client_id, api_version, vb.)
3. ✅ İşlem durumu (is_processed, processing_status)
4. ✅ Timestamp'ler (created_at, updated_at, deleted_at)
5. ✅ RLS policy'leri
6. ✅ GRANT yetkileri
7. ✅ Index'ler
8. ✅ Constraints

#### Kullanım:
```bash
# 1. Şablonu kopyala
cp TABLE_CREATION_ANAYASA.sql new_table.sql

# 2. TABLE_NAME'i değiştir
sed -i 's/TABLE_NAME/your_table_name/g' new_table.sql

# 3. Veri kolonlarını ekle
# 4. Supabase SQL Editor'da çalıştır
```

**Not:** Bu kurallara uymayan tablolarda permission denied hataları alınır!

