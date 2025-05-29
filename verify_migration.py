#!/usr/bin/env python3
"""
Final Migration Verification Script
Verifies that the BrainVenture Academy migration from old "degen types" to new "neuroleader types" was successful.
"""

import json
import sys
import os

# Add path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_migration():
    """Verify the migration was successful"""
    print("=== BrainVenture Academy Migration Verification ===\n")
    
    # Load user data
    try:
        with open('users_data.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading user data: {e}")
        return False
    
    print(f"📊 Total users in system: {len(users_data)}")
    
    # Check migration status
    migrated_users = 0
    users_with_test_scores = 0
    old_type_issues = 0
    
    print("\n📋 User Migration Status:")
    print("-" * 60)
    
    for username, data in users_data.items():
        degen_type = data.get('degen_type')
        neuroleader_type = data.get('neuroleader_type')
        test_scores = data.get('test_scores', {})
        test_taken = data.get('test_taken', False)
        
        status = "✅" if test_taken else "⚪"
        
        print(f"{status} User '{username}':")
        print(f"   degen_type: {degen_type}")
        if neuroleader_type:
            print(f"   neuroleader_type: {neuroleader_type}")
        
        if test_scores:
            users_with_test_scores += 1
            # Check for old degen type keys in test_scores
            old_keys = [k for k in test_scores.keys() if 'Degen' in k]
            if old_keys:
                old_type_issues += 1
                print(f"   ⚠️  OLD KEYS FOUND: {old_keys}")
            else:
                print(f"   ✅ test_scores: {list(test_scores.keys())}")
        elif test_taken:
            print(f"   ⚠️  Test taken but no test_scores found")
        else:
            print(f"   ℹ️  No test taken")
        
        if test_taken:
            migrated_users += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print("📈 MIGRATION SUMMARY:")
    print("-" * 60)
    print(f"✅ Users who completed tests: {migrated_users}")
    print(f"📊 Users with test_scores: {users_with_test_scores}")
    print(f"⚠️  Users with old degen type keys: {old_type_issues}")
    
    # Check for specific successful migrations
    success_cases = []
    for username in ['a', 'b', 'c', 'x', 'zx']:
        if username in users_data:
            user = users_data[username]
            if (user.get('test_taken') and 
                user.get('test_scores') and 
                not any('Degen' in k for k in user.get('test_scores', {}).keys())):
                success_cases.append(username)
    
    print(f"✅ Successfully migrated users: {success_cases}")
    
    # Final verdict
    if old_type_issues == 0 and users_with_test_scores > 0:
        print("\n🎉 MIGRATION SUCCESSFUL!")
        print("   All test_scores use new neuroleader type keys.")
        print("   No old degen type keys found in test data.")
        return True
    else:
        print("\n❌ MIGRATION ISSUES DETECTED!")
        if old_type_issues > 0:
            print(f"   Found {old_type_issues} users with old degen type keys")
        return False

if __name__ == "__main__":
    success = verify_migration()
    sys.exit(0 if success else 1)
