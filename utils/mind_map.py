"""
Funkcje do generowania interaktywnych map myśli dla lekcji
"""
import streamlit as st

def create_lesson_mind_map(lesson_data):
    """
    Tworzy interaktywną mapę myśli dla danej lekcji
    Implementuje system skalowalny z trzema trybami:
    1. Data-driven - używa danych z lesson_data['mind_map']
    2. Backward compatibility - dla B1C1L1 (stary hardcoded system)
    3. Auto-generated - automatyczne generowanie dla lekcji bez dedykowanych danych
    
    Args:
        lesson_data (dict): Dane lekcji w formacie JSON
    """
    try:
        # Inteligentna logika decyzyjna
        if 'mind_map' in lesson_data:
            # Tryb 1: Data-driven - używaj danych z JSON
            return create_data_driven_mind_map(lesson_data['mind_map'])
        elif lesson_data.get('id') == 'B1C1L1':
            # Tryb 2: Backward compatibility dla B1C1L1c
            return create_b1c1l1_mind_map()
        else:
            # Tryb 3: Auto-generated dla pozostałych lekcji
            return create_auto_generated_mind_map(lesson_data)
            
    except ImportError:
        # Fallback jeśli streamlit-agraph nie jest dostępne
        st.warning("📋 Mapa myśli nie jest obecnie dostępna. Zainstaluj bibliotekę streamlit-agraph aby włączyć tę funkcję.")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia mapy myśli: {str(e)}")
        return None

def create_b1c1l1_mind_map():
    """
    Tworzy mapę myśli specjalnie dla lekcji B1C1L1 - Strach przed stratą
    """
    try:
        from streamlit_agraph import agraph, Node, Edge, Config
        
        # Definiuj węzły
        nodes = []
        edges = []
          # Centralny węzeł
        nodes.append(Node(id="central", 
                         label="💸 STRACH PRZED STRATĄ", 
                         size=30,
                         color="#FF6B6B",
                         font={"size": 16, "color": "#FF6B6B"}))  # Kolor czcionki pasuje do węzła
        
        # Główne koncepty
        concepts = [
            {"id": "teoria", "label": "📊 Teoria perspektywy", "color": "#4ECDC4"},
            {"id": "dyspozycja", "label": "🔄 Efekt dyspozycji", "color": "#45B7D1"},
            {"id": "dopamina", "label": "🧠 Dopamina", "color": "#96CEB4"},
            {"id": "framing", "label": "🖼️ Framing", "color": "#FECA57"}        ]
        
        for concept in concepts:
            nodes.append(Node(id=concept["id"],
                            label=concept["label"],
                            size=20,
                            color=concept["color"],
                            font={"size": 12, "color": concept["color"]}))  # Kolor czcionki pasuje do węzła
            edges.append(Edge(source="central", target=concept["id"]))
        
        # Szczegóły teorii perspektywy
        teoria_details = [
            {"id": "bol_straty", "label": "😢 Ból straty 2-2,5x silniejszy", "parent": "teoria"},
            {"id": "pewnosc", "label": "🛡️ Preferujemy pewność", "parent": "teoria"},
            {"id": "awersja", "label": "⚠️ Awersja do ryzyka", "parent": "teoria"}
        ]
        
        # Szczegóły efektu dyspozycji
        dyspozycja_details = [
            {"id": "sprzedaj_zyski", "label": "💰 Za szybko sprzedajemy zyski", "parent": "dyspozycja"},
            {"id": "trzymaj_straty", "label": "📉 Za długo trzymamy straty", "parent": "dyspozycja"},
            {"id": "get_even", "label": "🎯 Syndrom 'wyjdę na zero'", "parent": "dyspozycja"}
        ]
        
        # Szczegóły dopaminy
        dopamina_details = [
            {"id": "nagroda", "label": "🎉 System nagrody w mózgu", "parent": "dopamina"},
            {"id": "uzaleznienie", "label": "🎰 Uzależnienie od transakcji", "parent": "dopamina"},
            {"id": "euforia", "label": "🚀 Euforia po zyskach", "parent": "dopamina"}
        ]
        
        # Szczegóły framingu
        framing_details = [
            {"id": "prezentacja", "label": "📝 Sposób prezentacji wpływa na decyzje", "parent": "framing"},
            {"id": "pozytywny", "label": "😊 Pozytywne vs negatywne ujęcie", "parent": "framing"},
            {"id": "manipulacja", "label": "🎭 Podatność na manipulację", "parent": "framing"}
        ]
          # Dodaj wszystkie szczegóły
        all_details = teoria_details + dyspozycja_details + dopamina_details + framing_details
        
        for detail in all_details:
            nodes.append(Node(id=detail["id"],
                            label=detail["label"],
                            size=12,
                            color="#DDA0DD",
                            font={"size": 10, "color": "#DDA0DD"}))  # Kolor czcionki pasuje do węzła
            edges.append(Edge(source=detail["parent"], target=detail["id"]))
        
        # Rozwiązania praktyczne
        solutions = [
            {"id": "zoom_out", "label": "🔍 Zoom out - szeroka perspektywa"},
            {"id": "limit_strat", "label": "🚧 Wyznacz limit strat"},
            {"id": "stop_checking", "label": "📵 Przestań sprawdzać apki"},
            {"id": "plan", "label": "📋 Trzymaj się planu"}        ]
        
        for solution in solutions:
            nodes.append(Node(id=solution["id"],
                            label=solution["label"],
                            size=15,
                            color="#90EE90",
                            font={"size": 11, "color": "#90EE90"}))  # Kolor czcionki pasuje do węzła
            edges.append(Edge(source="central", target=solution["id"]))
          # Case study - Kuba
        nodes.append(Node(id="kuba",
                        label="👨‍💻 Case Study: Kuba i $MOONZ",
                        size=18,
                        color="#FF8C42",
                        font={"size": 12, "color": "#FF8C42"}))  # Kolor czcionki pasuje do węzła
        edges.append(Edge(source="central", target="kuba"))
        
        kuba_details = [
            {"id": "fomo", "label": "😱 FOMO na $MOONZ", "parent": "kuba"},
            {"id": "spadek", "label": "📉 -20% w 2 dni", "parent": "kuba"},
            {"id": "panika", "label": "😰 Panika i sprawdzanie co 3 min", "parent": "kuba"}        ]
        
        for detail in kuba_details:
            nodes.append(Node(id=detail["id"],
                            label=detail["label"],
                            size=10,
                            color="#FFB347",
                            font={"size": 9, "color": "#FFB347"}))  # Kolor czcionki pasuje do węzła
            edges.append(Edge(source=detail["parent"], target=detail["id"]))
          # Konfiguracja wyświetlania
        config = Config(width=900,   # Zwiększona szerokość jak w course_map
                       height=850,   # Zwiększona wysokość jak w course_map
                       directed=False,
                       physics=True,
                       hierarchical=False,
                       nodeHighlightBehavior=True,
                       highlightColor="#F7A7A6",
                       collapsible=False)
        
        # Wyświetl mapę
        return_value = agraph(nodes=nodes, 
                             edges=edges, 
                             config=config)
        
        return return_value
        
    except ImportError:
        st.error("Nie można załadować biblioteki streamlit-agraph. Zainstaluj ją używając: pip install streamlit-agraph")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia mapy myśli: {str(e)}")
        return None

def create_generic_mind_map(lesson_data):
    """
    PRZESTARZAŁA: Używaj create_auto_generated_mind_map
    Zachowana dla zgodności wstecznej
    """
    return create_auto_generated_mind_map(lesson_data)

def create_data_driven_mind_map(mind_map_data):
    """
    Tworzy mapę myśli z danych strukturalnych JSON
    
    Args:
        mind_map_data (dict): Struktura mind_map z pliku JSON lekcji
    """
    try:
        from streamlit_agraph import agraph, Node, Edge, Config
        
        nodes = []
        edges = []
          # Centralny węzeł
        central = mind_map_data.get('central_node', {})
        nodes.append(Node(
            id=central.get('id', 'main_topic'),
            label=central.get('label', '🎯 GŁÓWNY TEMAT'),
            size=central.get('size', 30),
            color=central.get('color', '#FF6B6B'),
            font={"size": central.get('font_size', 16), "color": central.get('color', '#FF6B6B')}
        ))
          # Kategorie główne
        for category in mind_map_data.get('categories', []):
            nodes.append(Node(
                id=category.get('id', 'category'),
                label=category.get('label', 'Kategoria'),
                size=category.get('size', 20),
                color=category.get('color', '#4ECDC4'),
                font={"size": category.get('font_size', 12), "color": category.get('color', '#4ECDC4')}
            ))
            edges.append(Edge(source=central.get('id', 'main_topic'), target=category.get('id', 'category')))
            
            # Szczegóły kategorii
            for detail in category.get('details', []):
                nodes.append(Node(
                    id=detail.get('id', 'detail'),
                    label=detail.get('label', 'Szczegół'),
                    size=detail.get('size', 12),
                    color=detail.get('color', '#DDA0DD'),
                    font={"size": detail.get('font_size', 10), "color": detail.get('color', '#DDA0DD')}
                ))
                edges.append(Edge(source=category.get('id', 'category'), target=detail.get('id', 'detail')))
          # Rozwiązania praktyczne
        for solution in mind_map_data.get('solutions', []):
            nodes.append(Node(
                id=solution.get('id', 'solution'),
                label=solution.get('label', 'Rozwiązanie'),
                size=solution.get('size', 15),
                color=solution.get('color', '#90EE90'),
                font={"size": solution.get('font_size', 11), "color": solution.get('color', '#90EE90')}
            ))
            edges.append(Edge(source=central.get('id', 'main_topic'), target=solution.get('id', 'solution')))
          # Case study
        case_study = mind_map_data.get('case_study', {})
        if case_study:
            nodes.append(Node(
                id=case_study.get('id', 'case_study'),
                label=case_study.get('label', '📱 Case Study'),
                size=case_study.get('size', 18),
                color=case_study.get('color', '#FF8C42'),
                font={"size": case_study.get('font_size', 12), "color": case_study.get('color', '#FF8C42')}
            ))
            edges.append(Edge(source=central.get('id', 'main_topic'), target=case_study.get('id', 'case_study')))
            
            # Szczegóły case study
            for detail in case_study.get('details', []):
                nodes.append(Node(
                    id=detail.get('id', 'case_detail'),
                    label=detail.get('label', 'Szczegół'),
                    size=detail.get('size', 10),
                    color=detail.get('color', '#FFB347'),
                    font={"size": detail.get('font_size', 9), "color": detail.get('color', '#FFB347')}
                ))
                edges.append(Edge(source=case_study.get('id', 'case_study'), target=detail.get('id', 'case_detail')))
        
        # Dodatkowe połączenia
        for connection in mind_map_data.get('connections', []):
            edges.append(Edge(source=connection.get('from'), target=connection.get('to')))
          # Konfiguracja
        config_data = mind_map_data.get('config', {})
        config = Config(
            width=config_data.get('width', 900),    # Zwiększona domyślna szerokość
            height=config_data.get('height', 850),  # Zwiększona domyślna wysokość
            directed=config_data.get('directed', False),
            physics=config_data.get('physics', True),
            hierarchical=config_data.get('hierarchical', False),
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False
        )
        
        return agraph(nodes=nodes, edges=edges, config=config)
        
    except ImportError:
        st.error("Nie można załadować biblioteki streamlit-agraph. Zainstaluj ją używając: pip install streamlit-agraph")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia data-driven mapy myśli: {str(e)}")
        return None

def create_auto_generated_mind_map(lesson_data):
    """
    Automatycznie generuje mapę myśli TYLKO na podstawie sekcji "learning" z lekcji
    Używa tylko danych z lesson_data['sections']['learning']['sections']
    
    Args:
        lesson_data (dict): Dane lekcji w formacie JSON
    """
    try:
        from streamlit_agraph import agraph, Node, Edge, Config
        
        nodes = []
        edges = []
        
        # Informacja o źródle danych
        st.info("🧠 Ta mapa myśli została wygenerowana na podstawie sekcji nauki z lekcji. "
               "Pokazuje kluczowe koncepty z materiału edukacyjnego.")
        
        # Centralny węzeł z tytułem lekcji
        title = lesson_data.get('title', 'Lekcja')
        nodes.append(Node(id="central", 
                         label=f"📚 {title}", 
                         size=30,
                         color="#6C5CE7",
                         font={"size": 16, "color": "#6C5CE7"}))  # Kolor czcionki pasuje do węzła
        
        # Kolory dla sekcji nauki - różne odcienie i pełna paleta
        section_colors = [
            "#FF6B6B",  # Czerwony
            "#4ECDC4",  # Turkusowy
            "#45B7D1",  # Niebieski
            "#96CEB4",  # Miętowy
            "#FECA57",  # Żółty
            "#FD79A8",  # Różowy
            "#A29BFE",  # Fioletowy
            "#FDCB6E",  # Pomarańczowy
            "#74B9FF",  # Jasny niebieski
            "#E17055"   # Koralowy
        ]
        
        # Sprawdź czy mamy sekcję learning
        if ('sections' in lesson_data and 
            'learning' in lesson_data['sections'] and 
            'sections' in lesson_data['sections']['learning']):
            
            learning_sections = lesson_data['sections']['learning']['sections']
            
            # Dodaj każdą sekcję jako węzeł
            for i, section in enumerate(learning_sections):
                section_id = f"learning_section_{i}"
                section_title = section.get('title', f'Sekcja {i+1}')
                
                # Wyczyść emojis i skróć tytuł
                # Usuń emojis z początku tytułu dla lepszej czytelności
                import re
                clean_title = re.sub(r'^[^\w\s]+\s*', '', section_title)
                if len(clean_title) > 60:
                    clean_title = clean_title[:57] + "..."
                
                # Użyj koloru z palety (z cyklicznym powtarzaniem)
                color = section_colors[i % len(section_colors)]
                
                nodes.append(Node(id=section_id,
                                label=clean_title,
                                size=20,
                                color=color,
                                font={"size": 12, "color": color}))  # Kolor czcionki pasuje do węzła
                edges.append(Edge(source="central", target=section_id))
            
            # Dodaj informacje o liczbie sekcji jako dodatkowy węzeł
            info_node = Node(id="info",
                           label=f"📊 {len(learning_sections)} kluczowych tematów",
                           size=15,
                           color="#90EE90",
                           font={"size": 11, "color": "#90EE90"})
            nodes.append(info_node)
            edges.append(Edge(source="central", target="info"))
            
        else:
            # Jeśli nie ma sekcji learning, dodaj komunikat
            no_content_node = Node(id="no_content",
                                 label="❌ Brak sekcji nauki w tej lekcji",
                                 size=15,
                                 color="#FF6B6B",
                                 font={"size": 11, "color": "#FF6B6B"})
            nodes.append(no_content_node)
            edges.append(Edge(source="central", target="no_content"))
        
        # Konfiguracja z większym rozmiarem dla lepszej widoczności
        config = Config(width=900,   # Zwiększona szerokość jak w course_map
                       height=850,   # Zwiększona wysokość jak w course_map
                       directed=False,
                       physics=True,
                       hierarchical=False,
                       nodeHighlightBehavior=True,
                       highlightColor="#F7A7A6")
        
        return agraph(nodes=nodes, edges=edges, config=config)
        
    except ImportError:
        st.error("Nie można załadować biblioteki streamlit-agraph. Zainstaluj ją używając: pip install streamlit-agraph")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia mapy myśli: {str(e)}")
        return None
