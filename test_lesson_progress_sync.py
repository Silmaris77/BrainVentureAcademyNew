#!/usr/bin/env python3
"""
Test synchronizacji postępu lekcji po wprowadzonych poprawkach
"""

def test_lesson_progress_sync():
    """Testuje synchronizację postępu lekcji"""
    
    print("🧪 Test synchronizacji postępu lekcji")
    print("=" * 50)
    
    try:
        # Import potrzebnych funkcji
        from utils.lesson_progress import (
            award_fragment_xp, 
            get_lesson_fragment_progress
        )
        from data.users import load_user_data, save_user_data
        import streamlit as st
        
        # Symulacja użytkownika
        test_user = "test_progress_user"
        lesson_id = "B2C1L1"
        
        # Wczyść dane użytkownika
        users_data = load_user_data()
        if test_user in users_data:
            # Reset danych lekcji dla czystego testu
            if 'lesson_progress' in users_data[test_user]:
                if lesson_id in users_data[test_user]['lesson_progress']:
                    del users_data[test_user]['lesson_progress'][lesson_id]
        else:
            users_data[test_user] = {'xp': 0, 'lesson_progress': {}}
        
        save_user_data(users_data)
        
        # Symulacja session_state
        class MockSessionState:
            def __init__(self):
                self.username = test_user
        
        st.session_state = MockSessionState()
        
        print(f"📝 Testowy użytkownik: {test_user}")
        print(f"📚 Testowa lekcja: {lesson_id}")
        
        # Parametry lekcji (jak w lesson.py po poprawkach)
        base_xp = 20  # z pliku B2C1L1.json
        step_order = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
        
        step_xp_values = {
            'intro': int(base_xp * 0.05),          # 1 XP
            'opening_quiz': int(base_xp * 0.00),   # 0 XP
            'content': int(base_xp * 0.30),        # 6 XP
            'reflection': int(base_xp * 0.20),     # 4 XP
            'application': int(base_xp * 0.20),    # 4 XP
            'closing_quiz': int(base_xp * 0.20),   # 4 XP
            'summary': int(base_xp * 0.05)         # 1 XP
        }
        
        # Oblicz rzeczywiste maksimum XP (jak w poprawce)
        max_xp = sum(step_xp_values[step] for step in step_order)
        total_steps = len(step_order)
        
        print(f"\nKonfiguracja XP:")
        print(f"  Base XP z pliku: {base_xp}")
        print(f"  Obliczone max XP: {max_xp}")
        print(f"  Kroki: {step_order}")
        print(f"  XP za kroki: {step_xp_values}")
        
        # Test: Ukończ pierwszy krok (intro)
        print(f"\n🎯 Test 1: Ukończenie kroku 'intro'")
        success, xp_awarded = award_fragment_xp(lesson_id, 'intro', step_xp_values['intro'])
        
        if success:
            print(f"  ✅ Przyznano {xp_awarded} XP za intro")
        else:
            print(f"  ❌ Błąd przy przyznawaniu XP: {success}")
        
        # Pobierz postęp
        fragment_progress = get_lesson_fragment_progress(lesson_id)
        print(f"  Fragment progress: {fragment_progress}")
        
        # Oblicz postęp jak w lesson.py
        completed_steps = sum(1 for step in step_order if fragment_progress.get(f"{step}_completed", False))
        completion_percent = (completed_steps / total_steps) * 100
        
        current_xp = 0
        for step in step_order:
            step_xp_key = f"{step}_xp"
            if step_xp_key in fragment_progress:
                current_xp += fragment_progress[step_xp_key]
        
        print(f"\nWyniki:")
        print(f"  Ukończone kroki: {completed_steps}/{total_steps}")
        print(f"  Procent ukończenia: {completion_percent:.1f}%")
        print(f"  Zdobyte XP: {current_xp}/{max_xp}")
        print(f"  Procent XP: {(current_xp/max_xp)*100:.1f}%")
        
        # Sprawdź synchronizację
        expected_completion = (1/7) * 100  # 14.3%
        expected_xp_percent = (step_xp_values['intro']/max_xp) * 100  # 1/20 = 5%
        
        print(f"\nSprawdzenie synchronizacji:")
        print(f"  Oczekiwany procent ukończenia: {expected_completion:.1f}%")
        print(f"  Rzeczywisty procent ukończenia: {completion_percent:.1f}%")
        print(f"  Oczekiwany procent XP: {expected_xp_percent:.1f}%")
        print(f"  Rzeczywisty procent XP: {(current_xp/max_xp)*100:.1f}%")
        
        if abs(completion_percent - expected_completion) < 0.1:
            print("  ✅ Procent ukończenia jest poprawny!")
        else:
            print("  ❌ Problem z procentem ukończenia!")
            
        if abs((current_xp/max_xp)*100 - expected_xp_percent) < 0.1:
            print("  ✅ Procent XP jest poprawny!")
        else:
            print("  ❌ Problem z procentem XP!")
        
        # Test różnicy między % kroków a % XP
        print(f"\n📊 Analiza różnicy:")
        print(f"  Różnica między % kroków a % XP: {completion_percent - (current_xp/max_xp)*100:.1f} punktów procentowych")
        print(f"  To jest normalne, bo kroki mają różne wartości XP!")
        
        print(f"\n🎉 Test zakończony!")
        
    except Exception as e:
        print(f"❌ Błąd w teście: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lesson_progress_sync()
