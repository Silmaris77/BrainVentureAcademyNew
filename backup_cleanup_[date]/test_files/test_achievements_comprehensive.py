#!/usr/bin/env python3
"""
Test comprehensive badge algorithms implementation
"""

from utils.achievements import check_achievements
from data.users import load_user_data
from config.settings import BADGES

def test_badge_algorithms():
    """Test all badge algorithms"""
    
    # Test z użytkownikiem 'a' który ma najwięcej danych
    users_data = load_user_data()
    print('=== DANE UŻYTKOWNIKA A ===')
    user_a = users_data.get('a', {})
    print(f'XP: {user_a.get("xp", 0)}')
    print(f'Poziom: {user_a.get("level", 1)}')
    print(f'Ukończone lekcje: {len(user_a.get("completed_lessons", []))}')
    print(f'Typ neuroleadera: {user_a.get("neuroleader_type")}')
    print(f'Test wykonany: {user_a.get("test_taken", False)}')
    print(f'Obecne odznaki: {user_a.get("badges", [])}')
    
    print('\n=== SPRAWDZANIE ODZNAK ===')
    new_badges = check_achievements('a')
    print(f'Nowe odznaki: {new_badges}')
    
    # Sprawdź zaktualizowane dane
    users_data_updated = load_user_data()
    user_a_updated = users_data_updated.get('a', {})
    all_badges = user_a_updated.get("badges", [])
    print(f'Wszystkie odznaki po sprawdzeniu: {all_badges}')
    
    print('\n=== STATYSTYKI ODZNAK ===')
    print(f'Liczba dostępnych odznak: {len(BADGES)}')
    print(f'Liczba zdobytych odznak: {len(all_badges)}')
    print(f'Procent ukończenia: {(len(all_badges) / len(BADGES)) * 100:.1f}%')
    
    print('\n=== LISTA ZDOBYTYCH ODZNAK ===')
    for badge_id in all_badges:
        badge = BADGES.get(badge_id, {})
        print(f'• {badge.get("icon", "🏆")} {badge.get("name", badge_id)} - {badge.get("description", "Brak opisu")}')
    
    print('\n=== NIEZDOBYTE ODZNAKI ===')
    missing_badges = [badge_id for badge_id in BADGES.keys() if badge_id not in all_badges]
    for badge_id in missing_badges[:10]:  # Pokaż tylko pierwszych 10
        badge = BADGES.get(badge_id, {})
        print(f'• {badge.get("icon", "❌")} {badge.get("name", badge_id)} - {badge.get("description", "Brak opisu")}')
    
    if len(missing_badges) > 10:
        print(f'... i {len(missing_badges) - 10} więcej')
    
    print('\n=== TEST ZAKOŃCZONY ===')

if __name__ == "__main__":
    test_badge_algorithms()
