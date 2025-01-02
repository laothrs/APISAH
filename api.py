from flask import Flask, request, jsonify
from flask_cors import CORS
from sahibinden_scraper import SahibindenScraper
import threading
import queue
import time

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 