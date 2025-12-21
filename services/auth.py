from itsdangerous import URLSafeTimedSerializer
from app.config import settings

serializer = URLSafeTimedSerializer(settings.secret_key)

def create_email_token(email: str):
    return serializer.dumps(email, salt="email-confirm")

def verify_email_token(token: str):
    return serializer.loads(token, salt="email-confirm", max_age=3600)

def create_reset_token(email: str):
    return serializer.dumps(email, salt="password-reset")

def verify_reset_token(token: str):
    return serializer.loads(token, salt="password-reset", max_age=3600)
