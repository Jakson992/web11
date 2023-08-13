from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date, timedelta
from typing import List, Any, Sequence

from src.database.models import Contact
from src.schemas import ContactSchema, ContactUpdateSchema



async def get_contacts(limit: int, offset: int, db: AsyncSession):
    sq = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    contact_result = await db.execute(sq)
    contact = contact_result.scalar_one_or_none()
    return contact


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_info=body.additional_info
    )
    if body.completed:
        contact.completed = body.completed
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()

    if contact:
        if body.first_name is not None:
            contact.first_name = body.first_name
        if body.last_name is not None:
            contact.last_name = body.last_name
        if body.email is not None:
            contact.email = body.email
        if body.phone_number is not None:
            contact.phone_number = body.phone_number
        if body.birthday is not None:
            contact.birthday = body.birthday
        if body.additional_info is not None:
            contact.additional_info = body.additional_info
        if body.completed is not None:
            contact.completed = body.completed

        await db.commit()
        await db.refresh(contact)

    return contact


async def remove_contact(contact_id: int, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact



async def search_contacts(search: str, db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    stmt = select(Contact).filter(
        (Contact.first_name.ilike(f'%{search}%')) |
        (Contact.last_name.ilike(f'%{search}%')) |
        (Contact.email.ilike(f'%{search}%'))
    )
    result = await db.execute(stmt)
    return result.scalars().all()



async def get_upcoming_birthdays(start_date: date, end_date: date, db: AsyncSession) -> Sequence[
    Row | RowMapping | Any]:
    stmt = select(Contact).filter(
        func.extract('month', Contact.birthday) == start_date.month,
        func.extract('day', Contact.birthday) >= start_date.day,
        func.extract('day', Contact.birthday) <= end_date.day
    )
    result = await db.execute(stmt)
    return result.scalars().all()


# async def get_upcoming_birthdays_for_next_week(db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
#     today = date.today()
#     next_week = today + timedelta(days=7)
#     return await get_upcoming_birthdays(today, next_week, db)
