from typing import Optional

from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.services.auth import auth_service
from src.shemas import UserResponse
from src.repository import find as repository_contacts

find = APIRouter(prefix="/api/find", tags=['find'])


async def get_user_by_search_parameter(search_param: str, value: str, db: Session, current_user: User) -> Optional[
    UserResponse]:
    contact = None
    if search_param == "firstname":
        contact = await repository_contacts.get_user_by_firstname(value, db)
    elif search_param == "lastname":
        contact = await repository_contacts.get_user_by_lastname(value, db)
    elif search_param == "email":
        contact = await repository_contacts.get_user_by_email(value, db)
    elif search_param == "phone":
        contact = await repository_contacts.get_user_by_phone(value, db)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@find.get("/{search_param}")
async def search_contact(search_param: str, value: str = Query(..., min_length=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The search_contact function searches for a contact by either their username or email.
        The search_param parameter is the field to be searched, and value is the value of that field.
        If no user with that username or email exists, an HTTP 404 error will be returned.

    :param search_param: str: Specify the search parameter (e
    :param value: str: Specify the value of the search parameter
    :param min_length: Specify the minimum length of the value parameter
    :param db: Session: Get the database session
    :param current_user: User: Get the user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await get_user_by_search_parameter(search_param, value, db, current_user)
    return contact


@find.get("/birthday_list")
async def get_birthday_list(shift: int = Query(0),
                            db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_birthday_list function returns a list of contacts with birthdays in the next 7 days.
    The shift parameter allows you to specify how many days ahead or behind you want to look for birthdays.
    For example, if shift is set to 1, then it will return all contacts with birthdays tomorrow.

    :param shift: int: Determine the shift of birthdays to be returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of contacts who have a birthday in the next 30 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_birthday_list(shift, db)
    return contacts
