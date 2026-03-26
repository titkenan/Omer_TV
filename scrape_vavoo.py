#!/usr/bin/env python3
"""
Vavoo TR Scraper - API Tabanlı
Kanal isimlerini Vavoo API'den çeker
"""

import requests
import re
import json
from datetime import datetime
import os
import time

def get_vavoo_api_data():
    """Vavoo API'den kanal listesini al"""
    
    api_url = "https://rideordie.serv00.net/iptv/vavoo/tr.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/html',
        'Accept-Language': 'tr-TR,tr;q=0.9',
    }
    
    print(f"📥 {api_url}")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code}")
            return None
        
        html = response.text
        print(f"✅ Sayfa alındı ({len(html):,} byte)")
        
        # HTML kaydet
        with open('debug_vavoo.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        return html
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def get_channel_name_from_id(channel_id):
    """Channel ID'den isim al (Vavoo API)"""
    
    try:
        # Vavoo metadata endpoint'i (varsa)
        api_url = f"https://www.vavoo.to/api/channel/{channel_id}"
        
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('name', f'Kanal {channel_id}')
    except:
        pass
    
    return f'Kanal {channel_id}'

def parse_vavoo_html_advanced(html):
    """HTML'den kanal ID + isim çıkar"""
    
    channels = []
    
    # Pattern 1: M3U8 URL'leri bul
    m3u8_pattern = r'https://www\.vavoo\.to/play/(\d+)/index\.m3u8'
    channel_ids = re.findall(m3u8_pattern, html)
    
    print(f"🔍 {len(channel_ids)} kanal ID bulundu")
    
    # Pattern 2: HTML'de kanal isimlerini bul
    # Örnek yapılar:
    patterns = [
        # <td>Kanal İsmi</td>...<a href="...ID...">
        r'<td[^>]*>([^<]+)</td[^>]*>.*?/play/(\d+)/index\.m3u8',
        
        # <div class="name">Kanal</div>...<a href="...ID...">
        r'<div[^>]*class="[^"]*name[^"]*"[^>]*>([^<]+)</div>.*?/play/(\d+)/index\.m3u8',
        
        # <span>Kanal</span>...<a href="...ID...">
        r'<span[^>]*>([^<]+)</span>.*?/play/(\d+)/index\.m3u8',
        
        # JSON format: "name":"Kanal","id":"123"
        r'"(?:name|title)":\s*"([^"]+)"[^}]*"(?:id|channel)":\s*"?(\d+)"?',
    ]
    
    name_id_map = {}
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        print(f"   Pattern buldu: {len(matches)} eşleşme")
        
        for name, ch_id in matches:
            name = clean_name(name)
            if len(name) > 2 and not name.isdigit():
                name_id_map[ch_id] = name
    
    print(f"📋 {len(name_id_map)} kanal ismi eşleşti")
    
    # Eşleştir
    for ch_id in set(channel_ids):
        url = f"https://www.vavoo.to/play/{ch_id}/index.m3u8"
        
        # İsmi bul
        name = name_id_map.get(ch_id, f'Kanal {ch_id}')
        
        channels.append({
            'name': name,
            'url': url,
            'category': guess_category(name),
            'logo': '',
            'source': 'vavoo',
            'id': ch_id
        })
    
    return channels

def clean_name(name):
    """İsmi temizle"""
    # HTML entities
    name = re.sub(r'&nbsp;?', ' ', name)
    name = re.sub(r'&amp;', '&', name)
    name = re.sub(r'&[a-z]+;', '', name)
    
    # HTML tag'leri
    name = re.sub(r'<[^>]+>', '', name)
    
    # Fazla boşluk
    name = ' '.join(name.split())
    
    # Özel karakterler
    name = re.sub(r'[^\w\s\-\.&+\(\)]', '', name)
    
    return name.strip()

def guess_category(name):
    """Kategori tahmin et"""
    n = name.lower()
    
    if any(x in n for x in ['haber', 'news', 'cnn', 'ntv', 'tgrt', 'ulke', 'halk', 'tele1']):
        return 'Haber'
    elif any(x in n for x in ['spor', 'sport', 'bein', 'gs tv', 'fb tv', 'tjk']):
        return 'Spor'
    elif any(x in n for x in ['cocuk', 'çocuk', 'cartoon', 'kids', 'minika', 'disney']):
        return 'Çocuk'
    elif any(x in n for x in ['film', 'sinema', 'movie']):
        return 'Film'
    elif any(x in n for x in ['müzik', 'music', 'kral', 'power']):
        return 'Müzik'
    elif any(x in n for x in ['belgesel', 'documentary', 'nat geo', 'discovery']):
        return 'Belgesel'
    else:
        return 'Genel'

def create_m3u(channels, filename='vavoo_channels.m3u'):
    """M3U oluştur"""
    
    # Kategoriye göre sırala
    channels.sort(key=lambda x: (x['category'], x['name']))
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        f.write(f'# Vavoo TR - {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Total: {len(channels)} channels\n\n')
        
        current_cat = None
        for ch in channels:
            if ch['category'] != current_cat:
                f.write(f'\n### {ch["category"].upper()} ###\n\n')
                current_cat = ch['category']
            
            f.write(f'#EXTINF:-1 tvg-id="{ch["id"]}" group-title="{ch["category"]}",{ch["name"]}\n')
            f.write(f'{ch["url"]}\n')
    
    print(f"✅ {filename} ({len(channels)} kanal)")

def main():
    print("=" * 60)
    print("Vavoo TR Scraper - Gelişmiş İsim Algılama")
    print("=" * 60)
    
    # 1. HTML al
    html = get_vavoo_api_data()
    if not html:
        return
    
    # 2. Parse et
    print("\n🔍 Kanallar parse ediliyor...")
    channels = parse_vavoo_html_advanced(html)
    
    if not channels:
        print("❌ Hiç kanal bulunamadı!")
        return
    
    print(f"\n📺 {len(channels)} kanal bulundu")
    
    # İlk 20'yi göster
    print("\n📋 İlk 20 kanal:")
    for i, ch in enumerate(channels[:20], 1):
        print(f"  {i:2d}. {ch['name'][:50]:50s} [{ch['category']}]")
    
    # 3. Kaydet
    print("\n💾 Kaydediliyor...")
    os.makedirs('data', exist_ok=True)
    
    create_m3u(channels)
    
    with open('data/vavoo_channels.json', 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    
    print("✅ data/vavoo_channels.json")
    
    # Stats
    cats = {}
    for ch in channels:
        cats[ch['category']] = cats.get(ch['category'], 0) + 1
    
    print("\n📊 Kategoriler:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"   {cat:15s}: {count:3d}")
    
    print("\n✅ İşlem tamamlandı!")

if __name__ == "__main__":
    main()
