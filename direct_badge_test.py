#!/usr/bin/env python3
"""Direct test of badge awarding functionality"""

# Test direct imports first
try:
    print("Testing imports...")
    from config.settings import BADGES
    print(f"✅ BADGES imported successfully - {len(BADGES)} badges configured")
    
    from data.users import load_user_data, save_user_data
    print("✅ User data functions imported successfully")
    
    # Test loading user data
    print("\nTesting user data loading...")
    users_data = load_user_data()
    print(f"✅ Loaded {len(users_data)} users")
    
    # Check user 'ola' specifically
    print("\nTesting user 'ola'...")
    ola_data = users_data.get('ola', {})
    if ola_data:
        print(f"✅ User 'ola' found")
        print(f"  - test_taken: {ola_data.get('test_taken', False)}")
        print(f"  - neuroleader_type: {ola_data.get('neuroleader_type', 'None')}")
        print(f"  - current badges: {ola_data.get('badges', [])}")
        
        # Test badge conditions manually
        print("\nTesting badge conditions for 'ola'...")
        
        # Starter badge - should get if no badges
        if not ola_data.get('badges', []):
            print("  - Eligible for 'starter' badge (no current badges)")
        
        # Tester badge - should get if has test data
        if ola_data.get('neuroleader_type') or ola_data.get('degen_type'):
            print("  - Eligible for 'tester' badge (has test results)")
        
        # Manually award starter and tester badges
        print("\nManually awarding badges...")
        if 'badges' not in ola_data:
            ola_data['badges'] = []
            
        badges_to_add = []
        if 'starter' not in ola_data['badges']:
            badges_to_add.append('starter')
        if 'tester' not in ola_data['badges'] and (ola_data.get('neuroleader_type') or ola_data.get('degen_type')):
            badges_to_add.append('tester')
            
        if badges_to_add:
            print(f"  Adding badges: {badges_to_add}")
            ola_data['badges'].extend(badges_to_add)
            users_data['ola'] = ola_data
            
            # Save the data
            save_user_data(users_data)
            print("  ✅ Badges saved to user data")
            
            # Verify the save
            updated_data = load_user_data()
            updated_ola = updated_data.get('ola', {})
            print(f"  ✅ Verified: User 'ola' now has badges: {updated_ola.get('badges', [])}")
        else:
            print("  ℹ️ No new badges to add")
    else:
        print("❌ User 'ola' not found")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Direct badge test completed!")
