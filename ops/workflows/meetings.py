"""
Meetings Workflow — Calendar + Zoom + Notion

Automatyzuje przygotowanie do spotkań, tworzenie notatek,
i follow-up po spotkaniach.
"""

WORKFLOW = {
    "name": "Meeting Management",
    "sub_workflows": {
        "schedule_meeting": {
            "trigger": "Lead odpowiedział pozytywnie / użytkownik mówi 'zaplanuj spotkanie'",
            "steps": [
                {
                    "step": 1,
                    "name": "Znajdź wolny slot",
                    "mcp_tool": "mcp__calendar__suggest_time",
                    "notes": "Sugeruj 2-3 sloty w najbliższych 3 dniach roboczych",
                },
                {
                    "step": 2,
                    "name": "Stwórz event",
                    "mcp_tool": "mcp__calendar__create_event",
                    "params_template": {
                        "summary": "C1 Discovery Call — {company}",
                        "description": "Spotkanie z {name} ({title}) z {company}\n\nAgenda:\n1. Poznanie potrzeb\n2. Prezentacja rozwiązania\n3. Dalsze kroki",
                        "duration_minutes": 30,
                    },
                },
                {
                    "step": 3,
                    "name": "Wyślij potwierdzenie",
                    "mcp_tool": "mcp__gmail__create_draft",
                    "notes": "Wyślij email z potwierdzeniem i linkiem do spotkania",
                },
                {
                    "step": 4,
                    "name": "Zaktualizuj CRM",
                    "mcp_tool": "mcp__notion__update_page",
                    "notes": "Status → 'meeting_scheduled', dodaj datę spotkania",
                },
            ],
        },
        "prep_meeting": {
            "trigger": "Spotkanie za < 2h",
            "steps": [
                {
                    "step": 1,
                    "name": "Research firmy",
                    "mcp_tool": "mcp__bigdata__company_tearsheet",
                    "notes": "Pobierz dane o firmie: przychody, zatrudnienie, ostatnie newsy",
                },
                {
                    "step": 2,
                    "name": "Sprawdź historię w CRM",
                    "mcp_tool": "mcp__notion__search",
                    "notes": "Pobierz wszystkie notatki i interakcje z tym leadem",
                },
                {
                    "step": 3,
                    "name": "Stwórz brief",
                    "output": """
                        Meeting Brief:
                        - Firma: {company} — {opis}
                        - Osoba: {name}, {title}
                        - Historia: {interakcje}
                        - Potencjalne pain points: {analiza}
                        - Pytania do zadania: {lista}
                        - Propozycja wartości dopasowana: {wartość}
                    """,
                },
            ],
        },
        "post_meeting": {
            "trigger": "Po zakończonym spotkaniu",
            "steps": [
                {
                    "step": 1,
                    "name": "Pobierz nagranie",
                    "mcp_tool": "mcp__zoom__get_recording_resource",
                    "notes": "Pobierz transkrypcję jeśli dostępna",
                },
                {
                    "step": 2,
                    "name": "Stwórz notatki",
                    "mcp_tool": "mcp__notion__create_pages",
                    "notes": """
                        Stwórz stronę 'Meeting Notes — {company} — {date}':
                        - Uczestnicy
                        - Kluczowe ustalenia
                        - Potrzeby klienta
                        - Dalsze kroki
                        - Termin follow-upu
                    """,
                },
                {
                    "step": 3,
                    "name": "Wyślij follow-up email",
                    "mcp_tool": "mcp__gmail__create_draft",
                    "notes": "Podziękowanie + podsumowanie ustaleń + dalsze kroki",
                },
                {
                    "step": 4,
                    "name": "Zaktualizuj CRM",
                    "mcp_tool": "mcp__notion__update_page",
                    "notes": "Dodaj notatki, ustaw next follow-up, zmień status jeśli trzeba",
                },
            ],
        },
    },
}
