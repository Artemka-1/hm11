from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas import ContactCreate, ContactResponse
from app.models import Contact
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", status_code=201, response_model=ContactResponse)
def create_contact(
    body: ContactCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    contact = Contact(**body.dict(), owner_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get("/", response_model=list[ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Contact).filter(Contact.owner_id == user.id).all()
