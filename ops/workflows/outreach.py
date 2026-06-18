"""
Outreach & Follow-up Workflow — Notion CRM → Message Gen → Gmail → CRM Update

Maps to real Notion CRM:
- Pipeline: collection://7b716879-9481-42a1-835e-9ebb8d893ace
- Outreach: collection://31677235-f40e-4e24-8e82-147e44b8503e
"""

from .lead_gen import NOTION_IDS

WORKFLOW = {
    "name": "Outreach & Follow-up",
    "steps": [
        {
            "step": 1,
            "name": "Pobierz leady do kontaktu",
            "mcp_tool": "mcp__notion__search",
            "logic": """
                Z Pipeline:
                - Cold outreach: Etap='New' lub 'Qualifying', Score >= 40
                - Follow-up: Etap='Contacted', Data kontaktu > 3 dni temu
            """,
        },
        {
            "step": 2,
            "name": "Wygeneruj wiadomości",
            "logic": """
                Dla każdego leada:
                1. Sprawdź Lokalizacja → PL = po polsku, inne = po angielsku
                2. Użyj danych z Pipeline (Firma, Stanowisko, Nisza) do personalizacji
                3. Cold: max 5 zdań, konkretne CTA
                4. Follow-up: max 3 zdania, nawiąż do poprzedniego maila
            """,
        },
        {
            "step": 3,
            "name": "Stwórz drafty w Gmail",
            "mcp_tool": "mcp__gmail__create_draft",
            "notes": "Stwórz DRAFT, NIE wysyłaj. Użytkownik zatwierdza.",
        },
        {
            "step": 4,
            "name": "Zapisz w Outreach",
            "mcp_tool": "mcp__notion__create_pages",
            "params_mapping": {
                "database_id": NOTION_IDS["outreach_db"],
                "properties": {
                    "Temat": "{subject}",
                    "Kontakt": "{lead_name}",
                    "Firma": "{company}",
                    "Tresc": "{email_body}",
                    "Typ": "Cold outreach | Follow-up 1 | Follow-up 2 | Follow-up 3",
                    "Status": "Zaplanowany",
                    "Kanal": "Email",
                    "Data wysylki": "{today}",
                },
            },
        },
        {
            "step": 5,
            "name": "Po zatwierdzeniu — update CRM",
            "updates": {
                "pipeline": {
                    "Etap": "Contacted",
                    "Data kontaktu": "{today}",
                    "Data followup": "{today + 3 days}",
                    "Nastepny krok": "Czekaj na odpowiedź, follow-up za 3 dni",
                },
                "outreach": {
                    "Status": "Wyslany",
                },
            },
        },
    ],
}

COLD_EMAIL_PROMPT_PL = """Napisz cold email B2B po polsku dla firmy IT/Software.

Lead:
- Imię: {name}
- Stanowisko: {title}
- Firma: {company}
- Branża: {niche}
- Strona: {website}
- Technologie: {technologies}
- Wielkość firmy: {company_size}

Zasady:
- Max 5 zdań
- Zacznij od spersonalizowanego nawiązania do firmy lub roli
- Jasna propozycja wartości (efekt, nie produkt)
- Konkretne CTA (zaproponuj 15-minutową rozmowę)
- Zero corporate speak
- Ton: bezpośredni, pewny siebie, profesjonalny

Format:
TEMAT: <temat>

<treść>
"""

COLD_EMAIL_PROMPT_EN = """Write a B2B cold email in English for an IT/Software company.

Lead:
- Name: {name}
- Title: {title}
- Company: {company}
- Industry: {niche}
- Website: {website}
- Technologies: {technologies}
- Company size: {company_size}

Rules:
- Max 5 sentences
- Start with personalized reference to their company or role
- Clear value proposition (outcome, not product)
- Specific CTA (suggest a 15-minute call)
- No corporate speak
- Tone: direct, confident, professional

Format:
SUBJECT: <subject>

<body>
"""

FOLLOW_UP_RULES = {
    "max_follow_ups": 3,
    "intervals_days": [3, 5, 7],
    "daily_email_limit": 50,
    "delay_between_emails_sec": 8,
    "notion_typ_mapping": {
        1: "Follow-up 1",
        2: "Follow-up 2",
        3: "Follow-up 3",
    },
}
