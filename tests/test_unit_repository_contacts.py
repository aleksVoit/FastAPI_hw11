import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from datetime import date

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.database.models import Contact, User
from src.schemas import ContactModel, NotesContact, ContactResponse
from src.repository.contacts import (create_contact, read_contacts, read_contact, search_contact, birthdays,
                                     update_contact, add_note, remove_contact)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = MagicMock(contact_id=1, birthday=date(year=2000, month=9, day=1))

    async def test_create_contact(self):
        contact = ContactModel(first_name='first name', last_name='last name', email='tests@tests.com',
                               phone_number='1234567890', birthday=date(year=2001, month=1, day=1))
        self.session.query().filter().all.return_value = contact
        result = await create_contact(body=contact, user=self.user, db=self.session)

        self.assertEqual(result.first_name, contact.first_name)
        self.assertEqual(result.last_name, contact.last_name)
        self.assertEqual(result.email, contact.email)
        self.assertEqual(result.phone_number, contact.phone_number)
        self.assertEqual(result.birthday, contact.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_read_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await read_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_read_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await read_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_search_contact(self):
        contacts = [Contact(first_name='tests'), Contact(last_name='tests')]
        self.session.query().filter().all.return_value = contacts
        result = await search_contact(info='tests', user=self.user, db=self.session)
        self.assertEqual([contact.id for contact in result], [contact.id for contact in contacts])

    async def test_birthdays(self):
        contacts = [Contact(id=1, birthday=date(year=2000, month=9, day=30)),
                    Contact(id=2, birthday=date(year=2001, month=10, day=2))]
        self.session.query().filter().all.return_value = contacts
        result = await birthdays(period=7, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_update_contact(self):
        contact = Contact(first_name="test_f_n", last_name="test_l_n", email='tests@update.com', phone_number='123321',
                          birthday=date(year=2001, month=1, day=2), notes=['tests', 'note'])
        self.session.query().filter().first.return_value = contact
        body = ContactModel(first_name="test_f_n", last_name="test_l_n", email='tests@update.com', phone_number='123321',
                            birthday=date(year=2001, month=1, day=2), notes=['tests', 'note'])
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_add_note(self):
        notes = NotesContact(notes=["tests", "notes"])
        contact = Contact(notes=notes)
        self.session.query().filter().first.return_value = contact
        result = await add_note(contact_id=1, body=notes, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)


if __name__ == '__main__':
    unittest.main()

