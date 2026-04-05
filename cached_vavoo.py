import requests
import json
from datetime import datetime, timedelta
import os

CACHE_FILE = 'data/cache.json'
CACHE_DURATION = 30  # dakika

def load_cache():
    """Önbellekten yükle"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            
            if datetime.now() - cache_time < timedelta(minutes=CACHE_DURATION):
                return cache['channels']
    return None

def save_cache(channels):
    """Önbelleğe kaydet"""
    cache = {
        'timestamp': datetime.now().isoformat(),
        'channels': channels
    }
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_channels():
    """Önbellekli kanal getir"""
    cached = load_cache()
    if cached:
        print("✅ Önbellekten yüklendi (hızlı!)")
        return cached
    
    print("🔄 Vavoo'dan çekiliyor...")
    # Buraya vavoo_scraper.py'deki get_vavoo_channels() fonksiyonunu kopyala
    
    channels = get_vavoo_channels()
    save_cache(channels)
    return channels
