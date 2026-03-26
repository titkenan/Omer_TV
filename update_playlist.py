#!/usr/bin/env python3
"""
ÖMER TV - Playlist Manager
Tüm işlemleri tek script ile yönet
"""

import re
from datetime import datetime

# ========================================
# VAVOO TAM LİSTESİ (Senin verdiğin)
# ========================================

VAVOO_DATA = """#EXTM3U 
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
#EXTINF:-1 tvg-name="4K TR: A SPOR HD ", 4K TR: A SPOR HD 
https://www.vavoo.to/play/1771137539/index.m3u8
#EXTINF:-1 tvg-name="TV8 SD ", TV8 SD 
https://www.vavoo.to/play/208162889/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TRT SPOR HD ", 4K TR: TRT SPOR HD 
https://www.vavoo.to/play/2262969938/index.m3u8
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
#EXTINF:-1 tvg-name="TV 8 INT ", TV 8 INT 
https://www.vavoo.to/play/1764745585/index.m3u8
#EXTINF:-1 tvg-name="4K TR: A HABER HD ", 4K TR: A HABER HD 
https://www.vavoo.to/play/1064954896/index.m3u8
#EXTINF:-1 tvg-name="TV 8 HEVC ", TV 8 HEVC 
https://www.vavoo.to/play/1662562034/index.m3u8
#EXTINF:-1 tvg-name="A SPOR HD ", A SPOR HD 
https://www.vavoo.to/play/2556711030/index.m3u8
#EXTINF:-1 tvg-name="CNN TURK HD ", CNN TURK HD 
https://www.vavoo.to/play/4273153967/index.m3u8
#EXTINF:-1 tvg-name="TV8 5 RAW ", TV8 5 RAW 
https://www.vavoo.to/play/2412205937/index.m3u8
#EXTINF:-1 tvg-name="ATV FHD ", ATV FHD 
https://www.vavoo.to/play/2861010641/index.m3u8
#EXTINF:-1 tvg-name="TRT SPOR ", TRT SPOR 
https://www.vavoo.to/play/2781429267/index.m3u8
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
#EXTINF:-1 tvg-name="BEIN SPORTS 1 + ", BEIN SPORTS 1 + 
https://www.vavoo.to/play/2576216897/index.m3u8
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
#EXTINF:-1 tvg-name="4K TR: TRT HABER HD ", 4K TR: TRT HABER HD 
https://www.vavoo.to/play/603651638/index.m3u8
#EXTINF:-1 tvg-name="ATV AVRUPA ", ATV AVRUPA 
https://www.vavoo.to/play/3195910351/index.m3u8
#EXTINF:-1 tvg-name="KRAL TV ", KRAL TV 
https://www.vavoo.to/play/1505032467/index.m3u8
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
#EXTINF:-1 tvg-name="KRAL TV ", KRAL TV 
https://www.vavoo.to/play/1131281902/index.m3u8
#EXTINF:-1 tvg-name="ATV EUROPA ", ATV EUROPA 
https://www.vavoo.to/play/90085139/index.m3u8
#EXTINF:-1 tvg-name="FOX TV HD (H265) ", FOX TV HD (H265) 
https://www.vavoo.to/play/1345288490/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV ", BEYAZ TV 
https://www.vavoo.to/play/275850888/index.m3u8
#EXTINF:-1 tvg-name="4K TR: 24 HD ", 4K TR: 24 HD 
https://www.vavoo.to/play/1998168122/index.m3u8
#EXTINF:-1 tvg-name="CNN TURK ", CNN TURK 
https://www.vavoo.to/play/3278683973/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 FHD ", KANAL 7 FHD 
https://www.vavoo.to/play/2736723250/index.m3u8
#EXTINF:-1 tvg-name="EURO STAR ", EURO STAR 
https://www.vavoo.to/play/3814521935/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER HD ", TRT HABER HD 
https://www.vavoo.to/play/2579401878/index.m3u8
#EXTINF:-1 tvg-name="KANAL D ", KANAL D 
https://www.vavoo.to/play/387232860/index.m3u8
#EXTINF:-1 tvg-name="TRT MUZIK ", TRT MUZIK 
https://www.vavoo.to/play/2362678422/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 ", KANAL 7 
https://www.vavoo.to/play/2842046019/index.m3u8
#EXTINF:-1 tvg-name="TRT TURK ", TRT TURK 
https://www.vavoo.to/play/4098093256/index.m3u8
#EXTINF:-1 tvg-name="4K TR: A2 HD ", 4K TR: A2 HD 
https://www.vavoo.to/play/2019055277/index.m3u8
#EXTINF:-1 tvg-name="360 ", 360 
https://www.vavoo.to/play/1651455199/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER ", TRT HABER 
https://www.vavoo.to/play/2003703357/index.m3u8
#EXTINF:-1 tvg-name="360 ", 360 
https://www.vavoo.to/play/865410951/index.m3u8
#EXTINF:-1 tvg-name="TEVE 2 ", TEVE 2 
https://www.vavoo.to/play/2549900211/index.m3u8
#EXTINF:-1 tvg-name="TVNET ", TVNET 
https://www.vavoo.to/play/1221661755/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 4K ", TRT 1 4K 
https://www.vavoo.to/play/3059837792/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV HD ", BEYAZ TV HD 
https://www.vavoo.to/play/2755756005/index.m3u8
#EXTINF:-1 tvg-name="TVNET HD ", TVNET HD 
https://www.vavoo.to/play/1182480796/index.m3u8
#EXTINF:-1 tvg-name="A2 HD ", A2 HD 
https://www.vavoo.to/play/867875861/index.m3u8
#EXTINF:-1 tvg-name="ÜLKE TV ", ÜLKE TV 
https://www.vavoo.to/play/3053206623/index.m3u8
#EXTINF:-1 tvg-name="TV 8.5 FHD ", TV 8.5 FHD 
https://www.vavoo.to/play/1908265816/index.m3u8
#EXTINF:-1 tvg-name="ULKE TV ", ULKE TV 
https://www.vavoo.to/play/216740557/index.m3u8
#EXTINF:-1 tvg-name="TV 8.5 HD ", TV 8.5 HD 
https://www.vavoo.to/play/3472698776/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TVNET HD ", 4K TR: TVNET HD 
https://www.vavoo.to/play/1738739277/index.m3u8
#EXTINF:-1 tvg-name="4K TR: EKOL TV ", 4K TR: EKOL TV 
https://www.vavoo.to/play/2706210049/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 AVRUPA ", KANAL 7 AVRUPA 
https://www.vavoo.to/play/498645977/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 EUROPA ", KANAL 7 EUROPA 
https://www.vavoo.to/play/3264983364/index.m3u8
#EXTINF:-1 tvg-name="TÜRKHABER TV ", TÜRKHABER TV 
https://www.vavoo.to/play/2012038243/index.m3u8
#EXTINF:-1 tvg-name="TRT MUZIK ", TRT MUZIK 
https://www.vavoo.to/play/2332789634/index.m3u8
#EXTINF:-1 tvg-name="KANAL T ", KANAL T 
https://www.vavoo.to/play/1831675683/index.m3u8
#EXTINF:-1 tvg-name="LIDER HABER ", LIDER HABER 
https://www.vavoo.to/play/703698868/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 HD ", KANAL 7 HD 
https://www.vavoo.to/play/1639889598/index.m3u8
#EXTINF:-1 tvg-name="KRAL TV HD ", KRAL TV HD 
https://www.vavoo.to/play/2879812830/index.m3u8
#EXTINF:-1 tvg-name="ADA TV ", ADA TV 
https://www.vavoo.to/play/4225961715/index.m3u8
#EXTINF:-1 tvg-name="HRT AKDENIZ TV ", HRT AKDENIZ TV 
https://www.vavoo.to/play/4223430509/index.m3u8
#EXTINF:-1 tvg-name="KRAL POP ", KRAL POP 
https://www.vavoo.to/play/4169838993/index.m3u8
#EXTINF:-1 tvg-name="4K TR: MELTEM TV ", 4K TR: MELTEM TV 
https://www.vavoo.to/play/700381068/index.m3u8
#EXTINF:-1 tvg-name="4K TR: DREAM T RK ", 4K TR: DREAM T RK 
https://www.vavoo.to/play/4266683025/index.m3u8
"""

# ========================================
# FONKSİYONLAR
# ========================================

def auto_categorize(name):
    """İsimden otomatik kategori belirle"""
    n = name.lower()
    
    # Ulusal
    if any(x in n for x in ['trt 1', 'trt1', 'show', 'star', 'atv', 'kanal d', 'kanald', 'tv8', 'tv 8', 'kanal 7', 'kanal7', 'fox', 'now', 'beyaz', 'teve', '360', 'a2', 'euro', 'tvnet']):
        return 'Ulusal'
    
    # Haber
    elif any(x in n for x in ['haber', 'cnn', 'ntv', 'tgrt', '24', 'ulke', 'tv100', 'ekol', 'turk', 'lider', 'akdeniz']):
        return 'Haber'
    
    # Müzik
    elif any(x in n for x in ['muzik', 'müzik', 'music', 'kral', 'power', 'dream', 'meltem']):
        return 'Müzik'
    
    else:
        return 'Genel'

def create_m3u():
    """M3U dosyası oluştur"""
    
    # Parse
    pattern = r'#EXTINF:-1 tvg-name="([^"]+)"[^\n]*\n(https://[^\n]+)'
    matches = re.findall(pattern, VAVOO_DATA)
    
    print(f"✅ {len(matches)} kanal bulundu")
    
    # Kategorize
    channels_by_category = {}
    
    for name, url in matches:
        name = name.strip()
        category = auto_categorize(name)
        
        if category not in channels_by_category:
            channels_by_category[category] = []
        
        channels_by_category[category].append({'name': name, 'url': url})
    
    # İstatistik
    print("\n📊 Kategoriler:")
    for cat in sorted(channels_by_category.keys()):
        print(f"   {cat:15s}: {len(channels_by_category[category]):3d}")
    
    # M3U oluştur
    content = '#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n'
    content += f'# ÖMER TV - {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n'
    content += f'# Toplam: {len(matches)} kanal\n\n'
    
    category_order = ['Ulusal', 'Haber', 'Müzik', 'Genel']
    
    for category in category_order:
        if category in channels_by_category:
            content += f'\n#########################################\n'
            content += f'# {category.upper()} ({len(channels_by_category[category])} kanal)\n'
            content += f'#########################################\n\n'
            
            for ch in sorted(channels_by_category[category], key=lambda x: x['name']):
                content += f'#EXTINF:-1 group-title="{category}",{ch["name"]}\n'
                content += f'{ch["url"]}\n'
    
    # Kaydet
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ channels.m3u oluşturuldu! ({len(matches)} kanal)")
    print("\n🔗 Link:")
    print("   https://raw.githubusercontent.com/titkenan/Omer_TV/main/channels.m3u")

if __name__ == "__main__":
    print("=" * 60)
    print("ÖMER TV - Playlist Generator")
    print("=" * 60)
    create_m3u()
