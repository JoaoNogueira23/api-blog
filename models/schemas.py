from datetime import datetime, date
from pydantic import BaseModel, field_validator
from datetime import datetime
import re

class PostSchemaOut(BaseModel):
    postId: str
    rawText: str
    publishedDate: datetime
    ingestionDate: datetime
    author: str
    userId: str
    title: str
    subTitle: str
    imgUrlPost: str

    class Config:
        from_attributes = True

class UserSchemaOut(BaseModel):
    username: str
    birthdayDate: date
    usermail: str
    password: str
    userType: str

    class Config:
        from_attributes = True

    ### email format validate
    @field_validator('usermail')
    def email_validate(cls, value):
        if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise ValueError('Email format invalid')
        return value

class UserSchemaInfo(BaseModel):
    username: str
    birthdayDate: date
    usermail: str
    userType: str
    class Config:
        from_attributes = True

class UserSchemaLogin(BaseModel):
    usermail: str
    password: str

    ### email format validate
    @field_validator('usermail')
    def email_validate(cls, value):
        if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise ValueError('Email format invalid')
        return value

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserInDB(UserSchemaOut):
    hashed_password: str

