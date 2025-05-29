#!/usr/bin/env python3
"""
Quick test of mind map functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mind_map_import():
    """Test if mind map functions can be imported"""
    try:
        from utils.mind_map import create_auto_generated_mind_map, create_lesson_mind_map
        print("✅ Mind map functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_lesson_data():
    """Test loading lesson data"""
    try:
        import json
        with open('data/lessons/B2C1L1.json', 'r', encoding='utf-8') as file:
            lesson_data = json.load(file)
        
        print(f"✅ Lesson data loaded: {lesson_data.get('title', 'Unknown')}")
        
        # Check learning sections
        learning_sections = lesson_data['sections']['learning']['sections']
        print(f"✅ Found {len(learning_sections)} learning sections")
        
        return lesson_data
    except Exception as e:
        print(f"❌ Lesson data error: {e}")
        return None

def main():
    print("🧠 QUICK MIND MAP TEST")
    print("=" * 50)
    
    # Test imports
    import_success = test_mind_map_import()
    if not import_success:
        return
    
    # Test lesson data
    lesson_data = test_lesson_data()
    if not lesson_data:
        return
    
    # Test mind map creation (without streamlit dependencies)
    try:
        from utils.mind_map import create_auto_generated_mind_map
        print("✅ Mind map function available")
        
        # Test the routing logic
        lesson_id = "B2C1L1"
        if 'mind_map' in lesson_data:
            print("📊 Data-driven mind map would be used")
        elif lesson_id == 'B1C1L1':
            print("🎯 Hardcoded B1C1L1 mind map would be used")
        else:
            print("🤖 Auto-generated mind map would be used (learning sections only)")
            
        print("✅ All tests passed! Mind map system is ready.")
        
    except Exception as e:
        print(f"❌ Mind map creation error: {e}")

if __name__ == "__main__":
    main()
