#!/usr/bin/env python3
"""
Direct test of profile Tab 4 neuroleader section logic
"""

import sys
import json
sys.path.append('.')

# Direct imports matching profile.py
from data.test_questions import NEUROLEADER_TYPES
from data.neuroleader_details import degen_details
from utils.user_management import load_user_data

def test_tab4_logic():
    """Test exactly what Tab 4 in profile.py does"""
    print("=== DIRECT TAB 4 LOGIC TEST ===\n")
    
    # Load user data exactly like profile.py does after our fix
    users_data = load_user_data()
    user_data = users_data.get('a', {})
    
    print("1. User data check:")
    print(f"   User exists: {bool(user_data)}")
    print(f"   neuroleader_type: {repr(user_data.get('neuroleader_type'))}")
    print(f"   degen_type: {repr(user_data.get('degen_type'))}")
    print(f"   test_taken: {user_data.get('test_taken')}")
    print(f"   has_test_scores: {'test_scores' in user_data}")
    
    # Exact logic from profile.py lines 399-401
    neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type')
    test_taken = user_data.get('test_taken', False)
    has_test_scores = 'test_scores' in user_data
    
    print(f"\n2. Tab 4 condition logic:")
    print(f"   Resolved neuroleader_type: {repr(neuroleader_type)}")
    print(f"   test_taken: {test_taken}")
    print(f"   has_test_scores: {has_test_scores}")
    
    # Main condition from line 403
    main_condition = neuroleader_type and (test_taken or has_test_scores)
    print(f"   Main condition (line 403): {main_condition}")
    
    if main_condition:
        print("\n3. ✅ MAIN CONDITION PASSES - Neuroleader section will show")
        
        # Check NEUROLEADER_TYPES availability
        neuroleader_color = NEUROLEADER_TYPES.get(neuroleader_type, {}).get('color', '#3498db')
        print(f"   Neuroleader color: {neuroleader_color}")
        
        # Check inner condition from line 422
        inner_condition = neuroleader_type in NEUROLEADER_TYPES
        print(f"   Inner condition (line 422): {inner_condition}")
        
        if inner_condition:
            print("   ✅ INNER CONDITION PASSES - Will show detailed results")
            
            # Check available NEUROLEADER_TYPES
            print(f"   Available NEUROLEADER_TYPES: {list(NEUROLEADER_TYPES.keys())}")
            print(f"   User's type in NEUROLEADER_TYPES: {neuroleader_type in NEUROLEADER_TYPES}")
            
            # Check degen_details availability
            has_degen_details = neuroleader_type in degen_details
            print(f"   Has degen_details: {has_degen_details}")
            if has_degen_details:
                details_length = len(degen_details[neuroleader_type])
                print(f"   Details length: {details_length} chars")
            
            return True
        else:
            print("   ❌ INNER CONDITION FAILS - Will show warning message")
            print(f"   Expected types: {list(NEUROLEADER_TYPES.keys())}")
            print(f"   User type: {repr(neuroleader_type)}")
            return False
    else:
        print(f"\n3. ❌ MAIN CONDITION FAILS - Neuroleader section will NOT show")
        print(f"   Will show 'take test' message instead")
        return False

if __name__ == "__main__":
    result = test_tab4_logic()
    print(f"\n{'='*60}")
    print(f"FINAL RESULT: {'✅ TAB 4 WILL SHOW NEUROLEADER RESULTS' if result else '❌ TAB 4 WILL NOT SHOW RESULTS'}")
