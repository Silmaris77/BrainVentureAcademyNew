import streamlit as st

# Testowy układ strony
st.title("Test strony Inspiracje")
tab1, tab2, tab3 = st.tabs(["📝 Blog", "🎓 Tutoriale", "🧠 Ciekawostki"])

with tab1:
    st.markdown("### Artykuły i Posty")
    st.write("To jest prosty test zakładki Blog.")

with tab2:
    st.markdown("### Praktyczne Poradniki")
    st.write("To jest prosty test zakładki Tutoriale.")
    
with tab3:
    st.markdown("### Fascynujące Odkrycia")
    st.write("To jest prosty test zakładki Ciekawostki.")
    
if st.button("Powrót do dashboardu"):
    st.write("Przycisk działa poprawnie!")
