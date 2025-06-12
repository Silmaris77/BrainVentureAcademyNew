import json

# Test sprawdzający czy artykuł o żuciu gumy został dodany
try:
    with open('data/inspirations/inspirations_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    facts = data.get('facts', [])
    chewing_gum_fact = None
    
    for fact in facts:
        if fact.get('id') == 'chewing_gum_brain':
            chewing_gum_fact = fact
            break
    
    if chewing_gum_fact:
        print("✅ Artykuł znaleziony!")
        print(f"Tytuł: {chewing_gum_fact['title']}")
        print(f"Ikona: {chewing_gum_fact['icon']}")
        print(f"Źródło: {chewing_gum_fact['source']}")
        print(f"Ścieżka: {chewing_gum_fact['file_path']}")
        print(f"Tagi: {', '.join(chewing_gum_fact['tags'])}")
        
        # Sprawdź czy plik MD istnieje
        import os
        md_path = os.path.join('data', 'inspirations', chewing_gum_fact['file_path'])
        if os.path.exists(md_path):
            print("✅ Plik Markdown istnieje")
        else:
            print("❌ Plik Markdown nie istnieje")
    else:
        print("❌ Artykuł nie znaleziony")
        
except Exception as e:
    print(f"❌ Błąd: {e}")
