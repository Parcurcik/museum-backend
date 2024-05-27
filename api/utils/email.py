from api.configuration.config import settings
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from smtplib import SMTP

from ssl import create_default_context


def send_mail():
    message = MIMEText('<h1>Привет, я музеум</h1>', "html")
    message["From"] = settings.EMAIL_USERNAME
    message["To"] = ''
    message["Subject"] = 'Ближайшие события'

    ctx = create_default_context()

    try:
        with SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            print(type(settings.EMAIL_HOST), type(settings.EMAIL_PORT))
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            print(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            print(type(settings.EMAIL_USERNAME), type(settings.EMAIL_PASSWORD))
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}
