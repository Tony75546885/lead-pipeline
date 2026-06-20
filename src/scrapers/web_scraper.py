"""
Web scraper — extracts leads from company directories, yellow pages, etc.
"""
import re
import time
import random
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from src.storage.models import Lead
from src.utils.logger import get_logger

logger = get_logger(__name__)

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
]


class WebScraper:
    def __init__(self, config: dict):
        self.config = config
        self.session = requests.Session()
        self.delay_range = config.get("scrape_delay", (1.5, 4.0))

    def scrape(self, url: str, limit: int = 50) -> list[Lead]:
        logger.info(f"Scraping: {url}")
        leads = []
        visited = set()
        queue = [url]

        while queue and len(leads) < limit:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            try:
                html = self._fetch(current)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                page_leads = self._extract_leads(soup, current)
                leads.extend(page_leads)
                logger.debug(f"  {current} → {len(page_leads)} leads")

                # find sub-pages on same domain
                for link in soup.find_all("a", href=True):
                    href = urljoin(current, link["href"])
                    if urlparse(href).netloc == urlparse(url).netloc and href not in visited:
                        queue.append(href)
                        if len(queue) > 100:
                            break

                self._sleep()
            except Exception as e:
                logger.warning(f"Failed to scrape {current}: {e}")

        logger.info(f"Scraping done — {len(leads)} leads from {url}")
        return leads[:limit]

    def _fetch(self, url: str) -> Optional[str]:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        try:
            resp = self.session.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            logger.warning(f"HTTP error for {url}: {e}")
            return None

    def _extract_leads(self, soup: BeautifulSoup, source_url: str) -> list[Lead]:
        leads = []
        emails = set(EMAIL_REGEX.findall(soup.get_text()))

        for email in emails:
            if self._is_junk_email(email):
                continue
            lead = Lead(
                email=email.lower(),
                source=f"scrape:{source_url}",
                website=source_url,
            )
            # try to infer name/company from page
            lead.company = self._guess_company(soup, source_url)
            leads.append(lead)

        return leads

    def _guess_company(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        # Try og:site_name or title tag
        og = soup.find("meta", property="og:site_name")
        if og and og.get("content"):
            return og["content"].strip()
        title = soup.find("title")
        if title:
            parts = re.split(r"[\|\-–—]", title.text)
            return parts[-1].strip() if parts else None
        return urlparse(url).netloc.replace("www.", "")

    def _is_junk_email(self, email: str) -> bool:
        junk_patterns = [
            r"^(info|contact|hello|support|noreply|no-reply|admin|webmaster|postmaster)@",
            r"\.(png|jpg|gif|css|js)$",
            r"example\.(com|org)",
            r"@sentry\.",
            r"@.*test\.",
        ]
        return any(re.search(p, email, re.I) for p in junk_patterns)

    def _sleep(self):
        lo, hi = self.delay_range
        time.sleep(random.uniform(lo, hi))
