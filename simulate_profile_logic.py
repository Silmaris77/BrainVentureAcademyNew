#!/usr/bin/env python3
"""
Test symulujący działanie wyświetlania wyników testu neuroleadera w profilu
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.users import load_user_data
from data.test_questions import NEUROLEADER_TYPES
from data.neuroleader_details import degen_details

def simulate_profile_tab4_logic(username="a"):
    """Symuluje logikę Tab 4 w profilu użytkownika"""
    
    print(f"🔍 SYMULACJA WYŚWIETLANIA PROFILU NEUROLEADERA DLA UŻYTKOWNIKA: {username}")
    print("=" * 80)
    
    # Załaduj dane użytkownika (jak w profile.py)
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    print(f"📊 Dane użytkownika '{username}':")
    print(f"   neuroleader_type: {user_data.get('neuroleader_type')}")
    print(f"   degen_type: {user_data.get('degen_type')}")
    print(f"   test_taken: {user_data.get('test_taken', False)}")
    print(f"   has_test_scores: {'test_scores' in user_data}")
    
    # Logika warunkowa z profile.py
    neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type')
    test_taken = user_data.get('test_taken', False)
    has_test_scores = 'test_scores' in user_data
    
    print(f"\n🧮 Logika warunkowa:")
    print(f"   neuroleader_type: {neuroleader_type}")
    print(f"   test_taken: {test_taken}")
    print(f"   has_test_scores: {has_test_scores}")
    print(f"   Warunek: neuroleader_type and (test_taken or has_test_scores)")
    print(f"   Wynik: {neuroleader_type and (test_taken or has_test_scores)}")
    
    if neuroleader_type and (test_taken or has_test_scores):
        print(f"\n✅ UŻYTKOWNIK POWINIEN WIDZIEĆ WYNIKI TESTU")
        print("-" * 50)
        
        # Sprawdź czy typ istnieje w definicjach
        if neuroleader_type in NEUROLEADER_TYPES:
            type_info = NEUROLEADER_TYPES[neuroleader_type]
            color = type_info.get('color', '#3498db')
            
            print(f"📋 WYŚWIETLANE INFORMACJE:")
            print(f"   🧬 Typ neuroleadera: {neuroleader_type}")
            print(f"   🎨 Kolor: {color}")
            print(f"   📝 Opis: {type_info.get('description', 'Brak opisu')}")
            
            # Mocne strony
            strengths = type_info.get('strengths', [])
            print(f"\n   💪 Mocne strony ({len(strengths)}):")
            for strength in strengths:
                print(f"      - ✅ {strength}")
            
            # Wyzwania
            challenges = type_info.get('challenges', [])
            print(f"\n   🚧 Obszary do rozwoju ({len(challenges)}):")
            for challenge in challenges:
                print(f"      - ⚠️ {challenge}")
            
            # Strategia
            strategy = type_info.get('strategy', '')
            if strategy:
                print(f"\n   🎯 Rekomendowana strategia:")
                print(f"      {strategy}")
            
            # Wykres radarowy
            if has_test_scores:
                test_scores = user_data['test_scores']
                print(f"\n   📊 Dane do wykresu radarowego:")
                for typ, score in test_scores.items():
                    print(f"      {typ}: {score}")
            
            # Szczegółowy opis
            if neuroleader_type in degen_details:
                detail_text = degen_details[neuroleader_type]
                print(f"\n   📚 Szczegółowy opis dostępny (długość: {len(detail_text)} znaków)")
            else:
                print(f"\n   📚 Szczegółowy opis: NIEDOSTĘPNY")
            
        else:
            print(f"❌ BŁĄD: Typ '{neuroleader_type}' nie istnieje w NEUROLEADER_TYPES")
            
    else:
        print(f"\n❌ UŻYTKOWNIK POWINIEN WIDZIEĆ ZACHĘTĘ DO ZROBIENIA TESTU")
        print("-" * 50)
        print(f"   Wyświetlana będzie zachęta do wykonania testu neuroleadera")
    
    return neuroleader_type and (test_taken or has_test_scores)

def test_all_users():
    """Test dla wszystkich użytkowników"""
    print(f"\n🔍 TEST DLA WSZYSTKICH UŻYTKOWNIKÓW")
    print("=" * 80)
    
    users_data = load_user_data()
    users_with_results = []
    
    for username in users_data.keys():
        print(f"\n--- TEST DLA UŻYTKOWNIKA: {username} ---")
        has_results = simulate_profile_tab4_logic(username)
        if has_results:
            users_with_results.append(username)
    
    print(f"\n📊 PODSUMOWANIE:")
    print(f"   Użytkownicy z wynikami testu: {len(users_with_results)}")
    print(f"   Lista: {users_with_results}")

if __name__ == "__main__":
    print("🧠 SYMULACJA DZIAŁANIA PROFILU NEUROLEADERA")
    print("Testuje logikę wyświetlania wyników testu w Tab 4 profilu użytkownika\n")
    
    # Test głównego użytkownika 'a'
    simulate_profile_tab4_logic("a")
    
    # Test wszystkich użytkowników
    test_all_users()
    
    print(f"\n🎉 Test zakończony! Sprawdź wyniki powyżej.")
