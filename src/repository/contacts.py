from typing import List, Type
from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse, NotesContact
from datetime import date, timedelta


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:

    """
    Creates contact for specific user.

    :param body: Contact object.
    :type body: ContactModel
    :param user: User object.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of notes.
    :rtype: Contact
    """

    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        user=user
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def read_contacts(skip: int, limit: int, user: User, db: Session) -> list[Type[Contact]]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def read_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: ID of specific contact.
    :type contact_id: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()


async def search_contact(info: str, user: User, db: Session) -> list[Type[Contact]] | None:
    """
    Retrieves the contacts with corresponding information.

    :param info: The information about contact to search for.
    :type info: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact] | None
    """
    contacts_fn = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.first_name == info)).all()
    contacts_ln = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.last_name == info)).all()
    contacts_email = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.email == info)).all()
    contacts = contacts_fn + contacts_ln + contacts_email
    return list(set(contacts))


async def birthdays(period: int, user: User, db: Session) -> list[Type[Contact]]:
    """
    Retrieves the contacts with birthdays in corresponding period.

    :param period: The number of days to be checked.
    :type period: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact] | None
    """
    today = date.today()
    delta = timedelta(days=period)
    end_of_period = today + delta
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    birthdays_list = list()
    for contact in contacts:
        contact_next_birthday = date(year=today.year, month=contact.birthday.month, day=contact.birthday.day)
        if contact_next_birthday < today:
            contact_next_birthday = date(year=today.year + 1, month=contact.birthday.month, day=contact.birthday.day)

        # if contact.birthday.month >= today.month and contact.birthday.day >= today.day:
        #
        # else:
        #     contact_next_birthday = date(year=today.year + 1, month=contact.birthday.month, day=contact.birthday.day)
        if today <= contact_next_birthday <= end_of_period:
            birthdays_list.append(contact)
    return birthdays_list


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: ID of specific contact.
    :type contact_id: int
    :param body: The new data for contact.
    :type body: ContactModel
    :param user: The user to be updated.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: Updated contact.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def add_note(contact_id: int, body: NotesContact, user: User, db: Session) -> Contact | None:
    """
    Adding a note to specific contact.

    :param contact_id: ID of specific contact.
    :type contact_id: int
    :param body: The note to be added.
    :type body: NotesContact
    :param user: The user to be added the note.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: Updated contact.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        contact.notes = body.notes
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removing of specific contact.

    :param contact_id: ID of specific contact to be removed.
    :type contact_id: int
    :param user: The user to be removed.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: Updated contact.
    :rtype: Contact | None
    """

    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
