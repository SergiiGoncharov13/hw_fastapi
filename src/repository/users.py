from typing import Type

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas import UserModel, GuestModel


async def get_users(db: Session):
    """
    The get_users function returns a list of all users in the database.


    :param db: Session: Pass in the database session
    :return: A list of users
    :doc-author: Trelent
    """
    users = db.query(User).all()
    return users


async def get_user_by_id(user_id: int, db: Session):
    """
    The get_user_by_id function takes in a user_id and db Session object,
    and returns the User object with that id. If no such user exists, it returns None.

    :param user_id: int: Specify the type of data that is expected to be passed into the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def get_user_by_email(email: str, db: Session):
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists, it returns None.

    :param email: str: Pass in the email address of the user we want to retrieve
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = db.query(User).filter_by(email=email).first()
    return user


async def create(body: UserModel, db: Session):
    """
    The create function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object to be created.
            db (Session): The SQLAlchemy session object used for querying the database.

    :param body: UserModel: Validate the body of the request
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update(user_id: int, body: UserModel, db: Session):
    """
    The update function updates a user in the database.
        Args:
            user_id (int): The id of the user to update.
            body (UserModel): The updated version of the UserModel object.

    :param user_id: int: Identify the user to be deleted
    :param body: UserModel: Get the user's email from the request body
    :param db: Session: Access the database
    :return: The updated user object
    :doc-author: Trelent
    """
    user = await get_user_by_id(user_id, db)
    if user:
        user.email = body.email
        db.commit()
    return user


async def remove(user_id: int, db: Session):
    """
    The remove function removes a user from the database.
        Args:
            user_id (int): The id of the user to remove.
            db (Session): A connection to the database.

    :param user_id: int: Specify the user id of the user to be removed
    :param db: Session: Pass the database session to the function
    :return: The user that was removed
    :doc-author: Trelent
    """
    user = await get_user_by_id(user_id, db)
    if user:
        db.delete(user)
        db.commit()
    return user


async def create_guest(body: GuestModel, db: Session):
    """
    The create_guest function creates a new guest in the database.

    :param body: GuestModel: Pass the data from the request body into this function
    :param db: Session: Create a connection to the database
    :return: A tuple containing the new guest object
    :doc-author: Trelent
    """
    g = Gravatar(body.email)

    new_guest = User(**body.dict(), avatar=g.get_image()),
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)


async def update_token(user: User, refresh_token, db: Session):
    """
    The update_token function updates the refresh token for a user in the database.
        Args:
            user (User): The User object to update.
            refresh_token (str): The new refresh token to store in the database.
            db (Session): A connection to our Postgres database.

    :param user: User: Pass in the user object
    :param refresh_token: Update the refresh_token in the database
    :param db: Session: Access the database
    :return: The user object
    :doc-author: Trelent
    """
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Specify the email address of the user to confirm
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> Type[User] | None:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that will be passed to the function
    :param db: Session: Pass the database session to the function
    :return: A user object if the update was successful
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
