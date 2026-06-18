"""
Content Creation Workflow — Canva + Figma + Wix + Google Drive

Automatyzuje tworzenie materiałów marketingowych i sprzedażowych.
"""

WORKFLOW = {
    "name": "Content & Marketing",
    "sub_workflows": {
        "social_media_post": {
            "trigger": "Użytkownik mówi 'stwórz post' lub cotygodniowo",
            "steps": [
                {
                    "step": 1,
                    "name": "Wygeneruj treść",
                    "logic": """
                        Na podstawie:
                        - Ostatnich sukcesów (converted leads)
                        - Trendów w branży (Bigdata)
                        - Case studies
                        Napisz post na LinkedIn/social media
                    """,
                },
                {
                    "step": 2,
                    "name": "Stwórz grafikę w Canva",
                    "mcp_tool": "mcp__canva__generate_design",
                    "notes": "Stwórz grafikę do posta (1200x628 LinkedIn post)",
                },
                {
                    "step": 3,
                    "name": "Eksportuj",
                    "mcp_tool": "mcp__canva__export_design",
                    "notes": "Eksportuj PNG do Google Drive",
                },
            ],
        },
        "sales_proposal": {
            "trigger": "Lead po spotkaniu gotowy na propozycję",
            "steps": [
                {
                    "step": 1,
                    "name": "Zbierz dane",
                    "logic": "Pobierz z Notion CRM: potrzeby klienta, notatki ze spotkań, dane firmy",
                },
                {
                    "step": 2,
                    "name": "Stwórz propozycję",
                    "mcp_tool": "mcp__gdrive__create_file",
                    "notes": """
                        Stwórz Google Doc z propozycją:
                        1. Podsumowanie potrzeb
                        2. Proponowane rozwiązanie
                        3. Zakres prac
                        4. Timeline
                        5. Cennik
                        6. Dalsze kroki
                    """,
                },
                {
                    "step": 3,
                    "name": "Stwórz prezentację w Canva",
                    "mcp_tool": "mcp__canva__generate_design",
                    "notes": "Stwórz ładną prezentację z propozycją (opcjonalnie)",
                },
                {
                    "step": 4,
                    "name": "Wyślij propozycję",
                    "mcp_tool": "mcp__gmail__create_draft",
                    "notes": "Draft emaila z linkiem do propozycji",
                },
                {
                    "step": 5,
                    "name": "Zaktualizuj CRM",
                    "mcp_tool": "mcp__notion__update_page",
                    "notes": "Status → 'proposal_sent'",
                },
            ],
        },
        "landing_page": {
            "trigger": "Użytkownik mówi 'stwórz landing page' lub nowa kampania",
            "steps": [
                {
                    "step": 1,
                    "name": "Zaprojektuj w Figma",
                    "mcp_tool": "mcp__figma__generate_design",
                    "notes": "Stwórz makietę landing page'a",
                },
                {
                    "step": 2,
                    "name": "Zbuduj na Wix",
                    "mcp_tool": "mcp__wix__WixSiteBuilder",
                    "notes": "Zaimplementuj design na Wix",
                },
            ],
        },
    },
}
