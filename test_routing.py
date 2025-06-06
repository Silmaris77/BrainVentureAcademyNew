#!/usr/bin/env python3
"""
Test script to verify that dashboard routing fixes are working correctly.
This script will test the import structure and routing configuration.
"""

import sys
import os

# Add the current directory to Python path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from views.dashboard import show_dashboard
        print("✓ Dashboard import successful")
    except Exception as e:
        print(f"✗ Dashboard import failed: {e}")
        return False
      try:
        from views.neuroleader_explorer import show_neuroleader_explorer
        print("✓ Neuroleader explorer import successful")
    except Exception as e:
        print(f"✗ Neuroleader explorer import failed: {e}")
        return False
    
    try:
        import main
        print("✓ Main module import successful")
    except Exception as e:
        print(f"✗ Main module import failed: {e}")
        return False
    
    return True

def test_routing_configuration():
    """Test that routing is properly configured in main.py."""
    print("\nTesting routing configuration...")
    
    try:
        import main        # Check if the routing dictionary or logic includes 'degen_explorer'
        with open('main.py', 'r', encoding='utf-8') as f:
            main_content = f.read()
            
        if "'degen_explorer'" in main_content:
            print("✓ 'degen_explorer' route found in main.py")
        else:
            print("✗ 'degen_explorer' route not found in main.py")
            return False
            
        if "show_neuroleader_explorer" in main_content:
            print("✓ 'show_neuroleader_explorer' function call found in main.py")
        else:
            print("✗ 'show_neuroleader_explorer' function call not found in main.py")
            return False
            
    except Exception as e:
        print(f"✗ Routing configuration test failed: {e}")
        return False
    
    return True

def test_dashboard_routing_references():
    """Test that dashboard.py uses correct routing references."""
    print("\nTesting dashboard routing references...")
    
    try:
        with open('views/dashboard.py', 'r', encoding='utf-8') as f:
            dashboard_content = f.read()
            
        # Count occurrences of the old and new routing
        old_routing_count = dashboard_content.count("'neuroleader_explorer'")
        new_routing_count = dashboard_content.count("'degen_explorer'")
        
        print(f"Old routing references ('neuroleader_explorer'): {old_routing_count}")
        print(f"New routing references ('degen_explorer'): {new_routing_count}")
        
        if old_routing_count == 0:
            print("✓ No old routing references found")
        else:
            print(f"✗ Found {old_routing_count} old routing references that need to be fixed")
            return False
            
        if new_routing_count > 0:
            print("✓ New routing references found")
        else:
            print("✗ No new routing references found")
            return False
            
    except Exception as e:
        print(f"✗ Dashboard routing test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("BrainVenture Academy - Dashboard Routing Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test routing configuration
    if not test_routing_configuration():
        all_tests_passed = False
    
    # Test dashboard routing references
    if not test_dashboard_routing_references():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Dashboard routing should now work correctly.")
        print("\nNext steps:")
        print("1. Run: streamlit run main.py")
        print("2. Log in to the application")
        print("3. Go to the dashboard")
        print("4. Click 'Wykonaj test neuroleadera' or 'Wykonaj test' buttons")
        print("5. Verify they navigate to the neuroleader test page")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
