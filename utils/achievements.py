try:
    # Try to import from standalone config first (for testing)
    from config.badges import BADGES
except ImportError:
    # Fallback to settings config (for production)
    from config.settings import BADGES
    
from data.users import load_user_data, save_user_data
from datetime import datetime

def check_achievements(username):
    """Sprawdza osiągnięcia użytkownika i przyznaje nowe odznaki"""
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    user_badges = user_data.get("badges", [])
    new_badges = []
    # Sprawdź każdą odznakę, której użytkownik jeszcze nie ma
    for badge_id, badge in BADGES.items():
        if badge_id not in user_badges:
            # Sprawdź warunki dla poszczególnych odznak
            if badge_id == "starter" and not user_badges:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "tester" and (user_data.get("neuroleader_type") or user_data.get("degen_type")):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "learner" and user_data.get("completed_lessons"):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "consistent" and user_data.get("login_streak", 0) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            # Dodaj warunki dla nowych odznak neuroleaderskich            elif badge_id == "streak_master" and user_data.get("login_streak", 0) >= 10:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "daily_hero" and user_data.get("daily_missions_completed_in_day", 0) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "knowledge_seeker" and user_data.get("total_study_time", 0) >= 600:  # 10 godzin w minutach
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "quick_learner" and user_data.get("lessons_completed_today", 0) >= 3:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "neuroleader_master" and user_data.get("explorer_types_viewed", 0) >= 6:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "self_aware" and user_data.get("test_retaken", False):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "first_achievement" and len(user_badges) == 1:  # Po zdobyciu pierwszej odznaki
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "collector" and len(user_badges) >= 10:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "perfectionist" and user_data.get("perfect_quiz_score", False):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            # Odznaki socjalne
            elif badge_id == "social" and user_data.get("shared_profile", False):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki specjalistyczne neuroleaderstwa
            elif badge_id == "emotional_intelligence" and count_completed_eq_lessons(user_data) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "decision_maker" and count_completed_decision_lessons(user_data) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "team_builder" and count_completed_team_lessons(user_data) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "change_leader" and count_completed_change_lessons(user_data) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "communication_expert" and count_completed_communication_lessons(user_data) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki związane z aktywnością rozwoju
            elif badge_id == "weekend_warrior" and count_weekend_sessions(user_data) >= 4:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "night_owl" and has_late_night_session(user_data):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "early_bird" and has_early_morning_session(user_data):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki mentoringu i rozwoju innych
            elif badge_id == "mentor" and user_data.get("mentoring_sessions", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "coach" and user_data.get("coaching_sessions", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "team_developer" and user_data.get("team_members_developed", 0) >= 3:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "culture_builder" and user_data.get("culture_initiatives", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki osiągnięć i doskonalenia
            elif badge_id == "innovator" and user_data.get("innovation_proposals", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki typów neuroleaderów - rozszerzone
            elif badge_id == "adaptive_leader" and has_multi_type_development(user_data):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "authentic_leader" and user_data.get("authentic_leadership_score", 0) >= 80:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki zastosowania w praktyce
            elif badge_id == "practitioner" and user_data.get("business_applications", 0) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "results_driven" and user_data.get("measurable_results", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "feedback_master" and user_data.get("feedback_sessions", 0) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki wyzwań przywódczych
            elif badge_id == "challenge_accepted" and user_data.get("challenges_accepted", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "challenge_master" and user_data.get("challenges_completed", 0) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "transformation_leader" and user_data.get("transformations_led", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Odznaki specjalne
            elif badge_id == "visionary" and user_data.get("visions_created", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "empathy_champion" and user_data.get("empathy_score", 0) >= 90:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "resilient_leader" and user_data.get("resilience_challenges", 0) >= 1:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "mindful_leader" and user_data.get("mindfulness_practice_days", 0) >= 30:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
      # Zapisz aktualizację, jeśli przyznano nowe odznaki
    if new_badges:
        user_data["badges"] = user_badges
        
        # Dodaj timestampy dla nowych odznak
        if "badge_timestamps" not in user_data:
            user_data["badge_timestamps"] = {}
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for badge_id in new_badges:
            user_data["badge_timestamps"][badge_id] = current_time
        
        users_data[username] = user_data
        save_user_data(users_data)
        
        # Przyznaj XP za nowe odznaki
        xp_per_badge = 50
        total_xp = len(new_badges) * xp_per_badge
        add_xp(username, total_xp)
        
    return new_badges

def add_xp(username, xp_amount):
    """Dodaj XP użytkownikowi i sprawdź, czy awansował na nowy poziom"""
    from config.settings import XP_LEVELS
    
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    current_xp = user_data.get("xp", 0)
    current_level = user_data.get("level", 1)
    
    # Dodaj XP
    new_xp = current_xp + xp_amount
    user_data["xp"] = new_xp
    
    # Sprawdź, czy użytkownik awansował
    new_level = current_level
    for level, required_xp in sorted(XP_LEVELS.items()):
        if new_xp >= required_xp:
            new_level = level    
    # Jeśli jest nowy poziom, zaktualizuj
    if new_level > current_level:
        user_data["level"] = new_level
        users_data[username] = user_data
        save_user_data(users_data)
        return True, new_level
    
    # Zapisz dane
    users_data[username] = user_data
    save_user_data(users_data)
    return False, current_level

# Helper functions for badge conditions

def count_completed_eq_lessons(user_data):
    """Liczy ukończone lekcje z inteligencji emocjonalnej"""
    completed_lessons = user_data.get('completed_lessons', [])
    eq_lessons = [lesson for lesson in completed_lessons if 'eq' in str(lesson).lower() or 'emoc' in str(lesson).lower()]
    return len(eq_lessons)

def count_completed_decision_lessons(user_data):
    """Liczy ukończone lekcje o podejmowaniu decyzji"""
    completed_lessons = user_data.get('completed_lessons', [])
    decision_lessons = [lesson for lesson in completed_lessons if 'decyz' in str(lesson).lower() or 'decision' in str(lesson).lower()]
    return len(decision_lessons)

def count_completed_team_lessons(user_data):
    """Liczy ukończone lekcje o zespołach"""
    completed_lessons = user_data.get('completed_lessons', [])
    team_lessons = [lesson for lesson in completed_lessons if 'team' in str(lesson).lower() or 'zespol' in str(lesson).lower()]
    return len(team_lessons)

def count_completed_change_lessons(user_data):
    """Liczy ukończone lekcje o zarządzaniu zmianą"""
    completed_lessons = user_data.get('completed_lessons', [])
    change_lessons = [lesson for lesson in completed_lessons if 'chang' in str(lesson).lower() or 'zmian' in str(lesson).lower()]
    return len(change_lessons)

def count_completed_communication_lessons(user_data):
    """Liczy ukończone lekcje o komunikacji"""
    completed_lessons = user_data.get('completed_lessons', [])
    comm_lessons = [lesson for lesson in completed_lessons if 'komun' in str(lesson).lower() or 'comm' in str(lesson).lower()]
    return len(comm_lessons)

def count_weekend_sessions(user_data):
    """Liczy sesje nauki w weekendy na podstawie timestampów"""
    lesson_progress = user_data.get('lesson_progress', {})
    weekend_count = 0
    weekend_dates = set()
    
    for lesson_id, progress in lesson_progress.items():
        for step, timestamp in progress.items():
            if '_timestamp' in step and isinstance(timestamp, str):
                try:
                    from datetime import datetime
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    # 5 = Saturday, 6 = Sunday
                    if dt.weekday() in [5, 6]:
                        weekend_dates.add(dt.date())
                except:
                    continue
    
    return len(weekend_dates)

def has_late_night_session(user_data):
    """Sprawdza czy użytkownik miał sesję po 22:00"""
    lesson_progress = user_data.get('lesson_progress', {})
    
    for lesson_id, progress in lesson_progress.items():
        for step, timestamp in progress.items():
            if '_timestamp' in step and isinstance(timestamp, str):
                try:
                    from datetime import datetime
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    if dt.hour >= 22:
                        return True
                except:
                    continue
    return False

def has_early_morning_session(user_data):
    """Sprawdza czy użytkownik miał sesję przed 8:00"""
    lesson_progress = user_data.get('lesson_progress', {})
    
    for lesson_id, progress in lesson_progress.items():
        for step, timestamp in progress.items():
            if '_timestamp' in step and isinstance(timestamp, str):
                try:
                    from datetime import datetime
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    if dt.hour < 8:
                        return True
                except:
                    continue
    return False

def has_multi_type_development(user_data):
    """Sprawdza czy użytkownik rozwija umiejętności poza swoim dominującym typem"""
    neuroleader_type = user_data.get('neuroleader_type')
    if not neuroleader_type:
        return False
    
    # Sprawdź czy ma wysokie wyniki w testach dla różnych typów
    test_scores = user_data.get('test_scores', {})
    if not test_scores:
        return False
    
    # Policz ile typów ma wynik powyżej przeciętnej
    avg_score = sum(test_scores.values()) / len(test_scores) if test_scores else 0
    high_scores = [score for score in test_scores.values() if score > avg_score]
    
    return len(high_scores) >= 3  # Rozwija co najmniej 3 różne aspekty