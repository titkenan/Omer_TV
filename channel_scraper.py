import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class ZaferMuratChannelScraper:
    def __init__(self, headless=True):
        """Zafer Murat TV sitesinden kanal çeken scraper"""
        self.url = "https://zafermurat.github.io/Tv/"
        self.options = Options()
        
        if headless:
            self.options.add_argument('--headless')
        
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Network loglarını yakala
        self.options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        self.driver = None
    
    def start_driver(self):
        """Chrome driver başlat"""
        print("🚗 Chrome driver başlatılıyor...")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)
        print("✅ Driver hazır!")
    
    def scrape_channels(self, wait_time=15):
        """Siteden kanalları çek"""
        if not self.driver:
            self.start_driver()
        
        print(f"\n📥 Sayfa yükleniyor: {self.url}")
        self.driver.get(self.url)
        
        print(f"⏳ {wait_time} saniye bekleniyor (JavaScript yüklensin)...")
        time.sleep(wait_time)
        
        # HTML içeriğini al
        html = self.driver.page_source
        
        # Network isteklerinden M3U8 linklerini çek
        print("🔍 Network istekleri analiz ediliyor...")
        logs = self.driver.get_log('performance')
        
        media_urls = set()
        
        for log in logs:
            try:
                message = json.loads(log['message'])['message']
                
                if message['method'] == 'Network.requestWillBeSent':
                    url = message['params']['request']['url']
                    
                    # M3U8 linklerini filtrele
                    if '.m3u8' in url.lower() and not url.endswith(('.js', '.css')):
                        # Bazı kötü URL'leri filtrele
                        if 'hitnova' in url or 'turknet' in url or 'trt' in url or 'daioncdn' in url:
                            media_urls.add(url)
            
            except (KeyError, json.JSONDecodeError):
                continue
        
        # HTML'den de kanal bilgilerini çıkar
        channels = self._parse_html_channels(html, media_urls)
        
        return channels
    
    def _parse_html_channels(self, html, media_urls):
        """HTML'den kanal bilgilerini parse et"""
        channels = []
        
        # Kanal adlarını ve logo URL'lerini çıkar
        # Zafer Murat sitesinde kanallar genelde bu formatta:
        # <div class="channel-item" data-name="TRT 1" data-url="...">
        
        # Logo pattern'i
        logo_pattern = r'https://upload\.wikimedia\.org/[^"\']+\.(?:png|jpg|jpeg)'
        logos = re.findall(logo_pattern, html, re.IGNORECASE)
        
        # Kanal isimleri için bilinen kanalları eşleştir
        known_channels = {
            'trt1': {'name': 'TRT 1', 'category': 'Genel'},
            'trt2': {'name': 'TRT 2', 'category': 'Belgesel'},
            'trtcocuk': {'name': 'TRT Çocuk', 'category': 'Çocuk'},
            'trthaber': {'name': 'TRT Haber', 'category': 'Haber'},
            'trtspor': {'name': 'TRT Spor', 'category': 'Spor'},
            'atv': {'name': 'ATV', 'category': 'Genel'},
            'kanald': {'name': 'Kanal D', 'category': 'Genel'},
            'kanal7': {'name': 'Kanal 7', 'category': 'Genel'},
            'showtv': {'name': 'Show TV', 'category': 'Genel'},
            'show': {'name': 'Show TV', 'category': 'Genel'},
            'startv': {'name': 'Star TV', 'category': 'Genel'},
            'star': {'name': 'Star TV', 'category': 'Genel'},
            'tv8': {'name': 'TV8', 'category': 'Genel'},
            'ntv': {'name': 'NTV', 'category': 'Haber'},
            'haberturk': {'name': 'Habertürk', 'category': 'Haber'},
            'haberglobal': {'name': 'Haber Global', 'category': 'Haber'},
            'nowtv': {'name': 'Now TV', 'category': 'Genel'},
            'as': {'name': 'A Spor', 'category': 'Spor'},
            'aspor': {'name': 'A Spor', 'category': 'Spor'},
            'eurosport1': {'name': 'Eurosport 1', 'category': 'Spor'},
            'eurosport2': {'name': 'Eurosport 2', 'category': 'Spor'},
            'sspor': {'name': 'S Sport', 'category': 'Spor'},
            'ss': {'name': 'S Sport', 'category': 'Spor'},
            'smarts': {'name': 'Smart Spor', 'category': 'Spor'},
            'tivibu': {'name': 'Tivibu Spor', 'category': 'Spor'},
            'cbc': {'name': 'CBC Sport', 'category': 'Spor'},
            'idman': {'name': 'İdman TV', 'category': 'Spor'},
        }
        
        # Her URL için kanal bilgisi oluştur
        for url in sorted(media_urls):
            url_lower = url.lower()
            
            # URL'den kanal adını tahmin et
            matched = False
            for key, info in known_channels.items():
                if key in url_lower:
                    channels.append({
                        'name': info['name'],
                        'url': url,
                        'category': info['category'],
                        'source': 'Zafer Murat TV'
                    })
                    matched = True
                    break
            
            # Eşleşme bulunamazsa genel bir isim ver
            if not matched:
                # URL'den isim çıkar
                parts = url.split('/')
                for part in reversed(parts):
                    if part and not part.endswith('.m3u8'):
                        name = part.replace('_', ' ').title()
                        channels.append({
                            'name': name,
                            'url': url,
                            'category': 'Diğer',
                            'source': 'Zafer Murat TV'
                        })
                        break
        
        return channels
    
    def merge_with_existing(self, new_channels, existing_channels):
        """Yeni kanalları mevcut liste ile birleştir"""
        print("\n🔄 Kanallar birleştiriliyor...")
        
        # Mevcut URL'leri bul
        existing_urls = {ch['url'] for ch in existing_channels}
        
        added = 0
        updated = 0
        
        for new_ch in new_channels:
            if new_ch['url'] in existing_urls:
                # Mevcut kanalı güncelle
                for existing_ch in existing_channels:
                    if existing_ch['url'] == new_ch['url']:
                        # Sadece source bilgisini ekle
                        existing_ch['source'] = new_ch.get('source', 'Zafer Murat TV')
                        updated += 1
                        break
            else:
                # Yeni kanal ekle
                existing_channels.append(new_ch)
                added += 1
        
        print(f"✅ {added} yeni kanal eklendi")
        print(f"🔄 {updated} kanal güncellendi")
        print(f"📊 Toplam: {len(existing_channels)} kanal")
        
        return existing_channels
    
    def save_channels(self, channels, filename='data/channels.json'):
        """Kanalları kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=2, ensure_ascii=False)
        print(f"💾 Kaydedildi: {filename}")
    
    def close(self):
        """Driver'ı kapat"""
        if self.driver:
            self.driver.quit()
            print("🛑 Driver kapatıldı")


# ═══════════════════════════════════════════════════
#                    TEST KULLANIMI
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    scraper = ZaferMuratChannelScraper(headless=False)
    
    try:
        # Kanalları çek
        channels = scraper.scrape_channels(wait_time=15)
        
        print("\n" + "═" * 80)
        print(f"📺 BULUNAN KANALLAR: {len(channels)}")
        print("═" * 80)
        
        # Kategorilere göre grupla
        categories = {}
        for ch in channels:
            cat = ch['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ch)
        
        for cat, chs in sorted(categories.items()):
            print(f"\n📂 {cat} ({len(chs)} kanal)")
            for i, ch in enumerate(chs, 1):
                print(f"  {i}. {ch['name']}")
        
        # Kaydet
        scraper.save_channels(channels)
    
    finally:
        scraper.close()