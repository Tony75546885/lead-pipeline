"""
CRM Sync Workflow — synchronizacja stanu między Gmail, Calendar, i Notion CRM

Utrzymuje Notion CRM jako single source of truth.
"""

WORKFLOW = {
    "name": "CRM Sync",
    "trigger": "Część daily_review lub na żądanie",
    "steps": [
        {
            "step": 1,
            "name": "Skanuj Gmail za odpowiedziami",
            "mcp_tool": "mcp__gmail__search_threads",
            "logic": """
                Szukaj wiadomości: 'in:inbox is:unread'
                Dla każdego threadsa:
                1. Sprawdź czy nadawca jest w Notion CRM
                2. Jeśli tak → zaktualizuj status na 'replied'
                3. Oznacz jako przeczytany
                4. Sklasyfikuj odpowiedź:
                   - Pozytywna (zainteresowany) → status 'replied', notatka
                   - Negatywna (nie teraz) → status 'lost', notatka
                   - Pytanie → status 'replied', notatka z pytaniem
                   - Bounce/OOO → status 'bounced'
            """,
        },
        {
            "step": 2,
            "name": "Sync spotkań z Calendar",
            "mcp_tool": "mcp__calendar__list_events",
            "logic": """
                Pobierz spotkania z ostatnich 7 dni i nadchodzące.
                Dla każdego spotkania:
                1. Sprawdź czy uczestnik jest w CRM
                2. Jeśli tak → zaktualizuj status na 'meeting_scheduled'
                3. Dodaj notatkę ze spotkania jeśli już się odbyło
            """,
        },
        {
            "step": 3,
            "name": "Sprawdź Zoom za nagraniami",
            "mcp_tool": "mcp__zoom__recordings_list",
            "logic": """
                Pobierz nagrania z ostatnich 7 dni.
                Dla każdego nagrania:
                1. Powiąż z leadem w CRM
                2. Pobierz transkrypcję jeśli dostępna
                3. Dodaj podsumowanie do notatek w Notion
            """,
        },
        {
            "step": 4,
            "name": "Pipeline health check",
            "logic": """
                Policz leady na każdym etapie:
                - new, qualified, contacted, replied, meeting_scheduled,
                  proposal_sent, converted, lost

                Flagi:
                - Jeśli < 20 qualified → uruchom lead_gen
                - Jeśli > 10 contacted bez follow-up > 3 dni → uruchom follow_up
                - Jeśli replied bez akcji > 2 dni → alert
            """,
        },
    ],
}

GMAIL_REPLY_CLASSIFICATION = {
    "positive_signals": [
        "interested", "zainteresowany", "chętnie", "sounds good",
        "let's talk", "porozmawiajmy", "tell me more", "powiedzcie więcej",
        "when can we", "kiedy możemy", "send me", "wyślij mi",
    ],
    "negative_signals": [
        "not interested", "nie jestem zainteresowany", "no thanks",
        "unsubscribe", "wypisz", "remove me", "stop",
        "nie teraz", "not now", "maybe later",
    ],
    "bounce_signals": [
        "delivery failed", "undeliverable", "mailbox full",
        "out of office", "automatic reply", "auto-reply",
    ],
}
