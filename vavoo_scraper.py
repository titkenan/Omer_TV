#!/usr/bin/env python3
"""
Vavoo Scraper - Cloudflare Worker ile
Stabil ve otomatik güncellenen sistem
"""

import requests
import re
from datetime import datetime
import os

# Cloudflare Worker URL
CLOUDFLARE_WORKER = "https://omer-proxy.mmeindl06.workers.dev"

# Hedef URL
VAVOO_SOURCE = "https://rideordie.serv00.net/iptv/vavoo/tr.php"

def fetch_via_worker(url):
    """Cloudflare Worker üzerinden fetch"""
    
    worker_url = f"{CLOUDFLARE_WORKER}?url={url}"
    
    print(f"📡 Cloudflare Worker üzerinden çekiliyor...")
    print(f"   Worker: {CLOUDFLARE_WORKER}")
    print(f"   Hedef: {url}")
    
    try:
        response = requests.get(worker_url, timeout=30)
        
        if response.status_code == 200:
            print(f"   ✅ Başarılı! ({len(response.text):,} byte)")
            return response.text
        else:
            print(f"   ❌ HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"   ❌ Hata: {e}")
        return None

def parse_vavoo_html(html):
    """HTML'den kanalları çıkar"""
    
    # M3U pattern
    pattern = r'#EXTINF:-1 tvg-name="([^"]+)"[^\n]*\n(https://[^\n]+)'
    matches = re.findall(pattern, html)
    
    print(f"\n🔍 {len(matches)} kanal bulundu")
    
    channels = []
    
    for name, url in matches:
        name = name.strip()
        
        # Kategori belirle
        category = auto_categorize(name)
        
        channels.append({
            'name': name,
            'url': url,
            'category': category
        })
    
    return channels

def auto_categorize(name):
    """Otomatik kategori belirle"""
    n = name.lower()
    
    # Ulusal
    if any(x in n for x in ['trt 1', 'trt1', 'show', 'star', 'atv', 'kanal d', 'kanald', 'tv8', 'tv 8', 'kanal 7', 'kanal7', 'fox', 'now', 'beyaz', 'teve', '360', 'a2', 'euro']):
        return 'Ulusal'
    
    # Haber
    elif any(x in n for x in ['haber', 'cnn', 'ntv', 'tgrt', '24', 'ulke', 'sozcu', 'tv100', 'tvnet', 'ekol', 'lider']):
        return 'Haber'
    
    # Spor
    elif any(x in n for x in ['spor', 'sport', 'bein', 's sport', 'tabii', 'exxen', 'tivibu', 'eurosport', 'nba', 'idman']):
        return 'Spor'
    
    # Sinema
    elif any(x in n for x in ['sinema', 'cinema', 'film', 'movie', 'box', 'fix', 'sinemax']):
        return 'Sinema'
    
    # Dizi
    elif any(x in n for x in ['dizi', 'series', 'epic']):
        return 'Dizi'
    
    # Belgesel
    elif any(x in n for x in ['belgesel', 'nat geo', 'national', 'discovery', 'dmax', 'bbc', 'tlc', 'history', 'viasat']):
        return 'Belgesel'
    
    # Çocuk
    elif any(x in n for x in ['cocuk', 'çocuk', 'minika', 'cartoon', 'disney', 'baby', 'nick', 'boomerang', 'caillou']):
        return 'Çocuk'
    
    # Müzik
    elif any(x in n for x in ['muzik', 'müzik', 'music', 'kral', 'power', 'dream', 'number']):
        return 'Müzik'
    
    else:
        return 'Genel'

def create_m3u(channels):
    """M3U dosyası oluştur"""
    
    # Kategorilere ayır
    categories = {}
    for ch in channels:
        cat = ch['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ch)
    
    # İstatistik
    print("\n📊 Kategoriler:")
    total = 0
    for cat in sorted(categories.keys()):
        count = len(categories[cat])
        print(f"   {cat:15s}: {count:3d} kanal")
        total += count
    
    # M3U içeriği
    content = '#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n'
    content += f'# ÖMER TV - Vavoo Premium\n'
    content += f'# Güncelleme: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n'
    content += f'# Toplam: {total} kanal\n'
    content += f'# Kaynak: Vavoo (via Cloudflare Worker)\n\n'
    
    # Kategori sırası
    order = ['Ulusal', 'Haber', 'Spor', 'Sinema', 'Dizi', 'Belgesel', 'Çocuk', 'Müzik', 'Genel']
    
    for cat in order:
        if cat in categories:
            content += f'\n#########################################\n'
            content += f'# {cat.upper()} ({len(categories[cat])} kanal)\n'
            content += f'#########################################\n\n'
            
            for ch in sorted(categories[cat], key=lambda x: x['name']):
                content += f'#EXTINF:-1 group-title="{cat}",{ch["name"]}\n'
                content += f'{ch["url"]}\n'
    
    # Kaydet
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ channels.m3u oluşturuldu ({total} kanal)")

def main():
    print("=" * 60)
    print("VAVOO SCRAPER - Cloudflare Worker Edition")
    print("=" * 60)
    
    # 1. HTML çek
    html = fetch_via_worker(VAVOO_SOURCE)
    
    if not html:
        print("\n❌ HTML çekilemedi! Worker'ı kontrol et.")
        return
    
    # Debug kaydet
    with open('debug_vavoo.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("💾 debug_vavoo.html kaydedildi")
    
    # 2. Parse et
    channels = parse_vavoo_html(html)
    
    if not channels:
        print("\n❌ Hiç kanal bulunamadı!")
        return
    
    # 3. M3U oluştur
    create_m3u(channels)
    
    print("\n🎉 İşlem tamamlandı!")
    print(f"🔗 https://raw.githubusercontent.com/titkenan/Omer_TV/main/channels.m3u")

if __name__ == "__main__":
    main()
