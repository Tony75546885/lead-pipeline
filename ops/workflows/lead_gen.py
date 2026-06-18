"""
Lead Generation Workflow — Apollo → Enrichment → Scoring → Notion CRM

Maps to real Notion CRM structure:
- Pipeline: collection://7b716879-9481-42a1-835e-9ebb8d893ace
- Kontakty: collection://41489d85-cc78-498a-affa-cea4450166a0
"""

NOTION_IDS = {
    "pipeline": "collection://7b716879-9481-42a1-835e-9ebb8d893ace",
    "pipeline_db": "8bb60f0e-f502-4a54-b287-0dca38e6aec0",
    "kontakty": "collection://41489d85-cc78-498a-affa-cea4450166a0",
    "kontakty_db": "8bea6572-f6ea-4a1b-809b-0e35f9559547",
    "outreach": "collection://31677235-f40e-4e24-8e82-147e44b8503e",
    "outreach_db": "4b6dd10c-bba3-4226-878b-9d7e3ad28404",
    "crm_hub": "3726487675b5817998bbffb606ecaf5d",
}

WORKFLOW = {
    "name": "Lead Generation",
    "steps": [
        {
            "step": 1,
            "name": "Szukaj w Apollo",
            "mcp_tool": "mcp__apollo__mixed_people_api_search",
            "notes": "Dostosuj person_titles i person_locations do niszy",
        },
        {
            "step": 2,
            "name": "Enrichuj firmy",
            "mcp_tool": "mcp__apollo__organizations_enrich",
        },
        {
            "step": 3,
            "name": "Scoruj leady",
            "logic": """
                score = 0
                if business_email: score += 15
                if has_name: score += 10
                if has_company: score += 10
                if has_linkedin: score += 10
                if title in [CEO, Founder, Owner]: score += 20
                if title in [CTO, CMO, Director, VP]: score += 15
                if company_size 10-200: score += 15
                if valuable_tech: score += 5 per match
                qualified = score >= 40
            """,
        },
        {
            "step": 4,
            "name": "Zapisz do Pipeline",
            "mcp_tool": "mcp__notion__create_pages",
            "params_mapping": {
                "database_id": NOTION_IDS["pipeline_db"],
                "properties": {
                    "Lead": "{first_name} {last_name}",
                    "Email": "{email}",
                    "Firma": "{company}",
                    "Stanowisko": "{title}",
                    "Etap": "New",
                    "Score": "{score}",
                    "Nisza": "{niche}",
                    "Zrodlo": "Apollo",
                    "Priorytet": "Wysoki if score >= 70, Sredni if >= 50, Niski otherwise",
                },
            },
        },
        {
            "step": 5,
            "name": "Zapisz do Kontakty",
            "mcp_tool": "mcp__notion__create_pages",
            "params_mapping": {
                "database_id": NOTION_IDS["kontakty_db"],
                "properties": {
                    "Imie Nazwisko": "{first_name} {last_name}",
                    "Email": "{email}",
                    "Firma": "{company}",
                    "Stanowisko": "{title}",
                    "Status": "Lead",
                    "Score": "{score}",
                    "Nisza": "{niche}",
                    "Zrodlo": "Apollo",
                    "LinkedIn": "{linkedin_url}",
                    "Lokalizacja": "{location}",
                    "Telefon": "{phone}",
                },
            },
        },
    ],
}

APOLLO_SEARCH_PRESETS = {
    "saas_poland": {
        "person_titles": ["CEO", "Founder", "CTO", "Head of Product"],
        "person_locations": ["Poland"],
        "q_organization_keyword_tags": ["SaaS", "software"],
        "organization_num_employees_ranges": ["11,50", "51,200"],
    },
    "ecommerce_poland": {
        "person_titles": ["CEO", "Founder", "Head of Marketing", "CMO"],
        "person_locations": ["Poland"],
        "q_organization_keyword_tags": ["ecommerce", "e-commerce", "sklep internetowy"],
        "organization_num_employees_ranges": ["11,100"],
    },
    "marketing_agencies": {
        "person_titles": ["CEO", "Founder", "Managing Director"],
        "person_locations": ["Poland"],
        "q_organization_keyword_tags": ["marketing agency", "digital agency"],
        "organization_num_employees_ranges": ["5,50"],
    },
    "startups_cee": {
        "person_titles": ["CEO", "Founder", "Co-Founder", "CTO"],
        "person_locations": ["Poland", "Czech Republic", "Romania", "Hungary"],
        "q_organization_keyword_tags": ["startup", "tech"],
        "organization_num_employees_ranges": ["1,50"],
    },
}
