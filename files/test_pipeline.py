"""
Tests for C1 — run with: pytest
"""
import pytest
from src.storage.models import Lead, LeadStatus
from src.storage.lead_store import LeadStore
from src.utils.enricher import LeadEnricher


# --- Model tests ---

def test_lead_full_name():
    lead = Lead(first_name="Jan", last_name="Kowalski")
    assert lead.full_name == "Jan Kowalski"

def test_lead_full_name_missing():
    lead = Lead(email="jan@example.com")
    assert lead.full_name == "there"

def test_lead_serialization_roundtrip():
    lead = Lead(
        email="jan@firma.pl",
        first_name="Jan",
        company="Firma Sp. z o.o.",
        technologies=["Shopify", "Stripe"],
        status=LeadStatus.QUALIFIED,
        score=75,
    )
    d = lead.to_dict()
    restored = Lead.from_dict(d)
    assert restored.email == lead.email
    assert restored.score == 75
    assert restored.status == LeadStatus.QUALIFIED
    assert "Shopify" in restored.technologies


# --- Storage tests ---

def test_lead_store_upsert_and_dedup(tmp_path):
    store = LeadStore(db_path=str(tmp_path / "test.db"))
    lead = Lead(email="test@firma.pl", company="TestCo", score=55)
    store.upsert(lead)
    store.upsert(lead)  # should not duplicate
    emails = store.get_all_emails()
    assert emails.count("test@firma.pl") == 1

def test_lead_store_status_filter(tmp_path):
    store = LeadStore(db_path=str(tmp_path / "test.db"))
    lead = Lead(email="a@b.pl", status=LeadStatus.QUALIFIED, score=60)
    store.upsert(lead)
    results = store.get_by_status(LeadStatus.QUALIFIED)
    assert any(r.email == "a@b.pl" for r in results)

def test_lead_store_stats(tmp_path):
    store = LeadStore(db_path=str(tmp_path / "test.db"))
    for i in range(3):
        store.upsert(Lead(email=f"lead{i}@test.pl", status=LeadStatus.CONTACTED))
    stats = store.get_stats()
    assert stats["total"] == 3


# --- Enricher / Scoring tests ---

def test_scorer_business_email():
    config = {}
    enricher = LeadEnricher(config)
    lead = Lead(email="ceo@startup.pl", first_name="Anna", last_name="N", company="Startup", title="CEO")
    scored = enricher.enrich(lead)
    assert scored.score >= 60

def test_scorer_gmail_lower_score():
    config = {}
    enricher = LeadEnricher(config)
    lead = Lead(email="random@gmail.com")
    scored = enricher.enrich(lead)
    assert scored.score < 40

def test_scorer_max_100():
    config = {}
    enricher = LeadEnricher(config)
    lead = Lead(
        email="founder@corp.com",
        first_name="X", last_name="Y",
        company="Corp", title="CEO & Founder",
        linkedin_url="https://linkedin.com/in/x",
        technologies=["Shopify", "Stripe", "HubSpot", "Salesforce", "WordPress"],
        company_size="50",
    )
    scored = enricher.enrich(lead)
    assert scored.score <= 100
