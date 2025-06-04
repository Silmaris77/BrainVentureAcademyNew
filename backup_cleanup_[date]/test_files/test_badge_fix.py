#!/usr/bin/env python3
"""
Test script to verify badge categories fix
"""

from config.settings import BADGES

# Define the badge categories exactly as they are in profile.py
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

def test_badge_categories():
    """Test if all badge categories reference valid badges"""
    print("🔍 Testing Badge Categories Fix...")
    print("=" * 50)
    
    total_badges = 0
    missing_badges = []
    
    for category, category_data in badge_categories.items():
        print(f"\n{category}")
        print(f"📝 {category_data['description']}")
        print(f"📊 Badges in category: {len(category_data['badges'])}")
        
        valid_badges = 0
        for badge_id in category_data['badges']:
            if badge_id in BADGES:
                valid_badges += 1
                print(f"  ✅ {badge_id}: {BADGES[badge_id]['name']}")
            else:
                missing_badges.append((category, badge_id))
                print(f"  ❌ {badge_id}: MISSING!")
        
        total_badges += len(category_data['badges'])
        print(f"   Valid: {valid_badges}/{len(category_data['badges'])}")
    
    print("\n" + "=" * 50)
    print(f"📊 SUMMARY:")
    print(f"   Total categories: {len(badge_categories)}")
    print(f"   Total badges referenced: {total_badges}")
    print(f"   Total badges in BADGES config: {len(BADGES)}")
    print(f"   Missing badges: {len(missing_badges)}")
    
    if missing_badges:
        print(f"\n❌ MISSING BADGES:")
        for category, badge_id in missing_badges:
            print(f"   - {badge_id} (in {category})")
        return False
    else:
        print(f"\n✅ ALL BADGES VALID!")
        print(f"✅ Badge categories fix is working correctly!")
        return True

if __name__ == "__main__":
    success = test_badge_categories()
    exit(0 if success else 1)
