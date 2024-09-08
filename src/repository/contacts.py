from typing import List, Type
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse, NotesContact
from datetime import date, timedelta


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def read_contacts(skip: int, limit: int, db: Session) -> list[Type[Contact]]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def read_contact(contact_id: int, db: Session) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def search_contact(info: str, db: Session) -> list[Type[Contact]] | None:
    contacts_fn = db.query(Contact).filter(Contact.first_name == info).all()
    contacts_ln = db.query(Contact).filter(Contact.last_name == info).all()
    contacts_email = db.query(Contact).filter(Contact.email == info).all()
    contacts = contacts_fn + contacts_ln + contacts_email
    return list(set(contacts))


async def birthdays(period: int, db: Session) -> list[Type[Contact]] | None:
    today = date.today()
    delta = timedelta(days=period)
    end_of_period = today + delta
    contacts = db.query(Contact).all()
    birthdays_list = list()
    for contact in contacts:
        if contact.birthday.month >= today.month and contact.birthday.day >= today.day:
            contact_next_birthday = date(year=today.year, month=contact.birthday.month, day=contact.birthday.day)
        else:
            contact_next_birthday = date(year=today.year + 1, month=contact.birthday.month, day=contact.birthday.day)
        if today <= contact_next_birthday <= end_of_period:
            birthdays_list.append(contact)
    return birthdays_list


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def add_note(contact_id: int, body: NotesContact, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.notes = body.notes
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
