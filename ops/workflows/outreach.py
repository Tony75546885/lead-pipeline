"""
Outreach & Follow-up Workflow — Notion CRM → Message Gen → Gmail → CRM Update

Claude generuje spersonalizowane cold emails i follow-upy,
tworzy drafty w Gmail, i aktualizuje status w Notion CRM.
"""

WORKFLOW = {
    "name": "Outreach & Follow-up",
    "steps": [
        {
            "step": 1,
            "name": "Pobierz leady do kontaktu",
            "mcp_tool": "mcp__notion__search",
            "logic": "Szukaj w CRM leadów z status='qualified' (do cold outreach) "
                     "i status='contacted' z last_contact > 3 dni (do follow-up)",
        },
        {
            "step": 2,
            "name": "Wygeneruj wiadomości",
            "logic": """
                Dla każdego leada:
                1. Sprawdź lokalizację → PL = po polsku, inne = po angielsku
                2. Użyj danych z enrichmentu do personalizacji
                3. Cold email: max 5 zdań, konkretne CTA
                4. Follow-up: max 3 zdania, nawiąż do poprzedniej wiadomości
                5. Dodaj nową wartość w follow-upie (case study, statystyka)
            """,
        },
        {
            "step": 3,
            "name": "Stwórz drafty w Gmail",
            "mcp_tool": "mcp__gmail__create_draft",
            "notes": """
                Stwórz draft (NIE wysyłaj od razu) dla każdego leada.
                Użytkownik musi zatwierdzić drafty przed wysłaniem.

                Format:
                - To: {lead.email}
                - Subject: spersonalizowany temat
                - Body: wygenerowana wiadomość + footer z unsubscribe
            """,
        },
        {
            "step": 4,
            "name": "Czekaj na zatwierdzenie",
            "logic": "Pokaż użytkownikowi listę draftów. Czekaj na 'ok'/'wyślij'/'popraw X'",
        },
        {
            "step": 5,
            "name": "Zaktualizuj CRM",
            "mcp_tool": "mcp__notion__update_page",
            "notes": """
                Po wysłaniu:
                - Status → 'contacted' (cold) lub zostawić 'contacted' (follow-up)
                - Last Contact → dzisiaj
                - Next Follow-up → za 3 dni (cold) lub za 7 dni (follow-up)
                - Notes → dodaj "Cold email sent" lub "Follow-up #N sent"
            """,
        },
    ],
}

COLD_EMAIL_PROMPT_PL = """Napisz cold email B2B po polsku.

Lead:
- Imię: {name}
- Stanowisko: {title}
- Firma: {company}
- Branża: {niche}
- Strona: {website}
- Technologie: {technologies}
- Wielkość firmy: {company_size}

Nadawca: {sender_name} z {sender_company}
Propozycja wartości: {value_proposition}

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

COLD_EMAIL_PROMPT_EN = """Write a B2B cold email in English.

Lead:
- Name: {name}
- Title: {title}
- Company: {company}
- Industry: {niche}
- Website: {website}
- Technologies: {technologies}
- Company size: {company_size}

Sender: {sender_name} from {sender_company}
Value proposition: {value_proposition}

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

FOLLOW_UP_PROMPT_PL = """Napisz follow-up do cold emaila po polsku.

Kontekst poprzedniej wiadomości:
{previous_email_summary}

Lead: {name}, {title} w {company}
Dni od ostatniego kontaktu: {days_since}
Numer follow-upu: {follow_up_number}/2

Zasady:
- Max 3 zdania
- Nawiąż do poprzedniej wiadomości (nie powtarzaj jej)
- Dodaj nową wartość (statystyka, case study, insight)
- Lekkie CTA
- Jeśli to follow-up #2, bądź bardziej bezpośredni

Format:
TEMAT: Re: <oryginalny temat>

<treść>
"""

MAX_FOLLOW_UPS = 2
FOLLOW_UP_INTERVALS_DAYS = [3, 7]
DAILY_EMAIL_LIMIT = 50
DELAY_BETWEEN_EMAILS_SEC = 8
