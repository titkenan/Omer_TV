#!/usr/bin/env python3
import json
import os

def scrape_channels():
    """Tüm kanalları içeren liste"""
    
    channels = [
        # ═══════════════════════════════════════════════════
        #                    GENEL KANALLAR
        # ═══════════════════════════════════════════════════
        {'name': 'TRT 1', 'url': 'https://tv-trt1.medya.trt.com.tr/master.m3u8', 'category': 'Genel', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/6/6c/TRT_1_logo_%282012-2021%29.png'},
        {'name': 'TRT 2', 'url': 'https://tv-trt2.medya.trt.com.tr/master_1440.m3u8', 'category': 'Genel'},
        {'name': 'ATV', 'url': 'https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8', 'category': 'Genel', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/7/78/Atv_logosu.png'},
        {'name': 'ATV (Yedek)', 'url': 'https://api.hitnova.net/s/atv/mono.m3u8', 'category': 'Genel'},
        {'name': 'Kanal D', 'url': 'https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba/kanald/kanald_1080p.m3u8', 'category': 'Genel', 'logo': 'https://upload.wikimedia.org/wikipedia/tr/a/a4/Kanal_D_logo.png'},
        {'name': 'Show TV', 'url': 'https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/showtv/showtv.m3u8', 'category': 'Genel', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Logo_of_Show_TV.png'},
        {'name': 'Star TV', 'url': 'https://dygvideo.dygdigital.com/live/hls/startv4puhu', 'category': 'Genel', 'logo': 'https://upload.wikimedia.org/wikipedia/tr/9/92/Star_TV_.png'},
        {'name': 'Kanal 7', 'url': 'https://yurhnwtpys.turknet.ercdn.net/cvmbjbpmdx/kanal7/kanal7_1080p.m3u8', 'category': 'Genel', 'logo': 'https://static.wikia.nocookie.net/logopedia/images/c/ce/Kanal_7_logosu.png'},
        {'name': 'TV8', 'url': 'https://api.hitnova.net/s/tv8/mono.m3u8', 'category': 'Genel', 'logo': 'https://upload.wikimedia.org/wikipedia/tr/6/68/Tv8_Yeni_Logo.png'},
        {'name': 'TV8.5', 'url': 'https://api.hitnova.net/s/tv85/mono.m3u8', 'category': 'Genel'},
        {'name': 'Now TV', 'url': 'https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv_720p.m3u8', 'category': 'Genel'},
        {'name': 'Fox TV', 'url': 'https://api.hitnova.net/s/fox/mono.m3u8', 'category': 'Genel', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/c/c0/FOX_wordmark.svg'},
        {'name': 'TV360', 'url': 'https://api.hitnova.net/s/tv360/mono.m3u8', 'category': 'Genel'},
        {'name': 'Teve2', 'url': 'https://api.hitnova.net/s/teve2/mono.m3u8', 'category': 'Genel'},
        {'name': 'Beyaz TV', 'url': 'https://api.hitnova.net/s/beyaztv/mono.m3u8', 'category': 'Genel'},
        {'name': 'Flash TV', 'url': 'https://api.hitnova.net/s/flashtv/mono.m3u8', 'category': 'Genel'},
        
        # ═══════════════════════════════════════════════════
        #                    HABER KANALLARI
        # ═══════════════════════════════════════════════════
        {'name': 'TRT Haber', 'url': 'https://tv-trthaber.medya.trt.com.tr/master.m3u8', 'category': 'Haber', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/6/6b/TRT_Haber_logosu_%282013-2020%29.png'},
        {'name': 'NTV', 'url': 'https://dogus.daioncdn.net/ntv/ntv_1080p.m3u8', 'category': 'Haber', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/b/b5/NTV_logo.png'},
        {'name': 'Habertürk', 'url': 'https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/haberturktv/haberturktv_1080p.m3u8', 'category': 'Haber', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/7/78/Haberturk_logo.png'},
        {'name': 'Haber Global', 'url': 'https://tv.ensonhaber.com/haberglobal/haberglobal_720p.m3u8', 'category': 'Haber'},
        {'name': 'CNN Türk', 'url': 'https://api.hitnova.net/s/cnnturk/mono.m3u8', 'category': 'Haber'},
        {'name': 'A Haber', 'url': 'https://api.hitnova.net/s/ahaber/mono.m3u8', 'category': 'Haber'},
        {'name': 'TGRT Haber', 'url': 'https://api.hitnova.net/s/tgrthaber/mono.m3u8', 'category': 'Haber'},
        {'name': 'Ulke TV', 'url': 'https://api.hitnova.net/s/ulketv/mono.m3u8', 'category': 'Haber'},
        {'name': 'Halk TV', 'url': 'https://api.hitnova.net/s/halktv/mono.m3u8', 'category': 'Haber'},
        {'name': 'Tele1', 'url': 'https://api.hitnova.net/s/tele1/mono.m3u8', 'category': 'Haber'},
        {'name': 'KRT', 'url': 'https://api.hitnova.net/s/krt/mono.m3u8', 'category': 'Haber'},
        {'name': 'Sözcü TV', 'url': 'https://api.hitnova.net/s/sozcutv/mono.m3u8', 'category': 'Haber'},
        {'name': 'TV100', 'url': 'https://api.hitnova.net/s/tv100/mono.m3u8', 'category': 'Haber'},
        {'name': '24 TV', 'url': 'https://api.hitnova.net/s/24tv/mono.m3u8', 'category': 'Haber'},
        
        # ═══════════════════════════════════════════════════
        #                    SPOR KANALLARI
        # ═══════════════════════════════════════════════════
        {'name': 'TRT Spor', 'url': 'https://api.hitnova.net/s/trtspor/mono.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/c/c4/TRT_Spor_kurumsal_logo.png'},
        {'name': 'TRT Spor 2', 'url': 'https://api.hitnova.net/s/trtspor2/mono.m3u8', 'category': 'Spor'},
        {'name': 'A Spor', 'url': 'https://api.hitnova.net/s/as/mono.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/tr/e/e9/A_Spor_logosu.png'},
        {'name': 'beIN Sports 1', 'url': 'https://api.hitnova.net/s/bein1/mono.m3u8', 'category': 'Spor'},
        {'name': 'beIN Sports 2', 'url': 'https://api.hitnova.net/s/bein2/mono.m3u8', 'category': 'Spor'},
        {'name': 'beIN Sports 3', 'url': 'https://api.hitnova.net/s/bein3/mono.m3u8', 'category': 'Spor'},
        {'name': 'beIN Sports 4', 'url': 'https://api.hitnova.net/s/bein4/mono.m3u8', 'category': 'Spor'},
        {'name': 'S Sport', 'url': 'https://api.hitnova.net/s/ss/mono.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/0/07/S_Sport_logo.png'},
        {'name': 'S Sport 2', 'url': 'https://api.hitnova.net/s/ss2/mono.m3u8', 'category': 'Spor'},
        {'name': 'Smart Spor', 'url': 'https://api.hitnova.net/s/smarts/mono.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/tr/b/b2/SporSMART_HD_logo.png'},
        {'name': 'Smart Spor 2', 'url': 'https://api.hitnova.net/s/sms2/mono.m3u8', 'category': 'Spor'},
        {'name': 'Eurosport 1', 'url': 'https://api.hitnova.net/s/eu1/mono.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Eurosport_1_Logo_2015.png'},
        {'name': 'Eurosport 2', 'url': 'https://api.hitnova.net/s/eu2/mono.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/d/d0/Eurosport_2_Logo_2015.png'},
        {'name': 'Tivibu Spor 1', 'url': 'https://api.hitnova.net/s/t1/mono.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/tr/d/db/TivibuSporLogo1.PNG'},
        {'name': 'Tivibu Spor 2', 'url': 'https://api.hitnova.net/s/t2/mono.m3u8', 'category': 'Spor'},
        {'name': 'Tivibu Spor 3', 'url': 'https://api.hitnova.net/s/t3/mono.m3u8', 'category': 'Spor'},
        {'name': 'CBC Sport', 'url': 'https://andro.2385437.xyz/checklist/androstreamlivecbcs.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/az/0/04/CBC_Sport_TV_loqo.png'},
        {'name': 'Idman TV', 'url': 'https://andro.326503.xyz/checklist/androstreamliveidm.m3u8', 'category': 'Spor', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/0/01/%C4%B0dman_TV_logo.png'},
        {'name': 'NBA TV', 'url': 'https://api.hitnova.net/s/nbatv/mono.m3u8', 'category': 'Spor'},
        
        # ═══════════════════════════════════════════════════
        #                    ÇOCUK KANALLARI
        # ═══════════════════════════════════════════════════
        {'name': 'TRT Çocuk', 'url': 'https://tv-trtcocuk.medya.trt.com.tr/master_1080.m3u8', 'category': 'Çocuk', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/2/23/TRT_%C3%A7ocuk_logo.png'},
        {'name': 'Cartoon Network', 'url': 'https://api.hitnova.net/s/cn/mono.m3u8', 'category': 'Çocuk'},
        {'name': 'Minika Çocuk', 'url': 'https://api.hitnova.net/s/minikac/mono.m3u8', 'category': 'Çocuk'},
        {'name': 'Minika Go', 'url': 'https://api.hitnova.net/s/minikago/mono.m3u8', 'category': 'Çocuk'},
        {'name': 'Disney Channel', 'url': 'https://api.hitnova.net/s/disney/mono.m3u8', 'category': 'Çocuk'},
        
        # ═══════════════════════════════════════════════════
        #                    BELGESEL / KÜLTÜR
        # ═══════════════════════════════════════════════════
        {'name': 'TRT Belgesel', 'url': 'https://api.hitnova.net/s/trtbelgesel/mono.m3u8', 'category': 'Belgesel', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/b/ba/TRT_Belgesel_kurumsal_logo_%282015-2019%29.png'},
        {'name': 'National Geographic', 'url': 'https://api.hitnova.net/s/natgeo/mono.m3u8', 'category': 'Belgesel'},
        {'name': 'Discovery Channel', 'url': 'https://api.hitnova.net/s/discovery/mono.m3u8', 'category': 'Belgesel'},
        {'name': 'History Channel', 'url': 'https://api.hitnova.net/s/history/mono.m3u8', 'category': 'Belgesel'},
        
        # ═══════════════════════════════════════════════════
        #                    MÜZİK KANALLARI
        # ═══════════════════════════════════════════════════
        {'name': 'TRT Müzik', 'url': 'https://api.hitnova.net/s/trtmuzik/mono.m3u8', 'category': 'Müzik'},
        {'name': 'Kral TV', 'url': 'https://api.hitnova.net/s/kraltv/mono.m3u8', 'category': 'Müzik'},
        {'name': 'Kral Pop', 'url': 'https://api.hitnova.net/s/kralpop/mono.m3u8', 'category': 'Müzik'},
        {'name': 'Power Türk', 'url': 'https://api.hitnova.net/s/powerturk/mono.m3u8', 'category': 'Müzik'},
        {'name': 'MTV Türkiye', 'url': 'https://api.hitnova.net/s/mtv/mono.m3u8', 'category': 'Müzik'},
        
        # ═══════════════════════════════════════════════════
        #                    SİNEMA KANALLARI
        # ═══════════════════════════════════════════════════
        {'name': 'Sinema TV', 'url': 'https://api.hitnova.net/s/sinematv/mono.m3u8', 'category': 'Sinema'},
        {'name': 'FX', 'url': 'https://api.hitnova.net/s/fx/mono.m3u8', 'category': 'Sinema'},
        {'name': 'MovieSmart', 'url': 'https://api.hitnova.net/s/moviesmart/mono.m3u8', 'category': 'Sinema'},
        
        # ═══════════════════════════════════════════════════
        #                    DİNİ KANALLAR
        # ═══════════════════════════════════════════════════
        {'name': 'Diyanet TV', 'url': 'https://api.hitnova.net/s/diyanettv/mono.m3u8', 'category': 'Dini'},
        {'name': 'Semerkand TV', 'url': 'https://api.hitnova.net/s/semerkand/mono.m3u8', 'category': 'Dini'},
        
        # ═══════════════════════════════════════════════════
        #                    TRT KANALLARI (Ekstra)
        # ═══════════════════════════════════════════════════
        {'name': 'TRT 1 (Yedek)', 'url': 'https://api.hitnova.net/s/trt1/mono.m3u8', 'category': 'TRT'},
        {'name': 'TRT World', 'url': 'https://api.hitnova.net/s/trtworld/mono.m3u8', 'category': 'TRT'},
        {'name': 'TRT Avaz', 'url': 'https://api.hitnova.net/s/trtavaz/mono.m3u8', 'category': 'TRT'},
        {'name': 'TRT Kurdî', 'url': 'https://api.hitnova.net/s/trtkurdi/mono.m3u8', 'category': 'TRT'},
        {'name': 'TRT Arabi', 'url': 'https://api.hitnova.net/s/trtarabi/mono.m3u8', 'category': 'TRT'},
    ]
    
    # data klasörünü oluştur
    os.makedirs('data', exist_ok=True)
    
    # JSON'a kaydet
    output_file = 'data/scraped_channels.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(channels)} kanal kaydedildi: {output_file}")
    print(f"📄 Dosya boyutu: {os.path.getsize(output_file)} byte")
    
    # Kategori istatistikleri
    categories = {}
    for ch in channels:
        cat = ch.get('category', 'Diğer')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Kategori Dağılımı:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count} kanal")
    
    return channels


if __name__ == "__main__":
    scrape_channels()
