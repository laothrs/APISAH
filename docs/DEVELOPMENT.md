# Geliştirici Dokümantasyonu

## Geliştirme Ortamı Kurulumu

### Backend Gereksinimleri
- Python 3.8+
- Flask
- Selenium
- Chrome WebDriver
- BeautifulSoup4

### Frontend Gereksinimleri
- Node.js 16+
- React 18
- Chakra UI
- Axios

### Kurulum Adımları

1. Repo'yu klonlayın:
```bash
git clone https://github.com/kullanıcı/APISah.git
cd APISah
```

2. Backend kurulumu:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Frontend kurulumu:
```bash
cd frontend
npm install
```

4. Chrome WebDriver kurulumu:
```bash
# Linux için:
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Windows için Chrome'u manuel indirin ve PATH'e ekleyin
```

## Geliştirme

### Backend Geliştirme
1. Flask uygulamasını çalıştırın:
```bash
python api.py
```

2. API endpoint'leri:
- Tüm endpoint'ler `api.py` dosyasında tanımlanır
- Her endpoint için hata yönetimi ekleyin
- Yeni özellikler için `sahibinden_scraper.py`'ı güncelleyin

### Frontend Geliştirme
1. Geliştirme sunucusunu başlatın:
```bash
cd frontend
npm start
```

2. Bileşen yapısı:
- `src/components/` altında bileşenler
- Chakra UI tema özelleştirmeleri
- Form ve liste bileşenleri

## Test

### Backend Testleri
```bash
python -m pytest tests/
```

### Frontend Testleri
```bash
cd frontend
npm test
```

## Dağıtım

### Backend Dağıtımı
1. Gereksinimleri güncelleyin:
```bash
pip freeze > requirements.txt
```

2. Sunucu kurulumu:
- Python ve bağımlılıkları yükleyin
- Chrome ve WebDriver kurun
- Supervisor ile servis yapılandırın

### Frontend Dağıtımı
1. Üretim derlemesi:
```bash
cd frontend
npm run build
```

2. Derlenen dosyaları sunucuya aktarın

## Kodlama Standartları

### Python Kodlama Standartları
- PEP 8 kurallarına uyun
- Docstring kullanın
- Type hinting kullanın
- Anlamlı değişken isimleri kullanın

### JavaScript Kodlama Standartları
- ESLint kurallarına uyun
- Prettier formatlaması kullanın
- Component'leri fonksiyon olarak yazın
- Props için TypeScript kullanın

## Git Workflow

1. Feature branch oluşturun:
```bash
git checkout -b feature/yeni-ozellik
```

2. Commit mesajları:
```
feat: Yeni özellik eklendi
fix: Hata düzeltmesi
docs: Dokümantasyon güncellendi
style: Kod formatlaması
refactor: Kod iyileştirmesi
```

3. Pull Request açın ve review isteyin

## Versiyon Yönetimi

### Semantic Versioning
- MAJOR.MINOR.PATCH formatı
- MAJOR: Uyumsuz API değişiklikleri
- MINOR: Geriye dönük uyumlu yeni özellikler
- PATCH: Geriye dönük uyumlu hata düzeltmeleri

### Changelog
- Her sürüm için değişiklikleri CHANGELOG.md'ye ekleyin
- Değişiklikleri kategorilere ayırın:
  - Eklenenler
  - Değişenler
  - Düzeltmeler
  - Kaldırılanlar 