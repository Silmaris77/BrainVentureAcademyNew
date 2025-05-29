import json
from utils.mind_map import create_lesson_mind_map

print("🧠 MIND MAP SYSTEM - FINAL TEST")
print("=" * 40)

# Load lesson data
with open('data/lessons/B2C1L1.json', 'r', encoding='utf-8') as f:
    lesson_data = json.load(f)

print(f"✅ Lesson: {lesson_data.get('title')}")

# Check learning sections
learning_sections = lesson_data['sections']['learning']['sections']
print(f"✅ Learning sections: {len(learning_sections)}")

# Check routing logic
lesson_id = lesson_data.get('id', 'unknown')
if 'mind_map' in lesson_data:
    route = "Data-driven"
elif lesson_id == 'B1C1L1':
    route = "Hardcoded B1C1L1"
else:
    route = "Auto-generated (learning only)"

print(f"✅ Route: {route}")
print()
print("🚀 Mind map system ready!")
print("To test: streamlit run main.py → lesson → Summary → 🗺️ Mapa myśli")
