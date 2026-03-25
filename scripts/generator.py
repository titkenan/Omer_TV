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
    
    # README içeriği
    readme_lines = [
        "# 📺 OmEr TV - Türkiye IPTV",
        "",
        "![Auto Update](https://github.com/titkenan/Omer_TV/actions/workflows/update_m3u.yml/badge.svg)",
        f"![Channels](https://img.shields.io/badge/Channels-{total}-brightgreen)",
        f"![Last Update](https://img.shields.io/badge/Last%20Update-{datetime.now().strftime('%Y--%m--%d')}-blue)",
        "",
        "> 🔄 Otomatik güncellenen, test edilmiş Türkiye TV kanalları",
        "",
        "---",
        "",
        "## 📊 İstatistikler",
        "",
        f"- **Toplam Kanal:** {total}",
        f"- **Son Güncelleme:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "- **Güncelleme Sıklığı:** Her 6 saatte bir",
        "",
        "### Kategoriler",
        ""
    ]
    
    for cat, count in sorted(categories.items()):
        readme_lines.append(f"- **{cat}:** {count} kanal")
    
    readme_lines.extend([
        "",
        "---",
        "",
        "## 🚀 Kullanım",
        "",
        "### M3U Linki",
        "```",
        "https://raw.githubusercontent.com/titkenan/Omer_TV/main/channels.m3u",
        "```",
        "",
        "### VLC ile Aç",
        "1. VLC Player'ı aç",
        "2. Media > Open Network Stream",
        "3. URL'yi yapıştır",
        "4. Play",
        "",
        "### IPTV Uygulamaları",
        "- **Android:** IPTV, TiviMate",
        "- **iOS:** GSE Smart IPTV",
        "- **Smart TV:** Smart IPTV",
        "",
        "---",
        "",
        "## 📋 Kanal Listesi",
        ""
    ])
    
    for category in sorted(categories.keys()):
        matching = [ch for ch in channels if ch.get('category', 'Diger') == category]
        readme_lines.append(f"### 📂 {category} ({len(matching)} kanal)")
        readme_lines.append("")
        
        for ch in sorted(matching, key=lambda x: x['name']):
            ms = ch.get('response_time', 0)
            if ms < 1000:
                status = "🟢"
            elif ms < 3000:
                status = "🟡"
            else:
                status = "🔴"
            readme_lines.append(f"- {status} **{ch['name']}** ({ms}ms)")
        
        readme_lines.append("")
    
    readme_lines.extend([
        "---",
        "",
        "## ⚙️ Otomatik Güncelleme",
        "",
        "Bu liste GitHub Actions ile otomatik güncellenir:",
        "",
        "1. Her 6 saatte bir stream'ler test edilir",
        "2. Çalışmayan kanallar çıkarılır",
        "3. M3U dosyası güncellenir",
        "",
        "---",
        "",
        "## 📝 Lisans",
        "",
        "MIT License - Özgürce kullanabilirsiniz.",
        "",
        "---",
        "",
        "**⭐ Beğendiyseniz yıldız vermeyi unutmayın!**",
        ""
    ])
    
    readme = '\n'.join(readme_lines)
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✅ README.md güncellendi")


if __name__ == "__main__":
    generate_m3u()
