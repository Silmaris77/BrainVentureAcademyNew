#!/usr/bin/env python3
import json
import sys
import traceback

try:
    # Load user data
    with open('users_data.json', 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    # Check user 'a' data
    user_a = users_data.get('a', {})
    print('=== User A Data ===')
    print(f'neuroleader_type: {user_a.get("neuroleader_type", "NOT FOUND")}')
    print(f'degen_type: {user_a.get("degen_type", "NOT FOUND")}')
    print(f'test_taken: {user_a.get("test_taken", "NOT FOUND")}')
    print(f'has test_scores: {"test_scores" in user_a}')
    
    if 'test_scores' in user_a:
        print(f'test_scores: {user_a["test_scores"]}')
    
    # Simulate the profile tab logic
    neuroleader_type = user_a.get('neuroleader_type') or user_a.get('degen_type')
    test_taken = user_a.get('test_taken', False)
    has_test_scores = 'test_scores' in user_a
    
    print('\n=== Profile Tab Logic ===')
    print(f'Final neuroleader_type: {neuroleader_type}')
    print(f'test_taken: {test_taken}')
    print(f'has_test_scores: {has_test_scores}')
    print(f'Should show results: {neuroleader_type and (test_taken or has_test_scores)}')
    
    # Test if imports work
    print('\n=== Testing Imports ===')
    try:
        from data.neuroleader_details import degen_details
        print(f'degen_details import: OK')
        print(f'Has {neuroleader_type} in degen_details: {neuroleader_type in degen_details if neuroleader_type else "N/A"}')
    except Exception as e:
        print(f'degen_details import failed: {e}')
    
    try:
        from views.degen_test import plot_radar_chart
        print(f'plot_radar_chart import: OK')
    except Exception as e:
        print(f'plot_radar_chart import failed: {e}')
    
    # Test NEUROLEADER_TYPES
    try:
        from data.test_questions import NEUROLEADER_TYPES
        print(f'NEUROLEADER_TYPES import: OK')
        print(f'Has {neuroleader_type} in NEUROLEADER_TYPES: {neuroleader_type in NEUROLEADER_TYPES if neuroleader_type else "N/A"}')
        print(f'Available types: {list(NEUROLEADER_TYPES.keys())}')
    except Exception as e:
        print(f'NEUROLEADER_TYPES import failed: {e}')
    
    # Test config.settings import
    try:
        from config.settings import NEUROLEADER_TYPES as CONFIG_NEUROLEADER_TYPES
        print(f'config.settings NEUROLEADER_TYPES import: OK')
        print(f'Has {neuroleader_type} in config NEUROLEADER_TYPES: {neuroleader_type in CONFIG_NEUROLEADER_TYPES if neuroleader_type else "N/A"}')
        print(f'Config available types: {list(CONFIG_NEUROLEADER_TYPES.keys())}')
    except Exception as e:
        print(f'config NEUROLEADER_TYPES import failed: {e}')
    
except Exception as e:
    print(f'Error: {e}')
    traceback.print_exc()
