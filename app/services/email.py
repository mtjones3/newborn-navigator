import json
import os
from datetime import datetime
from pathlib import Path

from app.config import BASE_DIR, settings

EMAIL_LOG_DIR = BASE_DIR / "email_logs"
EMAIL_LOG_DIR.mkdir(exist_ok=True)


def send_email(to: str, subject: str, html_body: str) -> dict:
    """Stubbed email sender — writes to email_logs/ instead of sending.

    Compatible with Resend API interface. To switch to real sending,
    replace this function body with:
        import resend
        resend.api_key = settings.RESEND_API_KEY
        return resend.Emails.send({
            "from": settings.FROM_EMAIL,
            "to": to,
            "subject": subject,
            "html": html_body,
        })
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_entry = {
        "to": to,
        "from": settings.FROM_EMAIL,
        "subject": subject,
        "timestamp": datetime.utcnow().isoformat(),
        "api_key_configured": bool(settings.RESEND_API_KEY),
    }

    # Save metadata
    meta_path = EMAIL_LOG_DIR / f"{timestamp}_{to.replace('@', '_at_')}.json"
    with open(meta_path, "w") as f:
        json.dump(log_entry, f, indent=2)

    # Save HTML body
    html_path = EMAIL_LOG_DIR / f"{timestamp}_{to.replace('@', '_at_')}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_body)

    return {"id": f"stub_{timestamp}", "status": "logged", "path": str(html_path)}
