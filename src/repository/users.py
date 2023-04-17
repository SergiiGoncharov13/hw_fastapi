from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas import UserResponse, UserModel


async def get_users(db: Session):
    users = db.query(User).all()
    return users


async def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    return user


async def create(body: UserModel, db: Session):
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update(user_id: int, body: UserModel, db: Session):
    user = await get_user_by_id(user_id, db)
    if user:
        user.email = body.email
        db.commit()
    return user


async def remove(user_id: int, db: Session):
    user = await get_user_by_id(user_id, db)
    if user:
        db.delete(user)
        db.commit()
    return user
