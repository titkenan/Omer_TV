import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


class StreamTester:
    def __init__(self, timeout=10, max_workers=10):
        self.timeout = timeout
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def test_single_stream(self, channel):
        """Tek bir stream'i test et"""
        url = channel.get('url')
        name = channel.get('name', 'Unknown')
        
        result = {
            'name': name,
            'url': url,
            'status': 'unknown',
            'response_time': None,
            'status_code': None,
            'content_type': None,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            start_time = time.time()
            response = self.session.head(
                url, 
                timeout=self.timeout, 
                allow_redirects=True
            )
            response_time = round((time.time() - start_time) * 1000, 2)  # ms
            
            result['response_time'] = response_time
            result['status_code'] = response.status_code
            result['content_type'] = response.headers.get('Content-Type', 'unknown')
            
            if response.status_code in [200, 302, 301]:
                result['status'] = 'working'
                
                # Kalite değerlendirmesi
                if response_time < 500:
                    result['quality'] = 'excellent'
                elif response_time < 1500:
                    result['quality'] = 'good'
                elif response_time < 3000:
                    result['quality'] = 'fair'
                else:
                    result['quality'] = 'poor'
            else:
                result['status'] = 'failed'
                result['quality'] = 'unavailable'
        
        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            result['error'] = 'Connection timeout'
        except requests.exceptions.ConnectionError:
            result['status'] = 'connection_error'
            result['error'] = 'Cannot connect to stream'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def test_all_streams(self, channels):
        """Tüm stream'leri paralel olarak test et"""
        print(f"\n🧪 {len(channels)} stream test ediliyor...")
        print(f"⚙️ Paralel işlem sayısı: {self.max_workers}")
        print("─" * 80)
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.test_single_stream, ch): ch 
                for ch in channels
            }
            
            completed = 0
            total = len(futures)
            
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                results.append(result)
                
                # İlerleme göstergesi
                status_emoji = {
                    'working': '✅',
                    'timeout': '⏱️',
                    'failed': '❌',
                    'connection_error': '🔌',
                    'error': '⚠️'
                }.get(result['status'], '❓')
                
                quality_info = ''
                if result.get('response_time'):
                    quality_info = f" ({result['response_time']}ms)"
                
                print(f"[{completed}/{total}] {status_emoji} {result['name'][:40]}{quality_info}")
        
        return results
    
    def generate_report(self, results, output_file='test_results.json'):
        """Test sonuçlarını raporla"""
        # İstatistikler
        total = len(results)
        working = len([r for r in results if r['status'] == 'working'])
        failed = len([r for r in results if r['status'] in ['failed', 'timeout', 'connection_error', 'error']])
        
        # Kalite dağılımı
        quality_dist = {}
        for r in results:
            quality = r.get('quality', 'unknown')
            quality_dist[quality] = quality_dist.get(quality, 0) + 1
        
        # Ortalama yanıt süresi
        response_times = [r['response_time'] for r in results if r['response_time']]
        avg_response = round(sum(response_times) / len(response_times), 2) if response_times else 0
        
        report = {
            'summary': {
                'total_streams': total,
                'working': working,
                'failed': failed,
                'success_rate': round((working / total * 100), 2) if total > 0 else 0,
                'avg_response_time_ms': avg_response,
                'quality_distribution': quality_dist,
                'test_date': datetime.now().isoformat()
            },
            'results': results
        }
        
        # JSON olarak kaydet
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Konsol raporu
        print("\n" + "═" * 80)
        print("📊 TEST RAPORU")
        print("═" * 80)
        print(f"✅ Çalışan: {working}/{total} (%{report['summary']['success_rate']})")
        print(f"❌ Çalışmayan: {failed}")
        print(f"⏱️ Ortalama yanıt: {avg_response}ms")
        print(f"\n📈 Kalite Dağılımı:")
        for quality, count in quality_dist.items():
            print(f"   {quality.capitalize()}: {count}")
        print(f"\n💾 Detaylı rapor: {output_file}")
        print("═" * 80)
        
        return report
    
    def get_working_streams(self, results):
        """Sadece çalışan stream'leri döndür"""
        return [r for r in results if r['status'] == 'working']


# ═══════════════════════════════════════════════════
#                    TEST KULLANIMI
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    # Örnek kanallar
    test_channels = [
        {'name': 'TRT 1', 'url': 'https://tv-trt1.medya.trt.com.tr/master.m3u8'},
        {'name': 'ATV', 'url': 'https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8'},
        {'name': 'Kanal D', 'url': 'https://ackaxsqacw.turknet.ercdn.net/ozfkfbbjba/kanald/kanald_1080p.m3u8'},
    ]
    
    tester = StreamTester(timeout=10, max_workers=5)
    results = tester.test_all_streams(test_channels)
    tester.generate_report(results)