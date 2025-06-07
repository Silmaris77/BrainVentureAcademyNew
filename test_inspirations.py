import streamlit as st
import sys
import os
import traceback

# Ścieżka do głównego katalogu aplikacji (dla importów)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

try:
    from views.inspirations import show_inspirations
    
    st.title("Test zakładki Inspiracje")
    st.write("Próba uruchomienia funkcji show_inspirations()...")
    
    show_inspirations()
    st.success("Zakładka Inspiracje została poprawnie załadowana!")
    
except Exception as e:
    st.error(f"Wystąpił błąd: {str(e)}")
    st.code(traceback.format_exc())
