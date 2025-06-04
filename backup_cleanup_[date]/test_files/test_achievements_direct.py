#!/usr/bin/env python3
"""
Test the achievements module directly
"""

import json
import sys

print("🚀 Testing Achievements Module")

# Test import of achievements module
try:
    from utils.achievements import check_achievements
    print("✅ Successfully imported check_achievements function")
except Exception as e:
    print(f"❌ Failed to import achievements: {e}")
    sys.exit(1)

# Load user data to test with
try:
    with open('users_data.json', 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    print(f"✅ Loaded {len(users_data)} users")
except Exception as e:
    print(f"❌ Failed to load users: {e}")
    sys.exit(1)

# Test with user 'ola'
test_user = 'ola'
if test_user in users_data:
    user = users_data[test_user]
    print(f"\n👤 Testing user '{test_user}':")
    print(f"   XP: {user.get('xp', 0)}")
    print(f"   Level: {user.get('level', 1)}")
    print(f"   Test taken: {user.get('test_taken', False)}")
    print(f"   Neuroleader type: {user.get('neuroleader_type', 'None')}")
    print(f"   Current badges: {user.get('badges', [])}")
    
    # Test the check_achievements function
    try:
        new_badges = check_achievements(test_user)
        print(f"   🆕 New badges awarded: {new_badges}")
        
        # Check updated user data
        with open('users_data.json', 'r', encoding='utf-8') as f:
            updated_users_data = json.load(f)
        
        updated_user = updated_users_data.get(test_user, {})
        updated_badges = updated_user.get('badges', [])
        print(f"   🏆 Updated badges: {updated_badges}")
        
    except Exception as e:
        print(f"   ❌ Error in check_achievements: {e}")

else:
    print(f"❌ User '{test_user}' not found")

print("\n✅ Achievements test completed!")
