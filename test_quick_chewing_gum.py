import streamlit as st
import sys
import os

# Dodaj ścieżkę do głównego katalogu aplikacji
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

# Prosta aplikacja testowa
st.title("🧠 Test artykułu o żuciu gumy")

try:
    from utils.inspirations_loader import get_facts, load_inspiration_content
    
    st.write("Ładowanie ciekawostek...")
    facts = get_facts()
    
    st.write(f"Znaleziono {len(facts)} ciekawostek:")
    
    chewing_gum_found = False
    for fact in facts:
        st.write(f"- {fact['title']} (ID: {fact['id']})")
        if fact['id'] == 'chewing_gum_brain':
            chewing_gum_found = True
            st.success(f"✅ Znaleziono artykuł o żuciu gumy!")
            
            # Sprawdź czy można załadować treść
            content = load_inspiration_content(fact['file_path'])
            if "Bystrzak w mgnieniu oka" in content:
                st.success("✅ Treść ładuje się poprawnie!")
                
                # Pokaż pierwszych kilka linii
                st.write("**Początek artykułu:**")
                lines = content.split('\n')[:10]
                st.write('\n'.join(lines))
                
            else:
                st.error("❌ Problem z ładowaniem treści")
    
    if not chewing_gum_found:
        st.error("❌ Artykuł o żuciu gumy nie został znaleziony")
        
except Exception as e:
    st.error(f"Błąd: {str(e)}")
    st.code(str(e))

st.write("---")
st.write("**Aby zobaczyć artykuł w aplikacji:**")
st.write("1. Uruchom główną aplikację")
st.write("2. Przejdź do sekcji 'Inspiracje'")
st.write("3. Wybierz zakładkę '🧠 Ciekawostki'")
st.write("4. Znajdź 'Bystrzak w mgnieniu oka??? To proste!!!'")
st.write("5. Kliknij 'Czytaj więcej'")
