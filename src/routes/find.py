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
    contact = await get_user_by_search_parameter(search_param, value, db, current_user)
    return contact


@find.get("/birthday_list")
async def get_birthday_list(shift: int = Query(0),
                            db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_birthday_list(shift, db)
    return contacts
