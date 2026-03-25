import json
from datetime import datetime
import os


def generate_m3u():
    """M3U dosyası oluştur"""
    
    with open('data/working_channels.json', 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        f.write(f'# OmEr TV - Son Güncelleme: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
        f.write(f'# Toplam: {len(channels)} kanal\n\n')
        
        categories = {}
        for ch in channels:
            cat = ch.get('category', 'Diger')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ch)
        
        for category in sorted(categories.keys()):
            for ch in sorted(categories[category], key=lambda x: x['name']):
                logo = ch.get('logo', '')
                tvg_logo = f' tvg-logo="{logo}"' if logo else ''
                f.write(f'#EXTINF:-1 group-title="{category}"{tvg_logo},{ch["name"]}\n')
                f.write(f'{ch["url"]}\n\n')
    
    print(f"✅ channels.m3u oluşturuldu ({len(channels)} kanal)")
    update_readme(channels)


def update_readme(channels):
    """README güncelle"""
    
    total = len(channels)
    categories = {}
    for ch in channels:
        cat = ch.get('category', 'Diger')
        categories[cat] = categories.get(cat, 0) + 1
    
    readme = f"""# 📺 OmEr TV - Türkiye IPTV

![Auto Update](https://github.com/titkenan/Omer_TV/actions/workflows/update_m3u.yml/badge.svg)

> 🔄 Otomatik güncellenen Türkiye TV kanalları

## 📊 İstatistikler

- **Toplam Kanal:** {total}
- **Son Güncelleme:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### Kategoriler

"""
    
    for cat, count in sorted(categories.items()):
        readme += f"- **{cat}:** {count} kanal\n"
    
    readme += f"""

## 🚀 Kullanım

### M3U Linki
