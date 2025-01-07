# API Dokümantasyonu

## Genel Bilgiler
- Base URL: `http://127.0.0.1:5000/api`
- Tüm istekler JSON formatında yanıt döner
- Hata durumunda uygun HTTP durum kodu ve hata mesajı döner

## Endpoints

### 1. Veri Çekme İşlemi Başlatma
- **POST** `/scrape`
- İşlem başlatır ve job_id döner
- **Parametreler:**
  ```json
  {
    "kategori": "Emlak | Cep Telefonu",
    "sehir": "string | null",  // null ise tüm iller taranır (Emlak için)
    "ana_kategori": "string",  // Emlak için: Konut, Arsa, vs.
    "durum": "string",        // Satılık, Kiralık veya İkinci El, Sıfır
    "marka": "string"         // Cep Telefonu için: Apple, Samsung, vs.
  }
  ```
- **Başarılı Yanıt:**
  ```json
  {
    "job_id": "string",
    "status": "running",
    "start_time": "timestamp"
  }
  ```

### 2. İşlem Durumu Sorgulama
- **GET** `/status/<job_id>`
- İşlemin güncel durumunu döner
- **Başarılı Yanıt:**
  ```json
  {
    "status": "running | completed | failed",
    "data": "array | null",
    "error": "string | null",
    "total_items": "number | null"
  }
  ```

### 3. Tüm İşlemleri Listeleme
- **GET** `/jobs`
- Tüm aktif, tamamlanmış ve başarısız işlemleri listeler
- **Başarılı Yanıt:**
  ```json
  {
    "active_jobs": {},
    "completed_jobs": {},
    "failed_jobs": {}
  }
  ```

### 4. Dosya Varlığı Kontrolü
- **GET** `/check-file/<job_id>`
- İşleme ait dosyanın varlığını kontrol eder
- **Başarılı Yanıt:**
  ```json
  {
    "exists": "boolean"
  }
  ```

### 5. Veri İndirme
- **GET** `/download/<job_id>`
- İşleme ait verileri JSON formatında indirir
- **Başarılı Yanıt:** JSON dosyası
- **Dosya Formatları:**
  - Emlak: `{sehir}_{ana_kategori}_{durum}.json`
  - Telefon: `{marka}_{durum}_{tarih}.json`

## Hata Kodları
- 404: İşlem veya dosya bulunamadı
- 500: Sunucu hatası
- 400: Geçersiz istek parametreleri

## Dosya Yapısı
```
JSONLAR/
├── TumKonutSatilik/
│   ├── Ankara.json
│   └── Istanbul.json
└── TumTelefonlar/
    ├── Apple/
    │   ├── apple_ikinci-el_20240107_180610.json
    │   └── apple_sifir_20240107_181523.json
    └── Samsung/
        └── samsung_hepsi_20240107_175432.json
``` 