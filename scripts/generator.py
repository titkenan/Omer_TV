#!/usr/bin/env python3
import json
from datetime import datetime
import os


def generate_m3u():
    """M3U dosyası oluştur"""
    
    input_file = 'data/working_channels.json'
    
    if not os.path.exists(input_file):
        print(f"❌ Hata: {input_file} bulunamadı!")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    if not channels:
        print("⚠️ Kanal yok!")
        return
    
    print(f"📺 {len(channels)} kanal için M3U oluşturuluyor...")
    
    # M3U dosyası
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        f.write(f'# OmEr TV - Son Güncelleme: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Toplam: {len(channels)} kanal\n')
        f.write('# GitHub: https://github.com/titkenan/Omer_TV\n\n')
        
        # Kategorilere ayır
        categories = {}
        for ch in channels:
            cat = ch.get('category', 'Genel')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ch)
        
        # Kategori sırası
        category_order = ['Genel', 'Haber', 'Spor', 'Çocuk', 'Belgesel', 'Müzik', 'Sinema', 'Dini', 'TRT']
        
        for category in category_order:
            if category not in categories:
                continue
            
            for ch in sorted(categories[category], key=lambda x: x['name']):
                logo = ch.get('logo', '')
                tvg_logo = f' tvg-logo="{logo}"' if logo else ''
                
                f.write(f'#EXTINF:-1 group-title="{category}"{tvg_logo},{ch["name"]}\n')
                f.write(f'{ch["url"]}\n\n')
        
        # Sıralanmamış kategoriler
        for category in sorted(categories.keys()):
            if category in category_order:
                continue
            
            for ch in sorted(categories[category], key=lambda x: x['name']):
                logo = ch.get('logo', '')
                tvg_logo = f' tvg-logo="{logo}"' if logo else ''
                
                f.write(f'#EXTINF:-1 group-title="{category}"{tvg_logo},{ch["name"]}\n')
                f.write(f'{ch["url"]}\n\n')
    
    print(f"✅ channels.m3u oluşturuldu ({len(channels)} kanal)")
    
    # README güncelle
    update_readme(channels)


def update_readme(channels):
    """README güncelle"""
    
    total = len(channels)
    categories = {}
    for ch in channels:
        cat = ch.get('category', 'Genel')
        categories[cat] = categories.get(cat, 0) + 1
    
    readme_lines = [
        "# 📺 OmEr TV - Türkiye IPTV",
        "",
        "[![Auto Update](https://github.com/titkenan/Omer_TV/actions/workflows/update_m3u.yml/badge.svg)](https://github.com/titkenan/Omer_TV/actions)",
        f"![Channels](https://img.shields.io/badge/Channels-{total}-brightgreen)",
        "",
        "> 🔄 Otomatik güncellenen Türkiye TV kanalları listesi",
        "",
        "---",
        "",
        "## 📊 İstatistikler",
        "",
        f"- **Toplam Kanal:** {total}",
        f"- **Son Güncelleme:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "### 📁 Kategoriler",
        ""
    ]
    
    category_order = ['Genel', 'Haber', 'Spor', 'Çocuk', 'Belgesel', 'Müzik', 'Sinema', 'Dini', 'TRT']
    
    for cat in category_order:
        if cat in categories:
            readme_lines.append(f"- **{cat}:** {categories[cat]} kanal")
    
    for cat in sorted(categories.keys()):
        if cat not in category_order:
            readme_lines.append(f"- **{cat}:** {categories[cat]} kanal")
    
    readme_lines.extend([
        "",
        "---",
        "",
        "## 🚀 Kullanım",
        "",
        "### 📡 M3U Linki",
        "",
        "```",
        "https://raw.githubusercontent.com/titkenan/Omer_TV/main/channels.m3u",
        "```",
        "",
        "### 📺 Nasıl İzlenir?",
        "",
        "| Platform | Uygulama |",
        "|----------|----------|",
        "| 🖥️ PC | VLC Media Player |",
        "| 📱 Android | IPTV, TiviMate, OTT Navigator |",
        "| 🍎 iOS | GSE Smart IPTV, IPTV Smarters |",
        "| 📺 Smart TV | Smart IPTV, SS IPTV |",
        "",
        "### VLC ile Açma",
        "",
        "1. VLC Player'ı aç",
        "2. **Media** > **Open Network Stream**",
        "3. URL'yi yapıştır",
        "4. **Play**",
        "",
        "---",
        "",
        "## 📋 Kanal Listesi",
        ""
    ])
    
    for category in category_order:
        if category not in categories:
            continue
        
        matching = [ch for ch in channels if ch.get('category', 'Genel') == category]
        readme_lines.append(f"### 📂 {category} ({len(matching)} kanal)")
        readme_lines.append("")
        
        for ch in sorted(matching, key=lambda x: x['name']):
            readme_lines.append(f"- 📺 {ch['name']}")
        
        readme_lines.append("")
    
    readme_lines.extend([
        "---",
        "",
        "## ⚠️ Uyarı",
        "",
        "- Bazı kanallar geçici olarak çalışmayabilir",
        "- Yedek linkler mevcuttur",
        "- Sorun bildirmek için [Issues](https://github.com/titkenan/Omer_TV/issues) açın",
        "",
        "---",
        "",
        "## ⭐ Destek",
        "",
        "Beğendiyseniz **yıldız** vermeyi unutmayın!",
        "",
        "---",
        "",
        f"*Son güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*"
    ])
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_lines))
    
    print("✅ README.md güncellendi")


if __name__ == "__main__":
    generate_m3u()
