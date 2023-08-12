from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    sq = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(sq)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(title=body.title, description=body.description)
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
        contact.title = body.title
        contact.description = body.description
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