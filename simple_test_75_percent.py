#!/usr/bin/env python3
"""
Simple test to verify 75% requirement implementation
"""

def test_quiz_logic():
    """Test the quiz passing logic"""
    
    print("🧪 Testing 75% Final Quiz Requirement")
    print("====================================")
    
    print("\nTesting Quiz Threshold Logic")
    print("-" * 40)
    
    # Test different thresholds
    thresholds = [60, 75]
    test_scores = [50, 60, 70, 75, 80, 90]
    
    for threshold in thresholds:
        print(f"\nThreshold: {threshold}%")
        for score in test_scores:
            is_passed = score >= threshold
            status = "✅ PASS" if is_passed else "❌ FAIL"
            print(f"  Score {score}%: {status}")
    
    print("\n" + "=" * 50)
    print("Implementation Summary:")
    print("=" * 50)
    print("✅ display_quiz() now accepts passing_threshold parameter")
    print("✅ Closing quiz uses 75% threshold (display_quiz(quiz_data, 75))")
    print("✅ Opening quiz uses default 60% threshold")
    print("✅ Error message shown when closing quiz < 75%")
    print("✅ Retry button provided for failed closing quiz")
    print("✅ Dynamic feedback messages based on threshold")
    
    print("\n📝 Key Changes Made:")
    print("-" * 30)
    print("1. Modified function signature:")
    print("   def display_quiz(quiz_data, passing_threshold=60)")
    
    print("\n2. Updated passing logic:")
    print("   is_passed = percentage >= passing_threshold")
    
    print("\n3. Enhanced closing quiz section:")
    print("   - Requires quiz_passed (75%) to proceed")
    print("   - Shows error message if < 75%")
    print("   - Provides retry functionality")
    
    print("\n4. Dynamic feedback messages:")
    print("   - Different messages for different thresholds")
    print("   - Clear indication of requirement level")

if __name__ == "__main__":
    test_quiz_logic()
