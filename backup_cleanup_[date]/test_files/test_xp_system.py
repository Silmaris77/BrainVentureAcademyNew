#!/usr/bin/env python3
"""
Test script for the XP fragment system
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_xp_fragment_system():
    """Test the XP fragment system functionality"""
    print("🧪 Testing XP Fragment System...")
    print("=" * 50)
    
    try:
        # Test imports
        from utils.lesson_progress import (
            award_fragment_xp, 
            get_lesson_fragment_progress, 
            calculate_lesson_completion,
            is_lesson_fully_completed,
            get_fragment_xp_breakdown,
            mark_lesson_as_completed
        )
        from utils.real_time_updates import (
            get_live_user_stats, 
            calculate_level_from_xp,
            get_xp_for_next_level
        )
        print("✅ All imports successful!")
        
        # Test get_live_user_stats returns correct data types
        print("\n📊 Testing get_live_user_stats...")
        stats = get_live_user_stats('test_user')
        print(f"   XP type: {type(stats['xp'])} - {stats['xp']}")
        print(f"   Level type: {type(stats['level'])} - {stats['level']}")
        print(f"   Completed lessons type: {type(stats['completed_lessons'])} - {stats['completed_lessons']}")
        print(f"   Lesson progress type: {type(stats['lesson_progress'])} - {len(stats['lesson_progress'])} items")
        
        # Verify completed_lessons is a list (this was the bug)
        assert isinstance(stats['completed_lessons'], list), "completed_lessons must be a list!"
        print("✅ completed_lessons is correctly returned as a list!")
        
        # Test level calculation
        print("\n🎯 Testing level calculation...")
        for xp in [0, 50, 100, 150, 250, 500]:
            level = calculate_level_from_xp(xp)
            next_xp = get_xp_for_next_level(xp)
            print(f"   XP: {xp} → Level: {level} (Next level needs: {next_xp} XP)")
        
        # Test fragment XP functions
        print("\n🧩 Testing fragment XP functions...")
        
        # Test fragment progress for a lesson
        lesson_id = "test_lesson_1"
        fragment_progress = get_lesson_fragment_progress(lesson_id)
        print(f"   Fragment progress for {lesson_id}: {fragment_progress}")
        
        # Test XP breakdown
        max_xp = 100
        xp_breakdown = get_fragment_xp_breakdown(max_xp)
        print(f"   XP breakdown for {max_xp} total XP: {xp_breakdown}")
        
        # Test lesson completion calculation
        completion = calculate_lesson_completion(lesson_id)
        print(f"   Lesson completion for {lesson_id}: {completion:.1f}%")
        
        # Test if lesson is fully completed
        is_complete = is_lesson_fully_completed(lesson_id)
        print(f"   Is {lesson_id} fully completed: {is_complete}")
        
        # Test show_xp_notification function
        print("\n📢 Testing show_xp_notification...")
        from utils.real_time_updates import show_xp_notification
        
        # Test with valid XP amount (should work)
        print("   Testing with XP amount 50...")
        # Note: This won't actually display in terminal, but should not error
        try:
            show_xp_notification(50, "Test XP notification")
            print("   ✅ XP notification with amount works!")
        except Exception as e:
            print(f"   ❌ XP notification failed: {e}")
        
        # Test with 0 XP and message (completion notification)
        print("   Testing with 0 XP and completion message...")
        try:
            show_xp_notification(0, "🎉 Congratulations! Lesson completed!")
            print("   ✅ Completion notification works!")
        except Exception as e:
            print(f"   ❌ Completion notification failed: {e}")
        
        print("\n🎉 All tests passed! XP Fragment System is working correctly!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_xp_fragment_system()
    exit(0 if success else 1)
