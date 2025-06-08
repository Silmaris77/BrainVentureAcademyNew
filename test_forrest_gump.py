#!/usr/bin/env python3
# Test script for the new Forrest Gump article

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.inspirations_loader import get_blog_articles, load_inspiration_content

def test_forrest_gump_article():
    print("=== Testing Forrest Gump Article Implementation ===\n")
    
    # Test 1: Load all blog articles
    print("1. Loading all blog articles...")
    try:
        articles = get_blog_articles()
        print(f"✅ Successfully loaded {len(articles)} articles")
        
        # Find the Forrest Gump article
        forrest_article = None
        for article in articles:
            if article['id'] == 'forrest_gump_neuroleadership':
                forrest_article = article
                break
                
        if forrest_article:
            print("✅ Found Forrest Gump article in blog articles")
            print(f"   Title: {forrest_article['title']}")
            print(f"   Author: {forrest_article['author']}")
            print(f"   Date: {forrest_article['date']}")
            print(f"   Tags: {', '.join(forrest_article['tags'])}")
        else:
            print("❌ Forrest Gump article not found in blog articles")
            return False
            
    except Exception as e:
        print(f"❌ Error loading blog articles: {e}")
        return False
    
    # Test 2: Load the article content
    print("\n2. Loading article content...")
    try:
        content = load_inspiration_content(forrest_article['file_path'])
        if content and len(content) > 100:
            print("✅ Successfully loaded article content")
            print(f"   Content length: {len(content)} characters")
            # Show first few lines
            lines = content.split('\n')[:5]
            print("   First few lines:")
            for line in lines:
                print(f"     {line}")
        else:
            print("❌ Article content is empty or too short")
            return False
    except Exception as e:
        print(f"❌ Error loading article content: {e}")
        return False
    
    print("\n=== All tests passed! ✅ ===")
    return True

if __name__ == "__main__":
    test_forrest_gump_article()
