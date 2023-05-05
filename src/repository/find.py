from datetime import date, datetime

from sqlalchemy.orm import Session
from src.database.models import User


async def get_user_by_firstname(firstname: str, db: Session):
    """
    The get_user_by_firstname function returns a user by firstname.
        Args:
            firstname (str): The name of the user to find.

    :param firstname: str: Define the type of parameter that will be passed into the function
    :param db: Session: Pass the database session to the function
    :return: The first contact in the database whose firstname matches the given name
    :doc-author: Trelent
    """
    contact = db.query(User).filter_by(firstname=firstname).first()
    print(f"find : {contact}")
    return contact


async def get_user_by_lastname(lastname: str, db: Session):
    """
    The get_user_by_lastname function takes a lastname and returns the user with that lastname.

    :param lastname: str: Specify the lastname of the user we want to retrieve
    :param db: Session: Pass the database session to the function
    :return: The first user with the given lastname
    :doc-author: Trelent
    """
    contact = db.query(User).filter_by(lastname=lastname).first()
    return contact


async def get_user_by_email(email: str, db: Session):
    """
    The get_user_by_email function takes in an email address and a database session.
    It then queries the database for a user with that email address, returning the first result if it exists.

    :param email: str: Pass in the email of the user we want to get
    :param db: Session: Pass the database session to the function
    :return: A user object from the database
    :doc-author: Trelent
    """
    contact = db.query(User).filter_by(email=email).first()
    return contact


async def get_user_by_phone(phone: str, db: Session):
    """
    The get_user_by_phone function takes a phone number and returns the user associated with that phone number.
        Args:
            phone (str): The user's phone number.
            db (Session): A database session object to query for the user.

    :param phone: str: Pass the phone number of the user to be retrieved
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    contact = db.query(User).filter_by(phone=phone).first()
    return contact


async def get_birthday_list(shift: int, db: Session):
    """
    The get_birthday_list function takes in a shift value and a database connection.
    It then returns all contacts whose birthday is within the next 'shift' days.

    :param shift: int: Set the range of days in which to look for birthdays
    :param db: Session: Access the database
    :return: A list of contacts whose birthday is within the next 7 days
    :doc-author: Trelent
    """
    contacts = []
    all_contacts = db.query(User).all()
    today = date.today()
    for contact in all_contacts:
        birthday = contact.birthday
        evaluated_date = (datetime(today.year, birthday.month, birthday.day).date() - today).days
        if evaluated_date < 0:
            evaluated_date = (datetime(today.year + 1, birthday.month, birthday.day).date() - today).days
        if evaluated_date <= shift:
            contacts.append(contact)
    return contacts
