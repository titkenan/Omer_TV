import json
from datetime import datetime


def generate_m3u():
    """Çalışan kanallardan M3U dosyası oluştur"""
    
    # Çalışan kanalları yükle
    with open('data/working_channels.json', 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    # M3U dosyası oluştur
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        # Header
        f.write('#EXTM3U\n')
        f.write(f'#EXTINF:-1,OmEr TV - Last Update: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
        f.write('#\n\n')
        
        # Kategorilere göre grupla
        categories = {}
        for ch in channels:
            cat = ch.get('category', 'Diğer')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ch)
        
        # Her kategori için
        for category in sorted(categories.keys()):
            f.write(f'#EXTINF:-1 group-title="───── {category} ─────",KATEGORI\n')
            f.write('#\n\n')
            
            for ch in sorted(categories[category], key=lambda x: x['name']):
                logo = ch.get('logo', '')
                tvg_logo = f' tvg-logo="{logo}"' if logo else ''
                
                f.write(f'#EXTINF:-1 group-title="{category}"{tvg_logo},{ch["name"]}\n')
                f.write(f'{ch["url"]}\n\n')
    
    print(f"✅ channels.m3u oluşturuldu ({len(channels)} kanal)")
    
    # README güncelle
    update_readme(channels)


def update_readme(channels):
    """README.md dosyasını güncelle"""
    
    total = len(channels)
    categories = {}
    for ch in channels:
        cat = ch.get('category', 'Diğer')
        categories[cat] = categories.get(cat, 0) + 1
    
    readme_content = f"""# 📺 OmEr TV - Türkiye IPTV Kanalları

[![Auto Update](https://github.com/titkenan/Omer_TV/actions/workflows/update_m3u.yml/badge.svg)](https://github.com/titkenan/Omer_TV/actions/workflows/update_m3u.yml)
[![Channels](https://img.shields.io/badge/Channels-{total}-brightgreen)](channels.m3u)
[![Last Update](https://img.shields.io/badge/Last%20Update-{datetime.now().strftime("%Y--%m--%d")}-blue)](https://github.com/titkenan/Omer_TV/commits/main)

> 🔄 Otomatik güncellenen, test edilmiş Türkiye TV kanalları listesi

---

## 📊 İstatistikler

- **Toplam Kanal:** {total}
- **Son Güncelleme:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
- **Güncelleme Sıklığı:** Her 6 saatte bir

### Kategori Dağılımı

"""
    
    for cat, count in sorted(categories.items()):
        readme_content += f"- **{cat}:** {count} kanal\n"
    
    readme_content += f"""

---

## 🚀 Kullanım

### M3U URL
