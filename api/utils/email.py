import smtplib

from api.configuration.config import settings
from email.mime.text import MIMEText


def send_mail(emails: list, template: str):
    message = MIMEText(template, "html")
    message["Subject"] = 'Ближайшие события'
    message["From"] = settings.SMTP_SENDER
    message["To"] = ', '.join(emails)

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(
            settings.SMTP_SENDER, emails, message.as_string()
        )
        server.quit()
        return {"status": 200, "result": 'Success sent mails!'}
    except Exception as e:
        return {"status": 500, "errors": e}
