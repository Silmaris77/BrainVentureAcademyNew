#!/usr/bin/env python3
"""
Szybki test modułu course_map
"""
import sys
import os

# Dodaj ścieżkę do katalogu głównego
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Test importu course_map...")
    from utils.course_map import create_course_structure_map, create_simplified_course_map, show_course_statistics
    print("✅ Import course_map pomyślny")
    
    print("Test importu streamlit_agraph...")
    from streamlit_agraph import agraph, Node, Edge, Config
    print("✅ Import streamlit_agraph pomyślny")
    
    print("Test importu course_data...")
    from data.course_data import get_blocks, get_categories, get_lessons_for_category
    print("✅ Import course_data pomyślny")
    
    print("Test danych...")
    blocks = get_blocks()
    categories = get_categories()
    print(f"✅ Znaleziono {len(blocks)} bloków i {len(categories)} kategorii")
    
    print("🎉 Wszystkie testy podstawowe przeszły pomyślnie!")
    
except Exception as e:
    print(f"❌ Błąd: {e}")
    import traceback
    traceback.print_exc()
