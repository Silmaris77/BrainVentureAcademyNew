#!/usr/bin/env python3
"""
Test kompletnego procesu przyznawania XP w lekcji
Sprawdza czy wszystkie kroki poprawnie przyznają XP
"""

import sys
import os
sys.path.append('.')

def test_complete_lesson_xp():
    """Test całego procesu XP w lekcji"""
    print("🧪 Test kompletnego procesu XP w lekcji")
    print("=" * 50)
    
    # Test imports
    try:
        from utils.lesson_progress import award_fragment_xp, get_lesson_fragment_progress
        from utils.real_time_updates import get_live_user_stats
        print("✅ Wszystkie imports udane!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test lesson completion with all steps
    lesson_id = "test_complete_lesson"
    max_xp = 100
    
    # XP values for each step (new 7-step system)
    step_xp_values = {
        'intro': int(max_xp * 0.05),          # 5% = 5 XP
        'opening_quiz': int(max_xp * 0.00),   # 0% = 0 XP
        'content': int(max_xp * 0.30),        # 30% = 30 XP
        'reflection': int(max_xp * 0.20),     # 20% = 20 XP
        'application': int(max_xp * 0.20),    # 20% = 20 XP
        'closing_quiz': int(max_xp * 0.20),   # 20% = 20 XP
        'summary': int(max_xp * 0.05)         # 5% = 5 XP
    }
    
    total_expected_xp = sum(step_xp_values.values())
    print(f"📊 Maksymalne XP lekcji: {max_xp}")
    print(f"📊 Suma XP wszystkich kroków: {total_expected_xp}")
    
    if total_expected_xp != max_xp:
        print(f"⚠️  Różnica: {max_xp - total_expected_xp} XP (przez zaokrąglenia)")
    else:
        print("✅ Suma XP kroków = maksymalne XP lekcji")
    
    print("\n🎯 Test przyznawania XP dla każdego kroku:")
    total_awarded_xp = 0
    
    # Test each step
    steps = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
    
    for step in steps:
        expected_xp = step_xp_values[step]
        
        # Symuluj użytkownika w sesji (wymagane dla award_fragment_xp)
        import streamlit as st
        if not hasattr(st, 'session_state'):
            # Mock session state for testing
            class MockSessionState:
                def __init__(self):
                    self.username = 'test_user'
            st.session_state = MockSessionState()
        else:
            st.session_state.username = 'test_user'
        
        try:
            success, xp_awarded = award_fragment_xp(lesson_id, step, expected_xp)
            
            if success and xp_awarded == expected_xp:
                print(f"  ✅ {step:15}: {xp_awarded:2d} XP")
                total_awarded_xp += xp_awarded
            elif success and xp_awarded == 0:
                print(f"  ⭕ {step:15}: {xp_awarded:2d} XP (już przyznane)")
            else:
                print(f"  ❌ {step:15}: błąd przyznawania XP")
        except Exception as e:
            print(f"  ❌ {step:15}: błąd - {e}")
    
    print(f"\n📊 Razem przyznane XP: {total_awarded_xp}/{total_expected_xp}")
    
    if total_awarded_xp == total_expected_xp:
        print("✅ Wszystkie XP zostały poprawnie przyznane!")
    else:
        print(f"⚠️  Różnica w przyznanych XP: {total_expected_xp - total_awarded_xp}")
    
    # Test lesson completion calculation
    print(f"\n🧪 Test kalkulacji ukończenia lekcji...")
    try:
        from utils.lesson_progress import calculate_lesson_completion, is_lesson_fully_completed
        
        completion_percent = calculate_lesson_completion(lesson_id)
        is_complete = is_lesson_fully_completed(lesson_id)
        
        print(f"📊 Procent ukończenia: {completion_percent:.1f}%")
        print(f"📊 Czy lekcja ukończona: {is_complete}")
        
        if completion_percent == 100.0 and is_complete:
            print("✅ Lekcja poprawnie oznaczona jako ukończona!")
        elif completion_percent > 0:
            print(f"✅ Częściowe ukończenie lekcji: {completion_percent:.1f}%")
        else:
            print("⚠️  Lekcja nie jest oznaczona jako ukończona")
            
    except Exception as e:
        print(f"❌ Błąd w kalkulacji ukończenia: {e}")
    
    print("\n🎉 Test zakończony!")
    print("=" * 50)
    
    return total_awarded_xp, total_expected_xp

if __name__ == "__main__":
    test_complete_lesson_xp()
