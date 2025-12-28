import unittest
from unittest.mock import MagicMock
from app.repository.contacts import ContactRepository

class TestContactRepository(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repo = ContactRepository(self.session)
      
    def test_get_contacts(self):
        self.session.query().all.return_value = []

        result = self.repo.get_contacts()

        self.assertEqual(result, [])
