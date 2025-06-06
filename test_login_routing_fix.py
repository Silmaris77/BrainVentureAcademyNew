#!/usr/bin/env python3
"""
Test script to verify login routing fix
"""

import sys
import os

# Add the current directory to Python path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

def test_session_init():
    """Test session state initialization"""
    print("Testing session state initialization...")
    
    try:
        from utils.session import init_session_state
        
        # Mock streamlit session state
        class MockSessionState:
            def __init__(self):
                self._state = {}
            
            def __contains__(self, key):
                return key in self._state
            
            def __getitem__(self, key):
                return self._state[key]
            
            def __setitem__(self, key, value):
                self._state[key] = value
            
            def get(self, key, default=None):
                return self._state.get(key, default)
        
        # Replace streamlit session state for testing
        import streamlit as st
        original_session_state = st.session_state
        st.session_state = MockSessionState()
        
        # Test initialization
        init_session_state()
        
        # Check if default values are correct
        if not st.session_state.get("logged_in", True):  # Should be False
            print("✓ logged_in correctly initialized to False")
        else:
            print("✗ logged_in should be False by default")
            return False
        
        if st.session_state.get("username") is None:
            print("✓ username correctly initialized to None") 
        else:
            print("✗ username should be None by default")
            return False
        
        if st.session_state.get("page") == "login":
            print("✓ page correctly initialized to 'login' for non-logged users")
        else:
            print(f"✗ page should be 'login' for non-logged users, got '{st.session_state.get('page')}'")
            return False
        
        # Test with logged in user
        st.session_state = MockSessionState()
        st.session_state["logged_in"] = True
        init_session_state()
        
        if st.session_state.get("page") == "dashboard":
            print("✓ page correctly initialized to 'dashboard' for logged users")
        else:
            print(f"✗ page should be 'dashboard' for logged users, got '{st.session_state.get('page')}'")
            return False
        
        # Restore original session state
        st.session_state = original_session_state
        
        return True
        
    except Exception as e:
        print(f"✗ Session state test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_imports():
    """Test that main module imports correctly"""
    print("\nTesting main module imports...")
    
    try:
        import main
        print("✓ Main module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Main module import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routing_logic():
    """Test routing logic structure"""
    print("\nTesting routing logic...")
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Check for correct routing structure
        if "if not st.session_state.logged_in:" in main_content:
            print("✓ Logged-in check found in routing")
        else:
            print("✗ Logged-in check not found in routing")
            return False
        
        if "show_login_page()" in main_content:
            print("✓ Login page call found")
        else:
            print("✗ Login page call not found")
            return False
        
        # Check that routing is properly structured
        lines = main_content.split('\n')
        routing_started = False
        found_login_check = False
        found_else_clause = False
        
        for line in lines:
            line = line.strip()
            if "if not st.session_state.logged_in:" in line:
                routing_started = True
                found_login_check = True
            elif routing_started and line.startswith("else:"):
                found_else_clause = True
                break
        
        if found_login_check and found_else_clause:
            print("✓ Routing structure is correct (if/else for login state)")
        else:
            print("✗ Routing structure is incorrect")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Routing logic test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("LOGIN ROUTING FIX VERIFICATION")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test session initialization
    if not test_session_init():
        all_tests_passed = False
    
    # Test main imports
    if not test_main_imports():
        all_tests_passed = False
    
    # Test routing logic
    if not test_routing_logic():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nLogin routing fix has been successfully implemented:")
        print("✓ Session state properly initializes with logged_in = False")
        print("✓ Default page is 'login' for non-logged users")
        print("✓ Application should now show login page first")
        print("✓ After login, users will be redirected to dashboard")
        print("\nNow when you run 'streamlit run main.py', you should see:")
        print("1. Login page appears first (no sidebar)")
        print("2. After successful login, dashboard appears with sidebar")
        print("3. Navigation works correctly between pages")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix them.")
    print("=" * 60)

if __name__ == "__main__":
    main()
