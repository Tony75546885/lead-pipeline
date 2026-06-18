"""
C1 Daily Operations — instrukcje dla Claude Code

Ten plik definiuje DOKŁADNE kroki, które Claude powinien wykonać
przy każdej sesji jako "AI Business Operator".

Użycie: Claude czyta ten plik i wykonuje kolejne kroki używając MCP tools.
"""

DAILY_OPS_PROMPT = """
# Codzienny przegląd operacyjny C1

Wykonaj następujące kroki po kolei. Po każdym kroku wypisz krótkie podsumowanie.

---

## KROK 1: Sprawdź skrzynkę Gmail

Użyj `mcp__gmail__search_threads` z query "is:unread newer_than:1d"

Sklasyfikuj każdy mail:
- **Lead reply** → Zaktualizuj status w Notion CRM na "replied"
- **Nowy zapytanie** → Dodaj do Notion CRM jako nowy lead
- **Meeting request** → Zaplanuj w Calendar
- **Spam/nieistotne** → Pomiń

---

## KROK 2: Sprawdź kalendarz

Użyj `mcp__calendar__list_events` na dziś.

Dla każdego spotkania:
- Sprawdź uczestników w Notion CRM
- Przygotuj 3-zdaniowy brief o firmie (Bigdata.com jeśli potrzeba)
- Zanotuj w Notion czego dotyczy spotkanie

---

## KROK 3: Pipeline review

Użyj `mcp__notion__search` żeby sprawdzić:
- Leady z status="contacted" starsze niż 3 dni → potrzebują follow-up
- Leady z status="replied" → potrzebują akcji (spotkanie/propozycja)
- Leady z status="qualified" bez kontaktu → gotowe do outreach

Podsumuj: ile leadów na jakim etapie.

---

## KROK 4: Lead Generation (jeśli pipeline < 50 aktywnych leadów)

Użyj `mcp__apollo__mixed_people_api_search` z kryteriami:
- Tytuły: CEO, Founder, Head of Marketing, CMO
- Lokalizacja: Poland (lub z config)
- Branża: z config.yaml default_niche

Dla znalezionych leadów:
- Enrichuj przez `mcp__apollo__organizations_enrich`
- Scoruj (business email +15, C-suite +20, company size 10-200 +15)
- Leadów z score >= 40 dodaj do Notion CRM

---

## KROK 5: Outreach

Dla leadów z status="qualified" w Notion:
- Wygeneruj spersonalizowany cold email (po polsku dla PL, po angielsku dla reszty)
- Stwórz draft w Gmail (`mcp__gmail__create_draft`)
- Pokaż użytkownikowi drafty do zatwierdzenia
- Po zatwierdzeniu: oznacz w Notion jako "contacted"

---

## KROK 6: Follow-upy

Dla leadów kontaktowanych 3+ dni temu bez odpowiedzi:
- Sprawdź Gmail thread czy nie odpowiedzieli
- Jeśli brak odpowiedzi → wygeneruj follow-up
- Stwórz draft follow-up w Gmail
- Maksymalnie 2 follow-upy na leada

---

## KROK 7: Raport

Wypisz podsumowanie dnia:
```
Pipeline:
  Nowych leadów     : X
  Zakwalifikowanych : X
  Skontaktowanych   : X
  Odpowiedzi        : X
  Spotkań dziś      : X
  Follow-upów       : X

Akcje wykonane:
  - [lista]

Do zrobienia jutro:
  - [lista]
```

Zapisz raport w Notion.
"""

LEAD_SCORING_RULES = """
Scoring rules (0-100):
- Business email (nie gmail/yahoo): +15
- Imię i nazwisko obecne: +10
- Firma znana: +10
- LinkedIn URL: +10
- CEO/Founder/Owner: +20
- CTO/CMO/Director/VP: +15
- Manager/Lead: +8
- Firma 10-200 osób: +15
- Firma 200+: +8
- Technologie (shopify, stripe, hubspot, salesforce): +5 za każdą
"""

OUTREACH_TEMPLATES = {
    "cold_pl": {
        "rules": [
            "Max 5 zdań",
            "Zacznij od spersonalizowanego nawiązania do firmy",
            "Jasna propozycja wartości (efekt, nie produkt)",
            "Konkretne CTA (zaproponuj termin spotkania)",
            "Zero corporate speak",
            "Ton: bezpośredni, pewny siebie, profesjonalny",
        ],
        "example_subject": "Pytanie o [aspekt firmy]",
    },
    "cold_en": {
        "rules": [
            "Max 5 sentences",
            "Start with personalized reference to their company",
            "Clear value proposition (outcome, not product)",
            "Specific CTA (suggest a meeting time)",
            "No corporate speak",
            "Tone: direct, confident, professional",
        ],
        "example_subject": "Quick question about [company aspect]",
    },
    "follow_up_pl": {
        "rules": [
            "Max 3 zdania",
            "Nawiąż do poprzedniej wiadomości",
            "Dodaj nową wartość (case study, statystyka)",
            "Lekkie CTA",
        ],
    },
    "follow_up_en": {
        "rules": [
            "Max 3 sentences",
            "Reference previous email",
            "Add new value (case study, stat)",
            "Soft CTA",
        ],
    },
}

NOTION_CRM_SCHEMA = {
    "database_name": "C1 CRM",
    "properties": {
        "Name": "title",
        "Email": "email",
        "Company": "rich_text",
        "Title": "rich_text",
        "Status": {
            "type": "select",
            "options": [
                "new", "qualified", "contacted",
                "replied", "meeting_scheduled",
                "proposal_sent", "converted", "lost",
            ],
        },
        "Score": "number",
        "Source": "select",
        "Niche": "select",
        "Last Contact": "date",
        "Next Follow-up": "date",
        "Notes": "rich_text",
        "LinkedIn": "url",
        "Website": "url",
    },
}
