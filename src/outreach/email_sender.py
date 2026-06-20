"""
Email sender — SMTP with open tracking pixel + unsubscribe footer
"""
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import Optional

from src.storage.models import Lead
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EmailSender:
    def __init__(self, config: dict):
        self.config = config
        self.smtp_host = config.get("smtp_host", "smtp.gmail.com")
        self.smtp_port = config.get("smtp_port", 587)
        self.smtp_user = config.get("smtp_user", "")
        self.smtp_pass = config.get("smtp_pass", "")
        self.from_name = config.get("sender_name", "")
        self.from_email = config.get("smtp_user", "")
        self.tracking_domain = config.get("tracking_domain", "")
        self.unsubscribe_url = config.get("unsubscribe_url", "")

    def send(self, lead: Lead, message: dict) -> bool:
        if not lead.email:
            logger.warning(f"No email for lead: {lead.display}")
            return False

        msg_id = str(uuid.uuid4())
        html_body = self._build_html(message["body"], msg_id, lead)
        text_body = self._build_text(message["body"])

        msg = MIMEMultipart("alternative")
        msg["Subject"] = message["subject"]
        msg["From"] = f"{self.from_name} <{self.from_email}>"
        msg["To"] = lead.email
        msg["Message-ID"] = f"<{msg_id}@{self.smtp_host}>"
        msg["X-Lead-ID"] = msg_id

        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.from_email, lead.email, msg.as_string())
            logger.info(f"✓ Sent to {lead.email} | subject='{message['subject']}'")
            return True
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error for {lead.email}: {e}")
            return False

    def _build_text(self, body: str) -> str:
        footer = ""
        if self.unsubscribe_url:
            footer = f"\n\n---\nAby zrezygnować z wiadomości: {self.unsubscribe_url}"
        return body + footer

    def _build_html(self, body: str, msg_id: str, lead: Lead) -> str:
        paragraphs = "".join(f"<p>{line}</p>" for line in body.split("\n") if line.strip())
        
        tracking_pixel = ""
        if self.tracking_domain:
            tracking_pixel = f'<img src="{self.tracking_domain}/t/{msg_id}.png" width="1" height="1" style="display:none" />'

        unsubscribe_link = ""
        if self.unsubscribe_url:
            unsubscribe_link = f'<p style="color:#999;font-size:11px;margin-top:32px">Nie chcesz otrzymywać wiadomości? <a href="{self.unsubscribe_url}?id={msg_id}" style="color:#999">Wypisz się</a></p>'

        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#222;max-width:560px;margin:0 auto;padding:24px">
{paragraphs}
{unsubscribe_link}
{tracking_pixel}
</body>
</html>"""
