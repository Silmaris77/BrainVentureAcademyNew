#!/usr/bin/env python3
import json
import sys

try:
    with open('data/lessons/B1C1L1.json', 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = json.loads(content)
    print("✅ JSON is valid!")
    
except json.JSONDecodeError as e:
    print(f"❌ JSON Error: {e}")
    print(f"   Line: {e.lineno}, Column: {e.colno}")
    print(f"   Position: {e.pos}")
    
    # Show the problematic area
    lines = content.split('\n')
    if e.lineno <= len(lines):
        line = lines[e.lineno - 1]
        print(f"   Problematic line {e.lineno}: {line}")
        print(f"   Around column {e.colno}: {line[max(0, e.colno-20):e.colno+20]}")
        
except Exception as e:
    print(f"❌ Other error: {e}")
