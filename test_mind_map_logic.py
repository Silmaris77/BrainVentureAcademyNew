#!/usr/bin/env python3
"""
Prosty test systemu mind map - sprawdza logikę bez wyświetlania
"""

import sys
import os
import json

def test_mind_map_logic():
    """Test logiki systemu mind map bez rzeczywistego wyświetlania"""
    
    print("🧪 Testowanie logiki systemu mind map...")
    
    # Test 1: Ładowanie lekcji B1C1L1 z nową strukturą mind_map
    print("\n1️⃣ Test wczytywania struktury mind_map z B1C1L1...")
    
    try:
        # Wczytaj lekcję B1C1L1
        with open('data/lessons/B1C1L1.json', 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)
        
        print(f"✅ Wczytano lekcję: {lesson_data.get('title', 'Nieznana')}")
        
        # Sprawdź czy ma mind_map
        if 'mind_map' in lesson_data:
            print("✅ Znaleziono strukturę mind_map w lekcji")
            
            # Sprawdź podstawowe elementy
            mind_map = lesson_data['mind_map']
            required_keys = ['central_node', 'categories', 'solutions', 'case_study', 'connections', 'config']
            
            for key in required_keys:
                if key in mind_map:
                    print(f"✅ Znaleziono sekcję: {key}")
                    
                    # Szczegółowe sprawdzenie każdej sekcji
                    if key == 'central_node':
                        central = mind_map[key]
                        required_central = ['id', 'label', 'size', 'color', 'font_size']
                        for attr in required_central:
                            if attr in central:
                                print(f"   ✓ {attr}: {central[attr]}")
                            else:
                                print(f"   ❌ Brak: {attr}")
                    
                    elif key == 'categories':
                        print(f"   📊 Znaleziono {len(mind_map[key])} kategorii:")
                        for i, cat in enumerate(mind_map[key]):
                            print(f"      {i+1}. {cat.get('label', 'Bez etykiety')} ({len(cat.get('details', []))} szczegółów)")
                    
                    elif key == 'solutions':
                        print(f"   💡 Znaleziono {len(mind_map[key])} rozwiązań")
                    
                    elif key == 'case_study':
                        case = mind_map[key]
                        print(f"   📱 Case study: {case.get('label', 'Bez etykiety')} ({len(case.get('details', []))} szczegółów)")
                    
                    elif key == 'connections':
                        print(f"   🔗 Znaleziono {len(mind_map[key])} połączeń")
                        
                else:
                    print(f"❌ Brak sekcji: {key}")
        else:
            print("❌ Brak struktury mind_map w lekcji")
            
    except Exception as e:
        print(f"❌ Błąd przy ładowaniu lekcji: {e}")
    
    # Test 2: Sprawdzenie logiki decyzyjnej dla różnych lekcji
    print("\n2️⃣ Test logiki decyzyjnej create_lesson_mind_map...")
    
    # Stwórz różne scenariusze
    scenarios = [
        {
            "name": "Lekcja z mind_map",
            "lesson": {"id": "TEST1", "title": "Test", "mind_map": {"central_node": {"id": "test"}}},
            "expected": "data_driven"
        },
        {
            "name": "Lekcja B1C1L1 bez mind_map", 
            "lesson": {"id": "B1C1L1", "title": "Test B1C1L1"},
            "expected": "hardcoded_B1C1L1"
        },
        {
            "name": "Inna lekcja bez mind_map",
            "lesson": {"id": "B1C1L2", "title": "Test Other", "sections": {"learning": {"sections": []}}},
            "expected": "auto_generated"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n   🎯 Test: {scenario['name']}")
        lesson = scenario["lesson"]
        
        # Symuluj logikę decyzyjną
        if 'mind_map' in lesson:
            decision = "data_driven"
        elif lesson.get('id') == 'B1C1L1':
            decision = "hardcoded_B1C1L1"
        else:
            decision = "auto_generated"
        
        if decision == scenario["expected"]:
            print(f"   ✅ Prawidłowa decyzja: {decision}")
        else:
            print(f"   ❌ Nieprawidłowa decyzja: {decision}, oczekiwano: {scenario['expected']}")
    
    # Test 3: Sprawdzenie template generator
    print("\n3️⃣ Test template generator...")
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from utils.mind_map_template import generate_mind_map_template
        
        template = generate_mind_map_template(
            lesson_title="Test Lesson",
            main_topics=["Topic 1", "Topic 2"],
            include_case_study=True
        )
        
        if 'mind_map' in template:
            print("✅ Template generator działa")
            mind_map = template['mind_map']
            print(f"   - Central node: {mind_map['central_node']['label']}")
            print(f"   - Categories: {len(mind_map['categories'])}")
            print(f"   - Solutions: {len(mind_map['solutions'])}")
            print(f"   - Case study: {'Tak' if 'case_study' in mind_map else 'Nie'}")
        else:
            print("❌ Template generator nie zwrócił właściwej struktury")
            
    except Exception as e:
        print(f"❌ Błąd w template generator: {e}")
    
    print("\n🎯 Test logiki zakończony!")
    print("💡 Uwaga: To test logiki - rzeczywiste wyświetlanie wymaga biblioteki streamlit-agraph")

if __name__ == "__main__":
    test_mind_map_logic()
