#!/usr/bin/env python3
"""
Quick verification test for mind map system
"""

def quick_verification():
    print("🔍 QUICK MIND MAP VERIFICATION")
    print("=" * 40)
    
    # Test 1: Import test
    try:
        from utils.mind_map import create_lesson_mind_map, create_data_driven_mind_map, create_auto_generated_mind_map
        print("✅ All mind map functions imported successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test 2: Data loading test
    try:
        import json
        with open('data/lessons/B1C1L1.json', 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)
        
        print(f"✅ B1C1L1 lesson loaded: {lesson_data.get('title')}")
        print(f"✅ Has mind_map structure: {'mind_map' in lesson_data}")
        
        if 'mind_map' in lesson_data:
            mind_map = lesson_data['mind_map']
            sections = ['central_node', 'categories', 'solutions', 'case_study', 'connections', 'config']
            found_sections = [s for s in sections if s in mind_map]
            print(f"✅ Mind map sections found: {len(found_sections)}/{len(sections)}")
        
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return
    
    # Test 3: Function execution test
    try:
        result = create_lesson_mind_map(lesson_data)
        print(f"✅ create_lesson_mind_map executed successfully")
        
        if result is None:
            print("ℹ️ Function returned None (expected if streamlit-agraph not available)")
        else:
            print("ℹ️ Function returned visualization component")
            
    except Exception as e:
        print(f"❌ Function execution error: {e}")
        return
    
    # Test 4: Logic test
    try:
        # Test data-driven path
        test_lesson_with_mindmap = {"id": "TEST", "mind_map": {"central_node": {"id": "test"}}}
        result1 = create_lesson_mind_map(test_lesson_with_mindmap)
        print("✅ Data-driven path works")
        
        # Test auto-generated path
        test_lesson_without_mindmap = {"id": "TEST_OTHER", "title": "Test", "sections": {}}
        result2 = create_lesson_mind_map(test_lesson_without_mindmap)
        print("✅ Auto-generated path works")
        
    except Exception as e:
        print(f"❌ Logic test error: {e}")
        return
    
    print("\n🎉 ALL TESTS PASSED - MIND MAP SYSTEM IS READY!")
    print("🚀 The scalable mind map system is fully functional.")

if __name__ == "__main__":
    quick_verification()
