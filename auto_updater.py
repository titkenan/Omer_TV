def scrape_channels_job(self):
    """Zamanlanmış kanal güncelleme"""
    print(f"\n{'='*80}")
    print(f"🔃 Otomatik Kanal Güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    from channel_scraper import ZaferMuratChannelScraper
    
    scraper = ZaferMuratChannelScraper(headless=True)
    
    try:
        # Mevcut kanalları yükle
        channels = self.load_channels()
        
        # Yeni kanalları çek
        new_channels = scraper.scrape_channels(wait_time=15)
        
        if new_channels:
            # Birleştir
            merged = scraper.merge_with_existing(new_channels, channels)
            self.save_channels(merged)
            
            print(f"\n✅ Kanal listesi güncellendi")
        else:
            print(f"\n⚠️ Yeni kanal bulunamadı")
    
    finally:
        scraper.close()


def start_scheduler(self, test_interval_hours=6, epg_interval_hours=12, channel_scrape_interval_hours=24):
    """Zamanlayıcıyı başlat"""
    print("🚀 Otomatik Güncelleyici Başlatılıyor...")
    print(f"⏰ Stream testi: Her {test_interval_hours} saatte")
    print(f"📡 EPG güncelleme: Her {epg_interval_hours} saatte")
    print(f"🔃 Kanal güncelleme: Her {channel_scrape_interval_hours} saatte")  # YENİ
    print("─" * 80)
    
    # İlk işlemleri yap
    self.test_streams_job()
    self.update_epg_job()
    self.scrape_channels_job()  # YENİ
    
    # Zamanlamaları ayarla
    schedule.every(test_interval_hours).hours.do(self.test_streams_job)
    schedule.every(epg_interval_hours).hours.do(self.update_epg_job)
    schedule.every(channel_scrape_interval_hours).hours.do(self.scrape_channels_job)  # YENİ
    
    print("\n⏳ Zamanlayıcı çalışıyor... (Ctrl+C ile durdurun)")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n\n🛑 Zamanlayıcı durduruldu.")