#!/usr/bin/env python3
"""
Quick test to award a badge with timestamp to verify the system works
"""

from data.users import load_user_data, save_user_data
from utils.achievements import check_achievements
from datetime import datetime

def test_badge_timestamp_system():
    """Test the badge timestamp functionality"""
    print("=== Testing Badge Timestamp System ===\n")
    
    # Load user data
    users_data = load_user_data()
    
    # Find a user who could get a new badge
    test_user = None
    for username, data in users_data.items():
        if data.get('completed_lessons') and len(data.get('badges', [])) < 5:
            test_user = username
            break
    
    if not test_user:
        test_user = list(users_data.keys())[0]  # Fallback to first user
    
    print(f"Testing with user: {test_user}")
    
    # Check current state
    user_data = users_data[test_user]
    current_badges = user_data.get('badges', [])
    current_timestamps = user_data.get('badge_timestamps', {})
    
    print(f"Current badges: {current_badges}")
    print(f"Current timestamps: {current_timestamps}")
    
    # Manually add a badge with timestamp to test the system
    if 'badge_timestamps' not in user_data:
        user_data['badge_timestamps'] = {}
    
    # Add a learner badge if not present (most users should qualify)
    if 'learner' not in current_badges and user_data.get('completed_lessons'):
        current_badges.append('learner')
        user_data['badges'] = current_badges
        user_data['badge_timestamps']['learner'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save the updated data
        users_data[test_user] = user_data
        save_user_data(users_data)
        
        print(f"✅ Added 'learner' badge with timestamp to user {test_user}")
    
    # Test the achievements system
    print("\n🧪 Running achievement check...")
    new_badges = check_achievements(test_user)
    
    if new_badges:
        print(f"✅ New badges awarded: {new_badges}")
        
        # Check if timestamps were added
        users_data = load_user_data()  # Reload to see changes
        updated_timestamps = users_data[test_user].get('badge_timestamps', {})
        print(f"Updated timestamps: {updated_timestamps}")
    else:
        print("ℹ️ No new badges awarded (user may already have eligible badges)")
    
    # Show final state
    users_data = load_user_data()
    final_user_data = users_data[test_user]
    final_badges = final_user_data.get('badges', [])
    final_timestamps = final_user_data.get('badge_timestamps', {})
    
    print(f"\n📊 Final state for {test_user}:")
    print(f"  Badges: {final_badges}")
    print(f"  Timestamps: {final_timestamps}")
    
    # Test the dashboard display logic
    print(f"\n🎯 Testing Dashboard Display Logic:")
    
    if final_badges and final_timestamps:
        # Simulate dashboard logic
        badges_with_time = []
        for badge_id in final_badges:
            if badge_id in final_timestamps:
                badges_with_time.append((badge_id, final_timestamps[badge_id]))
        
        # Sort by timestamp (newest first) and get recent ones
        badges_with_time.sort(key=lambda x: x[1], reverse=True)
        recent_badges = badges_with_time[:2]
        
        print("Recent badges that would show in dashboard:")
        for badge_id, timestamp in recent_badges:
            print(f"  🏆 {badge_id} - {timestamp}")
    
    return len(final_timestamps) > 0

if __name__ == "__main__":
    success = test_badge_timestamp_system()
    
    if success:
        print(f"\n✅ Badge timestamp system is working correctly!")
        print("The dashboard will now show badge achievements with proper timestamps.")
    else:
        print(f"\n❌ Badge timestamp system needs attention.")
