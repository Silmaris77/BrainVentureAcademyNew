import streamlit as st
from data.users import load_user_data, save_user_data
import datetime
from datetime import timedelta
from utils.components import zen_header
from utils.material3_components import apply_material3_theme

# Check if this module is being used to avoid duplicate rendering
_IS_SHOP_NEW_LOADED = False

def buy_item(item_type, item_id, price, user_data, users_data):
    """
    Process the purchase of an item
    
    Parameters:
    - item_type: Type of the item (avatar, background, special_lesson, booster)
    - item_id: Unique identifier of the item
    - price: Cost in NeuroCoins
    - user_data: User's data dictionary
    - users_data: All users' data dictionary
    
    Returns:
    - (success, message): Tuple with success status and message
    """
    # Sprawdź czy użytkownik ma wystarczającą ilość monet
    if user_data.get('degen_coins', 0) < price:
        return False, "Nie masz wystarczającej liczby NeuroCoins!"
    
    # Odejmij monety
    user_data['degen_coins'] = user_data.get('degen_coins', 0) - price
    
    # Dodaj przedmiot do ekwipunku użytkownika
    if 'inventory' not in user_data:
        user_data['inventory'] = {}
    
    if item_type not in user_data['inventory']:
        user_data['inventory'][item_type] = []
    
    # Dodaj przedmiot do odpowiedniej kategorii (unikaj duplikatów)
    if item_id not in user_data['inventory'][item_type]:
        user_data['inventory'][item_type].append(item_id)
    
    # Dodaj specjalną obsługę dla boosterów (dodając datę wygaśnięcia)
    if item_type == 'booster':
        if 'active_boosters' not in user_data:
            user_data['active_boosters'] = {}
        
        # Ustawienie czasu wygaśnięcia na 24 godziny od teraz
        expiry_time = datetime.datetime.now() + timedelta(hours=24)
        user_data['active_boosters'][item_id] = expiry_time.isoformat()
    
    # Zapisz zmiany w danych użytkownika
    users_data[user_data['username']] = user_data
    save_user_data(users_data)
    
    return True, f"Pomyślnie zakupiono przedmiot za {price} NeuroCoins!"

def show_shop():
    """
    Wyświetla sklep z przedmiotami do zakupu - dostosowany dla menedżerów uczących się neuroleadershipu.
    """
    # Zastosuj style Material 3
    apply_material3_theme()
    
    global _IS_SHOP_NEW_LOADED
    
    # Unikaj podwójnego renderowania
    if _IS_SHOP_NEW_LOADED:
        return
    _IS_SHOP_NEW_LOADED = True
    
    # Załaduj dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Wyświetl główną zawartość
    zen_header("Sklep 🛒")
    
    # Wyświetl ilość monet użytkownika
    st.markdown(f"### Twoje NeuroCoins: <span style='color: #6366f1;'>🧠 {user_data.get('degen_coins', 0)}</span>", unsafe_allow_html=True)
    
    st.markdown("*Rozwijaj swoje umiejętności przywódcze poprzez nabycie specjalnych przedmiotów!*")
    
    # Zakładki sklepu
    tab_avatars, tab_backgrounds, tab_special_lessons, tab_boosters = st.tabs([
        "🎭 Profile Przywódcze", 
        "🖼️ Środowiska Pracy", 
        "📚 Zaawansowane Moduły", 
        "⚡ Wzmocnienia"
    ])
    
    # Profile Przywódcze (Awatary)
    with tab_avatars:
        st.markdown("# 🎭 Profile Przywódcze")
        st.markdown("*Wybierz awatar, który najlepiej odzwierciedla Twój styl przywództwa*")
        
        # Lista dostępnych awatarów dostosowanych do neuroleadershipu
        avatars = {
            "neuroleader_master": {
                "name": "🧠 Neuroleader Master",
                "price": 500,
                "description": "Awatar dla doświadczonych menedżerów poznających tajniki neuroleadershipu i neuronauków zarządzania."
            },
            "team_catalyst": {
                "name": "⚡ Team Catalyst",
                "price": 750,
                "description": "Dla liderów, którzy potrafią inspirować i motywować zespoły, tworząc synergię i wysoką wydajność."
            },
            "visionary_leader": {
                "name": "🌟 Visionary Leader",
                "price": 1000,
                "description": "Dla menedżerów z wizją, którzy prowadzą organizacje ku przyszłości, łącząc strategię z empatią."
            },
            "empathic_coach": {
                "name": "💝 Empathic Coach",
                "price": 600,
                "description": "Awatar dla liderów, którzy stawiają na rozwój innych i budowanie kultury wsparcia w zespole."
            }
        }
        
        # Wyświetl dostępne awatary w dwóch kolumnach
        cols = st.columns(2)
        
        for i, (avatar_id, avatar) in enumerate(avatars.items()):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### {avatar['name']}")
                    st.markdown(f"**Koszt:** 🧠 {avatar['price']} NeuroCoins")
                    st.markdown(f"*{avatar['description']}*")
                    
                    # Sprawdź czy użytkownik posiada już ten awatar
                    user_has_item = ('inventory' in user_data and 
                                   'avatar' in user_data.get('inventory', {}) and 
                                   avatar_id in user_data['inventory']['avatar'])
                    
                    if user_has_item:
                        # Sprawdź czy awatar jest aktualnie używany
                        is_active = user_data.get('active_avatar') == avatar_id
                        
                        if is_active:
                            st.success("✅ Ten profil jest aktualnie aktywny")
                        else:
                            if st.button(f"Aktywuj {avatar['name']}", key=f"use_{avatar_id}"):
                                user_data['active_avatar'] = avatar_id
                                users_data[st.session_state.username] = user_data
                                save_user_data(users_data)
                                st.success(f"Aktywowano profil {avatar['name']}!")
                                st.rerun()
                    else:
                        # Przycisk do zakupu
                        if st.button(f"Kup {avatar['name']}", key=f"buy_{avatar_id}"):
                            success, message = buy_item('avatar', avatar_id, avatar['price'], user_data, users_data)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    
                    st.markdown("---")
    
    # Środowiska Pracy (Tła)
    with tab_backgrounds:
        st.markdown("# 🖼️ Środowiska Pracy")
        st.markdown("*Stwórz inspirujące środowisko dla swojej przygody z neuroleadershipem*")
        
        # Lista dostępnych środowisk pracy
        backgrounds = {
            "modern_office": {
                "name": "🏢 Nowoczesne Biuro",
                "price": 300,
                "description": "Eleganckie, nowoczesne środowisko biurowe sprzyjające kreatywności i współpracy."
            },
            "zen_workspace": {
                "name": "🧘 Przestrzeń Zen",
                "price": 400,
                "description": "Spokojne, minimalistyczne środowisko wspierające koncentrację i mindfulness."
            },
            "innovation_lab": {
                "name": "🔬 Laboratorium Innowacji",
                "price": 600,
                "description": "Futurystyczne środowisko dla liderów, którzy tworzą przyszłość organizacji."
            },
            "nature_retreat": {
                "name": "🌿 Natura & Refleksja",
                "price": 450,
                "description": "Naturalne środowisko wspierające głęboką refleksję i holistyczne myślenie."
            }
        }
        
        # Wyświetl dostępne środowiska w dwóch kolumnach
        cols = st.columns(2)
        
        for i, (bg_id, bg) in enumerate(backgrounds.items()):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### {bg['name']}")
                    st.markdown(f"**Koszt:** 🧠 {bg['price']} NeuroCoins")
                    st.markdown(f"*{bg['description']}*")
                    
                    # Sprawdź czy użytkownik posiada już to środowisko
                    user_has_item = ('inventory' in user_data and 
                                   'background' in user_data.get('inventory', {}) and 
                                   bg_id in user_data['inventory']['background'])
                    
                    if user_has_item:
                        # Sprawdź czy środowisko jest aktualnie używane
                        is_active = user_data.get('active_background') == bg_id
                        
                        if is_active:
                            st.success("✅ To środowisko jest aktualnie aktywne")
                        else:
                            if st.button(f"Aktywuj {bg['name']}", key=f"use_{bg_id}"):
                                user_data['active_background'] = bg_id
                                users_data[st.session_state.username] = user_data
                                save_user_data(users_data)
                                st.success(f"Aktywowano środowisko {bg['name']}!")
                                st.rerun()
                    else:
                        # Przycisk do zakupu
                        if st.button(f"Kup {bg['name']}", key=f"buy_{bg_id}"):
                            success, message = buy_item('background', bg_id, bg['price'], user_data, users_data)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    
                    st.markdown("---")
    
    # Zaawansowane Moduły (Specjalne lekcje)
    with tab_special_lessons:
        st.markdown("# 📚 Zaawansowane Moduły Neuroleadershipu")
        st.markdown("*Pogłęb swoją wiedzę dzięki ekskluzywnym modułom szkoleniowym*")
        
        # Lista dostępnych zaawansowanych modułów
        special_lessons = {
            "neuroplasticity_leadership": {
                "name": "🧠 Neuroplastyczność w Przywództwie",
                "price": 800,
                "description": "Zaawansowane techniki wykorzystania neuroplastyczności do rozwoju zespołów i własnych umiejętności przywódczych."
            },
            "emotional_intelligence_pro": {
                "name": "💭 Inteligencja Emocjonalna PRO",
                "price": 700,
                "description": "Mistrzostwo w zarządzaniu emocjami - swoimi i zespołu. Narzędzia dla zaawansowanych liderów."
            },
            "decision_neuroscience": {
                "name": "⚖️ Neuronaukowedecyzje",
                "price": 1200,
                "description": "Jak mózg podejmuje decyzje? Wykorzystaj najnowsze odkrycia neuronaukowdo lepszego zarządzania."
            },
            "team_brain_sync": {
                "name": "🤝 Synchronizacja Zespołowa",
                "price": 900,
                "description": "Techniki budowania spójności zespołowej na poziomie neurologicznym. Tworzenie 'grupowego mózgu'."
            }
        }
        
        # Wyświetl dostępne moduły w dwóch kolumnach
        cols = st.columns(2)
        
        for i, (lesson_id, lesson) in enumerate(special_lessons.items()):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### {lesson['name']}")
                    st.markdown(f"**Koszt:** 🧠 {lesson['price']} NeuroCoins")
                    st.markdown(f"*{lesson['description']}*")
                    
                    # Sprawdź czy użytkownik posiada już ten moduł
                    user_has_item = ('inventory' in user_data and 
                                   'special_lesson' in user_data.get('inventory', {}) and 
                                   lesson_id in user_data['inventory']['special_lesson'])
                    
                    if user_has_item:
                        if st.button(f"📖 Rozpocznij {lesson['name']}", key=f"start_{lesson_id}"):
                            st.session_state.page = 'lesson'
                            st.session_state.lesson_id = f"special_{lesson_id}"
                            st.rerun()
                    else:
                        # Przycisk do zakupu
                        if st.button(f"Kup {lesson['name']}", key=f"buy_{lesson_id}"):
                            success, message = buy_item('special_lesson', lesson_id, lesson['price'], user_data, users_data)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    
                    st.markdown("---")
    
    # Wzmocnienia (Boostery)
    with tab_boosters:
        st.markdown("# ⚡ Wzmocnienia Neuroleadershipu")
        st.markdown("*Czasowe bonusy wspierające Twój rozwój przywódczy*")
        
        # Lista dostępnych wzmocnień
        boosters = {
            "focus_enhancer": {
                "name": "🎯 Wzmacniacz Koncentracji",
                "price": 200,
                "description": "Zwiększa efektywność nauki o 50% przez 24 godziny. Idealne przed ważnymi sesjami szkoleniowymi."
            },
            "empathy_boost": {
                "name": "💝 Boost Empatii",
                "price": 300,
                "description": "Wzmacnia zdolności empatyczne i intuicję przywódczą o 50% przez 24 godziny."
            },
            "creativity_spark": {
                "name": "💡 Iskra Kreatywności",
                "price": 250,
                "description": "Stymuluje kreatywne myślenie i innowacyjne rozwiązania przez 24 godziny."
            },
            "team_harmony": {
                "name": "🤝 Harmonia Zespołowa",
                "price": 350,
                "description": "Zwiększa skuteczność w budowaniu relacji i zarządzaniu zespołem przez 24 godziny."
            }
        }
        
        # Wyświetl dostępne wzmocnienia w dwóch kolumnach
        cols = st.columns(2)
        
        for i, (booster_id, booster) in enumerate(boosters.items()):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### {booster['name']}")
                    st.markdown(f"**Koszt:** 🧠 {booster['price']} NeuroCoins")
                    st.markdown(f"*{booster['description']}*")
                    
                    # Sprawdź czy wzmocnienie jest aktywne
                    is_active = False
                    remaining_time = None
                    
                    if 'active_boosters' in user_data and booster_id in user_data.get('active_boosters', {}):
                        expiry_time = datetime.datetime.fromisoformat(user_data['active_boosters'][booster_id])
                        now = datetime.datetime.now()
                        
                        if expiry_time > now:
                            is_active = True
                            remaining_seconds = (expiry_time - now).total_seconds()
                            remaining_hours = int(remaining_seconds // 3600)
                            remaining_minutes = int((remaining_seconds % 3600) // 60)
                            remaining_time = f"{remaining_hours}h {remaining_minutes}m"
                    
                    if is_active:
                        st.success(f"✅ Aktywne! Pozostały czas: {remaining_time}")
                    else:
                        # Przycisk do zakupu
                        if st.button(f"Aktywuj {booster['name']}", key=f"buy_{booster_id}"):
                            success, message = buy_item('booster', booster_id, booster['price'], user_data, users_data)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    
                    st.markdown("---")
    
    # Informacje dodatkowe
    st.markdown("---")
    st.markdown("### 💡 Jak zdobywać NeuroCoins?")
    st.markdown("""
    - 🎓 **Ukończenie lekcji**: 50-100 NeuroCoins za lekcję
    - ✅ **Realizacja celów**: 100-200 NeuroCoins za cel
    - 🎯 **Misje dzienne**: 25-75 NeuroCoins za misję
    - 🏆 **Osiągnięcia**: 200-500 NeuroCoins za osiągnięcie
    - 📝 **Aktywne uczestnictwo**: Dodatkowe punkty za refleksje i aktywność
    """)
