# Plik: initialize_neurocoin.py
import json
import os
from datetime import datetime

def initialize_neurocoin_for_existing_users():
    """
    Inicjalizuje Neurocoin dla wszystkich istniejących użytkowników
    Przyznaje Neurocoin równe obecnemu XP
    """
    print("🧠 Inicjalizacja systemu Neurocoin...")
    print("=" * 50)
    
    # Załaduj dane użytkowników
    users_file = 'users_data.json'
    
    if not os.path.exists(users_file):
        print("❌ Plik users_data.json nie został znaleziony!")
        return
    
    with open(users_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    print(f"📊 Znaleziono {len(users_data)} użytkowników do aktualizacji")
    
    updated_count = 0
    
    for username, user_data in users_data.items():
        # Sprawdź czy użytkownik już ma Neurocoin
        if 'neurocoin' not in user_data:
            # Przyznaj Neurocoin równe obecnemu XP
            current_xp = user_data.get('xp', 0)
            user_data['neurocoin'] = current_xp
            
            # Dodaj inventory dla przyszłych zakupów
            if 'inventory' not in user_data:
                user_data['inventory'] = {
                    "avatar": [],
                    "background": [],
                    "special_lesson": [],
                    "booster": []
                }
            
            # Dodaj active_boosters
            if 'active_boosters' not in user_data:
                user_data['active_boosters'] = {}
            
            # Dodaj aktywne kosmetyki
            if 'active_avatar' not in user_data:
                user_data['active_avatar'] = 'default'
            
            if 'active_background' not in user_data:
                user_data['active_background'] = 'default'
            
            updated_count += 1
            print(f"✅ {username}: przyznano {current_xp} Neurocoin (= XP)")
        else:
            print(f"⏭️ {username}: już posiada Neurocoin ({user_data.get('neurocoin', 0)})")
    
    # Zapisz zaktualizowane dane
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"🎉 Migracja zakończona!")
    print(f"📈 Zaktualizowano: {updated_count} użytkowników")
    print(f"📅 Data migracji: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    initialize_neurocoin_for_existing_users()
