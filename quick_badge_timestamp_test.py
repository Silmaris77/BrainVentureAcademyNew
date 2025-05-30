#!/usr/bin/env python3

from utils.achievements import check_achievements
from data.users import load_user_data, save_user_data
from datetime import datetime

# Test badge timestamps
users_data = load_user_data()
test_user = 'a'  # User with most activity

print(f'Testing with user: {test_user}')
user_data = users_data.get(test_user, {})
print(f'Current badges: {user_data.get("badges", [])}')
print(f'Badge timestamps: {user_data.get("badge_timestamps", {})}')

# Add timestamp to existing badges if missing
if 'badge_timestamps' not in user_data:
    user_data['badge_timestamps'] = {}
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for badge in user_data.get('badges', []):
        user_data['badge_timestamps'][badge] = current_time
    
    users_data[test_user] = user_data
    save_user_data(users_data)
    print('Added timestamps to existing badges')

print('Testing new badge award...')
new_badges = check_achievements(test_user)
print(f'New badges: {new_badges}')

# Check final state
users_data = load_user_data()
final_user_data = users_data[test_user]
print(f'Final badges: {final_user_data.get("badges", [])}')
print(f'Final timestamps: {final_user_data.get("badge_timestamps", {})}')
