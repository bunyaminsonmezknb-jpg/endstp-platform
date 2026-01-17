# End.STP — Proje Karar & Değişiklik Kayıtları (L5 Yolculuğu)

Bu doküman End.STP platformunda alınan tüm mimari, teknik, pedagojik ve ürün kararlarının
zaman sıralı kayıtlarını içerir.

Amaç:
- Tek kişiye bağımlılığı ortadan kaldırmak
- Teknik borcu görünür kılmak
- L5 (explainable, auditable, scalable) mimariyi sürdürülebilir kılmak
- Yeni bir mühendis / ekip / yatırımcı için hızlı bağlam sağlamak

Kural:
- Çalışan ama açıklanmamış **hiçbir** kod kabul edilmez.
- Her motor, endpoint, algoritma, formül burada iz bırakır.


## [2026-01-17] FAZ 4B — Priority Engine / Adapter Başlangıcı

**Kapsam**
- Dosyalar:
  - app/motors/priority/engine.py
- Endpoint:
  - GET /api/v1/student/motors/priority

**Problem / Neden**
- UI ve backend içinde dağılmış öncelik hesapları kontrolsüzdü
- Açıklanabilirlik ve test edilebilirlik yoktu

**Değişiklik**
- Priority motoru saf (pure) engine olarak ayrıştırıldı

**Kontrat**
- Input: Topic performans metrikleri
- Output: Öncelik sıralı liste + reason codes

**Risk & Mitigation**
- Risk: Yanlış skorlamanın öğrenci yönlendirmesi
- Önlem: deterministic engine + açıklama kodları

**Test**
- Adapter sonrası manuel test




## [2026-01-17] FAZ 4B — Priority Engine saf çekirdek (engine.py)

**Kapsam**
- Dosyalar:
  - app/motors/priority/types.py (kullanıcı oluşturdu)
  - app/motors/priority/engine.py (saf motor çekirdeği)
- Endpoint:
  - (henüz bağlanmadı, adapter sonraki adım)

**Problem / Neden**
- Motor mantıkları UI içinde dağılmamalı; açıklanabilir ve test edilebilir çekirdeğe alınmalı.
- Orchestrator/engine sorumluluk ayrımı net olmalı.

**Değişiklik**
- Priority motoru için saf skor/sıralama fonksiyonu tanımlandı (DB/HTTP yok).

**Kontrat**
- Input: topic listesi (başarı, test sayısı, last_test_date, trend)
- Output: sıralı items + reason_codes + meta
- Invariant: deterministic, side-effect yok

**Risk & Mitigation**
- Risk: tip uyuşmazlığı
- Önlem: defensive parsing + types.py kontratı
- Geri dönüş: engine yalnızca ek dosya; sistem davranışını bozmaz (adapter bağlanmadan)

**Test**
- Adapter sonrası unit test eklenebilir (örnek payload → sıralama bekleneni)


## [2026-01-17] FAZ 4B — Priority Engine (L5 Uyumlu) Başlangıcı

**Kapsam**
- Motor: Priority Engine
- Dosyalar:
  - app/motors/priority/engine.py
  - app/motors/priority/adapter.py
  - app/motors/priority/types.py
- Endpoint:
  - GET /student/motors/priority

**Problem / Neden**
- Öncelik hesapları UI ve backend içinde dağınıktı
- Açıklanabilirlik ve test edilebilirlik yoktu
- Teknik borç riski oluşuyordu

**Çözüm**
- Saf (pure) hesap yapan engine ayrıştırıldı
- HTTP, auth ve DB erişimi adapter katmanına alındı
- Engine deterministik ve state-free tasarlandı

**Kontrat**
- Input: Topic bazlı performans özetleri
- Output:
  - priority_score (0–100)
  - reason_codes (neden öncelikli olduğu)

**Açıklanabilirlik**
- Her skor, reason_codes ile gerekçelendiriliyor

**Risk & Önlem**
- Risk: Yanlış yönlendirme
- Önlem: Basit, şeffaf, test edilebilir kurallar

**Durum**
- FAZ 4B başlangıcı tamamlandı
