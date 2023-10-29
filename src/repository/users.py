import logging

from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserSchema


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
The get_user_by_email function takes in an email and a database session,
and returns the user with that email. If no such user exists, it returns None.

:param email: str: Filter the query by email
:param db: AsyncSession: Pass in the database session
:return: A user object
:doc-author: Trelent
"""
sq = select(User).filter_by(email=email)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    logging.info(user)
    return user


async def create_user(body: UserSchema, db: AsyncSession) -> User:
    """
The create_user function creates a new user in the database.

:param body: UserSchema: Validate the request body and create a userschema object
:param db: AsyncSession: Pass the database session to the function
:return: A user object
:doc-author: Trelent
"""
avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        logging.error(e)
    new_user = User(**body.model_dump(), avatar=avatar)  # User(username=username, email=email, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
The update_token function updates the refresh token for a user.

:param user: User: Identify the user
:param token: str | None: Specify that the token parameter can either be a string or none
:param db: AsyncSession: Pass in the database session
:return: None
:doc-author: Trelent
"""
user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
The confirmed_email function takes in an email and a database session,
and sets the confirmed field of the user with that email to True.


:param email: str: Specify the email address of the user to be confirmed
:param db: AsyncSession: Pass the database session into the function
:return: None
:doc-author: Trelent
"""
user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
The confirmed_email function takes in an email and a database session,
and sets the confirmed field of the user with that email to True.


:param email: str: Get the email of the user
:param db: AsyncSession: Pass in the database session to the function
:return: None
:doc-author: Trelent
"""
user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()
