"""
Reporting Workflow — zbieranie KPI z wszystkich narzędzi

Generuje raporty dzienne, tygodniowe i miesięczne.
"""

WORKFLOW = {
    "name": "Reporting & Analytics",
    "sub_workflows": {
        "daily_kpi": {
            "trigger": "Koniec każdej sesji / użytkownik mówi 'raport'",
            "data_sources": [
                {
                    "source": "Notion CRM",
                    "tool": "mcp__notion__search",
                    "metrics": [
                        "Leady na etapie: new, qualified, contacted, replied, meeting, proposal, converted, lost",
                        "Nowe leady dziś",
                        "Konwersja: qualified → contacted → replied → meeting → converted",
                    ],
                },
                {
                    "source": "Gmail",
                    "tool": "mcp__gmail__search_threads",
                    "metrics": [
                        "Wysłane maile dziś",
                        "Otrzymane odpowiedzi dziś",
                        "Open rate (jeśli tracking pixel)",
                    ],
                },
                {
                    "source": "Calendar",
                    "tool": "mcp__calendar__list_events",
                    "metrics": [
                        "Spotkania dziś/tydzień",
                        "Zaplanowane spotkania",
                    ],
                },
                {
                    "source": "Apollo",
                    "tool": "mcp__apollo__usage_stats_credit_usage_stats",
                    "metrics": [
                        "Kredyty użyte",
                        "Leady znalezione",
                    ],
                },
            ],
        },
        "weekly_report": {
            "trigger": "Piątek / użytkownik mówi 'raport tygodniowy'",
            "format": """
                # Raport tygodniowy C1 — {week}

                ## Pipeline
                | Etap | Liczba | Zmiana w/w |
                |------|--------|------------|
                | New  |   X    |    +Y      |
                | ...  |        |            |

                ## Aktywność
                - Nowe leady: X
                - Wysłane maile: X
                - Odpowiedzi: X (Y% response rate)
                - Spotkania: X
                - Propozycje: X
                - Konwersje: X

                ## Top leady
                1. {lead1} — {company} — score {score} — {status}
                2. ...

                ## Wnioski i akcje na przyszły tydzień
                - ...
            """,
        },
    },
}

KPI_DEFINITIONS = {
    "response_rate": {
        "formula": "replies / emails_sent * 100",
        "target": ">= 15%",
        "alert_below": 5,
    },
    "meeting_rate": {
        "formula": "meetings / replies * 100",
        "target": ">= 30%",
        "alert_below": 10,
    },
    "conversion_rate": {
        "formula": "converted / meetings * 100",
        "target": ">= 20%",
        "alert_below": 5,
    },
    "pipeline_velocity": {
        "formula": "avg days from qualified to converted",
        "target": "<= 30 days",
        "alert_above": 45,
    },
    "cost_per_lead": {
        "formula": "apollo_credits_used / qualified_leads",
        "target": "<= 5 credits",
    },
}
