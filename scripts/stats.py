import json
from datetime import datetime


def generate_stats():
    """İstatistik JSON'u oluştur"""
    
    with open('data/working_channels.json', 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    stats = {
        'total_channels': len(channels),
        'last_update': datetime.now().isoformat(),
        'categories': {},
        'average_response_time': 0
    }
    
    total_time = 0
    for ch in channels:
        cat = ch.get('category', 'Diğer')
        stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
        total_time += ch.get('response_time', 0)
    
    if channels:
        stats['average_response_time'] = round(total_time / len(channels), 2)
    
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ stats.json oluşturuldu")
    print(f"📊 {stats['total_channels']} kanal")
    print(f"⏱️ Ortalama yanıt: {stats['average_response_time']}ms")


if __name__ == "__main__":
    generate_stats()
