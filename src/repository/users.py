from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas import UserModel, GuestModel


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


async def create_guest(body: GuestModel, db: Session):
    g = Gravatar(body.email)

    new_guest = User(**body.dict(), avatar=g.get_image()),
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)


async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()
