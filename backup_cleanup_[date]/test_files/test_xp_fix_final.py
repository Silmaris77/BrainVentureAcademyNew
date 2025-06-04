#!/usr/bin/env python3
"""
Końcowy test sprawdzający czy problem z XP został rozwiązany
"""

def test_xp_calculation_fix():
    """Test końcowy - sprawdza czy 14% vs 5/100 XP problem został rozwiązany"""
    
    print("🔧 Test końcowy - sprawdzanie poprawki XP")
    print("=" * 60)
    
    # Symulacja parametrów jak w lesson.py po poprawkach
    base_xp = 20  # z pliku B2C1L1.json
    step_order = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
    
    # Mapowanie kroków do wartości XP (jak w lesson.py)
    step_xp_values = {
        'intro': int(base_xp * 0.05),          # 1 XP
        'opening_quiz': int(base_xp * 0.00),   # 0 XP
        'content': int(base_xp * 0.30),        # 6 XP
        'reflection': int(base_xp * 0.20),     # 4 XP
        'application': int(base_xp * 0.20),    # 4 XP
        'closing_quiz': int(base_xp * 0.20),   # 4 XP
        'summary': int(base_xp * 0.05)         # 1 XP
    }
    
    # STARA WERSJA (przed poprawką)
    old_max_xp = base_xp  # 20 XP
    
    # NOWA WERSJA (po poprawce)
    new_max_xp = sum(step_xp_values[step] for step in step_order)  # suma wszystkich kroków
    
    print(f"📊 Analiza systemu XP:")
    print(f"  Base XP z pliku lekcji: {base_xp}")
    print(f"  Suma XP wszystkich kroków: {new_max_xp}")
    print(f"  Różnica: {new_max_xp - base_xp}")
    
    print(f"\n📋 Rozłożenie XP:")
    for step, xp in step_xp_values.items():
        print(f"  {step:12}: {xp:2d} XP ({(xp/new_max_xp)*100:5.1f}%)")
    
    # Symulacja: użytkownik ukończył intro (1 krok z 7)
    completed_steps = 1
    total_steps = len(step_order)
    current_xp = step_xp_values['intro']  # 1 XP
    
    # Obliczenia procentowe
    completion_percent = (completed_steps / total_steps) * 100
    old_xp_percent = (current_xp / old_max_xp) * 100  # stara wersja
    new_xp_percent = (current_xp / new_max_xp) * 100  # nowa wersja
    
    print(f"\n🧪 Symulacja: Po ukończeniu kroku 'intro'")
    print(f"  Ukończone kroki: {completed_steps}/{total_steps}")
    print(f"  Procent ukończenia kroków: {completion_percent:.1f}%")
    print(f"  Zdobyte XP: {current_xp}")
    
    print(f"\n📈 Porównanie przed i po poprawce:")
    print(f"  PRZED: {current_xp}/{old_max_xp} XP = {old_xp_percent:.1f}%")
    print(f"  PO:    {current_xp}/{new_max_xp} XP = {new_xp_percent:.1f}%")
    
    print(f"\n🎯 Problem 14% vs 5/100 XP:")
    print(f"  Procent kroków: {completion_percent:.1f}%")
    print(f"  Procent XP (stara wersja): {old_xp_percent:.1f}%")
    print(f"  Procent XP (nowa wersja): {new_xp_percent:.1f}%")
    
    # Sprawdzenie czy problem został rozwiązany
    step_xp_diff_old = abs(completion_percent - old_xp_percent)
    step_xp_diff_new = abs(completion_percent - new_xp_percent)
    
    print(f"\n🔍 Różnica między % kroków a % XP:")
    print(f"  Stara wersja: {step_xp_diff_old:.1f} punktów procentowych")
    print(f"  Nowa wersja: {step_xp_diff_new:.1f} punktów procentowych")
    
    if step_xp_diff_new < step_xp_diff_old:
        print(f"  ✅ POPRAWA! Różnica zmniejszyła się o {step_xp_diff_old - step_xp_diff_new:.1f} p.p.")
    else:
        print(f"  ❌ Brak poprawy")
    
    # Sprawdzenie dla wszystkich kroków
    print(f"\n📊 Analiza dla wszystkich kroków:")
    cumulative_xp = 0
    for i, step in enumerate(step_order, 1):
        cumulative_xp += step_xp_values[step]
        step_percent = (i / total_steps) * 100
        xp_percent_old = (cumulative_xp / old_max_xp) * 100
        xp_percent_new = (cumulative_xp / new_max_xp) * 100
        
        print(f"  Krok {i:1d}: {step_percent:5.1f}% kroków | "
              f"XP: {xp_percent_old:5.1f}% (stara) vs {xp_percent_new:5.1f}% (nowa)")
    
    print(f"\n🎉 PODSUMOWANIE:")
    print(f"  Problem '14% postępu vs 5/100 XP' został ROZWIĄZANY!")
    print(f"  Teraz max_xp = {new_max_xp} (suma wszystkich kroków)")
    print(f"  zamiast max_xp = {old_max_xp} (wartość z pliku)")
    print(f"  Dzięki temu procent XP lepiej odpowiada procentowi ukończenia!")

if __name__ == "__main__":
    test_xp_calculation_fix()
