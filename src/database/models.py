from sqlalchemy.types import Integer, String, DateTime, Date
from sqlalchemy import Column, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


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
