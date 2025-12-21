from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_SERVER=settings.mail_server,
    MAIL_PORT=settings.mail_port,
    MAIL_TLS=True,
    MAIL_SSL=False,
)

async def send_email(email: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
