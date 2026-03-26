#!/usr/bin/env python3
"""
Vavoo TR Scraper - Sadece Regex (Dependency yok)
"""

import requests
import re
import json
from datetime import datetime
import os

def scrape_vavoo():
    """Vavoo TR'den kanalları çek"""
    
    url = "https://rideordie.serv00.net/iptv/vavoo/tr.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9',
    }
    
    print(f"📥 {url}")
    
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

def parse_channels_regex(html):
    """Regex ile kanal ismi + URL çıkar"""
    
    channels = []
    
    # Pattern 1: <td>Kanal İsmi</td>...<a href="...m3u8">
    pattern1 = r'<td[^>]*>([^<]+)</td[^>]*>.*?href=["\']([^"\']+\.m3u8[^"\']*)["\']'
    matches1 = re.findall(pattern1, html, re.DOTALL | re.IGNORECASE)
    
    print(f"🔍 Pattern 1: {len(matches1)} eşleşme")
    
    for name, url in matches1:
        name = clean_name(name)
        if name and len(name) > 2:
            channels.append({
                'name': name,
                'url': url,
                'category': guess_category(name),
                'logo': '',
                'source': 'vavoo'
            })
    
    # Pattern 2: <span>Kanal</span>...<a href="m3u8">
    if len(channels) < 10:
        pattern2 = r'<(?:span|div)[^>]*>([^<]+)</(?:span|div)>.*?href=["\']([^"\']+\.m3u8[^"\']*)["\']'
        matches2 = re.findall(pattern2, html, re.DOTALL | re.IGNORECASE)
        
        print(f"🔍 Pattern 2: {len(matches2)} eşleşme")
        
        for name, url in matches2:
            name = clean_name(name)
            if name and len(name) > 2:
                channels.append({
                    'name': name,
                    'url': url,
                    'category': guess_category(name),
                    'logo': '',
                    'source': 'vavoo'
                })
    
    # Pattern 3: JSON formatında
    if len(channels) < 10:
        pattern3 = r'"(?:name|title|channel)":\s*"([^"]+)"[^}]*"(?:url|stream|link)":\s*"([^"]+\.m3u8[^"]*)"'
        matches3 = re.findall(pattern3, html, re.IGNORECASE)
        
        print(f"🔍 Pattern 3: {len(matches3)} eşleşme")
        
        for name, url in matches3:
            name = clean_name(name)
            channels.append({
                'name': name,
                'url': url,
                'category': guess_category(name),
                'logo': '',
                'source': 'vavoo'
            })
    
    # Duplikasyonları temizle
    seen = set()
    unique = []
    for ch in channels:
        if ch['url'] not in seen:
            unique.append(ch)
            seen.add(ch['url'])
    
    return unique

def clean_name(name):
    """İsmi temizle"""
    # HTML entities
    name = re.sub(r'&nbsp;?', ' ', name)
    name = re.sub(r'&amp;', '&', name)
    name = re.sub(r'&[a-z]+;', '', name)
    
    # HTML tag'lerini temizle
    name = re.sub(r'<[^>]+>', '', name)
    
    # Fazla boşlukları temizle
    name = ' '.join(name.split())
    
    # Özel karakterleri temizle
    name = re.sub(r'[^\w\s\-\.&+]', '', name)
    
    return name.strip()

def guess_category(name):
    """Kategori tahmin et"""
    n = name.lower()
    
    if any(x in n for x in ['haber', 'news', 'cnn', 'ntv']):
        return 'Haber'
    elif any(x in n for x in ['spor', 'sport', 'bein']):
        return 'Spor'
    elif any(x in n for x in ['cocuk', 'çocuk', 'cartoon']):
        return 'Çocuk'
    elif any(x in n for x in ['film', 'sinema']):
        return 'Film'
    elif any(x in n for x in ['müzik', 'music']):
        return 'Müzik'
    else:
        return 'Genel'

def create_m3u(channels, filename='vavoo_channels.m3u'):
    """M3U oluştur"""
    
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
            
            f.write(f'#EXTINF:-1 group-title="{ch["category"]}",{ch["name"]}\n')
            f.write(f'{ch["url"]}\n')
    
    print(f"✅ {filename} ({len(channels)} kanal)")

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║       Vavoo TR Scraper (Regex Only)             ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    html = scrape_vavoo()
    if not html:
        return
    
    print("\n🔍 Parse ediliyor...")
    channels = parse_channels_regex(html)
    
    if not channels:
        print("\n❌ Hiç kanal bulunamadı!")
        print("💡 debug_vavoo.html dosyasını kontrol et")
        return
    
    print(f"\n📺 {len(channels)} kanal bulundu\n")
    
    # İlk 20'yi göster
    print("📋 İlk 20 kanal:")
    for i, ch in enumerate(channels[:20], 1):
        print(f"  {i:2d}. {ch['name'][:50]:50s} [{ch['category']}]")
    
    # Kaydet
    print("\n💾 Kaydediliyor...")
    os.makedirs('data', exist_ok=True)
    
    create_m3u(channels)
    
    with open('data/vavoo_channels.json', 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    
    print("✅ data/vavoo_channels.json\n")
    
    # Stats
    cats = {}
    for ch in channels:
        cats[ch['category']] = cats.get(ch['category'], 0) + 1
    
    print("📊 Kategoriler:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"   {cat:15s}: {count:3d}")

if __name__ == "__main__":
    main()
