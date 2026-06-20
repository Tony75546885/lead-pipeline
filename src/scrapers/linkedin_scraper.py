"""
LinkedIn lead finder — uses search API or scraping to find decision makers.
Requires LINKEDIN_EMAIL + LINKEDIN_PASSWORD in config (cookie-based session).
"""
import time
import random
from typing import Optional

from src.storage.models import Lead
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LinkedInScraper:
    """
    Finds leads on LinkedIn by niche/title/location.

    NOTE: LinkedIn's ToS restricts automated scraping. This module provides
    the interface; actual implementation should use an approved data provider
    (e.g. Proxycurl, Apollo, or LinkedIn's official API) rather than direct scraping.
    Configure via LINKEDIN_PROVIDER in config.
    """

    def __init__(self, config: dict):
        self.config = config
        self.provider = config.get("linkedin_provider", "mock")
        self._client = self._build_client()

    def _build_client(self):
        if self.provider == "proxycurl":
            return ProxycurlClient(self.config.get("proxycurl_api_key", ""))
        elif self.provider == "apollo":
            return ApolloClient(self.config.get("apollo_api_key", ""))
        else:
            logger.warning("LinkedIn provider=mock — returning synthetic leads for testing")
            return MockLinkedInClient()

    def search(
        self,
        niche: str,
        titles: Optional[list[str]] = None,
        location: Optional[str] = None,
        limit: int = 50,
    ) -> list[Lead]:
        titles = titles or self.config.get("target_titles", ["CEO", "Founder", "Head of Marketing", "CMO"])
        location = location or self.config.get("target_location", "Poland")
        logger.info(f"LinkedIn search | niche={niche} titles={titles} location={location}")
        return self._client.search(niche=niche, titles=titles, location=location, limit=limit)


class MockLinkedInClient:
    """Generates realistic fake leads for development/testing."""

    FIRST_NAMES = ["Tomasz", "Marek", "Piotr", "Anna", "Katarzyna", "Michał", "Adam", "Marta"]
    LAST_NAMES = ["Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamińska"]
    COMPANIES = ["TechFlow Sp. z o.o.", "DataPrime", "GrowthLab", "NovaSoft", "DigitalEdge"]
    TITLES = ["CEO", "Founder", "Head of Growth", "CMO", "Co-Founder & CEO"]

    def search(self, niche: str, titles: list[str], location: str, limit: int) -> list[Lead]:
        import random
        leads = []
        for _ in range(min(limit, 10)):
            fn = random.choice(self.FIRST_NAMES)
            ln = random.choice(self.LAST_NAMES)
            company = random.choice(self.COMPANIES)
            slug = company.lower().replace(" ", "").replace(".", "").replace(",", "")
            leads.append(Lead(
                first_name=fn,
                last_name=ln,
                email=f"{fn.lower()}.{ln.lower()}@{slug}.pl",
                company=company,
                title=random.choice(self.TITLES),
                niche=niche,
                location=location,
                linkedin_url=f"https://linkedin.com/in/{fn.lower()}-{ln.lower()}",
                source="linkedin:mock",
                score=random.randint(30, 90),
            ))
        return leads


class ProxycurlClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base = "https://nubela.co/proxycurl/api"

    def search(self, niche: str, titles: list[str], location: str, limit: int) -> list[Lead]:
        import requests
        headers = {"Authorization": f"Bearer {self.api_key}"}
        leads = []
        for title in titles:
            resp = requests.get(
                f"{self.base}/v2/search/person",
                headers=headers,
                params={"current_role_title": title, "region": location, "page_size": limit // len(titles)},
                timeout=15,
            )
            if resp.ok:
                for p in resp.json().get("results", []):
                    leads.append(Lead(
                        first_name=p.get("first_name"),
                        last_name=p.get("last_name"),
                        email=p.get("personal_emails", [None])[0],
                        company=p.get("current_company", {}).get("name"),
                        title=p.get("headline"),
                        linkedin_url=p.get("linkedin_profile_url"),
                        niche=niche,
                        location=location,
                        source="linkedin:proxycurl",
                    ))
        return leads[:limit]


class ApolloClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, niche: str, titles: list[str], location: str, limit: int) -> list[Lead]:
        import requests
        payload = {
            "api_key": self.api_key,
            "person_titles": titles,
            "person_locations": [location],
            "per_page": min(limit, 25),
        }
        resp = requests.post("https://api.apollo.io/v1/mixed_people/search", json=payload, timeout=15)
        leads = []
        if resp.ok:
            for p in resp.json().get("people", []):
                leads.append(Lead(
                    first_name=p.get("first_name"),
                    last_name=p.get("last_name"),
                    email=p.get("email"),
                    company=p.get("organization", {}).get("name"),
                    title=p.get("title"),
                    linkedin_url=p.get("linkedin_url"),
                    niche=niche,
                    location=location,
                    source="linkedin:apollo",
                ))
        return leads
