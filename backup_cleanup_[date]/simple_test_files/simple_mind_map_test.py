#!/usr/bin/env python3
"""
Prosty test mapy myśli
"""
import json

print("🧠 PROSTY TEST MAPY MYŚLI")
print("="*40)

# Test 1: Załaduj dane lekcji
print("1. Ładowanie B2C1L1.json...")
try:
    with open("data/lessons/B2C1L1.json", 'r', encoding='utf-8') as f:
        lesson_data = json.load(f)
    
    title = lesson_data.get('title', 'Brak tytułu')
    print(f"✅ Lekcja: {title}")
    
    # Sprawdź learning sections
    if 'sections' in lesson_data and 'learning' in lesson_data['sections']:
        learning = lesson_data['sections']['learning']
        if 'sections' in learning:
            sections = learning['sections']
            print(f"✅ Znaleziono {len(sections)} sekcji learning")
            
            for i, section in enumerate(sections[:3]):  # Pokaż pierwsze 3
                section_title = section.get('title', f'Sekcja {i+1}')[:50]
                print(f"   {i+1}. {section_title}...")
        else:
            print("❌ Brak 'sections' w learning")
    else:
        print("❌ Brak struktury learning")
        
except Exception as e:
    print(f"❌ Błąd: {e}")

print("\n✅ Test zakończony")
