#!/usr/bin/env python3
"""
Complete migration script for BrainVenture Academy
Converts all test_scores from old degen type keys to new neuroleader type keys
"""

import json
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Migration mapping from old degen types to new neuroleader types
DEGEN_TO_NEUROLEADER_MAPPING = {
    "YOLO Degen": "Neuroreaktor",
    "FOMO Hunter": "Neuroreaktor", 
    "Emo Degen": "Neuroempata",
    "Hype Degen": "Neuroinspirator",
    "Strategist Degen": "Neuroanalityk",
    "Mad Scientist Degen": "Neuroanalityk",
    "Spreadsheet Degen": "Neuroanalityk",
    "Meta Degen": "Neuroinnowator",
    "Zen Degen": "Neurobalanser"
}

def load_users_data():
    """Load users data from JSON file"""
    users_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'users_data.json')
    try:
        with open(users_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading users data: {e}")
        return None

def save_users_data(data):
    """Save users data to JSON file"""
    users_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'users_data.json')
    try:
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ': '))
        return True
    except Exception as e:
        print(f"Error saving users data: {e}")
        return False

def migrate_test_scores(test_scores):
    """Convert test_scores from old degen keys to new neuroleader keys"""
    if not test_scores:
        return {}
    
    new_test_scores = {}
    
    for old_key, score in test_scores.items():
        # If it's already a neuroleader type, keep it
        if old_key in DEGEN_TO_NEUROLEADER_MAPPING.values():
            new_test_scores[old_key] = score
        # If it's an old degen type, convert it
        elif old_key in DEGEN_TO_NEUROLEADER_MAPPING:
            new_key = DEGEN_TO_NEUROLEADER_MAPPING[old_key]
            # If we already have this neuroleader type, add the scores
            if new_key in new_test_scores:
                new_test_scores[new_key] += score
            else:
                new_test_scores[new_key] = score
        else:
            # Unknown key, keep it but warn
            print(f"Warning: Unknown test score key '{old_key}', keeping as is")
            new_test_scores[old_key] = score
    
    return new_test_scores

def complete_migration():
    """Complete the migration of all user data"""
    print("Starting complete migration...")
    
    # Load current data
    users_data = load_users_data()
    if not users_data:
        print("Failed to load users data")
        return False
    
    print(f"Loaded data for {len(users_data)} users")
    
    migration_count = 0
    
    for username, user_data in users_data.items():
        if not user_data.get('test_taken', False):
            continue
            
        # Check if user has test_scores that need migration
        test_scores = user_data.get('test_scores', {})
        if not test_scores:
            continue
            
        # Check if any test score keys are old degen types
        needs_migration = any(key in DEGEN_TO_NEUROLEADER_MAPPING for key in test_scores.keys())
        
        if needs_migration:
            print(f"Migrating test scores for user '{username}'...")
            
            # Migrate test scores
            new_test_scores = migrate_test_scores(test_scores)
            users_data[username]['test_scores'] = new_test_scores
            
            # Ensure user has neuroleader_type field
            if 'neuroleader_type' not in user_data:
                # Find the highest scoring neuroleader type
                if new_test_scores:
                    highest_type = max(new_test_scores.items(), key=lambda x: x[1])[0]
                    users_data[username]['neuroleader_type'] = highest_type
                    print(f"  Set neuroleader_type to '{highest_type}'")
            
            # Update degen_type to match neuroleader_type for consistency
            if 'neuroleader_type' in users_data[username]:
                users_data[username]['degen_type'] = users_data[username]['neuroleader_type']
            
            migration_count += 1
            print(f"  Migrated test scores: {test_scores} -> {new_test_scores}")
    
    if migration_count > 0:
        # Save the updated data
        if save_users_data(users_data):
            print(f"Successfully migrated {migration_count} users")
            return True
        else:
            print("Failed to save migrated data")
            return False
    else:
        print("No users needed migration")
        return True

if __name__ == "__main__":
    success = complete_migration()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
        sys.exit(1)
