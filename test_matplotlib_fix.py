#!/usr/bin/env python3
"""
Test script to verify matplotlib radar chart fix
"""

import sys
import os

# Add the current directory to Python path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

def test_matplotlib_radar():
    """Test the matplotlib radar chart functionality"""
    print("Testing matplotlib radar chart fix...")
    
    try:
        from views.neuroleader_explorer import plot_radar_chart
        print("✓ Successfully imported plot_radar_chart")
        
        # Test data
        test_scores = {
            "Strategiczny Wizjoner": 8.5,
            "Innowacyjny Kreator": 7.2,
            "Empatyczny Lider": 6.8,
            "Analityczny Myśliciel": 9.1,
            "Elastyczny Adapter": 7.5
        }
        
        # Try to create the chart
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        
        fig = plot_radar_chart(test_scores, device_type='desktop')
        print("✓ Radar chart created successfully - matplotlib fix works!")
        return True
        
    except Exception as e:
        print(f"✗ Radar chart test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test basic imports"""
    print("Testing basic imports...")
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib.pyplot imported successfully")
    except Exception as e:
        print(f"✗ matplotlib.pyplot import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except Exception as e:
        print(f"✗ numpy import failed: {e}")
        return False
        
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("Matplotlib Radar Chart Fix Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test basic imports
    if not test_imports():
        all_tests_passed = False
        print("❌ Basic imports failed - cannot proceed with radar chart test")
        return
    
    # Test radar chart
    if not test_matplotlib_radar():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Matplotlib radar chart fix is working correctly.")
        print("\nThe matplotlib compatibility issue has been resolved:")
        print("- Replaced deprecated ax.set_thetagrids() with ax.set_xticks() and ax.set_xticklabels()")
        print("- Used modern matplotlib methods for polar plots")
        print("- Charts should now display correctly in the neuroleader explorer")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
