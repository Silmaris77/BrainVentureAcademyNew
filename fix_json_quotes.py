#!/usr/bin/env python3
"""
Script to fix JSON escaping issues in lesson files
"""

import json
import os
import re

def fix_json_file(file_path):
    """Fix JSON escaping issues in a file"""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as JSON first
        try:
            data = json.loads(content)
            print(f"✅ {file_path} is already valid JSON")
            return True
        except json.JSONDecodeError as e:
            print(f"🔧 Fixing JSON issues in {file_path}")
            print(f"   Error: {e}")
            
            # Common fixes for JSON issues
            fixed_content = content
            
            # Fix unescaped quotes in strings (but be careful not to break intentional quotes)
            # Look for patterns like: "text with "quote" inside"
            # Replace with: "text with \"quote\" inside"
            
            # Pattern 1: Fix quotes that appear to be unescaped inside strings
            # This is a more conservative approach that looks for specific problematic patterns
            
            # Pattern for Polish quotes that might be causing issues
            fixed_content = re.sub(r'([^\\])"([^"]*[^\\])"([^,}\]])', r'\1\"\2\"\3', fixed_content)
            
            # Pattern for deadline quote issue
            fixed_content = fixed_content.replace('„deadline to deadline\"', '„deadline to deadline"')
            fixed_content = fixed_content.replace('deadline to deadline\"', 'deadline to deadline"')
            
            # Fix any remaining issues with quotes around Polish words
            problematic_patterns = [
                (r'„ogarnia\"', '„ogarnia"'),
                (r'„zarządza\"', '„zarządza"'),
                (r'„ogarniacz\"', '„ogarniacz"'),
                (r'„z góry\"', '„z góry"'),
            ]
            
            for pattern, replacement in problematic_patterns:
                fixed_content = fixed_content.replace(pattern, replacement)
            
            # Try to parse the fixed content
            try:
                data = json.loads(fixed_content)
                
                # If successful, write back the fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Fixed and saved {file_path}")
                return True
                
            except json.JSONDecodeError as e2:
                print(f"❌ Could not fix {file_path}: {e2}")
                return False
                
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all JSON files in lessons directory"""
    lessons_dir = "data/lessons"
    
    if not os.path.exists(lessons_dir):
        print(f"❌ Directory {lessons_dir} not found")
        return
    
    json_files = [f for f in os.listdir(lessons_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"❌ No JSON files found in {lessons_dir}")
        return
    
    print(f"🔍 Found {len(json_files)} JSON files to check")
    
    fixed_count = 0
    for json_file in json_files:
        file_path = os.path.join(lessons_dir, json_file)
        if fix_json_file(file_path):
            fixed_count += 1
    
    print(f"\n✨ Summary: {fixed_count}/{len(json_files)} files processed successfully")

if __name__ == "__main__":
    main()
