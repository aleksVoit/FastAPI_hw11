from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, NotesContact, UserModel
from src.repository import contacts as repository_contacts
from src.database.models import User
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post('/', response_model=ContactResponse,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel,
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    Creates new contact for specific user.

    :param body: Contact object.
    :type body: ContactModel
    :param current_user: current user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A list of notes.
    :rtype: Contact
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.get('/', response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100,
                        current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    """
    Retrieves required number of contacts for specific user with specific pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param current_user: current user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A list of notes.
    :rtype: Contact
    """
    contacts = await repository_contacts.read_contacts(skip, limit, current_user, db)
    return contacts


@router.get('/search', response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contact(contact_info: str,
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    Retrieves the contacts with corresponding info.

    :param contact_info: The information about contact to search for.
    :type contact_info: int
    :param current_user: current user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A list of notes.
    :rtype: Contact
    """
    contacts = await repository_contacts.search_contact(contact_info, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contacts


@router.get('/birthdays', response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def birthdays(period: int,
                    current_user: User = Depends(auth_service.get_current_user),
                    db: Session = Depends(get_db)):
    """
    Retrieves the contacts with birthdays in corresponding period.

    :param period: The number of days to be checked.
    :type period: int
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: Contact
    """
    contacts = await repository_contacts.birthdays(period, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: ID of specific contact.
    :type contact_id: int
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: Contact
    """
    contact = await repository_contacts.read_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.put('/{contact_id}', response_model=ContactResponse,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(contact_id: int, body: ContactModel,
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: ID of specific contact.
    :type contact_id: int
    :param body: The new data for contact.
    :type body: ContactModel
    :param current_user: The user to be updated.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Updated contact.
    :rtype: Contact
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.patch('/{contact_id}', response_model=ContactResponse,
              description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def add_note(contact_id: int, body: NotesContact,
                   current_user: User = Depends(auth_service.get_current_user),
                   db: Session = Depends(get_db)):
    """
    Adding a note to specific contact.

    :param contact_id: ID of specific contact.
    :type contact_id: int
    :param body: The note to be added.
    :type body: NotesContact
    :param current_user: The user to be added the note.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Updated contact.
    :rtype: Contact
    """
    contact = await repository_contacts.add_note(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse,
               description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int,
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    Removing of specific contact.

    :param contact_id: ID of specific contact to be removed.
    :type contact_id: int
    :param current_user: The user to be removed.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Updated contact.
    :rtype: Contact
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact
