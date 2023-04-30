from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.repository import users as repository_users
from src.shemas import UserResponse, UserModel
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/users", tags=['user'])

allowed_operation_get = RoleAccess([Role.guest, Role.admin, Role.moderator])
allowed_operation_create = RoleAccess([Role.guest, Role.admin, Role.moderator])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/", response_model=List[UserResponse], name="Users list",
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_users(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_user(body: UserModel, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')

    user = await repository_users.create(body, db)
    return user


@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.update(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def remove_user(user_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.remove(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user
