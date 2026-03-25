import json
from datetime import datetime, timedelta
import random


class EPGManager:
    def __init__(self):
        """EPG Manager - Sadece mock EPG kullanır"""
        self.epg_sources = []  # Boş liste, hiç kaynak aramayacak
        self.epg_data = {}
    
    def download_epg(self, url, save_path='data/epg.xml'):
        """Bu fonksiyon artık kullanılmıyor, boş dönüyor"""
        return None
    
    def parse_epg(self, xml_file):
        """Bu fonksiyon artık kullanılmıyor, boş dönüyor"""
        return None
    
    def _parse_xmltv_time(self, time_str):
        """XMLTV zaman formatını parse et"""
        if not time_str:
            return None
        try:
            dt_str = time_str.split()[0][:14]
            dt = datetime.strptime(dt_str, '%Y%m%d%H%M%S')
            return dt.isoformat()
        except Exception:
            return None
    
    def get_current_program(self, channel_id):
        """Şu anki programı getir"""
        if channel_id not in self.epg_data.get('programs', {}):
            return None
        
        now = datetime.now()
        for program in self.epg_data['programs'][channel_id]:
            if not program.get('start'):
                continue
            
            try:
                start = datetime.fromisoformat(program['start'])
                stop = datetime.fromisoformat(program['stop']) if program.get('stop') else start + timedelta(hours=2)
                
                if start <= now <= stop:
                    return program
            except:
                continue
        
        return None
    
    def get_channel_schedule(self, channel_id, hours=6):
        """Gelecek programları getir"""
        if channel_id not in self.epg_data.get('programs', {}):
            return []
        
        now = datetime.now()
        future = now + timedelta(hours=hours)
        
        schedule = []
        for program in self.epg_data['programs'][channel_id]:
            if not program.get('start'):
                continue
            
            try:
                start = datetime.fromisoformat(program['start'])
                if now <= start <= future:
                    schedule.append(program)
            except:
                continue
        
        return sorted(schedule, key=lambda x: x['start'])
    
    def save_epg_json(self, output_file='data/epg.json'):
        """JSON olarak kaydet"""
        if not self.epg_data:
            print("⚠️ Kaydedilecek veri yok")
            return False
        
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.epg_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 EPG JSON kaydedildi: {output_file}")
        return True
    
    def match_channel_to_epg(self, channel_name):
        """Kanal adını EPG ID'si ile eşleştir"""
        if not self.epg_data.get('channels'):
            return None
        
        def normalize(text):
            import re
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            text = re.sub(r'\s+', '', text)
            text = text.replace('tv', '').replace('hd', '').replace('türk', 'turk')
            return text
        
        channel_norm = normalize(channel_name)
        
        # Tam eşleşme
        for epg_id, epg_name in self.epg_data['channels'].items():
            if normalize(epg_name) == channel_norm:
                return epg_id
        
        # Kısmi eşleşme
        for epg_id, epg_name in self.epg_data['channels'].items():
            epg_norm = normalize(epg_name)
            if len(channel_norm) > 3 and (channel_norm in epg_norm or epg_norm in channel_norm):
                return epg_id
        
        return None
    
    def get_epg_stats(self):
        """İstatistikler"""
        if not self.epg_data:
            return None
        
        total_channels = len(self.epg_data.get('channels', {}))
        total_programs = sum(len(progs) for progs in self.epg_data.get('programs', {}).values())
        
        return {
            'total_channels': total_channels,
            'total_programs': total_programs,
            'last_update': self.epg_data.get('last_update', 'Bilinmiyor')
        }
    
    def create_mock_epg(self):
        """Profesyonel görünümlü örnek EPG oluştur"""
        print("📺 Örnek EPG verisi oluşturuluyor...")
        
        # Gerçek kanal isimleri
        mock_channels = {
            'TRT1.tr': 'TRT 1',
            'TRT2.tr': 'TRT 2',
            'TRTHaber.tr': 'TRT Haber',
            'TRTSpor.tr': 'TRT Spor',
            'TRTCocuk.tr': 'TRT Çocuk',
            'ATV.tr': 'ATV',
            'KanalD.tr': 'Kanal D',
            'ShowTV.tr': 'Show TV',
            'StarTV.tr': 'Star TV',
            'TV8.tr': 'TV8',
            'Kanal7.tr': 'Kanal 7',
            'NTV.tr': 'NTV',
            'Haberturk.tr': 'Habertürk',
            'HaberGlobal.tr': 'Haber Global',
            'NowTV.tr': 'Now TV',
            'ASpor.tr': 'A Spor',
        }
        
        # Gerçekçi program şablonları
        program_database = {
            'Genel': [
                ('Ana Haber', 60, 'Günün önemli haberleri'),
                ('Dizi: Kızılcık Şerbeti', 120, 'Aile dramı'),
                ('Dizi: Yalı Çapkını', 150, 'Romantik komedi'),
                ('Dizi: Ateş Kuşları', 120, 'Dram'),
                ('Film: Organize İşler', 120, 'Komedi filmi'),
                ('Film: Recep İvedik', 110, 'Komedi'),
                ('Gündüz Kuşağı', 90, 'Güncel konular'),
                ('Kim Milyoner Olmak İster?', 60, 'Yarışma'),
                ('Müge Anlı ile Tatlı Sert', 120, 'Magazin'),
                ('Esra Erol', 150, 'Talk show'),
                ('Belgesel: Evrim Ağacı', 45, 'Bilim belgeseli'),
                ('Müzik Programı', 90, 'Canlı performanslar'),
                ('O Ses Türkiye', 120, 'Müzik yarışması'),
            ],
            'Haber': [
                ('Ana Haber Bülteni', 60, 'Günün ana haberleri'),
                ('Sabah Bülteni', 120, 'Sabah haberleri'),
                ('Öğle Haberleri', 60, 'Öğle bülteni'),
                ('Akşam Haberleri', 90, 'Akşam bülteni'),
                ('Gece Haberleri', 45, 'Gün sonu özeti'),
                ('Gündem Özel', 60, 'Derinlemesine analiz'),
                ('Ekonomi Saati', 30, 'Ekonomi haberleri'),
                ('Dünya Gündemi', 45, 'Uluslararası haberler'),
                ('5. Gün', 60, 'Haber programı'),
                ('Teke Tek', 45, 'Tartışma programı'),
            ],
            'Spor': [
                ('Spor Haberleri', 30, 'Günün spor haberleri'),
                ('Canlı Maç: Galatasaray - Fenerbahçe', 120, 'Süper Lig'),
                ('Canlı Maç: Beşiktaş - Trabzonspor', 120, 'Süper Lig'),
                ('Maç Öncesi', 60, 'Maç analizi'),
                ('Maç Sonrası', 45, 'Maç değerlendirmesi'),
                ('Spor Ajansı', 60, 'Spor magazini'),
                ('Futbol Net', 90, 'Futbol programı'),
                ('Takım Oyunu', 60, 'Spor tartışma'),
                ('100% Futbol', 120, 'Haftalık futbol'),
                ('Basketbol: Fenerbahçe - Anadolu Efes', 120, 'Basketbol Süper Ligi'),
            ],
            'Çocuk': [
                ('Pepee', 30, 'Eğitici çizgi film'),
                ('Caillou', 30, 'Çizgi film'),
                ('TRT Çocuk Kuşağı', 45, 'Çocuk programları'),
                ('Rafadan Tayfa', 30, 'Macera çizgi filmi'),
                ('Keloğlan', 30, 'Masal çizgi filmi'),
                ('Heidi', 30, 'Klasik çizgi film'),
                ('Maysa ve Bulut', 30, 'Eğitici program'),
                ('İbi', 30, 'Çizgi film'),
            ],
        }
        
        mock_programs = {}
        
        # Bugünün başlangıcı (saat 06:00)
        base_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
        
        for ch_id, ch_name in mock_channels.items():
            mock_programs[ch_id] = []
            
            # Kanal kategorisini belirle
            if 'Haber' in ch_name or ch_name in ['NTV', 'Habertürk', 'Haber Global']:
                category = 'Haber'
                templates = program_database['Haber']
            elif 'Spor' in ch_name or ch_name == 'A Spor':
                category = 'Spor'
                templates = program_database['Spor']
            elif 'Çocuk' in ch_name:
                category = 'Çocuk'
                templates = program_database['Çocuk']
            else:
                category = 'Genel'
                templates = program_database['Genel']
            
            # 2 gün boyunca program oluştur (bugün + yarın)
            current_time = base_time
            end_time = base_time + timedelta(days=2)
            
            while current_time < end_time:
                # Rastgele program seç
                program_title, duration, description = random.choice(templates)
                
                start_time = current_time
                stop_time = start_time + timedelta(minutes=duration)
                
                mock_programs[ch_id].append({
                    'start': start_time.isoformat(),
                    'stop': stop_time.isoformat(),
                    'title': program_title,
                    'description': description,
                    'category': category
                })
                
                current_time = stop_time
        
        self.epg_data = {
            'channels': mock_channels,
            'programs': mock_programs,
            'last_update': datetime.now().isoformat(),
            'is_mock': True,
            'note': 'Bu EPG verisi örnek/test amaçlıdır. Gerçek program akışını yansıtmayabilir.'
        }
        
        total_programs = sum(len(progs) for progs in mock_programs.values())
        print(f"✅ {len(mock_channels)} kanal için {total_programs:,} program oluşturuldu")
        print(f"📅 Kapsanan süre: 2 gün (bugün + yarın)")
        
        return self.epg_data


# ═══════════════════════════════════════════════════════════════════════════════
#                              TEST
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    epg = EPGManager()
    
    print("📺 EPG Oluşturuluyor...\n")
    
    # Direkt mock EPG oluştur
    epg.create_mock_epg()
    epg.save_epg_json()
    
    stats = epg.get_epg_stats()
    
    print("\n" + "═" * 80)
    print("📊 EPG İSTATİSTİKLERİ")
    print("═" * 80)
    print(f"📺 Toplam Kanal  : {stats['total_channels']}")
    print(f"📅 Toplam Program: {stats['total_programs']:,}")
    print(f"🕒 Son Güncelleme: {stats['last_update'][:19]}")
    print("═" * 80)
    
    # Örnek: TRT 1 bugünkü programlar
    print("\n📋 TRT 1 - Bugünkü Program Akışı (İlk 10)")
    print("─" * 80)
    trt1_programs = epg.epg_data['programs'].get('TRT1.tr', [])
    today = datetime.now().date()
    
    count = 0
    for prog in trt1_programs:
        start = datetime.fromisoformat(prog['start'])
        if start.date() == today:
            stop = datetime.fromisoformat(prog['stop'])
            print(f"{start.strftime('%H:%M')}-{stop.strftime('%H:%M')} | {prog['title']}")
            count += 1
            if count >= 10:
                break
    
    print("─" * 80)
    
    # Şu anki program
    print("\n🔴 ŞUAN YAYINDA")
    print("─" * 80)
    for ch_id, ch_name in list(epg.epg_data['channels'].items())[:5]:
        current = epg.get_current_program(ch_id)
        if current:
            print(f"📺 {ch_name:15s} → {current['title']}")
        else:
            print(f"📺 {ch_name:15s} → Program bilgisi yok")
    
    print("═" * 80)