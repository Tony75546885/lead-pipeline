"""
Config loader — reads config.yaml + .env overrides
"""
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

DEFAULTS = {
    "db_path": "data/leads.db",
    "linkedin_provider": "mock",
    "default_niche": "SaaS",
    "target_titles": ["CEO", "Founder", "Head of Marketing", "CMO"],
    "target_location": "Poland",
    "min_qualification_score": 40,
    "outreach_delay_seconds": 5,
    "scrape_delay": [1.5, 4.0],
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
}

ENV_MAP = {
    "ANTHROPIC_API_KEY": "anthropic_api_key",
    "SMTP_USER": "smtp_user",
    "SMTP_PASS": "smtp_pass",
    "SENDER_NAME": "sender_name",
    "SENDER_COMPANY": "sender_company",
    "VALUE_PROPOSITION": "value_proposition",
    "CLEARBIT_API_KEY": "clearbit_api_key",
    "HUNTER_API_KEY": "hunter_api_key",
    "APOLLO_API_KEY": "apollo_api_key",
    "PROXYCURL_API_KEY": "proxycurl_api_key",
    "LINKEDIN_PROVIDER": "linkedin_provider",
    "TRACKING_DOMAIN": "tracking_domain",
    "UNSUBSCRIBE_URL": "unsubscribe_url",
}


def load_config(path: str = "config/config.yaml") -> dict:
    config = dict(DEFAULTS)

    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            file_config = yaml.safe_load(f) or {}
        config.update(file_config)

    for env_key, cfg_key in ENV_MAP.items():
        val = os.getenv(env_key)
        if val:
            config[cfg_key] = val

    return config
