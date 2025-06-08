import streamlit as st
import random
import os
from utils.components import zen_header
from utils.material3_components import apply_material3_theme, m3_card
from views.fix_card import m3_fixed_card  # Nasza naprawiona wersja karty
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view, apply_responsive_styles
from utils.inspirations_loader import get_blog_articles, get_tutorials, get_facts, load_inspiration_content

def show_inspirations():
    """
    Wyświetla zakładkę Inspiracje z trzema podstronami:
    - Blog: artykuły i posty na temat neuroleadershipu
    - Tutoriale: poradniki i instruktaże
    - Ciekawostki: interesujące fakty i odkrycia naukowe
    """
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
      # Zastosuj responsywne style
    apply_responsive_styles()
    
    # Dodaj custom CSS dla spójnego wyglądu zen_header
    st.markdown("""
    <style>
    /* Kompensacja marginesów dla zen_header w Inspiracjach */
    .zen_header {
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        padding: 15px 10px !important;
        width: 100% !important;
    }
    
    /* Zapewnij pełną szerokość header */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Dodatkowe style dla spójności z innymi zakładkami */
    [data-testid="stMarkdownContainer"]:first-child {
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Wyświetl nagłówek
    zen_header("Inspiracje 💡")
    
    st.markdown("*Odkryj interesujące treści, które poszerzą Twoje rozumienie neuroleadershipu*")
      # Zakładki
    tab1, tab2, tab3 = st.tabs(["📝 Blog", "🎓 Tutoriale", "🧠 Ciekawostki"])
    
    # Zakładka 1: Blog
    with tab1:
        st.markdown("### Artykuły i Posty")
        st.markdown("Najnowsze teksty z dziedziny neuroleadershipu i zarządzania.")
        
        # Pobieramy artykuły z systemu plików
        blog_articles = get_blog_articles()
        
        # Dodajemy opcje filtrowania
        if blog_articles:
            # Opcje wyszukiwania i filtrowania
            col1, col2 = st.columns([3, 1])
            with col1:
                search_query = st.text_input("🔍 Wyszukaj artykuł", "")
            with col2:
                sort_option = st.selectbox("Sortuj według", ["Najnowsze", "Najstarsze", "Alfabetycznie"])
            
            # Filtrujemy i sortujemy artykuły
            filtered_articles = blog_articles
            if search_query:
                filtered_articles = [a for a in blog_articles if search_query.lower() in a['title'].lower() 
                                    or search_query.lower() in a['content'].lower() 
                                    or search_query.lower() in a['author'].lower()]
            
            # Sortowanie
            if sort_option == "Najnowsze":
                filtered_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
            elif sort_option == "Najstarsze":
                filtered_articles = sorted(filtered_articles, key=lambda x: x['date'])
            elif sort_option == "Alfabetycznie":
                filtered_articles = sorted(filtered_articles, key=lambda x: x['title'])
            
            if not filtered_articles:
                st.info("Nie znaleziono artykułów pasujących do wyszukiwania.")
                
            # Wyświetl artykuły
            for article in filtered_articles:
                col1, col2 = st.columns([6, 1])
                with col1:
                    m3_fixed_card(
                        title=f"{article['title']}",
                        icon=article['icon'],
                        content=f"{article['content']}<br><br><i>Autor: {article['author']} | Opublikowano: {article['date']}</i>"
                    )
                with col2:
                    if st.button("Czytaj więcej", key=f"read_more_{article['id']}"):
                        st.session_state['current_article'] = article
                        st.session_state['show_article_detail'] = True                
                        st.markdown("<br>", unsafe_allow_html=True)
            
            # Wyświetlanie pełnego artykułu
            if st.session_state.get('show_article_detail', False) and 'current_article' in st.session_state:
                article = st.session_state['current_article']
                with st.expander(f"{article['icon']} {article['title']}", expanded=True):
                    # Pobierz pełną treść artykułu z pliku
                    content = load_inspiration_content(article['file_path'])
                    st.markdown(content, unsafe_allow_html=True)
                    st.markdown(f"<i>Autor: {article['author']} | Opublikowano: {article['date']}</i>", unsafe_allow_html=True)
                    if st.button("Zamknij artykuł"):
                        st.session_state['show_article_detail'] = False
                        st.rerun()
        else:
            st.info("Aktualnie brak dostępnych artykułów.")
      # Zakładka 2: Tutoriale
    with tab2:
        st.markdown("### Praktyczne Poradniki")
        st.markdown("Tutoriale i przewodniki, które pomogą Ci zastosować wiedzę z neuroleadershipu w praktyce.")
        
        # Pobieramy tutoriale z systemu plików
        tutorials = get_tutorials()
        
        if tutorials:
            # Opcje wyszukiwania i filtrowania
            col1, col2 = st.columns([3, 1])
            with col1:
                search_query = st.text_input("🔍 Wyszukaj tutorial", key="tutorial_search")
            with col2:
                sort_option = st.selectbox("Sortuj według", ["Najnowsze", "Poziom trudności", "Alfabetycznie"], key="tutorial_sort")
            
            # Filtrujemy tutoriale
            filtered_tutorials = tutorials
            if search_query:
                filtered_tutorials = [t for t in tutorials if search_query.lower() in t['title'].lower() 
                                     or search_query.lower() in t['content'].lower()
                                     or search_query.lower() in t.get('tags', [])]
            
            # Sortowanie
            if sort_option == "Najnowsze":
                # Tutaj możemy sortować po ID lub innym polu, dla przykładu sortujemy po ID
                filtered_tutorials = sorted(filtered_tutorials, key=lambda x: x['id'], reverse=True)
            elif sort_option == "Poziom trudności":
                # Mapowanie poziomów trudności do wartości liczbowych
                level_map = {"Początkujący": 1, "Średniozaawansowany": 2, "Zaawansowany": 3}
                filtered_tutorials = sorted(filtered_tutorials, key=lambda x: level_map.get(x['level'], 0))
            elif sort_option == "Alfabetycznie":
                filtered_tutorials = sorted(filtered_tutorials, key=lambda x: x['title'])
            
            if not filtered_tutorials:
                st.info("Nie znaleziono tutoriali pasujących do wyszukiwania.")
            
            # Wyświetl tutoriale
            for tutorial in filtered_tutorials:
                col1, col2 = st.columns([6, 1])
                with col1:
                    m3_fixed_card(
                        title=f"{tutorial['title']}",
                        icon=tutorial['icon'],
                        content=f"{tutorial['content']}<br><br><b>Czas: </b>{tutorial['duration']} | <b>Poziom:</b> {tutorial['level']}"
                    )
                with col2:
                    if st.button("Zobacz tutorial", key=f"view_tutorial_{tutorial['id']}"):
                        st.session_state['current_tutorial'] = tutorial
                        st.session_state['show_tutorial_detail'] = True
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Wyświetlanie pełnego tutoriala
            if st.session_state.get('show_tutorial_detail', False) and 'current_tutorial' in st.session_state:
                tutorial = st.session_state['current_tutorial']
                with st.expander(f"{tutorial['icon']} {tutorial['title']}", expanded=True):
                    # Pobierz pełną treść tutoriala z pliku
                    content = load_inspiration_content(tutorial['file_path'])
                    st.markdown(content, unsafe_allow_html=True)
                    st.markdown(f"<i><b>Czas:</b> {tutorial['duration']} | <b>Poziom:</b> {tutorial['level']}</i>", unsafe_allow_html=True)
                    if st.button("Zamknij tutorial"):
                        st.session_state['show_tutorial_detail'] = False
                        st.rerun()
        else:
            st.info("Aktualnie brak dostępnych tutoriali.")
      # Zakładka 3: Ciekawostki
    with tab3:
        st.markdown("### Fascynujące Odkrycia")
        st.markdown("Interesujące fakty i odkrycia naukowe z pogranicza neuronauków i zarządzania.")
        
        # Pobieramy ciekawostki z systemu plików
        facts = get_facts()
        
        if facts:
            # Opcje wyszukiwania
            search_query = st.text_input("🔍 Wyszukaj ciekawostki", key="facts_search")
            
            # Filtrujemy ciekawostki
            filtered_facts = facts
            if search_query:
                filtered_facts = [f for f in facts if search_query.lower() in f['title'].lower() 
                                or search_query.lower() in f['content'].lower()
                                or search_query.lower() in f.get('tags', [])]
            
            if not filtered_facts:
                st.info("Nie znaleziono ciekawostek pasujących do wyszukiwania.")
            
            # Wyświetl ciekawostki w układzie siatki
            cols = st.columns(2)
            for i, fact in enumerate(filtered_facts):
                with cols[i % 2]:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        m3_fixed_card(
                            title=f"{fact['title']}",
                            icon=fact['icon'],
                            content=f"{fact['content']}<br><br><i>Źródło: {fact['source']}</i>"
                        )
                    with col2:
                        if st.button("Więcej", key=f"view_fact_{fact['id']}"):
                            st.session_state['current_fact'] = fact
                            st.session_state['show_fact_detail'] = True
                    st.markdown("<br>", unsafe_allow_html=True)
            
            # Wyświetlanie pełnej ciekawostki
            if st.session_state.get('show_fact_detail', False) and 'current_fact' in st.session_state:
                fact = st.session_state['current_fact']
                with st.expander(f"{fact['icon']} {fact['title']}", expanded=True):
                    # Pobierz pełną treść ciekawostki z pliku
                    content = load_inspiration_content(fact['file_path'])
                    st.markdown(content, unsafe_allow_html=True)
                    st.markdown(f"<i>Źródło: {fact['source']}</i>", unsafe_allow_html=True)
                    if st.button("Zamknij"):
                        st.session_state['show_fact_detail'] = False
                        st.rerun()
        else:            st.info("Aktualnie brak dostępnych ciekawostek.")
    
    # Dodatkowe rekomendacje na dole strony
    st.markdown("---")
    st.markdown("### 💫 Polecane dla Ciebie")
    
    # Pobieramy ponownie wszystkie dane, aby mieć pewność, że mamy pełne listy
    all_blog_articles = get_blog_articles()
    all_tutorials = get_tutorials()
    all_facts = get_facts()
    
    # Sprawdzamy, czy mamy elementy z każdej kategorii
    recommendations = []
    
    if all_blog_articles:
        recommendations.append(("article", random.choice(all_blog_articles)))
    
    if all_tutorials:
        recommendations.append(("tutorial", random.choice(all_tutorials)))
        
    if all_facts:
        recommendations.append(("fact", random.choice(all_facts)))
    
    # Wyświetl rekomendacje w jednym rzędzie
    if recommendations:
        cols = st.columns(min(3, len(recommendations)))
        
        for i, (item_type, item) in enumerate(recommendations):
            with cols[i]:
                if item_type == "article":  # artykuł bloga
                    st.markdown(f"**📝 {item['title']}**")
                    st.markdown(f"*{item['author']}*")
                    if st.button("Czytaj", key=f"rec_article_{item['id']}"):
                        st.session_state['current_article'] = item
                        st.session_state['show_article_detail'] = True
                        st.rerun()
                elif item_type == "tutorial":  # tutorial
                    st.markdown(f"**🎓 {item['title']}**")
                    st.markdown(f"*Czas: {item['duration']}*")
                    if st.button("Zobacz", key=f"rec_tutorial_{item['id']}"):
                        st.session_state['current_tutorial'] = item
                        st.session_state['show_tutorial_detail'] = True
                        st.rerun()
                else:  # ciekawostka
                    st.markdown(f"**🧠 {item['title']}**")
                    st.markdown(f"*{item['source']}*")
                    if st.button("Odkryj", key=f"rec_fact_{item['id']}"):
                        st.session_state['current_fact'] = item
                        st.session_state['show_fact_detail'] = True
                        st.rerun()
