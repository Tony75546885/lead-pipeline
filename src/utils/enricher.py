"""
Lead enricher — adds company data, detects technologies, scores leads
"""
import re
from typing import Optional

import requests
from src.storage.models import Lead
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LeadEnricher:
    def __init__(self, config: dict):
        self.config = config
        self.clearbit_key = config.get("clearbit_api_key", "")
        self.hunter_key = config.get("hunter_api_key", "")

    def enrich(self, lead: Lead) -> Lead:
        if lead.website:
            domain = self._extract_domain(lead.website)
            self._enrich_from_domain(lead, domain)

        if lead.email and not lead.company:
            domain = lead.email.split("@")[-1]
            self._enrich_from_domain(lead, domain)

        lead.score = self._score(lead)
        logger.debug(f"Enriched {lead.display} | score={lead.score}")
        return lead

    def _enrich_from_domain(self, lead: Lead, domain: str):
        if self.clearbit_key:
            self._clearbit_enrich(lead, domain)
        else:
            self._basic_enrich(lead, domain)

    def _clearbit_enrich(self, lead: Lead, domain: str):
        try:
            resp = requests.get(
                f"https://company.clearbit.com/v2/companies/find?domain={domain}",
                auth=(self.clearbit_key, ""),
                timeout=8,
            )
            if resp.ok:
                data = resp.json()
                lead.company = lead.company or data.get("name")
                lead.company_size = str(data.get("metrics", {}).get("employees", "")) or lead.company_size
                lead.location = lead.location or data.get("location")
                techs = data.get("tech", [])
                lead.technologies = list(set(lead.technologies + techs))
                revenue = data.get("metrics", {}).get("estimatedAnnualRevenue")
                if revenue:
                    lead.revenue_range = revenue
        except Exception as e:
            logger.debug(f"Clearbit failed for {domain}: {e}")

    def _basic_enrich(self, lead: Lead, domain: str):
        """Lightweight enrichment without paid API — infer from domain patterns."""
        if not lead.website:
            lead.website = f"https://{domain}"
        # Infer company name from domain
        if not lead.company:
            name = domain.split(".")[0].replace("-", " ").replace("_", " ").title()
            lead.company = name

    def _score(self, lead: Lead) -> int:
        score = 0

        # Email quality
        if lead.email:
            score += 20
            if not re.search(r"(gmail|yahoo|hotmail|outlook)\.", lead.email):
                score += 15  # business email

        # Profile completeness
        if lead.first_name:
            score += 5
        if lead.last_name:
            score += 5
        if lead.company:
            score += 10
        if lead.linkedin_url:
            score += 10

        # Title scoring
        if lead.title:
            title_lower = lead.title.lower()
            if any(t in title_lower for t in ["ceo", "founder", "owner", "president"]):
                score += 20
            elif any(t in title_lower for t in ["cto", "cmo", "coo", "director", "head of", "vp"]):
                score += 15
            elif any(t in title_lower for t in ["manager", "lead", "principal"]):
                score += 8

        # Company size
        if lead.company_size:
            try:
                size = int(re.sub(r"\D", "", lead.company_size) or 0)
                if 10 <= size <= 200:
                    score += 15  # sweet spot for SME outreach
                elif size > 200:
                    score += 8
            except ValueError:
                pass

        # Technology signals
        if lead.technologies:
            valuable_tech = {"shopify", "stripe", "hubspot", "salesforce", "wordpress", "woocommerce"}
            matches = valuable_tech & {t.lower() for t in lead.technologies}
            score += len(matches) * 5

        return min(score, 100)

    @staticmethod
    def _extract_domain(url: str) -> str:
        url = re.sub(r"^https?://", "", url)
        url = url.split("/")[0]
        return url.replace("www.", "")
