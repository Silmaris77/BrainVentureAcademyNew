#!/usr/bin/env python3
"""Very simple shop test"""

try:
    from views.shop_neurocoin import SHOP_ITEMS, RARITY_TRANSLATIONS
    print("✅ Shop imported successfully!")
    print(f"Shop items count: {len(SHOP_ITEMS)}")
    print(f"Categories: {list(SHOP_ITEMS.keys())}")
    print(f"Polish rarity translations: {len(RARITY_TRANSLATIONS)}")
    print("✅ Basic shop functionality confirmed!")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
