from flask import Flask, request, jsonify
from flask_cors import CORS
from sahibinden_scraper import SahibindenScraper
import threading
import queue
import time
import os
import json

app = Flask(__name__)
CORS(app)

# Aktif scraping işlemlerini takip etmek için
active_jobs = {}
job_results = {}
job_counter = 0

def scraping_worker(job_id, kategori, **kwargs):
    try:
        scraper = SahibindenScraper(headless=True)
        
        # Şehir parametresi yoksa tüm illeri tara
        if 'sehir' not in kwargs and kategori == "Emlak":
            scraper.tum_illeri_tara(kategori=kategori, **kwargs)
        else:
            scraper.veri_topla_filtreli(kategori=kategori, **kwargs)
        
        # Verileri JSON olarak kaydet
        if kategori == "Emlak":
            folder_name = f"Tum{kwargs['ana_kategori']}{kwargs['durum']}"
            if kwargs.get('sehir'):
                os.makedirs(f"JSONLAR/{folder_name}", exist_ok=True)
                file_path = f"JSONLAR/{folder_name}/{kwargs['sehir']}.json"
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(scraper.ilanlar, f, ensure_ascii=False, indent=2)
        elif kategori == "Cep Telefonu":
            # Telefon verileri için klasör yapısı
            folder_name = f"TumTelefonlar/{kwargs['marka']}"
            os.makedirs(f"JSONLAR/{folder_name}", exist_ok=True)
            
            # Dosya adını oluştur: marka_durum_tarih.json
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_name = f"{kwargs['marka'].lower()}_{kwargs.get('durum', 'hepsi')}_{timestamp}.json"
            file_path = f"JSONLAR/{folder_name}/{file_name}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(scraper.ilanlar, f, ensure_ascii=False, indent=2)
            
        job_results[job_id] = {
            "status": "completed",
            "data": scraper.ilanlar,
            "total_items": len(scraper.ilanlar)
        }
    except Exception as e:
        job_results[job_id] = {
            "status": "failed",
            "error": str(e)
        }
    finally:
        if job_id in active_jobs:
            del active_jobs[job_id]

@app.route('/api/scrape/phone', methods=['POST'])
def scrape_phone():
    global job_counter
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    # Parametreleri al
    params = {
        "kategori": "Cep Telefonu",
        "sehir": data.get('sehir'),
        "marka": data.get('marka'),
        "ram": data.get('ram'),
        "renk": data.get('renk'),
        "durum": data.get('durum')
    }
    
    # Yeni job ID oluştur
    job_id = f"job_{job_counter}"
    job_counter += 1
    
    # Scraping işlemini başlat
    thread = threading.Thread(target=scraping_worker, args=(job_id,), kwargs=params)
    thread.start()
    
    active_jobs[job_id] = {
        "start_time": time.time(),
        "status": "running",
        "params": params
    }
    
    return jsonify({
        "job_id": job_id,
        "status": "started",
        "message": "Scraping işlemi başlatıldı"
    })

@app.route('/api/scrape/estate', methods=['POST'])
def scrape_estate():
    global job_counter
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    # Parametreleri al
    params = {
        "kategori": "Emlak",
        "ana_kategori": data.get('ana_kategori'),  # Konut, Daire, Arsa
        "durum": data.get('durum'),  # Satılık, Kiralık
        "oda_sayisi": data.get('oda_sayisi'),
        "isitma_tipi": data.get('isitma_tipi')
    }

    # Eğer tüm_iller seçili değilse şehir parametresini ekle
    if not data.get('tum_iller'):
        params["sehir"] = data.get('sehir')
    
    # Yeni job ID oluştur
    job_id = f"job_{job_counter}"
    job_counter += 1
    
    # Scraping işlemini başlat
    thread = threading.Thread(
        target=scraping_worker, 
        args=(job_id,), 
        kwargs=params
    )
    thread.start()
    
    active_jobs[job_id] = {
        "start_time": time.time(),
        "status": "running",
        "params": params
    }
    
    return jsonify({
        "job_id": job_id,
        "status": "started",
        "message": "Scraping işlemi başlatıldı"
    })

@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    # Aktif işlem kontrolü
    if job_id in active_jobs:
        return jsonify({
            "status": "running",
            "start_time": active_jobs[job_id]["start_time"],
            "params": active_jobs[job_id]["params"]
        })
    
    # Tamamlanmış işlem kontrolü
    if job_id in job_results:
        return jsonify(job_results[job_id])
    
    return jsonify({"error": "Job not found"}), 404

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    return jsonify({
        "active_jobs": active_jobs,
        "completed_jobs": {k: v for k, v in job_results.items() if v["status"] == "completed"},
        "failed_jobs": {k: v for k, v in job_results.items() if v["status"] == "failed"}
    })

@app.route('/api/check-file/<job_id>', methods=['GET'])
def check_file_exists(job_id):
    params = active_jobs.get(job_id, {}).get("params", {})
    
    try:
        if params.get("kategori") == "Emlak":
            folder_name = f"Tum{params['ana_kategori']}{params['durum']}"
            if params.get("sehir"):
                file_path = f"JSONLAR/{folder_name}/{params['sehir']}.json"
                exists = os.path.exists(file_path)
            else:
                folder_path = f"JSONLAR/{folder_name}"
                exists = os.path.exists(folder_path) and len([f for f in os.listdir(folder_path) if f.endswith('.json')]) > 0
        elif params.get("kategori") == "Cep Telefonu":
            folder_path = f"JSONLAR/TumTelefonlar/{params['marka']}"
            exists = os.path.exists(folder_path) and len([f for f in os.listdir(folder_path) if f.endswith('.json')]) > 0
        else:
            exists = job_id in job_results
            
        return jsonify({"exists": exists})
    except Exception:
        return jsonify({"exists": False})

@app.route('/api/download/<job_id>', methods=['GET'])
def download_job_data(job_id):
    params = active_jobs.get(job_id, {}).get("params", {})
    
    try:
        # Emlak kategorisi için JSONLAR klasöründen okuma
        if params.get("kategori") == "Emlak":
            folder_name = f"Tum{params['ana_kategori']}{params['durum']}"
            if params.get("sehir"):  # Tek şehir için
                file_path = f"JSONLAR/{folder_name}/{params['sehir']}.json"
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return jsonify(json.load(f))
            else:  # Tüm iller için tüm dosyaları birleştir
                folder_path = f"JSONLAR/{folder_name}"
                if os.path.exists(folder_path):
                    all_data = []
                    for file_name in os.listdir(folder_path):
                        if file_name.endswith('.json'):
                            with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
                                all_data.extend(json.load(f))
                    return jsonify(all_data)
                    
        # Telefon kategorisi için JSONLAR klasöründen okuma
        elif params.get("kategori") == "Cep Telefonu":
            folder_path = f"JSONLAR/TumTelefonlar/{params['marka']}"
            if os.path.exists(folder_path):
                # En son oluşturulan dosyayı bul
                json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
                if json_files:
                    latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
                    with open(os.path.join(folder_path, latest_file), 'r', encoding='utf-8') as f:
                        return jsonify(json.load(f))
                        
        # Diğer durumlar için normal veri dönüşü
        if job_id in job_results:
            return jsonify(job_results[job_id]["data"])
        
    except Exception as e:
        return jsonify({"error": f"Dosya okuma hatası: {str(e)}"}), 500
    
    return jsonify({"error": "Dosya bulunamadı"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 