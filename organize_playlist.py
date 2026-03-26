#!/usr/bin/env python3
"""
M3U playlist'ini kategorilere göre düzenle
Önce kategoriler, sonra alfabetik sıra
"""

import json
import re
from datetime import datetime
from collections import defaultdict

# Kategori öncelik sırası
CATEGORY_ORDER = [
    'Ulusal',
    'Haber',
    'Spor',
    'Eğlence',
    'Belgesel',
    'Çocuk',
    'Müzik',
    'Dini',
    'Yerel',
    'Film',
    'Dizi',
    'Genel'
]

def parse_m3u(filename='channels.m3u'):
    """M3U dosyasını parse et"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    channels = []
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('#EXTINF'):
            # Bilgileri çıkar
            name = line.split(',')[-1].strip()
            
            logo = ''
            category = 'Genel'
            tvg_id = ''
            
            logo_match = re.search(r'tvg-logo="([^"]+)"', line)
            if logo_match:
                logo = logo_match.group(1)
            
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match:
                category = group_match.group(1)
            
            id_match = re.search(r'tvg-id="([^"]+)"', line)
            if id_match:
                tvg_id = id_match.group(1)
            
            # URL (sonraki satır)
            i += 1
            if i < len(lines):
                url = lines[i].strip()
                
                if url and url.startswith('http'):
                    channels.append({
                        'name': name,
                        'url': url,
                        'category': normalize_category(category),
                        'logo': logo,
                        'tvg_id': tvg_id or name.replace(' ', '_').lower()
                    })
        
        i += 1
    
    return channels

def normalize_category(cat):
    """Kategori isimlerini standartlaştır"""
    cat_lower = cat.lower()
    
    # Ulusal kanallar
    if any(x in cat_lower for x in ['ulusal', 'genel tv', 'national', 'türkiye']):
        return 'Ulusal'
    
    # Haber
    if any(x in cat_lower for x in ['haber', 'news', 'haberler']):
        return 'Haber'
    
    # Spor
    if any(x in cat_lower for x in ['spor', 'sport', 'sports']):
        return 'Spor'
    
    # Eğlence
    if any(x in cat_lower for x in ['eğlence', 'eglence', 'entertainment']):
        return 'Eğlence'
    
    # Belgesel
    if any(x in cat_lower for x in ['belgesel', 'documentary', 'doğa']):
        return 'Belgesel'
    
    # Çocuk
    if any(x in cat_lower for x in ['çocuk', 'cocuk', 'kids', 'children']):
        return 'Çocuk'
    
    # Müzik
    if any(x in cat_lower for x in ['müzik', 'muzik', 'music']):
        return 'Müzik'
    
    # Dini
    if any(x in cat_lower for x in ['dini', 'din', 'religious']):
        return 'Dini'
    
    # Yerel
    if any(x in cat_lower for x in ['yerel', 'local', 'bölgesel']):
        return 'Yerel'
    
    # Film
    if any(x in cat_lower for x in ['film', 'sinema', 'movie', 'cinema']):
        return 'Film'
    
    # Dizi
    if any(x in cat_lower for x in ['dizi', 'series', 'tv series']):
        return 'Dizi'
    
    return 'Genel'

def categorize_by_name(channels):
    """İsme bakarak kategori tahmin et"""
    for ch in channels:
        name_lower = ch['name'].lower()
        
        # Eğer kategori Genel ise, isme bakarak tahmin et
        if ch['category'] == 'Genel':
            
            # Ulusal kanallar
            if any(x in name_lower for x in [
                'trt 1', 'kanal d', 'show tv', 'star tv', 'atv', 'tv8', 
                'fox', 'kanal 7', 'beyaz tv', 'teve2', 'tv100', 'flash tv'
            ]):
                ch['category'] = 'Ulusal'
            
            # Haber
            elif any(x in name_lower for x in [
                'haber', 'news', 'cnn', 'ntv', 'tgrt', 'halk tv', 'sözcü',
                'tele1', 'ulke tv', 'a haber', '24 tv', 'haber türk'
            ]):
                ch['category'] = 'Haber'
            
            # Spor
            elif any(x in name_lower for x in [
                'spor', 'sport', 'bein', 'trt spor', 'a spor', 'gs tv',
                'fb tv', 'tjk', 'tivibu', 'euro', 'lig', 'maç'
            ]):
                ch['category'] = 'Spor'
            
            # Çocuk
            elif any(x in name_lower for x in [
                'çocuk', 'cocuk', 'minika', 'cartoon', 'kids', 'disney',
                'nick', 'baby', 'penguen'
            ]):
                ch['category'] = 'Çocuk'
            
            # Müzik
            elif any(x in name_lower for x in [
                'müzik', 'muzik', 'music', 'kral', 'power', 'number one',
                'dream', 'mtv'
            ]):
                ch['category'] = 'Müzik'
            
            # Belgesel
            elif any(x in name_lower for x in [
                'belgesel', 'nat geo', 'discovery', 'history', 'planet',
                'trt belgesel', 'dmax'
            ]):
                ch['category'] = 'Belgesel'
            
            # Dini
            elif any(x in name_lower for x in [
                'dini', 'diyanet', 'semerkand', 'kudüs', 'lalegül'
            ]):
                ch['category'] = 'Dini'
    
    return channels

def sort_channels(channels):
    """Kanalları kategoriye ve isme göre sırala"""
    
    def sort_key(ch):
        category = ch['category']
        
        # Kategori önceliği
        if category in CATEGORY_ORDER:
            cat_index = CATEGORY_ORDER.index(category)
        else:
            cat_index = 999
        
        # İsim (alfabetik)
        name = ch['name'].lower()
        
        return (cat_index, name)
    
    return sorted(channels, key=sort_key)

def save_organized_m3u(channels, filename='channels.m3u'):
    """Düzenlenmiş M3U kaydet"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Header
        f.write('#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n')
        f.write(f'# Omer TV - Organized Playlist\n')
        f.write(f'# Updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Total Channels: {len(channels)}\n')
        f.write(f'# Organized by Category\n\n')
        
        # Kategoriye göre grupla
        by_category = defaultdict(list)
        for ch in channels:
            by_category[ch['category']].append(ch)
        
        # Her kategoriyi yaz
        for category in CATEGORY_ORDER:
            if category not in by_category:
                continue
            
            cat_channels = by_category[category]
            
            # Kategori başlığı
            f.write(f'\n#######################################\n')
            f.write(f'# {category.upper()} ({len(cat_channels)} kanal)\n')
            f.write(f'#######################################\n\n')
            
            # Kanallar (alfabetik)
            for ch in sorted(cat_channels, key=lambda x: x['name'].lower()):
                name = ch['name']
                url = ch['url']
                logo = ch['logo']
                tvg_id = ch['tvg_id']
                
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{category}",{name}\n')
                f.write(f'{url}\n')
        
        # Diğer kategoriler
        for category, cat_channels in by_category.items():
            if category in CATEGORY_ORDER:
                continue
            
            f.write(f'\n#######################################\n')
            f.write(f'# {category.upper()} ({len(cat_channels)} kanal)\n')
            f.write(f'#######################################\n\n')
            
            for ch in sorted(cat_channels, key=lambda x: x['name'].lower()):
                name = ch['name']
                url = ch['url']
                logo = ch['logo']
                tvg_id = ch['tvg_id']
                
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{category}",{name}\n')
                f.write(f'{url}\n')
    
    print(f"✅ {filename} kaydedildi ({len(channels)} kanal)")

def print_category_stats(channels):
    """Kategori istatistiklerini yazdır"""
    
    by_category = defaultdict(int)
    for ch in channels:
        by_category[ch['category']] += 1
    
    print("\n" + "="*60)
    print("📊 KATEGORİ İSTATİSTİKLERİ")
    print("="*60)
    
    total = len(channels)
    
    for category in CATEGORY_ORDER:
        if category in by_category:
            count = by_category[category]
            percentage = (count / total) * 100
            bar = "█" * (count // 3)
            print(f"{category:15s}: {count:4d} ({percentage:5.1f}%) {bar}")
    
    # Diğer kategoriler
    for category, count in sorted(by_category.items()):
        if category not in CATEGORY_ORDER:
            percentage = (count / total) * 100
            bar = "█" * (count // 3)
            print(f"{category:15s}: {count:4d} ({percentage:5.1f}%) {bar}")
    
    print("="*60)
    print(f"TOPLAM: {total} kanal\n")

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║       M3U Playlist Organizer (Omer TV)          ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    # 1. Parse
    print("📂 channels.m3u okunuyor...")
    channels = parse_m3u()
    print(f"✅ {len(channels)} kanal yüklendi\n")
    
    # 2. Kategori düzeltme
    print("🔄 Kategoriler düzenleniyor...")
    channels = categorize_by_name(channels)
    
    # 3. Sıralama
    print("📊 Kanallar sıralanıyor...")
    channels = sort_channels(channels)
    
    # 4. Kaydet
    print("💾 Düzenlenmiş playlist kaydediliyor...\n")
    save_organized_m3u(channels)
    
    # 5. İstatistikler
    print_category_stats(channels)
    
    # 6. JSON kaydet
    import os
    os.makedirs('data', exist_ok=True)
    with open('data/all_channels.json', 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    print("✅ data/all_channels.json kaydedildi\n")
    
    print("✅ İşlem tamamlandı!")

if __name__ == "__main__":
    main()
