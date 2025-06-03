#!/usr/bin/env python3
"""
Health check script for BrainVenture Academy application
"""

import os
import sys
import traceback
import py_compile

def check_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        py_compile.compile(file_path, doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)

def check_imports(file_path):
    """Check if a Python file can be imported without errors."""
    try:
        # Get module name from file path
        rel_path = os.path.relpath(file_path, os.getcwd())
        module_name = rel_path.replace(os.sep, '.').replace('.py', '')
        
        # Try to import
        __import__(module_name)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 BrainVenture Academy - Application Health Check")
    print("=" * 50)
    
    # Key files to check
    key_files = [
        'main.py',
        'views/degen_types.py',
        'views/dashboard.py', 
        'views/lesson.py',
        'views/profile.py',
        'views/shop_new.py',
        'views/skills_new.py',
        'utils/achievements.py',
        'utils/components.py',
        'utils/course_map.py',
        'utils/session.py',
        'data/lessons.py',
        'data/users.py',
        'config/settings.py'
    ]
    
    syntax_errors = []
    import_errors = []
    
    print("📝 Checking syntax...")
    for file_path in key_files:
        if os.path.exists(file_path):
            is_valid, error = check_syntax(file_path)
            if is_valid:
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path}: {error}")
                syntax_errors.append((file_path, error))
        else:
            print(f"  ⚠️  {file_path}: File not found")
    
    print(f"\n📦 Checking imports...")
    for file_path in key_files:
        if os.path.exists(file_path) and file_path not in [f[0] for f in syntax_errors]:
            is_valid, error = check_imports(file_path)
            if is_valid:
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path}: {error}")
                import_errors.append((file_path, error))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print(f"Syntax errors: {len(syntax_errors)}")
    print(f"Import errors: {len(import_errors)}")
    
    if syntax_errors:
        print("\n❌ SYNTAX ERRORS:")
        for file_path, error in syntax_errors:
            print(f"  - {file_path}: {error}")
    
    if import_errors:
        print("\n❌ IMPORT ERRORS:")
        for file_path, error in import_errors:
            print(f"  - {file_path}: {error}")
    
    if not syntax_errors and not import_errors:
        print("\n🎉 ALL CHECKS PASSED! Application appears healthy.")
        return 0
    else:
        print(f"\n⚠️  Found {len(syntax_errors + import_errors)} issues that need attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
