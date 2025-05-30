import sys
sys.path.append('.')

from data.users import load_user_data

users_data = load_user_data()
user_a = users_data.get('a', {})

print("=== USER 'a' DATA ===")
print(f"neuroleader_type: {user_a.get('neuroleader_type')}")
print(f"degen_type: {user_a.get('degen_type')}")
print(f"test_taken: {user_a.get('test_taken')}")
print(f"has test_scores: {bool(user_a.get('test_scores'))}")
print(f"xp: {user_a.get('xp')}")

# Test neuroleader type detection
neuroleader_type = user_a.get('neuroleader_type') or user_a.get('degen_type')
print(f"\nDetected neuroleader_type: {neuroleader_type}")

if neuroleader_type:
    print("✅ User HAS neuroleader data - dashboard will show results section")
else:
    print("❌ User has NO neuroleader data - dashboard will show test invitation")
