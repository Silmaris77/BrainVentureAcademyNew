#!/usr/bin/env python3
"""
Final comprehensive test for the badge system integration
This script tests the complete badge awarding functionality using the standalone config.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # Import standalone badge configuration (no streamlit dependency)
    from config.badges import BADGES
    print(f"✅ Successfully loaded standalone badge config: {len(BADGES)} badges")
except ImportError as e:
    print(f"❌ Failed to import standalone badge config: {e}")
    sys.exit(1)

def load_users_data():
    """Load current users data"""
    try:
        with open('users_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading users data: {e}")
        return {}

def check_achievements_standalone(username, user_data):
    """
    Standalone version of check_achievements function that doesn't depend on streamlit
    """
    new_badges = []
    current_badges = user_data.get('badges', [])
    
    # Helper function to check conditions
    def award_badge_if_eligible(badge_id, badge_info):
        if badge_id in current_badges:
            return False
            
        conditions = badge_info.get('conditions', {})
        
        # Check XP condition
        if 'min_xp' in conditions:
            if user_data.get('xp', 0) < conditions['min_xp']:
                return False
        
        # Check level condition
        if 'min_level' in conditions:
            if user_data.get('level', 1) < conditions['min_level']:
                return False
        
        # Check test completion
        if conditions.get('test_completed', False):
            if not user_data.get('test_taken', False):
                return False
        
        # Check lessons completed
        if 'min_lessons' in conditions:
            lessons_count = len(user_data.get('completed_lessons', []))
            if lessons_count < conditions['min_lessons']:
                return False
        
        # Check specific neuroleader type
        if 'neuroleader_type' in conditions:
            required_type = conditions['neuroleader_type']
            user_type = user_data.get('neuroleader_type')
            if user_type != required_type:
                return False
        
        # Check join date for time-based badges
        if 'join_before' in conditions:
            join_date_str = user_data.get('joined_date')
            if join_date_str:
                try:
                    join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
                    cutoff_date = datetime.strptime(conditions['join_before'], '%Y-%m-%d')
                    if join_date >= cutoff_date:
                        return False
                except:
                    return False
        
        # All conditions met
        return True
    
    # Check all badges
    for badge_id, badge_info in BADGES.items():
        if award_badge_if_eligible(badge_id, badge_info):
            new_badges.append(badge_id)
    
    return new_badges

def test_badge_system():
    """Test the complete badge system"""
    print("\n🔍 Testing Badge System Integration")
    print("=" * 50)
    
    # Load current data
    users_data = load_users_data()
    if not users_data:
        print("❌ No users data found")
        return
    
    print(f"📊 Found {len(users_data)} users in database\n")
    
    # Test specific users with test completion
    test_users = [
        'ola',  # Recently added, Neuroinnowator
        'a',    # Has badges already
        'b',    # Neuroreaktor with badges
        'c',    # Neuroinspirator with badges
        'q',    # Neuroreaktor
        'x',    # Neuroreaktor
        'zx',   # Neuroreaktor with night_owl badge
    ]
    
    for username in test_users:
        if username not in users_data:
            print(f"⚠️  User '{username}' not found in database")
            continue
            
        user_data = users_data[username]
        current_badges = user_data.get('badges', [])
        test_taken = user_data.get('test_taken', False)
        neuroleader_type = user_data.get('neuroleader_type')
        xp = user_data.get('xp', 0)
        level = user_data.get('level', 1)
        lessons_count = len(user_data.get('completed_lessons', []))
        
        print(f"👤 User: {username}")
        print(f"   📊 Stats: XP={xp}, Level={level}, Lessons={lessons_count}")
        print(f"   🧠 Type: {neuroleader_type}")
        print(f"   ✅ Test taken: {test_taken}")
        print(f"   🏆 Current badges: {current_badges}")
        
        # Test badge checking
        new_badges = check_achievements_standalone(username, user_data)
        
        if new_badges:
            print(f"   🆕 New badges eligible: {new_badges}")
        else:
            print(f"   ℹ️  No new badges eligible")
        
        # Check for specific badges that should exist
        expected_badges = []
        if test_taken:
            expected_badges.append('tester')
        if xp > 0:
            expected_badges.append('starter')
        if neuroleader_type:
            # Check for type-specific badges
            type_badge_map = {
                'Neuroinnowator': 'innovator',
                'Neuroreaktor': 'reactor', 
                'Neuroinspirator': 'inspirator',
                'Neuroanalityk': 'analyst',
                'Neuroempata': 'empath',
                'Neurobalanser': 'balancer'
            }
            if neuroleader_type in type_badge_map:
                expected_badges.append(type_badge_map[neuroleader_type])
        
        missing_expected = [badge for badge in expected_badges if badge not in current_badges and badge not in new_badges]
        if missing_expected:
            print(f"   ⚠️  Missing expected badges: {missing_expected}")
        
        print()
    
    # Test badge condition logic
    print("\n🧪 Testing Badge Condition Logic")
    print("=" * 40)
    
    # Test specific badge conditions
    test_badge_conditions = [
        ('starter', {'min_xp': 1}),
        ('tester', {'test_completed': True}),
        ('innovator', {'neuroleader_type': 'Neuroinnowator', 'test_completed': True}),
        ('reactor', {'neuroleader_type': 'Neuroreaktor', 'test_completed': True}),
        ('learner', {'min_lessons': 1}),
        ('achiever', {'min_xp': 1000}),
    ]
    
    for badge_id, conditions in test_badge_conditions:
        if badge_id in BADGES:
            badge_info = BADGES[badge_id]
            print(f"🏆 {badge_id}: {badge_info.get('name', badge_id)}")
            print(f"   📋 Expected conditions: {conditions}")
            print(f"   📋 Actual conditions: {badge_info.get('conditions', {})}")
            
            # Check if conditions match
            actual_conditions = badge_info.get('conditions', {})
            matches = all(actual_conditions.get(k) == v for k, v in conditions.items())
            print(f"   ✅ Conditions match: {matches}")
        else:
            print(f"❌ Badge '{badge_id}' not found in BADGES")
        print()

def test_integration_points():
    """Test the integration points where badges should be awarded"""
    print("\n🔗 Testing Integration Points")
    print("=" * 35)
    
    integration_files = [
        'views/degen_test.py',
        'views/neuroleader_explorer.py',
        'views/degen_explorer.py', 
        'views/degen_types.py',
        'views/degen_test_new.py'
    ]
    
    for file_path in integration_files:
        full_path = Path(file_path)
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_check_achievements = 'check_achievements' in content
                has_import = 'from utils.achievements import check_achievements' in content
                has_error_handling = 'try:' in content and 'check_achievements' in content
                
                print(f"📁 {file_path}")
                print(f"   ✅ Has check_achievements call: {has_check_achievements}")
                print(f"   ✅ Has proper import: {has_import}")
                print(f"   ✅ Has error handling: {has_error_handling}")
                
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
        else:
            print(f"❌ File not found: {file_path}")
        print()

if __name__ == "__main__":
    print("🚀 BrainVenture Academy Badge System Test")
    print("=" * 45)
    
    test_badge_system()
    test_integration_points()
    
    print("\n✅ Badge system test completed!")
    print("\nNext steps:")
    print("1. Run the live application and complete a test")
    print("2. Check if badges are automatically awarded")
    print("3. Verify badge display in user profile")
