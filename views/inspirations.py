import streamlit as st
import random
from utils.components import zen_header
from utils.material3_components import apply_material3_theme, m3_card
from views.fix_card import m3_fixed_card  # Dodajemy naszą naprawioną wersję karty
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view, apply_responsive_styles

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
    
    # Wyświetl nagłówek
    zen_header("Inspiracje 💡")
    
    st.markdown("*Odkryj interesujące treści, które poszerzą Twoje rozumienie neuroleadershipu*")
    
    # Zakładki
    tab1, tab2, tab3 = st.tabs(["📝 Blog", "🎓 Tutoriale", "🧠 Ciekawostki"])
    
    # Zakładka 1: Blog
    with tab1:
        st.markdown("### Artykuły i Posty")
        st.markdown("Najnowsze teksty z dziedziny neuroleadershipu i zarządzania.")
        
        # Przykładowe artykuły bloga
        blog_articles = [
            {
                "title": "Wpływ stresu na podejmowanie decyzji biznesowych",
                "content": "Najnowsze badania pokazują, jak poziom stresu wpływa na obszary mózgu odpowiedzialne za podejmowanie strategicznych decyzji w biznesie...",
                "date": "5 czerwca 2025",
                "author": "Dr Anna Kowalska",
                "icon": "🧠"
            },
            {
                "title": "Neuroplastyczność a rozwój umiejętności przywódczych",
                "content": "Jak świadome praktyki mogą zmienić połączenia neuronalne i poprawić zdolności przywódcze? Przegląd najnowszych badań z dziedziny neuroplastyczności...",
                "date": "1 czerwca 2025",
                "author": "Prof. Jan Nowak",
                "icon": "🔄"
            },
            {
                "title": "Empatia w zarządzaniu zespołem - perspektywa neuronaukowa",
                "content": "Odkrycia neuronaukowców dotyczące neuronów lustrzanych rzucają nowe światło na budowanie relacji w zespole i efektywne zarządzanie...",
                "date": "28 maja 2025",
                "author": "Marta Wiśniewska",
                "icon": "💓"
            }
        ]
          # Wyświetl artykuły
        for article in blog_articles:            # Używamy naszej nowej funkcji zamiast problematycznej m3_card
            m3_fixed_card(
                title=f"{article['title']}",
                icon=article['icon'],
                content=f"{article['content']}<br><br><i>Autor: {article['author']} | Opublikowano: {article['date']}</i>"
            )
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Zakładka 2: Tutoriale
    with tab2:
        st.markdown("### Praktyczne Poradniki")
        st.markdown("Tutoriale i przewodniki, które pomogą Ci zastosować wiedzę z neuroleadershipu w praktyce.")
        
        # Przykładowe tutoriale
        tutorials = [
            {
                "title": "Techniki redukcji stresu oparte na neuronaukach",
                "content": "Krok po kroku nauczysz się, jak stosować techniki oddechowe i mindfulness, które bezpośrednio wpływają na układ parasympatyczny, redukując poziom kortyzolu...",
                "duration": "15 minut",
                "level": "Początkujący",
                "icon": "🧘"
            },
            {
                "title": "Budowanie efektywnych nawyków w oparciu o neurobiologię",
                "content": "Ten tutorial pokazuje, jak wykorzystać wiedzę o mechanizmach nagrody w mózgu do tworzenia długotrwałych, pozytywnych nawyków w zarządzaniu...",
                "duration": "25 minut",
                "level": "Średniozaawansowany",
                "icon": "⏱️"
            },
            {
                "title": "Prowadzenie spotkań z wykorzystaniem zasad neuroergonomii",
                "content": "Dowiedz się, jak zaprojektować spotkania, które wykorzystują naturalne cykle energii mózgu, zwiększając produktywność i satysfakcję uczestników...",
                "duration": "20 minut",
                "level": "Zaawansowany",
                "icon": "👥"
            }
        ]
          # Wyświetl tutoriale
        for tutorial in tutorials:            # Używamy naszej nowej funkcji zamiast problematycznej m3_card
            m3_fixed_card(
                title=f"{tutorial['title']}",
                icon=tutorial['icon'],
                content=f"{tutorial['content']}<br><br><b>Czas: </b>{tutorial['duration']} | <b>Poziom:</b> {tutorial['level']}"
            )
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Zakładka 3: Ciekawostki
    with tab3:
        st.markdown("### Fascynujące Odkrycia")
        st.markdown("Interesujące fakty i odkrycia naukowe z pogranicza neuronauków i zarządzania.")
        
        # Przykładowe ciekawostki
        facts = [
            {
                "title": "Dlaczego najlepsze pomysły przychodzą pod prysznicem?",
                "content": "Badania pokazują, że monotonne czynności, takie jak prysznic, aktywują tzw. tryb domyślny mózgu (DMN - Default Mode Network), który sprzyja kreatywności i łączeniu odległych koncepcji...",
                "source": "Journal of Cognitive Neuroscience",
                "icon": "💡"
            },
            {
                "title": "Wpływ koloru niebieskiego na produktywność",
                "content": "Ekspozycja na kolor niebieski może zwiększyć produktywność o 15-20%. Neurobiologiczne badania pokazują, że niebieski aktywuje receptory w oku, które bezpośrednio stymulują obszar mózgu odpowiedzialny za czujność...",
                "source": "Color Research & Application Journal",
                "icon": "🔵"
            },
            {
                "title": "Efekt IKEA w psychologii zarządzania",
                "content": "Neuroimaging pokazuje, że ludzie wyżej cenią rzeczy, które sami współtworzyli. Ten fenomen, znany jako 'efekt IKEA', ma głębokie implikacje dla angażowania pracowników w procesy decyzyjne...",
                "source": "Harvard Business Review",
                "icon": "🪑"
            },
            {
                "title": "Dlaczego wielozadaniowość szkodzi wydajności",
                "content": "Mózg człowieka nie jest zdolny do prawdziwej wielozadaniowości. Badania pokazują, że tzw. 'switch cost' (koszt przełączania) między zadaniami może obniżyć produktywność nawet o 40% i zwiększyć ilość błędów...",
                "source": "Psychology Today",
                "icon": "⏳"
            }
        ]
        
        # Wyświetl ciekawostki w układzie siatki
        cols = st.columns(2)
        for i, fact in enumerate(facts):
            with cols[i % 2]:                # Używamy naszej nowej funkcji zamiast problematycznej m3_card
                m3_fixed_card(
                    title=f"{fact['title']}",
                    icon=fact['icon'],
                    content=f"{fact['content']}<br><br><i>Źródło: {fact['source']}</i>"
                )
                st.markdown("<br>", unsafe_allow_html=True)

    # Dodatkowe rekomendacje na dole strony
    st.markdown("---")
    st.markdown("### 💫 Polecane dla Ciebie")
    
    # Losowa rekomendacja z każdej kategorii
    recommendations = [
        random.choice(blog_articles),
        random.choice(tutorials),
        random.choice(facts)
    ]
    
    # Wyświetl rekomendacje w jednym rzędzie
    cols = st.columns(3)
    
    for i, recommendation in enumerate(recommendations):
        with cols[i]:
            if 'author' in recommendation:  # artykuł bloga
                st.markdown(f"**📝 {recommendation['title']}**")
                st.markdown(f"*{recommendation['author']}*")
            elif 'duration' in recommendation:  # tutorial
                st.markdown(f"**🎓 {recommendation['title']}**")
                st.markdown(f"*Czas: {recommendation['duration']}*")
            else:  # ciekawostka
                st.markdown(f"**🧠 {recommendation['title']}**")
                st.markdown(f"*{recommendation['source']}*")
