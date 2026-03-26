#!/usr/bin/env python3
# Dosya: add_new_sources.py
"""
Mevcut Omer_TV projesine yeni kaynakları ekle
- CanliTV.com scraper sonuçları
- GitHub M3U dosyaları
"""

import json
import requests
import re
from datetime import datetime

def parse_m3u(m3u_content):
    """M3U parse et"""
    channels = []
    lines = m3u_content.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('#EXTINF'):
            name = line.split(',')[-1].strip() if ',' in line else 'Unknown'
            
            logo = ''
            category = 'Genel'
            
            logo_match = re.search(r'tvg-logo="([^"]+)"', line)
            if logo_match:
                logo = logo_match.group(1)
            
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match:
                category = group_match.group(1)
            
            i += 1
            if i < len(lines):
                url = lines[i].strip()
                
                if url and not url.startswith('#'):
                    channels.append({
                        'name': name,
                        'url': url,
                        'category': category,
                        'logo': logo
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
        print("⚠️ channels.m3u bulunamadı, yeni dosya oluşturulacak")
        return []

def load_canlitv_channels():
    """CanliTV scraper sonuçlarını yükle"""
    try:
        with open('data/canlitv_channels.json', 'r', encoding='utf-8') as f:
            channels = json.load(f)
        print(f"✅ CanliTV kanalları: {len(channels)}")
        return channels
    except FileNotFoundError:
        print("⚠️ canlitv_channels.json bulunamadı")
        return []

def load_external_m3u():
    """Harici M3U dosyalarını yükle"""
    external_sources = [
        "https://raw.githubusercontent.com/impresents/my-iptv-list/refs/heads/main/trlist.m3u"
    ]
    
    all_channels = []
    
    for url in external_sources:
        try:
            print(f"📥 İndiriliyor: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            channels = parse_m3u(response.text)
            all_channels.extend(channels)
            print(f"   ✅ {len(channels)} kanal")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
    
    return all_channels

def merge_and_deduplicate(channel_lists):
    """Tüm kanal listelerini birleştir ve tekrarları temizle"""
    
    all_channels = []
    for channels in channel_lists:
        all_channels.extend(channels)
    
    # URL bazlı deduplikasyon
    unique_channels = []
    seen_urls = set()
    seen_names = set()
    
    for ch in all_channels:
        url = ch.get('url', '')
        name = ch.get('name', '').lower().strip()
        
        # URL veya isim tekrarı varsa atla
        if url in seen_urls or name in seen_names:
            continue
        
        # Geçersiz URL kontrolü
        if not url or not url.startswith('http'):
            continue
        
        unique_channels.append(ch)
        seen_urls.add(url)
        seen_names.add(name)
    
    return unique_channels

def save_m3u(channels, filename='channels.m3u'):
    """M3U formatında kaydet"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n')
        f.write(f'# Omer TV - Updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Total Channels: {len(channels)}\n\n')
        
        # Kategoriye göre sırala
        channels_sorted = sorted(channels, key=lambda x: (x.get('category', 'Genel'), x.get('name', '')))
        
        for ch in channels_sorted:
            name = ch.get('name', 'Unknown')
            url = ch.get('url', '')
            logo = ch.get('logo', '')
            category = ch.get('category', 'Genel')
            
            # TVG bilgileri
            tvg_name = name.replace(' ', '_')
            tvg_id = tvg_name.lower()
            
            f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{logo}" group-title="{category}",{name}\n')
            f.write(f'{url}\n')
    
    print(f"\n✅ {filename} kaydedildi ({len(channels)} kanal)")

def save_json(channels, filename='data/all_channels.json'):
    """JSON formatında da kaydet"""
    import os
    os.makedirs('data', exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {filename} kaydedildi")

def update_stats(channels):
    """stats.json güncelle"""
    
    categories = {}
    for ch in channels:
        cat = ch.get('category', 'Genel')
        categories[cat] = categories.get(cat, 0) + 1
    
    stats = {
        'last_update': datetime.now().isoformat(),
        'total_channels': len(channels),
        'categories': categories,
        'sources': ['canlitv.com', 'impresents/my-iptv-list', 'existing']
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
    
    print("\n" + "="*50)
    print("📊 ÖZET İSTATİSTİKLER")
    print("="*50)
    print(f"Toplam Kanal: {len(channels)}")
    print("\nKategoriler:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat:20s}: {count:3d}")
    print("="*50)

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
    
    # 4. Birleştir ve tekrarları temizle
    print("\n🔄 Kanallar birleştiriliyor...")
    all_channels = merge_and_deduplicate([existing, canlitv, external])
    
    print(f"\n✅ Toplam benzersiz kanal: {len(all_channels)}")
    
    # 5. Kaydet
    print("\n💾 Dosyalar kaydediliyor...")
    save_m3u(all_channels)
    save_json(all_channels)
    update_stats(all_channels)
    
    # 6. Özet
    print_summary(all_channels)
    
    print("\n✅ İşlem tamamlandı!")
    print("\n📤 Git ile yüklemek için:")
    print("   git add .")
    print('   git commit -m "Update channels"')
    print("   git push")

if __name__ == "__main__":
    main()