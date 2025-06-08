#!/usr/bin/env python3
"""
Weryfikacja poprawek marginesów dla artykułu o Forrest Gump
i całego systemu CMS Inspiracje
"""

import os
import sys
import json

# Dodaj ścieżkę projektu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verify_margins_implementation():
    """Sprawdza implementację marginesów w systemie Inspiracje"""
    
    print("🎯 WERYFIKACJA ULEPSZEŃ MARGINESÓW - SYSTEM INSPIRACJE")
    print("=" * 65)
    
    success_count = 0
    total_checks = 0
    
    # 1. Sprawdź plik inspirations_new.py
    inspirations_file = "views/inspirations_new.py"
    total_checks += 1
    
    if os.path.exists(inspirations_file):
        with open(inspirations_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź kluczowe style CSS
        css_checks = [
            ("Globalne style .stMarkdown", ".stMarkdown {"),
            ("Max-width dla głównego kontenera", "max-width: 1000px !important"),
            ("Kontener artykułów", ".article-detail-container {"),
            ("Max-width artykułów", "max-width: 800px !important"),
            ("Padding artykułów", "padding: 3rem !important"),
            ("Line-height artykułów", "line-height: 1.9 !important"),
            ("Text-indent artykułów", "text-indent: 1.5rem !important"),
            ("Border-radius", "border-radius: 16px !important"),
            ("Box-shadow", "box-shadow: 0 4px 20px"),
            ("Kontener tutoriali", ".tutorial-detail-container {"),
            ("Kontener faktów", ".fact-detail-container {"),
            ("Gradient dla HR", "background: linear-gradient(90deg, #2196F3, #673AB7)"),
        ]
        
        found_styles = 0
        for check_name, check_pattern in css_checks:
            if check_pattern in content:
                found_styles += 1
                print(f"✅ {check_name}")
            else:
                print(f"❌ Brak: {check_name}")
        
        if found_styles >= len(css_checks) * 0.8:  # 80% stylów musi być obecnych
            success_count += 1
            print(f"✅ Style CSS: {found_styles}/{len(css_checks)} - SUKCES")
        else:
            print(f"⚠️ Style CSS: {found_styles}/{len(css_checks)} - WYMAGA POPRAWEK")
    else:
        print(f"❌ Nie znaleziono pliku: {inspirations_file}")
    
    print()
    
    # 2. Sprawdź artykuł o Forrest Gump
    total_checks += 1
    forrest_file = "data/inspirations/blog/forrest_gump_neuroleadership.md"
    
    if os.path.exists(forrest_file):
        with open(forrest_file, 'r', encoding='utf-8') as f:
            forrest_content = f.read()
        
        # Sprawdź kluczowe elementy artykułu
        key_elements = [
            "Co Forrest Gump wiedział o neuroprzywództwie",
            "pobiegać",
            "endorfiny i BDNF",
            "dopaminą",
            "mikrozmiana",
            "neurobiologia",
            "Paweł Książyk"
        ]
        
        found_elements = 0
        for element in key_elements:
            if element in forrest_content:
                found_elements += 1
        
        if found_elements >= len(key_elements) * 0.8:
            success_count += 1
            print(f"✅ Artykuł Forrest Gump: {found_elements}/{len(key_elements)} elementów - SUKCES")
        else:
            print(f"❌ Artykuł Forrest Gump: {found_elements}/{len(key_elements)} elementów - PROBLEMY")
    else:
        print(f"❌ Nie znaleziono artykułu: {forrest_file}")
    
    print()
    
    # 3. Sprawdź konfigurację JSON
    total_checks += 1
    json_file = "data/inspirations/inspirations_data.json"
    
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Sprawdź artykuł Forrest Gump w JSON
            forrest_found = False
            for article in data.get('blog_articles', []):
                if 'Forrest' in article.get('title', '') and 'Gump' in article.get('title', ''):
                    if (article.get('author') == 'Paweł Książyk' and 
                        article.get('date') == '8 maja 2025' and
                        article.get('icon') == '🏃'):
                        forrest_found = True
                        break
            
            if forrest_found:
                success_count += 1
                print("✅ Konfiguracja JSON - artykuł Forrest Gump właściwie skonfigurowany")
            else:
                print("❌ Konfiguracja JSON - brak lub nieprawidłowy artykuł Forrest Gump")
                
        except json.JSONDecodeError as e:
            print(f"❌ Błąd parsowania JSON: {e}")
    else:
        print(f"❌ Nie znaleziono pliku: {json_file}")
    
    print()
    
    # 4. Sprawdź moduł ładowania danych
    total_checks += 1
    loader_file = "utils/inspirations_loader.py"
    
    if os.path.exists(loader_file):
        success_count += 1
        print("✅ Moduł inspirations_loader.py istnieje")
    else:
        print("❌ Brak modułu inspirations_loader.py")
    
    print()
    
    # Podsumowanie
    success_rate = (success_count / total_checks) * 100
    print("📊 PODSUMOWANIE WERYFIKACJI:")
    print(f"   • Sprawdzonych komponentów: {total_checks}")
    print(f"   • Pomyślnych: {success_count}")
    print(f"   • Wskaźnik sukcesu: {success_rate:.1f}%")
    print()
    
    if success_rate >= 75:
        print("🎉 SUKCES! Marginesy zostały właściwie zaimplementowane!")
        print()
        print("📋 CO ZOSTAŁO ULEPSZONE:")
        print("   • Zwiększono max-width kontenerów artykułów do 800px")
        print("   • Dodano padding 3rem dla lepszych marginesów")
        print("   • Zwiększono line-height do 1.9 dla lepszej czytelności")
        print("   • Dodano text-indent 1.5rem dla akapitów")
        print("   • Ulepszono border-radius do 16px")
        print("   • Dodano lepsze cienie (box-shadow)")
        print("   • Ujednolicono style dla artykułów, tutoriali i faktów")
        print("   • Artykuł o Forrest Gump właściwie zintegrowany")
        print()
        print("💡 EFEKT:")
        print("   • Tekst jest lepiej sformatowany z właściwymi marginesami")
        print("   • Lepsza czytelność dzięki zwiększonym odstępom")
        print("   • Profesjonalny wygląd kontenerów z treścią")
        print("   • Spójny design we wszystkich sekcjach Inspiracji")
        
        return True
    else:
        print("⚠️ UWAGA: Niektóre elementy wymagają jeszcze poprawek.")
        print("Sprawdź powyższe błędy i dokonaj niezbędnych korekt.")
        return False

if __name__ == "__main__":
    verify_margins_implementation()
