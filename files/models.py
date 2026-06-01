"""
Data models for leads
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class LeadStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    ENRICHED = "enriched"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"
    CONTACTED = "contacted"
    REPLIED = "replied"
    CONVERTED = "converted"
    BOUNCED = "bounced"


@dataclass
class Lead:
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    niche: Optional[str] = None
    location: Optional[str] = None
    company_size: Optional[str] = None
    revenue_range: Optional[str] = None
    technologies: list[str] = field(default_factory=list)
    source: Optional[str] = None
    score: int = 0
    status: LeadStatus = LeadStatus.NEW
    created_at: datetime = field(default_factory=datetime.now)
    contacted_at: Optional[datetime] = None
    notes: Optional[str] = None

    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.last_name]
        return " ".join(p for p in parts if p) or "there"

    @property
    def display(self) -> str:
        parts = []
        if self.full_name != "there":
            parts.append(self.full_name)
        if self.title:
            parts.append(self.title)
        if self.company:
            parts.append(f"@ {self.company}")
        return " ".join(parts) or self.email or "Unknown Lead"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        d["created_at"] = self.created_at.isoformat() if self.created_at else None
        d["contacted_at"] = self.contacted_at.isoformat() if self.contacted_at else None
        d["technologies"] = ",".join(self.technologies)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Lead":
        d = dict(d)
        if "status" in d and d["status"]:
            d["status"] = LeadStatus(d["status"])
        if "created_at" in d and d["created_at"]:
            d["created_at"] = datetime.fromisoformat(d["created_at"])
        if "contacted_at" in d and d["contacted_at"]:
            d["contacted_at"] = datetime.fromisoformat(d["contacted_at"])
        if "technologies" in d and isinstance(d["technologies"], str):
            d["technologies"] = [t for t in d["technologies"].split(",") if t]
        if "score" in d:
            d["score"] = int(d["score"] or 0)
        valid = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in valid})
