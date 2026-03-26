#!/usr/bin/env python3
"""
Vavoo TR Scraper - GitHub Actions için optimize edilmiş
Türk proxy'ler ile otomatik çalışır
"""

import requests
import re
import json
from datetime import datetime
import time

def get_free_turkish_proxies():
    """Ücretsiz Türk proxy'leri çek"""
    
    proxies = []
    
    # Yöntem 1: ProxyScrape API
    try:
        response = requests.get(
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=TR&ssl=all&anonymity=all',
            timeout=10
        )
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            for line in lines[:10]:  # İlk 10 proxy
                if line and ':' in line:
                    proxies.append({
                        'http': f'http://{line.strip()}',
                        'https': f'http://{line.strip()}'
                    })
    except Exception as e:
        print(f"⚠️ ProxyScrape hatası: {e}")
    
    # Yöntem 2: Proxy-List.download
    try:
        response = requests.get(
            'https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country=TR',
            timeout=10
        )
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            for line in lines[:5]:
                if line and ':' in line:
                    proxies.append({
                        'http': f'http://{line.strip()}',
                        'https': f'http://{line.strip()}'
                    })
    except Exception as e:
        print(f"⚠️ Proxy-List hatası: {e}")
    
    # Manuel yedek proxy'ler (genelde çalışanlar)
    backup_proxies = [
        {'http': 'http://88.255.102.120:8080', 'https': 'http://88.255.102.120:8080'},
        {'http': 'http://185.195.254.194:3128', 'https': 'http://185.195.254.194:3128'},
        {'http': 'http://213.159.214.193:3128', 'https': 'http://213.159.214.193:3128'},
    ]
    
    proxies.extend(backup_proxies)
    
    print(f"📋 {len(proxies)} proxy hazır")
    return proxies

def fetch_with_proxy(url, proxies):
    """Proxy'lerle sırayla dene"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/',
    }
    
    # Önce proxy'siz dene (GitHub Actions Türkiye'de olabilir)
    try:
        print("🔄 Direkt bağlantı deneniyor...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200 and len(response.text) > 1000:
            print("✅ Direkt bağlantı başarılı!")
            return response.text
    except Exception as e:
        print(f"❌ Direkt bağlantı başarısız: {e}")
    
    # Proxy'lerle dene
    for i, proxy in enumerate(proxies, 1):
        try:
            print(f"🔄 [{i}/{len(proxies)}] Proxy: {proxy['http'][:30]}...")
            response = requests.get(url, headers=headers, proxies=proxy, timeout=15)
            
            if response.status_code == 200 and len(response.text) > 1000:
                print(f"✅ Başarılı! (Proxy #{i})")
                return response.text
            
        except Exception as e:
            print(f"❌ Hata: {str(e)[:50]}")
            continue
        
        time.sleep(1)  # Rate limiting
    
    return None

def parse_vavoo_html(html):
    """HTML'den M3U8 linklerini ve kanal isimlerini çıkar"""
    
    channels = []
    
    # M3U8 linkleri
    m3u8_pattern = r'(https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)'
    m3u8_links = list(set(re.findall(m3u8_pattern, html, re.IGNORECASE)))
    
    print(f"📺 {len(m3u8_links)} M3U8 linki bulundu")
    
    # Basit kanal isimleri (M3U8 URL'den tahmin et)
    for url in m3u8_links:
        # URL'den kanal ismini tahmin et
        name_guess = url.split('/')[-2] if '/' in url else 'Kanal'
        name_guess = name_guess.replace('-', ' ').replace('_', ' ').title()
        
        # Kategori tahmin et
        url_lower = url.lower()
        if any(x in url_lower for x in ['haber', 'news', 'cnn', 'ntv']):
            category = 'Haber'
        elif any(x in url_lower for x in ['spor', 'sport']):
            category = 'Spor'
        else:
            category = 'Genel'
        
        channels.append({
            'name': name_guess,
            'url': url,
            'category': category,
            'logo': '',
            'source': 'vavoo'
        })
    
    return channels

def create_m3u(channels, filename='vavoo_channels.m3u'):
    """M3U dosyası oluştur"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        f.write(f'# Vavoo TR - Updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Total: {len(channels)} channels\n\n')
        
        for ch in channels:
            name = ch['name']
            url = ch['url']
            logo = ch.get('logo', '')
            category = ch.get('category', 'Genel')
            
            f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{name}\n')
            f.write(f'{url}\n')
    
    print(f"✅ {filename} oluşturuldu ({len(channels)} kanal)")

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║       Vavoo TR Scraper (Auto Proxy)             ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    # 1. Proxy'leri al
    print("📡 Türk proxy'ler alınıyor...")
    proxies = get_free_turkish_proxies()
    
    # 2. Sayfayı çek
    url = "https://rideordie.serv00.net/iptv/vavoo/tr.php"
    print(f"\n📥 {url}\n")
    
    html = fetch_with_proxy(url, proxies)
    
    if not html:
        print("\n❌ Sayfa çekilemedi! Tüm proxy'ler başarısız.")
        return
    
    # 3. Debug kaydet
    with open('debug_vavoo.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("\n💾 debug_vavoo.html kaydedildi")
    
    # 4. Parse et
    print("\n🔍 HTML parse ediliyor...")
    channels = parse_vavoo_html(html)
    
    if not channels:
        print("❌ Hiç kanal bulunamadı!")
        return
    
    # 5. Kaydet
    print(f"\n💾 Kanallar kaydediliyor...")
    
    # JSON
    with open('data/vavoo_channels.json', 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    print(f"✅ data/vavoo_channels.json ({len(channels)} kanal)")
    
    # M3U
    create_m3u(channels, 'vavoo_channels.m3u')
    
    print(f"\n🎉 Toplam {len(channels)} kanal başarıyla çekildi!")

if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    main()
