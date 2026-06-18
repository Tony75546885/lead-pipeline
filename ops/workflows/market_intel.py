"""
Market Intelligence Workflow — Bigdata.com + Apollo + Web

Automatyczny wywiad rynkowy o firmach, branżach i trendach.
"""

WORKFLOW = {
    "name": "Market Intelligence",
    "sub_workflows": {
        "company_research": {
            "trigger": "Przed spotkaniem / użytkownik mówi 'sprawdź firmę X'",
            "steps": [
                {
                    "step": 1,
                    "name": "Bigdata tearsheet",
                    "mcp_tool": "mcp__bigdata__company_tearsheet",
                    "notes": "Pobierz pełny profil firmy: przychody, zatrudnienie, funding, newsy",
                },
                {
                    "step": 2,
                    "name": "Apollo enrichment",
                    "mcp_tool": "mcp__apollo__organizations_enrich",
                    "notes": "Uzupełnij dane: tech stack, social profiles, description",
                },
                {
                    "step": 3,
                    "name": "Job postings",
                    "mcp_tool": "mcp__apollo__organizations_job_postings",
                    "notes": "Sprawdź jakie role rekrutują — sygnał growth i potrzeb",
                },
                {
                    "step": 4,
                    "name": "Decision makers",
                    "mcp_tool": "mcp__apollo__mixed_people_api_search",
                    "notes": "Znajdź kluczowe osoby w firmie",
                },
                {
                    "step": 5,
                    "name": "Kompiluj raport",
                    "output": """
                        ## Company Brief: {company}

                        **Podstawy:** {opis, branża, lokalizacja}
                        **Wielkość:** {employees} osób, {revenue} przychód
                        **Tech stack:** {technologies}
                        **Ostatnie newsy:** {newsy}
                        **Rekrutacja:** {job_postings} — sygnały: {analiza}
                        **Decision makers:** {lista osób}
                        **Potencjalne pain points:** {analiza na podstawie danych}
                        **Rekomendacja podejścia:** {jak pitchować}
                    """,
                },
            ],
        },
        "industry_trends": {
            "trigger": "Cotygodniowo / użytkownik mówi 'trendy w [branży]'",
            "steps": [
                {
                    "step": 1,
                    "name": "Szukaj trendów",
                    "mcp_tool": "mcp__bigdata__search",
                    "notes": "Szukaj ostatnich artykułów i raportów o branży docelowej",
                },
                {
                    "step": 2,
                    "name": "Sentiment",
                    "mcp_tool": "mcp__bigdata__sentiment_tearsheet",
                    "notes": "Sprawdź sentiment rynkowy (dla spółek publicznych w branży)",
                },
                {
                    "step": 3,
                    "name": "Zapisz w Notion",
                    "mcp_tool": "mcp__notion__create_pages",
                    "notes": "Stwórz stronę z podsumowaniem trendów",
                },
            ],
        },
    },
}
