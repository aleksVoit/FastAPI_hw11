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
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.get('/', response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100,
                        current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    contacts = await repository_contacts.read_contacts(skip, limit, current_user, db)
    return contacts


@router.get('/search', response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contact(contact_info: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contact(contact_info, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contacts


@router.get('/birthdays', response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def birthdays(period: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.birthdays(period, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
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
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact
