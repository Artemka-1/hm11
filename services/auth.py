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

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(email=user.email, password=hash_pwd(user.password))
    db.add(new_user)
    db.commit()

    token = create_email_token(new_user.email)
    link = f"http://localhost:8000/auth/verify/{token}"
    await send_email(new_user.email, "Verify email", link)

    return {"msg": "Check your email"}
@router.get("/verify/{token}")
def verify(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    user = db.query(User).filter(User.email == email).first()
    user.is_verified = True
    db.commit()
    return {"msg": "Email verified"}
