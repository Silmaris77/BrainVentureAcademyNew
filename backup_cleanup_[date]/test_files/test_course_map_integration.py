#!/usr/bin/env python3
"""
Test integracji mapy kursu z aplikacją BrainVenture Academy
"""
import sys
import os

# Dodaj ścieżkę do katalogu głównego
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testuje czy wszystkie moduły można zaimportować"""
    try:
        # Test importu podstawowych modułów
        from utils.course_map import create_course_structure_map, create_simplified_course_map, show_course_statistics
        print("✅ Moduł course_map zaimportowany pomyślnie")
        
        # Test importu streamlit-agraph
        from streamlit_agraph import agraph, Node, Edge, Config
        print("✅ streamlit-agraph zaimportowany pomyślnie")
        
        # Test importu danych kursu
        from data.course_data import get_blocks, get_categories, get_lessons_for_category
        print("✅ Moduły course_data zaimportowane pomyślnie")
        
        # Test importu views
        from views.skills_new import show_skill_tree
        print("✅ Moduł skills_new zaimportowany pomyślnie")
        
        return True
        
    except ImportError as e:
        print(f"❌ Błąd importu: {e}")
        return False

def test_data_structure():
    """Testuje strukturę danych kursu"""
    try:
        from data.course_data import get_blocks, get_categories, get_lessons_for_category
        
        blocks = get_blocks()
        categories = get_categories()
        
        print(f"✅ Znaleziono {len(blocks)} bloków/modułów")
        print(f"✅ Znaleziono {len(categories)} kategorii")
        
        # Test kilku kategorii
        lessons_count = 0
        for cat_id in list(categories.keys())[:3]:  # Test pierwszych 3 kategorii
            lessons = get_lessons_for_category(cat_id)
            lessons_count += len(lessons)
            print(f"✅ Kategoria {cat_id}: {len(lessons)} lekcji")
        
        print(f"✅ Przykładowa liczba lekcji: {lessons_count}")
        return True
        
    except Exception as e:
        print(f"❌ Błąd struktury danych: {e}")
        return False

def test_course_map_functions():
    """Testuje funkcje mapy kursu"""
    try:
        from utils.course_map import create_course_structure_map, create_simplified_course_map, show_course_statistics
        
        # Nie możemy uruchomić funkcji streamlit bez kontekstu, ale możemy sprawdzić czy się definiują
        print("✅ Funkcja create_course_structure_map jest dostępna")
        print("✅ Funkcja create_simplified_course_map jest dostępna") 
        print("✅ Funkcja show_course_statistics jest dostępna")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd funkcji mapy kursu: {e}")
        return False

def main():
    """Główna funkcja testowa"""
    print("🧪 Test integracji mapy kursu BrainVenture Academy")
    print("="*50)
    
    tests = [
        ("Import modułów", test_imports),
        ("Struktura danych", test_data_structure), 
        ("Funkcje mapy kursu", test_course_map_functions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - ZALICZONY")
        else:
            print(f"❌ {test_name} - NIEZALICZONY")
    
    print("\n" + "="*50)
    print(f"📊 Wyniki: {passed}/{total} testów zaliczonych ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 Wszystkie testy zaliczone! Integracja mapy kursu gotowa.")
        return True
    else:
        print("⚠️  Niektóre testy nie przeszły. Sprawdź błędy powyżej.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
