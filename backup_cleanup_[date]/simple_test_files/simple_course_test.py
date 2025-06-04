import json

# Test wczytywania struktury kursu
try:
    with open('data/course_structure.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("✅ Plik JSON został poprawnie wczytany")
    print(f"Bloki: {len(data.get('blocks', {}))}")
    print(f"Kategorie: {len(data.get('categories', {}))}")
    print(f"Lekcje: {len(data.get('lessons', {}))}")
    
    # Sprawdź pierwsze 3 bloki
    blocks = data.get('blocks', {})
    for i, (block_id, block) in enumerate(list(blocks.items())[:3]):
        print(f"\nBlok {block_id}: {block['name']}")
        print(f"Kategorie: {block['categories']}")
        
except Exception as e:
    print(f"❌ Błąd: {e}")
