import json

# Test the specific JSON file that was causing issues
try:
    with open('data/lessons/B1C1L1.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    
    print("SUCCESS: JSON is now valid!")
    print(f"Lesson title: {data['title']}")
    print(f"XP reward: {data['xp_reward']}")
    
    # Test the lesson loading function
    from data.lessons import load_lessons
    lessons = load_lessons()
    print(f"SUCCESS: Loaded {len(lessons)} lessons")
    
    if 'B1C1L1' in lessons:
        print("SUCCESS: Main lesson B1C1L1 is accessible")
    
except Exception as e:
    print(f"ERROR: {e}")
    
input("Press Enter to continue...")
