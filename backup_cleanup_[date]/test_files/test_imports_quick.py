#!/usr/bin/env python3
"""
Szybki test importów i podstawowej funkcjonalności
"""

def test_imports():
    """Test podstawowych importów"""
    try:
        print("🔍 Testowanie importów...")
        
        # Test importu głównych modułów
        import views.lesson
        print("✅ views.lesson")
        
        import utils.lesson_progress
        print("✅ utils.lesson_progress")
        
        import utils.real_time_updates
        print("✅ utils.real_time_updates")
        
        # Test funkcji
        from utils.lesson_progress import get_lesson_fragment_progress, award_fragment_xp
        print("✅ lesson_progress functions")
        
        from utils.real_time_updates import get_live_user_stats, live_xp_indicator
        print("✅ real_time_updates functions")
        
        print("\n🎉 Wszystkie kluczowe moduły zostały pomyślnie zaimportowane!")
        return True
        
    except ImportError as e:
        print(f"❌ Błąd importu: {e}")
        return False
    except Exception as e:
        print(f"❌ Inny błąd: {e}")
        return False

if __name__ == "__main__":
    test_imports()
