import json
import sys
import os

def test_migration():
    print("🧠 Testing BrainVenture Academy Migration...")
    
    try:
        # Test course structure
        with open('data/course_structure.json', 'r', encoding='utf-8') as f:
            course_data = json.load(f)
        
        print("✅ Course structure loaded successfully!")
        print(f"📚 Blocks: {len(course_data['blocks'])}")
        print(f"📂 Categories: {len(course_data['categories'])}")
        
        # Check neuroleadership content in first block
        first_block = course_data['blocks']['1']
        print(f"🧠 First block: {first_block['name']}")
        
        # Test skills file
        with open('views/skills_new.py', 'r', encoding='utf-8') as f:
            skills_content = f.read()
        
        if 'Akademia Neuroprzywództwa' in skills_content:
            print("✅ Skills tab updated to neuroleadership!")
        else:
            print("⚠️ Skills tab may need review")
        
        print("✅ Migration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_migration()
