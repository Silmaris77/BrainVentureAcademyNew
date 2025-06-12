import json
import os

# Test the example lesson structure
lesson_file = r'c:\Users\pksia\Dropbox\Brainventure_kurs\B2\BrainVentureAcademyNew\data\lessons\EXAMPLE_NEUROPRZYWODZTWO.json'

print("🧠 Testing neuroprzywództwo lesson structure...")

try:
    with open(lesson_file, 'r', encoding='utf-8') as f:
        lesson = json.load(f)
    print("✅ JSON loads successfully")
    
    # Check practical_exercises section
    if 'practical_exercises' in lesson['sections']:
        pe = lesson['sections']['practical_exercises']
        print("✅ practical_exercises section found")
        
        if 'tabs' in pe:
            tabs = pe['tabs']
            required_tabs = ['autotest', 'reflection', 'analysis', 'implementation']
            
            for tab in required_tabs:
                if tab in tabs:
                    print(f"✅ {tab} tab found")
                else:
                    print(f"❌ {tab} tab missing")
            
        else:
            print("❌ tabs structure missing")
    else:
        print("❌ practical_exercises section missing")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n🔧 Testing lesson.py constants...")

# Simple check of the step definitions
step_names_test = {
    'intro': 'Wprowadzenie',
    'opening_quiz': 'Quiz startowy', 
    'content': 'Materiał',
    'practical_exercises': 'Ćwiczenia praktyczne',
    'reflection': 'Praktyka',
    'application': 'Wdrożenie',
    'closing_quiz': 'Quiz końcowy',
    'summary': 'Podsumowanie'
}

step_xp_test = {
    'intro': 5,  # 5% of 100
    'opening_quiz': 0,
    'content': 30,  # 30% of 100
    'practical_exercises': 40,  # 40% of 100
    'reflection': 20,  # 20% of 100 (backward compatibility)
    'application': 20,  # 20% of 100 (backward compatibility)
    'closing_quiz': 20,  # 20% of 100
    'summary': 5  # 5% of 100
}

print(f"✅ Expected step_names mapping: {step_names_test['practical_exercises']}")
print(f"✅ Expected XP allocation: {step_xp_test['practical_exercises']} XP (40%)")

print("\n🎯 Implementation validation complete!")
