#!/usr/bin/env python3
"""
Test systemu mind map - sprawdza czy nowy system działa poprawnie
"""

import sys
import os
import json

# Dodaj path do głównego folderu
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_mind_map_system():
    """Test głównych funkcji systemu mind map"""
    
    # Import funkcji
    try:
        from utils.mind_map import create_lesson_mind_map, create_data_driven_mind_map, create_auto_generated_mind_map
        print("✅ Import funkcji mind_map pomyślny")
    except ImportError as e:
        print(f"❌ Błąd importu funkcji mind_map: {e}")
        return
    
    print("🧪 Testowanie systemu mind map...")
    
    # Test 1: Ładowanie lekcji B1C1L1 z nową strukturą mind_map
    print("\n1️⃣ Test data-driven mind map dla B1C1L1...")
    
    lesson_data = None
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
                else:
                    print(f"❌ Brak sekcji: {key}")
        else:
            print("❌ Brak struktury mind_map w lekcji")
            
    except Exception as e:
        print(f"❌ Błąd przy ładowaniu lekcji: {e}")
        lesson_data = None
    
    # Test 2: Testowanie funkcji create_data_driven_mind_map (bez wyświetlania)
    print("\n2️⃣ Test funkcji create_data_driven_mind_map...")
    
    try:
        if lesson_data and 'mind_map' in lesson_data:
            # Sprawdź czy funkcja się nie crashuje
            result = create_data_driven_mind_map(lesson_data['mind_map'])
            if result is not None:
                print("✅ Funkcja create_data_driven_mind_map działa")
            else:
                print("⚠️ Funkcja zwróciła None (prawdopodobnie brak streamlit-agraph)")
        else:
            print("❌ Brak danych mind_map do testu")
            
    except ImportError:
        print("⚠️ Brak biblioteki streamlit-agraph - normalny fallback")
    except Exception as e:
        print(f"❌ Błąd w funkcji create_data_driven_mind_map: {e}")
    
    # Test 3: Testowanie głównej funkcji create_lesson_mind_map
    print("\n3️⃣ Test głównej funkcji create_lesson_mind_map...")
    
    try:
        # Test z lekcją B1C1L1 (powinna użyć data-driven)
        if lesson_data:
            result = create_lesson_mind_map(lesson_data)
            if result is not None:
                print("✅ Funkcja create_lesson_mind_map działa dla B1C1L1")
            else:
                print("⚠️ Funkcja zwróciła None (prawdopodobnie brak streamlit-agraph)")
        else:
            print("❌ Brak danych lekcji do testu")
    except Exception as e:
        print(f"❌ Błąd w funkcji create_lesson_mind_map: {e}")
    
    # Test 4: Testowanie auto-generated mind map
    print("\n4️⃣ Test auto-generated mind map...")
    
    try:
        # Stwórz fake lekcję bez mind_map
        fake_lesson = {
            "id": "TEST",
            "title": "Test Lesson",
            "xp_reward": 50,
            "sections": {
                "learning": {
                    "sections": [
                        {"title": "Sekcja 1"},
                        {"title": "Sekcja 2"}
                    ]
                },
                "opening_quiz": True,
                "reflection": True
            }
        }
        
        result = create_auto_generated_mind_map(fake_lesson)
        if result is not None:
            print("✅ Funkcja create_auto_generated_mind_map działa")
        else:
            print("⚠️ Funkcja zwróciła None (prawdopodobnie brak streamlit-agraph)")
            
    except Exception as e:
        print(f"❌ Błąd w funkcji create_auto_generated_mind_map: {e}")
    
    print("\n🎯 Test zakończony!")

if __name__ == "__main__":
    test_mind_map_system()
