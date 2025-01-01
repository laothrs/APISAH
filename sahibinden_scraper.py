from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import time
import json
import random
from datetime import datetime
import sys
import os
from DrissionPage import ChromiumPage
from CloudflareBypassForScraping.CloudflareBypasser import CloudflareBypasser

class SahibindenScraper:
    def __init__(self, headless=False):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument('--headless')
        
        # Temel ayarlar
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        
        # Bot tespitini engelleme ayarları
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Ek bot koruması bypass ayarları
        self.chrome_options.add_argument('--disable-web-security')
        self.chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        self.chrome_options.add_argument('--disable-notifications')
        self.chrome_options.add_argument('--disable-popup-blocking')
        
        
        # Rastgele User-Agent
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        self.user_agent = random.choice(self.user_agents)
        
        # Ek header'lar
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        self.chrome_options.add_argument(f'--user-agent={self.user_agent}')
        
        # Chrome binary konumu
        self.chrome_options.binary_location = "/usr/bin/chromium-browser"
        
        self.driver = None
        self.ilanlar = []
        self.max_deneme = 3
        self.sayfa_ilan_sayisi = 0
        
        # DrissionPage ve CloudflareBypasser
        self.chromium_page = ChromiumPage()
        self.cf_bypasser = CloudflareBypasser(driver=self.chromium_page)
        
        # Filtre seçenekleri
        self.sehirler = {
            "Adana": "1", "Adıyaman": "2", "Afyonkarahisar": "3", "Ağrı": "4", "Amasya": "5",
            "Ankara": "6", "Antalya": "7", "Artvin": "8", "Aydın": "9", "Balıkesir": "10",
            "Bilecik": "11", "Bingöl": "12", "Bitlis": "13", "Bolu": "14", "Burdur": "15",
            "Bursa": "16", "Çanakkale": "17", "Çankırı": "18", "Çorum": "19", "Denizli": "20",
            "Diyarbakır": "21", "Edirne": "22", "Elazığ": "23", "Erzincan": "24", "Erzurum": "25",
            "Eskişehir": "26", "Gaziantep": "27", "Giresun": "28", "Gümüşhane": "29", "Hakkari": "30",
            "Hatay": "31", "Isparta": "32", "Mersin": "33", "İstanbul-Avrupa": "34", "İstanbul-Anadolu": "34",
            "İzmir": "35", "Kars": "36", "Kastamonu": "37", "Kayseri": "38", "Kırklareli": "39",
            "Kırşehir": "40", "Kocaeli": "41", "Konya": "42", "Kütahya": "43", "Malatya": "44",
            "Manisa": "45", "Kahramanmaraş": "46", "Mardin": "47", "Muğla": "48", "Muş": "49",
            "Nevşehir": "50", "Niğde": "51", "Ordu": "52", "Rize": "53", "Sakarya": "54",
            "Samsun": "55", "Siirt": "56", "Sinop": "57", "Sivas": "58", "Tekirdağ": "59",
            "Tokat": "60", "Trabzon": "61", "Tunceli": "62", "Şanlıurfa": "63", "Uşak": "64",
            "Van": "65", "Yozgat": "66", "Zonguldak": "67", "Aksaray": "68", "Bayburt": "69",
            "Karaman": "70", "Kırıkkale": "71", "Batman": "72", "Şırnak": "73", "Bartın": "74",
            "Ardahan": "75", "Iğdır": "76", "Yalova": "77", "Karabük": "78", "Kilis": "79",
            "Osmaniye": "80", "Düzce": "81"
        }
        
        self.markalar = {
            "Apple": "apple-cep-telefonu",
            "Samsung": "samsung-cep-telefonu",
            "Xiaomi": "xiaomi-cep-telefonu",
            "Huawei": "huawei-cep-telefonu",
            "Oppo": "oppo-cep-telefonu",
            "Vivo": "vivo-cep-telefonu",
            "Realme": "realme-cep-telefonu",
            "OnePlus": "oneplus-cep-telefonu",
            "Google": "google-cep-telefonu",
            "Sony": "sony-cep-telefonu",
            "LG": "lg-cep-telefonu",
            "Nokia": "nokia-cep-telefonu",
            "Motorola": "motorola-cep-telefonu",
            "Asus": "asus-cep-telefonu",
            "Honor": "honor-cep-telefonu",
            "Alcatel": "alcatel-cep-telefonu"
        }

        self.durumlar = {
            "Tümü": "",
            "Sıfır": "sifir",
            "İkinci El": "ikinci-el"
        }
        
        self.ram_secenekleri = {
            "2 GB": "60789",
            "3 GB": "60791",
            "4 GB": "1170397",
            "6 GB": "1170398",
            "8 GB": "1170399",
            "12 GB": "1170400",
            "16 GB": "1398858",
            "32 GB": "1064928196"
        }
        
        self.renkler = {
            "Altın": "41726",
            "Altın Sarısı": "41731",
            "Bej": "121252",
            "Beyaz": "41728",
            "Bordo": "121254",
            "Füme": "121255",
            "Gri": "41724",
            "Gümüş": "41730",
            "Haki": "121256",
            "Kahverengi": "41729",
            "Kırmızı": "41723",
            "Lacivert": "41721",
            "Mavi": "41720",
            "Mor": "41722",
            "Pembe": "41727",
            "Sarı": "41732",
            "Siyah": "41719",
            "Şampanya": "41733",
            "Turkuaz": "41734",
            "Turuncu": "41725",
            "Yeşil": "41735"
        }
        
        # Kategori seçenekleri
        self.kategoriler = {
            "Cep Telefonu": {
                "base_url": "https://www.sahibinden.com/modeller-cep-telefonu",
                "alt_kategoriler": None  # Cep telefonunda alt kategori yok
            },
            "Emlak": {
                "base_url": "https://www.sahibinden.com",
                "alt_kategoriler": {
                    "Konut": {
                        "base_url": "https://www.sahibinden.com",
                        "durumlar": {
                            "Satılık": "satilik",
                            "Kiralık": "kiralik"
                        }
                    },
                    "Daire": {
                        "base_url": "https://www.sahibinden.com",
                        "durumlar": {
                            "Satılık": "satilik-daire",
                            "Kiralık": "kiralik-daire"
                        }
                    },
                    "Arsa": {
                        "base_url": "https://www.sahibinden.com",
                        "durumlar": {
                            "Satılık": "satilik-arsa",
                            "Kiralık": "kiralik-arsa"
                        }
                    }
                }
            }
        }
        
        # Emlak özellikleri
        self.oda_sayilari = {
            "1+1": "4364",
            "2+1": "4365",
            "3+1": "4366",
            "4+1": "4367",
            "4+2": "4372"
        }
        
        self.isitma_tipleri = {
            "Doğalgaz (Kombi)": "4382",
            "Merkezi Sistem": "4386",
            "Soba": "4384",
            "Yerden Isıtma": "4389",
            "Klima": "107288"
        }
        
    def rastgele_bekleme(self, min_saniye=0.1, max_saniye=0.2):
        sure = random.uniform(min_saniye, max_saniye)
        print(f"[Bilgi] {sure:.1f} saniye bekleniyor...")
        time.sleep(sure)
        
    def tarayici_baslat(self):
        print("[Başlangıç] Tarayıcı başlatılıyor...")
        service = Service('/usr/bin/chromedriver')
        
        # WebDriver özelliğini gizle
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        
        # Ek header'ları ekle
        self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': self.headers})
        
        # Cloudflare bypass için ek ayarlar
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                Object.defineProperty(navigator, 'platform', {
                    get: function() {
                        return 'Win32';
                    }
                });
            '''
        })
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("[Başlangıç] Tarayıcı başlatıldı")
        
    def tarayici_kapat(self):
        if self.driver:
            print("[Bitiş] Tarayıcı kapatılıyor...")
            self.driver.quit()
            print("[Bitiş] Tarayıcı kapatıldı")
            
    def yeni_sekmede_ac(self, url):
        """Yeni sekmede URL'i açar ve eski sekmeyi kapatır"""
        try:
            print(f"[İşlem] Yeni sekme açılıyor: {url}")
            
            # Cloudflare bypass işlemi
            print("[İşlem] Cloudflare bypass başlatılıyor...")
            self.chromium_page.get(url)
            self.cf_bypasser.bypass()
            
            if not self.cf_bypasser.is_bypassed():
                print("[Hata] Cloudflare bypass başarısız oldu")
                return False
                
            html_content = self.chromium_page.html
            
            # Yeni sekme aç
            self.driver.execute_script("window.open('');")
            yeni_sekme = self.driver.window_handles[-1]
            self.driver.switch_to.window(yeni_sekme)
            
            # Temel cookie'leri ekle
            try:
                self.driver.add_cookie({
                    'name': 'cf_clearance',
                    'value': self.cf_bypasser.cf_clearance,
                    'domain': '.sahibinden.com',
                    'path': '/'
                })
            except Exception as e:
                print(f"[Uyarı] Cloudflare cookie eklenirken hata: {e}")
            
            # Yeni sekmede URL'i yükle
            self.driver.get(url)
            
            # Eski sekmeleri kapat
            mevcut_sekme = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != mevcut_sekme:
                    self.driver.switch_to.window(handle)
                    print(f"[İşlem] Eski sekme kapatılıyor: {handle}")
                    self.driver.close()
            
            # Aktif sekmeye geri dön
            self.driver.switch_to.window(mevcut_sekme)
            
            # HTML içeriğini güvenli bir şekilde yükle
            try:
                # JavaScript'teki özel karakterleri escape et
                html_content = html_content.replace('`', '\\`').replace('$', '\\$')
                self.driver.execute_script(f"document.documentElement.innerHTML = `{html_content}`")
                
                # Sayfanın tamamen yüklenmesini bekle
                self.driver.execute_script("return document.readyState") == "complete"
                
            except Exception as e:
                print(f"[Uyarı] HTML içeriği yüklenirken hata oluştu: {e}")
                # HTML içeriğini direkt olarak ayarla
                self.driver.execute_script("document.open()")
                self.driver.execute_script(f"document.write(`{html_content}`)")
                self.driver.execute_script("document.close()")
            
            return True
            
        except Exception as e:
            print(f"[Hata] Yeni sekme açılırken hata oluştu: {e}")
            return False
            
    def sayfa_verilerini_cek(self, url, deneme=0):
        self.sayfa_ilan_sayisi = 0
        try:
            if not self.yeni_sekmede_ac(url):
                if deneme < self.max_deneme:
                    print(f"[Uyarı] Sayfa açılamadı, {deneme + 1}. deneme yapılıyor...")
                    self.rastgele_bekleme(1, 2)
                    return self.sayfa_verilerini_cek(url, deneme + 1)
                return
            
            try:
                print("[İşlem] Sayfa elemanları bekleniyor...")
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "searchResultsItem"))
                )
            except TimeoutException:
                if deneme < self.max_deneme:
                    print(f"[Uyarı] Sayfa yüklenemedi, {deneme + 1}. deneme yapılıyor...")
                    self.rastgele_bekleme(1, 2)
                    return self.sayfa_verilerini_cek(url, deneme + 1)
                else:
                    print("[Hata] Maksimum deneme sayısına ulaşıldı, sayfa atlanıyor.")
                    return
            
            # İnsan davranışı simülasyonu
            print("[İşlem] Sayfa kaydırma simülasyonu başlıyor...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            print("[İşlem] Sayfa içeriği ayrıştırılıyor...")
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            ilan_elemanlari = soup.find_all("tr", class_="searchResultsItem")
            
            if not ilan_elemanlari:
                if deneme < self.max_deneme:
                    print("[Uyarı] İlan bulunamadı, sayfa yeniden yükleniyor...")
                    self.rastgele_bekleme(1, 2)
                    return self.sayfa_verilerini_cek(url, deneme + 1)
                else:
                    print("[Hata] İlan bulunamadı, sayfa atlanıyor.")
                    return
            
            print(f"[Bilgi] Toplam {len(ilan_elemanlari)} ilan bulundu, veriler çekiliyor...")
            
            for i, ilan in enumerate(ilan_elemanlari, 1):
                try:
                    baslik = ilan.find("a", class_="classifiedTitle").text.strip()
                    fiyat = ilan.find("td", class_="searchResultsPriceValue").text.strip()
                    konum = ilan.find("td", class_="searchResultsLocationValue").text.strip()
                    
                    ilan_bilgisi = {
                        "baslik": baslik,
                        "fiyat": fiyat,
                        "konum": konum
                    }
                    
                    self.ilanlar.append(ilan_bilgisi)
                    self.sayfa_ilan_sayisi += 1
                    print(f"[Başarılı] ({i}/{len(ilan_elemanlari)}) İlan eklendi: {baslik[:50]}...")
                    
                except AttributeError as e:
                    print(f"[Hata] ({i}/{len(ilan_elemanlari)}) İlan verisi çekilirken hata: {e}")
                    continue
                    
        except WebDriverException as e:
            if deneme < self.max_deneme:
                print(f"[Uyarı] Tarayıcı hatası, yeniden deneniyor... Hata: {e}")
                self.rastgele_bekleme(10, 15)
                return self.sayfa_verilerini_cek(url, deneme + 1)
            else:
                print(f"[Hata] Maksimum deneme sayısına ulaşıldı. Hata: {e}")
                
        except Exception as e:
            print(f"[Hata] Beklenmeyen hata: {e}")
            
        finally:
            print(f"[Özet] Bu sayfadan toplam {self.sayfa_ilan_sayisi} ilan başarıyla çekildi")
            
    def filtreli_url_olustur(self, kategori, base_url, **kwargs):
        """Seçilen filtrelere göre URL oluşturur"""
        if kategori == "Cep Telefonu":
            # Cep telefonu için URL oluşturma
            url_parcalari = [base_url]
            durum = kwargs.get('durum')
            marka = kwargs.get('marka')
            
            if durum:
                url_parcalari.append(durum)
                
            if marka:
                if durum:
                    url_parcalari[-1] = marka + "/" + url_parcalari[-1]
                else:
                    url_parcalari.append(marka)
                    
        elif kategori == "Emlak":
            # Emlak için URL oluşturma
            ana_kategori = kwargs.get('ana_kategori')
            durum = kwargs.get('durum')
            sehir = kwargs.get('sehir')
            
            # Base URL'yi oluştur
            url_parcalari = ["https://www.sahibinden.com"]
            
            # URL'yi oluştur
            url_parcalari.append(self.kategoriler["Emlak"]["alt_kategoriler"][ana_kategori]["durumlar"][durum])
            
            # Şehir ekle
            if sehir:
                # Şehir adını küçük harfe çevir ve Türkçe karakterleri değiştir
                sehir = sehir.lower().replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
                url_parcalari.append(sehir)
        
        # URL'yi birleştir
        url = "/".join(url_parcalari)
        
        # Filtreleri ekle
        filtreler = []
        
        if kategori == "Cep Telefonu":
            # Cep telefonu filtreleri
            sehir = kwargs.get('sehir')
            ram = kwargs.get('ram')
            renk = kwargs.get('renk')
            
            if sehir:
                filtreler.append(f"address_city={sehir}")
            if ram:
                filtreler.append(f"a103916={ram}")
            if renk:
                filtreler.append(f"a46187={renk}")
                
        elif kategori == "Emlak":
            # Emlak filtreleri
            if ana_kategori in ["Konut", "Daire"]:
                oda_sayisi = kwargs.get('oda_sayisi')
                isitma_tipi = kwargs.get('isitma_tipi')
                
                if oda_sayisi:
                    filtreler.append(f"a5943={oda_sayisi}")
                if isitma_tipi:
                    filtreler.append(f"a5946={isitma_tipi}")
        
        # Sayfalama için offset
        offset = kwargs.get('offset')
        if offset is not None:
            filtreler.append(f"pagingOffset={offset}")
            
        # Filtreleri URL'ye ekle
        if filtreler:
            url = url + "?" + "&".join(filtreler)
            
        return url
        
    def veri_topla_filtreli(self, kategori, **kwargs):
        """Filtrelere göre veri toplama"""
        try:
            self.tarayici_baslat()
            toplam_ilan = 0
            sayfa = 1
            
            # JSON dosya adını başlangıçta oluştur
            tarih = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Filtre bilgisini kategoriye göre oluştur
            if kategori == "Cep Telefonu":
                filtre_bilgisi = "_".join(filter(None, [
                    kwargs.get('sehir'), 
                    kwargs.get('marka'), 
                    kwargs.get('ram'), 
                    kwargs.get('renk'), 
                    kwargs.get('durum')
                ]))
            else:  # Emlak
                filtre_bilgisi = "_".join(filter(None, [
                    kwargs.get('sehir'),
                    kwargs.get('alt_kategori'),
                    kwargs.get('oda_sayisi'),
                    kwargs.get('isitma_tipi')
                ]))
                
            dosya_adi = f"{kategori.lower().replace(' ', '_')}_{filtre_bilgisi}_{tarih}.json"
            
            base_url = self.kategoriler[kategori]["base_url"]
            
            print(f"\n[Başlangıç] {kategori} için veri toplama işlemi başlıyor...")
            
            # Seçilen filtreleri göster
            print("\n[Filtreler]")
            for key, value in kwargs.items():
                if value:
                    print(f"{key.replace('_', ' ').title()}: {value}")

            print(f"\n[Bilgi] Veriler {dosya_adi} dosyasına kaydedilecek")
            
            while True:  # Sonsuz döngü
                # URL oluştur
                offset = None if sayfa == 1 else ((sayfa - 1) * 20)
                kwargs['offset'] = offset
                url = self.filtreli_url_olustur(kategori, base_url, **kwargs)
                
                print(f"\n[Sayfa {sayfa}] {'İlk sayfa' if sayfa == 1 else f'(offset={offset})'} taranıyor...")
                print(f"[Debug] URL: {url}")
                
                self.sayfa_verilerini_cek(url)
                toplam_ilan += self.sayfa_ilan_sayisi
                
                # Her sayfa sonrası verileri kaydet
                print(f"\n[Kayıt] Veriler {dosya_adi} dosyasına kaydediliyor...")
                with open(dosya_adi, 'w', encoding='utf-8') as f:
                    json.dump(self.ilanlar, f, ensure_ascii=False, indent=2)
                print(f"[Özet] Toplam ilan sayısı: {toplam_ilan}")
                
                # Sonraki sayfaya geç
                sayfa += 1
                
        except KeyboardInterrupt:
            print("\n\n[Bilgi] Kullanıcı tarafından durduruldu!")
            print(f"[Özet] Toplam {len(self.ilanlar)} ilan başarıyla kaydedildi")
            print(f"[Bilgi] Dosya konumu: {dosya_adi}")
            
        finally:
            self.tarayici_kapat()

def kullanici_arayuzu():
    """Kullanıcı arayüzü ile kategori ve filtre seçimi"""
    scraper = SahibindenScraper(headless=False)
    
    print("\nSahibinden.com Veri Çekme Aracı")
    print("=" * 50)
    
    # Kategori seçimi
    print("\nKategori Seçimi:")
    kategori_listesi = list(scraper.kategoriler.keys())
    for i, kategori in enumerate(kategori_listesi):
        print(f"{i+1}. {kategori}")
    kategori_secim = int(input("\nKategori seçiniz (1-2): "))
    secilen_kategori = kategori_listesi[kategori_secim-1]
    
    # Seçilen kategoriye göre filtre seçeneklerini göster
    if secilen_kategori == "Cep Telefonu":
        # Cep telefonu filtreleri
        # Durum seçimi
        print("\nDurum Seçimi:")
        durum_listesi = list(scraper.durumlar.keys())
        for i, durum in enumerate(durum_listesi):
            print(f"{i}. {durum}")
        durum_secim = int(input("\nDurum seçiniz (0-2): "))
        secilen_durum = scraper.durumlar[durum_listesi[durum_secim]] if durum_secim > 0 else None
        
        # Şehir seçimi
        print("\nŞehir Seçimi:")
        print("0. Tüm Şehirler")
        sehir_listesi = list(scraper.sehirler.keys())
        for i, sehir in enumerate(sehir_listesi, 1):
            print(f"{i}. {sehir}")
        sehir_secim = int(input("\nŞehir seçiniz (0-81): "))
        secilen_sehir = scraper.sehirler[sehir_listesi[sehir_secim-1]] if sehir_secim > 0 else None
        
        # Marka seçimi
        print("\nMarka Seçimi:")
        print("0. Tüm Markalar")
        marka_listesi = list(scraper.markalar.keys())
        for i, marka in enumerate(marka_listesi, 1):
            print(f"{i}. {marka}")
        marka_secim = int(input("\nMarka seçiniz (0-16): "))
        secilen_marka = scraper.markalar[marka_listesi[marka_secim-1]] if marka_secim > 0 else None
        
        # RAM seçimi
        print("\nRAM Seçimi:")
        print("0. Tüm RAM Seçenekleri")
        ram_listesi = list(scraper.ram_secenekleri.keys())
        for i, ram in enumerate(ram_listesi, 1):
            print(f"{i}. {ram}")
        ram_secim = int(input("\nRAM seçiniz (0-8): "))
        secilen_ram = scraper.ram_secenekleri[ram_listesi[ram_secim-1]] if ram_secim > 0 else None
        
        # Renk seçimi
        print("\nRenk Seçimi:")
        print("0. Tüm Renkler")
        renk_listesi = list(scraper.renkler.keys())
        for i, renk in enumerate(renk_listesi, 1):
            print(f"{i}. {renk}")
        renk_secim = int(input("\nRenk seçiniz (0-21): "))
        secilen_renk = scraper.renkler[renk_listesi[renk_secim-1]] if renk_secim > 0 else None
        
        # Seçilen filtreleri göster
        print("\nSeçilen Filtreler:")
        print(f"Kategori: {secilen_kategori}")
        print(f"Durum: {durum_listesi[durum_secim]}")
        print(f"Şehir: {sehir_listesi[sehir_secim-1] if sehir_secim > 0 else 'Tümü'} {f'(Plaka: {secilen_sehir})' if secilen_sehir else ''}")
        print(f"Marka: {marka_listesi[marka_secim-1] if marka_secim > 0 else 'Tümü'}")
        print(f"RAM: {ram_listesi[ram_secim-1] if ram_secim > 0 else 'Tümü'}")
        print(f"Renk: {renk_listesi[renk_secim-1] if renk_secim > 0 else 'Tümü'}")
        
        # Veri toplama işlemini başlat
        onay = input("\nVeri çekme işlemini başlatmak istiyor musunuz? (E/H): ")
        if onay.lower() == 'e':
            scraper.veri_topla_filtreli(
                kategori=secilen_kategori,
                sehir=secilen_sehir,
                marka=secilen_marka,
                ram=secilen_ram,
                renk=secilen_renk,
                durum=secilen_durum
            )
        else:
            print("İşlem iptal edildi.")
            
    elif secilen_kategori == "Emlak":  # Emlak kategorisi
        # Ana kategori seçimi (Konut/Daire/Arsa)
        print("\nAna Kategori Seçimi:")
        ana_kategoriler = list(scraper.kategoriler["Emlak"]["alt_kategoriler"].keys())
        for i, ana in enumerate(ana_kategoriler, 1):
            print(f"{i}. {ana}")
        ana_secim = int(input("\nAna kategori seçiniz (1-3): "))
        secilen_ana = ana_kategoriler[ana_secim-1]
        
        # Durum seçimi (Satılık/Kiralık)
        print("\nDurum Seçimi:")
        durumlar = list(scraper.kategoriler["Emlak"]["alt_kategoriler"][secilen_ana]["durumlar"].keys())
        for i, durum in enumerate(durumlar, 1):
            print(f"{i}. {durum}")
        durum_secim = int(input(f"\nDurum seçiniz (1-{len(durumlar)}): "))
        secilen_durum = durumlar[durum_secim-1]
        
        # Şehir seçimi
        print("\nŞehir Seçimi:")
        print("0. Tüm Şehirler")
        sehir_listesi = list(scraper.sehirler.keys())
        for i, sehir in enumerate(sehir_listesi, 1):
            print(f"{i}. {sehir}")
        sehir_secim = int(input("\nŞehir seçiniz (0-81): "))
        secilen_sehir = sehir_listesi[sehir_secim-1] if sehir_secim > 0 else None
        
        # Oda sayısı seçimi (sadece konut ve daire kategorisi için)
        secilen_oda = None
        if secilen_ana in ["Konut", "Daire"]:
            print("\nOda Sayısı Seçimi:")
            print("0. Tüm Oda Sayıları")
            oda_listesi = list(scraper.oda_sayilari.keys())
            for i, oda in enumerate(oda_listesi, 1):
                print(f"{i}. {oda}")
            oda_secim = int(input("\nOda sayısı seçiniz (0-5): "))
            secilen_oda = scraper.oda_sayilari[oda_listesi[oda_secim-1]] if oda_secim > 0 else None
        
        # Isıtma tipi seçimi (sadece konut ve daire kategorisi için)
        secilen_isitma = None
        if secilen_ana in ["Konut", "Daire"]:
            print("\nIsıtma Tipi Seçimi:")
            print("0. Tüm Isıtma Tipleri")
            isitma_listesi = list(scraper.isitma_tipleri.keys())
            for i, isitma in enumerate(isitma_listesi, 1):
                print(f"{i}. {isitma}")
            isitma_secim = int(input("\nIsıtma tipi seçiniz (0-5): "))
            secilen_isitma = scraper.isitma_tipleri[isitma_listesi[isitma_secim-1]] if isitma_secim > 0 else None
        
        # Seçilen filtreleri göster
        print("\nSeçilen Filtreler:")
        print(f"Kategori: {secilen_kategori}")
        print(f"Ana Kategori: {secilen_ana}")
        print(f"Durum: {secilen_durum}")
        print(f"Şehir: {sehir_listesi[sehir_secim-1] if sehir_secim > 0 else 'Tümü'}")
        if secilen_ana in ["Konut", "Daire"]:
            print(f"Oda Sayısı: {oda_listesi[oda_secim-1] if oda_secim > 0 else 'Tümü'}")
            print(f"Isıtma Tipi: {isitma_listesi[isitma_secim-1] if isitma_secim > 0 else 'Tümü'}")
        
        # Veri toplama işlemini başlat
        onay = input("\nVeri çekme işlemini başlatmak istiyor musunuz? (E/H): ")
        if onay.lower() == 'e':
            scraper.veri_topla_filtreli(
                kategori=secilen_kategori,
                ana_kategori=secilen_ana,
                durum=secilen_durum,
                sehir=secilen_sehir,
                oda_sayisi=secilen_oda,
                isitma_tipi=secilen_isitma
            )
        else:
            print("İşlem iptal edildi.")
    else:
        print("İşlem iptal edildi.")

if __name__ == "__main__":
    kullanici_arayuzu() 