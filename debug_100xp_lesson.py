#!/usr/bin/env python3
"""
Debug dla lekcji za 100 XP - sprawdzenie rzeczywistych wartości
"""

def debug_100xp_lesson():
    """Debuguje problem z lekcją za 100 XP"""
    
    print("🔍 Debug lekcji za 100 XP")
    print("=" * 50)
    
    # Parametry dla lekcji za 100 XP
    base_xp = 100  # z pliku B1C1L1.json
    step_order = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
    
    # Mapowanie kroków do wartości XP (jak w lesson.py)
    step_xp_values = {
        'intro': int(base_xp * 0.05),          # 5% = 5 XP
        'opening_quiz': int(base_xp * 0.00),   # 0% = 0 XP
        'content': int(base_xp * 0.30),        # 30% = 30 XP
        'reflection': int(base_xp * 0.20),     # 20% = 20 XP
        'application': int(base_xp * 0.20),    # 20% = 20 XP
        'closing_quiz': int(base_xp * 0.20),   # 20% = 20 XP
        'summary': int(base_xp * 0.05)         # 5% = 5 XP
    }
    
    # Oblicz rzeczywiste maksimum XP (jak w kodzie po poprawce)
    max_xp = sum(step_xp_values[step] for step in step_order)
    total_steps = len(step_order)
    
    print(f"Base XP z pliku: {base_xp}")
    print(f"Obliczone max XP: {max_xp}")
    print(f"Kroków ogółem: {total_steps}")
    
    print(f"\nRozłożenie XP:")
    for step, xp in step_xp_values.items():
        print(f"  {step:12}: {xp:2d} XP")
    
    # Po ukończeniu intro
    completed_steps = 1
    current_xp = step_xp_values['intro']  # 5 XP
    
    completion_percent = (completed_steps / total_steps) * 100
    xp_percent = (current_xp / max_xp) * 100
    
    print(f"\nPo ukończeniu intro:")
    print(f"  Ukończone kroki: {completed_steps}/{total_steps}")
    print(f"  Procent ukończenia kroków: {completion_percent:.1f}%")
    print(f"  Zdobyte XP: {current_xp}/{max_xp}")
    print(f"  Procent XP: {xp_percent:.1f}%")
    
    print(f"\n🔍 Problem:")
    print(f"  UI pokazuje: {completion_percent:.0f}% postępu")
    print(f"  Ale XP to: {current_xp}/{max_xp} = {xp_percent:.1f}%")
    print(f"  OCZEKIWANE: {current_xp}/{base_xp} = {(current_xp/base_xp)*100:.1f}%")
    
    print(f"\n💡 Diagnoza:")
    if max_xp == base_xp:
        print(f"  ✅ max_xp = base_xp = {base_xp}")
        print(f"  Problem powinien być rozwiązany!")
    else:
        print(f"  ❌ max_xp ({max_xp}) ≠ base_xp ({base_xp})")
        print(f"  Różnica: {max_xp - base_xp}")
        print(f"  To przez zaokrąglenia int()!")
        
    print(f"\n🔧 Rozwiązanie:")
    print(f"  Zamiast sum kroków, użyj base_xp jako max_xp")
    print(f"  Lub dostosuj step_xp_values aby suma = base_xp")

if __name__ == "__main__":
    debug_100xp_lesson()
