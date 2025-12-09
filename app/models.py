from sqlalchemy import Column, Integer, String, Date, Text
from .database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(120), nullable=False, index=True)
    last_name = Column(String(120), nullable=False, index=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    birthday = Column(Date, nullable=False)
    additional = Column(Text, nullable=True)
