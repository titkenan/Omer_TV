#!/usr/bin/env python3
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os


def test_stream(channel):
    """Tek bir stream'i test et"""
    try:
        start = time.time()
        response = requests.head(
            channel['url'], 
            timeout=10, 
            allow_redirects=True,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        elapsed = (time.time() - start) * 1000
        
        if response.status_code in [200, 302, 301]:
            channel['status'] = 'working'
            channel['response_time'] = round(elapsed, 2)
            print(f"✅ {channel['name']:20s} | {elapsed:.0f}ms")
            return channel
        else:
            print(f"❌ {channel['name']:20s} | Status: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(f"⏱️ {channel['name']:20s} | Timeout")
        return None
    except Exception as e:
        print(f"⚠️ {channel['name']:20s} | Error: {str(e)[:30]}")
        return None


def test_all_channels():
    """Tüm kanalları test et"""
    
    # Dosya kontrolü
    input_file = 'data/scraped_channels.json'
    if not os.path.exists(input_file):
        print(f"❌ Hata: {input_file} bulunamadı!")
        print("💡 Önce scraper.py çalıştırılmalı")
        return []
    
    print(f"📂 Okunan dosya: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    print(f"🧪 {len(channels)} kanal test ediliyor...\n")
    
    working_channels = []
    
    # Paralel test
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(test_stream, channels)
        working_channels = [r for r in results if r is not None]
    
    # Sonuçları kaydet
    os.makedirs('data', exist_ok=True)
    output_file = 'data/working_channels.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(working_channels, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ {len(working_channels)}/{len(channels)} kanal çalışıyor")
    print(f"💾 Kaydedildi: {output_file}")
    print(f"📄 Dosya boyutu: {os.path.getsize(output_file)} byte")
    
    return working_channels


if __name__ == "__main__":
    result = test_all_channels()
    if not result:
        print("\n⚠️ UYARI: Hiç çalışan kanal bulunamadı!")
        exit(1)
