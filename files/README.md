# C1 — Automated Client Acquisition System

Automates B2B lead generation and outreach: scrapes leads, enriches them with company data, scores by fit, generates personalized cold emails using AI, and sends them via SMTP.

## Features

- **Multi-source lead collection** — web scraping + LinkedIn (via Proxycurl / Apollo / mock)
- **Lead enrichment** — company size, tech stack, revenue range (Clearbit optional)
- **Scoring engine** — 0–100 score based on title seniority, email quality, company fit
- **AI-generated messages** — personalized cold emails via Claude API
- **SMTP sending** — with open tracking pixel + unsubscribe footer
- **SQLite storage** — deduplication, status tracking, export to CSV
- **Scheduler** — runs automatically on a configurable interval
- **CLI** — full control from the terminal

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Fill in ANTHROPIC_API_KEY, SMTP_USER, SMTP_PASS, SENDER_NAME, VALUE_PROPOSITION

# 3. Dry run (collect leads, no emails sent)
python main.py run --niche "ecommerce Poland" --dry-run

# 4. Full run
python main.py run --niche "SaaS" --limit 30

# 5. Schedule (every 24h)
python main.py schedule --interval 24 --niche "SaaS"

# 6. Report
python main.py report --last 7
```

## Architecture

```
main.py                  # CLI entry point
src/
  pipeline.py            # Orchestrates everything
  scrapers/
    web_scraper.py       # Extracts emails from websites
    linkedin_scraper.py  # Finds decision-makers on LinkedIn
  outreach/
    message_generator.py # Generates personalized emails via Claude
    email_sender.py      # SMTP sender with tracking
  storage/
    models.py            # Lead dataclass + LeadStatus enum
    lead_store.py        # SQLite persistence + dedup
  utils/
    enricher.py          # Enriches leads + scoring (0–100)
    config.py            # YAML + .env config loader
    logger.py            # File + console logging
    reporter.py          # Funnel analytics
config/
  config.yaml            # Non-sensitive configuration
tests/
  test_pipeline.py       # pytest test suite
```

## LinkedIn Providers

| Provider | Setup |
|----------|-------|
| `mock` | No setup needed — synthetic leads for dev/testing |
| `apollo` | Set `APOLLO_API_KEY` |
| `proxycurl` | Set `PROXYCURL_API_KEY` |

## Lead Scoring

| Signal | Points |
|--------|--------|
| Business email | +15 |
| Name present | +10 |
| Company present | +10 |
| LinkedIn URL | +10 |
| CEO/Founder title | +20 |
| C-suite / Director | +15 |
| Company size 10–200 | +15 |
| Valuable tech stack | +5 per match |

## Tests

```bash
pytest tests/ -v
```

## License

MIT
