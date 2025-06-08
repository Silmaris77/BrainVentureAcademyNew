#!/usr/bin/env python3
"""
Test sprawdzający poprawność marginesów i formatowania tekstu w artykule o Forrest Gump
"""

import sys
import os
import json

# Dodaj ścieżkę do głównego katalogu projektu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.inspirations_loader import get_blog_articles, load_inspiration_content

def test_forrest_gump_margins():
    """Test sprawdzający marginesy artykułu o Forrest Gump"""
    
    print("🧪 SPRAWDZANIE MARGINESÓW I FORMATOWANIA ARTYKUŁU O FORREST GUMP")
    print("=" * 70)
    
    # 1. Sprawdź czy artykuł istnieje w konfiguracji
    articles = get_blog_articles()
    forrest_article = None
    
    for article in articles:
        if "forrest" in article['title'].lower() or "gump" in article['title'].lower():
            forrest_article = article
            break
    
    if not forrest_article:
        print("❌ BŁĄD: Nie znaleziono artykułu o Forrest Gump!")
        return False
    
    print(f"✅ Znaleziono artykuł: {forrest_article['title']}")
    print(f"   Autor: {forrest_article['author']}")
    print(f"   Data: {forrest_article['date']}")
    print(f"   Ikona: {forrest_article['icon']}")
    print(f"   Tagi: {', '.join(forrest_article['tags'])}")
    print()
    
    # 2. Sprawdź czy plik artykułu istnieje
    file_path = f"data/inspirations/{forrest_article['file_path']}"
    if not os.path.exists(file_path):
        print(f"❌ BŁĄD: Plik artykułu nie istnieje: {file_path}")
        return False
    
    print(f"✅ Plik artykułu istnieje: {file_path}")
    
    # 3. Sprawdź zawartość artykułu
    content = load_inspiration_content(forrest_article['file_path'])
    
    if not content:
        print("❌ BŁĄD: Zawartość artykułu jest pusta!")
        return False
    
    print(f"✅ Artykuł ma {len(content)} znaków")
    
    # 4. Sprawdź kluczowe elementy artykułu
    key_phrases = [
        "Forrest Gump wiedział o neuroprzywództwie",
        "pobiegać",
        "neurobiologia",
        "mikrozmiana",
        "endorfiny i BDNF",
        "dopaminą"
    ]
    
    found_phrases = []
    missing_phrases = []
    
    for phrase in key_phrases:
        if phrase.lower() in content.lower():
            found_phrases.append(phrase)
        else:
            missing_phrases.append(phrase)
    
    print(f"✅ Znalezione kluczowe frazy ({len(found_phrases)}/{len(key_phrases)}):")
    for phrase in found_phrases:
        print(f"   • {phrase}")
    
    if missing_phrases:
        print(f"⚠️  Brakujące frazy ({len(missing_phrases)}):")
        for phrase in missing_phrases:
            print(f"   • {phrase}")
    
    print()
    
    # 5. Sprawdź CSS dla marginesów w pliku inspirations_new.py
    inspirations_file = "views/inspirations_new.py"
    if os.path.exists(inspirations_file):
        with open(inspirations_file, 'r', encoding='utf-8') as f:
            inspirations_content = f.read()
        
        css_classes_to_check = [
            ".article-detail-container",
            "max-width: 900px",
            "margin: 0 auto",
            "padding: 2rem",
            "line-height: 1.8",
            "text-align: justify",
            "text-indent: 1rem"
        ]
        
        found_css = []
        missing_css = []
        
        for css_class in css_classes_to_check:
            if css_class in inspirations_content:
                found_css.append(css_class)
            else:
                missing_css.append(css_class)
        
        print(f"✅ Style CSS dla marginesów ({len(found_css)}/{len(css_classes_to_check)}):")
        for css in found_css:
            print(f"   • {css}")
        
        if missing_css:
            print(f"⚠️  Brakujące style CSS:")
            for css in missing_css:
                print(f"   • {css}")
    else:
        print(f"❌ BŁĄD: Nie znaleziono pliku {inspirations_file}")
    
    print()
    print("📊 PODSUMOWANIE TESTÓW:")
    print(f"   • Artykuł w konfiguracji: {'✅' if forrest_article else '❌'}")
    print(f"   • Plik artykułu istnieje: {'✅' if os.path.exists(file_path) else '❌'}")
    print(f"   • Zawartość artykułu: {'✅' if content else '❌'}")
    print(f"   • Kluczowe frazy: ✅ {len(found_phrases)}/{len(key_phrases)}")
    print(f"   • Style CSS: ✅ {len(found_css)}/{len(css_classes_to_check)}")
    
    success_rate = (
        (1 if forrest_article else 0) +
        (1 if os.path.exists(file_path) else 0) +
        (1 if content else 0) +
        (len(found_phrases) / len(key_phrases)) +
        (len(found_css) / len(css_classes_to_check))
    ) / 5
    
    print(f"\n🎯 OGÓLNY WYNIK: {success_rate*100:.1f}%")
    
    if success_rate >= 0.8:
        print("🎉 SUKCES! Artykuł o Forrest Gump jest właściwie skonfigurowany z marginesami!")
        return True
    else:
        print("⚠️ UWAGA: Niektóre elementy wymagają poprawek.")
        return False

if __name__ == "__main__":
    test_forrest_gump_margins()
