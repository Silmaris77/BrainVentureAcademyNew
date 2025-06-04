#!/usr/bin/env python3
"""
Quick test to verify the neuroleader profile display fix
"""

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_profile_imports():
    """Test that all required imports work in profile.py"""
    try:
        from views.profile import show_profile_page
        from data.neuroleader_details import degen_details
        from views.degen_test import plot_radar_chart
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_neuroleader_data():
    """Test that user 'a' has complete neuroleader data"""
    try:
        with open('users_data.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        user_a = users_data.get('a', {})
        
        # Check required fields
        neuroleader_type = user_a.get('neuroleader_type') or user_a.get('degen_type')
        test_taken = user_a.get('test_taken', False)
        has_test_scores = 'test_scores' in user_a
        
        print(f"User 'a' neuroleader_type: {neuroleader_type}")
        print(f"User 'a' test_taken: {test_taken}")
        print(f"User 'a' has_test_scores: {has_test_scores}")
        
        if neuroleader_type and (test_taken or has_test_scores):
            print("✅ User 'a' has complete neuroleader data")
            return True
        else:
            print("❌ User 'a' missing neuroleader data")
            return False
            
    except Exception as e:
        print(f"❌ Error reading user data: {e}")
        return False

def test_neuroleader_details():
    """Test that neuroleader details are accessible"""
    try:
        from data.neuroleader_details import degen_details
        
        if 'Neuroreaktor' in degen_details:
            print("✅ Neuroleader details accessible")
            print(f"Neuroreaktor description: {degen_details['Neuroreaktor']['description'][:50]}...")
            return True
        else:
            print("❌ Neuroreaktor not found in degen_details")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing neuroleader details: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Testing neuroleader profile fix...")
    print("-" * 50)
    
    tests = [
        test_profile_imports,
        test_neuroleader_data,
        test_neuroleader_details
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n📝 Running {test.__name__}...")
        if test():
            passed += 1
        print("-" * 30)
    
    print(f"\n🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Neuroleader profile display should be working.")
    else:
        print("❌ Some tests failed. There may still be issues with the profile display.")

if __name__ == "__main__":
    main()
