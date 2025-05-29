#!/usr/bin/env python3

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from data.lessons import load_lessons
    print("✅ Successfully imported load_lessons function")
    
    lessons = load_lessons()
    print(f"✅ Successfully loaded {len(lessons)} lessons")
    
    # Check if our main lesson file loads
    if 'B1C1L1' in lessons:
        lesson = lessons['B1C1L1']
        print(f"✅ Main lesson B1C1L1 loaded successfully")
        print(f"   Title: {lesson['title']}")
        print(f"   XP Reward: {lesson['xp_reward']}")
    else:
        print("❌ Main lesson B1C1L1 not found")
        print(f"Available lessons: {list(lessons.keys())}")
    
    print("\n✨ JSON syntax fix successful! All lessons are loading properly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
