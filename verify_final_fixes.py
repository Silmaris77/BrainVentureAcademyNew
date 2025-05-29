#!/usr/bin/env python3
"""
Final verification of all XP calculation fixes and quiz requirements
"""

import sys
import os
import json

def test_lesson_data_consistency():
    """Test that lesson data has correct XP values"""
    print("🧪 Testing lesson data consistency...")
    
    lesson_files = [
        "data/lessons/B1C1L1.json",
        "data/lessons/B2C1L1.json"
    ]
    
    for lesson_file in lesson_files:
        if os.path.exists(lesson_file):
            print(f"\n📁 Testing {lesson_file}")
            
            with open(lesson_file, 'r', encoding='utf-8') as f:
                lesson_data = json.load(f)
            
            # Check max_xp
            max_xp = lesson_data.get('max_xp', 0)
            print(f"  📊 Max XP: {max_xp}")
            
            # Check sections XP
            sections = lesson_data.get('sections', {})
            section_xp = {}
            
            for section_name, section_data in sections.items():
                if isinstance(section_data, dict) and 'xp' in section_data:
                    section_xp[section_name] = section_data['xp']
                    print(f"  📊 {section_name}: {section_data['xp']} XP")
            
            total_section_xp = sum(section_xp.values())
            print(f"  📊 Total section XP: {total_section_xp}")
            
            if total_section_xp == max_xp:
                print(f"  ✅ XP values are consistent!")
            else:
                print(f"  ⚠️  XP mismatch: {max_xp} vs {total_section_xp}")
        else:
            print(f"❌ File not found: {lesson_file}")

def test_lesson_py_functions():
    """Test critical functions in lesson.py"""
    print("\n🧪 Testing lesson.py functions...")
    
    # Read lesson.py to check key fixes
    lesson_py_path = "views/lesson.py"
    if os.path.exists(lesson_py_path):
        with open(lesson_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key fixes
        fixes_to_check = [
            ("completion_percent = (current_xp / max_xp) * 100", "XP-based completion calculation"),
            ("passing_threshold=75", "75% requirement for closing quiz"),
            ("⏭️ Pomiń quiz", "Skip option for opening quiz"),
            ("award_fragment_xp", "XP awarding function calls"),
            ("quiz_completed, quiz_passed, earned_points = display_quiz", "Quiz result handling")
        ]
        
        for fix_text, description in fixes_to_check:
            if fix_text in content:
                print(f"  ✅ {description}: Found")
            else:
                print(f"  ❌ {description}: NOT FOUND")
    else:
        print(f"❌ File not found: {lesson_py_path}")

def test_progress_functions():
    """Test lesson progress functions"""
    print("\n🧪 Testing lesson progress functions...")
    
    progress_py_path = "utils/lesson_progress.py"
    if os.path.exists(progress_py_path):
        with open(progress_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for updated functions
        key_functions = [
            ("def calculate_lesson_completion", "Lesson completion calculation"),
            ("def award_fragment_xp", "XP awarding function"),
            ("completed_steps = 0", "Step counting logic"),
            ("max_steps = 7", "7-step system")
        ]
        
        for func_text, description in key_functions:
            if func_text in content:
                print(f"  ✅ {description}: Found")
            else:
                print(f"  ❌ {description}: NOT FOUND")
    else:
        print(f"❌ File not found: {progress_py_path}")

def main():
    """Run all verification tests"""
    print("🚀 Final Verification of XP Fixes and Quiz Requirements")
    print("=" * 60)
    
    test_lesson_data_consistency()
    test_lesson_py_functions()
    test_progress_functions()
    
    print("\n🎉 Verification completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
