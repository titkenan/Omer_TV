#!/usr/bin/env python3
"""
Vavoo Listesini Temizle ve Ekle
Sadece Ulusal ve Haber kanallarını alır.
Gereksiz (Spor, Sinema, Çocuk) kanalları siler.
"""

import re
from datetime import datetime

# Senin verdiğin ham liste
RAW_VAVOO_DATA = """
#EXTINF:-1 tvg-name="4K TR: TV8 HD ", 4K TR: TV8 HD 
https://www.vavoo.to/play/2693299013/index.m3u8
#EXTINF:-1 tvg-name="TV 8 ", TV 8 
https://www.vavoo.to/play/2196709234/index.m3u8
#EXTINF:-1 tvg-name="TV8 FHD ", TV8 FHD 
https://www.vavoo.to/play/3849481299/index.m3u8
#EXTINF:-1 tvg-name="TV8 HD ", TV8 HD 
https://www.vavoo.to/play/1702470161/index.m3u8
#EXTINF:-1 tvg-name="TV 8 HD (H265) ", TV 8 HD (H265) 
https://www.vavoo.to/play/3298026270/index.m3u8
#EXTINF:-1 tvg-name="TV 8 ", TV 8 
https://www.vavoo.to/play/4292306921/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TRT 1 HD ", 4K TR: TRT 1 HD 
https://www.vavoo.to/play/1762199258/index.m3u8
#EXTINF:-1 tvg-name="4K TR: SHOW TV HD ", 4K TR: SHOW TV HD 
https://www.vavoo.to/play/879588960/index.m3u8
#EXTINF:-1 tvg-name="4K TR: STAR TV HD ", 4K TR: STAR TV HD 
https://www.vavoo.to/play/2192971293/index.m3u8
#EXTINF:-1 tvg-name="4K TR: ATV HD ", 4K TR: ATV HD 
https://www.vavoo.to/play/2325261286/index.m3u8
#EXTINF:-1 tvg-name="TV8 SD ", TV8 SD 
https://www.vavoo.to/play/208162889/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NOW HD ", 4K TR: NOW HD 
https://www.vavoo.to/play/2578197593/index.m3u8
#EXTINF:-1 tvg-name="4K TR: CNN T RK HD ", 4K TR: CNN T RK HD 
https://www.vavoo.to/play/2056768647/index.m3u8
#EXTINF:-1 tvg-name="ATV HD ", ATV HD 
https://www.vavoo.to/play/1332310706/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TV8,5 HD ", 4K TR: TV8,5 HD 
https://www.vavoo.to/play/1886743624/index.m3u8
#EXTINF:-1 tvg-name="TV8 RAW ", TV8 RAW 
https://www.vavoo.to/play/1991010324/index.m3u8
#EXTINF:-1 tvg-name="TV 8 SD ", TV 8 SD 
https://www.vavoo.to/play/3695389987/index.m3u8
#EXTINF:-1 tvg-name="4K TR: A HABER HD ", 4K TR: A HABER HD 
https://www.vavoo.to/play/1064954896/index.m3u8
#EXTINF:-1 tvg-name="TV 8 HEVC ", TV 8 HEVC 
https://www.vavoo.to/play/1662562034/index.m3u8
#EXTINF:-1 tvg-name="CNN TURK HD ", CNN TURK HD 
https://www.vavoo.to/play/4273153967/index.m3u8
#EXTINF:-1 tvg-name="TV8 5 RAW ", TV8 5 RAW 
https://www.vavoo.to/play/2412205937/index.m3u8
#EXTINF:-1 tvg-name="ATV FHD ", ATV FHD 
https://www.vavoo.to/play/2861010641/index.m3u8
#EXTINF:-1 tvg-name="NOW TV FHD ", NOW TV FHD 
https://www.vavoo.to/play/919108696/index.m3u8
#EXTINF:-1 tvg-name="NOW TV HD ", NOW TV HD 
https://www.vavoo.to/play/161305206/index.m3u8
#EXTINF:-1 tvg-name="24 HABER HD+ SD ", 24 HABER HD+ SD 
https://www.vavoo.to/play/3828793616/index.m3u8
#EXTINF:-1 tvg-name="4K TR: HABER GLOBAL HD ", 4K TR: HABER GLOBAL HD 
https://www.vavoo.to/play/1196626387/index.m3u8
#EXTINF:-1 tvg-name="STAR TV FHD ", STAR TV FHD 
https://www.vavoo.to/play/2020035128/index.m3u8
#EXTINF:-1 tvg-name="STAR HD (H265) ", STAR HD (H265) 
https://www.vavoo.to/play/1134124382/index.m3u8
#EXTINF:-1 tvg-name="4K TR: KANAL D HD ", 4K TR: KANAL D HD 
https://www.vavoo.to/play/1677679684/index.m3u8
#EXTINF:-1 tvg-name="STAR TV HD ", STAR TV HD 
https://www.vavoo.to/play/2720556692/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV HD ", SHOW TV HD 
https://www.vavoo.to/play/351471337/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 HD ", TRT 1 HD 
https://www.vavoo.to/play/1221669131/index.m3u8
#EXTINF:-1 tvg-name="FOX ", FOX 
https://www.vavoo.to/play/1498459094/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV ", SHOW TV 
https://www.vavoo.to/play/2395422638/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV FHD ", SHOW TV FHD 
https://www.vavoo.to/play/1449499865/index.m3u8
#EXTINF:-1 tvg-name="EURO STAR ", EURO STAR 
https://www.vavoo.to/play/1827094680/index.m3u8
#EXTINF:-1 tvg-name="4K TR: 360 HD ", 4K TR: 360 HD 
https://www.vavoo.to/play/473300573/index.m3u8
#EXTINF:-1 tvg-name="STAR HD SD ", STAR HD SD 
https://www.vavoo.to/play/3209892863/index.m3u8
#EXTINF:-1 tvg-name="ATV ", ATV 
https://www.vavoo.to/play/1255594337/index.m3u8
#EXTINF:-1 tvg-name="KANAL D HD ", KANAL D HD 
https://www.vavoo.to/play/1130441933/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NTV HD ", 4K TR: NTV HD 
https://www.vavoo.to/play/2073292907/index.m3u8
#EXTINF:-1 tvg-name="ATV ", ATV 
https://www.vavoo.to/play/455930425/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 ", TRT 1 
https://www.vavoo.to/play/2041026135/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TGRT HABER HD ", 4K TR: TGRT HABER HD 
https://www.vavoo.to/play/1907154704/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 FHD ", TRT 1 FHD 
https://www.vavoo.to/play/406666682/index.m3u8
#EXTINF:-1 tvg-name="4K TR: AK T TV HD ", 4K TR: AK T TV HD 
https://www.vavoo.to/play/3445585687/index.m3u8
#EXTINF:-1 tvg-name="TV 8.5 ", TV 8.5 
https://www.vavoo.to/play/14092376/index.m3u8
#EXTINF:-1 tvg-name="4K TR: BEYAZ TV HD ", 4K TR: BEYAZ TV HD 
https://www.vavoo.to/play/805689873/index.m3u8
#EXTINF:-1 tvg-name="KANAL D ", KANAL D 
https://www.vavoo.to/play/231583905/index.m3u8
#EXTINF:-1 tvg-name="4K TR: HABERT RK HD ", 4K TR: HABERT RK HD 
https://www.vavoo.to/play/4253369376/index.m3u8
#EXTINF:-1 tvg-name="A HABER HD ", A HABER HD 
https://www.vavoo.to/play/535272601/index.m3u8
#EXTINF:-1 tvg-name="SHOW TURK ", SHOW TURK 
https://www.vavoo.to/play/1880270561/index.m3u8
#EXTINF:-1 tvg-name="ATV AVRUPA ", ATV AVRUPA 
https://www.vavoo.to/play/3195910351/index.m3u8
#EXTINF:-1 tvg-name="KANAL D FHD ", KANAL D FHD 
https://www.vavoo.to/play/1781656098/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 ", KANAL 7 
https://www.vavoo.to/play/3015649982/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 ", TRT 1 
https://www.vavoo.to/play/115261333/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER ", TRT HABER 
https://www.vavoo.to/play/1890976041/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TEVE2 HD ", 4K TR: TEVE2 HD 
https://www.vavoo.to/play/1917502631/index.m3u8
#EXTINF:-1 tvg-name="24 ", 24 
https://www.vavoo.to/play/1702937932/index.m3u8
#EXTINF:-1 tvg-name="FOX ", FOX 
https://www.vavoo.to/play/145391758/index.m3u8
#EXTINF:-1 tvg-name="ATV EUROPA ", ATV EUROPA 
https://www.vavoo.to/play/90085139/index.m3u8
#EXTINF:-1 tvg-name="FOX TV HD (H265) ", FOX TV HD (H265) 
https://www.vavoo.to/play/1345288490/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV ", BEYAZ TV 
https://www.vavoo.to/play/275850888/index.m3u8
#EXTINF:-1 tvg-name="4K TR: 24 HD ", 4K TR: 24 HD 
https://www.vavoo.to/play/1998168122/index.m3u8
#EXTINF:-1 tvg-name="ATV HD (H265) ", ATV HD (H265) 
https://www.vavoo.to/play/129909794/index.m3u8
#EXTINF:-1 tvg-name="CNN T RK HD+ SD ", CNN T RK HD+ SD 
https://www.vavoo.to/play/2868318534/index.m3u8
#EXTINF:-1 tvg-name="A HABER ", A HABER 
https://www.vavoo.to/play/1174108535/index.m3u8
#EXTINF:-1 tvg-name="A HABER ", A HABER 
https://www.vavoo.to/play/1596095882/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 HD ", KANAL 7 HD 
https://www.vavoo.to/play/1639889598/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 RAW ", TRT 1 RAW 
https://www.vavoo.to/play/2346924541/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 SD ", TRT 1 SD 
https://www.vavoo.to/play/566281043/index.m3u8
#EXTINF:-1 tvg-name="HABERTURK RAW ", HABERTURK RAW 
https://www.vavoo.to/play/2129890787/index.m3u8
#EXTINF:-1 tvg-name="A2 HD ", A2 HD 
https://www.vavoo.to/play/867875861/index.m3u8
#EXTINF:-1 tvg-name="4K TR: A2 HD ", 4K TR: A2 HD 
https://www.vavoo.to/play/2019055277/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV HEVC ", BEYAZ TV HEVC 
https://www.vavoo.to/play/1510783901/index.m3u8
#EXTINF:-1 tvg-name="360 ", 360 
https://www.vavoo.to/play/1651455199/index.m3u8
#EXTINF:-1 tvg-name="SHOW HD (H265) ", SHOW HD (H265) 
https://www.vavoo.to/play/3537232978/index.m3u8
#EXTINF:-1 tvg-name="A HABER HEVC ", A HABER HEVC 
https://www.vavoo.to/play/3766846723/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER ", TRT HABER 
https://www.vavoo.to/play/2003703357/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 HEVC ", KANAL 7 HEVC 
https://www.vavoo.to/play/3897412802/index.m3u8
#EXTINF:-1 tvg-name="360 ", 360 
https://www.vavoo.to/play/865410951/index.m3u8
#EXTINF:-1 tvg-name="TEVE 2 ", TEVE 2 
https://www.vavoo.to/play/2549900211/index.m3u8
#EXTINF:-1 tvg-name="KANAL D SD ", KANAL D SD 
https://www.vavoo.to/play/712040085/index.m3u8
#EXTINF:-1 tvg-name="TVNET ", TVNET 
https://www.vavoo.to/play/1221661755/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 4K ", TRT 1 4K 
https://www.vavoo.to/play/3059837792/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV HD ", BEYAZ TV HD 
https://www.vavoo.to/play/2755756005/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV RAW ", SHOW TV RAW 
https://www.vavoo.to/play/3317405854/index.m3u8
#EXTINF:-1 tvg-name="TVNET HD ", TVNET HD 
https://www.vavoo.to/play/1182480796/index.m3u8
#EXTINF:-1 tvg-name="ATV RAW ", ATV RAW 
https://www.vavoo.to/play/962169494/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER HEVC ", TRT HABER HEVC 
https://www.vavoo.to/play/2057965553/index.m3u8
#EXTINF:-1 tvg-name="SHOW MAX ", SHOW MAX 
https://www.vavoo.to/play/1495761327/index.m3u8
#EXTINF:-1 tvg-name="SHOW MAX ", SHOW MAX 
https://www.vavoo.to/play/2196278652/index.m3u8
#EXTINF:-1 tvg-name="TGRT HABER ", TGRT HABER 
https://www.vavoo.to/play/1907154704/index.m3u8
#EXTINF:-1 tvg-name="TGRT BELGESEL ", TGRT BELGESEL 
https://www.vavoo.to/play/1743993546/index.m3u8
#EXTINF:-1 tvg-name="ULKE TV ", ULKE TV 
https://www.vavoo.to/play/3053206623/index.m3u8
#EXTINF:-1 tvg-name="ULKE TV ", ULKE TV 
https://www.vavoo.to/play/216740557/index.m3u8
"""

def parse_and_filter():
    """Vavoo verisini parse et ve filtrele"""
    
    channels = []
    
    # İsim ve URL'yi eşleştir
    pattern = r'#EXTINF:-1 tvg-name="([^"]+)"[^\n]*\n(https://[^\n]+)'
    matches = re.findall(pattern, RAW_VAVOO_DATA)
    
    print(f"Toplam {len(matches)} kanal bulundu.")
    
    for name, url in matches:
        # İsim temizleme
        clean_name = name.strip()
        clean_name = clean_name.replace('4K TR:', '').strip()
        clean_name = clean_name.replace(' HD', '').replace(' FHD', '').replace(' SD', '').strip()
        clean_name = clean_name.replace(' (H265)', '').replace(' HEVC', '').replace(' RAW', '').strip()
        clean_name = clean_name.replace('NOW', 'FOX') # NOW -> FOX standardı
        clean_name = clean_name.replace('CNN T RK', 'CNN TURK')
        
        # Filtreleme (Sadece Ulusal ve Haber)
        category = get_category(clean_name)
        
        if category in ['Ulusal', 'Haber']:
            channels.append({
                'name': clean_name,
                'url': url,
                'category': category
            })
    
    return channels

def get_category(name):
    """Kanal adına göre kategori belirle"""
    n = name.lower()
    
    # ❌ YASAKLI KELİMELER (Spor, Sinema, Çocuk vb.)
    forbidden = [
        'spor', 'sport', 'bein', 'exxen', 's sport', 'tivibu', 'smart', 'fanatik', 'aspor',
        'sinema', 'cinema', 'film', 'dizi', 'movie', 'action', 'komedi', 'aile', 'yerli', 'yabanci', 'box',
        'cocuk', 'çocuk', 'kids', 'cartoon', 'disney', 'minika', 'tr child', 'baby', 'nick', 'pijama', 'caillou', 'niloya', 'rafadan',
        'belgesel', 'docu', 'planet', 'nat geo', 'discovery', 'history', 'tlc', 'dmax', 'yaban', 'bbc earth',
        'muzik', 'music', 'kral', 'power', 'dream', 'nr1', 'mm tv',
        'adult', 'xxx', 'plus', '+18'
    ]
    
    if any(x in n for x in forbidden):
        return 'Yasakli'
    
    # ✅ İZİNLİ KELİMELER (Ulusal)
    ulusal = [
        'trt 1', 'show', 'star', 'atv', 'kanal d', 'tv8', 'kanal 7', 'fox', 'now', 'beyaz', 'teve2', '360', 'a2', 'tlc', 'dmax'
    ]
    
    # ✅ İZİNLİ KELİMELER (Haber)
    haber = [
        'haber', 'cnn', 'ntv', 'tgrt', 'ulke', 'tv100', '24', 'tvnet', 'ekol'
    ]
    
    if any(x in n for x in ulusal):
        return 'Ulusal'
    elif any(x in n for x in haber):
        return 'Haber'
    
    return 'Diger'

def create_m3u(channels):
    """M3U Dosyası Oluştur"""
    
    # Kategoriye göre sırala
    channels.sort(key=lambda x: (x['category'], x['name']))
    
    content = '#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n'
    content += f'# ÖMER TV - Updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n'
    content += '# Vavoo Premium Kaynaklar (Ulusal + Haber)\n\n'
    
    current_cat = None
    for ch in channels:
        if ch['category'] != current_cat:
            content += f'\n### {ch["category"].upper()} ###\n'
            current_cat = ch['category']
        
        # User-agent ekle (Vavoo için bazen gerekebilir)
        content += f'#EXTINF:-1 group-title="{ch["category"]}",{ch["name"]}\n'
        content += '#EXTVLCOPT:http-user-agent=Vavoo/2.6\n'
        content += f'{ch["url"]}\n'
    
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ channels.m3u oluşturuldu! ({len(channels)} kanal)")

if __name__ == "__main__":
    channels = parse_and_filter()
    create_m3u(channels)
