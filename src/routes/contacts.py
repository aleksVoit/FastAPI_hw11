from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, NotesContact
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post('/', response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.read_contacts(skip, limit, db)
    return contacts


@router.get('/search', response_model=List[ContactResponse])
async def search_contact(contact_info: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contact(contact_info, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contacts


@router.get('/birthdays', response_model=List[ContactResponse])
async def birthdays(period: int, db: Session = Depends(get_db)):
    contacts = await repository_contacts.birthdays(period, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.read_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.patch('/{contact_id}', response_model=ContactResponse)
async def add_note(contact_id: int, body: NotesContact, db: Session = Depends(get_db)):
    contact = await repository_contacts.add_note(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact
