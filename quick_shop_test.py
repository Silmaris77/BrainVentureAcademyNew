import sys
sys.path.append('.')

try:
    from views.shop_neurocoin import SHOP_ITEMS, RARITY_TRANSLATIONS
    print("SUCCESS: Shop imports working")
    print(f"Shop has {len(SHOP_ITEMS)} categories")
    print(f"Rarity translations: {list(RARITY_TRANSLATIONS.keys())}")
    
    # Check specific translations
    neural_leader = SHOP_ITEMS['avatars']['neural_leader']['name']
    print(f"Neural Leader translated to: {neural_leader}")
    
except Exception as e:
    print(f"ERROR: {e}")
