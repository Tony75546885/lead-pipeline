"""
C1 Business Operations Orchestrator

Centralny punkt sterowania wszystkimi workflow'ami biznesowymi.
Łączy MCP tools (Apollo, Gmail, Notion, Calendar, etc.) w spójne procesy.

Użycie z Claude Code:
    from ops.orchestrator import BusinessOrchestrator
    ops = BusinessOrchestrator()
    await ops.daily_review()
    await ops.run_lead_gen("SaaS", limit=30)
"""
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class OpStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class OpResult:
    operation: str
    status: OpStatus
    summary: str
    details: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_log_entry(self) -> str:
        return f"[{self.timestamp:%H:%M}] {self.operation}: {self.status.value} — {self.summary}"


@dataclass
class DailyReport:
    date: str
    leads_found: int = 0
    leads_qualified: int = 0
    emails_sent: int = 0
    replies_received: int = 0
    meetings_scheduled: int = 0
    follow_ups_sent: int = 0
    operations: list[OpResult] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"📊 Raport dzienny — {self.date}",
            f"{'='*40}",
            f"  Nowe leady znalezione  : {self.leads_found}",
            f"  Zakwalifikowane        : {self.leads_qualified}",
            f"  Wysłane maile          : {self.emails_sent}",
            f"  Odpowiedzi            : {self.replies_received}",
            f"  Spotkania zaplanowane  : {self.meetings_scheduled}",
            f"  Follow-upy wysłane     : {self.follow_ups_sent}",
            f"{'='*40}",
            "",
            "Operacje:",
        ]
        for op in self.operations:
            lines.append(f"  {op.to_log_entry()}")
        return "\n".join(lines)


# --- Workflow step definitions ---
# Each workflow is a sequence of MCP tool calls that Claude executes.
# The orchestrator provides structure; Claude provides intelligence.

WORKFLOWS = {
    "daily_review": {
        "name": "Poranny przegląd",
        "steps": [
            {
                "id": "check_emails",
                "tool": "gmail.search_threads",
                "description": "Sprawdź nowe maile (ostatnie 24h)",
                "params": {"query": "is:unread newer_than:1d"},
            },
            {
                "id": "check_calendar",
                "tool": "calendar.list_events",
                "description": "Pobierz dzisiejsze spotkania",
                "params": {"date": "today"},
            },
            {
                "id": "check_crm",
                "tool": "notion.search",
                "description": "Sprawdź follow-upy na dziś w CRM",
                "params": {"query": "follow-up today"},
            },
        ],
    },
    "lead_generation": {
        "name": "Generowanie leadów",
        "steps": [
            {
                "id": "search_apollo",
                "tool": "apollo.mixed_people_api_search",
                "description": "Szukaj leadów po kryteriach",
            },
            {
                "id": "enrich_companies",
                "tool": "apollo.organizations_enrich",
                "description": "Enrichuj dane firmowe",
            },
            {
                "id": "score_leads",
                "tool": "internal.score",
                "description": "Scoruj leady (0-100)",
            },
            {
                "id": "save_to_crm",
                "tool": "notion.create_pages",
                "description": "Zapisz zakwalifikowane leady do Notion CRM",
            },
        ],
    },
    "outreach": {
        "name": "Outreach i follow-upy",
        "steps": [
            {
                "id": "get_qualified",
                "tool": "notion.search",
                "description": "Pobierz leady do kontaktu z CRM",
            },
            {
                "id": "generate_messages",
                "tool": "internal.message_gen",
                "description": "Wygeneruj spersonalizowane wiadomości",
            },
            {
                "id": "send_emails",
                "tool": "gmail.create_draft",
                "description": "Wyślij/drafty maili w Gmail",
            },
            {
                "id": "update_crm",
                "tool": "notion.update_page",
                "description": "Zaktualizuj status leadów w CRM",
            },
        ],
    },
    "follow_up": {
        "name": "Follow-upy",
        "steps": [
            {
                "id": "find_no_reply",
                "tool": "notion.search",
                "description": "Znajdź leady kontaktowane 3+ dni temu bez odpowiedzi",
            },
            {
                "id": "check_threads",
                "tool": "gmail.search_threads",
                "description": "Sprawdź czy nie odpowiedzieli poza CRM",
            },
            {
                "id": "send_followup",
                "tool": "gmail.create_draft",
                "description": "Wyślij follow-up",
            },
        ],
    },
    "meeting_prep": {
        "name": "Przygotowanie do spotkania",
        "steps": [
            {
                "id": "get_meeting",
                "tool": "calendar.list_events",
                "description": "Pobierz szczegóły spotkania",
            },
            {
                "id": "research_company",
                "tool": "bigdata.company_tearsheet",
                "description": "Przygotuj brief o firmie",
            },
            {
                "id": "get_lead_history",
                "tool": "notion.search",
                "description": "Pobierz historię interakcji z CRM",
            },
            {
                "id": "create_agenda",
                "tool": "notion.create_pages",
                "description": "Stwórz agendę spotkania w Notion",
            },
        ],
    },
    "market_intelligence": {
        "name": "Wywiad rynkowy",
        "steps": [
            {
                "id": "search_market",
                "tool": "bigdata.search",
                "description": "Szukaj trendów w branży docelowej",
            },
            {
                "id": "analyze_competitors",
                "tool": "bigdata.company_tearsheet",
                "description": "Analizuj konkurencję klienta",
            },
            {
                "id": "save_report",
                "tool": "notion.create_pages",
                "description": "Zapisz raport w Notion",
            },
        ],
    },
    "content_creation": {
        "name": "Tworzenie treści",
        "steps": [
            {
                "id": "create_design",
                "tool": "canva.generate_design",
                "description": "Stwórz grafikę w Canva",
            },
            {
                "id": "export_assets",
                "tool": "canva.export_design",
                "description": "Eksportuj gotowe materiały",
            },
            {
                "id": "upload_drive",
                "tool": "gdrive.create_file",
                "description": "Zapisz w Google Drive",
            },
        ],
    },
    "reporting": {
        "name": "Raportowanie KPI",
        "steps": [
            {
                "id": "count_leads",
                "tool": "notion.search",
                "description": "Policz leady na każdym etapie",
            },
            {
                "id": "count_emails",
                "tool": "gmail.search_threads",
                "description": "Policz wysłane i odebrane maile",
            },
            {
                "id": "count_meetings",
                "tool": "calendar.list_events",
                "description": "Policz spotkania w okresie",
            },
            {
                "id": "save_report",
                "tool": "notion.create_pages",
                "description": "Zapisz raport w Notion",
            },
        ],
    },
}


def get_workflow(name: str) -> dict:
    return WORKFLOWS.get(name, {})


def list_workflows() -> list[str]:
    return [f"{k}: {v['name']}" for k, v in WORKFLOWS.items()]


def get_daily_ops_plan() -> list[dict]:
    return [
        {"workflow": "daily_review", "priority": 1, "auto": True},
        {"workflow": "lead_generation", "priority": 2, "auto": True},
        {"workflow": "follow_up", "priority": 3, "auto": True},
        {"workflow": "outreach", "priority": 4, "auto": False},
        {"workflow": "reporting", "priority": 5, "auto": True},
    ]
