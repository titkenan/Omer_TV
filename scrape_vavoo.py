#!/usr/bin/env python3
"""
Vavoo TR Scraper - Gelişmiş Versiyon
Kanal isimlerini ve URL'leri doğru eşleştirir
"""

import requests
import re
import json
from datetime import datetime
import os
from bs4 import BeautifulSoup

def scrape_vavoo():
    """Vavoo TR scraper - VPN gerekli"""
    
    url = "https://rideordie.serv00.net/iptv/vavoo/tr.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9',
    }
    
    print(f"📥 {url}")
    print("⚠️ Türkiye VPN gerekli!\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code}")
            return None
        
        html = response.text
        print(f"✅ Sayfa alındı ({len(html):,} byte)\n")
        
        # Debug kaydet
        with open('debug_vavoo.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("💾 debug_vavoo.html kaydedildi")
        
        return html
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def parse_channels_advanced(html):
    """HTML'den kanal ismi + URL'leri akıllıca çıkar"""
    
    channels = []
    
    # BeautifulSoup ile parse
    soup = BeautifulSoup(html, 'html.parser')
    
    # YÖNTEM 1: Table yapısı (genelde TV listeleri table'da)
    tables = soup.find_all('table')
    print(f"📊 {len(tables)} tablo bulundu")
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            
            if len(cells) >= 2:
                # İlk cell genelde isim, ikincisi link
                name_cell = cells[0].get_text(strip=True)
                
                # M3U8 linki bul
                links = row.find_all('a', href=re.compile(r'\.m3u8'))
                if links:
                    url = links[0]['href']
                    
                    if name_cell and url:
                        channels.append({
                            'name': clean_channel_name(name_cell),
                            'url': url,
                            'category': guess_category(name_cell),
                            'logo': '',
                            'source': 'vavoo'
                        })
    
    # YÖNTEM 2: Div/Span yapısı
    if len(channels) < 10:
        print("🔄 Alternatif parse yöntemi deneniyor...")
        
        # M3U8 linklerini bul
        m3u8_pattern = r'(https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)'
        m3u8_links = re.findall(m3u8_pattern, html)
        
        # Her link için önceki metni kanal ismi olarak al
        for m3u8_url in m3u8_links:
            # M3U8 linkinden önceki 200 karakteri al
            pos = html.find(m3u8_url)
            if pos > 200:
                prev_text = html[pos-200:pos]
                
                # HTML tag'lerini temizle
                clean_text = re.sub(r'<[^>]+>', ' ', prev_text)
                
                # Kelimeleri al (en son kelime genelde kanal ismi)
                words = clean_text.split()
                if words:
                    # Son 1-3 kelimeyi al
                    name = ' '.join(words[-3:]).strip()
                    
                    # Sayı değilse ve 3 karakterden uzunsa
                    if len(name) > 2 and not name.isdigit():
                        channels.append({
                            'name': clean_channel_name(name),
                            'url': m3u8_url,
                            'category': guess_category(name),
                            'logo': '',
                            'source': 'vavoo'
                        })
    
    # YÖNTEM 3: JSON içinde olabilir (bazı siteler JS ile yükler)
    if len(channels) < 10:
        print("🔄 JSON pattern aranıyor...")
        
        json_pattern = r'\{[^}]*"name"\s*:\s*"([^"]+)"[^}]*"url"\s*:\s*"([^"]+\.m3u8[^"]*)"[^}]*\}'
        json_matches = re.findall(json_pattern, html, re.IGNORECASE)
        
        for name, url in json_matches:
            channels.append({
                'name': clean_channel_name(name),
                'url': url,
                'category': guess_category(name),
                'logo': '',
                'source': 'vavoo'
            })
    
    return channels

def clean_channel_name(name):
    """Kanal ismini temizle"""
    # HTML entities
    name = name.replace('&nbsp;', ' ')
    name = name.replace('&amp;', '&')
    
    # Fazla boşlukları temizle
    name = ' '.join(name.split())
    
    # Özel karakterleri temizle
    name = re.sub(r'[^\w\s\-\.&+]', '', name)
    
    return name.strip()

def guess_category(name):
    """Kanal isminden kategori tahmin et"""
    name_lower = name.lower()
    
    if any(x in name_lower for x in ['haber', 'news', 'cnn', 'ntv', 'tgrt']):
        return 'Haber'
    elif any(x in name_lower for x in ['spor', 'sport', 'bein', 'gs', 'fb']):
        return 'Spor'
    elif any(x in name_lower for x in ['cocuk', 'çocuk', 'cartoon', 'kids']):
        return 'Çocuk'
    elif any(x in name_lower for x in ['film', 'sinema', 'movie']):
        return 'Film'
    elif any(x in name_lower for x in ['müzik', 'music', 'kral']):
        return 'Müzik'
    else:
        return 'Genel'

def create_m3u(channels, filename='vavoo_channels.m3u'):
    """M3U dosyası oluştur"""
    
    # Duplikasyonları temizle
    seen_urls = set()
    unique_channels = []
    
    for ch in channels:
        if ch['url'] not in seen_urls:
            unique_channels.append(ch)
            seen_urls.add(ch['url'])
    
    # Kategoriye göre sırala
    unique_channels.sort(key=lambda x: (x['category'], x['name']))
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        f.write(f'# Vavoo TR - Updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Total: {len(unique_channels)} channels\n\n')
        
        current_category = None
        for ch in unique_channels:
            # Kategori başlığı
            if ch['category'] != current_category:
                f.write(f'\n### {ch["category"].upper()} ###\n\n')
                current_category = ch['category']
            
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["category"]}",{ch["name"]}\n')
            f.write(f'{ch["url"]}\n')
    
    print(f"✅ {filename} oluşturuldu ({len(unique_channels)} kanal)")
    return unique_channels

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║   Vavoo TR Scraper - Gelişmiş Versiyon          ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    # 1. Scrape
    html = scrape_vavoo()
    if not html:
        return
    
    # 2. Parse
    print("\n🔍 Kanallar parse ediliyor...")
    channels = parse_channels_advanced(html)
    
    if not channels:
        print("❌ Hiç kanal bulunamadı!")
        print("💡 debug_vavoo.html dosyasını kontrol et")
        return
    
    print(f"📺 {len(channels)} kanal bulundu\n")
    
    # İlk 10 kanalı göster
    print("📋 İlk 10 kanal:")
    for i, ch in enumerate(channels[:10], 1):
        print(f"  {i:2d}. {ch['name'][:40]:40s} [{ch['category']}]")
    
    # 3. Kaydet
    print(f"\n💾 Kaydediliyor...")
    
    os.makedirs('data', exist_ok=True)
    
    # M3U
    unique_channels = create_m3u(channels)
    
    # JSON
    with open('data/vavoo_channels.json', 'w', encoding='utf-8') as f:
        json.dump(unique_channels, f, indent=2, ensure_ascii=False)
    print(f"✅ data/vavoo_channels.json kaydedildi")
    
    # Kategori istatistikleri
    categories = {}
    for ch in unique_channels:
        cat = ch['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Kategoriler:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"   {cat:15s}: {count:3d}")

if __name__ == "__main__":
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("⚠️ BeautifulSoup gerekli!")
        print("Kur: pip install beautifulsoup4")
        exit(1)
    
    main()
