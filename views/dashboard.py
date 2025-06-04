import streamlit as st
import random
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data
from data.test_questions import NEUROLEADER_TYPES
from config.settings import DAILY_MISSIONS, XP_LEVELS, USER_AVATARS
from data.lessons import load_lessons
from utils.goals import get_user_goals, calculate_goal_metrics
from utils.daily_missions import get_daily_missions_progress
from views.degen_explorer import plot_radar_chart
from data.neuroleader_details import degen_details
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from utils.components import (
    zen_header, mission_card, degen_card, progress_bar, stat_card, 
    xp_level_display, zen_button, notification, leaderboard_item, 
    add_animations_css, data_chart, user_stats_panel, lesson_card
)
from utils.real_time_updates import get_live_user_stats, live_xp_indicator

def calculate_xp_progress(user_data):
    """Calculate XP progress and dynamically determine the user's level"""
    # Dynamically determine the user's level based on XP
    for level, xp_threshold in sorted(XP_LEVELS.items(), reverse=True):
        if user_data['xp'] >= xp_threshold:
            user_data['level'] = level
            break

    # Calculate progress to the next level
    next_level = user_data['level'] + 1
    if next_level in XP_LEVELS:
        current_level_xp = XP_LEVELS[user_data['level']]
        next_level_xp = XP_LEVELS[next_level]
        xp_needed = next_level_xp - current_level_xp
        xp_progress = user_data['xp'] - current_level_xp
        xp_percentage = min(100, int((xp_progress / xp_needed) * 100))
        return xp_percentage, xp_needed - xp_progress

    return 100, 0

def get_top_users(limit=5):
    """Get top users by XP"""
    users_data = load_user_data()
    leaderboard = []
    
    for username, data in users_data.items():
        leaderboard.append({
            'username': username,
            'level': data.get('level', 1),
            'xp': data.get('xp', 0)
        })
    
    # Sort by XP (descending)
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)
    return leaderboard[:limit]

def get_user_rank(username):
    """Get user rank in the leaderboard"""
    users_data = load_user_data()
    leaderboard = []
    
    for user, data in users_data.items():
        leaderboard.append({
            'username': user,
            'xp': data.get('xp', 0)
        })
    
    # Sort by XP (descending)
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)
    
    # Find user rank
    for i, user in enumerate(leaderboard):
        if user['username'] == username:
            return {'rank': i + 1, 'xp': user['xp']}
    
    return {'rank': 0, 'xp': 0}

def get_user_xp_history(username, days=30):
    """Simulate XP history data (for now)"""
    # This would normally come from a database
    # For now, we'll generate fictional data
    history = []
    today = datetime.now()
    
    # Generate data points for the last X days
    xp = load_user_data().get(username, {}).get('xp', 0)
    daily_increment = max(1, int(xp / days))
    
    for i in range(days):
        date = today - timedelta(days=days-i)
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'xp': max(0, int(xp * (i+1) / days))
        })
    
    return history

# def display_lesson_cards(lessons_list, tab_name="", custom_columns=None):
#     """Display lesson cards in a responsive layout
    
#     Args:
#         lessons_list: Dictionary of lessons to display
#         tab_name: Name of the tab to use for creating unique button keys
#         custom_columns: Optional pre-defined columns for responsive layout
#     """
#     if not lessons_list:
#         st.info("Brak dostępnych lekcji w tej kategorii.")
#         return
    
#     users_data = load_user_data()
#     user_data = users_data.get(st.session_state.username, {})
#       # Jeśli nie dostarczono niestandardowych kolumn, użyj jednej kolumny na całą szerokość
#     if custom_columns is None:
#         # Zawsze używaj jednej kolumny na całą szerokość
#         custom_columns = [st.container()]
    
#     # Display lessons in the responsive grid
#     for i, (lesson_id, lesson) in enumerate(lessons_list.items()):
#         # Get lesson properties
#         difficulty = lesson.get('difficulty', 'intermediate')
#         is_completed = lesson_id in user_data.get('completed_lessons', [])# Przygotuj symbol trudności
#         if difficulty == "beginner":
#             difficulty_symbol = "🟢"
#         elif difficulty == "intermediate":
#             difficulty_symbol = "🟠"
#         else:
#             difficulty_symbol = "🔴"
#           # Użyj zawsze pierwszej kolumny, bo teraz mamy tylko jedną kolumnę
#         with custom_columns[0]:
#             # Użyj komponentu lesson_card dla spójności z widokiem lekcji
#             lesson_card(
#                 title=lesson.get('title', 'Lekcja'),
#                 description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
#                 xp=lesson.get('xp_reward', 30),
#                 difficulty=difficulty,
#                 category=lesson.get('tag', ''),
#                 completed=is_completed,
#                 button_text="Powtórz lekcję" if is_completed else "Rozpocznij",
#                 button_key=f"{tab_name}_start_{lesson_id}_{i}",
#                 lesson_id=lesson_id,
#                 on_click=lambda lesson_id=lesson_id: (
#                     setattr(st.session_state, 'current_lesson', lesson_id),
#                     setattr(st.session_state, 'page', 'lesson'),
#                     st.rerun()
#                 )
#         )

def display_lesson_cards(lessons_list, tab_name="", custom_columns=None):
    """Display lesson cards in a responsive layout
    
    Args:
        lessons_list: Dictionary of lessons to display
        tab_name: Name of the tab to use for creating unique button keys
        custom_columns: Optional pre-defined columns for responsive layout
    """
    if not lessons_list:
        st.info("Brak dostępnych lekcji w tej kategorii.")
        return
    
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    completed_lessons = user_data.get('completed_lessons', [])
    
    # Jeśli nie dostarczono niestandardowych kolumn, użyj jednej kolumny na całą szerokość
    if custom_columns is None:
        custom_columns = [st.container()]
    
    # Display lessons using lesson_card component
    for i, (lesson_id, lesson) in enumerate(lessons_list.items()):
        is_completed = lesson_id in completed_lessons
        
        # Użyj zawsze pierwszej kolumny
        with custom_columns[0]:
            lesson_card(
                title=lesson.get('title', 'Lekcja'),
                description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                xp=lesson.get('xp_reward', 30),
                difficulty=lesson.get('difficulty', 'beginner'),
                category=lesson.get('tag', ''),
                completed=is_completed,
                button_text="Powtórz lekcję" if is_completed else "Rozpocznij",
                button_key=f"{tab_name}_start_{lesson_id}_{i}",
                lesson_id=lesson_id,
                on_click=lambda lesson_id=lesson_id: (
                    setattr(st.session_state, 'current_lesson', lesson_id),
                    setattr(st.session_state, 'page', 'lesson'),
                    st.rerun()
                )
            )
def get_recommended_lessons(username):
    """Get recommended lessons based on user type"""
    lessons = load_lessons()
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    neuroleader_type = user_data.get('neuroleader_type', None)
    
    # If user has a neuroleader type, filter lessons to match
    if neuroleader_type:
        return {k: v for k, v in lessons.items() if v.get('recommended_for', None) == neuroleader_type}
    
    # Otherwise, return a small selection of beginner lessons
    return {k: v for k, v in lessons.items() if v.get('difficulty', 'medium') == 'beginner'}

def get_popular_lessons():
    """Get most popular lessons based on completion count"""
    # Dla symulanty, zwracamy standardowe lekcje z modyfikatorem "popular"
    # aby zapewnić unikalność kluczy lekcji między różnymi kategoriami
    lessons = load_lessons()
    return lessons

def get_newest_lessons():
    """Get newest lessons"""
    # Dla symulanty, zwracamy standardowe lekcje z modyfikatorem "newest"
    # aby zapewnić unikalność kluczy lekcji między różnymi kategoriami
    lessons = load_lessons()
    return lessons

def get_daily_missions(username):
    """Get daily missions for user"""
    # For now, use the missions from settings
    # We're only showing the first 3 missions to the user
    return DAILY_MISSIONS[:3]

def show_stats_section(user_data, device_type):
    """Sekcja z kartami statystyk - alternatywne podejście z kolumnami"""
    
    # Oblicz dane statystyk
    xp = user_data.get('xp', 0)
    completed_lessons = len(user_data.get('completed_lessons', []))
    missions_progress = get_daily_missions_progress(st.session_state.username)
    streak = missions_progress['streak']
    level = user_data.get('level', 1)
    
    # Oblicz trend XP (przykładowy +15%)
    xp_change = "+15%"
    lessons_change = f"+{min(3, completed_lessons)}"
    streak_change = f"+{min(1, streak)}"
    level_change = f"+{max(0, level - 1)}"
    
    # Utwórz 5 kolumn
    cols = st.columns(4)
    
    # 5 kart statystyk
    stats = [
        {"icon": "🏆", "value": f"{xp}", "label": "Punkty XP", "change": xp_change},
        {"icon": "⭐", "value": f"{level}", "label": "Poziom", "change": level_change},
        {"icon": "📚", "value": f"{completed_lessons}", "label": "Ukończone lekcje", "change": lessons_change},
        {"icon": "🔥", "value": f"{streak}", "label": "Aktualna passa", "change": streak_change},

        # {"icon": "🎯", "value": f"{missions_progress['completed']}", "label": "Dzisiejsze misje", "change": f"+{missions_progress['completed']}"}
    ]
    
    # Wygeneruj kartę w każdej kolumnie
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{stat['icon']}</div>
                <div class="stat-value">{stat['value']}</div>
                <div class="stat-label">{stat['label']}</div>
                <div class="stat-change positive">{stat['change']}</div>
            </div>
            """, unsafe_allow_html=True)

# def show_main_content(user_data, device_type):
#     """Główna zawartość dashboardu"""
    
#     # Sekcja ostatnich aktywności
#     show_recent_activities(user_data)
    
#     # Sekcja dostępnych lekcji
#     show_available_lessons(device_type)
    
#     # Sekcja misji dziennych
#     show_daily_missions_section()

def show_main_content(user_data, device_type):
    """Główna zawartość dashboardu"""
    # Sekcja dostępnych lekcji - teraz używa lesson_card
    show_available_lessons(device_type)
    # Sekcja wyników testu neuroleadera - tylko jeśli użytkownik wykonał test
    show_neuroleader_results_section(user_data, device_type)
        


    # Sekcja misji dziennych
    show_daily_missions_section()    # Sekcja ostatnich aktywności

    

def show_neuroleader_results_section(user_data, device_type):
    """Sekcja wyników testu neuroleadera w głównej zawartości dashboardu"""
    
    # Sprawdź czy użytkownik ma wyniki testu neuroleadera
    neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type')
    test_taken = user_data.get('test_taken', False)
    test_scores = user_data.get('test_scores')
    
    if neuroleader_type and (test_taken or test_scores):
        st.markdown("""
        <div class="dashboard-section">
            <div class="section-header">
                <h3 class="section-title">🧠 Twój profil neuroleaderski</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Get neuroleader color for styling
        neuroleader_color = NEUROLEADER_TYPES.get(neuroleader_type, {}).get('color', '#3498db')
        
        # Header with prominent display of result
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; border-radius: 15px; 
                    background: linear-gradient(135deg, {neuroleader_color}20, {neuroleader_color}10);
                    border: 2px solid {neuroleader_color}40; margin-bottom: 20px;'>
            <h3 style='color: {neuroleader_color}; margin-bottom: 10px; font-size: 1.2em;'>
                🧬 Twój dominujący typ neuroleadera
            </h3>
            <h2 style='color: {neuroleader_color}; margin: 10px 0; font-size: 1.8em; font-weight: bold;'>
                {neuroleader_type}
            </h2>
            <p style='color: #666; margin: 0; font-size: 1em;'>
                {NEUROLEADER_TYPES.get(neuroleader_type, {}).get('description', 'Opis niedostępny')}
            </p>
        </div>
        """, unsafe_allow_html=True)
          # Show radar chart if test scores are available
        if test_scores:
            try:
                radar_fig = plot_radar_chart(test_scores, device_type=device_type)
                
                # Display radar chart based on device type
                if device_type == 'mobile':
                    st.markdown("#### 📊 Twój profil w szczegółach")
                    st.pyplot(radar_fig)
                else:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown("#### 📊 Twój profil w szczegółach")
                        st.pyplot(radar_fig)
                        
                    with col2:
                        # Show key characteristics in sidebar format
                        st.markdown("##### 💪 Mocne strony:")
                        strengths = NEUROLEADER_TYPES.get(neuroleader_type, {}).get('strengths', [])
                        for strength in strengths[:3]:  # Show only first 3 for space
                            st.markdown(f"• {strength}")
                        
                        st.markdown("##### 🚧 Wyzwania:")
                        challenges = NEUROLEADER_TYPES.get(neuroleader_type, {}).get('challenges', [])
                        for challenge in challenges[:3]:  # Show only first 3 for space
                            st.markdown(f"• {challenge}")
                            
            except Exception as e:
                st.warning("Nie udało się wygenerować wykresu radarowego.")
          # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if zen_button("🔍 Szczegółowy opis", key="dashboard_detailed_description"):
                st.session_state.page = 'degen_explorer'
                st.rerun()
                
        with col2:
            if zen_button("🔄 Wykonaj test ponownie", key="dashboard_retake_test"):
                st.session_state.page = 'degen_explorer'
                st.rerun()
                
        with col3:
            if zen_button("📈 Zobacz profil", key="dashboard_view_profile"):
                st.session_state.page = 'profile'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif not neuroleader_type:
        # Encourage user to take the test if they haven't yet
        st.markdown("""
        <div class="dashboard-section">
            <div class="section-header">
                <h3 class="section-title">🧠 Odkryj swój typ neuroleadera</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; padding: 20px; border-radius: 15px; 
                    background: linear-gradient(135deg, #3498db20, #3498db10);
                    border: 2px solid #3498db40; margin-bottom: 20px;'>
            <h3 style='color: #3498db; margin-bottom: 15px;'>
                🎯 Jeszcze nie poznałeś swojego typu neuroleadera!
            </h3>
            <p style='color: #666; margin-bottom: 20px; line-height: 1.6;'>
                Wykonaj nasz test psychologiczny i odkryj swój unikalny profil przywódczy. 
                Test zajmie tylko kilka minut i pomoże Ci lepiej zrozumieć swoje mocne strony jako lider.
            </p>        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if zen_button("🚀 Wykonaj test neuroleadera", key="dashboard_take_test", use_container_width=True):
                st.session_state.page = 'degen_explorer'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)


def show_dashboard_sidebar(user_data, device_type):
    """Sidebar z dodatkowymi informacjami"""       # Profil neuroleaderski
    show_recent_activities(user_data)

    show_neuroleader_profile_compact(user_data)
    
    # Ranking XP
    show_leaderboard_compact()

    # Widget postępu
    show_progress_widget(user_data)
    


def show_recent_activities(user_data):
    """Lista ostatnich aktywności"""
    st.markdown("""
    <div class="dashboard-section">
        <div class="section-header">
            <h3 class="section-title">Ostatnie aktywności</h3>
            <a href="#" class="section-action">Zobacz wszystkie</a>
        </div>
        <div class="activity-list">
    """, unsafe_allow_html=True)
      # Import badge configuration
    try:
        from config.badges import BADGES
    except ImportError:
        from config.settings import BADGES
    
    # Pobierz dane użytkownika
    completed_lessons = user_data.get('completed_lessons', [])
    neuroleader_type = user_data.get('neuroleader_type', None)
    user_badges = user_data.get('badges', [])
    badge_timestamps = user_data.get('badge_timestamps', {})
    
    activities = []
    
    def get_time_ago(timestamp_str):
        """Oblicza ile czasu temu wydarzyło się coś na podstawie timestampu"""
        try:
            from datetime import datetime
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            diff = now - timestamp
            
            if diff.days > 0:
                return f"{diff.days} {'dzień' if diff.days == 1 else 'dni'} temu"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} {'godzinę' if hours == 1 else 'godzin'} temu"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} {'minutę' if minutes == 1 else 'minut'} temu"
            else:
                return "przed chwilą"
        except:
            return "niedawno"
    
    # Dodaj informacje o zdobytych odznakach z timestampami
    if user_badges and badge_timestamps:
        # Sortuj odznaki według czasu zdobycia (najnowsze pierwsze)
        badges_with_time = []
        for badge_id in user_badges:
            if badge_id in badge_timestamps:
                badges_with_time.append((badge_id, badge_timestamps[badge_id]))
        
        # Sortuj według timestampu (najnowsze pierwsze) i weź ostatnie 2
        badges_with_time.sort(key=lambda x: x[1], reverse=True)
        recent_badges = badges_with_time[:2]
        
        for badge_id, timestamp in recent_badges:
            badge_info = BADGES.get(badge_id, {})
            badge_name = badge_info.get('name', badge_id)
            badge_icon = badge_info.get('icon', '🏆')
            time_ago = get_time_ago(timestamp)
            
            activities.append({
                'icon': badge_icon,
                'color': '#f39c12',
                'title': f'Zdobyto odznakę: {badge_name}',
                'time': time_ago
            })
    elif user_badges:
        # Fallback dla starych danych bez timestampów
        recent_badges = user_badges[-2:] if len(user_badges) >= 2 else user_badges
        for badge_id in reversed(recent_badges):
            badge_info = BADGES.get(badge_id, {})
            badge_name = badge_info.get('name', badge_id)
            badge_icon = badge_info.get('icon', '🏆')
            
            activities.append({
                'icon': badge_icon,
                'color': '#f39c12',
                'title': f'Zdobyto odznakę: {badge_name}',
                'time': 'niedawno'
            })
      # Dodaj informacje o ukończonych lekcjach
    if completed_lessons:
        # Pobierz tytuł ostatniej ukończonej lekcji
        last_lesson_id = completed_lessons[-1]
        lessons_data = load_lessons()
        lesson_title = lessons_data.get(last_lesson_id, {}).get('title', last_lesson_id)
        
        activities.append({
            'icon': '✓',
            'color': '#27ae60',
            'title': f'Ukończono lekcję: {lesson_title}',
            'time': '2 godziny temu'
        })
    
    # Dodaj informacje o odkrytym typie neuroleadera
    if neuroleader_type:
        activities.append({
            'icon': '🧠',
            'color': '#3498db',
            'title': f'Odkryto typ neuroleadera: {neuroleader_type}',
            'time': '1 dzień temu'
        })
    
    # Dodaj standardową aktywność jeśli brak innych
    if not activities:
        activities.append({
            'icon': '🔥',
            'color': '#e67e22',
            'title': 'Rozpoczęto nową passę dzienną',
            'time': '3 godziny temu'
        })
    
    for activity in activities:
        st.markdown(f"""
            <div class="activity-item">
                <div class="activity-icon" style="background: rgba({activity['color'][1:3]}, {activity['color'][3:5]}, {activity['color'][5:7]}, 0.1); color: {activity['color']};">
                    {activity['icon']}
                </div>
                <div class="activity-content">
                    <div class="activity-title">{activity['title']}</div>
                    <div class="activity-time">{activity['time']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# def show_available_lessons(device_type):
#     """Sekcja dostępnych lekcji w głównej zawartości"""
#     st.markdown("""
#     <div class="dashboard-section">
#         <div class="section-header">
#             <h3 class="section-title">Dostępne lekcje</h3>
#         </div>
#     """, unsafe_allow_html=True)
    
#     # Pobierz lekcje
#     lessons = load_lessons()
    
#     # Wyświetl pierwsze 3 lekcje w kompaktowym formacie
#     lesson_count = 0
#     for lesson_id, lesson in lessons.items():
#         if lesson_count >= 3:  # Ogranicz do 3 lekcji w widoku głównym
#             break
            
#         difficulty = lesson.get('difficulty', 'intermediate')
#         if difficulty == "beginner":
#             difficulty_color = "#27ae60"
#             difficulty_icon = "🟢"
#         elif difficulty == "intermediate":
#             difficulty_color = "#f39c12"
#             difficulty_icon = "🟠"
#         else:
#             difficulty_color = "#e74c3c"
#             difficulty_icon = "🔴"
        
#         st.markdown(f"""
#         <div class="compact-item">
#             <div class="compact-icon" style="color: {difficulty_color};">{difficulty_icon}</div>
#             <div class="compact-content">
#                 <div class="compact-title">{lesson.get('title', 'Lekcja')}</div>
#                 <div class="compact-progress">XP: {lesson.get('xp_reward', 30)} • {difficulty.title()}</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         lesson_count += 1
    
#     # Przycisk do wszystkich lekcji
#     if zen_button("Zobacz wszystkie lekcje", key="all_lessons_compact"):
#         # Tu można dodać nawigację do pełnej listy lekcji
#         pass
    
#     st.markdown("</div>", unsafe_allow_html=True)

def show_available_lessons(device_type):
    """Sekcja dostępnych lekcji w głównej zawartości"""
    st.markdown("""
    <div class="dashboard-section">
        <div class="section-header">
            <h3 class="section-title">Dostępne lekcje</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    completed_lessons = user_data.get('completed_lessons', [])
    
    # Pobierz lekcje
    lessons = load_lessons()
    
    # Wyświetl pierwsze 3 lekcje używając lesson_card
    lesson_count = 0
    for lesson_id, lesson in lessons.items():
        if lesson_count >= 3:  # Ogranicz do 3 lekcji w widoku głównym
            break
            
        # Sprawdź czy lekcja jest ukończona
        is_completed = lesson_id in completed_lessons
        
        # Użyj lesson_card z utils.components
        lesson_card(
            title=lesson.get('title', 'Lekcja bez tytułu'),
            description=lesson.get('description', 'Opis lekcji...'),
            xp=lesson.get('xp_reward', 30),
            difficulty=lesson.get('difficulty', 'beginner'),
            category=lesson.get('tag', 'Ogólne'),
            completed=is_completed,
            button_text="Powtórz lekcję" if is_completed else "Rozpocznij lekcję",
            button_key=f"dashboard_lesson_{lesson_id}_{lesson_count}",
            lesson_id=lesson_id,
            on_click=lambda lid=lesson_id: (
                setattr(st.session_state, 'current_lesson', lid),
                setattr(st.session_state, 'page', 'lesson'),
                st.rerun()
            )
        )
        
        lesson_count += 1
    
    # Przycisk do wszystkich lekcji
    if zen_button("Zobacz wszystkie lekcje", key="all_lessons_from_dashboard"):
        st.session_state.page = 'lesson'
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_daily_missions_section():
    """Sekcja misji dziennych w głównej zawartości"""
    st.markdown("""
    <div class="dashboard-section">
        <div class="section-header">
            <h3 class="section-title">Misje dnia</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Get daily missions and progress
    daily_missions = get_daily_missions(st.session_state.username)
    missions_progress = get_daily_missions_progress(st.session_state.username)
    
    # Wyświetl pierwsze 3 misje w kompaktowym formacie
    mission_count = 0
    for mission in daily_missions:
        if mission_count >= 3:
            break
            
        is_completed = mission['title'] in missions_progress['completed_ids']
        
        st.markdown(f"""
        <div class="compact-item">
            <div class="compact-icon">{mission['badge']}</div>
            <div class="compact-content">
                <div class="compact-title">{mission['title']}</div>
                <div class="compact-progress">{'✅ Ukończone' if is_completed else f"XP: {mission['xp']}"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        mission_count += 1
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_progress_widget(user_data):
    """Widget postępu w sidebarze"""
    xp = user_data.get('xp', 0)
    level = user_data.get('level', 1)
    next_level_xp = XP_LEVELS.get(level + 1, xp + 100)
    current_level_xp = XP_LEVELS.get(level, 0)
    
    # Zabezpieczenie przed None values
    if next_level_xp is None:
        next_level_xp = xp + 100
    if current_level_xp is None:
        current_level_xp = 0
    
    # Oblicz procent postępu
    if next_level_xp > current_level_xp:
        progress_percent = int(((xp - current_level_xp) / (next_level_xp - current_level_xp)) * 100)
    else:
        progress_percent = 100
    
    # Upewnij się, że progress_percent jest w zakresie 0-100
    progress_percent = max(0, min(100, progress_percent))
    
    st.markdown(f"""
    <div class="progress-widget">
        <div class="progress-text">{progress_percent}%</div>
        <div class="progress-label">Postęp do poziomu {level + 1}</div>
        <div style="margin-top: 16px; font-size: 14px;">
            Poziom {level} • {xp} XP
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_neuroleader_profile_compact(user_data):
    """Kompaktowy profil neuroleaderski"""
    st.markdown("""
    <div class="dashboard-section">
        <div class="section-header">
            <h3 class="section-title">Profil neuroleaderski</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'test_scores' in user_data:
        # Pokaż dominujący typ
        dominant_type = max(user_data['test_scores'].items(), key=lambda x: x[1])[0]
        neuroleader_color = NEUROLEADER_TYPES.get(dominant_type, {}).get('color', '#3498db')
        
        st.markdown(f"""
        <div style="text-align: center; padding: 16px;">
            <div style="font-size: 24px; margin-bottom: 8px;">🧬</div>
            <div style="font-weight: 600; color: {neuroleader_color};">{dominant_type}</div>
            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                Twój dominujący typ
            </div>
        </div>
        """, unsafe_allow_html=True)        
        if zen_button("Zobacz szczegóły", key="profile_details"):
            st.session_state.page = 'degen_explorer'
            st.rerun()
    else:
        st.info("Wykonaj test, aby odkryć swój profil")
        if zen_button("Wykonaj test", key="take_test_sidebar"):
            st.session_state.page = 'degen_explorer'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_leaderboard_compact():
    """Kompaktowy ranking XP"""
    st.markdown("""
    <div class="dashboard-section">
        <div class="section-header">
            <h3 class="section-title">Ranking XP</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Pobierz top 3 użytkowników
    top_users = get_top_users(3)
    
    for i, user in enumerate(top_users):
        rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        is_current = user['username'] == st.session_state.username
        
        st.markdown(f"""
        <div class="compact-item" style="{'background: rgba(41, 128, 185, 0.1);' if is_current else ''}">
            <div class="compact-icon">{rank_icon}</div>
            <div class="compact-content">
                <div class="compact-title">{'Ty' if is_current else user['username']}</div>
                <div class="compact-progress">{user['xp']} XP</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_dashboard():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
      # Używamy naszego komponentu nagłówka - bez dodatkowego CSS
    zen_header("Dashboard Neuroleaderów")
    
    # Add live XP indicator
    live_xp_indicator()
    
    # Dodajemy animacje CSS
    add_animations_css()    # Use complete user data instead of limited live stats to access neuroleader test data
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Główny kontener dashboard
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Sekcja statystyk - pełna szerokość
    show_stats_section(user_data, device_type)
    
    # Główna zawartość i sidebar
    if device_type == 'mobile':
        # Na telefonach wyświetl sekcje jedna pod drugą
        show_main_content(user_data, device_type)
        show_dashboard_sidebar(user_data, device_type)
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="main-content">', unsafe_allow_html=True)
            show_main_content(user_data, device_type)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-sidebar">', unsafe_allow_html=True)
            show_dashboard_sidebar(user_data, device_type)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)    # Sekcja promująca rozwój umiejętności
    st.markdown("""
    <div class="dashboard-section">
        <h3>🌳 Rozwijaj swoje umiejętności</h3>
        <p>Ulepszaj swoje umiejętności przywódcze i odblokuj nowe możliwości.</p>
    </div>
    """, unsafe_allow_html=True)

    if zen_button("Przejdź do drzewa umiejętności", key="goto_skills"):
        st.session_state.page = "skills"
        st.rerun()

    # Admin button for admin users
    admin_users = ["admin", "zenmaster"]  # Lista administratorów
    if st.session_state.get('username') in admin_users:
        st.markdown("---")
        if zen_button("🛡️ Panel administratora", key="admin_panel"):
            st.session_state.page = 'admin'
            st.rerun()
