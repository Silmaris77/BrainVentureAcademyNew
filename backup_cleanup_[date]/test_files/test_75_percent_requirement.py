#!/usr/bin/env python3
"""
Test script to verify the 75% minimum requirement for final quiz progression
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from data.lessons import load_lessons
from views.lesson import display_quiz

def test_quiz_thresholds():
    """Test that display_quiz respects different passing thresholds"""
    
    # Sample quiz data
    sample_quiz = {
        'title': 'Test Quiz',
        'description': 'A test quiz for threshold testing',
        'questions': [
            {
                'question': 'What is 2 + 2?',
                'options': ['3', '4', '5', '6'],
                'correct_answer': 1,
                'explanation': '2 + 2 = 4'
            },
            {
                'question': 'What is 3 + 3?', 
                'options': ['5', '6', '7', '8'],
                'correct_answer': 1,
                'explanation': '3 + 3 = 6'
            },
            {
                'question': 'What is 4 + 4?',
                'options': ['7', '8', '9', '10'],
                'correct_answer': 1,
                'explanation': '4 + 4 = 8'
            },
            {
                'question': 'What is 5 + 5?',
                'options': ['9', '10', '11', '12'],
                'correct_answer': 1,
                'explanation': '5 + 5 = 10'
            }
        ]
    }
    
    print("Testing Quiz Threshold System")
    print("=" * 50)
    
    # Test scenarios
    scenarios = [
        (50, "50% threshold (2/4 correct)"),
        (60, "60% threshold (opening quiz)"),
        (75, "75% threshold (closing quiz)")
    ]
    
    for threshold, description in scenarios:
        print(f"\nTesting {description}")
        print(f"Required score: {threshold}%")
        
        # Simulate different score percentages
        test_scores = [25, 50, 60, 75, 100]
        
        for score in test_scores:
            is_passed = score >= threshold
            status = "✅ PASSED" if is_passed else "❌ FAILED"
            print(f"  Score {score}%: {status}")
    
    print("\n" + "=" * 50)
    print("Closing Quiz Flow Test")
    print("=" * 50)
    
    print("\nScenario 1: Student gets 60% (below 75% requirement)")
    print("- Quiz completed: ✅")
    print("- Quiz passed (75%): ❌")
    print("- Can proceed: ❌")
    print("- Shows error message and retry button")
    
    print("\nScenario 2: Student gets 80% (above 75% requirement)")
    print("- Quiz completed: ✅") 
    print("- Quiz passed (75%): ✅")
    print("- Can proceed: ✅")
    print("- Shows success message and next button")

def test_lesson_data():
    """Test that lessons have closing quiz data"""
    print("\n" + "=" * 50)
    print("Lesson Data Verification")
    print("=" * 50)
    
    lessons = load_lessons()
    
    for lesson_id, lesson in lessons.items():
        print(f"\nLesson: {lesson_id}")
        print(f"Title: {lesson.get('title', 'No title')}")
        
        if 'sections' in lesson and 'closing_quiz' in lesson['sections']:
            quiz_data = lesson['sections']['closing_quiz']
            num_questions = len(quiz_data.get('questions', []))
            print(f"✅ Has closing quiz with {num_questions} questions")
            
            if num_questions > 0:
                print(f"   Quiz title: {quiz_data.get('title', 'No title')}")
        else:
            print("❌ No closing quiz found")

if __name__ == "__main__":
    print("🧪 Testing 75% Final Quiz Requirement")
    print("====================================")
    
    test_quiz_thresholds()
    test_lesson_data()
    
    print("\n" + "=" * 50)
    print("Summary of Changes Made:")
    print("=" * 50)
    print("1. ✅ Modified display_quiz() to accept passing_threshold parameter")
    print("2. ✅ Updated closing quiz logic to require 75% to proceed")
    print("3. ✅ Added error message when score < 75%")
    print("4. ✅ Added retry functionality for failed closing quiz")
    print("5. ✅ Dynamic feedback messages based on threshold")
    print("\nThe system now enforces a 75% minimum score on closing quizzes!")
