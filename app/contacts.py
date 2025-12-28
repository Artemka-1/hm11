

class ContactRepository:

    def __init__(self, session):
        self.session = session

    def get_contacts(self):
        return self.session.query().all()
