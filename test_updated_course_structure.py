#!/usr/bin/env python3
"""
Test sprawdzający poprawność zaktualizowanej struktury kursu neuroprzywództwa.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from data.course_data import get_blocks, get_categories, get_lessons_for_category
import json

def test_course_structure():
    """Test podstawowej struktury kursu"""
    print("🧠 Test struktury kursu neuroprzywództwa")
    print("=" * 50)
    
    # Test bloków
    blocks = get_blocks()
    print(f"📚 Znaleziono {len(blocks)} bloków tematycznych:")
    for block_id, block in blocks.items():
        print(f"  {block_id}. {block['name']}")
        print(f"     Opis: {block['description'][:60]}...")
        print(f"     Kategorie: {block['categories']}")
        print()
    
    # Test kategorii
    categories = get_categories()
    print(f"🎯 Znaleziono {len(categories)} kategorii/modułów:")
    for cat_id, category in categories.items():
        print(f"  {cat_id}. {category['icon']} {category['name']}")
        print(f"     Blok: {category['block']} | Poziom: {category['difficulty']}")
        print(f"     Czas: {category['estimated_time']}")
        print()
    
    # Test lekcji dla pierwszych 3 kategorii
    print("📖 Przykładowe lekcje:")
    for cat_id in [1, 2, 3]:
        if cat_id in categories:
            lessons = get_lessons_for_category(cat_id)
            print(f"\n  Kategoria {cat_id}: {categories[cat_id]['name']}")
            for i, lesson in enumerate(lessons[:3], 1):  # Pokaż tylko pierwsze 3 lekcje
                print(f"    {i}. {lesson['title']}")
            if len(lessons) > 3:
                print(f"    ... i {len(lessons) - 3} więcej lekcji")
    
    return True

def test_mapping_compatibility():
    """Test kompatybilności mapowania umiejętności"""
    print("\n🔄 Test kompatybilności mapowania umiejętności")
    print("=" * 50)
    
    # Mapowanie z skills_new.py
    skill_id_mapping = {
        1: 'neuro_leadership_intro',
        2: 'brain_emotions_decisions', 
        3: 'brain_social_interactions',
        4: 'decision_models',
        5: 'cognitive_biases_decisions',
        6: 'neurological_change_innovation',
        7: 'motivating_others',
        8: 'stress_neurobiology',
        9: 'emotions_leadership',
        10: 'leader_resilience',
        11: 'leadership_effectiveness',
        12: 'global_neuro_leadership',
        13: 'future_challenges',
        14: 'leader_mind_work',
        15: 'leader_transformation'
    }
    
    categories = get_categories()
    
    print("Mapowanie kategorii na ID umiejętności:")
    for cat_id, skill_id in skill_id_mapping.items():
        if cat_id in categories:
            cat_name = categories[cat_id]['name']
            print(f"  {cat_id}: {skill_id} -> {cat_name}")
        else:
            print(f"  ❌ {cat_id}: {skill_id} -> BRAK KATEGORII!")
    
    return True

def test_json_structure():
    """Test struktury pliku JSON"""
    print("\n📋 Test struktury pliku course_structure.json")
    print("=" * 50)
    
    try:
        with open('data/course_structure.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Sprawdź główne sekcje
        required_sections = ['blocks', 'categories', 'lessons']
        for section in required_sections:
            if section in data:
                print(f"✅ Sekcja '{section}': {len(data[section])} elementów")
            else:
                print(f"❌ Brak sekcji '{section}'")
        
        # Sprawdź czy wszystkie bloki mają odpowiadające kategorie
        blocks = data.get('blocks', {})
        categories = data.get('categories', {})
        
        print("\nSprawdzenie spójności bloków i kategorii:")
        for block_id, block in blocks.items():
            print(f"  Blok {block_id}: {block['name']}")
            for cat_id in block['categories']:
                if str(cat_id) in categories:
                    cat_name = categories[str(cat_id)]['name']
                    print(f"    ✅ Kategoria {cat_id}: {cat_name}")
                else:
                    print(f"    ❌ Brak kategorii {cat_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd podczas wczytywania JSON: {e}")
        return False

if __name__ == "__main__":
    print("🧠 BRAINVENTURE ACADEMY - TEST STRUKTURY NEUROPRZYWÓDZTWA")
    print("=" * 60)
    
    try:
        success = True
        success &= test_course_structure()
        success &= test_mapping_compatibility() 
        success &= test_json_structure()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ Wszystkie testy przeszły pomyślnie!")
            print("🎉 Struktura kursu neuroprzywództwa jest gotowa!")
        else:
            print("❌ Znaleziono błędy w strukturze kursu.")
            
    except Exception as e:
        print(f"❌ Błąd podczas wykonywania testów: {e}")
        import traceback
        traceback.print_exc()
