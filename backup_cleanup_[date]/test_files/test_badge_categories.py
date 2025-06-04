#!/usr/bin/env python3
"""
Test wyświetlania odznak z kategoriami i opisami
"""

import sys
sys.path.append(r'c:\Users\pksia\Dropbox\Brainventure - kurs\B2\BrainVentureAcademyNew')

def test_badge_categories():
    """Test struktury kategorii odznak"""
    
    # Struktura kategorii jak w profile.py
    badge_categories = {
        "📚 Podstawowe": {
            "description": "Start w neuroleaderstwie",
            "badges": ["starter", "tester", "learner", "consistent", "social"]
        },
        "🧠 Kompetencje Przywódcze": {
            "description": "EQ, decyzje, zespoły, zmiany, komunikacja",
            "badges": ["emotional_intelligence", "decision_maker", "team_builder", 
                      "change_leader", "communication_expert"]
        },
        "📈 Rozwój Osobisty": {
            "description": "Systematyczność i efektywność nauki",
            "badges": ["streak_master", "daily_hero", "weekend_warrior", "knowledge_seeker", 
                      "quick_learner", "night_owl", "early_bird"]
        },
        "👨‍🏫 Mentoring i Coaching": {
            "description": "Rozwój innych liderów",
            "badges": ["mentor", "coach", "team_developer", "culture_builder"]
        },
        "🏆 Osiągnięcia": {
            "description": "Sukcesy i ekspertyza",
            "badges": ["first_achievement", "collector", "perfectionist", "innovator"]
        },
        "🔍 Typy Neuroleaderów": {
            "description": "Samoświadomość i adaptacyjność",
            "badges": ["neuroleader_master", "self_aware", "adaptive_leader", "authentic_leader"]
        },
        "💼 Praktyka Biznesowa": {
            "description": "Zastosowanie w rzeczywistości",
            "badges": ["practitioner", "results_driven", "feedback_master"]
        },
        "🚀 Wyzwania Przywódcze": {
            "description": "Transformacja i innowacje",
            "badges": ["challenge_accepted", "challenge_master", "transformation_leader"]
        },
        "⭐ Specjalne": {
            "description": "Wizjonerstwo, empatia, resilience, mindfulness",
            "badges": ["visionary", "empathy_champion", "resilient_leader", "mindful_leader"]
        }
    }
    
    # Sprawdź strukturę
    print("🏆 TEST KATEGORII ODZNAK NEUROLEADERSKICH")
    print("=" * 50)
    
    total_badges = 0
    for category, data in badge_categories.items():
        print(f"\n{category}")
        print(f"📄 Opis: {data['description']}")
        print(f"🔢 Liczba odznak: {len(data['badges'])}")
        print(f"📋 Odznaki: {', '.join(data['badges'])}")
        total_badges += len(data['badges'])
    
    print(f"\n{'='*50}")
    print(f"📊 PODSUMOWANIE:")
    print(f"📂 Liczba kategorii: {len(badge_categories)}")
    print(f"🏆 Łączna liczba odznak: {total_badges}")
    
    # Sprawdź czy wszystkie odznaki z config.settings są uwzględnione
    try:
        from config.settings import BADGES
        
        all_category_badges = []
        for data in badge_categories.values():
            all_category_badges.extend(data['badges'])
        
        missing_badges = set(BADGES.keys()) - set(all_category_badges)
        extra_badges = set(all_category_badges) - set(BADGES.keys())
        
        if missing_badges:
            print(f"\n⚠️  BRAKUJĄCE ODZNAKI W KATEGORIACH: {missing_badges}")
        else:
            print(f"\n✅ Wszystkie odznaki z BADGES są uwzględnione w kategoriach")
            
        if extra_badges:
            print(f"\n⚠️  ODZNAKI W KATEGORIACH BEZ DEFINICJI: {extra_badges}")
        else:
            print(f"✅ Wszystkie odznaki w kategoriach mają definicje")
            
        print(f"\n🎯 Odznaki w config.settings: {len(BADGES)}")
        print(f"🎯 Odznaki w kategoriach: {len(all_category_badges)}")
        
    except ImportError as e:
        print(f"\n❌ Nie można zaimportować BADGES: {e}")
    
    return True

if __name__ == "__main__":
    test_badge_categories()
