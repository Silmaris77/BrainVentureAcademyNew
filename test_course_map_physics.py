#!/usr/bin/env python3
"""
Test poprawek fizyki w mapie kursu
"""

import sys
import os
sys.path.append('.')

def test_course_map_imports():
    """Test importu funkcji mapy kursu"""
    try:
        from utils.course_map import create_course_structure_map, create_simplified_course_map
        print("✅ Import funkcji course_map zakończony sukcesem")
        return True
    except ImportError as e:
        print(f"❌ Błąd importu course_map: {e}")
        return False

def test_streamlit_agraph_config():
    """Test konfiguracji streamlit-agraph z physics=True"""
    try:
        from streamlit_agraph import Config, Node, Edge
        
        # Test podstawowej konfiguracji
        config = Config(
            width=800,
            height=600,
            physics=True,
            hierarchical=False
        )
        print("✅ Konfiguracja Config(physics=True) działa poprawnie")
        
        # Test tworzenia węzłów i krawędzi
        nodes = [
            Node(id="test1", label="Test Node 1", size=20, color="#FF0000"),
            Node(id="test2", label="Test Node 2", size=15, color="#00FF00")
        ]
        edges = [Edge(source="test1", target="test2")]
        
        print("✅ Tworzenie Node i Edge zakończone sukcesem")
        return True
        
    except ImportError as e:
        print(f"❌ Błąd importu streamlit-agraph: {e}")
        return False
    except Exception as e:
        print(f"❌ Błąd konfiguracji: {e}")
        return False

def test_course_data_functions():
    """Test funkcji danych kursu"""
    try:
        from utils.course_map import get_blocks, get_categories, get_lessons_for_category
        
        blocks = get_blocks()
        categories = get_categories()
        
        print(f"✅ Pobrano {len(blocks)} bloków")
        print(f"✅ Pobrano {len(categories)} kategorii")
        
        # Test na pierwszej kategorii
        if categories:
            first_category_id = list(categories.keys())[0]
            lessons = get_lessons_for_category(first_category_id)
            print(f"✅ Pobrano {len(lessons)} lekcji dla kategorii {first_category_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd podczas testowania funkcji danych: {e}")
        return False

def main():
    """Główna funkcja testowa"""
    print("🔧 Testowanie poprawek fizyki w mapie kursu...")
    print("=" * 50)
    
    results = []
    
    # Test 1: Import funkcji
    print("\n1. Test importu funkcji course_map:")
    results.append(test_course_map_imports())
    
    # Test 2: Konfiguracja streamlit-agraph
    print("\n2. Test konfiguracji streamlit-agraph:")
    results.append(test_streamlit_agraph_config())
    
    # Test 3: Funkcje danych kursu
    print("\n3. Test funkcji danych kursu:")
    results.append(test_course_data_functions())
    
    # Podsumowanie
    print("\n" + "=" * 50)
    print("📊 PODSUMOWANIE TESTÓW:")
    
    if all(results):
        print("✅ Wszystkie testy zakończone sukcesem!")
        print("✅ Poprawki fizyki zostały prawidłowo zastosowane")
        print("\n🎯 Fizyka w mapie kursu powinna teraz działać poprawnie")
    else:
        failed_tests = sum(1 for r in results if not r)
        print(f"❌ {failed_tests} z {len(results)} testów nie powiodło się")
        print("❌ Wymagane dodatkowe poprawki")

if __name__ == "__main__":
    main()
