#!/usr/bin/env python3
"""
ÖMER TV - Playlist Generator
Vavoo kanalları kategorize edilmiş şekilde
"""

from datetime import datetime

# TÜM VAVOO KANALLARI (İsim ve URL)
CHANNELS = [
    # ULUSAL
    ("TRT 1 4K", "https://www.vavoo.to/play/3059837792/index.m3u8", "Ulusal"),
    ("TRT 1 HD", "https://www.vavoo.to/play/1221669131/index.m3u8", "Ulusal"),
    ("TRT 1 FHD", "https://www.vavoo.to/play/406666682/index.m3u8", "Ulusal"),
    ("TRT 1", "https://www.vavoo.to/play/2041026135/index.m3u8", "Ulusal"),
    ("TRT 1", "https://www.vavoo.to/play/115261333/index.m3u8", "Ulusal"),
    ("Show TV HD", "https://www.vavoo.to/play/351471337/index.m3u8", "Ulusal"),
    ("Show TV FHD", "https://www.vavoo.to/play/1449499865/index.m3u8", "Ulusal"),
    ("Show TV", "https://www.vavoo.to/play/2395422638/index.m3u8", "Ulusal"),
    ("Show Türk", "https://www.vavoo.to/play/1880270561/index.m3u8", "Ulusal"),
    ("Star TV HD", "https://www.vavoo.to/play/2720556692/index.m3u8", "Ulusal"),
    ("Star TV FHD", "https://www.vavoo.to/play/2020035128/index.m3u8", "Ulusal"),
    ("Star TV", "https://www.vavoo.to/play/863472446/index.m3u8", "Ulusal"),
    ("ATV HD", "https://www.vavoo.to/play/1332310706/index.m3u8", "Ulusal"),
    ("ATV FHD", "https://www.vavoo.to/play/2861010641/index.m3u8", "Ulusal"),
    ("ATV", "https://www.vavoo.to/play/1255594337/index.m3u8", "Ulusal"),
    ("ATV", "https://www.vavoo.to/play/455930425/index.m3u8", "Ulusal"),
    ("ATV Avrupa", "https://www.vavoo.to/play/3195910351/index.m3u8", "Ulusal"),
    ("Kanal D HD", "https://www.vavoo.to/play/1130441933/index.m3u8", "Ulusal"),
    ("Kanal D FHD", "https://www.vavoo.to/play/1781656098/index.m3u8", "Ulusal"),
    ("Kanal D", "https://www.vavoo.to/play/231583905/index.m3u8", "Ulusal"),
    ("Kanal D", "https://www.vavoo.to/play/387232860/index.m3u8", "Ulusal"),
    ("TV8 HD", "https://www.vavoo.to/play/2693299013/index.m3u8", "Ulusal"),
    ("TV8 FHD", "https://www.vavoo.to/play/3849481299/index.m3u8", "Ulusal"),
    ("TV8 HD", "https://www.vavoo.to/play/1702470161/index.m3u8", "Ulusal"),
    ("TV8", "https://www.vavoo.to/play/2196709234/index.m3u8", "Ulusal"),
    ("TV8", "https://www.vavoo.to/play/4292306921/index.m3u8", "Ulusal"),
    ("TV 8.5 HD", "https://www.vavoo.to/play/3472698776/index.m3u8", "Ulusal"),
    ("TV 8.5 FHD", "https://www.vavoo.to/play/1908265816/index.m3u8", "Ulusal"),
    ("TV 8.5", "https://www.vavoo.to/play/14092376/index.m3u8", "Ulusal"),
    ("FOX TV HD", "https://www.vavoo.to/play/1345288490/index.m3u8", "Ulusal"),
    ("FOX TV", "https://www.vavoo.to/play/1498459094/index.m3u8", "Ulusal"),
    ("FOX TV", "https://www.vavoo.to/play/145391758/index.m3u8", "Ulusal"),
    ("NOW TV FHD", "https://www.vavoo.to/play/919108696/index.m3u8", "Ulusal"),
    ("NOW TV HD", "https://www.vavoo.to/play/161305206/index.m3u8", "Ulusal"),
    ("Kanal 7 HD", "https://www.vavoo.to/play/1639889598/index.m3u8", "Ulusal"),
    ("Kanal 7 FHD", "https://www.vavoo.to/play/2736723250/index.m3u8", "Ulusal"),
    ("Kanal 7", "https://www.vavoo.to/play/3015649982/index.m3u8", "Ulusal"),
    ("Kanal 7", "https://www.vavoo.to/play/2842046019/index.m3u8", "Ulusal"),
    ("Kanal 7 Avrupa", "https://www.vavoo.to/play/498645977/index.m3u8", "Ulusal"),
    ("Beyaz TV HD", "https://www.vavoo.to/play/2755756005/index.m3u8", "Ulusal"),
    ("Beyaz TV", "https://www.vavoo.to/play/275850888/index.m3u8", "Ulusal"),
    ("Teve 2", "https://www.vavoo.to/play/2549900211/index.m3u8", "Ulusal"),
    ("360 TV", "https://www.vavoo.to/play/1651455199/index.m3u8", "Ulusal"),
    ("360 TV", "https://www.vavoo.to/play/865410951/index.m3u8", "Ulusal"),
    ("A2 HD", "https://www.vavoo.to/play/867875861/index.m3u8", "Ulusal"),
    ("A2 HD", "https://www.vavoo.to/play/2019055277/index.m3u8", "Ulusal"),
    ("Euro Star", "https://www.vavoo.to/play/1827094680/index.m3u8", "Ulusal"),
    ("Euro Star", "https://www.vavoo.to/play/3814521935/index.m3u8", "Ulusal"),
    ("TRT Türk", "https://www.vavoo.to/play/4098093256/index.m3u8", "Ulusal"),
    ("TRT Müzik", "https://www.vavoo.to/play/2362678422/index.m3u8", "Ulusal"),
    ("Kanal T", "https://www.vavoo.to/play/1831675683/index.m3u8", "Ulusal"),
    ("Ada TV", "https://www.vavoo.to/play/4225961715/index.m3u8", "Ulusal"),
    
    # HABER
    ("CNN Türk HD", "https://www.vavoo.to/play/4273153967/index.m3u8", "Haber"),
    ("CNN Türk", "https://www.vavoo.to/play/3278683973/index.m3u8", "Haber"),
    ("CNN Türk", "https://www.vavoo.to/play/2056768647/index.m3u8", "Haber"),
    ("NTV HD", "https://www.vavoo.to/play/2073292907/index.m3u8", "Haber"),
    ("A Haber HD", "https://www.vavoo.to/play/535272601/index.m3u8", "Haber"),
    ("A Haber", "https://www.vavoo.to/play/1064954896/index.m3u8", "Haber"),
    ("Habertürk HD", "https://www.vavoo.to/play/4253369376/index.m3u8", "Haber"),
    ("TRT Haber HD", "https://www.vavoo.to/play/2579401878/index.m3u8", "Haber"),
    ("TRT Haber", "https://www.vavoo.to/play/1890976041/index.m3u8", "Haber"),
    ("TRT Haber", "https://www.vavoo.to/play/2003703357/index.m3u8", "Haber"),
    ("TRT Haber", "https://www.vavoo.to/play/603651638/index.m3u8", "Haber"),
    ("Haber Global HD", "https://www.vavoo.to/play/1196626387/index.m3u8", "Haber"),
    ("TGRT Haber HD", "https://www.vavoo.to/play/1907154704/index.m3u8", "Haber"),
    ("24 TV HD", "https://www.vavoo.to/play/1998168122/index.m3u8", "Haber"),
    ("24 TV", "https://www.vavoo.to/play/3828793616/index.m3u8", "Haber"),
    ("24 TV", "https://www.vavoo.to/play/1702937932/index.m3u8", "Haber"),
    ("Ülke TV", "https://www.vavoo.to/play/3053206623/index.m3u8", "Haber"),
    ("Ülke TV", "https://www.vavoo.to/play/216740557/index.m3u8", "Haber"),
    ("TVNET HD", "https://www.vavoo.to/play/1182480796/index.m3u8", "Haber"),
    ("TVNET", "https://www.vavoo.to/play/1221661755/index.m3u8", "Haber"),
    ("TVNET HD", "https://www.vavoo.to/play/1738739277/index.m3u8", "Haber"),
    ("Halk TV HD", "https://www.vavoo.to/play/1771999100/index.m3u8", "Haber"),
    ("Halk TV", "https://www.vavoo.to/play/1320391955/index.m3u8", "Haber"),
    ("Sözcü TV", "https://www.vavoo.to/play/960578312/index.m3u8", "Haber"),
    ("TV100", "https://www.vavoo.to/play/3760496907/index.m3u8", "Haber"),
    ("Bloomberg HT HD", "https://www.vavoo.to/play/3152079168/index.m3u8", "Haber"),
    ("Türkhaber TV", "https://www.vavoo.to/play/2012038243/index.m3u8", "Haber"),
    ("Lider Haber", "https://www.vavoo.to/play/703698868/index.m3u8", "Haber"),
    ("Ekol TV", "https://www.vavoo.to/play/2706210049/index.m3u8", "Haber"),
    ("HRT Akdeniz TV", "https://www.vavoo.to/play/4223430509/index.m3u8", "Haber"),
    
    # SPOR
    ("beIN Sports 1 HD", "https://www.vavoo.to/play/662179620/index.m3u8", "Spor"),
    ("beIN Sports 1", "https://www.vavoo.to/play/300113394/index.m3u8", "Spor"),
    ("beIN Sports 1", "https://www.vavoo.to/play/2576216897/index.m3u8", "Spor"),
    ("beIN Sports 1 50 FPS", "https://www.vavoo.to/play/1352421053/index.m3u8", "Spor"),
    ("beIN Sports 1 720P", "https://www.vavoo.to/play/3840475653/index.m3u8", "Spor"),
    ("beIN Sports 2 HD", "https://www.vavoo.to/play/2851539143/index.m3u8", "Spor"),
    ("beIN Sports 2", "https://www.vavoo.to/play/2509466191/index.m3u8", "Spor"),
    ("beIN Sports 2", "https://www.vavoo.to/play/1447241506/index.m3u8", "Spor"),
    ("beIN Sports 3 UHD", "https://www.vavoo.to/play/3410167560/index.m3u8", "Spor"),
    ("beIN Sports 3", "https://www.vavoo.to/play/2834514943/index.m3u8", "Spor"),
    ("beIN Sports 4 UHD", "https://www.vavoo.to/play/2938268353/index.m3u8", "Spor"),
    ("beIN Sports 4", "https://www.vavoo.to/play/3640906370/index.m3u8", "Spor"),
    ("beIN Sports 4", "https://www.vavoo.to/play/450076655/index.m3u8", "Spor"),
    ("beIN Sports 5 FHD", "https://www.vavoo.to/play/4000315601/index.m3u8", "Spor"),
    ("beIN Sports 5", "https://www.vavoo.to/play/3831757618/index.m3u8", "Spor"),
    ("A Spor HD", "https://www.vavoo.to/play/2556711030/index.m3u8", "Spor"),
    ("A Spor FHD", "https://www.vavoo.to/play/911836506/index.m3u8", "Spor"),
    ("A Spor", "https://www.vavoo.to/play/819272696/index.m3u8", "Spor"),
    ("A Spor", "https://www.vavoo.to/play/1771137539/index.m3u8", "Spor"),
    ("TRT Spor HD", "https://www.vavoo.to/play/312904614/index.m3u8", "Spor"),
    ("TRT Spor FHD", "https://www.vavoo.to/play/2952828245/index.m3u8", "Spor"),
    ("TRT Spor", "https://www.vavoo.to/play/2781429267/index.m3u8", "Spor"),
    ("TRT Spor", "https://www.vavoo.to/play/2114335424/index.m3u8", "Spor"),
    ("TRT Spor", "https://www.vavoo.to/play/2262969938/index.m3u8", "Spor"),
    ("TRT Spor Yıldız", "https://www.vavoo.to/play/2750507083/index.m3u8", "Spor"),
    ("S Sport HD", "https://www.vavoo.to/play/919993168/index.m3u8", "Spor"),
    ("S Sport", "https://www.vavoo.to/play/3718336295/index.m3u8", "Spor"),
    ("S Sport", "https://www.vavoo.to/play/3346549722/index.m3u8", "Spor"),
    ("S Sport", "https://www.vavoo.to/play/2123273598/index.m3u8", "Spor"),
    ("S Sport 2", "https://www.vavoo.to/play/1234604880/index.m3u8", "Spor"),
    ("S Sport 2", "https://www.vavoo.to/play/1313768516/index.m3u8", "Spor"),
    ("S Sport 2", "https://www.vavoo.to/play/936908274/index.m3u8", "Spor"),
    ("Spor Smart HD", "https://www.vavoo.to/play/1313563350/index.m3u8", "Spor"),
    ("Spor Smart", "https://www.vavoo.to/play/1771511397/index.m3u8", "Spor"),
    ("Spor Smart 2 HD", "https://www.vavoo.to/play/2726496671/index.m3u8", "Spor"),
    ("Tivibu Spor 1 HD", "https://www.vavoo.to/play/3654518007/index.m3u8", "Spor"),
    ("Tivibu Spor 3 HD", "https://www.vavoo.to/play/2616624010/index.m3u8", "Spor"),
    ("Tivibu Spor 3", "https://www.vavoo.to/play/568442751/index.m3u8", "Spor"),
    ("Tivibu Spor 4 HD", "https://www.vavoo.to/play/3307062704/index.m3u8", "Spor"),
    ("Tabii Spor HD", "https://www.vavoo.to/play/2259480087/index.m3u8", "Spor"),
    ("Tabii Spor", "https://www.vavoo.to/play/184486327/index.m3u8", "Spor"),
    ("Tabii Spor 1", "https://www.vavoo.to/play/1097795141/index.m3u8", "Spor"),
    ("Tabii Spor 2", "https://www.vavoo.to/play/114261141/index.m3u8", "Spor"),
    ("Tabii Spor 3", "https://www.vavoo.to/play/1001346341/index.m3u8", "Spor"),
    ("Tabii Spor 4 HD", "https://www.vavoo.to/play/1375986171/index.m3u8", "Spor"),
    ("Tabii Spor 4", "https://www.vavoo.to/play/2307885365/index.m3u8", "Spor"),
    ("Tabii Spor 6 UHD", "https://www.vavoo.to/play/3713708963/index.m3u8", "Spor"),
    ("Tabii Spor 6 HD", "https://www.vavoo.to/play/270984838/index.m3u8", "Spor"),
    ("Tabii Spor 6", "https://www.vavoo.to/play/4082096725/index.m3u8", "Spor"),
    ("EXXEN Spor 1", "https://www.vavoo.to/play/1842018252/index.m3u8", "Spor"),
    ("EXXEN Spor 1", "https://www.vavoo.to/play/1188258066/index.m3u8", "Spor"),
    ("EXXEN Spor 2", "https://www.vavoo.to/play/3961480108/index.m3u8", "Spor"),
    ("EXXEN Spor 2", "https://www.vavoo.to/play/24320962/index.m3u8", "Spor"),
    ("EXXEN Spor 3", "https://www.vavoo.to/play/3807939453/index.m3u8", "Spor"),
    ("EXXEN Spor 4", "https://www.vavoo.to/play/2771024060/index.m3u8", "Spor"),
    ("EXXEN Spor 5", "https://www.vavoo.to/play/2555007244/index.m3u8", "Spor"),
    ("EXXEN Spor 7", "https://www.vavoo.to/play/3800695404/index.m3u8", "Spor"),
    ("EXXEN Spor 8", "https://www.vavoo.to/play/1624937917/index.m3u8", "Spor"),
    ("Eurosport 1 HD", "https://www.vavoo.to/play/2078862937/index.m3u8", "Spor"),
    ("Eurosport 2 HD", "https://www.vavoo.to/play/4117227962/index.m3u8", "Spor"),
    ("Eurosport 2 HD", "https://www.vavoo.to/play/1821942247/index.m3u8", "Spor"),
    ("NBA TV HD", "https://www.vavoo.to/play/545548133/index.m3u8", "Spor"),
    ("Idman TV HD", "https://www.vavoo.to/play/2368422760/index.m3u8", "Spor"),
    
    # SİNEMA
    ("beIN Movies Action", "https://www.vavoo.to/play/1873478131/index.m3u8", "Sinema"),
    ("beIN Movies Action 2", "https://www.vavoo.to/play/650851542/index.m3u8", "Sinema"),
    ("beIN Movies Premiere 2", "https://www.vavoo.to/play/2244069093/index.m3u8", "Sinema"),
    ("beIN Movies Premiere 2", "https://www.vavoo.to/play/2120218356/index.m3u8", "Sinema"),
    ("beIN Movies Türk", "https://www.vavoo.to/play/3390575948/index.m3u8", "Sinema"),
    ("beIN Movies Türk", "https://www.vavoo.to/play/1835579025/index.m3u8", "Sinema"),
    ("beIN Box Office 1", "https://www.vavoo.to/play/1320363850/index.m3u8", "Sinema"),
    ("beIN Box Office 3", "https://www.vavoo.to/play/879981610/index.m3u8", "Sinema"),
    ("Sinema Aile", "https://www.vavoo.to/play/4245508443/index.m3u8", "Sinema"),
    ("Sinema Komedi", "https://www.vavoo.to/play/257449668/index.m3u8", "Sinema"),
    ("Sinema 1002", "https://www.vavoo.to/play/4269042044/index.m3u8", "Sinema"),
    ("FX", "https://www.vavoo.to/play/2851147991/index.m3u8", "Sinema"),
    ("Fix Cinema Action", "https://www.vavoo.to/play/140294889/index.m3u8", "Sinema"),
    ("Fix Cinema Comedy", "https://www.vavoo.to/play/4140720869/index.m3u8", "Sinema"),
    ("Fix Cinema Yerli", "https://www.vavoo.to/play/239201347/index.m3u8", "Sinema"),
    ("Fix Cinema Yeşilçam", "https://www.vavoo.to/play/4110861662/index.m3u8", "Sinema"),
    ("Sinemax Türk", "https://www.vavoo.to/play/4201568953/index.m3u8", "Sinema"),
    ("Movie Smart Classic", "https://www.vavoo.to/play/3597292408/index.m3u8", "Sinema"),
    
    # DİZİ
    ("beIN Series 1", "https://www.vavoo.to/play/2190922298/index.m3u8", "Dizi"),
    ("beIN Series 2", "https://www.vavoo.to/play/3308693738/index.m3u8", "Dizi"),
    ("beIN Series 3", "https://www.vavoo.to/play/4166418778/index.m3u8", "Dizi"),
    ("beIN Series Comedy", "https://www.vavoo.to/play/1668144911/index.m3u8", "Dizi"),
    ("beIN Series Sci-Fi", "https://www.vavoo.to/play/3016529666/index.m3u8", "Dizi"),
    ("Dizi Smart Premium", "https://www.vavoo.to/play/791616758/index.m3u8", "Dizi"),
    ("Epic Drama", "https://www.vavoo.to/play/678261693/index.m3u8", "Dizi"),
    
    # BELGESEL
    ("TRT Belgesel", "https://www.vavoo.to/play/599757405/index.m3u8", "Belgesel"),
    ("TRT Belgesel", "https://www.vavoo.to/play/2439012215/index.m3u8", "Belgesel"),
    ("TGRT Belgesel", "https://www.vavoo.to/play/1743993546/index.m3u8", "Belgesel"),
    ("National Geographic HD", "https://www.vavoo.to/play/1078355325/index.m3u8", "Belgesel"),
    ("Nat Geo Wild HD", "https://www.vavoo.to/play/132416616/index.m3u8", "Belgesel"),
    ("Discovery Channel HD", "https://www.vavoo.to/play/4017734592/index.m3u8", "Belgesel"),
    ("DMAX", "https://www.vavoo.to/play/3239529951/index.m3u8", "Belgesel"),
    ("DMAX HD", "https://www.vavoo.to/play/869937351/index.m3u8", "Belgesel"),
    ("BBC Earth", "https://www.vavoo.to/play/2618455562/index.m3u8", "Belgesel"),
    ("BBC Earth", "https://www.vavoo.to/play/2613731614/index.m3u8", "Belgesel"),
    ("beIN iZ", "https://www.vavoo.to/play/1691223078/index.m3u8", "Belgesel"),
    ("TLC", "https://www.vavoo.to/play/951448076/index.m3u8", "Belgesel"),
    ("TLC", "https://www.vavoo.to/play/1766840660/index.m3u8", "Belgesel"),
    ("Viasat History", "https://www.vavoo.to/play/1900945213/index.m3u8", "Belgesel"),
    ("Investigation Discovery", "https://www.vavoo.to/play/1372455233/index.m3u8", "Belgesel"),
    
    # ÇOCUK
    ("TRT Çocuk HD", "https://www.vavoo.to/play/3029180506/index.m3u8", "Çocuk"),
    ("Cartoon Network", "https://www.vavoo.to/play/3278185898/index.m3u8", "Çocuk"),
    ("Disney Junior", "https://www.vavoo.to/play/649228722/index.m3u8", "Çocuk"),
    ("Nicktoons", "https://www.vavoo.to/play/988691374/index.m3u8", "Çocuk"),
    ("Boomerang", "https://www.vavoo.to/play/3510107618/index.m3u8", "Çocuk"),
    ("Baby TV", "https://www.vavoo.to/play/1758313456/index.m3u8", "Çocuk"),
    ("Minika Çocuk", "https://www.vavoo.to/play/3036231687/index.m3u8", "Çocuk"),
    
    # MÜZİK
    ("Kral TV HD", "https://www.vavoo.to/play/2879812830/index.m3u8", "Müzik"),
    ("Kral TV", "https://www.vavoo.to/play/1505032467/index.m3u8", "Müzik"),
    ("Kral TV", "https://www.vavoo.to/play/1131281902/index.m3u8", "Müzik"),
    ("Kral Pop", "https://www.vavoo.to/play/4169838993/index.m3u8", "Müzik"),
    ("Number1 Türk HD", "https://www.vavoo.to/play/4042887584/index.m3u8", "Müzik"),
    ("Dream Türk", "https://www.vavoo.to/play/4266683025/index.m3u8", "Müzik"),
]

def create_m3u():
    """M3U dosyası oluştur"""
    
    print("=" * 60)
    print("ÖMER TV - Playlist Generator")
    print("=" * 60)
    
    # Kategorilere ayır
    categories = {}
    for name, url, cat in CHANNELS:
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, url))
    
    # İstatistik
    total = len(CHANNELS)
    print(f"\n✅ {total} kanal yüklendi\n")
    print("📊 Kategoriler:")
    for cat in sorted(categories.keys()):
        print(f"   {cat:15s}: {len(categories[cat]):3d} kanal")
    
    # M3U oluştur
    content = '#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n'
    content += f'# ÖMER TV - Premium IPTV\n'
    content += f'# Güncelleme: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n'
    content += f'# Toplam: {total} kanal\n\n'
    
    # Kategori sırası
    order = ['Ulusal', 'Haber', 'Spor', 'Sinema', 'Dizi', 'Belgesel', 'Çocuk', 'Müzik']
    
    for cat in order:
        if cat in categories:
            content += f'\n#########################################\n'
            content += f'# {cat.upper()} ({len(categories[cat])} kanal)\n'
            content += f'#########################################\n\n'
            
            for name, url in sorted(categories[cat], key=lambda x: x[0]):
                content += f'#EXTINF:-1 group-title="{cat}",{name}\n'
                content += f'{url}\n'
    
    # Kaydet
    with open('channels.m3u', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ channels.m3u oluşturuldu!")
    print(f"\n🔗 Link: https://raw.githubusercontent.com/titkenan/Omer_TV/main/channels.m3u")

if __name__ == "__main__":
    create_m3u()
