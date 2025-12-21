from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud
from .database import SessionLocal, engine, Base

from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.contacts.router import router as contacts_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(contacts_router)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API", version="1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(contact_in: schemas.ContactCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Contact).filter(models.Contact.email == contact_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_contact(db, contact_in)


@app.get("/contacts/", response_model=List[schemas.ContactOut])
def list_contacts(q: Optional[str] = Query(None, description="Search by first name, last name or email"),
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit, q=q)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, updates: schemas.ContactUpdate, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    data = updates.dict(exclude_unset=True)
    if "email" in data:
        other = db.query(models.Contact).filter(models.Contact.email == data["email"], models.Contact.id != contact_id).first()
        if other:
            raise HTTPException(status_code=400, detail="Email already in use by another contact")
    return crud.update_contact(db, contact, updates)


@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud.delete_contact(db, contact)
    return None


@app.get("/contacts/birthdays/", response_model=List[schemas.ContactOut])
def birthdays(days: int = Query(7, ge=1, le=365), db: Session = Depends(get_db)):
    return crud.upcoming_birthdays(db, days=days)


from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post("/forgot-password")
async def forgot(email: EmailStr):
    token = create_reset_token(email)
    link = f"http://localhost:8000/auth/reset/{token}"
    await send_email(email, "Reset password", link)

@router.post("/reset-password/{token}")
def reset(token: str, password: str):
    email = verify_reset_token(token)
    user.password = hash_pwd(password)
