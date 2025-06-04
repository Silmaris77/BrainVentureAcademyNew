#!/usr/bin/env python3
"""
Simple badge system test
"""

import json
import sys

print("🚀 Starting Badge System Test")

# Test 1: Load badge config
try:
    from config.badges import BADGES
    print(f"✅ Loaded {len(BADGES)} badges from standalone config")
except Exception as e:
    print(f"❌ Failed to load badges: {e}")
    sys.exit(1)

# Test 2: Load users data
try:
    with open('users_data.json', 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    print(f"✅ Loaded {len(users_data)} users from database")
except Exception as e:
    print(f"❌ Failed to load users: {e}")
    sys.exit(1)

# Test 3: Check specific user
test_user = 'ola'
if test_user in users_data:
    user = users_data[test_user]
    print(f"\n👤 User '{test_user}':")
    print(f"   XP: {user.get('xp', 0)}")
    print(f"   Level: {user.get('level', 1)}")
    print(f"   Test taken: {user.get('test_taken', False)}")
    print(f"   Neuroleader type: {user.get('neuroleader_type', 'None')}")
    print(f"   Current badges: {user.get('badges', [])}")
    
    # Test 4: Check badge eligibility
    current_badges = user.get('badges', [])
    
    # Check starter badge
    if user.get('xp', 0) > 0 and 'starter' not in current_badges:
        print("   🆕 Should have 'starter' badge")
    
    # Check tester badge  
    if user.get('test_taken', False) and 'tester' not in current_badges:
        print("   🆕 Should have 'tester' badge")
    
    # Check neuroleader type badge
    neuroleader_type = user.get('neuroleader_type')
    if neuroleader_type == 'Neuroinnowator' and 'innovator' not in current_badges:
        print("   🆕 Should have 'innovator' badge")
        
else:
    print(f"❌ User '{test_user}' not found")

print("\n✅ Simple badge test completed!")
