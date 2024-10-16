from datetime import datetime, date
from pydantic import BaseModel, field_validator
from datetime import datetime
import re
from typing import List
from fastapi import UploadFile, File

class PostSchemaOut(BaseModel):
    postId: str
    rawText: str
    publishedDate: datetime
    acthor: str
    title: str
    resume: str
    urlImage: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @field_validator('publishedDate', mode='before')
    def parse_dade(cls,v):
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d %H:%M:%S")
        return v
    

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


class PostItem(BaseModel):
    title: str
    paragraphs: str
    resume: str
    acthor: str
    image: str


    class Config:
        from_attributes = True

