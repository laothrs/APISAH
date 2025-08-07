CURSOR AI IDE TEST PROJESİDİR PROJE TAMAMIYLE CURSOR UZERINDEN YAPILMIŞTIR
# Veri Çekme API'si  (SADECE EGITIM AMACLIDIR HICBIR YASAL YUKUMLULUK VESAIRE YOKTUR SORUMLULUK BANA DEGIL KULLANAN KISIYE AITTIR)

Bu proje,  üzerinden cep telefonu ve emlak kategorilerindeki ilanları otomatik olarak çekebilen bir API ve web arayüzü sunar.

## Özellikler

- Cep telefonu ve emlak ilanlarını filtreleme ve çekme
- Tüm illeri otomatik tarama (Ankara'dan başlayarak)
- Her il için 50 sayfa veri çekme
- Türkçe karakter desteği
- Asenkron işlem yönetimi
- İşlem durumu takibi
- Modern web arayüzü
- Cloudflare bypass desteği
- Bot tespiti engelleme
- Otomatik veri kaydetme
- Düzenli klasör yapısı

## Klasör Yapısı

```
JSONLAR/
  └── TumIllerSatilikDaire/
      ├── Ankara.json
      ├── Istanbul.json
      ├── Izmir.json
      └── ...
```

## Gereksinimler

### Backend
- Python 3.8+
- Flask
- Selenium
- BeautifulSoup4
- DrissionPage
- CloudflareBypassForScraping

### Frontend
- Node.js 16+
- React
- Material-UI
- Axios

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. Frontend bağımlılıklarını yükleyin:
```bash
cd frontend
npm install
```

3. ChromeDriver'ı yükleyin:
```bash
sudo apt-get install chromium-chromedriver
```

## Kullanım

1. API'yi başlatın:
```bash
python api.py
```

2. Frontend geliştirme sunucusunu başlatın:
```bash
cd frontend
npm run dev
```

3. Tarayıcıda `http://localhost:5173` adresine gidin

## API Endpoints

### Cep Telefonu İlanları
- **Endpoint:** `/api/scrape/phone`
- **Method:** POST
- **Parametreler:**
  - sehir (string): Şehir plaka kodu
  - marka (string): Telefon markası
  - ram (string): RAM miktarı
  - renk (string): Renk kodu
  - durum (string): Sıfır/İkinci el

### Emlak İlanları
- **Endpoint:** `/api/scrape/estate`
- **Method:** POST
- **Parametreler:**
  - ana_kategori (string): Konut/Daire/Arsa
  - durum (string): Satılık/Kiralık
  - sehir (string): Şehir adı
  - oda_sayisi (string): Oda sayısı kodu
  - isitma_tipi (string): Isıtma tipi kodu
  - tum_iller (boolean): Tüm illeri tarama seçeneği

### İşlem Durumu
- **Endpoint:** `/api/status/<job_id>`
- **Method:** GET

### Tüm İşlemler
- **Endpoint:** `/api/jobs`
- **Method:** GET

## Güvenlik

- Bot tespiti engelleme
- Cloudflare bypass
- Rate limiting
- User-Agent rotasyonu
- Header optimizasyonu

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın. 
