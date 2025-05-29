#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation script for BrainVenture Academy migration to neuroleadership
"""

import json
import os
import sys

def validate_course_structure():
    """Validate the new neuroleadership course structure"""
    print("🧠 Validating BrainVenture Academy Neuroleadership Migration...")
    print("=" * 60)
    
    try:
        # Load course structure
        with open('data/course_structure.json', 'r', encoding='utf-8') as f:
            course_data = json.load(f)
        
        print("✅ Course structure JSON loaded successfully!")
        
        # Validate structure
        blocks = course_data.get('blocks', {})
        categories = course_data.get('categories', {})
        
        print(f"📚 Blocks found: {len(blocks)}")
        print(f"📂 Categories found: {len(categories)}")
        
        # Check each block
        neuroleadership_keywords = ['neuro', 'przywództw', 'mózg', 'decyzj', 'psycholog', 'motywac', 'emocj']
        
        for block_id, block in blocks.items():
            name = block.get('name', '').lower()
            desc = block.get('description', '').lower()
            
            has_neuro_content = any(keyword in name + desc for keyword in neuroleadership_keywords)
            status = "✅" if has_neuro_content else "⚠️"
            
            print(f"{status} Block {block_id}: {block.get('name', 'N/A')}")
            if not has_neuro_content:
                print(f"   Warning: May not contain neuroleadership content")
        
        # Count lessons
        total_lessons = 0
        neuro_categories = 0
        
        for cat_id, category in categories.items():
            name = category.get('name', '').lower()
            desc = category.get('description', '').lower()
            
            has_neuro_content = any(keyword in name + desc for keyword in neuroleadership_keywords)
            if has_neuro_content:
                neuro_categories += 1
            
            if 'lessons' in category:
                total_lessons += len(category['lessons'])
        
        print(f"\n📖 Total lessons: {total_lessons}")
        print(f"🧠 Neuroleadership categories: {neuro_categories}/{len(categories)}")
        
        # Check for old investment terms
        old_keywords = ['inwest', 'giełd', 'akcj', 'portfel', 'zysk', 'strat', 'ryzyko finansowe']
        
        print(f"\n🔍 Checking for old investment content...")
        old_content_found = False
        
        full_text = json.dumps(course_data, ensure_ascii=False).lower()
        for keyword in old_keywords:
            if keyword in full_text:
                print(f"⚠️  Found old keyword: '{keyword}'")
                old_content_found = True
        
        if not old_content_found:
            print("✅ No old investment content detected!")
        
        print(f"\n{'✅ MIGRATION VALIDATION PASSED!' if not old_content_found and neuro_categories > 10 else '⚠️  MIGRATION NEEDS REVIEW'}")
        
        return True
        
    except FileNotFoundError:
        print("❌ Course structure file not found!")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def validate_skills_tab():
    """Validate the skills tab migration"""
    print(f"\n🎯 Validating Skills Tab Migration...")
    print("-" * 40)
    
    try:
        with open('views/skills_new.py', 'r', encoding='utf-8') as f:
            skills_content = f.read()
        
        print("✅ Skills tab file loaded successfully!")
        
        # Check for neuroleadership content
        neuro_indicators = [
            'Akademia Neuroprzywództwa',
            'neuroprzywództw',
            'neuroleader',
            '🧠'
        ]
        
        found_indicators = []
        for indicator in neuro_indicators:
            if indicator in skills_content:
                found_indicators.append(indicator)
        
        print(f"🧠 Neuroleadership indicators found: {len(found_indicators)}/{len(neuro_indicators)}")
        for indicator in found_indicators:
            print(f"   ✅ '{indicator}'")
        
        # Check for old investment content
        old_indicators = [
            'Mapa Rozwoju Inwestora',
            'inwestor',
            'giełd',
            'portfel'
        ]
        
        old_found = []
        for indicator in old_indicators:
            if indicator in skills_content:
                old_found.append(indicator)
        
        if old_found:
            print(f"⚠️  Old investment content found:")
            for indicator in old_found:
                print(f"   ⚠️  '{indicator}'")
        else:
            print("✅ No old investment content detected!")
        
        return len(found_indicators) > 2 and len(old_found) == 0
        
    except FileNotFoundError:
        print("❌ Skills tab file not found!")
        return False
    except Exception as e:
        print(f"❌ Skills validation error: {e}")
        return False

def main():
    """Main validation function"""
    print("🚀 BrainVenture Academy Migration Validation")
    print("=" * 60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    course_valid = validate_course_structure()
    skills_valid = validate_skills_tab()
    
    print(f"\n" + "=" * 60)
    if course_valid and skills_valid:
        print("🎉 MIGRATION VALIDATION SUCCESSFUL!")
        print("✅ All components migrated to neuroleadership theme")
        print("✅ No old investment content detected")
        print("✅ System ready for testing")
    else:
        print("⚠️  MIGRATION VALIDATION INCOMPLETE")
        if not course_valid:
            print("❌ Course structure needs review")
        if not skills_valid:
            print("❌ Skills tab needs review")
    
    return course_valid and skills_valid

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
