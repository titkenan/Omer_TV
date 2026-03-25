#!/usr/bin/env python3
import json
from datetime import datetime
import os


def generate_m3u():
    """M3U dosyası oluştur"""
    
    input_file = 'data/working_channels.json'
    
    # Dosya kontrolü
    if not os.path.exists(input_file):
        print(f"❌ Hata: {input_file} bulunamadı!")
        print("💡 Önce tester.py çalıştırılmalı")
        
        # Boş M3U oluştur
        with open('channels.m3u', 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            f.write('# OmEr TV - Kanallar yükleniyor...\n')
        
        return
    
    print(f"📂 Okunan dosya: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    if not channels:
        print("⚠️ Çalışan kanal yok!")
        with open('channels.m3u', 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            f.write('# OmEr TV - Şu an çalışan kanal yok\n')
        return
    
    print(f"📺 {len(channels)} kanal için M3U oluşturuluyor...\n")
    
    # M3U dosyası
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        f.write(f'# OmEr TV - Son Güncelleme: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}\n')
        f.write(f'# Toplam: {len(channels)} kanal\n\n')
        
        # Kategorilere ayır
        categories = {}
        for ch in channels:
            cat = ch.get('category', 'Genel')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ch)
        
        # Her kategori için
        for category in sorted(categories.keys()):
            for ch in sorted(categories[category], key=lambda x: x['name']):
                logo = ch.get('logo', '')
                tvg_logo = f' tvg-logo="{logo}"' if logo else ''
                
                f.write(f'#EXTINF:-1 group-title="{category}"{tvg_logo},{ch["name"]}\n')
                f.write(f'{ch["url"]}\n\n')
    
    file_size = os.path.getsize('channels.m3u')
    print(f"✅ channels.m3u oluşturuldu")
    print(f"📺 Kanal sayısı: {len(channels)}")
    print(f"📄 Dosya boyutu: {file_size} byte")
    
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
        "> 🔄 Otomatik güncellenen, test edilmiş Türkiye TV kanalları",
        "",
        "## 📊 İstatistikler",
        "",
        f"- **Toplam Kanal:** {total}",
        f"- **Son Güncelleme:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
        "### Kategoriler",
        ""
    ]
    
    for cat, count in sorted(categories.items()):
        readme_lines.append(f"- **{cat}:** {count} kanal")
    
    readme_lines.extend([
        "",
        "## 🚀 M3U Linki",
        "",
        "```",
        "https://raw.githubusercontent.com/titkenan/Omer_TV/main/channels.m3u",
        "```",
        "",
        "## 📋 Kanal Listesi",
        ""
    ])
    
    for category in sorted(categories.keys()):
        matching = [ch for ch in channels if ch.get('category', 'Genel') == category]
        readme_lines.append(f"### {category}")
        
        for ch in sorted(matching, key=lambda x: x['name']):
            ms = ch.get('response_time', 0)
            status = "🟢" if ms < 1000 else "🟡" if ms < 3000 else "🔴"
            readme_lines.append(f"- {status} {ch['name']} ({int(ms)}ms)")
        
        readme_lines.append("")
    
    readme_lines.append("---\n\n⭐ Beğendiyseniz yıldız vermeyi unutmayın!")
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_lines))
    
    print("✅ README.md güncellendi")


if __name__ == "__main__":
    generate_m3u()
