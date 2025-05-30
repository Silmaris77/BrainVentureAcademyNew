# Standalone badge configuration for testing
# This file doesn't import streamlit to avoid hanging in test scripts

BADGES = {
    # Podstawowe odznaki neuroleaderskie
    "starter": {"name": "Nowy Lider", "icon": "🌱", "description": "Rozpocznij swoją podróż w BrainVenture Academy neuroleaderstwa"},
    "tester": {"name": "Odkrywca Profilu", "icon": "🔍", "description": "Wykonaj test i odkryj swój typ neuroleadera"},
    "learner": {"name": "Student Przywództwa", "icon": "📚", "description": "Ukończ pierwszą lekcję z neuroleaderstwa"},
    "consistent": {"name": "Systematyczny Lider", "icon": "📆", "description": "Rozwijaj się systematycznie - zaloguj się 5 dni z rzędu"},
    "social": {"name": "Lider Społeczności", "icon": "🤝", "description": "Podziel się swoim profilem neuroleaderskim z zespołem"},
    
    # Odznaki specjalistyczne neuroleaderstwa
    "emotional_intelligence": {"name": "Mistrz EQ", "icon": "❤️", "description": "Ukończ wszystkie lekcje z inteligencji emocjonalnej"},
    "decision_maker": {"name": "Strateg Decyzji", "icon": "⚖️", "description": "Ukończ wszystkie lekcje o procesach decyzyjnych"},
    "team_builder": {"name": "Architekt Zespołów", "icon": "👥", "description": "Ukończ wszystkie lekcje o budowaniu zespołów"},
    "change_leader": {"name": "Agent Zmian", "icon": "🔄", "description": "Ukończ wszystkie lekcje o zarządzaniu zmianą"},
    "communication_expert": {"name": "Mistrz Komunikacji", "icon": "💬", "description": "Ukończ wszystkie lekcje o komunikacji przywódczej"},
    
    # Odznaki związane z aktywnością rozwoju
    "streak_master": {"name": "Konsekwentny w Rozwoju", "icon": "🔥", "description": "Utrzymaj 10-dniową serię nauki neuroleaderstwa"},
    "daily_hero": {"name": "Lider Dnia", "icon": "⭐", "description": "Ukończ wszystkie dzienne zadania rozwojowe"},
    "weekend_warrior": {"name": "Weekend z Rozwojem", "icon": "🏆", "description": "Ucz się neuroleaderstwa regularnie przez 4 weekendy"},
    
    # Odznaki związane z głębią nauki
    "knowledge_seeker": {"name": "Poszukiwacz Wiedzy", "icon": "🧠", "description": "Spędź łącznie 10 godzin na nauce neuroleaderstwa"},
    "quick_learner": {"name": "Efektywny Uczeń", "icon": "⚡", "description": "Ukończ 3 lekcje neuroleaderstwa w jeden dzień"},
    "night_owl": {"name": "Nocny Strateg", "icon": "🦉", "description": "Ukończ lekcję po godzinie 22:00"},
    "early_bird": {"name": "Poranny Lider", "icon": "🐦", "description": "Rozpocznij dzień nauką przed godziną 8:00"},
    
    # Odznaki mentoringu i rozwoju innych
    "mentor": {"name": "Mentor Przywództwa", "icon": "👨‍🏫", "description": "Pomóż innemu liderowi w rozwoju neuroleaderskim"},
    "coach": {"name": "Coach Biznesowy", "icon": "🏋️‍♂️", "description": "Poprowadź sesję coachingową z wykorzystaniem neuroleaderstwa"},
    "team_developer": {"name": "Rozwija Zespoły", "icon": "🌐", "description": "Zastosuj wiedzę neuroleaderską w rozwoju 3 osób z zespołu"},
    "culture_builder": {"name": "Budowniczy Kultury", "icon": "🏛️", "description": "Wpłyń na kulturę organizacyjną poprzez neuroleaderstwo"},
    
    # Odznaki osiągnięć i doskonalenia
    "first_achievement": {"name": "Pierwszy Sukces", "icon": "🏁", "description": "Osiągnij pierwszy cel rozwojowy w neuroleaderstwie"},
    "collector": {"name": "Kolekcjoner Kompetencji", "icon": "🧩", "description": "Rozwiń 10 różnych kompetencji przywódczych"},
    "perfectionist": {"name": "Ekspert Neuroleader", "icon": "💯", "description": "Uzyskaj 100% w teście z neuroleaderstwa"},
    "innovator": {"name": "Innowator Przywództwa", "icon": "💡", "description": "Zaproponuj nowe rozwiązanie wykorzystujące neuroleaderstwo"},
    
    # Odznaki typów neuroleaderów
    "neuroleader_master": {"name": "Mistrz Neuroleaderów", "icon": "👑", "description": "Poznaj wszystkie typy neuroleaderów w eksploratorze"},
    "self_aware": {"name": "Samoświadomy Lider", "icon": "🔮", "description": "Wykonaj ponownie test i pogłęb samoświadomość"},
    "adaptive_leader": {"name": "Elastyczny Lider", "icon": "🦋", "description": "Rozwiń umiejętności poza swój dominujący typ neuroleadera"},
    "authentic_leader": {"name": "Autentyczny Lider", "icon": "🎭", "description": "Buduj autentyczne relacje przywódcze"},
    
    # Odznaki zastosowania w praktyce
    "practitioner": {"name": "Praktyk Neuroleaderstwa", "icon": "⚙️", "description": "Zastosuj narzędzia neuroleaderskie w 5 sytuacjach biznesowych"},
    "results_driven": {"name": "Lider Rezultatów", "icon": "📈", "description": "Osiągnij mierzalne wyniki dzięki neuroleaderstwu"},
    "feedback_master": {"name": "Mistrz Feedbacku", "icon": "🎯", "description": "Prowadź efektywne rozmowy zwrotne z zespołem"},
    
    # Odznaki wyzwań przywódczych
    "challenge_accepted": {"name": "Przyjmuję Wyzwanie", "icon": "🚀", "description": "Podejmij pierwsze wyzwanie przywódcze"},
    "challenge_master": {"name": "Mistrz Wyzwań", "icon": "🏅", "description": "Ukończ 5 wyzwań rozwoju przywódczego"},
    "transformation_leader": {"name": "Lider Transformacji", "icon": "🌟", "description": "Poprowadź znaczącą zmianę w organizacji"},
    
    # Odznaki specjalne
    "visionary": {"name": "Wizjoner", "icon": "🔭", "description": "Stwórz inspirującą wizję dla zespołu"},
    "empathy_champion": {"name": "Mistrz Empatii", "icon": "💝", "description": "Wykaż się wyjątkową empatią przywódczą"},
    "resilient_leader": {"name": "Odporny Lider", "icon": "🛡️", "description": "Przejdź przez trudny okres dzięki resilience"},
    "mindful_leader": {"name": "Uważny Lider", "icon": "🧘‍♂️", "description": "Praktykuj mindfulness w codziennym przywództwie"}
}
