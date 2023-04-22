import enum

from sqlalchemy.types import Integer, String, DateTime, Date
from sqlalchemy import Column, func, event, Enum
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    guest: str = 'guest'


class User(Base):
    __tablename__ = "users" # noqa
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(20), index=True)
    last_name = Column(String(30), index=True)
    email = Column(String(15), unique=True, index=True)
    tel_number = Column(Integer)
    birthday = Column(Date, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Guest(Base):
    __tablename__ = "guest"
    id = Column(Integer, primary_key=True)
    guest_name = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.guest)

