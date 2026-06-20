"""
Persistent lead storage using SQLite
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional
from contextlib import contextmanager

from .models import Lead, LeadStatus
from ..utils.logger import get_logger

logger = get_logger(__name__)


class LeadStore:
    def __init__(self, db_path: str = "data/leads.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        import os
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else ".", exist_ok=True)
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    first_name TEXT,
                    last_name TEXT,
                    company TEXT,
                    title TEXT,
                    website TEXT,
                    linkedin_url TEXT,
                    phone TEXT,
                    niche TEXT,
                    location TEXT,
                    company_size TEXT,
                    revenue_range TEXT,
                    technologies TEXT,
                    source TEXT,
                    score INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'new',
                    created_at TEXT,
                    contacted_at TEXT,
                    notes TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON leads(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_score ON leads(score)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON leads(created_at)")
        logger.debug(f"DB initialized at {self.db_path}")

    def upsert(self, lead: Lead) -> int:
        d = lead.to_dict()
        with self._conn() as conn:
            cursor = conn.execute("""
                INSERT INTO leads (email, first_name, last_name, company, title, website,
                    linkedin_url, phone, niche, location, company_size, revenue_range,
                    technologies, source, score, status, created_at, contacted_at, notes)
                VALUES (:email, :first_name, :last_name, :company, :title, :website,
                    :linkedin_url, :phone, :niche, :location, :company_size, :revenue_range,
                    :technologies, :source, :score, :status, :created_at, :contacted_at, :notes)
                ON CONFLICT(email) DO UPDATE SET
                    first_name=excluded.first_name,
                    last_name=excluded.last_name,
                    company=excluded.company,
                    title=excluded.title,
                    website=excluded.website,
                    linkedin_url=excluded.linkedin_url,
                    phone=excluded.phone,
                    niche=excluded.niche,
                    location=excluded.location,
                    company_size=excluded.company_size,
                    revenue_range=excluded.revenue_range,
                    technologies=excluded.technologies,
                    source=excluded.source,
                    score=excluded.score,
                    status=excluded.status,
                    contacted_at=excluded.contacted_at,
                    notes=excluded.notes
            """, d)
            return cursor.lastrowid

    def get_all_emails(self) -> list[str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT email FROM leads WHERE email IS NOT NULL").fetchall()
            return [r["email"] for r in rows]

    def get_by_status(self, status: LeadStatus) -> list[Lead]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM leads WHERE status = ? ORDER BY score DESC", (status.value,)
            ).fetchall()
            return [Lead.from_dict(dict(r)) for r in rows]

    def get_stats(self, since: Optional[datetime] = None) -> dict:
        with self._conn() as conn:
            base = "SELECT status, COUNT(*) as cnt FROM leads"
            if since:
                base += f" WHERE created_at >= '{since.isoformat()}'"
            base += " GROUP BY status"
            rows = conn.execute(base).fetchall()
            stats = {r["status"]: r["cnt"] for r in rows}
            total = conn.execute(
                "SELECT COUNT(*) as c FROM leads" + (f" WHERE created_at >= '{since.isoformat()}'" if since else "")
            ).fetchone()["c"]
            stats["total"] = total
            return stats

    def export_csv(self, path: str, status: Optional[LeadStatus] = None):
        import csv
        with self._conn() as conn:
            q = "SELECT * FROM leads"
            if status:
                q += f" WHERE status = '{status.value}'"
            rows = conn.execute(q).fetchall()
        with open(path, "w", newline="", encoding="utf-8") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows([dict(r) for r in rows])
        logger.info(f"Exported {len(rows)} leads to {path}")
