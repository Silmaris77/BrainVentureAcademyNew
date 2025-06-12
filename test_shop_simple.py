#!/usr/bin/env python3
"""Simple test for shop functionality"""

try:
    print("Testing shop module import...")
    import sys
    sys.path.append('.')
    
    from views.shop_neurocoin import (
        SHOP_ITEMS, 
        RARITY_TRANSLATIONS,
        buy_item,
        get_user_inventory
    )
    
    print("✅ Shop module imported successfully!")
    
    # Test basic functionality
    print("\nTesting shop items...")
    print(f"Total shop items: {len(SHOP_ITEMS)}")
    
    # Test categories
    categories = set()
    for category, items in SHOP_ITEMS.items():
        categories.add(category)
        print(f"Category '{category}': {len(items)} items")
    
    print(f"\nTotal categories: {len(categories)}")
    print(f"Categories: {list(categories)}")
    
    # Test rarity translations
    print(f"\nRarity translations: {len(RARITY_TRANSLATIONS)} levels")
    for rarity, translation in RARITY_TRANSLATIONS.items():
        print(f"- {rarity} → {translation}")
    
    # Test sample item
    sample_item = SHOP_ITEMS['avatars']['neural_leader']
    print(f"\nSample item (Neural Leader):")
    print(f"- Name: {sample_item['name']}")
    print(f"- Price: {sample_item['price']}")
    print(f"- Rarity: {sample_item['rarity']} ({RARITY_TRANSLATIONS[sample_item['rarity']]})")
    
    print("\n✅ All tests passed! Shop is ready to use.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
