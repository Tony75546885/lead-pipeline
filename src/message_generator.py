"""
Personalized outreach message generator using Claude API
"""
import anthropic
from ..storage.models import Lead
from ..utils.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """Jesteś ekspertem od cold outreach B2B. Piszesz krótkie, spersonalizowane wiadomości po polsku lub angielsku (w zależności od lokalizacji leada).

Zasady:
- Max 5 zdań
- Zacznij od spersonalizowanego nawiązania do firmy lub roli
- Jasna propozycja wartości (nie produkt, a efekt)
- Jedno konkretne CTA (nie "daj znać" — zaproponuj konkretny termin/akcję)
- Zero corporate speak, zero "Mam nadzieję że ta wiadomość zastanie Cię w dobrym momencie"
- Ton: bezpośredni, człowieczy, pewny siebie
"""


class MessageGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.get("anthropic_api_key", ""))
        self.sender_name = config.get("sender_name", "")
        self.sender_company = config.get("sender_company", "")
        self.value_prop = config.get("value_proposition", "")

    def generate(self, lead: Lead) -> dict:
        """Returns dict with subject and body"""
        prompt = self._build_prompt(lead)

        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        subject, body = self._parse_response(raw, lead)

        logger.debug(f"Generated message for {lead.display}")
        return {"subject": subject, "body": body}

    def _build_prompt(self, lead: Lead) -> str:
        parts = [
            f"Napisz cold email do: {lead.display}",
            f"Firma: {lead.company or 'nieznana'}",
            f"Branża: {lead.niche or 'nieznana'}",
        ]
        if lead.website:
            parts.append(f"Strona: {lead.website}")
        if lead.technologies:
            parts.append(f"Technologie: {', '.join(lead.technologies)}")
        if lead.company_size:
            parts.append(f"Wielkość firmy: {lead.company_size}")
        parts.append(f"\nNadawca: {self.sender_name} z {self.sender_company}")
        parts.append(f"Propozycja wartości: {self.value_prop}")
        parts.append("\nFormat odpowiedzi:\nTEMAT: <temat maila>\n\n<treść maila>")
        return "\n".join(parts)

    def _parse_response(self, raw: str, lead: Lead) -> tuple[str, str]:
        if "TEMAT:" in raw:
            lines = raw.split("\n", 2)
            subject_line = lines[0].replace("TEMAT:", "").strip()
            body = "\n".join(lines[2:]).strip() if len(lines) > 2 else raw
        else:
            subject_line = f"Pytanie do {lead.company or lead.full_name}"
            body = raw

        return subject_line, body

    def preview(self, lead: Lead) -> str:
        msg = self.generate(lead)
        return f"TEMAT: {msg['subject']}\n\n{msg['body']}"
