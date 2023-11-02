from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date, timedelta
from typing import List, Any, Sequence

from src.database.models import Contact, User
from src.schemas import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
The get_contacts function returns a list of contacts for the user.

:param limit: int: Limit the number of contacts returned
:param offset: int: Skip the first n contacts
:param db: AsyncSession: Pass the database session to the function
:param user: User: Filter the contacts by user
:return: A list of contact objects
:doc-author: Trelent
"""


    sq = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
The get_contact function is used to retrieve a contact from the database.
    It takes in an integer representing the id of the contact, a database session, and a user object.
    The function then queries for that specific contact using its id and returns it.

:param contact_id: int: Specify the contact id
:param db: AsyncSession: Pass the database session to the function
:param user: User: Check if the user is authorized to access this contact
:return: The contact with the given id, or none if there is no such contact
:doc-author: Trelent
"""


    sq = select(Contact).filter_by(id=contact_id, user=user)
    contact_result = await db.execute(sq)
    contact = contact_result.scalar_one_or_none()
    return contact


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
The create_contact function creates a new contact in the database.

:param body: ContactSchema: Validate the data that is passed in
:param db: AsyncSession: Create a new database session
:param user: User: Get the user that is logged in
:return: A contact object
:doc-author: Trelent
"""


    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_info=body.additional_info,
        user=user
)
    if body.completed:
        contact.completed = body.completed
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User):
    """
The update_contact function updates a contact in the database.
    Args:
        contact_id (int): The id of the contact to update.
        body (ContactUpdateSchema): A schema containing all fields that can be updated for a given Contact object.

:param contact_id: int: Specify which contact to update
:param body: ContactUpdateSchema: Get the information from the body of the request
:param db: AsyncSession: Pass the database session to the function
:param user: User: Get the user from the token
:return: A contact object
:doc-author: Trelent
"""


    sq = select(Contact).filter_by(id=contact_id, user=user)
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


async def remove_contact(contact_id: int, db: AsyncSession, user: User):
    """
The remove_contact function removes a contact from the database.

:param contact_id: int: Specify the contact to be removed
:param db: AsyncSession: Pass the database session to the function
:param user: User: Check if the user is logged in
:return: The contact that was removed
:doc-author: Trelent
"""


    sq = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(search: str, db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    """
The search_contacts function searches the database for contacts that match a given search string.
The function takes in two arguments:
    - search: The string to be searched for. This can be any part of a contact's first name, last name, or email address.
    - db: A database session object used to execute queries against the database.

:param search: str: Search for a contact by first name, last name or email
:param db: AsyncSession: Pass the database session to the function
:return: A list of contacts
:doc-author: Trelent
"""


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
