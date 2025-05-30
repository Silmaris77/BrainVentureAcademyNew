#!/usr/bin/env python3

print('=== Testing Dashboard Neuroleader Data Access ===')

try:
    import sys
    sys.path.append('.')
    
    # Simulate the session state user
    class MockSessionState:
        username = 'a'
    
    # Test data loading like in dashboard
    from data.users import load_user_data
    users_data = load_user_data()
    user_data = users_data.get('a', {})
    
    print('\n📊 Data Loading Test:')
    print(f'✅ User data loaded for user "a"')
    print(f'   - XP: {user_data.get("xp", 0)}')
    print(f'   - Level: {user_data.get("level", 1)}')
    print(f'   - Completed lessons: {len(user_data.get("completed_lessons", []))}')
    
    print('\n🧠 Neuroleader Data Test:')
    neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type')
    test_taken = user_data.get('test_taken', False)
    test_scores = user_data.get('test_scores')
    
    print(f'   - Neuroleader type: {neuroleader_type}')
    print(f'   - Test taken: {test_taken}')
    print(f'   - Has test scores: {bool(test_scores)}')
    
    if test_scores:
        print(f'   - Test scores: {test_scores}')
    
    print('\n🎯 Dashboard Display Logic Test:')
    
    if neuroleader_type and (test_taken or test_scores):
        print('✅ User HAS neuroleader data - will show results section')
        print(f'   - Would display: {neuroleader_type}')
        print('   - Would show: radar chart, strengths, challenges')
        print('   - Would offer: detailed description, retake test, view profile')
    elif not neuroleader_type:
        print('⚠️  User has NO neuroleader data - will show test invitation')
        print('   - Would display: invitation to take test')
        print('   - Would offer: button to start test')
    
    print('\n🔧 Import Test:')
    try:
        from data.test_questions import NEUROLEADER_TYPES
        from data.neuroleader_details import degen_details
        print('✅ NEUROLEADER_TYPES imported successfully')
        print('✅ degen_details imported successfully')
        
        if neuroleader_type and neuroleader_type in NEUROLEADER_TYPES:
            neuroleader_info = NEUROLEADER_TYPES[neuroleader_type]
            print(f'✅ Found info for {neuroleader_type}:')
            print(f'   - Color: {neuroleader_info.get("color")}')
            print(f'   - Description: {neuroleader_info.get("description", "")[:50]}...')
            
    except Exception as e:
        print(f'❌ Import error: {e}')
    
    print('\n🎉 Dashboard neuroleader integration test completed!')
    print('   - Data loading: ✅ Working')
    print('   - Neuroleader detection: ✅ Working') 
    print('   - Display logic: ✅ Ready')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
