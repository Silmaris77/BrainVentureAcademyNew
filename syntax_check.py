#!/usr/bin/env python3
import ast

def check_python_syntax(file_path):
    """Check if Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        ast.parse(source)
        print(f"✅ {file_path} - Syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path} - Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path} - Error reading file: {e}")
        return False

if __name__ == "__main__":
    files_to_check = [
        "utils/achievements.py",
        "config/settings.py",
        "views/profile.py"
    ]
    
    print("🔍 Checking Python syntax...")
    print("="*40)
    
    all_good = True
    for file_path in files_to_check:
        if not check_python_syntax(file_path):
            all_good = False
    
    print("="*40)
    if all_good:
        print("🎉 All files have valid Python syntax!")
    else:
        print("⚠️  Some files have syntax errors!")
