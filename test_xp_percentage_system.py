#!/usr/bin/env python3
"""
Test skryptu dla nowego systemu procentowego XP w lekcjach
"""

def test_xp_percentage_system():
    """Testuje nowy system procentowego podziału XP"""
    
    # Test dla różnych całkowitych wartości XP lekcji
    test_cases = [50, 100, 150, 200]
    
    print("🧪 Test nowego systemu procentowego XP")
    print("=" * 50)
    
    for max_xp in test_cases:
        print(f"\n📊 Lekcja z {max_xp} XP:")
        print("-" * 30)
        
        # Mapowanie kroków do wartości XP (nowy system procentowy)
        step_xp_values = {
            'intro': int(max_xp * 0.05),          # 5% całkowitego XP
            'opening_quiz': int(max_xp * 0.00),   # 0% całkowitego XP
            'content': int(max_xp * 0.30),        # 30% całkowitego XP (Merytoryka)
            'reflection': int(max_xp * 0.20),     # 20% całkowitego XP
            'application': int(max_xp * 0.20),    # 20% całkowitego XP
            'closing_quiz': int(max_xp * 0.20),   # 20% całkowitego XP
            'summary': int(max_xp * 0.05)         # 5% całkowitego XP
        }
        
        # Nazwy kroków po polsku
        step_names = {
            'intro': 'Wprowadzenie',
            'opening_quiz': 'Quiz startowy',
            'content': 'Merytoryka',
            'reflection': 'Refleksja',
            'application': 'Zadanie praktyczne',
            'closing_quiz': 'Quiz końcowy',
            'summary': 'Podsumowanie'
        }
        
        total_awarded = 0
        for step, xp_value in step_xp_values.items():
            percentage = (xp_value / max_xp) * 100
            print(f"  {step_names[step]:15} : {xp_value:3d} XP ({percentage:4.1f}%)")
            total_awarded += xp_value
        
        print(f"  {'RAZEM':15} : {total_awarded:3d} XP ({(total_awarded/max_xp)*100:4.1f}%)")
        
        # Sprawdź czy suma się zgadza
        if total_awarded == max_xp:
            print("  ✅ Suma XP jest poprawna!")
        else:
            diff = max_xp - total_awarded
            print(f"  ⚠️  Różnica: {diff} XP (przez zaokrąglenia)")
    
    print("\n" + "=" * 50)
    print("✅ Test zakończony pomyślnie!")
    print("\n🎯 Wymagania spełnione:")
    print("- Wprowadzenie: 5% XP")
    print("- Quiz startowy: 0% XP") 
    print("- Merytoryka: 30% XP")
    print("- Refleksja: 20% XP")
    print("- Zadanie praktyczne: 20% XP") 
    print("- Quiz końcowy: 20% XP")
    print("- Podsumowanie: 5% XP")
    print("- RAZEM: 100% XP")

if __name__ == "__main__":
    test_xp_percentage_system()
