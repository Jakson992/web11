from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import ContactSchema, ContactUpdateSchema
from src.repository import contacts
from src.database.db import get_db
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/contacts/")
async def get_contacts(limit: int = 10, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await contacts.get_contacts(limit, offset, db)


@router.get("/contacts/{contact_id}")
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    return await contacts.get_contact(contact_id, db)


@router.post("/contacts/")
async def create_contact(contact: ContactSchema, db: AsyncSession = Depends(get_db)):
    return await contacts.create_contact(contact, db)


@router.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: ContactUpdateSchema, db: AsyncSession = Depends(get_db)):
    return await contacts.update_contact(contact_id, contact, db)


@router.delete("/contacts/{contact_id}")
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    return await contacts.remove_contact(contact_id, db)


@router.get("/contacts/search/")
async def search_contacts(
        search: str = Query(..., description="Пошук за ім'ям, прізвищем або адресою електронної пошти"),
        db: AsyncSession = Depends(get_db)):
    return await contacts.search_contacts(search, db)


@router.get("/contacts/birthdays/")
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    today = datetime.today().date()
    next_seven_days = today + timedelta(days=7)

    return await contacts.get_upcoming_birthdays(today, next_seven_days, db)

#
# async def get_contacts(limit: int, offset: int, db: AsyncSession):
#     sq = select(Contact).offset(offset).limit(limit)
#     contacts = await db.execute(sq)
#     return contacts.scalars().all()
#
#
# async def get_contact(contact_id: int, db: AsyncSession):
#     sq = select(Contact.filter_by(id=contact_id)
#     contact = await db.execute(sq)
#     return contact.scalar_one_or_none()
#
#
# async def create_contact(body: ContactSchema, db: AsyncSession):
#     contact = Contact(title=body.title, description=body.description)
#     if body.completed:
#         contact.completed = body.completed
#     db.add(contact)
#     await db.commit()
#     await db.refresh(contact)
#     return contact
#
#
# async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
#     sq = select(Contact).filter_by(id=contact_id)
#     result = await db.execute(sq)
#     contact = result.scalar_one_or_none()
#     if contact:
#         contact.title = body.title
#         contact.description = body.description
#         contact.completed = body.completed
#         await db.commit()
#         await db.refresh(contact)
#     return contact
#
#
# async def remove_contact(contact_id: int, db: AsyncSession):
#     sq = select(Contact).filter_by(id=contact_id)
#     result = await db.execute(sq)
#     contact = result.scalar_one_or_none()
#     if contact:
#         await db.delete(contact)
#         await db.commit()
#     return contact