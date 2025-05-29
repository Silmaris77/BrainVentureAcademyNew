#!/usr/bin/env python3
"""
Final verification that the JSON syntax error has been fixed
"""

import json
import os
import sys

def test_lesson_loading():
    """Test the exact scenario that was failing before"""
    
    print("🔍 Testing JSON syntax fix...")
    
    # Test 1: Direct JSON parsing of the problematic file
    print("\n1. Testing B1C1L1.json direct parsing...")
    try:
        with open('data/lessons/B1C1L1.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("   ✅ B1C1L1.json parses successfully")
        print(f"   📚 Lesson title: {data['title']}")
        print(f"   🏆 XP reward: {data['xp_reward']}")
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON Error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Other error: {e}")
        return False
    
    # Test 2: Load lessons using the actual function that was failing
    print("\n2. Testing load_lessons() function...")
    try:
        sys.path.insert(0, os.path.abspath('.'))
        from data.lessons import load_lessons
        
        lessons = load_lessons()
        print(f"   ✅ Successfully loaded {len(lessons)} lessons")
        
        if 'B1C1L1' in lessons:
            lesson = lessons['B1C1L1']
            print("   ✅ Main lesson B1C1L1 accessible")
            print(f"   📝 Has intro section: {'intro' in lesson}")
            print(f"   📚 Has sections: {'sections' in lesson}")
        else:
            available = list(lessons.keys())
            print(f"   ⚠️  B1C1L1 not found, available: {available}")
            
    except Exception as e:
        print(f"   ❌ Error loading lessons: {e}")
        return False
    
    # Test 3: Test all lesson files for JSON validity
    print("\n3. Testing all lesson files...")
    lessons_dir = 'data/lessons'
    json_files = [f for f in os.listdir(lessons_dir) if f.endswith('.json')]
    
    valid_count = 0
    for json_file in json_files:
        file_path = os.path.join(lessons_dir, json_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"   ✅ {json_file}")
            valid_count += 1
        except json.JSONDecodeError as e:
            print(f"   ❌ {json_file}: {e}")
        except Exception as e:
            print(f"   ❌ {json_file}: {e}")
    
    print(f"\n📊 Summary: {valid_count}/{len(json_files)} lesson files are valid JSON")
    
    # Test 4: Check for any remaining problematic patterns
    print("\n4. Checking for remaining escape issues...")
    problematic_found = False
    for json_file in json_files:
        file_path = os.path.join(lessons_dir, json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for the specific pattern that was causing issues
            if '„' in content and '\\"' in content:
                # Check if there are any unescaped patterns like „word\"
                import re
                patterns = re.findall(r'„[^"]*\\"', content)
                if patterns:
                    print(f"   ⚠️  {json_file}: Found {len(patterns)} potentially problematic patterns")
                    problematic_found = True
    
    if not problematic_found:
        print("   ✅ No problematic escape patterns found")
    
    print("\n🎉 JSON syntax fix verification complete!")
    print("✨ The application should now load lessons without JSONDecodeError")
    
    return valid_count == len(json_files)

if __name__ == "__main__":
    success = test_lesson_loading()
    if success:
        print("\n🚀 SUCCESS: All tests passed - JSON syntax error is fixed!")
    else:
        print("\n⚠️  WARNING: Some issues remain")
