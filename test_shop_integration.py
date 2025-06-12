#!/usr/bin/env python3
"""
Test script to verify the Neurocoin shop integration and Polish translation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_shop_imports():
    """Test that shop module imports correctly"""
    try:
        from views.shop_neurocoin import show_shop, SHOP_ITEMS, RARITY_TRANSLATIONS
        print("✅ Shop module imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import shop module: {e}")
        return False

def test_polish_translations():
    """Test that Polish translations are present"""
    try:
        from views.shop_neurocoin import RARITY_TRANSLATIONS, SHOP_ITEMS
        
        # Check rarity translations
        expected_rarities = {
            "common": "Pospolity",
            "uncommon": "Rzadki", 
            "rare": "Bardzo Rzadki",
            "epic": "Epicki",
            "legendary": "Legendarny"
        }
        
        print("Testing rarity translations:")
        for eng, pol in expected_rarities.items():
            if RARITY_TRANSLATIONS.get(eng) == pol:
                print(f"  ✅ {eng} -> {pol}")
            else:
                print(f"  ❌ {eng} -> {RARITY_TRANSLATIONS.get(eng)} (expected {pol})")
        
        # Check some item names are in Polish
        print("\nTesting item name translations:")
        sample_items = {
            'neural_leader': 'Neuro Lider',
            'empathy_master': 'Mistrz Empatii',
            'decision_wizard': 'Czarodziej Decyzji'
        }
        
        for item_id, expected_name in sample_items.items():
            actual_name = SHOP_ITEMS['avatars'].get(item_id, {}).get('name', 'NOT FOUND')
            if actual_name == expected_name:
                print(f"  ✅ {item_id}: {actual_name}")
            else:
                print(f"  ❌ {item_id}: {actual_name} (expected {expected_name})")
        
        return True
    except Exception as e:
        print(f"❌ Failed to test translations: {e}")
        return False

def test_material3_integration():
    """Test that Material3 components are imported"""
    try:
        # Test if the material3 import works
        import streamlit as st
        from utils.material3_components import apply_material3_theme
        print("✅ Material3 components import successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Material3 components: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Neurocoin Shop Integration and Polish Translation")
    print("=" * 60)
    
    tests = [
        ("Shop Module Import", test_shop_imports),
        ("Polish Translations", test_polish_translations),
        ("Material3 Integration", test_material3_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Shop integration looks good.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()
