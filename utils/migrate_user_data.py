# Data migration utility for converting old degen types to new neuroleader types
import json
import os

def load_user_data():
    """Load user data from JSON file"""
    try:
        with open('users_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    """Save user data to JSON file"""
    with open('users_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Mapping from old degen types to new neuroleader types
OLD_TO_NEW_TYPE_MAPPING = {
    # Old degen types -> New neuroleader types
    "YOLO Degen": "Neuroreaktor",        # Impulsive, quick decisions -> Impulsive Guardian
    "FOMO Hunter": "Neuroreaktor",       # Fear of missing out -> Impulsive Guardian  
    "Emo Degen": "Neuroempata",          # Emotional decisions -> Relationship Architect
    "Hype Degen": "Neuroinspirator",     # Following trends, charismatic -> Charismatic Visionary
    "Strategist Degen": "Neuroanalityk", # Strategic, analytical -> Risk-Averse Analyst
    "Mad Scientist Degen": "Neuroanalityk", # Analysis paralysis -> Risk-Averse Analyst
    "Spreadsheet Degen": "Neuroanalityk",   # Over-analysis -> Risk-Averse Analyst
    "Meta Degen": "Neuroinnowator",      # Innovation focused -> Change Navigator
    "Zen Degen": "Neurobalanser",        # Balanced approach -> Balanced Integrator
    
    # Handle null/None cases
    None: None,
    "null": None,
    "": None
}

def migrate_user_types():
    """
    Migrates users from old degen type format to new neuroleader type format.
    Updates both degen_type and neuroleader_type fields for consistency.
    """
    print("🔄 Starting user data migration...")
    
    users_data = load_user_data()
    migrated_count = 0
    error_count = 0
    
    for username, user_data in users_data.items():
        try:
            current_degen_type = user_data.get('degen_type')
            current_neuroleader_type = user_data.get('neuroleader_type')
            
            # Check if user needs migration
            if current_degen_type in OLD_TO_NEW_TYPE_MAPPING:
                new_type = OLD_TO_NEW_TYPE_MAPPING[current_degen_type]
                
                # Only migrate if the user doesn't already have the new format
                if current_neuroleader_type != new_type:
                    users_data[username]['neuroleader_type'] = new_type
                    users_data[username]['degen_type'] = new_type  # Keep for backward compatibility
                    
                    print(f"✅ Migrated user '{username}': '{current_degen_type}' -> '{new_type}'")
                    migrated_count += 1
                else:
                    print(f"⏭️ User '{username}' already has correct type: '{new_type}'")
            
            elif current_degen_type is None and not user_data.get('test_taken', False):
                # User hasn't taken test yet - no migration needed
                print(f"⏭️ User '{username}' hasn't taken test yet - no migration needed")
            
            elif current_degen_type and current_degen_type not in OLD_TO_NEW_TYPE_MAPPING:
                # User already has new format or unknown type
                print(f"⏭️ User '{username}' has type '{current_degen_type}' - no migration needed")
                
        except Exception as e:
            print(f"❌ Error migrating user '{username}': {e}")
            error_count += 1
    
    # Save migrated data
    if migrated_count > 0:
        try:
            save_user_data(users_data)
            print(f"\n✅ Migration completed successfully!")
            print(f"📊 Summary:")
            print(f"   - Users migrated: {migrated_count}")
            print(f"   - Errors: {error_count}")
            print(f"   - Total users: {len(users_data)}")
        except Exception as e:
            print(f"❌ Error saving migrated data: {e}")
    else:
        print(f"\n✅ No migration needed - all users already have correct format!")

def validate_migration():
    """
    Validates that migration was successful by checking user data consistency.
    """
    print("\n🔍 Validating migration results...")
    
    users_data = load_user_data()
    
    old_format_users = []
    new_format_users = []
    inconsistent_users = []
    no_test_users = []
    
    for username, user_data in users_data.items():
        degen_type = user_data.get('degen_type')
        neuroleader_type = user_data.get('neuroleader_type')
        test_taken = user_data.get('test_taken', False)
        
        if not test_taken:
            no_test_users.append(username)
        elif degen_type in OLD_TO_NEW_TYPE_MAPPING.keys() and degen_type not in ["Neuroanalityk", "Neuroreaktor", "Neurobalanser", "Neuroempata", "Neuroinnowator", "Neuroinspirator"]:
            old_format_users.append((username, degen_type))
        elif degen_type in ["Neuroanalityk", "Neuroreaktor", "Neurobalanser", "Neuroempata", "Neuroinnowator", "Neuroinspirator"]:
            if neuroleader_type == degen_type:
                new_format_users.append((username, degen_type))
            else:
                inconsistent_users.append((username, degen_type, neuroleader_type))
    
    print(f"📊 Validation Results:")
    print(f"   - Users with new format: {len(new_format_users)}")
    print(f"   - Users with old format: {len(old_format_users)}")
    print(f"   - Users with inconsistent data: {len(inconsistent_users)}")
    print(f"   - Users who haven't taken test: {len(no_test_users)}")
    
    if old_format_users:
        print(f"\n⚠️ Users still with old format:")
        for username, old_type in old_format_users:
            print(f"   - {username}: {old_type}")
    
    if inconsistent_users:
        print(f"\n❌ Users with inconsistent data:")
        for username, degen_type, neuroleader_type in inconsistent_users:
            print(f"   - {username}: degen_type='{degen_type}', neuroleader_type='{neuroleader_type}'")
    
    return len(old_format_users) == 0 and len(inconsistent_users) == 0

if __name__ == "__main__":
    migrate_user_types()
    validate_migration()
