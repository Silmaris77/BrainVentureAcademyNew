print("Starting badge test...")

try:
    from utils.achievements import check_achievements
    print("✅ Successfully imported check_achievements")
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

try:
    from data.users import load_user_data
    print("✅ Successfully imported load_user_data")
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

try:
    users_data = load_user_data()
    print(f"✅ Successfully loaded user data. Found {len(users_data)} users")
except Exception as e:
    print(f"❌ Load error: {e}")
    exit(1)

try:
    ola_data = users_data.get('ola', {})
    print(f"✅ Found user 'ola': test_taken={ola_data.get('test_taken')}, badges={ola_data.get('badges')}")
except Exception as e:
    print(f"❌ User data error: {e}")
    exit(1)

try:
    print("Calling check_achievements for user 'ola'...")
    new_badges = check_achievements('ola')
    print(f"✅ Function completed. New badges: {new_badges}")
except Exception as e:
    print(f"❌ Achievement check error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("Test completed successfully!")
