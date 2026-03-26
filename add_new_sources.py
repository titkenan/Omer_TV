#!/usr/bin/env python3
"""
Omer TV - Kanal Listesi Güncelleyici
CanliTV + Harici M3U kaynaklarını mevcut listeye ekler
"""

import json
import requests
import re
from datetime import datetime
import os

def parse_m3u(m3u_content):
    """M3U içeriğini parse et"""
    channels = []
    lines = m3u_content.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('#EXTINF'):
            # Bilgileri çıkar
            name = line.split(',')[-1].strip() if ',' in line else 'Unknown'
            
            logo = ''
            category = 'Genel'
            tvg_id = ''
            
            # tvg-logo
            logo_match = re.search(r'tvg-logo="([^"]+)"', line)
            if logo_match:
                logo = logo_match.group(1)
            
            # group-title
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match:
                category = group_match.group(1)
            
            # tvg-id
            id_match = re.search(r'tvg-id="([^"]+)"', line)
            if id_match:
                tvg_id = id_match.group(1)
            
            # Sonraki satır URL
            i += 1
            if i < len(lines):
                url = lines[i].strip()
                
                if url and not url.startswith('#'):
                    channels.append({
                        'name': name,
                        'url': url,
                        'category': category,
                        'logo': logo,
                        'tvg_id': tvg_id
                    })
        
        i += 1
    
    return channels

def load_existing_channels():
    """Mevcut channels.m3u dosyasını yükle"""
    try:
        with open('channels.m3u', 'r', encoding='utf-8') as f:
            content = f.read()
        
        channels = parse_m3u(content)
        print(f"✅ Mevcut kanallar: {len(channels)}")
        return channels
    except FileNotFoundError:
        print("⚠️ channels.m3u bulunamadı")
        return []

def load_canlitv_channels():
    """CanliTV scraper sonuçlarını yükle"""
    paths = [
        'data/canlitv_channels.json',
        '../data/canlitv_channels.json',
        'canlitv_channels.json'
    ]
    
    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                channels = json.load(f)
            print(f"✅ CanliTV kanalları: {len(channels)} ({path})")
            return channels
        except FileNotFoundError:
            continue
    
    print("⚠️ canlitv_channels.json bulunamadı")
    return []

def load_external_m3u():
    """Harici M3U dosyalarını yükle"""
    sources = [
        "https://raw.githubusercontent.com/impresents/my-iptv-list/refs/heads/main/trlist.m3u",
        "https://iptv-org.github.io/iptv/countries/tr.m3u"
    ]
    
    all_channels = []
    
    for url in sources:
        try:
            print(f"📥 İndiriliyor: {url.split('/')[-2]}/{url.split('/')[-1]}")
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            channels = parse_m3u(response.text)
            all_channels.extend(channels)
            print(f"   ✅ {len(channels)} kanal")
        except Exception as e:
            print(f"   ❌ Hata: {str(e)[:50]}")
    
    return all_channels

def merge_and_deduplicate(channel_lists):
    """Birleştir ve tekrarları temizle"""
    
    all_channels = []
    for channels in channel_lists:
        all_channels.extend(channels)
    
    print(f"\n🔄 Toplam {len(all_channels)} kanal birleştiriliyor...")
    
    # URL ve isim bazlı deduplikasyon
    unique_channels = []
    seen_urls = set()
    seen_names = set()
    
    for ch in all_channels:
        url = ch.get('url', '').strip()
        name = ch.get('name', '').lower().strip()
        
        # Geçersiz kontroller
        if not url or not name:
            continue
        
        if not url.startswith('http'):
            continue
        
        # Tekrar kontrolü
        if url in seen_urls:
            continue
        
        # İsim benzerliği kontrolü (çok benzer isimler)
        name_simple = re.sub(r'[^a-z0-9]', '', name)
        if name_simple in seen_names:
            continue
        
        unique_channels.append(ch)
        seen_urls.add(url)
        seen_names.add(name_simple)
    
    print(f"✅ {len(unique_channels)} benzersiz kanal")
    return unique_channels

def save_m3u(channels, filename='channels.m3u'):
    """M3U formatında kaydet"""
    
    # Kategoriye göre sırala
    channels_sorted = sorted(channels, key=lambda x: (
        x.get('category', 'Genel'), 
        x.get('name', '')
    ))
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Header
        f.write('#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n')
        f.write(f'# Omer TV - Updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Total Channels: {len(channels)}\n\n')
        
        # Kanallar
        for ch in channels_sorted:
            name = ch.get('name', 'Unknown')
            url = ch.get('url', '')
            logo = ch.get('logo', '')
            category = ch.get('category', 'Genel')
            tvg_id = ch.get('tvg_id', name.replace(' ', '_').lower())
            
            f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{category}",{name}\n')
            f.write(f'{url}\n')
    
    print(f"✅ {filename} kaydedildi ({len(channels)} kanal)")

def save_json(channels):
    """JSON formatında da kaydet"""
    os.makedirs('data', exist_ok=True)
    
    with open('data/all_channels.json', 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    
    print(f"✅ data/all_channels.json kaydedildi")

def update_stats(channels):
    """stats.json güncelle"""
    
    categories = {}
    sources = {}
    
    for ch in channels:
        cat = ch.get('category', 'Genel')
        categories[cat] = categories.get(cat, 0) + 1
        
        src = ch.get('source', 'unknown')
        sources[src] = sources.get(src, 0) + 1
    
    stats = {
        'last_update': datetime.utcnow().isoformat(),
        'total_channels': len(channels),
        'categories': dict(sorted(categories.items(), key=lambda x: -x[1])),
        'sources': sources
    }
    
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ stats.json güncellendi")

def print_summary(channels):
    """Özet bilgi"""
    
    categories = {}
    for ch in channels:
        cat = ch.get('category', 'Genel')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n" + "="*60)
    print("📊 ÖZET İSTATİSTİKLER")
    print("="*60)
    print(f"Toplam Kanal: {len(channels)}\n")
    print("Kategoriler:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        bar = "█" * (count // 5)
        print(f"  {cat:20s}: {count:4d} {bar}")
    print("="*60)

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║     Omer TV - Kanal Listesi Güncelleyici        ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    # 1. Mevcut kanalları yükle
    print("📂 Mevcut kanallar yükleniyor...")
    existing = load_existing_channels()
    
    # 2. CanliTV kanallarını yükle
    print("\n📺 CanliTV kanalları yükleniyor...")
    canlitv = load_canlitv_channels()
    
    # 3. Harici M3U dosyalarını yükle
    print("\n🌐 Harici M3U dosyaları yükleniyor...")
    external = load_external_m3u()
    
    # 4. Birleştir
    all_channels = merge_and_deduplicate([existing, canlitv, external])
    
    # 5. Kaydet
    print("\n💾 Dosyalar kaydediliyor...")
    save_m3u(all_channels)
    save_json(all_channels)
    update_stats(all_channels)
    
    # 6. Özet
    print_summary(all_channels)
    
    print("\n✅ İşlem tamamlandı!\n")

if __name__ == "__main__":
    main()
