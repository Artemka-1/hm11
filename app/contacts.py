

class ContactRepository:

    def __init__(self, session):
        self.session = session

    def get_contacts(self):
        return self.session.query().all()
from fastapi import APIRouter

router = APIRouter()
@router.get("/")
async def get_contacts():
    return []
