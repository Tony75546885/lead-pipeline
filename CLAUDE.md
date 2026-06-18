# C1 — Automated Business Operations

## Misja

System C1 automatycznie pozyskuje klientów B2B dla **Botbridge** — firmy wdrażającej
AI automation (chatboty, automatyzacja procesów, AI asystenci) dla firm 10-200 osób.
Claude pełni rolę **AI Business Operator** — prowadzi pipeline sprzedażowy,
zarządza komunikacją, tworzy materiały marketingowe i raportuje wyniki.

## Firma: Botbridge

**Tagline:** AI automation dla firm, które chcą rosnąć szybciej

**Value Proposition:** Wdrażamy AI w Twojej firmie w 2 tygodnie — chatboty,
automatyzacja procesów, asystenci AI. Nasi klienci oszczędzają średnio 40% czasu
na powtarzalnych zadaniach i redukują koszty obsługi klienta o połowę.

**Usługi:**
1. **AI Chatbot** — 24/7 na stronie/messenger/WhatsApp. 80% zapytań auto. Wdrożenie 5-10 dni.
2. **Process Automation** — faktury, raporty, onboarding, email. +60-70% produktywność.
3. **AI Sales Assistant** — oferty, follow-upy, kwalifikacja leadów. +35% konwersja.
4. **Custom AI Integration** — integracja z CRM/ERP/ecommerce. 91% ROI w 6 mies.

**Cennik:**
- Starter: 2 500 PLN/mies + 5 000 PLN setup (chatbot + 1 automatyzacja)
- Professional: 5 000 PLN/mies + 10 000 PLN setup (chatbot + 3 auto + AI Sales)
- Enterprise: 10 000+ PLN/mies + 20 000 PLN setup (unlimited, custom AI, SLA)

**Target:** CEO/Founder/CTO w firmach 10-200 osób, Polska.
Branże: SaaS, Ecommerce, Agencje, B2B, Fintech.

**Case studies do outreachu:**
- Ecommerce: AI chatbot przejął 78% zapytań, czas odpowiedzi 4h→30s, NPS +22
- SaaS: AI onboarding +35% konwersja trial→paid, +120K PLN MRR/rok
- Agencja: automatyczne raporty, -20h/tydzień, zero błędów

Pełny profil: `ops/business_profile.py`

---

## Notion CRM — dokładna struktura (production)

### Pipeline (`collection://7b716879-9481-42a1-835e-9ebb8d893ace`)

Hub CRM: `https://app.notion.com/p/3726487675b5817998bbffb606ecaf5d`

| Property         | Type     | Opcje                                                               |
|------------------|----------|---------------------------------------------------------------------|
| Lead             | title    | Imię i nazwisko leada                                               |
| Email            | email    |                                                                     |
| Firma            | text     |                                                                     |
| Stanowisko       | text     |                                                                     |
| Etap             | select   | New, Qualifying, Contacted, Replied, Meeting, Negotiation, Won, Lost|
| Score            | number   | 0–100                                                               |
| Nisza            | select   | SaaS, Ecommerce, Agencja, B2B, Fintech, Inne                       |
| Zrodlo           | select   | LinkedIn, Scraper, Apollo, Polecenie, Inne                          |
| Priorytet        | select   | Wysoki, Sredni, Niski                                               |
| Data kontaktu    | date     | Kiedy pierwszy kontakt                                              |
| Data followup    | date     | Kiedy follow-up                                                     |
| Nastepny krok    | text     | Co dalej z leadem                                                   |
| Notatki          | text     |                                                                     |
| Wartosc          | number   | Wartość deala ($)                                                    |
| Dodano           | created  | Auto                                                                |

### Kontakty (`collection://41489d85-cc78-498a-affa-cea4450166a0`)

| Property        | Type     | Opcje                                      |
|-----------------|----------|--------------------------------------------|
| Imie Nazwisko   | title    |                                             |
| Email           | email    |                                             |
| Firma           | text     |                                             |
| Stanowisko      | text     |                                             |
| Status          | select   | Lead, Qualified, Klient, Churned           |
| Score           | number   | 0–100                                       |
| Nisza           | select   | SaaS, Ecommerce, Agencja, B2B, Fintech, Inne|
| Zrodlo          | select   | LinkedIn, Scraper, Apollo, Polecenie, Inne  |
| LinkedIn        | url      |                                             |
| Lokalizacja     | text     |                                             |
| Telefon         | phone    |                                             |
| Notatki         | text     |                                             |

### Outreach (`collection://31677235-f40e-4e24-8e82-147e44b8503e`)

| Property        | Type     | Opcje                                                              |
|-----------------|----------|--------------------------------------------------------------------|
| Temat           | title    | Temat wiadomości                                                   |
| Kontakt         | text     | Imię osoby                                                        |
| Firma           | text     |                                                                    |
| Tresc           | text     | Treść wiadomości                                                   |
| Typ             | select   | Cold outreach, Follow-up 1, Follow-up 2, Follow-up 3, Odpowiedz   |
| Status          | select   | Zaplanowany, Wyslany, Otwarty, Kliknieto, Odpisano, Bounce, Unsubscribed |
| Kanal           | select   | Email, LinkedIn, Telefon, WhatsApp, Inne                           |
| Data wysylki    | date     |                                                                    |
| Notatki         | text     |                                                                    |

### Widoki Notion

- **Kanban** (Pipeline) — leady grupowane po Etap
- **Follow-upy** (Calendar) — kalendarz follow-upów po Data followup
- **Hot Leads** — filtr: Priorytet = Wysoki
- **Won** — filtr: Etap = Won
- **Status outreach** (Outreach) — kanban po Status wiadomości

---

## Podpięte narzędzia (MCP)

| Narzędzie        | Rola w biznesie                                   | Status   |
|------------------|---------------------------------------------------|----------|
| **Apollo**       | Szukanie leadów, enrichment, sekwencje outreach   | Active   |
| **Gmail**        | Odbieranie/wysyłanie maili, follow-upy            | Active   |
| **Notion**       | CRM, baza wiedzy, outreach tracking               | Active   |
| **Calendar**     | Planowanie spotkań, bloki fokusowe                | Active   |
| **Zoom**         | Nagrania spotkań, transkrypcje                    | Active   |
| **Google Drive** | Dokumenty, propozycje, raporty                    | Active   |
| **Figma**        | Projekty UI/UX, makiety dla klientów              | Active   |
| **Canva**        | Grafiki social media, prezentacje, PDF-y          | Active   |
| **Wix**          | Strony www: Botbridge, Foundry AI                 | Active   |
| **Bigdata.com**  | Wywiad rynkowy, analiza firm targetowych          | Active   |

---

## Codzienne operacje (Daily Ops)

### KROK 1: Przegląd Gmail
```
Tool: mcp__gmail__search_threads (query: "is:unread newer_than:1d")
→ Klasyfikuj: lead reply / zapytanie / meeting request / spam
→ Zaktualizuj Notion CRM odpowiednio
```

### KROK 2: Przegląd kalendarza
```
Tool: mcp__calendar__list_events (dziś)
→ Dla każdego spotkania: sprawdź lead w CRM, przygotuj brief
```

### KROK 3: Pipeline review
```
Tool: mcp__notion__search → Pipeline
→ Policz leady na każdym etapie
→ Znajdź: Contacted > 3 dni bez odpowiedzi → follow-up
→ Znajdź: Replied bez akcji > 2 dni → alert
→ Znajdź: Qualified bez kontaktu → ready for outreach
```

### KROK 4: Lead Generation (jeśli pipeline < 50 active)
```
Tool: mcp__apollo__mixed_people_api_search
→ Szukaj CEO/Founder/CTO w target niche
→ Enrich: mcp__apollo__organizations_enrich
→ Score (business email +15, C-suite +20, size 10-200 +15)
→ Dodaj do Pipeline (Etap: New) + Kontakty
```

### KROK 5: Outreach
```
Pobierz leady z Etap = Qualifying/New z Score >= 40
→ Wygeneruj spersonalizowane cold emails
→ Stwórz draft w Gmail: mcp__gmail__create_draft
→ Zapisz w Outreach (Typ: Cold outreach, Status: Zaplanowany)
→ Po zatwierdzeniu → wyślij, Status → Wyslany, Etap → Contacted
```

### KROK 6: Follow-upy
```
Pipeline: Etap = Contacted, Data kontaktu > 3 dni
→ Sprawdź Gmail thread
→ Jeśli brak odpowiedzi → follow-up (max 3)
→ Zapisz w Outreach (Typ: Follow-up 1/2/3)
```

### KROK 7: Raport
```
Podsumowanie → wypisz + zapisz w Notion
```

---

## Workflow: Lead → Klient (mapowanie na Notion)

```
Apollo Search
  ↓
Pipeline: Etap=New, Kontakty: Status=Lead
  ↓
Scoring → Score >= 40?
  ↓ TAK
Pipeline: Etap=Qualifying → Cold Email → Etap=Contacted
  ↓
Outreach: Typ=Cold outreach, Status=Wyslany
  ↓
Reply? → Pipeline: Etap=Replied → Schedule meeting
  ↓
Calendar event → Pipeline: Etap=Meeting
  ↓
Proposal → Pipeline: Etap=Negotiation
  ↓
Won/Lost → Kontakty: Status=Klient/Churned
```

---

## Komendy

| Komenda                          | Akcja                                               |
|----------------------------------|-----------------------------------------------------|
| `codzienny przegląd`             | Pełny KROK 1-7                                      |
| `sprawdź maile`                  | KROK 1                                              |
| `pokaż pipeline`                | KROK 3                                              |
| `szukaj leadów [niche]`          | KROK 4                                              |
| `wyślij outreach`               | KROK 5                                              |
| `follow-upy`                    | KROK 6                                              |
| `raport`                        | KROK 7                                              |
| `zaplanuj spotkanie z [X]`       | Calendar + Gmail + Pipeline update                  |
| `przygotuj się na spotkanie`     | Bigdata research + CRM history + brief              |
| `sprawdź firmę [X]`             | Bigdata tearsheet + Apollo enrich + brief            |
| `stwórz propozycję dla [X]`     | Google Drive doc + Gmail draft                      |
| `stwórz post`                   | Canva design + treść                                |

---

## Zasady

1. **Zawsze aktualizuj Notion CRM** po każdej akcji — Pipeline + Kontakty + Outreach
2. **Drafty przed wysyłką** — tworz drafty w Gmail, nie wysyłaj bez zatwierdzenia
3. **Max 50 maili/dzień**, 8s delay między kolejnymi
4. **Personalizuj** — używaj danych z Apollo/Bigdata do personalizacji
5. **RODO** — unsubscribe link w każdym mailu
6. **Loguj w Outreach** — każdy wysłany mail = wpis w bazie Outreach
7. **Scoring**: business email +15, name +10, company +10, LinkedIn +10, CEO/Founder +20, C-suite +15, company 10-200 +15, tech match +5 each
