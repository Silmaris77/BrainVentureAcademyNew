import json
import os
from datetime import datetime
import streamlit as st
from data.users import load_user_data, save_user_data

def save_lesson_progress(username, lesson_id, step, notes=None):
    """Save user's progress in a lesson"""
    progress_file = 'lesson_progress.json'
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
    else:
        progress_data = {}
    
    if username not in progress_data:
        progress_data[username] = {}
    
    progress_data[username][str(lesson_id)] = {
        'current_step': step,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'notes': notes or {},
        'bookmarks': progress_data.get(username, {}).get(str(lesson_id), {}).get('bookmarks', [])
    }
    
    with open(progress_file, 'w') as f:
        json.dump(progress_data, f)

def get_lesson_progress(username, lesson_id):
    """Get user's progress in a lesson"""
    if os.path.exists('lesson_progress.json'):
        with open('lesson_progress.json', 'r') as f:
            progress_data = json.load(f)
            
        if username in progress_data and str(lesson_id) in progress_data[username]:
            return progress_data[username][str(lesson_id)]
    
    return {
        'current_step': 'intro',
        'notes': {},
        'bookmarks': []
    }

def save_lesson_note(username, lesson_id, step, note):
    """Save a note for a specific part of the lesson"""
    progress = get_lesson_progress(username, lesson_id)
    if 'notes' not in progress:
        progress['notes'] = {}
    
    if step not in progress['notes']:
        progress['notes'][step] = []
    
    note_entry = {
        'text': note,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    progress['notes'][step].append(note_entry)
    
    save_lesson_progress(username, lesson_id, progress['current_step'], progress['notes'])

def add_bookmark(username, lesson_id, step, description):
    """Add a bookmark to a specific part of the lesson"""
    progress = get_lesson_progress(username, lesson_id)
    
    bookmark = {
        'step': step,
        'description': description,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if 'bookmarks' not in progress:
        progress['bookmarks'] = []
    
    progress['bookmarks'].append(bookmark)
    save_lesson_progress(username, lesson_id, progress['current_step'], progress.get('notes', {}))

def get_bookmarks(username, lesson_id):
    """Get all bookmarks for a lesson"""
    progress = get_lesson_progress(username, lesson_id)
    return progress.get('bookmarks', [])

def award_fragment_xp(lesson_id, fragment_type, xp_amount):
    """
    Przyznaj XP za ukończenie fragmentu lekcji
    
    Args:
        lesson_id: ID lekcji
        fragment_type: 'intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary'
        xp_amount: Ilość XP do przyznania
    """
    users_data = load_user_data()
    username = st.session_state.username
    
    if username in users_data:
        user_data = users_data[username]
        
        # Struktura: lesson_progress[lesson_id][fragment_type] = {'completed': True, 'xp_awarded': 10}
        lesson_progress = user_data.get('lesson_progress', {})
        
        if lesson_id not in lesson_progress:
            lesson_progress[lesson_id] = {}
          # Sprawdź czy XP za ten fragment już zostało przyznane
        fragment_key = f"{fragment_type}_xp_awarded"
        if not lesson_progress[lesson_id].get(fragment_key, False):
            # Dodaj XP
            current_xp = user_data.get('xp', 0)
            user_data['xp'] = current_xp + xp_amount
            
            # Dodaj Neurocoin równe ilości XP ← KLUCZOWA FUNKCJONALNOŚĆ
            current_neurocoin = user_data.get('neurocoin', 0)
            user_data['neurocoin'] = current_neurocoin + xp_amount
            
            # Zaznacz że XP zostało przyznane
            lesson_progress[lesson_id][fragment_key] = True
            lesson_progress[lesson_id][f"{fragment_type}_completed"] = True
            lesson_progress[lesson_id][f"{fragment_type}_xp"] = xp_amount
            lesson_progress[lesson_id][f"{fragment_type}_neurocoin"] = xp_amount  # ← NOWE
            lesson_progress[lesson_id][f"{fragment_type}_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            user_data['lesson_progress'] = lesson_progress
            
            # Zapisz dane
            users_data[username] = user_data
            save_user_data(users_data)
            
            # Odśwież session_state
            st.session_state.user_data = user_data
            
            return True, xp_amount
    
    return False, 0

def get_lesson_fragment_progress(lesson_id):
    """Pobierz postęp fragmentów dla danej lekcji"""
    users_data = load_user_data()
    username = st.session_state.username
    
    if username in users_data:
        lesson_progress = users_data[username].get('lesson_progress', {})
        return lesson_progress.get(lesson_id, {})
    
    return {}

def calculate_lesson_completion(lesson_id):
    """Oblicz procent ukończenia lekcji"""
    progress = get_lesson_fragment_progress(lesson_id)
    
    # Nowa struktura z practical_exercises lub backward compatibility
    if progress.get('practical_exercises_completed', False):
        # Nowa struktura neuroleadership - 6 kroków
        steps = ['intro', 'opening_quiz', 'content', 'practical_exercises', 'closing_quiz', 'summary']
    else:
        # Stara struktura - 7 kroków (backward compatibility)
        steps = ['intro', 'opening_quiz', 'content', 'reflection', 'application', 'closing_quiz', 'summary']
    
    completed = sum(1 for step in steps if progress.get(f"{step}_completed", False))
    
    return (completed / len(steps)) * 100

def is_lesson_fully_completed(lesson_id):
    """Sprawdź czy lekcja jest w pełni ukończona"""
    return calculate_lesson_completion(lesson_id) == 100

def get_fragment_xp_breakdown(lesson_total_xp):
    """Oblicz podział XP na fragmenty lekcji"""
    return {
        'intro': int(lesson_total_xp * 0.3),    # 30% za wprowadzenie
        'content': int(lesson_total_xp * 0.5),  # 50% za treść
        'quiz': int(lesson_total_xp * 0.2)      # 20% za quiz (+ bonus za wynik)
    }

def mark_lesson_as_completed(lesson_id):
    """Oznacz lekcję jako w pełni ukończoną"""
    users_data = load_user_data()
    username = st.session_state.username
    
    if username in users_data:
        user_data = users_data[username]
        completed_lessons = user_data.get('completed_lessons', [])
        
        if lesson_id not in completed_lessons:
            completed_lessons.append(lesson_id)
            user_data['completed_lessons'] = completed_lessons
            
            # Zapisz dane
            users_data[username] = user_data
            save_user_data(users_data)
            
            # Odśwież session_state
            st.session_state.user_data = user_data
            
            return True
    
    return False