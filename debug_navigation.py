import streamlit as st
import os
import sys

# Dodaj ścieżkę głównego katalogu aplikacji do sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

st.title("Debug Menu Nawigacji")

st.markdown("""
## Sprawdzenie importów

Sprawdzamy, czy wszystkie niezbędne importy działają:
""")

try:
    from utils.session import init_session_state
    st.success("✅ utils.session zaimportowane poprawnie")
except Exception as e:
    st.error(f"❌ Błąd importu utils.session: {str(e)}")

try:
    from utils.components import navigation_menu
    st.success("✅ utils.components (navigation_menu) zaimportowane poprawnie")
except Exception as e:
    st.error(f"❌ Błąd importu utils.components: {str(e)}")

try:
    from views.inspirations import show_inspirations
    st.success("✅ views.inspirations zaimportowane poprawnie")
except Exception as e:
    st.error(f"❌ Błąd importu views.inspirations: {str(e)}")

st.markdown("---")
st.markdown("## Testowanie nawigacji")

# Inicjalizacja stanu
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
if 'username' not in st.session_state:
    st.session_state.username = 'testuser'

st.write(f"Obecnie wybrana strona: **{st.session_state.page}**")

try:
    if st.button("Przełącz na Inspiracje"):
        st.session_state.page = 'inspirations'
        st.rerun()
        
    if st.button("Pokaż menu nawigacyjne"):
        with st.sidebar:
            st.markdown("### Menu")
            navigation_menu()
    
    if st.button("Uruchom show_inspirations()"):
        show_inspirations()
except Exception as e:
    st.error(f"Wystąpił błąd: {str(e)}")
    st.code(f"```python\n{e.__traceback__}\n```")
