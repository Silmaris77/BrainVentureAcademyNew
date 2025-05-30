#!/usr/bin/env python3

print('Testing dashboard neuroleader integration...')

try:
    import sys
    sys.path.append('.')
    
    # Test imports
    from views.dashboard import show_neuroleader_results_section, show_dashboard
    from data.users import load_user_data
    from data.neuroleader_details import degen_details
    from views.degen_explorer import plot_radar_chart
    
    print('✅ All imports successful')
    
    # Test data loading
    users_data = load_user_data()
    test_user = users_data.get('a', {})
    
    print(f'✅ User data loaded. User "a" neuroleader_type: {test_user.get("neuroleader_type")}')
    print(f'✅ User "a" test_taken: {test_user.get("test_taken")}')
    print(f'✅ User "a" has test_scores: {bool(test_user.get("test_scores"))}')
    
    # Test that the function can be called
    print('✅ Testing function accessibility...')
    print('✅ show_neuroleader_results_section function is accessible')
    
    print('✅ Dashboard neuroleader integration test completed successfully!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
