#!/usr/bin/env python3
"""
Test script to verify badge integration is working
"""

from utils.achievements import check_achievements
from data.users import load_user_data
import sys

def test_badge_integration():
    """Test the badge integration for various users"""
    print('🧪 Testing Badge Integration')
    print('=' * 50)
    
    # Test user "ola" - should get badges for completing test
    print('\n👤 Testing user "ola":')
    users_data = load_user_data()
    ola_data = users_data.get('ola', {})
    
    print(f"  Test taken: {ola_data.get('test_taken', False)}")
    print(f"  Neuroleader type: {ola_data.get('neuroleader_type', 'None')}")
    print(f"  Current badges: {ola_data.get('badges', [])}")
    
    try:
        new_badges = check_achievements('ola')
        print(f"  New badges awarded: {new_badges}")
        
        # Check updated user data
        updated_data = load_user_data()
        ola_updated = updated_data.get('ola', {})
        print(f"  Updated badges: {ola_updated.get('badges', [])}")
        
        if new_badges:
            print('  ✅ SUCCESS: Badge integration is working!')
        else:
            print('  ℹ️ INFO: No new badges (may already have all eligible badges)')
            
    except Exception as e:
        print(f'  ❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False
    
    # Test other users with test_taken = true but empty badges
    print('\n👥 Testing other users with empty badges:')
    
    test_users = ['q', 'b', 'c', 'x', 'zx']  # Users with test_taken=true but badges=[]
    
    for username in test_users:
        user_data = users_data.get(username, {})
        if user_data.get('test_taken', False) and not user_data.get('badges', []):
            print(f"\n  Testing user '{username}':")
            print(f"    Type: {user_data.get('neuroleader_type', 'None')}")
            
            try:
                new_badges = check_achievements(username)
                if new_badges:
                    print(f"    ✅ Awarded badges: {new_badges}")
                else:
                    print(f"    ℹ️ No new badges awarded")
            except Exception as e:
                print(f"    ❌ Error: {e}")
    
    print('\n' + '=' * 50)
    print('Badge integration test completed!')
    return True

if __name__ == "__main__":
    success = test_badge_integration()
    sys.exit(0 if success else 1)
