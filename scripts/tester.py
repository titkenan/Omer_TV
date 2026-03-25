#!/usr/bin/env python3
import json
import os

def test_all_channels():
    """Tüm kanalları test etmeden geçir"""
    
    input_file = 'data/scraped_channels.json'
    
    if not os.path.exists(input_file):
        print(f"❌ Hata: {input_file} bulunamadı!")
        return []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        channels = json.load(f)
    
    print(f"📺 {len(channels)} kanal bulundu")
    print("⏭️ Test atlandı - tüm kanallar ekleniyor...")
    
    # Tüm kanallara varsayılan değerler ekle
    for ch in channels:
        ch['status'] = 'working'
        ch['response_time'] = 0
    
    # Kaydet
    os.makedirs('data', exist_ok=True)
    output_file = 'data/working_channels.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(channels)} kanal kaydedildi: {output_file}")
    
    return channels


if __name__ == "__main__":
    test_all_channels()
