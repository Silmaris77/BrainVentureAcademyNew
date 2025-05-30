#!/usr/bin/env python3
"""
Simple verification test for neuroleader profile display
"""
import json

def test_neuroleader_profile_logic():
    """Test the exact same logic used in profile.py Tab 4"""
    
    print("🔍 Testing neuroleader profile display logic...")
    
    # Load user data
    with open('users_data.json', 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    user_data = users_data.get('a', {})
    
    # Same logic as in profile.py Tab 4
    neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type')
    test_taken = user_data.get('test_taken', False)
    has_test_scores = 'test_scores' in user_data
    
    print(f"📋 User 'a' data check:")
    print(f"   neuroleader_type: {neuroleader_type}")
    print(f"   test_taken: {test_taken}")
    print(f"   has_test_scores: {has_test_scores}")
    
    # The condition from profile.py
    if neuroleader_type and (test_taken or has_test_scores):
        print("✅ CONDITION MET: Neuroleader results should display!")
        print(f"   -> Would show: {neuroleader_type} profile")
        
        if has_test_scores:
            print(f"   -> Would show radar chart with scores:")
            for ntype, score in user_data['test_scores'].items():
                print(f"      {ntype}: {score}")
        
        return True
    else:
        print("❌ CONDITION NOT MET: Neuroleader results would NOT display")
        return False

if __name__ == "__main__":
    test_neuroleader_profile_logic()
