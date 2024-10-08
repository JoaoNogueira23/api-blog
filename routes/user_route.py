from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import LimitOffsetPage, paginate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_pagination.ext.sqlalchemy import paginate as slqalchemy_paginate

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.connection import DBConn
from models.schemas import UserSchemaOut, UserSchemaLogin, UserSchemaInfo
from models.models import User as UserModel

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from uuid6 import uuid6
from jose import JWTError, jwt
from decouple import config

db = DBConn()
user_router = APIRouter(prefix='/user')

### config of pwt token
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_TIME = config('ACCESS_TOKEN_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_token(access_token):
    try:
        data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid access token'
        )
    
    user_on_db = select.query(UserModel).filter_by(username=data['sub']).first()

    if user_on_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid access token'
        )

@user_router.post('/register')
async def user_register(
    user: UserSchemaOut,
    db_session: Session = Depends(db.get_session),
):
    try:
        new_uuid6 = uuid6()

        birthdayDateStr = user.birthdayDate.strftime('%Y-%m-%d')

        user_model = UserModel(
            username=user.username,
            password=pwd_context.hash(user.password),
            usermail=user.usermail,
            userId=str(new_uuid6),
            birthdayDate= datetime.strptime(birthdayDateStr, '%Y-%m-%d'),
            userType=user.userType
        )

        async with db_session as session:
            session.add(user_model)
            await session.commit()

            return JSONResponse(
                content={'message': 'User registered successfully'},
                status_code=status.HTTP_201_CREATED
            )
        
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Intern Server Error'
        )


@user_router.post('/login')
async def user_login(
    request_form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(db.get_session),
):
    try:
        ## read payload request
        user = UserSchemaLogin(
            usermail=request_form_user.username,
            password=request_form_user.password
        )

        ## object query for request
        user_on_db = select(UserModel).filter_by(usermail=user.usermail)

        ## request ('raw sql')
        result = await db_session.execute(user_on_db)
        user_result = result.scalars().first()

        ## user not found
        if user_result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )

    
        ## user found but sent wrong credentials
        if not pwd_context.verify(user.password, user_result.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )

        ## token validation
        exp = datetime.now(timezone.utc) + timedelta(minutes=30)
        payload = {
            'user_id': user_result.userId,
            'exp': exp
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


        ## fin token on database
        return JSONResponse(
            content={
                "message": "Login successfully",
                "data": {
                    "username": user_result.username,
                    "userType": user_result.userType,
                    "token": token
                }
            },
            status_code=status.HTTP_200_OK
        )
    
    except HTTPException as err:
        return JSONResponse(
            content={
                "message": err.detail
            },
            status_code=err.status_code
        )
    
    finally:
        await db_session.close()
