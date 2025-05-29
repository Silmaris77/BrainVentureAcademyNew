import streamlit as st
import pandas as pd
import altair as alt
import json
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Dodaj ścieżkę główną projektu do systemu, aby móc importować moduły
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.neuroleader_details import degen_details
from data.test_questions import NEUROLEADER_TYPES, TEST_QUESTIONS
from utils.components import zen_header, zen_button, notification
from utils.material3_components import apply_material3_theme
from data.users import load_user_data, save_user_data

def show_degen_types():
    """Wyświetla nową zakładkę Typy Neuroleaderów, zawierającą test i eksplorator typów neuroleaderów"""
    
    apply_material3_theme()
    
    # Utwórz tabs dla podsekcji
    tab1, tab2 = st.tabs(["Test Neuroleadera", "Eksplorator Typów"])
    
    with tab1:
        show_degen_test_content()
    
    with tab2:
        show_degen_explorer_content()


def show_degen_test_content():
    """Wyświetla zawartość testu typu neuroleadera"""
    
    zen_header("Test Typu Neuroleadera 🎭")
    
    st.markdown("""
    ## Odkryj swój typ przywódcy
    
    Ten test pozwoli Ci lepiej poznać swój profil psychologiczny jako lidera. 
    Odpowiedz szczerze na poniższe pytania, aby otrzymać swój profil neuroleadera.
    
    ### Instrukcje:
    * Test składa się z 10 pytań
    * Przy każdym pytaniu zaznacz odpowiedź, która najlepiej Cię opisuje
    * Na końcu otrzymasz wynik wraz z opisem Twojego profilu
    * Wyniki testu zostaną zapisane w Twoim profilu
    """)
      # Sprawdź, czy użytkownik już wypełnił test
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Check both old nested format and new unified format
    test_results = user_data.get("degen_test", None)
    has_test_scores = user_data.get("test_scores", None) is not None
    user_degen_type = user_data.get("degen_type", None)
    
    if "reset_test" not in st.session_state:
        st.session_state.reset_test = False
        
    # User has completed test if either format exists
    if (test_results or has_test_scores) and not st.session_state.reset_test:
        # Get the degen type from either format
        degen_type = user_degen_type or (test_results['degen_type'] if test_results else None)
        
        if degen_type:
            st.success(f"Już wypełniłeś test! Twój typ neuroleadera to: {degen_type}")
            
            # Wyświetl szczegóły typu
            show_degen_type_details(degen_type)
        
        # Przycisk do resetowania testu
        if st.button("Wypełnij test ponownie"):
            st.session_state.reset_test = True
            st.rerun()
    else:
        # Użytkownik nie wypełnił testu lub chce go zresetować
        run_test()


def run_test():
    """Uruchamia test typu degena"""
    
    # Użyj bezpośrednio TEST_QUESTIONS z importu
    questions = TEST_QUESTIONS
    
    # Inicjalizacja stanu pytań
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = []
        
    if st.session_state.current_question < len(questions):
        # Wyświetl aktualne pytanie
        question = questions[st.session_state.current_question]
        
        st.markdown(f"### Pytanie {st.session_state.current_question + 1} / {len(questions)}")
        st.markdown(f"**{question['question']}**")
          # Pokaż odpowiedzi jako przyciski
        answered = False
        
        for i, option in enumerate(question['options']):
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(option['text'], key=f"answer_{i}", use_container_width=True):
                    # Zapisz wyniki dla tej odpowiedzi
                    if 'scores' not in st.session_state:
                        st.session_state.scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
                      # Dodaj punkty z wybranej odpowiedzi
                    for neuroleader_type, score in option['scores'].items():
                        st.session_state.scores[neuroleader_type] = st.session_state.scores.get(neuroleader_type, 0) + score
                    
                    st.session_state.current_question += 1
                    answered = True
        
        if answered:
            st.rerun()
            
    else:
        # Wszystkie pytania zostały odpowiedziane - oblicz wyniki
        calculate_results()


def calculate_results():
    """Oblicza wyniki testu i zapisuje je w profilu użytkownika"""
      # Użyj zebranych punktów dla każdego typu neuroleadera
    if 'scores' not in st.session_state:
        st.session_state.scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
    
    # Określ dominujący typ na podstawie punktacji
    dominant_type = max(st.session_state.scores.items(), key=lambda x: x[1])[0]
      # Zapisz wyniki - unified format with other test implementations
    users_data = load_user_data()
    
    # Maintain compatibility with both field names and consistent format
    users_data[st.session_state.username]["neuroleader_type"] = dominant_type
    users_data[st.session_state.username]["degen_type"] = dominant_type  # For backward compatibility
    users_data[st.session_state.username]["test_taken"] = True
    users_data[st.session_state.username]["test_scores"] = st.session_state.scores  # Use test_scores key for consistency
    users_data[st.session_state.username]["xp"] = users_data[st.session_state.username].get("xp", 0) + 50  # Bonus XP for completing the test
    
    # Also save detailed test results for backward compatibility
    test_results = {
        "degen_type": dominant_type,
        "scores": st.session_state.scores,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    users_data[st.session_state.username]["degen_test"] = test_results
    
    save_user_data(users_data)
      # Pokaż wyniki
    st.balloons()
    st.success(f"Test zakończony! Twój typ neuroleadera to: {dominant_type}")
    
    # Wyświetl szczegóły typu
    show_degen_type_details(dominant_type)
    
    # Resetuj stan testu
    st.session_state.reset_test = False
    del st.session_state.current_question
    del st.session_state.answers
    
    # Dodaj przycisk do powrotu do głównej strony
    if st.button("Wróć do dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


def show_degen_type_details(neuroleader_type):
    """Wyświetla szczegółowe informacje o typie neuroleadera"""
    
    # Pobierz dane o typie neuroleadera z dostępnych struktur danych
    neuroleader_type_data = NEUROLEADER_TYPES.get(neuroleader_type, {})
    description = neuroleader_type_data.get("description", "Brak opisu")
    strengths = neuroleader_type_data.get("strengths", [])
    challenges = neuroleader_type_data.get("challenges", [])
    strategy = neuroleader_type_data.get("strategy", "")
    
    # Pobierz pełny opis z degen_details
    full_details = degen_details.get(neuroleader_type, "")
    
    # Tytuł i opis
    st.markdown(f"## Twój typ neuroleadera: {neuroleader_type}")
    
    # Opis krótki
    st.markdown(f"**{description}**")
    
    # Pełny opis w expander
    with st.expander("Szczegółowy opis Twojego typu", expanded=False):
        # Mocne strony
        st.markdown("#### 💪 Mocne strony:")
        for strength in strengths:
            st.markdown(f"- {strength}")
        
        # Wyzwania
        st.markdown("#### 🤔 Wyzwania:")
        for challenge in challenges:
            st.markdown(f"- {challenge}")
        
        # Strategia
        st.markdown("#### 🚀 Strategia rozwoju:")
        st.markdown(f"- {strategy}")
        
        # Pełny opis z degen_details jeśli istnieje
        if full_details:
            st.markdown("#### 📝 Pełny opis:")
            st.markdown(full_details)


def show_degen_explorer_content():
    """Wyświetla zawartość eksploratora typów neuroleaderów"""
    
    zen_header("Eksplorator Typów Neuroleaderów 🔍")
    st.markdown("""
    ## Poznaj wszystkie profile przywódcy
    
    Każdy przywódca ma swój unikalny styl podejmowania decyzji. Poznaj charakterystyki wszystkich typów i ich
    mocne strony oraz wyzwania.
    """)
    
    # Wybierz typ do eksploracji
    neuroleader_type = st.selectbox(
        "Wybierz typ neuroleadera do eksploracji:",
        list(NEUROLEADER_TYPES.keys())
    )
    
    # Wyświetl szczegóły wybranego typu
    show_degen_type_details(neuroleader_type)
    
    # Dodaj sekcję porównania
    with st.expander("Porównaj wszystkie typy", expanded=False):
        show_comparison_table()


def show_comparison_table():
    """Wyświetla tabelę porównawczą wszystkich typów neuroleaderów"""
    
    st.markdown("### Porównanie typów neuroleaderów")
    
    # Przygotuj dane do tabeli z faktycznych danych NEUROLEADER_TYPES
    neuroleader_types_list = list(NEUROLEADER_TYPES.keys())
    descriptions = [NEUROLEADER_TYPES[t].get("description", "") for t in neuroleader_types_list]
    
    # Przygotuj listy mocnych stron i wyzwań
    strengths_list = []
    challenges_list = []
    strategies_list = []
    
    for t in neuroleader_types_list:
        # Pozyskaj listę mocnych stron i połącz w string
        strengths = NEUROLEADER_TYPES[t].get("strengths", [])
        strengths_str = ", ".join(strengths) if strengths else "Brak danych"
        strengths_list.append(strengths_str)
        
        # Pozyskaj listę wyzwań i połącz w string
        challenges = NEUROLEADER_TYPES[t].get("challenges", [])
        challenges_str = ", ".join(challenges) if challenges else "Brak danych"
        challenges_list.append(challenges_str)
        
        # Pozyskaj strategię
        strategy = NEUROLEADER_TYPES[t].get("strategy", "Brak danych")
        strategies_list.append(strategy)
      # Utwórz słownik danych do tabeli
    comparison_data = {
        'Typ neuroleadera': neuroleader_types_list,
        'Opis': descriptions,
        'Mocne strony': strengths_list,
        'Wyzwania': challenges_list,
        'Strategia': strategies_list
    }
    
    # Wyświetl tabelę
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    # Dodaj wizualizację typów
    st.markdown("### Wizualizacja cech typów przywódcy")
    
    # Przygotuj dane do wykresu - najprostsze podejście z konkretnymi wartościami
    chart_data = pd.DataFrame({
        'Kategoria': ['Szybkość decyzji', 'Analityczność', 'Zarządzanie ryzykiem', 'Adaptacja do zmian'],
    })
    
    # Dodaj kolumny dla każdego typu neuroleadera
    for idx, neuroleader_type in enumerate(NEUROLEADER_TYPES.keys()):
        # Generowanie różnych wartości dla każdego typu używając indeksu
        values = []
        for i in range(4):
            # Generuj wartości w zakresie 20-90 bazując na indeksie typu i kategorii
            base_value = ((idx * 17) + (i * 19)) % 70 + 20
            values.append(base_value)
        
        # Dodaj jako nową kolumnę
        chart_data[neuroleader_type] = values
    
    # Przekształć dane do formatu długiego
    chart_data_long = pd.melt(
        chart_data, 
        id_vars=['Kategoria'], 
        var_name='Typ neuroleadera', 
        value_name='Wartość'
    )
    
    # Stwórz wykres słupkowy porównawczy
    chart = alt.Chart(chart_data_long).mark_bar().encode(
        x=alt.X('Typ neuroleadera:N', title=None),
        y=alt.Y('Wartość:Q', title='Poziom cechy (0-100)'),
        color=alt.Color('Typ neuroleadera:N', legend=None),
        column=alt.Column('Kategoria:N', title=None)
    ).properties(
        width=alt.Step(80)
    )
    
    st.altair_chart(chart, use_container_width=True)
