#!/usr/bin/env python3
"""
Vavoo Listesini Olduğu Gibi Ekle
Tüm kanallar, tüm kategoriler
"""

import re
from datetime import datetime

# Senin verdiğin tam liste
RAW_VAVOO_DATA = """#EXTM3U 
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
#EXTINF:-1 tvg-name="4K TR: SOZCU TV ", 4K TR: SOZCU TV 
https://www.vavoo.to/play/960578312/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 50 FPS ", BEIN SPORTS 1 50 FPS 
https://www.vavoo.to/play/1352421053/index.m3u8
#EXTINF:-1 tvg-name="STAR TV HD ", STAR TV HD 
https://www.vavoo.to/play/2720556692/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 (720P) ", BEIN SPORTS 1 (720P) 
https://www.vavoo.to/play/3840475653/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV HD ", SHOW TV HD 
https://www.vavoo.to/play/351471337/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 HD ", TRT 1 HD 
https://www.vavoo.to/play/1221669131/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 (720PFEED) ", BEIN SPORTS 1 (720PFEED) 
https://www.vavoo.to/play/2233066433/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPOR 1 SD ", EXXEN SPOR 1 SD 
https://www.vavoo.to/play/2024568982/index.m3u8
#EXTINF:-1 tvg-name="EXXEN TV SPOR 8 ", EXXEN TV SPOR 8 
https://www.vavoo.to/play/1159078202/index.m3u8
#EXTINF:-1 tvg-name="4K TR: HALK TV ", 4K TR: HALK TV 
https://www.vavoo.to/play/1320391955/index.m3u8
#EXTINF:-1 tvg-name="HALK TV HD ", HALK TV HD 
https://www.vavoo.to/play/1771999100/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA KOMED HD ", 4K TR: S NEMA KOMED HD 
https://www.vavoo.to/play/440774949/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S SPORT ", 4K TR: S SPORT 
https://www.vavoo.to/play/2123273598/index.m3u8
#EXTINF:-1 tvg-name="FOX ", FOX 
https://www.vavoo.to/play/1498459094/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV ", SHOW TV 
https://www.vavoo.to/play/2395422638/index.m3u8
#EXTINF:-1 tvg-name="TRT SPOR HD ", TRT SPOR HD 
https://www.vavoo.to/play/312904614/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV FHD ", SHOW TV FHD 
https://www.vavoo.to/play/1449499865/index.m3u8
#EXTINF:-1 tvg-name="TRT SPOR RAW ", TRT SPOR RAW 
https://www.vavoo.to/play/601788690/index.m3u8
#EXTINF:-1 tvg-name="EURO STAR ", EURO STAR 
https://www.vavoo.to/play/1827094680/index.m3u8
#EXTINF:-1 tvg-name="4K TR: 360 HD ", 4K TR: 360 HD 
https://www.vavoo.to/play/473300573/index.m3u8
#EXTINF:-1 tvg-name="STAR HD SD ", STAR HD SD 
https://www.vavoo.to/play/3209892863/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 ", BEIN SPORTS 1 
https://www.vavoo.to/play/300113394/index.m3u8
#EXTINF:-1 tvg-name="ATV ", ATV 
https://www.vavoo.to/play/1255594337/index.m3u8
#EXTINF:-1 tvg-name="KANAL D HD ", KANAL D HD 
https://www.vavoo.to/play/1130441933/index.m3u8
#EXTINF:-1 tvg-name="BEIN 1 SD (480P) ", BEIN 1 SD (480P) 
https://www.vavoo.to/play/2919229346/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NTV HD ", 4K TR: NTV HD 
https://www.vavoo.to/play/2073292907/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NUMBER1 TURK HD ", 4K TR: NUMBER1 TURK HD 
https://www.vavoo.to/play/4042887584/index.m3u8
#EXTINF:-1 tvg-name="ATV ", ATV 
https://www.vavoo.to/play/455930425/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 ", TRT 1 
https://www.vavoo.to/play/2041026135/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA TV AKS YON HD ", 4K TR: S NEMA TV AKS YON HD 
https://www.vavoo.to/play/2246993811/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TGRT HABER HD ", 4K TR: TGRT HABER HD 
https://www.vavoo.to/play/1907154704/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 HD ", BEIN SPORTS 1 HD 
https://www.vavoo.to/play/662179620/index.m3u8
#EXTINF:-1 tvg-name="4K TR: DMAX HD ", 4K TR: DMAX HD 
https://www.vavoo.to/play/869937351/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 FHD ", TRT 1 FHD 
https://www.vavoo.to/play/406666682/index.m3u8
#EXTINF:-1 tvg-name="4K TR: AK T TV HD ", 4K TR: AK T TV HD 
https://www.vavoo.to/play/3445585687/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S SPORT 2 ", 4K TR: S SPORT 2 
https://www.vavoo.to/play/936908274/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA TV 1001 HD ", 4K TR: S NEMA TV 1001 HD 
https://www.vavoo.to/play/2761385166/index.m3u8
#EXTINF:-1 tvg-name="A SPOR ", A SPOR 
https://www.vavoo.to/play/819272696/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA TV 2 HD ", 4K TR: S NEMA TV 2 HD 
https://www.vavoo.to/play/295060524/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 2 [LIVE DURING EVENTS ONLY] ", EXXEN SPORTS 2 [LIVE DURING EVENTS ONLY] 
https://www.vavoo.to/play/3961480108/index.m3u8
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
#EXTINF:-1 tvg-name="4K TR: S NEMA AKS YON 2 HD ", 4K TR: S NEMA AKS YON 2 HD 
https://www.vavoo.to/play/3440711580/index.m3u8
#EXTINF:-1 tvg-name="KANAL D FHD ", KANAL D FHD 
https://www.vavoo.to/play/1781656098/index.m3u8
#EXTINF:-1 tvg-name="S SPORT 2 ", S SPORT 2 
https://www.vavoo.to/play/1234604880/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 8K FEED ", BEIN SPORTS 8K FEED 
https://www.vavoo.to/play/2113462398/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA 1002 HD ", 4K TR: S NEMA 1002 HD 
https://www.vavoo.to/play/1076643856/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 ", KANAL 7 
https://www.vavoo.to/play/3015649982/index.m3u8
#EXTINF:-1 tvg-name="S SPORT ", S SPORT 
https://www.vavoo.to/play/3718336295/index.m3u8
#EXTINF:-1 tvg-name="STAR TV ", STAR TV 
https://www.vavoo.to/play/863472446/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NATIONAL GEOGRAPHIC WILD HD ", 4K TR: NATIONAL GEOGRAPHIC WILD HD 
https://www.vavoo.to/play/132416616/index.m3u8
#EXTINF:-1 tvg-name="SOZCU SZC TV SD ", SOZCU SZC TV SD 
https://www.vavoo.to/play/1098172953/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 ", TRT 1 
https://www.vavoo.to/play/115261333/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER ", TRT HABER 
https://www.vavoo.to/play/1890976041/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TEVE2 HD ", 4K TR: TEVE2 HD 
https://www.vavoo.to/play/1917502631/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NBA TV HD ", 4K TR: NBA TV HD 
https://www.vavoo.to/play/545548133/index.m3u8
#EXTINF:-1 tvg-name="BEIN SERIES 1 ", BEIN SERIES 1 
https://www.vavoo.to/play/2190922298/index.m3u8
#EXTINF:-1 tvg-name="S-SPORT HD ", S-SPORT HD 
https://www.vavoo.to/play/919993168/index.m3u8
#EXTINF:-1 tvg-name="24 ", 24 
https://www.vavoo.to/play/1702937932/index.m3u8
#EXTINF:-1 tvg-name="FOX ", FOX 
https://www.vavoo.to/play/145391758/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 720P FEED ", BEIN SPORTS 720P FEED 
https://www.vavoo.to/play/499485497/index.m3u8
#EXTINF:-1 tvg-name="KRAL TV ", KRAL TV 
https://www.vavoo.to/play/1131281902/index.m3u8
#EXTINF:-1 tvg-name="TRT SPOR ", TRT SPOR 
https://www.vavoo.to/play/2114335424/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 4 ", BEIN SPORTS 4 
https://www.vavoo.to/play/3640906370/index.m3u8
#EXTINF:-1 tvg-name="YABAN ", YABAN 
https://www.vavoo.to/play/3338159581/index.m3u8
#EXTINF:-1 tvg-name="ATV EUROPA ", ATV EUROPA 
https://www.vavoo.to/play/90085139/index.m3u8
#EXTINF:-1 tvg-name="FOX TV HD (H265) ", FOX TV HD (H265) 
https://www.vavoo.to/play/1345288490/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 5 FHD ", BEIN SPORTS 5 FHD 
https://www.vavoo.to/play/4000315601/index.m3u8
#EXTINF:-1 tvg-name="4K TR: BLOOMBERG HT HD ", 4K TR: BLOOMBERG HT HD 
https://www.vavoo.to/play/3152079168/index.m3u8
#EXTINF:-1 tvg-name="HALK TV ", HALK TV 
https://www.vavoo.to/play/4148513719/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TV100 ", 4K TR: TV100 
https://www.vavoo.to/play/3760496907/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV ", BEYAZ TV 
https://www.vavoo.to/play/275850888/index.m3u8
#EXTINF:-1 tvg-name="A SPOR FHD ", A SPOR FHD 
https://www.vavoo.to/play/911836506/index.m3u8
#EXTINF:-1 tvg-name="4K TR: 24 HD ", 4K TR: 24 HD 
https://www.vavoo.to/play/1998168122/index.m3u8
#EXTINF:-1 tvg-name="S ZC SZC TV ", S ZC SZC TV 
https://www.vavoo.to/play/2466905700/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA A LE 2 HD ", 4K TR: S NEMA A LE 2 HD 
https://www.vavoo.to/play/3000594763/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA BILM KURGU ", FIX CINEMA BILM KURGU 
https://www.vavoo.to/play/2480231926/index.m3u8
#EXTINF:-1 tvg-name="BEIN 1 SD (360P) ", BEIN 1 SD (360P) 
https://www.vavoo.to/play/3692337241/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 H265 ", BEIN SPORTS 1 H265 
https://www.vavoo.to/play/2403425031/index.m3u8
#EXTINF:-1 tvg-name="4K TR: EPIC DRAMA ", 4K TR: EPIC DRAMA 
https://www.vavoo.to/play/678261693/index.m3u8
#EXTINF:-1 tvg-name="4K TR: EUROSPORT 1 HD ", 4K TR: EUROSPORT 1 HD 
https://www.vavoo.to/play/2078862937/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TRT M Z K ", 4K TR: TRT M Z K 
https://www.vavoo.to/play/970382162/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA YERL 2 HD ", 4K TR: S NEMA YERL 2 HD 
https://www.vavoo.to/play/3971603427/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TRT SPOR YILDIZ ", 4K TR: TRT SPOR YILDIZ 
https://www.vavoo.to/play/2750507083/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 2 ", EXXEN SPORTS 2 
https://www.vavoo.to/play/24320962/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 3 ", BEIN SPORTS 3 
https://www.vavoo.to/play/2834514943/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA NETFLIX ", FIX CINEMA NETFLIX 
https://www.vavoo.to/play/3216985800/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 2 ", BEIN SPORTS 2 
https://www.vavoo.to/play/2509466191/index.m3u8
#EXTINF:-1 tvg-name="24 KITCHEN ", 24 KITCHEN 
https://www.vavoo.to/play/3295699287/index.m3u8
#EXTINF:-1 tvg-name="HORROR 1 HD ", HORROR 1 HD 
https://www.vavoo.to/play/3611975312/index.m3u8
#EXTINF:-1 tvg-name="ÜLKE TV ", ÜLKE TV 
https://www.vavoo.to/play/3053206623/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 4 ", EXXEN SPORTS 4 
https://www.vavoo.to/play/2771024060/index.m3u8
#EXTINF:-1 tvg-name="TV 85 ", TV 85 
https://www.vavoo.to/play/2159436641/index.m3u8
#EXTINF:-1 tvg-name="TV 8.5 FHD ", TV 8.5 FHD 
https://www.vavoo.to/play/1908265816/index.m3u8
#EXTINF:-1 tvg-name="4K TR: BOOMERANG ", 4K TR: BOOMERANG 
https://www.vavoo.to/play/3510107618/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 6 UHD ", TABII SPOR 6 UHD 
https://www.vavoo.to/play/3713708963/index.m3u8
#EXTINF:-1 tvg-name="SPOR SMART ", SPOR SMART 
https://www.vavoo.to/play/1771511397/index.m3u8
#EXTINF:-1 tvg-name="GURBET24 TV ", GURBET24 TV 
https://www.vavoo.to/play/55116964/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR HD ", TABII SPOR HD 
https://www.vavoo.to/play/2259480087/index.m3u8
#EXTINF:-1 tvg-name="SHOW MAX ", SHOW MAX 
https://www.vavoo.to/play/2196278652/index.m3u8
#EXTINF:-1 tvg-name="YABAN TV ", YABAN TV 
https://www.vavoo.to/play/4204615990/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NICKTOONS ", 4K TR: NICKTOONS 
https://www.vavoo.to/play/988691374/index.m3u8
#EXTINF:-1 tvg-name="NOW ", NOW 
https://www.vavoo.to/play/3105184056/index.m3u8
#EXTINF:-1 tvg-name="NR 1 HD ", NR 1 HD 
https://www.vavoo.to/play/4021287013/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA YESILCAM ", FIX CINEMA YESILCAM 
https://www.vavoo.to/play/4110861662/index.m3u8
#EXTINF:-1 tvg-name="ATV HEVC ", ATV HEVC 
https://www.vavoo.to/play/3511150491/index.m3u8
#EXTINF:-1 tvg-name="4K TR: KANAL 7 HD ", 4K TR: KANAL 7 HD 
https://www.vavoo.to/play/1092667959/index.m3u8
#EXTINF:-1 tvg-name="TRT BELGESEL ", TRT BELGESEL 
https://www.vavoo.to/play/599757405/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 HD (TURKEY) ", BEIN SPORTS 1 HD (TURKEY) 
https://www.vavoo.to/play/593493860/index.m3u8
#EXTINF:-1 tvg-name="TRANSFORMERS ", TRANSFORMERS 
https://www.vavoo.to/play/3939293866/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 1 ", EXXEN SPORTS 1 
https://www.vavoo.to/play/1842018252/index.m3u8
#EXTINF:-1 tvg-name="KRAL POP ", KRAL POP 
https://www.vavoo.to/play/4169838993/index.m3u8
#EXTINF:-1 tvg-name="TV 8 INT ", TV 8 INT 
https://www.vavoo.to/play/137677598/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 4K FEED(UYDU) ", BEIN SPORTS 4K FEED(UYDU) 
https://www.vavoo.to/play/1536730627/index.m3u8
#EXTINF:-1 tvg-name="S SPORT ", S SPORT 
https://www.vavoo.to/play/3346549722/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TV 4 ", 4K TR: TV 4 
https://www.vavoo.to/play/357442962/index.m3u8
#EXTINF:-1 tvg-name="HALK TV SD ", HALK TV SD 
https://www.vavoo.to/play/9403684/index.m3u8
#EXTINF:-1 tvg-name="BEIN SERIES 3 ", BEIN SERIES 3 
https://www.vavoo.to/play/4166418778/index.m3u8
#EXTINF:-1 tvg-name="FASIL NEVIZADE GECELERI ", FASIL NEVIZADE GECELERI 
https://www.vavoo.to/play/3597878428/index.m3u8
#EXTINF:-1 tvg-name="TÜRKHABER TV ", TÜRKHABER TV 
https://www.vavoo.to/play/2012038243/index.m3u8
#EXTINF:-1 tvg-name="SINEMA AILE 1 ", SINEMA AILE 1 
https://www.vavoo.to/play/4245508443/index.m3u8
#EXTINF:-1 tvg-name="SPOR SMART 2 HD ", SPOR SMART 2 HD 
https://www.vavoo.to/play/2726496671/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 6 ", TABII SPOR 6 
https://www.vavoo.to/play/4082096725/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 5 ", BEIN SPORTS 5 
https://www.vavoo.to/play/3831757618/index.m3u8
#EXTINF:-1 tvg-name="KANAL D HD (H265) ", KANAL D HD (H265) 
https://www.vavoo.to/play/1371306270/index.m3u8
#EXTINF:-1 tvg-name="TRT MUZIK ", TRT MUZIK 
https://www.vavoo.to/play/2362678422/index.m3u8
#EXTINF:-1 tvg-name="CNN TURK ", CNN TURK 
https://www.vavoo.to/play/3278683973/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 FHD ", KANAL 7 FHD 
https://www.vavoo.to/play/2736723250/index.m3u8
#EXTINF:-1 tvg-name="BEIN MOVIES ACTION ", BEIN MOVIES ACTION 
https://www.vavoo.to/play/1873478131/index.m3u8
#EXTINF:-1 tvg-name="EURO STAR ", EURO STAR 
https://www.vavoo.to/play/3814521935/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 2 ", BEIN SPORTS 2 
https://www.vavoo.to/play/1447241506/index.m3u8
#EXTINF:-1 tvg-name="EXXEN TV SPOR 7 ", EXXEN TV SPOR 7 
https://www.vavoo.to/play/3343300331/index.m3u8
#EXTINF:-1 tvg-name="TGRT BELGESEL ", TGRT BELGESEL 
https://www.vavoo.to/play/1743993546/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 2 ", TABII SPOR 2 
https://www.vavoo.to/play/114261141/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER HD ", TRT HABER HD 
https://www.vavoo.to/play/2579401878/index.m3u8
#EXTINF:-1 tvg-name="SINEMA KOMEDI ", SINEMA KOMEDI 
https://www.vavoo.to/play/257449668/index.m3u8
#EXTINF:-1 tvg-name="BEIN MOVIES PREMIERE 2 ", BEIN MOVIES PREMIERE 2 
https://www.vavoo.to/play/2244069093/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 3 ", TABII SPOR 3 
https://www.vavoo.to/play/1001346341/index.m3u8
#EXTINF:-1 tvg-name="KANAL D ", KANAL D 
https://www.vavoo.to/play/387232860/index.m3u8
#EXTINF:-1 tvg-name="KANAL D HEVC ", KANAL D HEVC 
https://www.vavoo.to/play/4113822297/index.m3u8
#EXTINF:-1 tvg-name="TRT 2 UHD ", TRT 2 UHD 
https://www.vavoo.to/play/2005305132/index.m3u8
#EXTINF:-1 tvg-name="TLC TV ", TLC TV 
https://www.vavoo.to/play/3281641786/index.m3u8
#EXTINF:-1 tvg-name="EXXEN TV SPOR 5 ", EXXEN TV SPOR 5 
https://www.vavoo.to/play/3179734411/index.m3u8
#EXTINF:-1 tvg-name="TRT MUZIK HD+ ", TRT MUZIK HD+ 
https://www.vavoo.to/play/3063329534/index.m3u8
#EXTINF:-1 tvg-name="CNN T RK RAW ", CNN T RK RAW 
https://www.vavoo.to/play/3583754923/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 3 UHD ", BEIN SPORTS 3 UHD 
https://www.vavoo.to/play/3410167560/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 ", KANAL 7 
https://www.vavoo.to/play/2842046019/index.m3u8
#EXTINF:-1 tvg-name="TRT SPOR FHD ", TRT SPOR FHD 
https://www.vavoo.to/play/2952828245/index.m3u8
#EXTINF:-1 tvg-name="TIVIBU SPOR 4 HD ", TIVIBU SPOR 4 HD 
https://www.vavoo.to/play/3307062704/index.m3u8
#EXTINF:-1 tvg-name="TRT TURK ", TRT TURK 
https://www.vavoo.to/play/4098093256/index.m3u8
#EXTINF:-1 tvg-name="4K TR: BABYTV ", 4K TR: BABYTV 
https://www.vavoo.to/play/1758313456/index.m3u8
#EXTINF:-1 tvg-name="DMAX ", DMAX 
https://www.vavoo.to/play/3239529951/index.m3u8
#EXTINF:-1 tvg-name="4K TR: EXXEN TV ", 4K TR: EXXEN TV 
https://www.vavoo.to/play/194469526/index.m3u8
#EXTINF:-1 tvg-name="BEIN IZ ", BEIN IZ 
https://www.vavoo.to/play/1691223078/index.m3u8
#EXTINF:-1 tvg-name="BEIN BOX OFFICE 1 ", BEIN BOX OFFICE 1 
https://www.vavoo.to/play/1320363850/index.m3u8
#EXTINF:-1 tvg-name="4K TR: A2 HD ", 4K TR: A2 HD 
https://www.vavoo.to/play/2019055277/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA ACTION ", FIX CINEMA ACTION 
https://www.vavoo.to/play/140294889/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV HEVC ", BEYAZ TV HEVC 
https://www.vavoo.to/play/1510783901/index.m3u8
#EXTINF:-1 tvg-name="360 ", 360 
https://www.vavoo.to/play/1651455199/index.m3u8
#EXTINF:-1 tvg-name="STAR TV HEVC ", STAR TV HEVC 
https://www.vavoo.to/play/138632579/index.m3u8
#EXTINF:-1 tvg-name="SHOW HD (H265) ", SHOW HD (H265) 
https://www.vavoo.to/play/3537232978/index.m3u8
#EXTINF:-1 tvg-name="TRT TURK ", TRT TURK 
https://www.vavoo.to/play/797768731/index.m3u8
#EXTINF:-1 tvg-name="A HABER HEVC ", A HABER HEVC 
https://www.vavoo.to/play/3766846723/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 2 HD ", BEIN SPORTS 2 HD 
https://www.vavoo.to/play/2851539143/index.m3u8
#EXTINF:-1 tvg-name="TIVIBU SPOR 3 ", TIVIBU SPOR 3 
https://www.vavoo.to/play/568442751/index.m3u8
#EXTINF:-1 tvg-name="BEIN GURME ", BEIN GURME 
https://www.vavoo.to/play/3583230858/index.m3u8
#EXTINF:-1 tvg-name="GLOBAL BOX KORKU ", GLOBAL BOX KORKU 
https://www.vavoo.to/play/562681030/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER ", TRT HABER 
https://www.vavoo.to/play/2003703357/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 HEVC ", KANAL 7 HEVC 
https://www.vavoo.to/play/3897412802/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TRT OCUK HD ", 4K TR: TRT OCUK HD 
https://www.vavoo.to/play/3029180506/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPOTS1 SD ", BEIN SPOTS1 SD 
https://www.vavoo.to/play/143239535/index.m3u8
#EXTINF:-1 tvg-name="BEIN SERIES SCI-FI ", BEIN SERIES SCI-FI 
https://www.vavoo.to/play/3016529666/index.m3u8
#EXTINF:-1 tvg-name="360 ", 360 
https://www.vavoo.to/play/865410951/index.m3u8
#EXTINF:-1 tvg-name="FX ", FX 
https://www.vavoo.to/play/2851147991/index.m3u8
#EXTINF:-1 tvg-name="BEIN MOVIES TURK ", BEIN MOVIES TURK 
https://www.vavoo.to/play/3390575948/index.m3u8
#EXTINF:-1 tvg-name="TEVE 2 ", TEVE 2 
https://www.vavoo.to/play/2549900211/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA YERLI ", FIX CINEMA YERLI 
https://www.vavoo.to/play/239201347/index.m3u8
#EXTINF:-1 tvg-name="KANAL D SD ", KANAL D SD 
https://www.vavoo.to/play/712040085/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ HD+ SD ", BEYAZ HD+ SD 
https://www.vavoo.to/play/1020985035/index.m3u8
#EXTINF:-1 tvg-name="4K TR: NATIONAL GEOGRAPHIC HD ", 4K TR: NATIONAL GEOGRAPHIC HD 
https://www.vavoo.to/play/1078355325/index.m3u8
#EXTINF:-1 tvg-name="TVNET ", TVNET 
https://www.vavoo.to/play/1221661755/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA TV HD ", 4K TR: S NEMA TV HD 
https://www.vavoo.to/play/2780830033/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 1 720P ", TABII SPOR 1 720P 
https://www.vavoo.to/play/3665914763/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 1 ", TABII SPOR 1 
https://www.vavoo.to/play/1097795141/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 4K ", TRT 1 4K 
https://www.vavoo.to/play/3059837792/index.m3u8
#EXTINF:-1 tvg-name="BEYAZ TV HD ", BEYAZ TV HD 
https://www.vavoo.to/play/2755756005/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV RAW ", SHOW TV RAW 
https://www.vavoo.to/play/3317405854/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA A LE HD ", 4K TR: S NEMA A LE HD 
https://www.vavoo.to/play/698495811/index.m3u8
#EXTINF:-1 tvg-name="BEIN BOX OFFICE 3 ", BEIN BOX OFFICE 3 
https://www.vavoo.to/play/879981610/index.m3u8
#EXTINF:-1 tvg-name="GLOBAL BOX YERLI ", GLOBAL BOX YERLI 
https://www.vavoo.to/play/2322262210/index.m3u8
#EXTINF:-1 tvg-name="TVNET HD ", TVNET HD 
https://www.vavoo.to/play/1182480796/index.m3u8
#EXTINF:-1 tvg-name="NAT GEO WILD HD+ ", NAT GEO WILD HD+ 
https://www.vavoo.to/play/124345657/index.m3u8
#EXTINF:-1 tvg-name="4K TR: CARTOON NETWORK ", 4K TR: CARTOON NETWORK 
https://www.vavoo.to/play/3278185898/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 4 UHD ", BEIN SPORTS 4 UHD 
https://www.vavoo.to/play/2938268353/index.m3u8
#EXTINF:-1 tvg-name="4K TR: EUROSPORT 2 HD ", 4K TR: EUROSPORT 2 HD 
https://www.vavoo.to/play/4117227962/index.m3u8
#EXTINF:-1 tvg-name="ATV RAW ", ATV RAW 
https://www.vavoo.to/play/962169494/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 RAW ", TRT 1 RAW 
https://www.vavoo.to/play/2346924541/index.m3u8
#EXTINF:-1 tvg-name="BBC EARTH ", BBC EARTH 
https://www.vavoo.to/play/2618455562/index.m3u8
#EXTINF:-1 tvg-name="TRT 1 SD ", TRT 1 SD 
https://www.vavoo.to/play/566281043/index.m3u8
#EXTINF:-1 tvg-name="HABERTURK RAW ", HABERTURK RAW 
https://www.vavoo.to/play/2129890787/index.m3u8
#EXTINF:-1 tvg-name="A2 HD ", A2 HD 
https://www.vavoo.to/play/867875861/index.m3u8
#EXTINF:-1 tvg-name="4K TR: DISNEY JUNIOR ", 4K TR: DISNEY JUNIOR 
https://www.vavoo.to/play/649228722/index.m3u8
#EXTINF:-1 tvg-name="A SPOR RAW ", A SPOR RAW 
https://www.vavoo.to/play/2777121053/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS FEED (OZEL FEED YAYIN) ", BEIN SPORTS FEED (OZEL FEED YAYIN) 
https://www.vavoo.to/play/1453692314/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 1 ", EXXEN SPORTS 1 
https://www.vavoo.to/play/1188258066/index.m3u8
#EXTINF:-1 tvg-name="SINEMA 1002 ", SINEMA 1002 
https://www.vavoo.to/play/4269042044/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TRT AVAZ ", 4K TR: TRT AVAZ 
https://www.vavoo.to/play/2990410352/index.m3u8
#EXTINF:-1 tvg-name="4K TR: S NEMA YERL HD ", 4K TR: S NEMA YERL HD 
https://www.vavoo.to/play/1897159473/index.m3u8
#EXTINF:-1 tvg-name="EUROSPORT2 HD ", EUROSPORT2 HD 
https://www.vavoo.to/play/1821942247/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 3 [LIVE DURING EVENTS ONLY] ", EXXEN SPORTS 3 [LIVE DURING EVENTS ONLY] 
https://www.vavoo.to/play/3807939453/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR ", TABII SPOR 
https://www.vavoo.to/play/184486327/index.m3u8
#EXTINF:-1 tvg-name="TV 8 INTERNATIONAL ", TV 8 INTERNATIONAL 
https://www.vavoo.to/play/3546432682/index.m3u8
#EXTINF:-1 tvg-name="SHOW TV SD ", SHOW TV SD 
https://www.vavoo.to/play/2112025777/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 AVRUPA ", KANAL 7 AVRUPA 
https://www.vavoo.to/play/498645977/index.m3u8
#EXTINF:-1 tvg-name="4K TR: TVNET HD ", 4K TR: TVNET HD 
https://www.vavoo.to/play/1738739277/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 EUROPA ", KANAL 7 EUROPA 
https://www.vavoo.to/play/3264983364/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 1 [LIVE DURING EVENTS ONLY] ", BEIN SPORTS 1 [LIVE DURING EVENTS ONLY] 
https://www.vavoo.to/play/3428984703/index.m3u8
#EXTINF:-1 tvg-name="BEIN MOVIES TURK ", BEIN MOVIES TURK 
https://www.vavoo.to/play/1835579025/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 4K FEED(KUTU) ", BEIN SPORTS 4K FEED(KUTU) 
https://www.vavoo.to/play/267105889/index.m3u8
#EXTINF:-1 tvg-name="DIZI SMART PREMIUM ", DIZI SMART PREMIUM 
https://www.vavoo.to/play/791616758/index.m3u8
#EXTINF:-1 tvg-name="BBC EARTH ", BBC EARTH 
https://www.vavoo.to/play/2613731614/index.m3u8
#EXTINF:-1 tvg-name="4K TR: EKOL TV ", 4K TR: EKOL TV 
https://www.vavoo.to/play/2706210049/index.m3u8
#EXTINF:-1 tvg-name="MOVIE SMART CLASSIC ", MOVIE SMART CLASSIC 
https://www.vavoo.to/play/3597292408/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 2 UHD ", BEIN SPORTS 2 UHD 
https://www.vavoo.to/play/3694662475/index.m3u8
#EXTINF:-1 tvg-name="RAFADAN TAYFA ", RAFADAN TAYFA 
https://www.vavoo.to/play/2834759579/index.m3u8
#EXTINF:-1 tvg-name="SZC ", SZC 
https://www.vavoo.to/play/2036794972/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 4 ", BEIN SPORTS 4 
https://www.vavoo.to/play/450076655/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA COMEDY ", FIX CINEMA COMEDY 
https://www.vavoo.to/play/4140720869/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA DRAM ", FIX CINEMA DRAM 
https://www.vavoo.to/play/2830763591/index.m3u8
#EXTINF:-1 tvg-name="FIX CINEMA FANTASTIC ", FIX CINEMA FANTASTIC 
https://www.vavoo.to/play/2459747332/index.m3u8
#EXTINF:-1 tvg-name="BEIN SERIES COMEDY ", BEIN SERIES COMEDY 
https://www.vavoo.to/play/1668144911/index.m3u8
#EXTINF:-1 tvg-name="COCUK 1 HD ", COCUK 1 HD 
https://www.vavoo.to/play/204606561/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 5 ", EXXEN SPORTS 5 
https://www.vavoo.to/play/2555007244/index.m3u8
#EXTINF:-1 tvg-name="64 KARE ULKESI ", 64 KARE ULKESI 
https://www.vavoo.to/play/3842003262/index.m3u8
#EXTINF:-1 tvg-name="4K TR: MELTEM TV ", 4K TR: MELTEM TV 
https://www.vavoo.to/play/700381068/index.m3u8
#EXTINF:-1 tvg-name="4K TR: DREAM T RK ", 4K TR: DREAM T RK 
https://www.vavoo.to/play/4266683025/index.m3u8
#EXTINF:-1 tvg-name="ULKE TV ", ULKE TV 
https://www.vavoo.to/play/216740557/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 8 ", EXXEN SPORTS 8 
https://www.vavoo.to/play/1624937917/index.m3u8
#EXTINF:-1 tvg-name="TV 8.5 HD ", TV 8.5 HD 
https://www.vavoo.to/play/3472698776/index.m3u8
#EXTINF:-1 tvg-name="EXXEN SPORTS 7 ", EXXEN SPORTS 7 
https://www.vavoo.to/play/3800695404/index.m3u8
#EXTINF:-1 tvg-name="4K TR: DISCOVERY CHANNEL HD ", 4K TR: DISCOVERY CHANNEL HD 
https://www.vavoo.to/play/4017734592/index.m3u8
#EXTINF:-1 tvg-name="HORROR 2 HD ", HORROR 2 HD 
https://www.vavoo.to/play/1506105715/index.m3u8
#EXTINF:-1 tvg-name="4K TR: ENGLISH CLUB TV ", 4K TR: ENGLISH CLUB TV 
https://www.vavoo.to/play/925055356/index.m3u8
#EXTINF:-1 tvg-name="MINIKA COCUK ", MINIKA COCUK 
https://www.vavoo.to/play/3036231687/index.m3u8
#EXTINF:-1 tvg-name="CAILLOU ", CAILLOU 
https://www.vavoo.to/play/4136709820/index.m3u8
#EXTINF:-1 tvg-name="ADA TV ", ADA TV 
https://www.vavoo.to/play/4225961715/index.m3u8
#EXTINF:-1 tvg-name="BULMACA KULESI ", BULMACA KULESI 
https://www.vavoo.to/play/910953672/index.m3u8
#EXTINF:-1 tvg-name="HRT AKDENIZ TV ", HRT AKDENIZ TV 
https://www.vavoo.to/play/4223430509/index.m3u8
#EXTINF:-1 tvg-name="PIJAMA MASKE ", PIJAMA MASKE 
https://www.vavoo.to/play/3413915058/index.m3u8
#EXTINF:-1 tvg-name="BEST ANIMASYON ", BEST ANIMASYON 
https://www.vavoo.to/play/1822425118/index.m3u8
#EXTINF:-1 tvg-name="WM TV WOMAN KADIN ", WM TV WOMAN KADIN 
https://www.vavoo.to/play/3259520726/index.m3u8
#EXTINF:-1 tvg-name="KANAL T ", KANAL T 
https://www.vavoo.to/play/1831675683/index.m3u8
#EXTINF:-1 tvg-name="REDBOX ARABESK TV ", REDBOX ARABESK TV 
https://www.vavoo.to/play/1149613711/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 6 HD ", TABII SPOR 6 HD 
https://www.vavoo.to/play/270984838/index.m3u8
#EXTINF:-1 tvg-name="BEIN 1 FEED (720P) ", BEIN 1 FEED (720P) 
https://www.vavoo.to/play/1363827223/index.m3u8
#EXTINF:-1 tvg-name="BEIN SERIES 2 ", BEIN SERIES 2 
https://www.vavoo.to/play/3308693738/index.m3u8
#EXTINF:-1 tvg-name="ATV HD (H265) ", ATV HD (H265) 
https://www.vavoo.to/play/129909794/index.m3u8
#EXTINF:-1 tvg-name="CNN T RK HD+ SD ", CNN T RK HD+ SD 
https://www.vavoo.to/play/2868318534/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR SD ", TABII SPOR SD 
https://www.vavoo.to/play/4022148175/index.m3u8
#EXTINF:-1 tvg-name="A HABER ", A HABER 
https://www.vavoo.to/play/1174108535/index.m3u8
#EXTINF:-1 tvg-name="GLOBAL BOX KEMAL SUNAL ", GLOBAL BOX KEMAL SUNAL 
https://www.vavoo.to/play/4275446197/index.m3u8
#EXTINF:-1 tvg-name="A HABER ", A HABER 
https://www.vavoo.to/play/1596095882/index.m3u8
#EXTINF:-1 tvg-name="VIASAT HISTORY ", VIASAT HISTORY 
https://www.vavoo.to/play/1900945213/index.m3u8
#EXTINF:-1 tvg-name="IDMAN TV HD ", IDMAN TV HD 
https://www.vavoo.to/play/2368422760/index.m3u8
#EXTINF:-1 tvg-name="TLC ", TLC 
https://www.vavoo.to/play/951448076/index.m3u8
#EXTINF:-1 tvg-name="BEIN MOVIES PREMIERE 2 ", BEIN MOVIES PREMIERE 2 
https://www.vavoo.to/play/2120218356/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 4 HD ", TABII SPOR 4 HD 
https://www.vavoo.to/play/1375986171/index.m3u8
#EXTINF:-1 tvg-name="LIDER HABER ", LIDER HABER 
https://www.vavoo.to/play/703698868/index.m3u8
#EXTINF:-1 tvg-name="KRAL TV HD ", KRAL TV HD 
https://www.vavoo.to/play/2879812830/index.m3u8
#EXTINF:-1 tvg-name="LIMON ZEYTIN ", LIMON ZEYTIN 
https://www.vavoo.to/play/4190426847/index.m3u8
#EXTINF:-1 tvg-name="SINEVIZYON 8 ", SINEVIZYON 8 
https://www.vavoo.to/play/3644982305/index.m3u8
#EXTINF:-1 tvg-name="INVESTIGATION DISCOVERY ", INVESTIGATION DISCOVERY 
https://www.vavoo.to/play/1372455233/index.m3u8
#EXTINF:-1 tvg-name="SPOR SMART HD ", SPOR SMART HD 
https://www.vavoo.to/play/1313563350/index.m3u8
#EXTINF:-1 tvg-name="KANAL 7 HD ", KANAL 7 HD 
https://www.vavoo.to/play/1639889598/index.m3u8
#EXTINF:-1 tvg-name="TARIH TV ", TARIH TV 
https://www.vavoo.to/play/3856957052/index.m3u8
#EXTINF:-1 tvg-name="TRT TURK RAW ", TRT TURK RAW 
https://www.vavoo.to/play/4095879853/index.m3u8
#EXTINF:-1 tvg-name="TIVIBUSPOR 1 HD ", TIVIBUSPOR 1 HD 
https://www.vavoo.to/play/3654518007/index.m3u8
#EXTINF:-1 tvg-name="BEIN SPORTS 2 SD ", BEIN SPORTS 2 SD 
https://www.vavoo.to/play/3236362911/index.m3u8
#EXTINF:-1 tvg-name="SINEMAX TURK ", SINEMAX TURK 
https://www.vavoo.to/play/4201568953/index.m3u8
#EXTINF:-1 tvg-name="BEIN MOVIES ACTION 2 ", BEIN MOVIES ACTION 2 
https://www.vavoo.to/play/650851542/index.m3u8
#EXTINF:-1 tvg-name="TRT HABER HEVC ", TRT HABER HEVC 
https://www.vavoo.to/play/2057965553/index.m3u8
#EXTINF:-1 tvg-name="S SPORT 2 ", S SPORT 2 
https://www.vavoo.to/play/1313768516/index.m3u8
#EXTINF:-1 tvg-name="NILOYA HD+ ", NILOYA HD+ 
https://www.vavoo.to/play/692811579/index.m3u8
#EXTINF:-1 tvg-name="SHOW MAX ", SHOW MAX 
https://www.vavoo.to/play/1495761327/index.m3u8
#EXTINF:-1 tvg-name="TIVIBUSPOR 3 HD ", TIVIBUSPOR 3 HD 
https://www.vavoo.to/play/2616624010/index.m3u8
#EXTINF:-1 tvg-name="TRT MUZIK ", TRT MUZIK 
https://www.vavoo.to/play/2332789634/index.m3u8
#EXTINF:-1 tvg-name="TABII SPOR 4 ", TABII SPOR 4 
https://www.vavoo.to/play/2307885365/index.m3u8
#EXTINF:-1 tvg-name="TLC ", TLC 
https://www.vavoo.to/play/1766840660/index.m3u8
#EXTINF:-1 tvg-name="TRT BELGESEL ", TRT BELGESEL 
https://www.vavoo.to/play/2439012215/index.m3u8
"""

def auto_categorize(name):
    """İsimden kategori tahmin et"""
    n = name.lower()
    
    # Ulusal
    if any(x in n for x in ['trt 1', 'trt1', 'show', 'star', 'atv', 'kanal d', 'kanald', 'tv8', 'tv 8', 'kanal 7', 'kanal7', 'fox', 'now', 'beyaz', 'teve', '360', 'a2', 'euro']):
        return 'Ulusal'
    
    # Haber
    elif any(x in n for x in ['haber', 'cnn', 'ntv', 'tgrt', '24', 'ulke', 'tv100', 'tvnet', 'sozcu', 'ekol', 'turkhaber', 'lider']):
        return 'Haber'
    
    # Spor
    elif any(x in n for x in ['spor', 'sport', 'bein', 'exxen', 's sport', 'tabii', 'tivibu', 'eurosport', 'idman', 'nba']):
        return 'Spor'
    
    # Sinema
    elif any(x in n for x in ['sinema', 'cinema', 'film', 'movie', 'box', 'fix', 'sinemax']):
        return 'Film'
    
    # Çocuk
    elif any(x in n for x in ['cocuk', 'çocuk', 'minika', 'kids', 'cartoon', 'disney', 'baby', 'nick', 'boomerang', 'caillou', 'rafadan', 'niloya', 'pijama']):
        return 'Çocuk'
    
    # Müzik
    elif any(x in n for x in ['muzik', 'müzik', 'music', 'kral', 'power', 'dream', 'nr 1', 'fasil']):
        return 'Müzik'
    
    # Belgesel
    elif any(x in n for x in ['belgesel', 'nat geo', 'national', 'discovery', 'history', 'tlc', 'dmax', 'bbc', 'planet', 'viasat', 'tarih']):
        return 'Belgesel'
    
    # Dizi
    elif any(x in n for x in ['dizi', 'series', 'epic']):
        return 'Dizi'
    
    else:
        return 'Genel'

def main():
    print("=" * 60)
    print("Vavoo Listesi - Kategorize Ediliyor")
    print("=" * 60)
    
    # Parse
    pattern = r'#EXTINF:-1 tvg-name="([^"]+)"[^\n]*\n(https://[^\n]+)'
    matches = re.findall(pattern, RAW_VAVOO_DATA)
    
    print(f"\n✅ {len(matches)} kanal bulundu")
    
    # Kategorize et
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
        print(f"   {cat:15s}: {len(channels_by_category[cat]):3d} kanal")
    
    # M3U oluştur
    content = '#EXTM3U x-tvg-url="https://bit.ly/TurkoTvEpg"\n'
    content += f'# ÖMER TV + VAVOO - {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n'
    content += f'# Toplam: {len(matches)} kanal\n\n'
    
    # Kategori sırası
    category_order = ['Ulusal', 'Haber', 'Spor', 'Film', 'Dizi', 'Belgesel', 'Çocuk', 'Müzik', 'Genel']
    
    for category in category_order:
        if category in channels_by_category:
            content += f'\n#########################################\n'
            content += f'# {category.upper()} ({len(channels_by_category[category])} kanal)\n'
            content += f'#########################################\n\n'
            
            for ch in sorted(channels_by_category[category], key=lambda x: x['name']):
                content += f'#EXTINF:-1 group-title="{category}",{ch["name"]}\n'
                content += f'{ch["url"]}\n'
    
    # Kalanlar (Genel vb.)
    for category in sorted(channels_by_category.keys()):
        if category not in category_order:
            content += f'\n### {category.upper()} ###\n\n'
            for ch in channels_by_category[category]:
                content += f'#EXTINF:-1 group-title="{category}",{ch["name"]}\n'
                content += f'{ch["url"]}\n'
    
    # Kaydet
    with open('vavoo_full.m3u', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ vavoo_full.m3u oluşturuldu! ({len(matches)} kanal)")
    print("\n🔗 Link:")
    print("   https://raw.githubusercontent.com/titkenan/Omer_TV/main/vavoo_full.m3u")

if __name__ == "__main__":
    main()
