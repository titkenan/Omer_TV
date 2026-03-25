import json
import requests
from concurrent.futures import ThreadPoolExecutor
import time


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
            channel['status'] = 'failed'
            print(f"❌ {channel['name']:20s} | Status: {response.status_code}")
            return None
    
    except Exception as e:
        channel['status'] = 'error'
        print(f"⚠️ {channel['name']:20s} | Timeout")
        return None


def test_all_channels():
    """Tüm kanalları test et"""
    print("🧪 Kanallar test ediliyor...\n")
    
    # Scraped kanalları yükle
    with open('data/scraped_channels.json', 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    working_channels = []
    
    # Paralel test
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(test_stream, channels)
        working_channels = [r for r in results if r is not None]
    
    # Sonuçları kaydet
    with open('data/working_channels.json', 'w', encoding='utf-8') as f:
        json.dump(working_channels, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ {len(working_channels)}/{len(channels)} kanal çalışıyor")
    
    return working_channels


if __name__ == "__main__":
    test_all_channels()
