"""
CRM Sync Workflow — synchronizacja Gmail ↔ Calendar ↔ Notion CRM

Utrzymuje Notion CRM jako single source of truth.

Notion databases:
- Pipeline: collection://7b716879-9481-42a1-835e-9ebb8d893ace
- Kontakty: collection://41489d85-cc78-498a-affa-cea4450166a0
- Outreach: collection://31677235-f40e-4e24-8e82-147e44b8503e
"""

from .lead_gen import NOTION_IDS

WORKFLOW = {
    "name": "CRM Sync",
    "steps": [
        {
            "step": 1,
            "name": "Skanuj Gmail za odpowiedziami",
            "mcp_tool": "mcp__gmail__search_threads",
            "query": "is:unread newer_than:1d",
            "logic": """
                Dla każdego threada:
                1. Sprawdź czy nadawca jest w Kontakty (po Email)
                2. Jeśli tak:
                   - Pipeline: Etap → 'Replied'
                   - Outreach: Status → 'Odpisano'
                3. Sklasyfikuj odpowiedź:
                   - Pozytywna → Pipeline.Nastepny krok = 'Umówić spotkanie'
                   - Negatywna → Pipeline.Etap = 'Lost'
                   - Pytanie → Pipeline.Nastepny krok = 'Odpowiedzieć na pytanie'
                   - Bounce → Pipeline.Etap = 'Lost', Outreach.Status = 'Bounce'
            """,
        },
        {
            "step": 2,
            "name": "Sync spotkań z Calendar",
            "mcp_tool": "mcp__calendar__list_events",
            "logic": """
                Pobierz spotkania z ostatnich 7 dni + nadchodzące.
                Dla spotkań z leadami:
                - Pipeline: Etap → 'Meeting'
                - Dodaj notatkę o spotkaniu
            """,
        },
        {
            "step": 3,
            "name": "Sprawdź Zoom nagrania",
            "mcp_tool": "mcp__zoom__recordings_list",
            "logic": """
                Pobierz nagrania z ostatnich 7 dni.
                Powiąż z leadem → dodaj podsumowanie do Pipeline.Notatki
            """,
        },
        {
            "step": 4,
            "name": "Pipeline health check",
            "logic": """
                Policz leady per Etap:
                New | Qualifying | Contacted | Replied | Meeting | Negotiation | Won | Lost

                Alerty:
                - pipeline < 20 Qualifying/New → uruchom lead_gen
                - > 10 Contacted bez follow-up > 3 dni → uruchom follow_up
                - Replied bez akcji > 2 dni → pokaż alert
            """,
        },
    ],
}

GMAIL_REPLY_CLASSIFICATION = {
    "positive_signals": [
        "interested", "zainteresowany", "chętnie", "sounds good",
        "let's talk", "porozmawiajmy", "tell me more", "powiedzcie więcej",
        "when can we", "kiedy możemy", "send me", "wyślij mi",
        "sure", "jasne", "ok", "tak",
    ],
    "negative_signals": [
        "not interested", "nie jestem zainteresowany", "no thanks",
        "unsubscribe", "wypisz", "remove me", "stop",
        "nie teraz", "not now", "maybe later", "nie potrzebujemy",
    ],
    "bounce_signals": [
        "delivery failed", "undeliverable", "mailbox full",
        "out of office", "automatic reply", "auto-reply",
        "nie istnieje", "does not exist",
    ],
}
