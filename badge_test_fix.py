#!/usr/bin/env python3
"""Test badge integration for BrainVenture Academy"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.achievements import check_achievements
from data.users import load_user_data

def test_badge_integration():
    """Test badge integration for user ola"""
    print("🧪 Testing Badge Integration")
    print("="*50)
    
    # Test badge integration
    print("Testing badge integration...")
    users_data = load_user_data()
    ola_data = users_data.get('ola', {})
    print(f"User 'ola' before: test_taken={ola_data.get('test_taken')}, badges={ola_data.get('badges')}")

    try:
        new_badges = check_achievements('ola')
        print(f"New badges awarded: {new_badges}")

        updated_data = load_user_data()
        ola_updated = updated_data.get('ola', {})
        print(f"User 'ola' after: badges={ola_updated.get('badges')}")
        
        if new_badges:
            print("✅ SUCCESS: Badge integration is working!")
        else:
            print("ℹ️ INFO: No new badges awarded (may already have eligible badges)")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    # Test other users with test_taken=true but empty badges
    print("\n👥 Testing other users:")
    test_users = ['q', 'b', 'c', 'x', 'zx']
    
    for username in test_users:
        user_data = users_data.get(username, {})
        if user_data.get('test_taken', False) and not user_data.get('badges', []):
            print(f"  Testing user '{username}' (type: {user_data.get('neuroleader_type', 'None')})...")
            try:
                new_badges = check_achievements(username)
                if new_badges:
                    print(f"    ✅ Awarded badges: {new_badges}")
                else:
                    print(f"    ℹ️ No new badges")
            except Exception as e:
                print(f"    ❌ Error: {e}")

if __name__ == "__main__":
    test_badge_integration()
