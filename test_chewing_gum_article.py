#!/usr/bin/env python3
"""
Test sprawdzający czy nowy artykuł 'Żucie_gumy_a_mózg.md' jest dostępny w systemie inspiracji
"""

import os
import sys
import json

# Dodaj ścieżkę do głównego katalogu aplikacji
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

def test_chewing_gum_article():
    """Test sprawdzający czy artykuł o żuciu gumy jest dostępny"""
    print("🧠 Testowanie dostępności artykułu o żuciu gumy...")
    
    # Test 1: Sprawdź czy plik Markdown istnieje
    md_file = os.path.join(app_dir, 'data', 'inspirations', 'facts', 'Żucie_gumy_a_mózg.md')
    if os.path.exists(md_file):
        print("✅ Plik Markdown istnieje")
        
        # Sprawdź zawartość pliku
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > 100:  # Sprawdź czy ma jakąś zawartość
            print(f"✅ Plik ma zawartość ({len(content)} znaków)")
        else:
            print("❌ Plik jest zbyt krótki")
            return False
    else:
        print("❌ Plik Markdown nie istnieje")
        return False
    
    # Test 2: Sprawdź czy wpis istnieje w JSON
    json_file = os.path.join(app_dir, 'data', 'inspirations', 'inspirations_data.json')
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Szukaj artykułu o żuciu gumy
        facts = data.get('facts', [])
        chewing_gum_fact = None
        
        for fact in facts:
            if fact.get('id') == 'chewing_gum_brain':
                chewing_gum_fact = fact
                break
        
        if chewing_gum_fact:
            print("✅ Wpis znaleziony w inspirations_data.json")
            print(f"   Tytuł: {chewing_gum_fact['title']}")
            print(f"   Ikona: {chewing_gum_fact['icon']}")
            print(f"   Źródło: {chewing_gum_fact['source']}")
            print(f"   Tagi: {', '.join(chewing_gum_fact['tags'])}")
        else:
            print("❌ Wpis nie znaleziony w JSON")
            return False
            
    except Exception as e:
        print(f"❌ Błąd przy czytaniu JSON: {e}")
        return False
    
    # Test 3: Sprawdź czy można załadować przez system
    try:
        from utils.inspirations_loader import get_facts, load_inspiration_content
        
        facts = get_facts()
        chewing_gum_loaded = None
        
        for fact in facts:
            if fact.get('id') == 'chewing_gum_brain':
                chewing_gum_loaded = fact
                break
        
        if chewing_gum_loaded:
            print("✅ Artykuł ładuje się przez system inspiracji")
            
            # Test załadowania treści
            content = load_inspiration_content(chewing_gum_loaded['file_path'])
            if "Bystrzak w mgnieniu oka" in content:
                print("✅ Treść artykułu ładuje się poprawnie")
            else:
                print("❌ Problem z ładowaniem treści")
                return False
        else:
            print("❌ Artykuł nie ładuje się przez system")
            return False
            
    except Exception as e:
        print(f"❌ Błąd przy testowaniu systemu: {e}")
        return False
    
    return True

def main():
    """Uruchom test"""
    print("🔬 TEST DOSTĘPNOŚCI ARTYKUŁU O ŻUCIU GUMY")
    print("=" * 50)
    
    if test_chewing_gum_article():
        print("\n🎉 SUKCES! Artykuł jest dostępny w aplikacji!")
        print("\n📋 Aby zobaczyć artykuł:")
        print("1. Uruchom aplikację")
        print("2. Przejdź do sekcji 'Inspiracje'")
        print("3. Wybierz zakładkę '🧠 Ciekawostki'")
        print("4. Znajdź artykuł 'Bystrzak w mgnieniu oka??? To proste!!!'")
        print("5. Kliknij 'Czytaj więcej' aby zobaczyć pełną treść")
    else:
        print("\n❌ BŁĄD! Artykuł nie jest dostępny. Sprawdź konfigurację.")
    
    return True

if __name__ == "__main__":
    main()
