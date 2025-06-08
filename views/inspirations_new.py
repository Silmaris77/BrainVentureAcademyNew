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
    """    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Dodaj globalne style dla lepszego formatowania tekstu
    # Usunięto bezpośrednie stylowanie zen_header, aby polegać na globalnych lub domyślnych stylach komponentu
    # dla spójności z innymi zakładkami, takimi jak Dashboard.
    # Jeśli specyficzne dostosowania są nadal potrzebne, można je dodać tutaj,
    # ale z uwzględnieniem globalnej spójności.

    st.markdown("""
    <style>
    /* Globalne style dla zakładki Inspiracje */
    /* Zmieniono selektor z .stMarkdown na .stTabs .stMarkdown, aby style dotyczyły tylko treści wewnątrz zakładek */
    .stTabs .stMarkdown {
        text-align: justify !important;
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding: 0 2rem !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f5f5f5;
        border-radius: 12px;
        color: #666;
        border: none;
        padding: 0 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2196F3 !important;
        color: white !important;
    }
      /* Lepsze marginesy dla tekstu głównego - zachowujemy to, jeśli jest potrzebne dla treści */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important; /* Dodano dla symetrii */
        /* padding-top: 1rem !important; Usunięto lub dostosowano, aby nie kolidowało z zen_header */
    }

    /* Upewnij się, że pierwszy element markdown nie dodaje niepotrzebnego marginesu na górze,
       co mogłoby wpływać na pozycję zen_header lub elementów bezpośrednio pod nim. */
    [data-testid="stMarkdownContainer"]:first-child {
       margin-top: 0 !important; /* Może być potrzebne, jeśli zen_header jest renderowany wewnątrz markdown */
    }
    </style>
    """, unsafe_allow_html=True)

    # Używamy naszego komponentu nagłówka - spójnie z Dashboard
    # Tytuł zostanie ustawiony dynamicznie w zależności od wybranej podstrony
    # zen_header("Inspiracje") # Usunięto stąd, aby tytuł był dynamiczny

    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Zastosuj responsywne style
    apply_responsive_styles()
    
    # Wyświetl nagłówek
    zen_header("Inspiracje 💡")
    
    st.markdown("*Odkryj interesujące treści, które poszerzą Twoje rozumienie neuroleadershipu*")
    
    # Zakładki
    tab1, tab2, tab3 = st.tabs(["📝 Blog", "🎓 Tutoriale", "🧠 Ciekawostki"])
    
    # Inicjalizacja zmiennych stanu
    if 'show_article_detail' not in st.session_state:
        st.session_state['show_article_detail'] = False
    if 'show_tutorial_detail' not in st.session_state:
        st.session_state['show_tutorial_detail'] = False
    if 'show_fact_detail' not in st.session_state:
        st.session_state['show_fact_detail'] = False
    
    # Zakładka 1: Blog
    with tab1:
        st.markdown("### Artykuły i Posty")
        st.markdown("Najnowsze teksty z dziedziny neuroleadershipu i zarządzania.")
        
        # Pobranie artykułów
        blog_articles = get_blog_articles()
          # Wyświetlanie szczegółów lub listy artykułów
        if st.session_state['show_article_detail'] and 'current_article' in st.session_state:
            article = st.session_state['current_article']
            
            # Przycisk powrotu
            if st.button("← Powrót do listy artykułów"):
                st.session_state['show_article_detail'] = False
                st.rerun()            # Dodaj CSS dla marginesów w szczegółowym widoku
            st.markdown("""
            <style>
            .article-detail-container {
                max-width: 800px !important;
                margin: 2rem auto !important;
                padding: 3rem !important;
                line-height: 1.8 !important;
                background-color: white !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
                border: 1px solid #e0e0e0 !important;
            }
            
            .article-detail-container * {
                max-width: 100% !important;
                box-sizing: border-box !important;
            }
            
            .article-detail-container h1, 
            .article-detail-container h2, 
            .article-detail-container h3,
            .article-detail-container h4,
            .article-detail-container h5,
            .article-detail-container h6 {
                margin-top: 3rem !important;
                margin-bottom: 1.8rem !important;
                padding: 0 2rem !important;
                color: #1A237E !important;
                font-weight: 600 !important;
            }
            
            .article-detail-container p {
                margin-bottom: 2rem !important;
                text-align: justify !important;
                line-height: 1.9 !important;
                padding: 0 2rem !important;
                text-indent: 1.5rem !important;
                font-size: 1.1rem !important;
                color: #333 !important;
            }
            
            .article-detail-container ul, 
            .article-detail-container ol {
                margin-left: 3rem !important;
                margin-bottom: 2rem !important;
                padding: 0 2rem !important;
            }
            
            .article-detail-container li {
                margin-bottom: 1rem !important;
                line-height: 1.8 !important;
                text-align: justify !important;
                font-size: 1.1rem !important;
                color: #333 !important;
            }
            
            .article-detail-container hr {
                margin: 3rem 2rem !important;
                border: none !important;
                height: 3px !important;
                background: linear-gradient(90deg, #2196F3, #673AB7) !important;
                border-radius: 2px !important;
            }
            
            .article-detail-container strong, 
            .article-detail-container b {
                color: #1A237E !important;
                font-weight: 700 !important;
            }
            
            .article-detail-container em, 
            .article-detail-container i {
                color: #555 !important;
                font-style: italic !important;
            }
            
            /* Dodatkowe marginesy dla lepszej czytelności */
            .article-detail-container > * {
                margin-left: auto !important;
                margin-right: auto !important;
            }
            </style>
            """, unsafe_allow_html=True)
                
            # Wyświetlanie szczegółów artykułu w kontenerze z marginesami
            st.markdown('<div class="article-detail-container">', unsafe_allow_html=True)
            st.markdown(f"## {article['icon']} {article['title']}")
            st.markdown(f"*Autor: {article['author']} | Opublikowano: {article['date']}*")
            st.markdown("---")
            
            # Pobierz treść artykułu
            content = load_inspiration_content(article['file_path'])
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Wyświetlanie listy artykułów
            if blog_articles:
                # Opcje wyszukiwania i filtrowania
                col1, col2 = st.columns([3, 1])
                with col1:
                    search_query = st.text_input("🔍 Wyszukaj artykuł", "")
                with col2:
                    sort_option = st.selectbox("Sortuj według", ["Najnowsze", "Najstarsze", "Alfabetycznie"])
                
                # Filtrowanie i sortowanie
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
                    
                # Wyświetlanie artykułów
                for article in filtered_articles:
                    col1, col2 = st.columns([6, 1])
                    with col1:
                        m3_fixed_card(
                            title=article['title'],
                            icon=article['icon'],
                            content=f"{article['content']}<br><br><i>Autor: {article['author']} | Opublikowano: {article['date']}</i>"
                        )
                    with col2:
                        if st.button("Czytaj więcej", key=f"read_more_{article['id']}"):
                            st.session_state['current_article'] = article
                            st.session_state['show_article_detail'] = True
                            st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Aktualnie brak dostępnych artykułów.")
    
    # Zakładka 2: Tutoriale
    with tab2:
        st.markdown("### Praktyczne Poradniki")
        st.markdown("Tutoriale i przewodniki, które pomogą Ci zastosować wiedzę z neuroleadershipu w praktyce.")
        
        # Pobranie tutoriali
        tutorials = get_tutorials()
          # Wyświetlanie szczegółów lub listy tutoriali
        if st.session_state['show_tutorial_detail'] and 'current_tutorial' in st.session_state:
            tutorial = st.session_state['current_tutorial']
            
            # Przycisk powrotu
            if st.button("← Powrót do listy tutoriali"):
                st.session_state['show_tutorial_detail'] = False
                st.rerun()            # Dodaj CSS dla marginesów w szczegółowym widoku
            st.markdown("""
            <style>
            .tutorial-detail-container {
                max-width: 800px !important;
                margin: 2rem auto !important;
                padding: 3rem !important;
                line-height: 1.8 !important;
                background-color: white !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
                border: 1px solid #e0e0e0 !important;
            }
            
            .tutorial-detail-container * {
                max-width: 100% !important;
                box-sizing: border-box !important;
            }
            
            .tutorial-detail-container h1, 
            .tutorial-detail-container h2, 
            .tutorial-detail-container h3,
            .tutorial-detail-container h4,
            .tutorial-detail-container h5,
            .tutorial-detail_container h6 {
                margin-top: 3rem !important;
                margin-bottom: 1.8rem !important;
                padding: 0 2rem !important;
                color: #1A237E !important;
                font-weight: 600 !important;
            }
            
            .tutorial-detail-container p {
                margin-bottom: 2rem !important;
                text-align: justify !important;
                line-height: 1.9 !important;
                padding: 0 2rem !important;
                text-indent: 1.5rem !important;
                font-size: 1.1rem !important;
                color: #333 !important;
            }
            
            .tutorial-detail-container ul, 
            .tutorial-detail-container ol {
                margin-left: 3rem !important;
                margin-bottom: 2rem !important;
                padding: 0 2rem !important;
            }
            
            .tutorial-detail-container li {
                margin-bottom: 1rem !important;
                line-height: 1.8 !important;
                text-align: justify !important;
                font-size: 1.1rem !important;
                color: #333 !important;
            }
              .tutorial-detail-container hr {
                margin: 3rem 2rem !important;
                border: none !important;
                height: 3px !important;
                background: linear-gradient(90deg, #2196F3, #673AB7) !important;
                border-radius: 2px !important;
            }
            
            .tutorial-detail-container strong, 
            .tutorial-detail-container b {
                color: #1A237E !important;
                font-weight: 700 !important;
            }
            
            .tutorial-detail-container em, 
            .tutorial-detail-container i {
                color: #555 !important;
                font-style: italic !important;
            }
            </style>
            """, unsafe_allow_html=True)
                
            # Wyświetlanie szczegółów tutoriala w kontenerze z marginesami
            st.markdown('<div class="tutorial-detail-container">', unsafe_allow_html=True)
            st.markdown(f"## {tutorial['icon']} {tutorial['title']}")
            st.markdown(f"**Poziom: {tutorial['level']} | Czas: {tutorial['duration']}**")
            st.markdown("---")
            
            # Pobierz treść tutoriala
            content = load_inspiration_content(tutorial['file_path'])
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Wyświetlanie listy tutoriali
            if tutorials:
                # Opcje filtrowania
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    search_query = st.text_input("🔍 Wyszukaj tutorial", "")
                with col2:
                    levels = ["Wszystkie poziomy"] + list(set([t['level'] for t in tutorials]))
                    level_filter = st.selectbox("Poziom", levels)
                with col3:
                    durations = ["Dowolny czas"] + sorted(list(set([t['duration'] for t in tutorials])))
                    duration_filter = st.selectbox("Czas trwania", durations)
                
                # Filtrowanie tutoriali
                filtered_tutorials = tutorials
                if search_query:
                    filtered_tutorials = [t for t in filtered_tutorials if search_query.lower() in t['title'].lower() 
                                         or search_query.lower() in t['content'].lower()]
                if level_filter != "Wszystkie poziomy":
                    filtered_tutorials = [t for t in filtered_tutorials if t['level'] == level_filter]
                if duration_filter != "Dowolny czas":
                    filtered_tutorials = [t for t in filtered_tutorials if t['duration'] == duration_filter]
                
                if not filtered_tutorials:
                    st.info("Nie znaleziono tutoriali pasujących do kryteriów wyszukiwania.")
                
                # Wyświetlanie tutoriali
                for tutorial in filtered_tutorials:
                    col1, col2 = st.columns([6, 1])
                    with col1:
                        m3_fixed_card(
                            title=tutorial['title'],
                            icon=tutorial['icon'],
                            content=f"{tutorial['content']}<br><br><b>Czas: </b>{tutorial['duration']} | <b>Poziom:</b> {tutorial['level']}"
                        )
                    with col2:
                        if st.button("Zobacz tutorial", key=f"tutorial_{tutorial['id']}"):
                            st.session_state['current_tutorial'] = tutorial
                            st.session_state['show_tutorial_detail'] = True
                            st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Aktualnie brak dostępnych tutoriali.")
    
    # Zakładka 3: Ciekawostki
    with tab3:
        st.markdown("### Fascynujące Odkrycia")
        st.markdown("Interesujące fakty i odkrycia naukowe z pogranicza neuronauków i zarządzania.")
        
        # Pobranie ciekawostek
        facts = get_facts()
          # Wyświetlanie szczegółów lub listy ciekawostek
        if st.session_state['show_fact_detail'] and 'current_fact' in st.session_state:
            fact = st.session_state['current_fact']
            
            # Przycisk powrotu
            if st.button("← Powrót do listy ciekawostek"):
                st.session_state['show_fact_detail'] = False
                st.rerun()
                  # Dodaj CSS dla marginesów w szczegółowym widoku
            st.markdown("""
            <style>
            .fact-detail-container {
                max-width: 800px !important;
                margin: 2rem auto !important;
                padding: 3rem !important;
                line-height: 1.8 !important;
                background-color: white !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
                border: 1px solid #e0e0e0 !important;
            }
            
            .fact-detail-container * {
                max-width: 100% !important;
                box-sizing: border-box !important;
            }
            
            .fact-detail-container h1, 
            .fact-detail-container h2, 
            .fact-detail-container h3,
            .fact-detail-container h4,
            .fact-detail-container h5,
            .fact-detail-container h6 {
                margin-top: 3rem !important;
                margin-bottom: 1.8rem !important;
                padding: 0 2rem !important;
                color: #1A237E !important;
                font-weight: 600 !important;
            }
            
            .fact-detail-container p {
                margin-bottom: 2rem !important;
                text-align: justify !important;
                line-height: 1.9 !important;
                padding: 0 2rem !important;
                text-indent: 1.5rem !important;
                font-size: 1.1rem !important;
                color: #333 !important;
            }
            
            .fact-detail-container ul, 
            .fact-detail-container ol {
                margin-left: 3rem !important;
                margin-bottom: 2rem !important;
                padding: 0 2rem !important;
            }
            
            .fact-detail-container li {
                margin-bottom: 1rem !important;
                line-height: 1.8 !important;
                text-align: justify !important;
                font-size: 1.1rem !important;
                color: #333 !important;
            }
            
            .fact-detail-container hr {
                margin: 3rem 2rem !important;
                border: none !important;
                height: 3px !important;
                background: linear-gradient(90deg, #2196F3, #673AB7) !important;
                border-radius: 2px !important;
            }
            
            .fact-detail-container strong, 
            .fact-detail-container b {
                color: #1A237E !important;
                font-weight: 700 !important;
            }
            
            .fact-detail-container em, 
            .fact-detail-container i {
                color: #555 !important;
                font-style: italic !important;
            }
            </style>
            """, unsafe_allow_html=True)
                
            # Wyświetlanie szczegółów ciekawostki w kontenerze z marginesami
            st.markdown('<div class="fact-detail-container">', unsafe_allow_html=True)
            st.markdown(f"## {fact['icon']} {fact['title']}")
            st.markdown(f"*Źródło: {fact['source']}*")
            st.markdown("---")
            
            # Pobierz treść ciekawostki
            content = load_inspiration_content(fact['file_path'])
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Wyświetlanie listy ciekawostek
            if facts:
                # Opcje wyszukiwania
                search_query = st.text_input("🔍 Wyszukaj ciekawostkę", "")
                
                # Filtrowanie ciekawostek
                filtered_facts = facts
                if search_query:
                    filtered_facts = [f for f in facts if search_query.lower() in f['title'].lower() 
                                     or search_query.lower() in f['content'].lower()
                                     or search_query.lower() in f['source'].lower()]
                
                if not filtered_facts:
                    st.info("Nie znaleziono ciekawostek pasujących do wyszukiwania.")
                
                # Wyświetlanie ciekawostek w siatce
                cols = st.columns(2)
                for i, fact in enumerate(filtered_facts):
                    with cols[i % 2]:
                        m3_fixed_card(
                            title=fact['title'],
                            icon=fact['icon'],
                            content=f"{fact['content']}<br><br><i>Źródło: {fact['source']}</i>"
                        )
                        if st.button("Czytaj więcej", key=f"fact_{fact['id']}"):
                            st.session_state['current_fact'] = fact
                            st.session_state['show_fact_detail'] = True
                            st.rerun()
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Aktualnie brak dostępnych ciekawostek.")

    # Dodatkowe rekomendacje na dole strony
    if not st.session_state.get('show_article_detail', False) and not st.session_state.get('show_tutorial_detail', False) and not st.session_state.get('show_fact_detail', False):
        st.markdown("---")
        st.markdown("### 💫 Polecane dla Ciebie")
        
        # Losowe rekomendacje (jeśli są dostępne materiały)
        recommendations = []
        if blog_articles:
            recommendations.append(random.choice(blog_articles))
        if tutorials:
            recommendations.append(random.choice(tutorials))
        if facts:
            recommendations.append(random.choice(facts))
        
        # Wyświetlanie rekomendacji
        if recommendations:
            cols = st.columns(len(recommendations))
            for i, recommendation in enumerate(recommendations):
                with cols[i]:
                    if 'author' in recommendation:  # artykuł bloga
                        st.markdown(f"**📝 {recommendation['title']}**")
                        st.markdown(f"*{recommendation['author']}*")
                        if st.button("Przejdź", key=f"rec_article_{recommendation['id']}"):
                            st.session_state['current_article'] = recommendation
                            st.session_state['show_article_detail'] = True
                            st.rerun()
                    elif 'duration' in recommendation:  # tutorial
                        st.markdown(f"**🎓 {recommendation['title']}**")
                        st.markdown(f"*Czas: {recommendation['duration']}*")
                        if st.button("Przejdź", key=f"rec_tutorial_{recommendation['id']}"):
                            st.session_state['current_tutorial'] = recommendation
                            st.session_state['show_tutorial_detail'] = True
                            st.rerun()
                    else:  # ciekawostka
                        st.markdown(f"**🧠 {recommendation['title']}**")
                        st.markdown(f"*{recommendation['source']}*")
                        if st.button("Przejdź", key=f"rec_fact_{recommendation['id']}"):
                            st.session_state['current_fact'] = recommendation
                            st.session_state['show_fact_detail'] = True
                            st.rerun()
