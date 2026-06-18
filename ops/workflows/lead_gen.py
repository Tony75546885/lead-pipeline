"""
Lead Generation Workflow — Apollo → Enrichment → Scoring → Notion CRM

Instrukcje dla Claude Code dotyczące generowania leadów.
Claude wykonuje te kroki używając MCP tools w Claude Code session.
"""

WORKFLOW = {
    "name": "Lead Generation",
    "trigger": "Użytkownik mówi 'szukaj leadów' LUB pipeline ma < 50 aktywnych leadów",
    "steps": [
        {
            "step": 1,
            "name": "Szukaj w Apollo",
            "mcp_tool": "mcp__apollo__mixed_people_api_search",
            "params_template": {
                "person_titles": ["CEO", "Founder", "Head of Marketing", "CMO", "Co-Founder"],
                "person_locations": ["Poland"],
                "per_page": 25,
                "page": 1,
            },
            "notes": "Dostosuj person_titles i person_locations do niszy użytkownika",
        },
        {
            "step": 2,
            "name": "Enrichuj firmy",
            "mcp_tool": "mcp__apollo__organizations_enrich",
            "notes": "Dla każdego leada z kroku 1, enrichuj domenę firmy",
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
            "name": "Zapisz do Notion CRM",
            "mcp_tool": "mcp__notion__create_pages",
            "notes": """
                Dla każdego zakwalifikowanego leada stwórz stronę w bazie CRM:
                - Name: {first_name} {last_name}
                - Email: {email}
                - Company: {company}
                - Title: {title}
                - Status: 'qualified'
                - Score: {score}
                - Source: 'apollo'
                - LinkedIn: {linkedin_url}
                - Website: {website}
            """,
        },
        {
            "step": 5,
            "name": "Raport",
            "output": "Podsumowanie: ile znaleziono, ile zakwalifikowano, ile dodano do CRM",
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
        "q_organization_keyword_tags": ["marketing agency", "digital agency", "agencja marketingowa"],
        "organization_num_employees_ranges": ["5,50"],
    },
    "startups_cee": {
        "person_titles": ["CEO", "Founder", "Co-Founder", "CTO"],
        "person_locations": ["Poland", "Czech Republic", "Romania", "Hungary"],
        "q_organization_keyword_tags": ["startup", "tech"],
        "organization_num_employees_ranges": ["1,50"],
    },
}
