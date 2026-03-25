import schedule
import time
import json
import os
from datetime import datetime


class AutoUpdater:
    def __init__(self, channels_file='data/channels.json'):
        """Otomatik güncelleme yöneticisi"""
        self.channels_file = channels_file
        self.last_test = None
        self.last_epg_update = None
    
    def load_channels(self):
        """Kanal listesini yükle"""
        try:
            with open(self.channels_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ {self.channels_file} bulunamadı!")
            return []
        except json.JSONDecodeError:
            print(f"❌ {self.channels_file} bozuk!")
            return []
    
    def save_channels(self, channels):
        """Kanal listesini kaydet"""
        os.makedirs(os.path.dirname(self.channels_file), exist_ok=True)
        with open(self.channels_file, 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=2, ensure_ascii=False)
    
    def test_streams_job(self):
        """Zamanlanmış stream testi"""
        print(f"\n{'='*80}")
        print(f"🔄 Otomatik Stream Testi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        try:
            from stream_tester import StreamTester
            
            channels = self.load_channels()
            if not channels:
                print("❌ Kanal bulunamadı!")
                return
            
            tester = StreamTester(timeout=10, max_workers=10)
            results = tester.test_all_streams(channels)
            tester.generate_report(results, 'data/test_results.json')
            
            # Sonuçları kanallara ekle
            for channel in channels:
                for result in results:
                    if channel['url'] == result['url']:
                        channel['last_test'] = result
                        channel['is_working'] = (result['status'] == 'working')
                        break
            
            self.save_channels(channels)
            self.last_test = datetime.now()
            
            working = len([r for r in results if r['status'] == 'working'])
            print(f"\n✅ Test tamamlandı: {working}/{len(results)} kanal çalışıyor")
        
        except ImportError:
            print("❌ stream_tester.py bulunamadı!")
        except Exception as e:
            print(f"❌ Test hatası: {e}")
    
    def update_epg_job(self):
        """Zamanlanmış EPG güncelleme"""
        print(f"\n{'='*80}")
        print(f"📡 Otomatik EPG Güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        try:
            from epg_manager import EPGManager
            import urllib3
            urllib3.disable_warnings()
            
            epg = EPGManager()
            
            for source in epg.epg_sources:
                print(f"🔗 Deneniyor: {source[:60]}...")
                xml_file = epg.download_epg(source)
                
                if xml_file:
                    epg_data = epg.parse_epg(xml_file)
                    if epg_data:
                        epg.save_epg_json()
                        self.last_epg_update = datetime.now()
                        
                        stats = epg.get_epg_stats()
                        print(f"\n✅ EPG güncellendi: {stats['total_channels']} kanal, {stats['total_programs']} program")
                        return
            
            # Hiçbir kaynak çalışmadıysa mock veri oluştur
            print("⚠️ EPG kaynakları başarısız, örnek veri oluşturuluyor...")
            epg.create_mock_epg()
            epg.save_epg_json()
        
        except ImportError:
            print("❌ epg_manager.py bulunamadı!")
        except Exception as e:
            print(f"❌ EPG güncelleme hatası: {e}")
    
    def scrape_channels_job(self):
        """Zamanlanmış kanal çekme"""
        print(f"\n{'='*80}")
        print(f"🔃 Otomatik Kanal Güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        try:
            from channel_scraper import ZaferMuratChannelScraper
            
            channels = self.load_channels()
            scraper = ZaferMuratChannelScraper(headless=True)
            
            try:
                new_channels = scraper.scrape_channels(wait_time=15)
                
                if new_channels:
                    merged = scraper.merge_with_existing(new_channels, channels)
                    self.save_channels(merged)
                    print(f"\n✅ Kanal listesi güncellendi: {len(merged)} kanal")
                else:
                    print("⚠️ Yeni kanal bulunamadı")
            finally:
                scraper.close()
        
        except ImportError:
            print("⚠️ channel_scraper.py bulunamadı, kanal güncelleme atlandı")
        except Exception as e:
            print(f"❌ Kanal çekme hatası: {e}")
    
    def start_scheduler(self, test_interval_hours=6, epg_interval_hours=12, channel_interval_hours=24):
        """Zamanlayıcıyı başlat"""
        print("🚀 Otomatik Güncelleyici Başlatılıyor...")
        print("─" * 80)
        print(f"⏰ Stream testi     : Her {test_interval_hours} saatte")
        print(f"📡 EPG güncelleme   : Her {epg_interval_hours} saatte")
        print(f"🔃 Kanal güncelleme : Her {channel_interval_hours} saatte")
        print("─" * 80)
        
        # İlk işlemleri hemen yap
        print("\n📌 İlk çalıştırma yapılıyor...\n")
        self.test_streams_job()
        self.update_epg_job()
        
        # Zamanlamaları ayarla
        schedule.every(test_interval_hours).hours.do(self.test_streams_job)
        schedule.every(epg_interval_hours).hours.do(self.update_epg_job)
        schedule.every(channel_interval_hours).hours.do(self.scrape_channels_job)
        
        print("\n" + "═" * 80)
        print("⏳ Zamanlayıcı çalışıyor...")
        print("⏹️ Durdurmak için: Ctrl+C")
        print("═" * 80)
        
        try:
            while True:
                schedule.run_pending()
                
                # Her dakika durumu göster
                next_run = schedule.next_run()
                if next_run:
                    remaining = next_run - datetime.now()
                    mins = int(remaining.total_seconds() // 60)
                    if mins > 0 and mins % 30 == 0:  # Her 30 dakikada bir göster
                        print(f"⏰ Sonraki işlem: {mins} dakika sonra")
                
                time.sleep(60)  # Her dakika kontrol
        
        except KeyboardInterrupt:
            print("\n\n🛑 Zamanlayıcı durduruldu.")
            self._show_summary()
    
    def _show_summary(self):
        """Özet göster"""
        print("\n" + "═" * 80)
        print("📊 OTURUM ÖZETİ")
        print("═" * 80)
        
        if self.last_test:
            print(f"🧪 Son test: {self.last_test.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("🧪 Son test: Yapılmadı")
        
        if self.last_epg_update:
            print(f"📡 Son EPG: {self.last_epg_update.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("📡 Son EPG: Yapılmadı")
        
        print("═" * 80)


# ═══════════════════════════════════════════════════════════════════════════════
#                              TEST
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🔄 Auto Updater Test Modu")
    print("─" * 80)
    
    updater = AutoUpdater()
    
    # Tek seferlik test
    print("\n1. Stream testi yapılıyor...")
    updater.test_streams_job()
    
    print("\n2. EPG güncelleniyor...")
    updater.update_epg_job()
    
    print("\n✅ Test tamamlandı!")