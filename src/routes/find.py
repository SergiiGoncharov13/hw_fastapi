from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.shemas import UserResponse
from src. repository import find as repository_contacts

find = APIRouter(prefix="/api/find", tags=['find'])


@find.get("/firstname/{firstname}", response_model=UserResponse)
async def get_user_firstname(firstname: str = Path(), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_user_by_firstname(firstname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@find.get("/lastname/{lastname}", response_model=UserResponse)
async def get_user_lastname(lastname: str = Path(), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_user_by_lastname(lastname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@find.get("/email/{email}", response_model=UserResponse)
async def get_user_email(email: str = Path(), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_user_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@find.get("/phone/{phone}", response_model=UserResponse)
async def get_user_email(phone: str = Path(), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_user_by_phone(phone, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@find.get("/shift/{shift}", response_model=List[UserResponse])
async def get_birthday_list(shift: int, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_birthday_list(shift, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts
