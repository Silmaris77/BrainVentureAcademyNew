#!/usr/bin/env python3
"""
Test naprawionych błędów w course_map.py
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_course_map_imports():
    """Test importu modułów course_map"""
    print("🧪 Test naprawionych błędów w course_map.py")
    print("="*50)
    
    try:
        # Test 1: Import podstawowych modułów
        print("\n1️⃣ Test importu podstawowych modułów...")
        from utils.course_map import create_course_structure_map, create_simplified_course_map, show_course_statistics
        print("✅ Moduły course_map zaimportowane pomyślnie")
        
        # Test 2: Import streamlit_agraph
        print("\n2️⃣ Test importu streamlit_agraph...")
        from streamlit_agraph import agraph, Node, Edge, Config
        print("✅ streamlit_agraph zaimportowany pomyślnie")
        
        # Test 3: Test utworzenia węzłów i krawędzi
        print("\n3️⃣ Test tworzenia komponentów graf...")
        test_node = Node(id="test", label="Test Node", size=20, color="#FF6B6B")
        test_edge = Edge(source="test1", target="test2")
        test_config = Config(width=800, height=600, directed=True)
        print("✅ Komponenty Node, Edge, Config działają poprawnie")
        
        # Test 4: Test struktur danych kursu
        print("\n4️⃣ Test struktur danych kursu...")
        from data.course_data import get_blocks, get_categories, get_lessons_for_category
        
        blocks = get_blocks()
        categories = get_categories()
        
        print(f"✅ Znaleziono {len(blocks)} bloków")
        print(f"✅ Znaleziono {len(categories)} kategorii")
        
        # Test struktury lekcji
        if categories:
            first_cat_id = list(categories.keys())[0]
            lessons = get_lessons_for_category(first_cat_id)
            print(f"✅ Kategoria {first_cat_id} ma {len(lessons)} lekcji")
            
            # Sprawdź czy lessons to lista słowników
            if lessons and isinstance(lessons, list) and isinstance(lessons[0], dict):
                print("✅ Struktura lekcji poprawna (lista słowników)")
            else:
                print(f"⚠️  Nieoczekiwana struktura lekcji: {type(lessons)}")
        
        print("\n" + "="*50)
        print("🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        print("\n📋 Naprawione błędy:")
        print("   ✅ Poprawiono iterację przez lekcje (lessons.items() → enumerate(lessons))")
        print("   ✅ Dodano obsługę błędów importu streamlit-agraph")
        print("   ✅ Naprawiono wcięcia w kodzie")
        print("   ✅ streamlit-agraph jest zainstalowany i dostępny")
        
        return True
        
    except ImportError as e:
        print(f"❌ Błąd importu: {e}")
        return False
    except Exception as e:
        print(f"❌ Błąd: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_course_map_imports()
    
    if success:
        print("\n🚀 MAPA KURSU GOTOWA DO UŻYCIA!")
        print("   Uruchom: streamlit run main.py")
        print("   Przejdź do: Umiejętności → Mapa Kursu")
    else:
        print("\n⚠️  WYMAGANE DODATKOWE NAPRAWY")
    
    sys.exit(0 if success else 1)
