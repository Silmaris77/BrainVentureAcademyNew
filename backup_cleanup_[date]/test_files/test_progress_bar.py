#!/usr/bin/env python3
"""
Test paska postępu lekcji - sprawdza czy dane XP i procenty są poprawnie obliczane
"""

def test_progress_calculation():
    """Test obliczania postępu i XP"""
    
    # Symulacja danych lekcji
    max_xp = 100
    
    # Nowy system procentowy
    step_xp_values = {
        'intro': int(max_xp * 0.05),          # 5% całkowitego XP
        'opening_quiz': int(max_xp * 0.00),   # 0% całkowitego XP
        'content': int(max_xp * 0.30),        # 30% całkowitego XP (Merytoryka)
        'reflection': int(max_xp * 0.20),     # 20% całkowitego XP
        'application': int(max_xp * 0.20),    # 20% całkowitego XP
        'closing_quiz': int(max_xp * 0.20),   # 20% całkowitego XP
        'summary': int(max_xp * 0.05)         # 5% całkowitego XP
    }
    
    # Przykładowa kolejność kroków
    step_order = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
    total_steps = len(step_order)
    
    # Symulacja postępu - 3 kroki ukończone
    lesson_progress = {
        'intro': True,
        'opening_quiz': True, 
        'content': True,
        'reflection': False,
        'application': False,
        'closing_quiz': False,
        'summary': False
    }
    
    # Oblicz postęp
    completed_steps = sum(1 for step in step_order if lesson_progress.get(step, False))
    completion_percent = (completed_steps / total_steps) * 100
    
    # Oblicz zdobyte XP
    current_xp = 0
    for step in step_order:
        if lesson_progress.get(step, False):
            current_xp += step_xp_values.get(step, 0)
    
    print("🧪 Test paska postępu lekcji")
    print("=" * 50)
    print(f"📊 Lekcja z {max_xp} XP")
    print(f"📈 Ukończone kroki: {completed_steps}/{total_steps}")
    print(f"📊 Procent ukończenia: {completion_percent:.1f}%")
    print(f"💎 Zdobyte XP: {current_xp}/{max_xp}")
    print()
    
    print("📋 Szczegóły kroków:")
    for step in step_order:
        completed = lesson_progress.get(step, False)
        xp = step_xp_values.get(step, 0)
        status = "✅" if completed else "⭕"
        print(f"  {status} {step}: {xp} XP")
    
    print()
    print("🎯 Sprawdzenia:")
    
    # Sprawdź czy suma XP się zgadza
    total_possible_xp = sum(step_xp_values.values())
    if total_possible_xp == max_xp:
        print(f"✅ Suma XP kroków = {total_possible_xp} (zgadza się z max_xp)")
    else:
        print(f"⚠️  Suma XP kroków = {total_possible_xp} (różni się od max_xp = {max_xp})")
    
    # Sprawdź logikę procentów
    expected_percent = (3 / 7) * 100  # 3 ukończone z 7 kroków
    if abs(completion_percent - expected_percent) < 0.1:
        print(f"✅ Procent ukończenia: {completion_percent:.1f}% (oczekiwane: {expected_percent:.1f}%)")
    else:
        print(f"⚠️  Procent ukończenia: {completion_percent:.1f}% (oczekiwane: {expected_percent:.1f}%)")
    
    # Sprawdź zdobyte XP
    expected_xp = step_xp_values['intro'] + step_xp_values['opening_quiz'] + step_xp_values['content']
    if current_xp == expected_xp:
        print(f"✅ Zdobyte XP: {current_xp} (oczekiwane: {expected_xp})")
    else:
        print(f"⚠️  Zdobyte XP: {current_xp} (oczekiwane: {expected_xp})")
    
    print("\n🎉 Test zakończony!")

if __name__ == "__main__":
    test_progress_calculation()
