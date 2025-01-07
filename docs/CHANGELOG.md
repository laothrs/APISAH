# Değişiklik Günlüğü

## [Yayınlanmamış]

### Eklenenler
- JSONLAR klasörü yapısı güncellendi
  - Emlak verileri için: `JSONLAR/Tum{AnaKategori}{Durum}/{Sehir}.json`
  - Telefon verileri için: `JSONLAR/TumTelefonlar/{Marka}/{marka}_{durum}_{tarih}.json`
- İndirme sistemi geliştirildi
  - Dosya varlığı kontrolü eklendi
  - İşlem durumundan bağımsız indirme özelliği
  - Anlamlı dosya isimlendirmesi
- İşlem listesi arayüzü geliştirildi
  - Durum rozetleri eklendi (Devam Ediyor, Tamamlandı, Başarısız)
  - İş detayları görünümü iyileştirildi
  - İndirme butonu optimizasyonu

### Değişenler
- Material-UI'dan Chakra UI'ya geçiş yapıldı
- İndirme sistemi dosya bazlı çalışacak şekilde güncellendi
- Arayüz modern ve kullanıcı dostu hale getirildi

### Düzeltmeler
- İndirme butonunun sadece tamamlanmış işlemlerde aktif olması sorunu giderildi
- Dosya adı formatı standardize edildi
- Hata yönetimi geliştirildi

## [1.0.0] - 2024-01-02

### Eklenenler
- Docs klasörü oluşturuldu
- CHANGELOG.md dosyası eklendi
- API.md dosyası eklendi
- DEVELOPMENT.md dosyası eklendi

### Özellikler
- Sahibinden.com veri çekme sistemi
- Emlak ve telefon kategorileri desteği
- Çoklu şehir tarama özelliği
- JSON formatında veri saklama
- Modern web arayüzü

### Teknik Detaylar
- Python Flask backend
- React frontend
- Selenium web scraping
- Chakra UI component library
- RESTful API mimarisi
