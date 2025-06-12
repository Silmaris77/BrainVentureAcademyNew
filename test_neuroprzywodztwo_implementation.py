#!/usr/bin/env python3
"""
Test script for the new practical_exercises implementation
"""

import sys
import os
import json

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_lesson_structure():
    """Test if the new lesson structure is valid"""
    lesson_file = os.path.join(project_root, 'data', 'lessons', 'EXAMPLE_NEUROPRZYWODZTWO.json')
    
    print("🧠 Testing new neuroprzywództwo lesson structure...")
    
    # Check if file exists
    if not os.path.exists(lesson_file):
        print(f"❌ Lesson file not found: {lesson_file}")
        return False
    
    # Load and validate JSON
    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            lesson = json.load(f)
        print("✅ JSON structure is valid")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    
    # Check required fields
    required_fields = ['id', 'title', 'sections']
    for field in required_fields:
        if field not in lesson:
            print(f"❌ Missing required field: {field}")
            return False
    print("✅ Required fields present")
    
    # Check if practical_exercises section exists
    if 'practical_exercises' not in lesson['sections']:
        print("❌ Missing practical_exercises section")
        return False
    print("✅ practical_exercises section found")
    
    # Check practical_exercises structure
    pe_section = lesson['sections']['practical_exercises']
    
    if 'tabs' not in pe_section:
        print("❌ Missing tabs in practical_exercises")
        return False
    print("✅ tabs structure found")
    
    # Check for required tabs
    required_tabs = ['autotest', 'reflection', 'analysis', 'implementation']
    tabs = pe_section['tabs']
    
    for tab in required_tabs:
        if tab not in tabs:
            print(f"❌ Missing required tab: {tab}")
            return False
        
        # Check tab structure
        tab_data = tabs[tab]
        if 'title' not in tab_data or 'sections' not in tab_data:
            print(f"❌ Invalid structure in tab: {tab}")
            return False
    
    print("✅ All 4 required tabs present with valid structure")
    
    # Check if each tab has sections with content
    for tab_name, tab_data in tabs.items():
        sections = tab_data['sections']
        if not sections or len(sections) == 0:
            print(f"❌ Empty sections in tab: {tab_name}")
            return False
        
        for section in sections:
            if 'title' not in section or 'content' not in section:
                print(f"❌ Invalid section structure in tab: {tab_name}")
                return False
    
    print("✅ All tabs have valid sections with content")
    
    return True

def test_step_names_mapping():
    """Test if step names mapping includes practical_exercises"""
    try:
        from views.lesson import step_names
        
        if 'practical_exercises' not in step_names:
            print("❌ practical_exercises not found in step_names mapping")
            return False
        
        if step_names['practical_exercises'] != 'Ćwiczenia praktyczne':
            print(f"❌ Incorrect mapping for practical_exercises: {step_names['practical_exercises']}")
            return False
        
        print("✅ step_names mapping is correct")
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import lesson module: {e}")
        return False

def test_xp_allocation():
    """Test if XP allocation includes practical_exercises"""
    try:
        from views.lesson import step_xp_values
        
        if 'practical_exercises' not in step_xp_values:
            print("❌ practical_exercises not found in step_xp_values")
            return False
        
        # Check if practical_exercises gets 40% of XP (for 100 XP lesson = 40 XP)
        expected_xp = int(100 * 0.40)  # 40% of 100 XP
        actual_xp = step_xp_values['practical_exercises']
        
        if actual_xp != expected_xp:
            print(f"❌ Incorrect XP allocation for practical_exercises: {actual_xp}, expected: {expected_xp}")
            return False
        
        print(f"✅ XP allocation is correct: {actual_xp} XP (40%)")
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import lesson module: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 NEUROPRZYWÓDZTWO IMPLEMENTATION TEST")
    print("=" * 50)
    
    tests = [
        ("Lesson Structure", test_lesson_structure),
        ("Step Names Mapping", test_step_names_mapping),
        ("XP Allocation", test_xp_allocation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"🎯 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Implementation is ready!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
