"""
Test mapy myśli - sprawdza czy nowa funkcjonalność działa poprawnie
"""
import streamlit as st
import json
import os

def test_mind_map():
    st.title("🗺️ Test Mapy Myśli")
    
    # Załaduj dane lekcji B1C1L1
    try:
        lesson_path = os.path.join("data", "lessons", "B1C1L1.json")
        with open(lesson_path, 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)
        
        st.success("✅ Dane lekcji załadowane pomyślnie")
        
        # Spróbuj zaimportować funkcję mapy myśli
        try:
            from utils.mind_map import create_lesson_mind_map
            st.success("✅ Moduł mind_map zaimportowany pomyślnie")
            
            # Spróbuj stworzyć mapę myśli
            try:
                st.subheader("Mapa myśli dla lekcji: " + lesson_data.get('title', 'B1C1L1'))
                
                # Informacja dla użytkownika
                st.info("📋 Poniżej powinna pojawić się interaktywna mapa myśli. Jeśli widzisz tylko komunikat o błędzie, oznacza to że biblioteka streamlit-agraph wymaga dodatkowej konfiguracji.")
                
                # Stwórz mapę myśli
                mind_map_result = create_lesson_mind_map(lesson_data)
                
                if mind_map_result:
                    st.success("✅ Mapa myśli została wygenerowana!")
                else:
                    st.warning("⚠️ Mapa myśli nie została wygenerowana - sprawdź logi powyżej")
                    
            except Exception as e:
                st.error(f"❌ Błąd podczas tworzenia mapy myśli: {str(e)}")
                st.code(str(e))
                
        except ImportError as e:
            st.error(f"❌ Błąd importu modułu mind_map: {str(e)}")
            
    except Exception as e:
        st.error(f"❌ Błąd podczas ładowania danych lekcji: {str(e)}")

if __name__ == "__main__":
    test_mind_map()
