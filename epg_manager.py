import requests
import json
import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os


class EPGManager:
    def __init__(self):
        # 2024 çalışan Türkiye EPG kaynakları
        self.epg_sources = [
            # IPTV-ORG (En güncel)
            'https://iptv-org.github.io/epg/guides/tr/tvplus.com.tr.epg.xml',
            'https://iptv-org.github.io/epg/guides/tr/turk.tv.epg.xml',
            
            # Telekom EPG
            'http://www.telkutvplus.com.tr/EPG/tvplus.xml.gz',
            
            # Alternatif kaynaklar
            'https://www.bevy.be/bevyfiles/turkey.xml',
            'https://www.bevy.be/bevyfiles/turkeypremium.xml',
            
            # GitHub ücretsiz kaynaklar
            'https://raw.githubusercontent.com/mitthu/iptv-epg/main/epg.xml',
        ]
        self.epg_data = {}
    
    def download_epg(self, url, save_path='data/epg.xml'):
        """EPG XML dosyasını indir (gzip desteği ile)"""
        print(f"📡 EPG indiriliyor: {url[:80]}...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, timeout=60, stream=True, headers=headers, verify=False)
            response.raise_for_status()
            
            # Gzip kontrolü
            is_gzip = url.endswith('.gz') or response.headers.get('Content-Encoding') == 'gzip'
            
            if is_gzip:
                print("🗜️ Gzip sıkıştırması tespit edildi, açılıyor...")
                try:
                    content = gzip.decompress(response.content)
                    with open(save_path, 'wb') as f:
                        f.write(content)
                except Exception as e:
                    print(f"⚠️ Gzip açma hatası: {e}")
                    return None
            else:
                # Normal XML
                with open(save_path, 'wb') as f:
                    total = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            total += len(chunk)
                    print(f"📦 İndirilen: {total:,} byte")
            
            # Dosya boyutunu kontrol et
            file_size = os.path.getsize(save_path)
            if file_size < 1000:  # 1KB'dan küçükse hatalı
                print(f"⚠️ Dosya çok küçük ({file_size} byte), geçersiz olabilir")
                
                # İçeriğe bak
                with open(save_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview = f.read(200)
                    print(f"📄 Dosya içeriği: {preview[:100]}...")
                
                return None
            
            print(f"✅ EPG kaydedildi: {save_path} ({file_size:,} byte)")
            return save_path
        
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if '404' in error_msg:
                print(f"❌ Dosya bulunamadı (404)")
            elif 'timeout' in error_msg.lower():
                print(f"❌ Zaman aşımı (timeout)")
            else:
                print(f"❌ İndirme hatası: {error_msg[:100]}")
            return None
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return None
    
    def parse_epg(self, xml_file):
        """EPG XML'ini parse et"""
        print(f"🔍 EPG parse ediliyor...")
        
        try:
            # Encoding denemesi
            encodings = ['utf-8', 'iso-8859-9', 'windows-1254']
            
            tree = None
            for encoding in encodings:
                try:
                    tree = ET.parse(xml_file)
                    print(f"✅ Encoding: {encoding}")
                    break
                except ET.ParseError:
                    continue
                except Exception:
                    continue
            
            if not tree:
                print("❌ XML parse edilemedi (encoding sorunu)")
                return None
            
            root = tree.getroot()
            
            # Root tag kontrolü
            if root.tag not in ['tv', 'TV']:
                print(f"⚠️ Beklenmeyen root tag: {root.tag}")
            
            # Kanalları parse et
            channels = {}
            for channel in root.findall('.//channel'):
                ch_id = channel.get('id')
                if not ch_id:
                    continue
                
                # Birden fazla display-name olabilir
                names = channel.findall('display-name')
                if names and names[0].text:
                    channels[ch_id] = names[0].text
            
            print(f"📺 {len(channels)} kanal bulundu")
            
            if not channels:
                print("⚠️ Hiç kanal bulunamadı!")
                return None
            
            # Programları parse et
            programs = {}
            program_count = 0
            
            for programme in root.findall('.//programme'):
                ch_id = programme.get('channel')
                if not ch_id:
                    continue
                
                start = programme.get('start')
                stop = programme.get('stop')
                
                if not start:
                    continue
                
                # Başlık
                title_elem = programme.find('title')
                title_text = 'Bilinmiyor'
                if title_elem is not None and title_elem.text:
                    title_text = title_elem.text
                
                # Açıklama
                desc_elem = programme.find('desc')
                desc_text = ''
                if desc_elem is not None and desc_elem.text:
                    desc_text = desc_elem.text
                
                # Kategori
                category_elem = programme.find('category')
                category = category_elem.text if category_elem is not None and category_elem.text else ''
                
                if ch_id not in programs:
                    programs[ch_id] = []
                
                parsed_start = self._parse_xmltv_time(start)
                parsed_stop = self._parse_xmltv_time(stop) if stop else None
                
                if parsed_start:  # En azından başlangıç zamanı olmalı
                    programs[ch_id].append({
                        'start': parsed_start,
                        'stop': parsed_stop,
                        'title': title_text,
                        'description': desc_text,
                        'category': category
                    })
                    program_count += 1
            
            print(f"📅 {program_count} program bulundu")
            
            if not programs:
                print("⚠️ Hiç program bulunamadı!")
                # Yine de kanalları kaydet
                self.epg_data = {
                    'channels': channels,
                    'programs': {},
                    'last_update': datetime.now().isoformat()
                }
                return self.epg_data
            
            self.epg_data = {
                'channels': channels,
                'programs': programs,
                'last_update': datetime.now().isoformat()
            }
            
            print(f"✅ Toplam: {len(channels)} kanal, {program_count:,} program")
            return self.epg_data
        
        except ET.ParseError as e:
            print(f"❌ XML parse hatası: {e}")
            return None
        except Exception as e:
            print(f"❌ Parse hatası: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _parse_xmltv_time(self, time_str):
        """XMLTV zaman formatını parse et"""
        if not time_str:
            return None
        try:
            # Format: 20240325120000 +0300 veya 20240325120000
            dt_str = time_str.split()[0][:14]  # Sadece tarih kısmı
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
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.epg_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 EPG JSON kaydedildi: {output_file}")
        return True
    
    def match_channel_to_epg(self, channel_name):
        """Kanal adını EPG ID'si ile eşleştir"""
        if not self.epg_data.get('channels'):
            return None
        
        def normalize(text):
            """Metni normalize et"""
            import re
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)  # Özel karakterleri kaldır
            text = re.sub(r'\s+', '', text)  # Boşlukları kaldır
            text = text.replace('tv', '').replace('hd', '')
            return text
        
        channel_norm = normalize(channel_name)
        
        # Önce tam eşleşme dene
        for epg_id, epg_name in self.epg_data['channels'].items():
            if normalize(epg_name) == channel_norm:
                return epg_id
        
        # Kısmi eşleşme
        for epg_id, epg_name in self.epg_data['channels'].items():
            epg_norm = normalize(epg_name)
            if channel_norm in epg_norm or epg_norm in channel_norm:
                if len(channel_norm) > 3:  # En az 4 karakter benzerlik
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
        """EPG bulunamazsa sahte veri oluştur (test için)"""
        print("⚠️ Gerçek EPG bulunamadı, örnek veri oluşturuluyor...")
        
        mock_channels = {
            'TRT1': 'TRT 1',
            'ATV': 'ATV',
            'KanalD': 'Kanal D',
            'ShowTV': 'Show TV',
            'StarTV': 'Star TV',
            'TV8': 'TV8',
            'Kanal7': 'Kanal 7',
        }
        
        mock_programs = {}
        now = datetime.now()
        
        for ch_id in mock_channels.keys():
            mock_programs[ch_id] = []
            for i in range(10):
                start_time = now + timedelta(hours=i*2)
                stop_time = start_time + timedelta(hours=2)
                
                mock_programs[ch_id].append({
                    'start': start_time.isoformat(),
                    'stop': stop_time.isoformat(),
                    'title': f'Program {i+1}',
                    'description': 'Örnek program açıklaması',
                    'category': 'Eğlence'
                })
        
        self.epg_data = {
            'channels': mock_channels,
            'programs': mock_programs,
            'last_update': datetime.now().isoformat(),
            'is_mock': True
        }
        
        return self.epg_data


# ═══════════════════════════════════════════════════
#                    TEST
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()  # SSL uyarılarını kapat
    
    epg = EPGManager()
    
    print("🔍 EPG kaynakları test ediliyor...\n")
    
    for i, source in enumerate(epg.epg_sources, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(epg.epg_sources)}] {source}")
        print('='*80)
        
        xml_file = epg.download_epg(source)
        if xml_file:
            epg_data = epg.parse_epg(xml_file)
            if epg_data:
                epg.save_epg_json()
                stats = epg.get_epg_stats()
                
                print("\n✅ BAŞARILI!")
                print(f"📺 Kanallar: {stats['total_channels']}")
                print(f"📅 Programlar: {stats['total_programs']:,}")
                break
    else:
        print("\n⚠️ Tüm kaynaklar başarısız, örnek veri oluşturuluyor...")
        epg.create_mock_epg()
        epg.save_epg_json()