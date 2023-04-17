from datetime import date, datetime

from sqlalchemy.orm import Session
from src.database.models import User


async def get_user_by_firstname(firstname: str, db: Session):
    contact = db.query(User).filter_by(firstname=firstname).first()
    print(f"find : {contact}")
    return contact


async def get_user_by_lastname(lastname: str, db: Session):
    contact = db.query(User).filter_by(lastname=lastname).first()
    return contact


async def get_user_by_email(email: str, db: Session):
    contact = db.query(User).filter_by(email=email).first()
    return contact


async def get_user_by_phone(phone: str, db: Session):
    contact = db.query(User).filter_by(phone=phone).first()
    return contact


async def get_birthday_list(shift: int, db: Session):
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
