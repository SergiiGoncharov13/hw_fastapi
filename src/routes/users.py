from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.shemas import UserResponse, UserModel


router = APIRouter(prefix="/users", tags=['user'])


@router.get("/", response_model=List[UserResponse], name="Users list")
async def get_users(db: Session = Depends(get_db)):
    users = await repository_users.get_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponse,)
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserModel, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')

    user = await repository_users.create(body, db)
    return user


@router.put("/{user_id}", response_model=UserResponse,)
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.update(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,)
async def remove_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.remove(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user
