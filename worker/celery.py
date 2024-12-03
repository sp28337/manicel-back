import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from app.settings import Settings


settings = Settings()

celery = Celery(__name__)

celery.conf.broker_url = settings.CELERY_REDIS_URL
celery.conf.result_backend = settings.CELERY_REDIS_URL


@celery.task(name="send_email_task")
def send_emal_task(subject: str, text: str, to: str) -> None:
    msg = _build_message(subject=subject, text=text, to=to)
    _send_email(msg=msg)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    msg = MIMEMultipart()

    msg["from"] = settings.SMTP_FROM_EMAIL
    msg["to"] = to
    msg["subject"] = subject

    msg.attach(MIMEText(text, "plain"))
    return msg


def _send_email(msg: MIMEMultipart) -> None:
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context)
    server.login(settings.SMTP_FROM_EMAIL, settings.SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()
