#!/usr/bin/env python3
"""
Test sprawdzający działanie wyświetlania wyników testu neuroleadera w profilu
"""
print("🔍 Rozpoczynam test wyświetlania wyników neuroleadera...")

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from data.users import load_user_data
from data.test_questions import NEUROLEADER_TYPES

def test_neuroleader_display_logic():
    """Test logiki wyświetlania wyników testu neuroleadera"""
    
    print("=== TEST WYŚWIETLANIA WYNIKÓW TESTU NEUROLEADERA ===\n")
    
    # Załaduj dane użytkowników
    try:
        users_data = load_user_data()
        print("✅ Dane użytkowników załadowane pomyślnie")
    except Exception as e:
        print(f"❌ Błąd ładowania danych użytkowników: {e}")
        return False
    
    # Sprawdź użytkowników, którzy zrobili test
    users_with_test = []
    
    for username, user_data in users_data.items():
        neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type')
        test_taken = user_data.get('test_taken', False)
        has_test_scores = 'test_scores' in user_data
        
        print(f"\n--- Użytkownik: {username} ---")
        print(f"neuroleader_type: {neuroleader_type}")
        print(f"test_taken: {test_taken}")
        print(f"has_test_scores: {has_test_scores}")
        
        if neuroleader_type and (test_taken or has_test_scores):
            users_with_test.append(username)
            print(f"✅ {username} - ma wyniki testu - POWINIEN WIDZIEĆ WYNIKI")
            
            if has_test_scores:
                print(f"test_scores: {user_data['test_scores']}")
                
            # Sprawdź czy typ neuroleadera istnieje w definicjach
            if neuroleader_type in NEUROLEADER_TYPES:
                print(f"✅ Typ neuroleadera '{neuroleader_type}' istnieje w definicjach")
                type_info = NEUROLEADER_TYPES[neuroleader_type]
                print(f"   - Opis: {type_info.get('description', 'Brak opisu')}")
                print(f"   - Mocne strony: {len(type_info.get('strengths', []))} elementów")
                print(f"   - Wyzwania: {len(type_info.get('challenges', []))} elementów")
                print(f"   - Strategia: {'Tak' if type_info.get('strategy') else 'Brak'}")
            else:
                print(f"❌ Typ neuroleadera '{neuroleader_type}' NIE ISTNIEJE w definicjach")
        else:
            print(f"❌ {username} - nie ma wyników testu - POWINIEN WIDZIEĆ ZACHĘTĘ DO TESTU")
    
    print(f"\n=== PODSUMOWANIE ===")
    print(f"Użytkownicy z wynikami testu: {len(users_with_test)}")
    print(f"Lista: {users_with_test}")
    
    # Sprawdź dostępne typy neuroleaderów
    print(f"\nDostępne typy neuroleaderów:")
    for typ in NEUROLEADER_TYPES.keys():
        print(f"  - {typ}")
    
    return len(users_with_test) > 0

def test_import_functionality():
    """Test czy importy działają"""
    print("\n=== TEST IMPORTÓW ===")
    
    try:
        from data.neuroleader_details import degen_details
        print("✅ Import degen_details - OK")
        print(f"   Dostępne szczegóły dla typów: {list(degen_details.keys())}")
    except Exception as e:
        print(f"❌ Import degen_details - BŁĄD: {e}")
        return False
    
    try:
        from views.degen_test import plot_radar_chart
        print("✅ Import plot_radar_chart - OK")
    except Exception as e:
        print(f"❌ Import plot_radar_chart - BŁĄD: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Rozpoczynam testy...")
    
    success1 = test_import_functionality()
    success2 = test_neuroleader_display_logic()
    
    if success1 and success2:
        print("\n🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        print("Logika wyświetlania wyników testu neuroleadera powinna działać poprawnie.")
    else:
        print("\n❌ NIEKTÓRE TESTY NIE PRZESZŁY!")
        print("Sprawdź błędy powyżej.")
