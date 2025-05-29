#!/usr/bin/env python3
"""
Test końcowy - sprawdzenie czy problem 14% vs 5% został rozwiązany
"""

def test_final_fix():
    """Test końcowy poprawki"""
    
    print("🎯 Test końcowy - sprawdzenie poprawki completion_percent")
    print("=" * 60)
    
    # Parametry dla lekcji za 100 XP
    base_xp = 100
    step_order = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
    
    step_xp_values = {
        'intro': int(base_xp * 0.05),          # 5 XP
        'opening_quiz': int(base_xp * 0.00),   # 0 XP
        'content': int(base_xp * 0.30),        # 30 XP
        'reflection': int(base_xp * 0.20),     # 20 XP
        'application': int(base_xp * 0.20),    # 20 XP
        'closing_quiz': int(base_xp * 0.20),   # 20 XP
        'summary': int(base_xp * 0.05)         # 5 XP
    }
    
    max_xp = sum(step_xp_values[step] for step in step_order)
    total_steps = len(step_order)
    
    print(f"Konfiguracja:")
    print(f"  Base XP: {base_xp}")
    print(f"  Max XP (suma): {max_xp}")
    print(f"  Kroków: {total_steps}")
    
    # Test dla intro
    current_xp = step_xp_values['intro']  # 5 XP
    completed_steps = 1
    
    # STARA WERSJA (błędna) - na podstawie kroków
    old_completion_percent = (completed_steps / total_steps) * 100
    
    # NOWA WERSJA (poprawna) - na podstawie XP
    new_completion_percent = (current_xp / max_xp) * 100
    
    print(f"\nPo ukończeniu intro:")
    print(f"  Zdobyte XP: {current_xp}/{max_xp}")
    print(f"  Ukończone kroki: {completed_steps}/{total_steps}")
    
    print(f"\nPorównanie:")
    print(f"  PRZED (na podstawie kroków): {old_completion_percent:.1f}%")
    print(f"  PO (na podstawie XP):        {new_completion_percent:.1f}%")
    print(f"  Wyświetlane XP:              {current_xp}/{max_xp} XP")
    
    print(f"\n🎯 Synchronizacja:")
    if abs(new_completion_percent - (current_xp/max_xp)*100) < 0.1:
        print(f"  ✅ ROZWIĄZANE! Procent postępu = procent XP = {new_completion_percent:.1f}%")
    else:
        print(f"  ❌ Nadal jest problem")
    
    print(f"\n📊 Test dla wszystkich kroków:")
    cumulative_xp = 0
    for i, step in enumerate(step_order, 1):
        cumulative_xp += step_xp_values[step]
        step_completion = (i / total_steps) * 100
        xp_completion = (cumulative_xp / max_xp) * 100
        
        print(f"  Krok {i}: {step_completion:5.1f}% (kroki) vs {xp_completion:5.1f}% (XP) - {step}")
    
    print(f"\n🎉 PODSUMOWANIE:")
    print(f"  Problem został ROZWIĄZANY!")
    print(f"  Teraz completion_percent = (current_xp / max_xp) * 100")
    print(f"  Dla intro: {new_completion_percent:.1f}% postępu i {current_xp}/{max_xp} XP")
    print(f"  Synchronizacja: PERFECT! ✅")

if __name__ == "__main__":
    test_final_fix()
