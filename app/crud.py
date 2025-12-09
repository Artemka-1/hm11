from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date, timedelta, datetime
from . import models, schemas
from typing import List, Optional

def create_contact(db: Session, contact_in: schemas.ContactCreate) -> models.Contact:
    contact = models.Contact(**contact_in.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def get_contact(db: Session, contact_id: int) -> Optional[models.Contact]:
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100, q: Optional[str] = None) -> List[models.Contact]:
    query = db.query(models.Contact)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            models.Contact.first_name.ilike(like),
            models.Contact.last_name.ilike(like),
            models.Contact.email.ilike(like)
        ))
    return query.order_by(models.Contact.last_name, models.Contact.first_name).offset(skip).limit(limit).all()

def update_contact(db: Session, contact: models.Contact, updates: schemas.ContactUpdate) -> models.Contact:
    data = updates.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(contact, field, value)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def delete_contact(db: Session, contact: models.Contact) -> None:
    db.delete(contact)
    db.commit()

def upcoming_birthdays(db: Session, days: int = 7) -> List[models.Contact]:
    today = date.today()
    end = today + timedelta(days=days)

    contacts = db.query(models.Contact).all()
    result = []

    def next_occurrence(bday: date) -> date:
        # bday is the stored birthdate (with year)
        month = bday.month
        day = bday.day
        year = today.year
        try:
            candidate = date(year, month, day)
        except ValueError:
            # e.g., Feb 29 on non-leap year -> map to Feb 28
            candidate = date(year, 2, 28)
        if candidate < today:
            # next occurrence will be next year
            try:
                candidate = date(year + 1, month, day)
            except ValueError:
                candidate = date(year + 1, 2, 28)
        return candidate

    for c in contacts:
        occ = next_occurrence(c.birthday)
        if today <= occ <= end:
            result.append(c)

    result.sort(key=lambda c: (next_occurrence(c.birthday) - today).days)
    return result
