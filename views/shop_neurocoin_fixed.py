import streamlit as st
from data.users import load_user_data, save_user_data
from utils.components import zen_button, zen_header
from utils.layout import get_device_type
from utils.material3_components import apply_material3_theme
from datetime import datetime, timedelta
import json

# Neurocoin Shop Items - Neuroleadership themed
SHOP_ITEMS = {
    "avatars": {
        "neural_leader": {
            "name": "Neuro Lider",
            "description": "Awatar przedstawiający lidera z aktywną siecią neuronową w tle",
            "price": 100,
            "icon": "🧠",
            "rarity": "common",
            "image": "🧠👤"
        },
        "empathy_master": {
            "name": "Mistrz Empatii",
            "description": "Awatar symbolizujący mistrza empatii z sercem i połączeniami",
            "price": 150,
            "icon": "❤️",
            "rarity": "uncommon",
            "image": "❤️👤"
        },
        "decision_wizard": {
            "name": "Czarodziej Decyzji",
            "description": "Awatar przedstawiający eksperta od podejmowania decyzji",
            "price": 200,
            "icon": "🎯",
            "rarity": "rare",
            "image": "🎯👤"
        },
        "neuro_strategist": {
            "name": "Neuro Strateg",
            "description": "Awatar zaawansowanego stratega neuroliderstwa",
            "price": 300,
            "icon": "🧩",
            "rarity": "epic",
            "image": "🧩👤"
        }
    },
    "backgrounds": {
        "brain_network": {
            "name": "Sieć Mózgowa",
            "description": "Tło przedstawiające sieć neuronową z pulsującymi połączeniami",
            "price": 80,
            "icon": "🧠",
            "rarity": "common",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        },
        "team_synergy": {
            "name": "Synergia Zespołu",
            "description": "Tło symbolizujące synergię zespołową z połączonymi elementami",
            "price": 120,
            "icon": "🤝",
            "rarity": "uncommon",
            "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        },
        "leadership_summit": {
            "name": "Szczyt Przywództwa",
            "description": "Tło przedstawiające szczyt przywództwa z górskim krajobrazem",
            "price": 180,
            "icon": "⛰️",
            "rarity": "rare",
            "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        },
        "neural_cosmos": {
            "name": "Neuronalny Kosmos",
            "description": "Kosmiczne tło z neuronalnymi konstelacjami",
            "price": 250,
            "icon": "🌌",
            "rarity": "epic",
            "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
        }
    },
    "boosters": {
        "neuro_boost": {
            "name": "Neuro Wzmocnienie",
            "description": "Zwiększa zdobywane XP o 25% przez 1 godzinę",
            "price": 50,
            "icon": "⚡",
            "rarity": "common",
            "effect": {"type": "xp_multiplier", "value": 1.25, "duration": 3600},
            "stackable": True
        },
        "empathy_amplifier": {
            "name": "Wzmacniacz Empatii",
            "description": "Zwiększa zdobywane XP o 50% przy lekcjach empatii przez 30 minut",
            "price": 75,
            "icon": "💫",
            "rarity": "uncommon",
            "effect": {"type": "category_xp_multiplier", "category": "empathy", "value": 1.5, "duration": 1800},
            "stackable": False
        },
        "leadership_accelerator": {
            "name": "Akcelerator Przywództwa",
            "description": "Podwaja XP z wszystkich źródeł przez 15 minut",
            "price": 120,
            "icon": "🚀",
            "rarity": "rare",
            "effect": {"type": "xp_multiplier", "value": 2.0, "duration": 900},
            "stackable": False
        },
        "neural_flow": {
            "name": "Neuronalny Przepływ",
            "description": "Potraja XP przez 5 minut - użyj mądrze!",
            "price": 200,
            "icon": "🌊",
            "rarity": "epic",
            "effect": {"type": "xp_multiplier", "value": 3.0, "duration": 300},
            "stackable": False
        }
    },
    "special_lessons": {
        "advanced_neuroscience": {
            "name": "Zaawansowana Neuronauka",
            "description": "Ekskluzywna lekcja o zaawansowanych aspektach neuroliderstwa",
            "price": 500,
            "icon": "🔬",
            "rarity": "legendary",
            "content": "advanced_neuroscience_lesson",
            "one_time_purchase": True
        },
        "emotional_mastery": {
            "name": "Mistrzostwo Emocjonalne",
            "description": "Specjalistyczny kurs o opanowaniu emocji w liderskim kontekście",
            "price": 400,
            "icon": "🎭",
            "rarity": "epic",
            "content": "emotional_mastery_course",
            "one_time_purchase": True
        },
        "decision_science": {
            "name": "Nauka o Decyzjach",
            "description": "Naukowe podejście do podejmowania strategicznych decyzji",
            "price": 600,
            "icon": "🧬",
            "rarity": "legendary",
            "content": "decision_science_masterclass",
            "one_time_purchase": True
        }
    }
}

# Rarity colors and translations for styling
RARITY_COLORS = {
    "common": "#95a5a6",
    "uncommon": "#3498db",
    "rare": "#9b59b6",
    "epic": "#e74c3c",
    "legendary": "#f39c12"
}

RARITY_TRANSLATIONS = {
    "common": "Pospolity",
    "uncommon": "Rzadki",
    "rare": "Bardzo Rzadki",
    "epic": "Epicki",
    "legendary": "Legendarny"
}

def get_user_inventory(username):
    """Get user's current inventory"""
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    return {
        'neurocoin': user_data.get('neurocoin', 0),
        'inventory': user_data.get('inventory', {"avatar": [], "background": [], "special_lesson": [], "booster": []}),
        'active_boosters': user_data.get('active_boosters', {}),
        'active_avatar': user_data.get('active_avatar', 'default'),
        'active_background': user_data.get('active_background', 'default')
    }

def buy_item(username, category, item_id):
    """Kup przedmiot za Neurocoin"""
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    # Get item details
    if category not in SHOP_ITEMS or item_id not in SHOP_ITEMS[category]:
        return False, "Przedmiot nie został znaleziony"
    
    item = SHOP_ITEMS[category][item_id]
    price = item['price']
    current_neurocoin = user_data.get('neurocoin', 0)
    
    # Check if user has enough Neurocoin
    if current_neurocoin < price:
        return False, f"Za mało Neurocoin! Potrzebujesz {price}, ale masz {current_neurocoin}"
    
    # Check if item is already owned (for one-time purchases)
    user_inventory = user_data.get('inventory', {"avatar": [], "background": [], "special_lesson": [], "booster": []})
    
    if item.get('one_time_purchase', False) and item_id in user_inventory.get(category, []):
        return False, "Już posiadasz ten przedmiot"
    
    try:
        # Deduct Neurocoin
        user_data['neurocoin'] = current_neurocoin - price
        
        # Add item to inventory
        if category not in user_inventory:
            user_inventory[category] = []
        
        if category == 'booster':
            # For boosters, add multiple copies or track quantity
            user_inventory[category].append({
                'id': item_id,
                'purchased_at': datetime.now().isoformat(),
                'used': False
            })
        else:
            # For other items, just add the ID if not already present
            if item_id not in user_inventory[category]:
                user_inventory[category].append(item_id)
        
        user_data['inventory'] = user_inventory
        users_data[username] = user_data
        save_user_data(users_data)
        
        return True, f"Pomyślnie kupiono {item['name']} za {price} Neurocoin!"
        
    except Exception as e:
        return False, f"Zakup nie powiódł się: {str(e)}"

def use_booster(username, booster_id):
    """Activate a booster"""
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    user_inventory = user_data.get('inventory', {"avatar": [], "background": [], "special_lesson": [], "booster": []})
    active_boosters = user_data.get('active_boosters', {})
    
    # Find unused booster in inventory
    unused_booster = None
    for i, booster in enumerate(user_inventory.get('booster', [])):
        if isinstance(booster, dict) and booster.get('id') == booster_id and not booster.get('used', False):
            unused_booster = (i, booster)
            break
        elif isinstance(booster, str) and booster == booster_id:
            # Convert old format to new format
            unused_booster = (i, {'id': booster_id, 'used': False})
            break
    
    if not unused_booster:
        return False, "Nie znaleziono nieużywanego wzmocnienia"
    
    booster_index, booster_data = unused_booster
    booster_info = SHOP_ITEMS['boosters'].get(booster_id)
    
    if not booster_info:
        return False, "Wzmocnienie nie zostało znalezione w danych sklepu"
    
    # Check if booster is stackable
    if not booster_info.get('stackable', True) and booster_id in active_boosters:
        return False, "To wzmocnienie jest już aktywne i nie można go kumulować"
    
    try:
        # Mark booster as used
        user_inventory['booster'][booster_index]['used'] = True
        
        # Add to active boosters
        expiry_time = datetime.now() + timedelta(seconds=booster_info['effect']['duration'])
        active_boosters[booster_id] = {
            'effect': booster_info['effect'],
            'expires_at': expiry_time.isoformat(),
            'name': booster_info['name']
        }
        
        user_data['inventory'] = user_inventory
        user_data['active_boosters'] = active_boosters
        users_data[username] = user_data
        save_user_data(users_data)
        
        duration_text = f"{booster_info['effect']['duration'] // 60} minut"
        return True, f"Aktywowano {booster_info['name']} na {duration_text}!"
        
    except Exception as e:
        return False, f"Nie udało się aktywować wzmocnienia: {str(e)}"

def equip_cosmetic(username, category, item_id):
    """Załóż awatar lub tło"""
    if category not in ['avatar', 'background']:
        return False, "Nieprawidłowa kategoria kosmetyczna"
    
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    user_inventory = user_data.get('inventory', {"avatar": [], "background": [], "special_lesson": [], "booster": []})
    
    # Check if user owns the item
    if item_id not in user_inventory.get(category, []):
        category_polish = "awatara" if category == "avatar" else "tła"
        return False, f"Nie posiadasz tego {category_polish}"
    
    try:
        # Equip the cosmetic
        user_data[f'active_{category}'] = item_id
        users_data[username] = user_data
        save_user_data(users_data)
        
        item_name = SHOP_ITEMS[category + 's'][item_id]['name']
        return True, f"Założono {item_name}!"
        
    except Exception as e:
        category_polish = "awatara" if category == "avatar" else "tła"
        return False, f"Nie udało się założyć {category_polish}: {str(e)}"

def show_shop_item(category, item_id, item, user_inventory):
    """Display a single shop item card in the style from the image"""
    rarity_color = RARITY_COLORS.get(item.get('rarity', 'common'), "#95a5a6")
    rarity_text = RARITY_TRANSLATIONS.get(item.get('rarity', 'common'), "Pospolity")
    
    # Check ownership status
    owned = False
    if category == 'booster':
        # Count unused boosters
        booster_count = 0
        for booster in user_inventory['inventory'].get('booster', []):
            if isinstance(booster, dict) and booster.get('id') == item_id and not booster.get('used', False):
                booster_count += 1
            elif isinstance(booster, str) and booster == item_id:
                booster_count += 1
        owned = booster_count > 0
    else:
        owned = item_id in user_inventory['inventory'].get(category, [])
    
    # Check if currently equipped (for cosmetics)
    equipped = False
    if category in ['avatar', 'background']:
        equipped = user_inventory.get(f'active_{category}') == item_id
    
    # Create card layout similar to the image
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid {rarity_color};
        display: flex;
        align-items: center;
        gap: 15px;
    ">
        <div style="font-size: 2.5rem;">{item['icon']}</div>
        <div style="flex: 1;">
            <h4 style="margin: 0; color: #1f2937; font-weight: 600;">{item['name']}</h4>
            <p style="margin: 5px 0; color: #6b7280; font-size: 0.9rem;">{item['description'][:50]}...</p>
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 8px;">
                <span style="background: #f3f4f6; padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; color: #6b7280;">
                    Cena: 🪙 {item['price']}
                </span>
                <span style="color: {rarity_color}; font-weight: 500; font-size: 0.8rem;">
                    {rarity_text}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons in columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Purchase button
        can_purchase = (
            user_inventory['neurocoin'] >= item['price'] and
            (not item.get('one_time_purchase', False) or not owned)
        )
        
        if can_purchase:
            if zen_button(f"KUP 🪙 {item['name'].upper()}", key=f"buy_{category}_{item_id}", use_container_width=True):
                success, message = buy_item(st.session_state.username, category, item_id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        else:
            reason = "Już posiadane" if owned and item.get('one_time_purchase', False) else "Za mało DegenCoins"
            st.button(f"KUP ({reason})", disabled=True, key=f"buy_disabled_{category}_{item_id}", use_container_width=True)
    
    with col2:
        # Use/Equip button
        if category == 'booster' and owned:
            if zen_button(f"UŻYJ 🧙 {item['name'].split()[0].upper()}", key=f"use_{category}_{item_id}", use_container_width=True):
                success, message = use_booster(st.session_state.username, item_id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        elif category in ['avatar', 'background'] and owned:
            if equipped:
                st.success("Ten awatar jest aktualnie używany", icon="✅")
            else:
                if zen_button("Załóż", key=f"equip_{category}_{item_id}", use_container_width=True):
                    success, message = equip_cosmetic(st.session_state.username, category, item_id)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.empty()

def show_shop_category(category, category_name, user_inventory, device_type):
    """Display items for a specific category"""
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <h3 style="color: #1f2937; margin-bottom: 15px;">{category_name}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    items = SHOP_ITEMS.get(category, {})
    if not items:
        st.info(f"Brak dostępnych przedmiotów w kategorii {category_name}")
        return
    
    # Display items in single column layout like in the image
    for item_id, item in items.items():
        show_shop_item(category, item_id, item, user_inventory)

def show_active_boosters(active_boosters):
    """Wyświetl aktualnie aktywne wzmocnienia"""
    if not active_boosters:
        return
    
    st.markdown("### 🚀 Aktywne Wzmocnienia")
    
    current_time = datetime.now()
    expired_boosters = []
    
    for booster_id, booster_data in active_boosters.items():
        try:
            expires_at = datetime.fromisoformat(booster_data['expires_at'])
            time_left = expires_at - current_time
            
            if time_left.total_seconds() <= 0:
                expired_boosters.append(booster_id)
                continue
            
            # Format time left
            minutes_left = int(time_left.total_seconds() // 60)
            seconds_left = int(time_left.total_seconds() % 60)
            time_text = f"{minutes_left}m {seconds_left}s"
            
            effect = booster_data['effect']
            multiplier_text = f"{effect['value']}x XP" if effect['type'] == 'xp_multiplier' else "Efekt Specjalny"
            
            st.markdown(f"""
            <div class="active-booster">
                <div class="booster-name">{booster_data['name']}</div>
                <div class="booster-effect">{multiplier_text}</div>
                <div class="booster-time">⏰ {time_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            expired_boosters.append(booster_id)
    
    # Clean up expired boosters
    if expired_boosters:
        users_data = load_user_data()
        user_data = users_data.get(st.session_state.username, {})
        current_active = user_data.get('active_boosters', {})
        
        for expired_id in expired_boosters:
            current_active.pop(expired_id, None)
        
        user_data['active_boosters'] = current_active
        users_data[st.session_state.username] = user_data
        save_user_data(users_data)
        st.rerun()

def show_shop():
    """Główny interfejs sklepu Neurocoin"""
    # Apply Material3 theme
    apply_material3_theme()
    
    # Add custom CSS for shop styling to match the image
    st.markdown("""
    <style>
    /* Custom shop button styles */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    
    .stButton > button:disabled {
        background: #e5e7eb;
        color: #9ca3af;
        box-shadow: none;
        transform: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add zen header
    zen_header("Sklep Neurocoin 🧠")
    
    device_type = get_device_type()
    
    # Get user inventory and display balance
    user_inventory = get_user_inventory(st.session_state.username)
    
    # Display balance in the style shown in the image
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <h3 style="color: #64748b; margin-bottom: 10px;">Twoje DegenCoins: 🪙 {user_inventory['neurocoin']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Show active boosters if any
    if user_inventory['active_boosters']:
        show_active_boosters(user_inventory['active_boosters'])
        st.markdown("---")
    
    # Shop tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎭 Awatary", "🖼️ Tła", "⚡ Wzmocnienia", "📚 Lekcje Premium"])
    
    with tab1:
        show_shop_category('avatars', '🎭 Awatary', user_inventory, device_type)
    
    with tab2:
        show_shop_category('backgrounds', '🖼️ Tła', user_inventory, device_type)
    
    with tab3:
        show_shop_category('boosters', '⚡ Wzmocnienia XP', user_inventory, device_type)
    
    with tab4:
        show_shop_category('special_lessons', '📚 Lekcje Premium', user_inventory, device_type)
    
    # Footer with helpful information
    st.markdown("---")
    st.markdown("""
    ### ℹ️ Informacje o sklepie
    
    **Jak zdobywać Neurocoin:**
    - Ukończ lekcje, aby zdobyć Neurocoin równy zdobytemu XP
    - Twój aktualny balans Neurocoin: 🪙 """ + str(user_inventory['neurocoin']) + """
    
    **Typy przedmiotów:**
    - **Awatary**: Personalizuj wygląd swojego profilu
    - **Tła**: Zmień tło swojego dashboardu
    - **Wzmocnienia**: Tymczasowe mnożniki XP dla szybszego postępu
    - **Lekcje Premium**: Ekskluzywna zawartość dla zaawansowanej nauki
    
    **Poziomy rzadkości:**
    - <span style="color: #95a5a6;">**Pospolity**</span>: Podstawowe przedmioty, przystępne ceny
    - <span style="color: #3498db;">**Rzadki**</span>: Lepsze efekty, umiarkowane ceny  
    - <span style="color: #9b59b6;">**Bardzo Rzadki**</span>: Znaczące korzyści, wyższe ceny
    - <span style="color: #e74c3c;">**Epicki**</span>: Potężne efekty, premium ceny
    - <span style="color: #f39c12;">**Legendarny**</span>: Najlepsze przedmioty, ekskluzywna zawartość
    """, unsafe_allow_html=True)
