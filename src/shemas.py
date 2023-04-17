import datetime
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    firstname: str = Field(default='Unknown', min_length=1, max_length=50)
    lastname: str = Field(default='Unknown', min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(default='+380001234567', min_length=10, max_length=15)
    birthday: datetime.date = Field(default='2022-04-15')
    additional_info: str = Field(default='nothing yet', min_length=1, max_length=150)


class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: datetime.date
    additional_info: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
