#!/usr/bin/env python3
"""
Vavoo Scraper - Ücretsiz Türk Proxy ile
"""

import requests
import re
from datetime import datetime
import time

VAVOO_SOURCE = "https://rideordie.serv00.net/iptv/vavoo/tr.php"

def get_turkish_proxies():
    """Güncel Türk proxy'leri çek"""
    
    proxies = []
    
    # API'den Türk proxy listesi al
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=TR&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country=TR",
    ]
    
    for source_url in sources:
        try:
            print(f"📡 Proxy listesi çekiliyor: {source_url.split('/')[2]}")
            response = requests.get(source_url, timeout=10)
            
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines[:5]:  # İlk 5 proxy
                    if line and ':' in line:
                        ip_port = line.strip()
                        proxies.append({
                            'http': f'http://{ip_port}',
                            'https': f'http://{ip_port}'
                        })
                        print(f"   ✅ {ip_port}")
        except Exception as e:
            print(f"   ❌ {e}")
    
    return proxies

def fetch_via_proxy(url, proxies):
    """Proxy'lerle sırayla dene"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9',
    }
    
    for i, proxy in enumerate(proxies, 1):
        try:
            print(f"\n🔄 Proxy {i}/{len(proxies)} deneniyor: {proxy['http'][:30]}...")
            
            response = requests.get(url, headers=headers, proxies=proxy, timeout=15)
            
            if response.status_code == 200 and len(response.text) > 5000:
                print(f"   ✅ BAŞARILI! ({len(response.text):,} byte)")
                return response.text
            else:
                print(f"   ❌ HTTP {response.status_code} veya küçük içerik")
                
        except Exception as e:
            print(f"   ❌ {str(e)[:50]}")
            continue
        
        time.sleep(2)
    
    return None

def parse_vavoo_html(html):
    """HTML'den kanalları çıkar"""
    
    pattern = r'#EXTINF:-1 tvg-name="([^"]+)"[^\n]*\n(https://[^\n]+)'
    matches = re.findall(pattern, html)
    
    print(f"\n🔍 {len(matches)} kanal bulundu")
    
    channels = []
    for name, url in matches:
        name = name.strip()
        category = auto_categorize(name)
        channels.append({'name': name, 'url': url, 'category': category})
    
    return channels

def auto_categorize(name):
    """Kategori belirle"""
    n = name.lower()
    
    if any(x in n for x in ['trt 1', 'show', 'star', 'atv', 'kanal d', 'tv8', 'kanal 7', 'fox', 'beyaz', 'teve', '360', 'a2']):
        return 'Ulusal'
    elif any(x in n for x in ['haber', 'cnn', 'ntv', 'tgrt', 'ulke', 'sozcu']):
        return 'Haber'
    elif any(x in n for x in ['spor', 'sport', 'bein', 'exxen', 'tabii']):
        return 'Spor'
    elif any(x in n for x in ['sinema', 'cinema', 'film']):
        return 'Sinema'
    elif any(x in n for x in ['dizi', 'series']):
        return 'Dizi'
    elif any(x in n for x in ['belgesel', 'nat geo', 'discovery', 'dmax']):
        return 'Belgesel'
    elif any(x in n for x in ['cocuk', 'çocuk', 'minika', 'cartoon']):
        return 'Çocuk'
    elif any(x in n for x in ['muzik', 'müzik', 'kral']):
        return 'Müzik'
    else:
        return 'Genel'

def create_m3u(channels):
    """M3U dosyası oluştur"""
    
    categories = {}
    for ch in channels:
        cat = ch['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ch)
    
    print("\n📊 Kategoriler:")
    for cat in sorted(categories.keys()):
        print(f"   {cat:15s}: {len(categories[cat]):3d}")
    
    content = '#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n'
    content += f'# ÖMER TV - Vavoo\n'
    content += f'# Güncelleme: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n'
    content += f'# Toplam: {len(channels)} kanal\n\n'
    
    order = ['Ulusal', 'Haber', 'Spor', 'Sinema', 'Dizi', 'Belgesel', 'Çocuk', 'Müzik', 'Genel']
    
    for cat in order:
        if cat in categories:
            content += f'\n### {cat.upper()} ({len(categories[cat])} kanal) ###\n\n'
            for ch in sorted(categories[cat], key=lambda x: x['name']):
                content += f'#EXTINF:-1 group-title="{cat}",{ch["name"]}\n'
                content += f'{ch["url"]}\n'
    
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ channels.m3u oluşturuldu ({len(channels)} kanal)")

def main():
    print("=" * 60)
    print("VAVOO SCRAPER - Türk Proxy Edition")
    print("=" * 60)
    
    # 1. Türk proxy'leri al
    print("\n📡 Türk proxy'ler alınıyor...\n")
    proxies = get_turkish_proxies()
    
    if not proxies:
        print("\n❌ Hiç proxy bulunamadı!")
        return
    
    print(f"\n✅ {len(proxies)} proxy hazır")
    
    # 2. HTML çek
    html = fetch_via_proxy(VAVOO_SOURCE, proxies)
    
    if not html:
        print("\n❌ Tüm proxy'ler başarısız oldu!")
        return
    
    # Debug kaydet
    with open('debug_vavoo.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("💾 debug_vavoo.html kaydedildi")
    
    # 3. Parse et
    channels = parse_vavoo_html(html)
    
    if not channels:
        print("❌ Kanal bulunamadı!")
        return
    
    # 4. M3U oluştur
    create_m3u(channels)
    
    print("\n🎉 Başarıyla tamamlandı!")

if __name__ == "__main__":
    main()
