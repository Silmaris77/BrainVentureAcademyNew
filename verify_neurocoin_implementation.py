"""
Simple verification script for Neurocoin system implementation
"""
import json
import sys
import os

def check_user_data():
    """Check if users have Neurocoin fields"""
    print("🔍 Checking user data structure...")
    
    try:
        with open('users_data.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        users_with_neurocoin = 0
        sample_user = None
        
        for username, user_data in users_data.items():
            if 'neurocoin' in user_data:
                users_with_neurocoin += 1
                if sample_user is None:
                    sample_user = (username, user_data)
        
        print(f"✅ {users_with_neurocoin}/{len(users_data)} users have Neurocoin field")
        
        if sample_user:
            username, data = sample_user
            print(f"📊 Sample user {username}:")
            print(f"   - XP: {data.get('xp', 0)}")
            print(f"   - Neurocoin: {data.get('neurocoin', 0)}")
            print(f"   - Has inventory: {'inventory' in data}")
            
        return users_with_neurocoin > 0
        
    except Exception as e:
        print(f"❌ Error reading user data: {e}")
        return False

def check_shop_import():
    """Check if shop can be imported"""
    print("\n🔍 Checking shop import...")
    
    try:
        from views.shop_neurocoin import SHOP_ITEMS, show_shop
        
        total_items = sum(len(items) for items in SHOP_ITEMS.values())
        print(f"✅ Shop imported successfully with {total_items} total items")
        
        categories = list(SHOP_ITEMS.keys())
        print(f"📦 Categories: {', '.join(categories)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing shop: {e}")
        return False

def check_dashboard_import():
    """Check if dashboard with Neurocoin support can be imported"""
    print("\n🔍 Checking dashboard import...")
    
    try:
        from views.dashboard import show_stats_section, show_neurocoin_shop_widget
        print("✅ Dashboard functions imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error importing dashboard: {e}")
        return False

def check_xp_system_import():
    """Check if XP/Neurocoin awarding system can be imported"""
    print("\n🔍 Checking XP/Neurocoin system import...")
    
    try:
        from utils.lesson_progress import award_fragment_xp
        from utils.real_time_updates import show_xp_notification
        print("✅ XP/Neurocoin awarding system imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error importing XP system: {e}")
        return False

def check_main_routing():
    """Check if main.py has correct routing"""
    print("\n🔍 Checking main.py routing...")
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'shop_neurocoin' in content:
            print("✅ Main.py has Neurocoin shop routing")
            return True
        else:
            print("❌ Main.py missing Neurocoin shop routing")
            return False
            
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🚀 NEUROCOIN SYSTEM VERIFICATION")
    print("=" * 40)
    
    checks = [
        ("User Data Structure", check_user_data),
        ("Shop Import", check_shop_import),
        ("Dashboard Import", check_dashboard_import),
        ("XP System Import", check_xp_system_import),
        ("Main Routing", check_main_routing),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            result = check_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {name} check failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 RESULTS: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED!")
        print("\n📝 Next steps:")
        print("1. Run: streamlit run main.py")
        print("2. Login to the application")
        print("3. Check dashboard for Neurocoin balance")
        print("4. Visit 'Sklep Neurocoin' in navigation")
        print("5. Complete a lesson to earn Neurocoin")
        print("6. Purchase items from the shop")
    else:
        print("⚠️ Some checks failed. Please review above.")
    
    return passed == total

if __name__ == "__main__":
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    main()
