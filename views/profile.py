import streamlit as st
import pandas as pd
import random
import re
import os
import numpy as np
import json
from data.test_questions import NEUROLEADER_TYPES
from data.users import load_user_data, save_user_data, update_single_user_field
from data.neuroleader_details import degen_details
from views.degen_test import plot_radar_chart
from PIL import Image
from utils.components import zen_header, zen_button, notification, content_section, tip_block
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view, apply_responsive_styles, get_responsive_figure_size

from datetime import datetime, timedelta
import time
from utils.personalization import (
    update_user_avatar,
    update_user_theme,
    get_user_style,
    generate_user_css
)
from utils.goals import (
    add_user_goal,
    update_goal_progress,
    delete_goal,
    get_user_goals,
    calculate_goal_metrics
)
from utils.inventory import (
    activate_item,
    get_user_inventory,
    is_booster_active,
    format_time_remaining
)
from config.settings import USER_AVATARS, THEMES, NEUROLEADER_TYPES, BADGES
from data.neuroleader_details import degen_details
from views.degen_explorer import plot_radar_chart
from views.dashboard import calculate_xp_progress
from utils.components import zen_header, zen_button, notification, content_section, stat_card, xp_level_display, goal_card, badge_card, progress_bar, tip_block, quote_block,  add_animations_css
from utils.user_components import user_stats_panel
from utils.real_time_updates import get_live_user_stats, live_xp_indicator

def show_profile():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Zastosuj responsywne style
    apply_responsive_styles()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
      # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    zen_header("Profil użytkownika")
      # Add live XP indicator
    live_xp_indicator()
    
    # Load full user data instead of limited live stats for profile display
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    style = get_user_style(st.session_state.username)
    
    # Wyświetl personalizowane style
    st.markdown(generate_user_css(st.session_state.username), unsafe_allow_html=True)
    
    # Add animations and effects using the component
    add_animations_css()
    
    # User Statistics Section - z wykorzystaniem nowych komponentów Material 3
    st.markdown("<div class='st-bx fadeIn'>", unsafe_allow_html=True)    # Setup data for user stats panel
    avatar = style['avatar']
    neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type', 'Typ nie określony')
    level = user_data.get('level', 1)
    xp = user_data.get('xp', 0)
    completed = len(user_data.get('completed_lessons', []))
    
    # Calculate XP data
    xp_progress, xp_needed = calculate_xp_progress(user_data)
    next_level_xp = xp + xp_needed  # Estimated XP for next level
    
    # Display user stats using the component
    user_stats_panel(
        username=st.session_state.username,
        avatar=avatar,
        neuroleader_type=neuroleader_type,
        level=level,
        xp=xp,
        completed_lessons=completed,
        next_level_xp=next_level_xp
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
      # Main Profile Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Personalizacja", "Ekwipunek", "Odznaki", "Typ Neuroleadera"])
    
    # Tab 1: Personalization
    with tab1:
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        personalization_cols = st.columns(2)
        
        # Avatar Selection
        with personalization_cols[0]:
            st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
            st.subheader("Wybierz avatar")
            
            # Visual avatar selector with all options displayed
            current_avatar = user_data.get('avatar', 'default')
            
            # Create a visual avatar grid using Streamlit components instead of raw HTML/JS
            # This approach avoids raw HTML/JS being shown to users
            avatar_grid = st.container()
            with avatar_grid:
                # Show header text
                st.write("Kliknij, aby wybrać:")
                
                # Create rows of avatars with 4 avatars per row
                items_per_row = 4
                avatar_rows = [list(USER_AVATARS.items())[i:i+items_per_row] for i in range(0, len(USER_AVATARS), items_per_row)]
                
                for row in avatar_rows:
                    cols = st.columns(items_per_row)
                    for i, (avatar_id, avatar_emoji) in enumerate(row):
                        with cols[i]:
                            # Style based on whether this avatar is selected
                            highlight = f"color: {style['theme']['primary']}; transform: scale(1.2);" if avatar_id == current_avatar else ""
                            
                            # Add visible indicator for selected avatar
                            selected_indicator = "✓ " if avatar_id == current_avatar else ""
                            
                            st.markdown(f"""
                            <div style="text-align: center; cursor: pointer; {highlight}">
                                <div style="font-size: 2.5rem; margin-bottom: 5px;">{avatar_emoji}</div>
                                <div style="font-size: 0.8rem;">{selected_indicator}{avatar_id.title()}</div>
                            </div>
                            """, unsafe_allow_html=True)
            
            # We still need a form to submit the selection
            # Streamlit's JavaScript interaction is limited, so we use a dropdown for actual selection
            selected_avatar = st.selectbox(
                "Wybierz swojego avatara:",
                options=list(USER_AVATARS.keys()),
                format_func=lambda x: f"{USER_AVATARS[x]} - {x.title()}",
                index=list(USER_AVATARS.keys()).index(current_avatar),
                label_visibility="collapsed"
            )
            
            if zen_button("Zapisz avatar", key="save_avatar"):
                if update_user_avatar(st.session_state.username, selected_avatar):
                    notification("Avatar został zaktualizowany!", type="success")
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Theme Selection
        with personalization_cols[1]:
            st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
            st.subheader("Wybierz motyw")
            
            current_theme = user_data.get('theme', 'default')
            
            # Visual theme selector
            for theme_id, theme_colors in THEMES.items():
                selected_class = "selected" if theme_id == current_theme else ""
                
                st.markdown(f"""
                <div class="theme-option {selected_class}" id="theme-{theme_id}">
                    <div><strong>{theme_id.replace('_', ' ').title()}</strong></div>
                    <div class="theme-colors">
                        <div class="theme-color-sample" style="background-color: {theme_colors['primary']};"></div>
                        <div class="theme-color-sample" style="background-color: {theme_colors['secondary']};"></div>
                        <div class="theme-color-sample" style="background-color: {theme_colors['accent']};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # We still need a dropdown for selection
            selected_theme = st.selectbox(
                "Wybierz motyw:",
                options=list(THEMES.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                index=list(THEMES.keys()).index(current_theme),
                label_visibility="collapsed"
            )
            
            if zen_button("Zapisz motyw", key="save_theme"):
                if update_user_theme(st.session_state.username, selected_theme):
                    notification("Motyw został zaktualizowany!", type="success")
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab 2: Inventory/Equipment
    with tab2:
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        
        # Load user inventory
        inventory = get_user_inventory(st.session_state.username)
        
        # Create subtabs for different inventory categories
        inv_tabs = st.tabs(["Awatary", "Tła", "Specjalne Lekcje", "Boostery"])
        
        # Tab for Avatars
        with inv_tabs[0]:
            st.subheader("Twoje Awatary")
            
            if inventory['avatars']:
                # Create a grid of avatars
                avatar_cols = st.columns(4)
                
                for i, avatar_id in enumerate(inventory['avatars']):
                    if avatar_id in USER_AVATARS:
                        with avatar_cols[i % 4]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 3rem; margin-bottom: 5px;">{USER_AVATARS[avatar_id]}</div>
                                <div style="font-size: 0.9rem;">{avatar_id.replace('_', ' ').title()}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Add a button to activate this avatar
                            if st.button(f"Aktywuj {avatar_id.title()}", key=f"activate_avatar_{avatar_id}"):
                                success, message = activate_item(st.session_state.username, 'avatar', avatar_id)
                                if success:
                                    notification(message, type="success")
                                    st.rerun()
                                else:
                                    notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych awatarów. Kup je w sklepie!")
                if st.button("Przejdź do sklepu", key="go_to_shop_avatars"):
                    st.session_state.page = 'shop'
                    st.rerun()
        
        # Tab for Backgrounds
        with inv_tabs[1]:
            st.subheader("Twoje Tła")
            
            if inventory['backgrounds']:
                # Create a grid of backgrounds
                bg_cols = st.columns(2)
                
                for i, bg_id in enumerate(inventory['backgrounds']):
                    with bg_cols[i % 2]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px;">
                            <div style="font-size: 2rem; margin-bottom: 5px;">🖼️</div>
                            <div style="font-size: 1rem; font-weight: bold;">{bg_id.replace('_', ' ').title()}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a button to activate this background
                        if st.button(f"Aktywuj {bg_id.title()}", key=f"activate_bg_{bg_id}"):
                            success, message = activate_item(st.session_state.username, 'background', bg_id)
                            if success:
                                notification(message, type="success")
                                st.rerun()
                            else:
                                notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych teł. Kup je w sklepie!")
                if st.button("Przejdź do sklepu", key="go_to_shop_bgs"):
                    st.session_state.page = 'shop'
                    st.rerun()
        
        # Tab for Special Lessons
        with inv_tabs[2]:
            st.subheader("Twoje Specjalne Lekcje")
            
            if inventory['special_lessons']:
                # Display special lessons
                for lesson_id in inventory['special_lessons']:
                    with st.container():
                        st.markdown(f"""
                        <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 15px;">
                            <div style="display: flex; align-items: center;">
                                <div style="font-size: 2rem; margin-right: 15px;">📚</div>
                                <div>
                                    <div style="font-size: 1.2rem; font-weight: bold;">{lesson_id.replace('_', ' ').title()}</div>
                                    <div style="font-size: 0.9rem; color: #666;">Specjalna lekcja dostępna do odblokowania</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a button to unlock this special lesson
                        if st.button(f"Odblokuj lekcję", key=f"unlock_lesson_{lesson_id}"):
                            success, message = activate_item(st.session_state.username, 'special_lesson', lesson_id)
                            if success:
                                notification(message, type="success")
                                st.rerun()
                            else:
                                notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych specjalnych lekcji. Kup je w sklepie!")
                if st.button("Przejdź do sklepu", key="go_to_shop_lessons"):
                    st.session_state.page = 'shop'
                    st.rerun()
        
        # Tab for Boosters
        with inv_tabs[3]:
            st.subheader("Twoje Boostery")
            
            if inventory['boosters']:
                # Display active boosters
                for booster_id, booster_data in inventory['boosters'].items():
                    is_active, expiration = is_booster_active(st.session_state.username, booster_id)
                    status = "Aktywny" if is_active else "Nieaktywny"
                    status_color = "#4CAF50" if is_active else "#F44336"
                    
                    # Format time remaining
                    time_remaining = format_time_remaining(expiration) if is_active else "Wygasł"
                    
                    st.markdown(f"""
                    <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 15px;">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div style="display: flex; align-items: center;">
                                <div style="font-size: 2rem; margin-right: 15px;">⚡</div>
                                <div>
                                    <div style="font-size: 1.2rem; font-weight: bold;">{booster_id.replace('_', ' ').title()}</div>
                                    <div style="font-size: 0.9rem; color: #666;">{time_remaining}</div>
                                </div>
                            </div>
                            <div style="font-size: 0.9rem; font-weight: bold; color: {status_color};">{status}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add button to reactivate if not active
                    if not is_active:
                        if st.button(f"Reaktywuj {booster_id.replace('_', ' ').title()}", key=f"reactivate_booster_{booster_id}"):
                            success, message = activate_item(st.session_state.username, 'booster', booster_id)
                            if success:
                                notification(message, type="success")
                                st.rerun()
                            else:
                                notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych boosterów. Kup je w sklepie!")
                if st.button("Przejdź do sklepu", key="go_to_shop_boosters"):
                    st.session_state.page = 'shop'
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
      # Tab 3: Badges - Use the new categorized badge system
    with tab3:
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        
        # Call the new badge section with 9 thematic categories
        show_badges_section()
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
      # Tab 4: Neuroleader Type - Test Results
    with tab4:
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        
        # Check for test results - support both old and new field names
        neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type')
        test_taken = user_data.get('test_taken', False)
        has_test_scores = 'test_scores' in user_data
        
        if neuroleader_type and (test_taken or has_test_scores):
            # User has completed the test - show results
            st.markdown("### 🧠 Twoje wyniki testu neuroleadera")
            
            # Get neuroleader color for styling
            neuroleader_color = NEUROLEADER_TYPES.get(neuroleader_type, {}).get('color', '#3498db')
            
            # Header with prominent display of result
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; border-radius: 10px; 
                        background: linear-gradient(135deg, {neuroleader_color}20, {neuroleader_color}10);
                        border: 2px solid {neuroleader_color}40; margin-bottom: 20px;'>
                <h3 style='color: {neuroleader_color}; margin-bottom: 10px;'>
                    🧬 Twój dominujący typ neuroleadera
                </h3>
                <h2 style='color: {neuroleader_color}; margin: 10px 0;'>{neuroleader_type}</h2>
                <p style='color: #666; margin: 0;'>
                    {NEUROLEADER_TYPES.get(neuroleader_type, {}).get('description', '')}
                </p>
            </div>
            """, unsafe_allow_html=True)            
            if neuroleader_type in NEUROLEADER_TYPES:
                # Radar chart if test scores are available
                if has_test_scores:
                    st.subheader("📊 Twój szczegółowy profil")
                    
                    # Ensure the radar chart is responsive by passing device_type
                    radar_fig = plot_radar_chart(user_data['test_scores'], device_type=device_type)
                    
                    # Add mobile-specific styles for the chart container
                    if device_type == 'mobile':
                        st.markdown("""
                        <style>
                        .radar-chart-container {
                            margin: 0 -20px; /* Negative margin to use full width on mobile */
                            padding-bottom: 15px;
                        }
                        </style>
                        <div class="radar-chart-container">
                        """, unsafe_allow_html=True)
                        
                    st.pyplot(radar_fig)
                    
                    if device_type == 'mobile':
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # Strengths and challenges - responsive layout
                if device_type == 'mobile':
                    # Na telefonach wyświetl sekcje jedna pod drugą
                    content_section(
                        "💪 Twoje mocne strony", 
                        "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[neuroleader_type]["strengths"]]),
                        icon="💪",
                        border_color="#27ae60",
                        collapsed=False
                    )
                    
                    content_section(
                        "🚧 Obszary do rozwoju", 
                        "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[neuroleader_type]["challenges"]]),
                        icon="🔍",
                        border_color="#e74c3c",
                        collapsed=False
                    )
                else:
                    # Na tabletach i desktopach użyj dwóch kolumn
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        content_section(
                            "💪 Twoje mocne strony", 
                            "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[neuroleader_type]["strengths"]]),
                            icon="💪",
                            border_color="#27ae60",
                            collapsed=False
                        )
                    
                    with col2:
                        content_section(
                            "🚧 Obszary do rozwoju", 
                            "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[neuroleader_type]["challenges"]]),
                            icon="🔍",
                            border_color="#e74c3c",
                            collapsed=False
                        )
                
                # Rekomendowana strategia
                strategy = NEUROLEADER_TYPES.get(neuroleader_type, {}).get('strategy', '')
                if strategy:
                    st.markdown(f"""
                    <div style='padding: 15px; background-color: #f0f8ff; border-left: 4px solid {neuroleader_color}; 
                                border-radius: 5px; margin: 20px 0;'>
                        <h4 style='color: {neuroleader_color}; margin-top: 0;'>🎯 Rekomendowana strategia:</h4>
                        <p style='margin-bottom: 0;'>{strategy}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed description
                if neuroleader_type in degen_details:
                    content_section(
                        "📚 Szczegółowy opis twojego typu neuroleadera", 
                        degen_details[neuroleader_type],
                        icon="📚",
                        collapsed=True
                    )
                
                # Option to retake the test
                st.markdown("---")
                if zen_button("🔄 Wykonaj test ponownie", key="retake_neuroleader_test"):
                    # Reset test data
                    users_data = load_user_data()
                    if 'test_scores' in users_data[st.session_state.username]:
                        del users_data[st.session_state.username]['test_scores']
                    if 'neuroleader_type' in users_data[st.session_state.username]:
                        del users_data[st.session_state.username]['neuroleader_type']
                    if 'degen_type' in users_data[st.session_state.username]:
                        del users_data[st.session_state.username]['degen_type']
                    users_data[st.session_state.username]['test_taken'] = False
                    save_user_data(users_data)
                    
                    # Redirect to test
                    st.session_state.page = 'degen_test'
                    st.session_state.test_step = 0
                    st.session_state.show_test_info = True
                    st.rerun()
            else:
                st.warning("Szczegółowy opis dla tego typu neuroleadera nie jest jeszcze dostępny.")
        else:
            # User hasn't taken the test - encourage them to take it
            st.markdown("### 🧠 Test neuroleadera")
            st.markdown("""
            <div style='text-align: center; padding: 30px; border-radius: 10px; 
                        background: linear-gradient(135deg, #667eea20, #764ba240);
                        border: 2px dashed #667eea; margin-bottom: 20px;'>
                <h3 style='color: #667eea; margin-bottom: 15px;'>
                    🎯 Odkryj swój typ neuroleadera!
                </h3>
                <p style='color: #666; margin-bottom: 20px;'>
                    Jeszcze nie wykonałeś testu neuroleadera. Poznaj swój styl przywództwa 
                    i otrzymaj spersonalizowane rekomendacje rozwoju.
                </p>
                <p style='color: #888; font-size: 0.9em;'>
                    Test składa się z kilku pytań i zajmuje około 5 minut. 
                    Po zakończeniu zobaczysz szczegółowy profil ze swoimi mocnymi stronami i obszarami do rozwoju.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if zen_button("🚀 Rozpocznij test neuroleadera", key="start_neuroleader_test"):
                st.session_state.page = 'degen_test'
                st.session_state.show_test_info = True
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def show_badges_section():
    """Wyświetla odznaki użytkownika"""
    # Add CSS for badge containers
    st.markdown("""
    <style>
    .badge-container {
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .badge-container.unlocked {
        background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
        border: 2px solid #27ae60;
    }
    
    .badge-container.locked {
        background: linear-gradient(135deg, #f5f5f5, #eeeeee);
        border: 2px solid #bdc3c7;
        opacity: 0.6;
    }
    
    .badge-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .badge-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
        display: block;
    }
    
    .badge-name {
        font-weight: bold;
        font-size: 1.1rem;
        color: #2c3e50;
        margin-bottom: 5px;
    }
    
    .badge-description {
        font-size: 0.9rem;
        color: #7f8c8d;
        line-height: 1.3;
    }
    
    .locked .badge-name,
    .locked .badge-description {
        color: #95a5a6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    user_badges = user_data.get("badges", [])
    
    if not user_badges:
        st.subheader("Dostępne odznaki")
        st.info("Jeszcze nie masz żadnych odznak. Rozpocznij naukę i wykonuj zadania, aby je zdobyć!")
    else:
        st.subheader("Twoje odznaki")
      # Pogrupuj odznaki według kategorii neuroleaderstwa z opisami
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
    
    # Pokaż odznaki w kategoriach z opisami
    tab_names = list(badge_categories.keys())
    tabs = st.tabs(tab_names)
    
    for i, (category, category_data) in enumerate(badge_categories.items()):
        with tabs[i]:
            # Wyświetl opis kategorii
            st.markdown(f"**{category_data['description']}**")
            st.markdown("---")
            
            badge_ids = category_data['badges']
            
            # Check if any badges from this category exist in the BADGES config
            valid_badge_ids = [badge_id for badge_id in badge_ids if badge_id in BADGES]
            
            if not valid_badge_ids:
                st.warning(f"Brak odznak w kategorii {category}")
                continue
                
            cols = st.columns(3)
            badges_displayed = 0
            
            # Najpierw pokaż odblokowane odznaki
            for badge_id in valid_badge_ids:
                if badge_id in user_badges:
                    badge_info = BADGES[badge_id]
                    with cols[badges_displayed % 3]:
                        st.markdown(f"""
                        <div class="badge-container unlocked">
                            <div class="badge-icon">{badge_info['icon']}</div>
                            <div class="badge-name">{badge_info['name']}</div>
                            <div class="badge-description">{badge_info['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    badges_displayed += 1
            
            # Potem pokaż zablokowane odznaki
            for badge_id in valid_badge_ids:
                if badge_id not in user_badges:
                    badge_info = BADGES[badge_id]
                    with cols[badges_displayed % 3]:
                        st.markdown(f"""
                        <div class="badge-container locked">
                            <div class="badge-icon">🔒</div>
                            <div class="badge-name">{badge_info['name']}</div>
                            <div class="badge-description">{badge_info['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    badges_displayed += 1
