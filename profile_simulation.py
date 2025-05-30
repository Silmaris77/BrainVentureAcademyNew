#!/usr/bin/env python3
"""
Simulate exactly what profile.py Tab 4 does to verify the fix
"""

import sys
import json
sys.path.append('.')

def load_user_data():
    """Simulate the load_user_data function"""
    try:
        with open('users_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def simulate_profile_tab4():
    """Simulate exactly what happens in profile.py Tab 4"""
    print("=== SIMULATING PROFILE.PY TAB 4 LOGIC ===\n")
    
    # Simulate the fixed data loading (instead of get_live_user_stats)
    users_data = load_user_data()
    user_data = users_data.get('a', {})  # Test with user 'a'
    
    print("1. Data Loading Results:")
    print(f"   - User data loaded: {bool(user_data)}")
    print(f"   - neuroleader_type: {user_data.get('neuroleader_type')}")
    print(f"   - degen_type: {user_data.get('degen_type')}")
    print(f"   - test_taken: {user_data.get('test_taken')}")
    print(f"   - has_test_scores: {'test_scores' in user_data}")
    
    # Simulate the neuroleader type resolution logic from profile.py
    neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type', 'Typ nie określony')
    test_taken = user_data.get('test_taken', False)
    has_test_scores = 'test_scores' in user_data
    
    print(f"\n2. Logic Evaluation:")
    print(f"   - Resolved neuroleader_type: '{neuroleader_type}'")
    print(f"   - test_taken: {test_taken}")
    print(f"   - has_test_scores: {has_test_scores}")
    
    # Simulate the condition check from profile.py
    condition_met = neuroleader_type and (test_taken or has_test_scores)
    
    print(f"\n3. Condition Check:")
    print(f"   - neuroleader_type exists: {bool(neuroleader_type)}")
    print(f"   - (test_taken or has_test_scores): {test_taken or has_test_scores}")
    print(f"   - FINAL CONDITION: {condition_met}")
    
    # Check if neuroleader details would be found
    try:
        from data.neuroleader_details import degen_details
        has_details = neuroleader_type in degen_details
        print(f"   - Neuroleader details available: {has_details}")
        if has_details:
            details = degen_details[neuroleader_type]
            print(f"   - Details title: '{details.get('title', 'Brak tytułu')}'")
    except ImportError as e:
        print(f"   - Import error: {e}")
        has_details = False
    
    # Final result
    will_display = condition_met and has_details
    print(f"\n4. FINAL RESULT:")
    print(f"   {'✅ NEUROLEADER SECTION WILL DISPLAY' if will_display else '❌ NEUROLEADER SECTION WILL NOT DISPLAY'}")
    
    return will_display

if __name__ == "__main__":
    result = simulate_profile_tab4()
    print(f"\n{'='*50}")
    print(f"FIX STATUS: {'SUCCESS - Issue resolved!' if result else 'FAILURE - Issue remains'}")
