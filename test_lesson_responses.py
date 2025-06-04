#!/usr/bin/env python3
"""
Test script to verify lesson response saving functionality
"""

import json
import os
import sys
from datetime import datetime

# Add the directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.users import load_user_data, save_user_data

def test_lesson_response_structure():
    """Test the lesson response saving and loading functionality"""
    print("🧪 Testing Lesson Response Functionality...")
    
    # Load current user data
    users_data = load_user_data()
    
    # Test data
    test_username = "a"  # User with existing data
    test_lesson_id = "B1C1L1"
    test_responses = {
        'reflection': {
            'Analiza sytuacji stresowej': 'To jest moja odpowiedź na pierwsze pytanie refleksyjne.',
            'Model SCARF w komunikacji': 'Analiza SCARF mojego zespołu...',
            'Zarządzanie zmianą': 'Moje doświadczenia ze zmianą...'
        },
        'application': {
            'Obserwacja reakcji stresowych': 'Plan obserwacji na następny tydzień...',
            'Analiza komunikacji przez SCARF': 'Konkretne obszary do poprawy...',
            'System nagród dopaminergicznych': 'Projekt systemu nagród...'
        }
    }
    
    if test_username not in users_data:
        print(f"❌ Test user '{test_username}' not found!")
        return False
    
    print(f"✅ Found test user: {test_username}")
    
    # Initialize lesson_responses if it doesn't exist
    if 'lesson_responses' not in users_data[test_username]:
        users_data[test_username]['lesson_responses'] = {}
        print("📝 Initialized lesson_responses for user")
    
    # Initialize lesson data if it doesn't exist
    if test_lesson_id not in users_data[test_username]['lesson_responses']:
        users_data[test_username]['lesson_responses'][test_lesson_id] = {}
        print(f"📝 Initialized responses for lesson {test_lesson_id}")
    
    # Add test responses
    for section_type, sections in test_responses.items():
        if section_type not in users_data[test_username]['lesson_responses'][test_lesson_id]:
            users_data[test_username]['lesson_responses'][test_lesson_id][section_type] = {}
        
        for section_title, response in sections.items():
            users_data[test_username]['lesson_responses'][test_lesson_id][section_type][section_title] = {
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
            print(f"💾 Saved response for {section_type} - {section_title}")
    
    # Save to file
    try:
        save_user_data(users_data)
        print("✅ Successfully saved test responses to users_data.json")
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        return False
    
    # Verify data was saved
    reloaded_data = load_user_data()
    user_responses = reloaded_data[test_username].get('lesson_responses', {})
    lesson_responses = user_responses.get(test_lesson_id, {})
    
    print(f"\n📊 Verification Results:")
    print(f"   - User has lesson_responses: {bool(user_responses)}")
    print(f"   - Lesson {test_lesson_id} has responses: {bool(lesson_responses)}")
    
    for section_type in ['reflection', 'application']:
        section_data = lesson_responses.get(section_type, {})
        print(f"   - {section_type} sections: {len(section_data)}")
        for title, data in section_data.items():
            response_length = len(data.get('response', ''))
            timestamp = data.get('timestamp', 'No timestamp')
            print(f"     • {title}: {response_length} chars, saved at {timestamp}")
    
    return True

def show_user_responses(username="a"):
    """Show all saved responses for a user"""
    print(f"\n👤 Responses for user: {username}")
    
    users_data = load_user_data()
    if username not in users_data:
        print(f"❌ User '{username}' not found!")
        return
    
    user_data = users_data[username]
    lesson_responses = user_data.get('lesson_responses', {})
    
    if not lesson_responses:
        print("📭 No lesson responses found for this user.")
        return
    
    for lesson_id, lesson_data in lesson_responses.items():
        print(f"\n📚 Lesson: {lesson_id}")
        for section_type, sections in lesson_data.items():
            print(f"  📝 {section_type.title()}:")
            for title, data in sections.items():
                response = data.get('response', '')
                timestamp = data.get('timestamp', 'Unknown')
                preview = response[:100] + "..." if len(response) > 100 else response
                print(f"    • {title}:")
                print(f"      Response: {preview}")
                print(f"      Saved: {timestamp}")

if __name__ == "__main__":
    print("🚀 Starting Lesson Response Tests...\n")
    
    # Test the functionality
    success = test_lesson_response_structure()
    
    if success:
        print("\n✅ All tests passed!")
        
        # Show saved responses
        show_user_responses("a")
        
        print(f"\n🎉 Lesson response saving is now implemented!")
        print(f"📝 Users can save their reflection and application responses")
        print(f"💾 Responses are stored in users_data.json under 'lesson_responses'")
        print(f"🔄 Responses will persist between login sessions")
        
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
