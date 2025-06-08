import os
import json
import streamlit as st

# Ścieżka do katalogu data/inspirations względem głównego katalogu aplikacji
INSPIRATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "inspirations")
CONFIG_PATH = os.path.join(INSPIRATIONS_DIR, "inspirations_data.json")

def load_inspirations_data():
    """
    Wczytuje dane o inspiracjach z pliku JSON.
    
    Returns:
        dict: Dane o artykułach, tutorialach i ciekawostkach
    """
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Błąd podczas wczytywania danych inspiracji: {str(e)}")
        # Zwracamy pustą strukturę w przypadku błędu
        return {
            "blog_articles": [],
            "tutorials": [],
            "facts": []
        }

def load_inspiration_content(file_path):
    """
    Wczytuje zawartość pliku z inspiracją.
    
    Args:
        file_path (str): Względna ścieżka do pliku wewnątrz katalogu data/inspirations
        
    Returns:
        str: Zawartość pliku lub komunikat o błędzie
    """
    full_path = os.path.join(INSPIRATIONS_DIR, file_path)
    
    try:
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        else:
            return f"Nie znaleziono pliku: {file_path}"
    except Exception as e:
        return f"Błąd podczas wczytywania pliku: {str(e)}"

def get_blog_articles():
    """Zwraca listę artykułów bloga"""
    data = load_inspirations_data()
    return data.get("blog_articles", [])

def get_tutorials():
    """Zwraca listę tutoriali"""
    data = load_inspirations_data()
    return data.get("tutorials", [])

def get_facts():
    """Zwraca listę ciekawostek"""
    data = load_inspirations_data()
    return data.get("facts", [])

def search_inspirations(query):
    """
    Wyszukuje inspiracje zawierające podaną frazę.
    
    Args:
        query (str): Fraza do wyszukania
        
    Returns:
        dict: Słownik z listami pasujących artykułów, tutoriali i ciekawostek
    """
    query = query.lower()
    data = load_inspirations_data()
    
    # Funkcja pomocnicza do sprawdzania czy element zawiera frazę
    def contains_query(item):
        # Sprawdzamy w tytule
        if query in item.get("title", "").lower():
            return True
        # Sprawdzamy w treści
        if query in item.get("content", "").lower():
            return True
        # Sprawdzamy w tagach
        for tag in item.get("tags", []):
            if query in tag.lower():
                return True
        # Sprawdzamy w autorze (dla artykułów)
        if "author" in item and query in item["author"].lower():
            return True
        return False
    
    # Filtrujemy każdą kategorię
    matched_articles = [item for item in data.get("blog_articles", []) if contains_query(item)]
    matched_tutorials = [item for item in data.get("tutorials", []) if contains_query(item)]
    matched_facts = [item for item in data.get("facts", []) if contains_query(item)]
    
    return {
        "blog_articles": matched_articles,
        "tutorials": matched_tutorials,
        "facts": matched_facts
    }
