"""
Lead Pipeline — test suite. Run with: pytest tests/ -v
"""
import pytest
from src.storage.models import Lead, LeadStatus
from src.storage.lead_store import LeadStore
from src.utils.enricher import LeadEnricher
from src.scrapers.web_scraper import WebScraper


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


# --- Web scraper tests ---

def test_junk_email_filter():
    scraper = WebScraper(config={})
    assert scraper._is_junk_email("support@company.com") is True
    assert scraper._is_junk_email("noreply@service.io") is True
    assert scraper._is_junk_email("jan.kowalski@firma.pl") is False

def test_junk_email_rejects_image_extensions():
    scraper = WebScraper(config={})
    assert scraper._is_junk_email("icon@site.png") is True

def test_domain_extraction():
    from src.utils.enricher import LeadEnricher
    assert LeadEnricher._extract_domain("https://www.example.com/page") == "example.com"
    assert LeadEnricher._extract_domain("http://startup.pl") == "startup.pl"


# --- Lead display ---

def test_lead_display_with_full_info():
    lead = Lead(first_name="Anna", last_name="N", title="CEO", company="TechCo")
    assert "Anna N" in lead.display
    assert "CEO" in lead.display
    assert "TechCo" in lead.display

def test_lead_display_email_fallback():
    lead = Lead(email="test@example.com")
    assert lead.display == "test@example.com"
