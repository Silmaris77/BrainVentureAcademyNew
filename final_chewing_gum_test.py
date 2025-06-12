#!/usr/bin/env python3
"""
Końcowy test weryfikujący pełną integrację artykułu o żuciu gumy
"""

import os
import sys
import json

# Dodaj ścieżkę do głównego katalogu aplikacji
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

def test_article_integration():
    """Test pełnej integracji artykułu o żuciu gumy"""
    print("🧠 KOŃCOWY TEST INTEGRACJI ARTYKUŁU O ŻUCIU GUMY")
    print("=" * 60)
    
    success_count = 0
    total_tests = 6
    
    # Test 1: Sprawdź plik Markdown
    print("\n1️⃣ Test istnienia pliku Markdown...")
    md_path = os.path.join('data', 'inspirations', 'facts', 'Żucie_gumy_a_mózg.md')
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content) > 100 and "Bystrzak w mgnieniu oka" in content:
            print("✅ Plik Markdown istnieje i ma poprawną treść")
            success_count += 1
        else:
            print("❌ Plik Markdown ma niepoprawną treść")
    else:
        print("❌ Plik Markdown nie istnieje")
    
    # Test 2: Sprawdź wpis w JSON
    print("\n2️⃣ Test wpisu w pliku konfiguracyjnym...")
    try:
        with open('data/inspirations/inspirations_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        facts = data.get('facts', [])
        gum_fact = next((f for f in facts if f.get('id') == 'chewing_gum_brain'), None)
        
        if gum_fact:
            required_fields = ['id', 'title', 'content', 'source', 'icon', 'tags', 'file_path']
            if all(field in gum_fact for field in required_fields):
                print("✅ Wpis w JSON zawiera wszystkie wymagane pola")
                success_count += 1
            else:
                print("❌ Wpis w JSON nie zawiera wszystkich wymaganych pól")
        else:
            print("❌ Wpis nie znaleziony w JSON")
    except Exception as e:
        print(f"❌ Błąd przy czytaniu JSON: {e}")
    
    # Test 3: Test systemu ładowania
    print("\n3️⃣ Test systemu ładowania danych...")
    try:
        from utils.inspirations_loader import get_facts
        facts = get_facts()
        
        gum_fact = next((f for f in facts if f.get('id') == 'chewing_gum_brain'), None)
        if gum_fact:
            print("✅ Artykuł ładuje się przez system inspiracji")
            success_count += 1
        else:
            print("❌ Artykuł nie ładuje się przez system")
    except Exception as e:
        print(f"❌ Błąd w systemie ładowania: {e}")
    
    # Test 4: Test ładowania treści
    print("\n4️⃣ Test ładowania treści artykułu...")
    try:
        from utils.inspirations_loader import load_inspiration_content
        content = load_inspiration_content('facts/Żucie_gumy_a_mózg.md')
        
        if "Bystrzak w mgnieniu oka" in content and "Serge Onyper" in content:
            print("✅ Treść artykułu ładuje się poprawnie")
            success_count += 1
        else:
            print("❌ Problem z ładowaniem treści artykułu")
    except Exception as e:
        print(f"❌ Błąd przy ładowaniu treści: {e}")
    
    # Test 5: Test konfiguracji aplikacji
    print("\n5️⃣ Test konfiguracji aplikacji...")
    try:
        from config.settings import FEATURE_FLAGS
        if FEATURE_FLAGS.get('USE_NEW_INSPIRATIONS', False):
            print("✅ Aplikacja używa nowego systemu inspiracji")
            success_count += 1
        else:
            print("❌ Aplikacja nie używa nowego systemu inspiracji")
    except Exception as e:
        print(f"❌ Błąd przy sprawdzaniu konfiguracji: {e}")
    
    # Test 6: Test importu widoku
    print("\n6️⃣ Test importu widoku inspiracji...")
    try:
        from views.inspirations_new import show_inspirations
        print("✅ Widok inspiracji_new importuje się poprawnie")
        success_count += 1
    except Exception as e:
        print(f"❌ Błąd przy imporcie widoku: {e}")
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print(f"🎯 WYNIKI TESTÓW: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        print("\n📋 Artykuł jest gotowy do użycia:")
        print("   1. Uruchom aplikację: streamlit run main.py")
        print("   2. Przejdź do: Inspiracje → 🧠 Ciekawostki")
        print("   3. Znajdź: 'Bystrzak w mgnieniu oka??? To proste!!!'")
        print("   4. Kliknij: 'Czytaj więcej'")
        return True
    else:
        print("⚠️  Niektóre testy nie przeszły. Sprawdź konfigurację.")
        return False

if __name__ == "__main__":
    test_article_integration()
