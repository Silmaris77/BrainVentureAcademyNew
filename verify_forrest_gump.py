#!/usr/bin/env python3
"""
Final verification script for the Forrest Gump article implementation
This script verifies that the article is properly integrated into the blog system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.inspirations_loader import get_blog_articles, load_inspiration_content, search_inspirations

def main():
    print("🎬 FORREST GUMP ARTICLE VERIFICATION")
    print("=" * 50)
    
    # Test 1: Verify article exists in blog articles
    print("\n1. 📚 Loading blog articles...")
    articles = get_blog_articles()
    print(f"   Total articles found: {len(articles)}")
    
    forrest_article = None
    for article in articles:
        if article['id'] == 'forrest_gump_neuroleadership':
            forrest_article = article
            break
    
    if forrest_article:
        print("   ✅ Forrest Gump article found!")
        print(f"   📝 Title: {forrest_article['title']}")
        print(f"   👤 Author: {forrest_article['author']}")
        print(f"   📅 Date: {forrest_article['date']}")
        print(f"   🎯 Icon: {forrest_article['icon']}")
        print(f"   🏷️ Tags: {', '.join(forrest_article['tags'])}")
    else:
        print("   ❌ Forrest Gump article NOT found!")
        return False
    
    # Test 2: Verify article content loads properly
    print("\n2. 📄 Loading article content...")
    try:
        content = load_inspiration_content(forrest_article['file_path'])
        if content and len(content) > 500:
            print("   ✅ Article content loaded successfully!")
            print(f"   📊 Content length: {len(content)} characters")
            
            # Check key sections
            sections = ["Wprowadzenie", "Autentyczność", "Empatia", "Prostota", "Wytrwałość", "Przywództwo"]
            found_sections = []
            for section in sections:
                if section in content:
                    found_sections.append(section)
            
            print(f"   📋 Sections found: {len(found_sections)}/{len(sections)}")
            print(f"   🔍 Sections: {', '.join(found_sections)}")
        else:
            print("   ❌ Article content is missing or too short!")
            return False
    except Exception as e:
        print(f"   ❌ Error loading content: {e}")
        return False
    
    # Test 3: Verify search functionality works
    print("\n3. 🔍 Testing search functionality...")
    search_results = search_inspirations("Forrest", "blog")
    if search_results:
        print("   ✅ Search for 'Forrest' works!")
        print(f"   🎯 Found {len(search_results)} results")
    else:
        print("   ❌ Search functionality failed!")
        return False
    
    # Test 4: Verify tag-based search
    print("\n4. 🏷️ Testing tag-based search...")
    neuroleadership_results = search_inspirations("neuroprzywództwo", "blog")
    if neuroleadership_results:
        print("   ✅ Tag-based search works!")
        print(f"   🎯 Found {len(neuroleadership_results)} results for 'neuroprzywództwo'")
    else:
        print("   ❌ Tag-based search failed!")
        return False
    
    # Test 5: Show article preview
    print("\n5. 👀 Article preview:")
    print("   " + "─" * 60)
    preview_lines = content.split('\n')[:15]
    for line in preview_lines:
        if line.strip():
            print(f"   {line}")
    print("   " + "─" * 60)
    
    print("\n🎉 ALL TESTS PASSED! 🎉")
    print("The Forrest Gump article is successfully integrated into the blog system!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
