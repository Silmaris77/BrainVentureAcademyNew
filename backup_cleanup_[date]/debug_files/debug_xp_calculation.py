#!/usr/bin/env python3
"""
Skrypt diagnostyczny dla systemu XP - sprawdzenie kalkulacji
"""

def debug_xp_calculation():
    """Debuguje kalkulację XP dla lekcji"""
    
    print("🔍 Debug XP calculation")
    print("=" * 50)
    
    # Symulacja wartości z lekcji
    max_xp_from_lesson = 20  # z pliku B2C1L1.json
    
    # Mapowanie kroków do wartości XP (jak w lesson.py)
    step_xp_values = {
        'intro': int(max_xp_from_lesson * 0.05),          # 5% całkowitego XP
        'opening_quiz': int(max_xp_from_lesson * 0.00),   # 0% całkowitego XP  
        'content': int(max_xp_from_lesson * 0.30),        # 30% całkowitego XP
        'reflection': int(max_xp_from_lesson * 0.20),     # 20% całkowitego XP
        'application': int(max_xp_from_lesson * 0.20),    # 20% całkowitego XP
        'closing_quiz': int(max_xp_from_lesson * 0.20),   # 20% całkowitego XP
        'summary': int(max_xp_from_lesson * 0.05)         # 5% całkowitego XP
    }
    
    print(f"Max XP z pliku lekcji: {max_xp_from_lesson}")
    print("\nRozpis XP dla każdego kroku:")
    total_calculated_xp = 0
    for step, xp in step_xp_values.items():
        print(f"  {step}: {xp} XP")
        total_calculated_xp += xp
    
    print(f"\nSuma wszystkich kroków: {total_calculated_xp} XP")
    print(f"Różnica: {max_xp_from_lesson - total_calculated_xp}")
    
    # Test dla postępu 1/7 kroków (14.3%)
    completed_steps = 1
    total_steps = 7
    completion_percent = (completed_steps / total_steps) * 100
    
    print(f"\nTest postępu:")
    print(f"Ukończone kroki: {completed_steps}/{total_steps}")
    print(f"Procent ukończenia: {completion_percent:.1f}%")
    
    # Sprawdzenie rzeczywistego XP za 1 krok (intro)
    current_xp = step_xp_values['intro']
    print(f"XP za intro: {current_xp}")
    print(f"Wyświetlane: {current_xp}/{max_xp_from_lesson} XP")
    
    print("\n🔍 Problem:")
    print(f"UI pokazuje: 14% postępu ale {current_xp}/{max_xp_from_lesson} XP")
    print(f"To jest niezgodne bo {current_xp}/{max_xp_from_lesson} = {(current_xp/max_xp_from_lesson)*100:.1f}%")
    
    print("\n💡 Rozwiązanie:")
    print(f"Zamiast max_xp = {max_xp_from_lesson}, użyj max_xp = {total_calculated_xp}")
    print(f"Wtedy {current_xp}/{total_calculated_xp} = {(current_xp/total_calculated_xp)*100:.1f}% (blisko 14%)")

if __name__ == "__main__":
    debug_xp_calculation()
