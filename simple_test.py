import sys
sys.path.append('.')

from utils.user_management import load_user_data
from data.neuroleader_details import degen_details

print('=== TESTING PROFILE DATA LOADING FIX ===')

# Test the data loading fix
users_data = load_user_data()
user_data = users_data.get('a', {})

print(f'User data keys: {list(user_data.keys())}')
print(f'neuroleader_type: {user_data.get("neuroleader_type")}')
print(f'degen_type: {user_data.get("degen_type")}') 
print(f'test_taken: {user_data.get("test_taken")}')
print(f'has_test_scores: {"test_scores" in user_data}')

# Test the neuroleader type resolution
neuroleader_type = user_data.get('neuroleader_type') or user_data.get('degen_type', 'Typ nie określony')
test_taken = user_data.get('test_taken', False)
has_test_scores = 'test_scores' in user_data

print(f'\nResolved neuroleader_type: {neuroleader_type}')
print(f'Condition check - neuroleader_type exists: {bool(neuroleader_type and neuroleader_type != "Typ nie określony")}')
print(f'Condition check - test_taken or has_test_scores: {test_taken or has_test_scores}')

should_display = bool(neuroleader_type and neuroleader_type != "Typ nie określony") and (test_taken or has_test_scores)
print(f'Should display neuroleader section: {should_display}')

if neuroleader_type in degen_details:
    print(f'\nNeuroleader details found for {neuroleader_type}')
    details = degen_details[neuroleader_type]
    print(f'Title: {details.get("title", "Brak tytułu")}')
    print(f'Description length: {len(details.get("description", ""))} characters')
else:
    print(f'\nERROR: No details found for neuroleader type: {neuroleader_type}')

print(f'\n=== RESULT: {"✅ FIX SUCCESSFUL" if should_display else "❌ ISSUE REMAINS"} ===')
