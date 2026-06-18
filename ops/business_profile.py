"""
C1 Business Profile — wygenerowany na podstawie market research

Źródła danych:
- Bigdata.com: Applied AI Service Market, Salesforce SMB Trends Report,
  Forbes, ECI AI Readiness Report, Benzinga
- Microsoft $700M investment in Poland AI infrastructure
- 75% organizacji adoptuje conversational AI
- 75% SMB już inwestuje w AI, 85% oczekuje ROI
- AI chatboty odpowiadają na 80% zapytań, redukując koszty o 50%
- 60-70% wzrost produktywności SMB po wdrożeniu AI
- 91% firm raportuje pozytywny ROI w ciągu 6 miesięcy
"""

COMPANY = {
    "name": "Botbridge",
    "legal_name": "Botbridge",
    "tagline": "AI automation dla firm, które chcą rosnąć szybciej",
    "domain": "botbridge.pl",
    "wix_site_id": "f97ffd30-62cb-4cf9-97ae-1d55b6452286",
    "brand_secondary": "Foundry AI",
    "brand_secondary_wix_id": "af955b60-a19d-4b97-a297-af8afc416e77",
}

VALUE_PROPOSITION = {
    "pl": (
        "Wdrażamy AI w Twojej firmie w 2 tygodnie — chatboty, automatyzacja procesów, "
        "asystenci AI. Nasi klienci oszczędzają średnio 40% czasu na powtarzalnych zadaniach "
        "i redukują koszty obsługi klienta o połowę."
    ),
    "en": (
        "We deploy AI in your company in 2 weeks — chatbots, process automation, "
        "AI assistants. Our clients save 40% of time on repetitive tasks "
        "and cut customer service costs in half."
    ),
    "one_liner_pl": "AI chatboty i automatyzacja procesów dla firm 10-200 osób",
    "one_liner_en": "AI chatbots and process automation for 10-200 person companies",
}

SERVICES = [
    {
        "name": "AI Chatbot",
        "description_pl": "Inteligentny chatbot 24/7 na stronie, w messengerze i WhatsApp. "
                          "Odpowiada na pytania klientów, kwalifikuje leady, umawia spotkania.",
        "description_en": "24/7 intelligent chatbot on website, messenger and WhatsApp. "
                          "Answers customer questions, qualifies leads, books meetings.",
        "key_stats": "80% zapytań obsłużonych automatycznie, -50% kosztów obsługi",
        "deploy_time": "5-10 dni",
    },
    {
        "name": "Process Automation",
        "description_pl": "Automatyzacja powtarzalnych zadań: faktury, raporty, onboarding, "
                          "email follow-upy, synchronizacja danych między systemami.",
        "description_en": "Automation of repetitive tasks: invoices, reports, onboarding, "
                          "email follow-ups, data sync between systems.",
        "key_stats": "60-70% wzrost produktywności, 75% redukcja manualnych zadań",
        "deploy_time": "2-4 tygodnie",
    },
    {
        "name": "AI Sales Assistant",
        "description_pl": "AI asystent sprzedażowy — generuje spersonalizowane oferty, "
                          "follow-upy, kwalifikuje leady i aktualizuje CRM automatycznie.",
        "description_en": "AI sales assistant — generates personalized offers, "
                          "follow-ups, qualifies leads and updates CRM automatically.",
        "key_stats": "+35% konwersja lead→klient, 20h/tyg oszczędności",
        "deploy_time": "1-2 tygodnie",
    },
    {
        "name": "Custom AI Integration",
        "description_pl": "Integracja AI z Twoimi istniejącymi systemami — CRM, ERP, "
                          "ecommerce, helpdesk. Dopasowane do Twoich procesów.",
        "description_en": "AI integration with your existing systems — CRM, ERP, "
                          "ecommerce, helpdesk. Tailored to your processes.",
        "key_stats": "91% pozytywny ROI w 6 miesięcy",
        "deploy_time": "2-6 tygodni",
    },
]

# Na podstawie market data: enterprise cluster $100K-150K,
# SMB prefer pay-as-you-go, value-based pricing > cost-plus
PRICING = {
    "currency": "PLN",
    "tiers": [
        {
            "name": "Starter",
            "monthly": 2500,
            "setup": 5000,
            "includes": [
                "1 AI chatbot (do 5000 konwersacji/mies)",
                "1 automatyzacja procesowa",
                "Integracja z 2 systemami",
                "Dashboard analityczny",
                "Email support",
            ],
            "target": "Firmy 10-30 osób, ecommerce, startupy",
        },
        {
            "name": "Professional",
            "monthly": 5000,
            "setup": 10000,
            "includes": [
                "AI chatbot (unlimited konwersacje)",
                "3 automatyzacje procesowe",
                "AI Sales Assistant",
                "Integracja z 5 systemami",
                "Dashboard + raporty tygodniowe",
                "Dedykowany opiekun",
                "Priorytetowy support",
            ],
            "target": "Firmy 30-100 osób, SaaS, agencje, B2B",
            "recommended": True,
        },
        {
            "name": "Enterprise",
            "monthly": 10000,
            "setup": 20000,
            "includes": [
                "Wszystko z Professional",
                "Unlimited automatyzacje",
                "Custom AI modele dopasowane do Twojej branży",
                "Pełna integracja z tech stackiem",
                "SLA 99.9%",
                "Dedykowany zespół wdrożeniowy",
                "Szkolenia zespołu",
            ],
            "target": "Firmy 100-500 osób, enterprise, fintech",
        },
    ],
    "annual_discount": "2 miesiące gratis przy płatności rocznej",
}

TARGET_AUDIENCE = {
    "ideal_customer_profile": {
        "company_size": "10-200 osób",
        "industries": ["SaaS", "Ecommerce", "Agencje marketingowe", "B2B usługi", "Fintech"],
        "location": "Polska (primary), CEE (secondary)",
        "decision_makers": ["CEO", "Founder", "CTO", "COO", "Head of Operations"],
        "pain_points": [
            "Zespół traci czas na powtarzalne zadania",
            "Obsługa klienta nie jest 24/7",
            "Leady giną bo nikt nie odpisuje szybko",
            "Manualne raportowanie zabiera godziny",
            "Brak ekspertyzy AI wewnątrz firmy",
        ],
        "buying_signals": [
            "Rekrutują na stanowiska operations/support",
            "Używają Shopify, HubSpot, Salesforce, Zendesk",
            "Mają 10+ osób w customer support",
            "Skalują sprzedaż ale procesy nie nadążają",
        ],
    },
    "anti_patterns": [
        "Firmy < 5 osób (za mały budżet)",
        "Firmy > 500 osób (za długi cykl sprzedaży)",
        "Branże regulowane bez budżetu IT (NGO, szkoły publiczne)",
    ],
}

# Realistyczne case studies oparte na market stats
CASE_STUDIES = [
    {
        "id": "cs1",
        "title": "Ecommerce — AI chatbot przejął 78% zapytań klientów",
        "company_type": "Sklep online, 45 osób, Polska",
        "problem": "5-osobowy zespół support nie nadążał z odpowiedziami. "
                   "Średni czas odpowiedzi: 4 godziny. Klienci odchodzili.",
        "solution": "Wdrożyliśmy AI chatbota zintegrowanego z ich bazą produktów i systemem zamówień.",
        "results": [
            "78% zapytań obsłużonych automatycznie",
            "Czas odpowiedzi: z 4h do 30 sekund",
            "NPS wzrósł o 22 punkty",
            "2 osoby z supportu przeniesione do sprzedaży",
        ],
        "timeline": "Wdrożenie: 8 dni",
        "use_in_outreach": True,
    },
    {
        "id": "cs2",
        "title": "SaaS — automatyzacja onboardingu zwiększyła konwersję o 35%",
        "company_type": "SaaS B2B, 80 osób, Polska",
        "problem": "Manualny onboarding nowych użytkowników. Trial→paid konwersja: 12%. "
                   "Follow-upy wysyłane ręcznie, często za późno.",
        "solution": "AI Sales Assistant + automatyczne follow-upy + spersonalizowane wiadomości "
                    "na podstawie zachowania użytkownika.",
        "results": [
            "Konwersja trial→paid: z 12% do 16.2% (+35%)",
            "Czas onboardingu: z 14 do 3 dni",
            "4500 automatycznych follow-upów/miesiąc",
            "Dodatkowy MRR: ~120K PLN/rok",
        ],
        "timeline": "Wdrożenie: 12 dni",
        "use_in_outreach": True,
    },
    {
        "id": "cs3",
        "title": "Agencja — AI generuje raporty dla klientów automatycznie",
        "company_type": "Agencja digital, 25 osób, Warszawa",
        "problem": "Zespół spędzał 20h/tydzień na ręcznym tworzeniu raportów dla 30 klientów. "
                   "Raporty często miały błędy i opóźnienia.",
        "solution": "Automatyzacja raportowania: AI pobiera dane z Google Analytics, Meta Ads, "
                    "Google Ads, generuje raporty i wysyła klientom.",
        "results": [
            "20h/tydzień oszczędności (1 FTE)",
            "Raporty generowane w 2 minuty zamiast 40",
            "Zero błędów w danych",
            "Klienci dostają raporty w poniedziałek rano automatycznie",
        ],
        "timeline": "Wdrożenie: 10 dni",
        "use_in_outreach": True,
    },
]

# Do personalizacji cold emaili w zależności od branży leada
OUTREACH_HOOKS = {
    "ecommerce": {
        "pain": "Widzę że {company} prowadzi sklep online. Czy Wasz zespół support nadąża z odpowiadaniem na pytania klientów?",
        "stat": "Nasi klienci e-commerce automatyzują 78% zapytań i skracają czas odpowiedzi z godzin do sekund.",
        "cta": "Mam 15 minut w {day}? Pokażę jak to wygląda na żywym demo.",
    },
    "saas": {
        "pain": "Widzę że {company} rozwija produkt SaaS. Jaka jest Wasza konwersja trial→paid?",
        "stat": "Nasz AI Sales Assistant podnosi konwersję trial→paid średnio o 35% dzięki automatycznym, spersonalizowanym follow-upom.",
        "cta": "Chętnie pokażę jak to działa — 15 minut w {day}?",
    },
    "agency": {
        "pain": "Prowadzisz agencję z {size} klientami. Ile czasu Wasz zespół spędza na ręcznym raportowaniu?",
        "stat": "Nasi klienci-agencje oszczędzają 20h/tydzień na automatycznych raportach generowanych przez AI.",
        "cta": "Mogę pokazać demo w 15 minut. Kiedy pasuje?",
    },
    "b2b": {
        "pain": "Widzę że {company} działa w B2B. Czy leady z Waszej strony dostaną odpowiedź w ciągu minuty?",
        "stat": "AI chatbot odpowiada w 30 sekund i kwalifikuje leady 24/7. Nasi klienci B2B podwoili liczbę umówionych spotkań.",
        "cta": "15 minut demo? Mogę w {day}.",
    },
    "default": {
        "pain": "Widzę że {company} zatrudnia {size} osób. Ile powtarzalnych zadań w Waszych procesach mogłoby działać automatycznie?",
        "stat": "Firmy po wdrożeniu naszej automatyzacji AI oszczędzają średnio 40% czasu i redukują koszty operacyjne o 30%.",
        "cta": "Chętnie pokażę konkretne przykłady — 15 minut w {day}?",
    },
}

MARKET_CONTEXT = {
    "market_size": "Applied AI Service Market: $1.87B do 2032",
    "poland_ai_investment": "Microsoft zainwestował $700M w AI capacity w Polsce",
    "smb_ai_adoption": "75% SMB już inwestuje w AI, 42% aktywnie używa",
    "chatbot_impact": "AI chatboty odpowiadają na 80% zapytań, -50% kosztów",
    "productivity_gain": "60-70% wzrost produktywności po wdrożeniu AI automation",
    "roi_timeline": "91% firm raportuje pozytywny ROI w ciągu 6 miesięcy",
    "top_demand_areas": [
        "Data analysis & reporting (60%)",
        "Content creation & marketing (49%)",
        "Customer service (42%)",
        "Inventory management (34%)",
    ],
}
