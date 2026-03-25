import os
import json
import sys
from stream_tester import StreamTester
from epg_manager import EPGManager
from auto_updater import AutoUpdater


def setup_directories():
    """Gerekli klasörleri oluştur"""
    directories = ['data', 'web_player/templates', 'web_player/static']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Klasörler kontrol edildi")


def create_sample_channels():
    """Örnek kanal listesi oluştur"""
    channels = [
        # Ana Kanallar
        {'name': 'TRT 1', 'url': 'https://tv-trt1.medya.trt.com.tr/master.m3u8', 'category': 'Genel', 'epg_id': 'TRT1'},
        {'name': 'ATV', 'url': 'https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8', 'category': 'Genel', 'epg_id': 'ATV'},
        {'name': 'Kanal D', 'url': 'https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba/kanald/kanald_1080p.m3u8', 'category': 'Genel', 'epg_id': 'KanalD'},
        {'name': 'Show TV', 'url': 'https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/showtv/showtv.m3u8', 'category': 'Genel', 'epg_id': 'ShowTV'},
        {'name': 'Star TV', 'url': 'https://dygvideo.dygdigital.com/live/hls/startv4puhu', 'category': 'Genel', 'epg_id': 'StarTV'},
        {'name': 'Kanal 7', 'url': 'https://yurhnwtpys.turknet.ercdn.net/cvmbjbpmdx/kanal7/kanal7_1080p.m3u8', 'category': 'Genel', 'epg_id': 'Kanal7'},
        {'name': 'TV8', 'url': 'https://api.hitnova.net/s/tv8/mono.m3u8', 'category': 'Genel', 'epg_id': 'TV8'},
        {'name': 'Now TV', 'url': 'https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv_720p.m3u8', 'category': 'Genel'},
        
        # Haber Kanalları
        {'name': 'TRT Haber', 'url': 'https://tv-trthaber.medya.trt.com.tr/master.m3u8', 'category': 'Haber'},
        {'name': 'NTV', 'url': 'https://dogus.daioncdn.net/ntv/ntv_1080p.m3u8', 'category': 'Haber'},
        {'name': 'Habertürk', 'url': 'https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/haberturktv/haberturktv_1080p.m3u8', 'category': 'Haber'},
        {'name': 'Haber Global', 'url': 'https://tv.ensonhaber.com/haberglobal/haberglobal_720p.m3u8', 'category': 'Haber'},
        
        # Spor Kanalları
        {'name': 'TRT Spor', 'url': 'https://api.hitnova.net/s/trtspor/mono.m3u8', 'category': 'Spor'},
        {'name': 'A Spor', 'url': 'https://api.hitnova.net/s/as/mono.m3u8', 'category': 'Spor'},
        
        # Çocuk Kanalları
        {'name': 'TRT Çocuk', 'url': 'https://tv-trtcocuk.medya.trt.com.tr/master_1080.m3u8', 'category': 'Çocuk'},
        
        # Belgesel
        {'name': 'TRT 2', 'url': 'https://tv-trt2.medya.trt.com.tr/master_1440.m3u8', 'category': 'Belgesel'},
    ]
    
    with open('data/channels.json', 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    
    print("✅ Kanal listesi oluşturuldu: data/channels.json")
    print(f"📺 Toplam {len(channels)} kanal eklendi")
    return channels


def load_channels():
    """Kanalları yükle, yoksa oluştur"""
    channels_file = 'data/channels.json'
    
    if not os.path.exists(channels_file):
        print("⚠️ Kanal listesi bulunamadı, yeni liste oluşturuluyor...")
        return create_sample_channels()
    
    try:
        with open(channels_file, 'r', encoding='utf-8') as f:
            channels = json.load(f)
        
        if not channels:
            print("⚠️ Kanal listesi boş, yenisi oluşturuluyor...")
            return create_sample_channels()
        
        return channels
    
    except json.JSONDecodeError:
        print("❌ Kanal listesi bozuk, yenisi oluşturuluyor...")
        return create_sample_channels()


def save_channels(channels):
    """Kanalları kaydet"""
    with open('data/channels.json', 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)


def display_channels(channels):
    """Kanalları kategorilere göre göster"""
    print("\n" + "═" * 80)
    print("📋 MEVCUT KANALLAR")
    print("═" * 80)
    
    categories = {}
    for ch in channels:
        cat = ch.get('category', 'Diğer')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ch)
    
    total = 0
    for cat in sorted(categories.keys()):
        chs = categories[cat]
        print(f"\n📂 {cat} ({len(chs)} kanal)")
        print("─" * 80)
        
        for i, ch in enumerate(chs, 1):
            is_working = ch.get('is_working', None)
            if is_working is True:
                status = "✅"
            elif is_working is False:
                status = "❌"
            else:
                status = "❓"
            
            quality = ch.get('last_test', {}).get('quality', '')
            quality_badge = f"[{quality}]" if quality else ""
            
            response_time = ch.get('last_test', {}).get('response_time')
            time_info = f" ({response_time}ms)" if response_time else ""
            
            source = ch.get('source', '')
            source_badge = f" 🌐" if source else ""
            
            print(f"  {total+i:2d}. {status} {ch['name']:20s} {quality_badge:12s}{time_info}{source_badge}")
        
        total += len(chs)
    
    print("═" * 80)
    print(f"📊 Toplam: {total} kanal")


def main_menu():
    """Ana menü"""
    print("\n" + "═" * 80)
    print("📺 OmEr TV - KONTROL MERKEZİ")
    print("═" * 80)
    print("1.  🧪 Stream Kalite Testi Yap")
    print("2.  📡 EPG Güncelle")
    print("3.  🔄 Otomatik Güncelleyiciyi Başlat")
    print("4.  🌐 Web Player'ı Başlat")
    print("5.  📊 Son Test Sonuçlarını Göster")
    print("6.  📋 Mevcut Kanalları Listele")
    print("7.  ➕ Yeni Kanal Ekle (Manuel)")
    print("8.  🔃 Zafer Murat TV'den Kanalları Çek (Otomatik)")
    print("9.  🛠️ Kanal Listesini Sıfırla")
    print("10. 🗑️ Tüm Verileri Temizle")
    print("0.  ❌ Çıkış")
    print("═" * 80)
    
    choice = input("\nSeçiminiz (0-10): ").strip()
    return choice


def test_streams():
    """Stream kalite testi"""
    print("\n🔍 Kanallar yükleniyor...")
    channels = load_channels()
    print(f"📊 {len(channels)} kanal bulundu\n")
    
    print("⚙️ Test Ayarları:")
    try:
        timeout = int(input("  Timeout (saniye, varsayılan 10): ") or "10")
        max_workers = int(input("  Paralel test sayısı (varsayılan 10): ") or "10")
    except ValueError:
        timeout, max_workers = 10, 10
        print("  ⚠️ Geçersiz değer, varsayılanlar kullanılıyor")
    
    print()
    
    tester = StreamTester(timeout=timeout, max_workers=max_workers)
    results = tester.test_all_streams(channels)
    report = tester.generate_report(results, 'data/test_results.json')
    
    for channel in channels:
        for result in results:
            if channel['url'] == result['url']:
                channel['last_test'] = result
                channel['is_working'] = (result['status'] == 'working')
                break
    
    save_channels(channels)
    print("\n✅ Kanal durumları güncellendi ve kaydedildi")
    
    return report


def update_epg():
    """EPG güncelle"""
    import urllib3
    urllib3.disable_warnings()
    
    print("\n📡 EPG güncelleniyor...")
    epg = EPGManager()
    
    success = False
    total_sources = len(epg.epg_sources)
    
    for i, source in enumerate(epg.epg_sources, 1):
        print(f"\n[{i}/{total_sources}] 🔗 Kaynak:")
        print(f"    {source[:75]}...")
        print("─" * 80)
        
        xml_file = epg.download_epg(source)
        if xml_file:
            epg_data = epg.parse_epg(xml_file)
            if epg_data:
                if epg.save_epg_json():
                    stats = epg.get_epg_stats()
                    
                    print("\n" + "═" * 80)
                    print("✅ EPG BAŞARIYLA GÜNCELLENDİ!")
                    print("═" * 80)
                    print(f"📺 Toplam Kanal  : {stats['total_channels']}")
                    print(f"📅 Toplam Program: {stats['total_programs']:,}")
                    print(f"🕒 Son Güncelleme: {stats['last_update'][:19]}")
                    
                    if epg_data.get('is_mock'):
                        print("\n⚠️ NOT: Bu örnek veri (gerçek EPG değil)")
                    
                    print("═" * 80)
                    success = True
                    break
        
        if i < total_sources:
            print("⏭️ Sonraki kaynağa geçiliyor...\n")
    
    if not success:
        print("\n" + "═" * 80)
        print("⚠️ TÜM EPG KAYNAKLARI BAŞARISIZ!")
        print("═" * 80)
        print("\n📝 Örnek EPG verisi oluşturuluyor...")
        epg.create_mock_epg()
        epg.save_epg_json()
        print("\n✅ Örnek EPG oluşturuldu")
        print("═" * 80)


def start_auto_updater():
    """Otomatik güncelleyiciyi başlat"""
    print("\n⚙️ Otomatik Güncelleyici Ayarları")
    print("─" * 80)
    
    try:
        test_interval = int(input("Stream test aralığı (saat, varsayılan 6): ") or "6")
        epg_interval = int(input("EPG güncelleme aralığı (saat, varsayılan 12): ") or "12")
    except ValueError:
        test_interval, epg_interval = 6, 12
        print("⚠️ Geçersiz değer, varsayılanlar kullanılıyor")
    
    print("\n🚀 Başlatılıyor...")
    print(f"   ⏰ Stream testi: Her {test_interval} saatte")
    print(f"   📡 EPG güncelleme: Her {epg_interval} saatte")
    print("\n⏹️ Durdurmak için: Ctrl+C\n")
    
    updater = AutoUpdater()
    
    try:
        updater.start_scheduler(test_interval_hours=test_interval, epg_interval_hours=epg_interval)
    except KeyboardInterrupt:
        print("\n\n🛑 Otomatik güncelleyici durduruldu")


def start_web_player():
    """Web player'ı başlat"""
    print("\n🌐 Web Player Başlatılıyor...")
    print("═" * 80)
    
    channels = load_channels()
    print(f"✅ {len(channels)} kanal yüklendi")
    
    if os.path.exists('data/epg.json'):
        print("✅ EPG verisi mevcut")
    else:
        print("⚠️ EPG verisi yok (menüden EPG güncelleyin)")
    
    print("\n📺 Tarayıcınızda şu adreslerden birini açın:")
    print("   👉 http://localhost:5000")
    print("   👉 http://127.0.0.1:5000")
    print("\n⏹️ Durdurmak için: Ctrl+C")
    print("═" * 80 + "\n")
    
    try:
        sys.path.insert(0, 'web_player')
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
    
    except ImportError as e:
        print(f"❌ web_player/app.py bulunamadı: {e}")
    except OSError as e:
        if "Address already in use" in str(e):
            print("❌ Port 5000 zaten kullanımda!")
        else:
            print(f"❌ Hata: {e}")
    except KeyboardInterrupt:
        print("\n\n🛑 Web Player durduruldu")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")


def show_test_results():
    """Son test sonuçlarını göster"""
    results_file = 'data/test_results.json'
    
    if not os.path.exists(results_file):
        print("\n⚠️ Henüz test yapılmamış!")
        print("💡 Önce '1. Stream Kalite Testi Yap' seçeneğini çalıştırın.")
        return
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        summary = results.get('summary', {})
        
        print("\n" + "═" * 80)
        print("📊 SON TEST SONUÇLARI")
        print("═" * 80)
        print(f"📺 Toplam Stream    : {summary.get('total_streams', 0)}")
        print(f"✅ Çalışan         : {summary.get('working', 0)} ({summary.get('success_rate', 0)}%)")
        print(f"❌ Çalışmayan      : {summary.get('failed', 0)}")
        print(f"⏱️ Ortalama Yanıt  : {summary.get('avg_response_time_ms', 0)}ms")
        print(f"📅 Test Tarihi     : {summary.get('test_date', 'Bilinmiyor')[:19]}")
        
        quality_dist = summary.get('quality_distribution', {})
        if quality_dist:
            print("\n📈 Kalite Dağılımı:")
            print("─" * 80)
            
            quality_labels = {
                'excellent': '🟢 Mükemmel',
                'good': '🟡 İyi',
                'fair': '🟠 Orta',
                'poor': '🔴 Zayıf',
                'unavailable': '⚫ Erişilemez'
            }
            
            for quality in ['excellent', 'good', 'fair', 'poor', 'unavailable']:
                count = quality_dist.get(quality, 0)
                if count > 0:
                    bar = "█" * min(count, 40)
                    label = quality_labels.get(quality, quality)
                    print(f"  {label:15s}: {bar} ({count})")
        
        print("═" * 80)
        
        show_detail = input("\n📋 Detaylı liste görmek ister misiniz? (e/h): ").lower()
        if show_detail == 'e':
            print("\n" + "─" * 80)
            for i, result in enumerate(results.get('results', []), 1):
                status_emoji = {'working': '✅', 'timeout': '⏱️', 'failed': '❌'}.get(result.get('status'), '❓')
                name = result.get('name', 'Bilinmiyor')
                response_time = result.get('response_time', 'N/A')
                print(f"{i:3d}. {status_emoji} {name:25s} | {response_time}ms")
    
    except Exception as e:
        print(f"❌ Sonuçlar okunamadı: {e}")


def add_new_channel():
    """Yeni kanal ekle"""
    print("\n➕ YENİ KANAL EKLE")
    print("─" * 80)
    
    try:
        name = input("Kanal adı: ").strip()
        if not name:
            print("❌ Kanal adı boş olamaz!")
            return
        
        url = input("Stream URL (.m3u8): ").strip()
        if not url:
            print("❌ URL boş olamaz!")
            return
        
        category = input("Kategori (Genel/Haber/Spor/Çocuk/Belgesel): ").strip() or "Genel"
        
        channels = load_channels()
        
        new_channel = {
            'name': name,
            'url': url,
            'category': category
        }
        
        channels.append(new_channel)
        save_channels(channels)
        
        print(f"\n✅ '{name}' kanalı eklendi!")
    
    except KeyboardInterrupt:
        print("\n\n❌ İşlem iptal edildi")


def scrape_from_zafer_murat():
    """Zafer Murat TV'den kanalları çek"""
    try:
        from channel_scraper import ZaferMuratChannelScraper
    except ImportError:
        print("\n❌ channel_scraper.py bulunamadı!")
        print("💡 Dosyanın aynı klasörde olduğundan emin olun.")
        return
    
    print("\n🌐 Zafer Murat TV'den Kanallar Çekiliyor...")
    print("═" * 80)
    
    existing_channels = load_channels()
    print(f"📊 Mevcut kanal sayısı: {len(existing_channels)}")
    
    print("\n⚙️ Ayarlar:")
    try:
        headless_input = input("Tarayıcıyı göster? (e/h, varsayılan h): ").lower()
        headless = headless_input != 'e'
        wait_time = int(input("Bekleme süresi (saniye, varsayılan 15): ") or "15")
    except ValueError:
        headless = True
        wait_time = 15
    
    scraper = ZaferMuratChannelScraper(headless=headless)
    
    try:
        new_channels = scraper.scrape_channels(wait_time=wait_time)
        
        if not new_channels:
            print("\n⚠️ Hiç kanal bulunamadı!")
            print("💡 İpucu: Bekleme süresini artırın veya tarayıcıyı göstererek deneyin")
            return
        
        print(f"\n📺 Bulunan kanal sayısı: {len(new_channels)}")
        
        # Bulunan kanalları göster
        print("\n📋 Bulunan Kanallar:")
        print("─" * 80)
        categories = {}
        for ch in new_channels:
            cat = ch.get('category', 'Diğer')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ch)
        
        for cat, chs in sorted(categories.items()):
            print(f"\n📂 {cat} ({len(chs)})")
            for ch in chs[:5]:
                print(f"   • {ch['name']}")
            if len(chs) > 5:
                print(f"   ... ve {len(chs)-5} kanal daha")
        
        print("\n" + "─" * 80)
        print("🔀 Birleştirme Modu:")
        print("  1. Ekle (Sadece yeni kanalları ekle, mevcut kalsın)")
        print("  2. Güncelle (Yeni ekle + mevcut olanları güncelle)")
        print("  3. Değiştir (Tüm listeyi sil, sadece yenileri koy)")
        print("  4. İptal")
        
        mode = input("\nSeçim (1-4): ").strip()
        
        if mode == "1":
            merged = scraper.merge_with_existing(new_channels, existing_channels)
            scraper.save_channels(merged)
            print("\n✅ Yeni kanallar eklendi!")
        
        elif mode == "2":
            merged = scraper.merge_with_existing(new_channels, existing_channels)
            scraper.save_channels(merged)
            print("\n✅ Kanallar güncellendi!")
        
        elif mode == "3":
            confirm = input("\n⚠️ Mevcut tüm kanallar silinecek! EVET yazın: ").strip()
            if confirm == "EVET":
                scraper.save_channels(new_channels)
                print("\n✅ Kanal listesi tamamen yenilendi!")
            else:
                print("❌ İşlem iptal edildi")
        
        else:
            print("❌ İşlem iptal edildi")
            return
        
        test_now = input("\n🧪 Kanalları şimdi test etmek ister misiniz? (e/h): ").lower()
        if test_now == 'e':
            test_streams()
    
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        scraper.close()


def reset_channels():
    """Kanal listesini sıfırla"""
    print("\n🛠️ KANAL LİSTESİNİ SIFIRLA")
    print("─" * 80)
    print("⚠️ Mevcut kanal listesi silinecek ve varsayılan liste yüklenecek!")
    
    confirm = input("\nDevam etmek için EVET yazın: ").strip()
    
    if confirm == "EVET":
        create_sample_channels()
        print("\n✅ Kanal listesi varsayılana döndürüldü")
    else:
        print("❌ İşlem iptal edildi")


def clean_all_data():
    """Tüm verileri temizle"""
    print("\n🗑️ TÜM VERİLERİ TEMİZLE")
    print("─" * 80)
    print("⚠️ Silinecek veriler:")
    print("   • channels.json")
    print("   • test_results.json")
    print("   • epg.json, epg.xml")
    
    confirm = input("\n⚠️ Emin misiniz? EVET yazın: ").strip()
    
    if confirm == "EVET":
        files = ['data/channels.json', 'data/test_results.json', 'data/epg.json', 'data/epg.xml']
        
        deleted = 0
        for file in files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"🗑️ Silindi: {file}")
                    deleted += 1
                except Exception as e:
                    print(f"❌ Silinemedi {file}: {e}")
        
        print(f"\n✅ {deleted} dosya silindi")
    else:
        print("❌ İşlem iptal edildi")


# ═══════════════════════════════════════════════════════════════════════════════
#                              ANA PROGRAM
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Ana program döngüsü"""
    setup_directories()
    
    while True:
        try:
            choice = main_menu()
            
            if choice == '1':
                test_streams()
            
            elif choice == '2':
                update_epg()
            
            elif choice == '3':
                start_auto_updater()
            
            elif choice == '4':
                start_web_player()
            
            elif choice == '5':
                show_test_results()
            
            elif choice == '6':
                channels = load_channels()
                display_channels(channels)
            
            elif choice == '7':
                add_new_channel()
            
            elif choice == '8':
                scrape_from_zafer_murat()
            
            elif choice == '9':
                reset_channels()
            
            elif choice == '10':
                clean_all_data()
            
            elif choice == '0':
                print("\n" + "═" * 80)
                print("👋 OmEr TV - Görüşmek üzere!")
                print("═" * 80)
                break
            
            else:
                print("\n❌ Geçersiz seçim! Lütfen 0-10 arasında bir sayı girin.")
            
            if choice != '0':
                input("\n⏸️ Devam etmek için Enter'a basın...")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Program durduruldu")
            confirm = input("Çıkmak istiyor musunuz? (e/h): ").lower()
            if confirm == 'e':
                break
        
        except Exception as e:
            print(f"\n❌ Hata: {e}")
            import traceback
            traceback.print_exc()
            input("\n⏸️ Devam etmek için Enter'a basın...")


# ═══════════════════════════════════════════════════════════════════════════════
#                              BAŞLANGIÇ
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                           📺 OmEr TV - IPTV Sistemi                          ║
║                                                                              ║
║                              Versiyon 1.0.0                                  ║
║                                                                              ║
║                    • Stream Kalite Testi                                     ║
║                    • EPG Program Rehberi                                     ║
║                    • Otomatik Kanal Güncelleme                               ║
║                    • Web Tabanlı Player                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        main()
    except Exception as e:
        print(f"\n💥 Kritik Hata: {e}")
        import traceback
        traceback.print_exc()
        input("\nÇıkmak için Enter'a basın...")