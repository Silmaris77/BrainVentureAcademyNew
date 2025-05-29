import json
import sys

def test_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        data = json.loads(content)
        print(f"✅ {filename} is valid JSON!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error in {filename}: {e}")
        print(f"   Line: {e.lineno}, Column: {e.colno}")
        return False
        
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return False

# Test the main lesson file
test_json_file('data/lessons/B1C1L1.json')

# Test all lesson files
import os
lessons_dir = 'data/lessons'
if os.path.exists(lessons_dir):
    json_files = [f for f in os.listdir(lessons_dir) if f.endswith('.json')]
    print(f"\nTesting {len(json_files)} JSON files:")
    
    valid_count = 0
    for json_file in json_files:
        file_path = os.path.join(lessons_dir, json_file)
        if test_json_file(file_path):
            valid_count += 1
    
    print(f"\n✨ Summary: {valid_count}/{len(json_files)} files are valid JSON")
