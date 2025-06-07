import streamlit as st
from utils.components import zen_header
from utils.material3_components import apply_material3_theme

def show_inspirations():
    """
    Wyświetla zakładkę Inspiracje z trzema podstronami:
    - Blog: artykuły i posty na temat neuroleadershipu
    - Tutoriale: poradniki i instruktaże
    - Ciekawostki: interesujące fakty i odkrycia naukowe
    """
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Wyświetl nagłówek
    zen_header("Inspiracje 💡")
    
    st.markdown("*Odkryj interesujące treści, które poszerzą Twoje rozumienie neuroleadershipu*")
    
    # Zakładki
    tab1, tab2, tab3 = st.tabs(["📝 Blog", "🎓 Tutoriale", "🧠 Ciekawostki"])
    
    # Zakładka 1: Blog
    with tab1:
        st.markdown("### Artykuły i Posty")
        st.markdown("Najnowsze teksty z dziedziny neuroleadershipu i zarządzania.")
        
        # Przykładowy artykuł
        with st.container():
            st.markdown("#### 🧠 Wpływ stresu na podejmowanie decyzji biznesowych")
            st.markdown("Najnowsze badania pokazują, jak poziom stresu wpływa na obszary mózgu odpowiedzialne za podejmowanie strategicznych decyzji w biznesie...")
            st.markdown("*Autor: Dr Anna Kowalska | Opublikowano: 5 czerwca 2025*")
    
    # Zakładka 2: Tutoriale
    with tab2:
        st.markdown("### Praktyczne Poradniki")
        st.markdown("Tutoriale i przewodniki, które pomogą Ci zastosować wiedzę z neuroleadershipu w praktyce.")
        
        # Przykładowy tutorial
        with st.container():
            st.markdown("#### 🧘 Techniki redukcji stresu oparte na neuronaukach")
            st.markdown("Krok po kroku nauczysz się, jak stosować techniki oddechowe i mindfulness, które bezpośrednio wpływają na układ parasympatyczny, redukując poziom kortyzolu...")
            st.markdown("**Czas:** 15 minut | **Poziom:** Początkujący")
    
    # Zakładka 3: Ciekawostki
    with tab3:
        st.markdown("### Fascynujące Odkrycia")
        st.markdown("Interesujące fakty i odkrycia naukowe z pogranicza neuronauków i zarządzania.")
        
        # Przykładowa ciekawostka
        with st.container():
            st.markdown("#### 💡 Dlaczego najlepsze pomysły przychodzą pod prysznicem?")
            st.markdown("Badania pokazują, że monotonne czynności, takie jak prysznic, aktywują tzw. tryb domyślny mózgu (DMN - Default Mode Network), który sprzyja kreatywności i łączeniu odległych koncepcji...")
            st.markdown("*Źródło: Journal of Cognitive Neuroscience*")
    
    # Dodatkowa sekcja
    st.markdown("---")
    st.markdown("### 💫 Polecane dla Ciebie")
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("**📝 Wpływ stresu na podejmowanie decyzji biznesowych**")
        st.markdown("*Dr Anna Kowalska*")
    with cols[1]:
        st.markdown("**🎓 Techniki redukcji stresu oparte na neuronaukach**")
        st.markdown("*Czas: 15 minut*")
    with cols[2]:
        st.markdown("**🧠 Dlaczego najlepsze pomysły przychodzą pod prysznicem?**")
        st.markdown("*Journal of Cognitive Neuroscience*")
