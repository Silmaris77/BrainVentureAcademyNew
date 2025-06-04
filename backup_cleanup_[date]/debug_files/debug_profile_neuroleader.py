import streamlit as st
from data.users import load_user_data
from data.test_questions import NEUROLEADER_TYPES

st.title("🔍 Test Profile Neuroleader Display")

# Sprawdź dane użytkownika 'a'
users_data = load_user_data()
user_a = users_data.get('a', {})

st.write("### Dane użytkownika 'a':")
st.write(f"- neuroleader_type: {user_a.get('neuroleader_type')}")
st.write(f"- degen_type: {user_a.get('degen_type')}")
st.write(f"- test_taken: {user_a.get('test_taken')}")
st.write(f"- has_test_scores: {'test_scores' in user_a}")

if 'test_scores' in user_a:
    st.write(f"- test_scores: {user_a['test_scores']}")

# Test logiki warunkowej
neuroleader_type = user_a.get('neuroleader_type') or user_a.get('degen_type')
test_taken = user_a.get('test_taken', False)
has_test_scores = 'test_scores' in user_a

st.write("### Logika warunkowa:")
st.write(f"- neuroleader_type: {neuroleader_type}")
st.write(f"- test_taken: {test_taken}")
st.write(f"- has_test_scores: {has_test_scores}")

if neuroleader_type and (test_taken or has_test_scores):
    st.success("✅ WARUNEK SPEŁNIONY - użytkownik POWINIEN widzieć wyniki testu")
    
    if neuroleader_type in NEUROLEADER_TYPES:
        st.write(f"✅ Typ '{neuroleader_type}' istnieje w definicjach")
        type_info = NEUROLEADER_TYPES[neuroleader_type]
        st.write(f"- Opis: {type_info.get('description', 'Brak')}")
        st.write(f"- Mocne strony: {type_info.get('strengths', [])}")
        st.write(f"- Wyzwania: {type_info.get('challenges', [])}")
    else:
        st.error(f"❌ Typ '{neuroleader_type}' NIE istnieje w definicjach")
else:
    st.error("❌ WARUNEK NIE SPEŁNIONY - użytkownik będzie widział zachętę do testu")

# Test importów
st.write("### Test importów:")
try:
    from data.neuroleader_details import degen_details
    st.success("✅ Import degen_details - OK")
    st.write(f"Dostępne typy: {list(degen_details.keys())}")
except Exception as e:
    st.error(f"❌ Import degen_details - BŁĄD: {e}")

try:
    from views.degen_test import plot_radar_chart
    st.success("✅ Import plot_radar_chart - OK")
except Exception as e:
    st.error(f"❌ Import plot_radar_chart - BŁĄD: {e}")
