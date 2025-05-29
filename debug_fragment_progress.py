#!/usr/bin/env python3
"""
Debug test - sprawdź co się dzieje z fragment_progress
"""

import sys
import os
sys.path.append('.')

def debug_fragment_progress():
    """Debuguj postęp fragmentów"""
    print("🔍 Debug test - fragment progress")
    print("=" * 50)
    
    try:
        from utils.lesson_progress import get_lesson_fragment_progress, award_fragment_xp
        import streamlit as st
        
        # Mock session state
        class MockSessionState:
            def __init__(self):
                self.username = 'test_user'
        
        if not hasattr(st, 'session_state'):
            st.session_state = MockSessionState()
        else:
            st.session_state.username = 'test_user'
        
        lesson_id = "test_lesson_debug"
        
        # Sprawdź początkowy stan
        print("📊 Początkowy stan fragmentów:")
        initial_progress = get_lesson_fragment_progress(lesson_id)
        print(f"   {initial_progress}")
        
        # Spróbuj przyznać XP za intro
        print("\n🎯 Próba przyznania 5 XP za intro...")
        success, xp_awarded = award_fragment_xp(lesson_id, 'intro', 5)
        print(f"   Success: {success}, XP: {xp_awarded}")
        
        # Sprawdź stan po przyznaniu XP
        print("\n📊 Stan po przyznaniu XP za intro:")
        after_intro = get_lesson_fragment_progress(lesson_id)
        print(f"   {after_intro}")
        
        # Sprawdź jakie klucze są dostępne
        print("\n🔑 Dostępne klucze w fragment_progress:")
        for key in after_intro.keys():
            print(f"   - {key}: {after_intro[key]}")
        
        # Spróbuj przyznać XP za content
        print("\n🎯 Próba przyznania 30 XP za content...")
        success2, xp_awarded2 = award_fragment_xp(lesson_id, 'content', 30)
        print(f"   Success: {success2}, XP: {xp_awarded2}")
        
        # Sprawdź końcowy stan
        print("\n📊 Końcowy stan fragmentów:")
        final_progress = get_lesson_fragment_progress(lesson_id)
        print(f"   {final_progress}")
        
        # Test kalkulacji XP
        print("\n🧮 Test kalkulacji current_xp:")
        current_xp = 0
        step_order = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
        
        for step in step_order:
            step_xp_key = f"{step}_xp"
            if step_xp_key in final_progress:
                step_xp = final_progress[step_xp_key]
                current_xp += step_xp
                print(f"   - {step}: {step_xp} XP")
            else:
                print(f"   - {step}: 0 XP (brak klucza {step_xp_key})")
        
        print(f"\n💎 Razem current_xp: {current_xp}")
        
        # Test czy completed_steps się zgadza
        print("\n✅ Test ukończonych kroków:")
        completed_steps = 0
        for step in step_order:
            completed_key = f"{step}_completed"
            if final_progress.get(completed_key, False):
                completed_steps += 1
                print(f"   ✅ {step}")
            else:
                print(f"   ⭕ {step}")
        
        print(f"\n📊 Ukończone kroki: {completed_steps}/7 = {(completed_steps/7)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Błąd podczas debugowania: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_fragment_progress()
