"""
Core acquisition pipeline - orchestrates scraping, enrichment, outreach
"""
import time
import schedule
from datetime import datetime
from typing import Optional

from .scrapers.web_scraper import WebScraper
from .scrapers.linkedin_scraper import LinkedInScraper
from .outreach.email_sender import EmailSender
from .outreach.message_generator import MessageGenerator
from .storage.lead_store import LeadStore
from .storage.models import Lead, LeadStatus
from .utils.logger import get_logger
from .utils.reporter import Reporter

logger = get_logger(__name__)


class AcquisitionPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.store = LeadStore(config["db_path"])
        self.msg_gen = MessageGenerator(config)
        self.email_sender = EmailSender(config)
        self.reporter = Reporter(self.store)

    def run(
        self,
        source: str = "all",
        niche: Optional[str] = None,
        url: Optional[str] = None,
        limit: int = 50,
        dry_run: bool = False,
    ):
        logger.info(f"Starting acquisition run | source={source} niche={niche} limit={limit} dry_run={dry_run}")
        start = datetime.now()

        raw_leads: list[Lead] = []

        if source in ("scrape", "all") and url:
            scraper = WebScraper(self.config)
            raw_leads += scraper.scrape(url, limit=limit)

        if source in ("linkedin", "all"):
            li = LinkedInScraper(self.config)
            raw_leads += li.search(niche=niche or self.config.get("default_niche", "SaaS"), limit=limit)

        logger.info(f"Collected {len(raw_leads)} raw leads")

        new_leads = self._deduplicate(raw_leads)
        logger.info(f"{len(new_leads)} new leads after dedup")

        enriched = self._enrich_leads(new_leads)
        qualified = self._qualify_leads(enriched)

        logger.info(f"{len(qualified)} leads passed qualification")

        if not dry_run:
            sent = self._run_outreach(qualified)
            logger.info(f"Outreach sent to {sent} leads")
        else:
            logger.info("Dry run — skipping outreach")
            for lead in qualified:
                lead.status = LeadStatus.PENDING
                self.store.upsert(lead)

        elapsed = (datetime.now() - start).total_seconds()
        logger.info(f"Run complete in {elapsed:.1f}s")
        self._print_summary(raw_leads, new_leads, qualified)

    def schedule(self, interval_hours: int = 24, niche: Optional[str] = None):
        logger.info(f"Scheduling pipeline every {interval_hours}h")

        def job():
            self.run(source="all", niche=niche)

        schedule.every(interval_hours).hours.do(job)
        job()  # run immediately on start

        while True:
            schedule.run_pending()
            time.sleep(60)

    def report(self, days: int = 30, fmt: str = "table"):
        self.reporter.print_report(days=days, fmt=fmt)

    def enrich(self, input_file: str):
        import csv
        leads = []
        with open(input_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(Lead.from_dict(row))
        enriched = self._enrich_leads(leads)
        for lead in enriched:
            self.store.upsert(lead)
        logger.info(f"Enriched and saved {len(enriched)} leads from {input_file}")

    def _deduplicate(self, leads: list[Lead]) -> list[Lead]:
        seen_emails = set(self.store.get_all_emails())
        new = []
        for lead in leads:
            if lead.email and lead.email not in seen_emails:
                seen_emails.add(lead.email)
                new.append(lead)
        return new

    def _enrich_leads(self, leads: list[Lead]) -> list[Lead]:
        from .utils.enricher import LeadEnricher
        enricher = LeadEnricher(self.config)
        return [enricher.enrich(lead) for lead in leads]

    def _qualify_leads(self, leads: list[Lead]) -> list[Lead]:
        min_score = self.config.get("min_qualification_score", 40)
        qualified = [l for l in leads if l.score >= min_score]
        for lead in leads:
            lead.status = LeadStatus.QUALIFIED if lead.score >= min_score else LeadStatus.DISQUALIFIED
            self.store.upsert(lead)
        return qualified

    def _run_outreach(self, leads: list[Lead]) -> int:
        sent = 0
        for lead in leads:
            try:
                message = self.msg_gen.generate(lead)
                if lead.email:
                    self.email_sender.send(lead, message)
                    lead.status = LeadStatus.CONTACTED
                    lead.contacted_at = datetime.now()
                    self.store.upsert(lead)
                    sent += 1
                    time.sleep(self.config.get("outreach_delay_seconds", 5))
            except Exception as e:
                logger.error(f"Failed outreach for {lead.email}: {e}")
        return sent

    def _print_summary(self, raw, new, qualified):
        print(f"\n{'='*50}")
        print(f"  Lead Pipeline — Run Summary")
        print(f"{'='*50}")
        print(f"  Raw leads collected : {len(raw)}")
        print(f"  New (after dedup)   : {len(new)}")
        print(f"  Qualified           : {len(qualified)}")
        print(f"{'='*50}\n")
