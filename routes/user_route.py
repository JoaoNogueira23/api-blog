from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from controllers.connection import DBConn
from models.schemas import UserSchemaOut, UserSchemaLogin
from models.models import User as UserModel
from sqlalchemy import select

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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

    print(user_on_db)
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
        async with db_session as session:
            async with db._engine.begin() as conn:

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
            detail='Intern Server Error | Register Router'
        )


@user_router.post('/login')
async def user_register(
    request_form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(db.get_session),
    expires_in=30
):
    try:
        ## read payload request
        user = UserSchemaLogin(
            usermail=request_form_user.username,
            password=request_form_user.password
        )

        print('input usermail:', user.usermail)

        ### query of find user
        print('vamos fazer a query')
        user_on_db = select(UserModel).filter_by(usermail=user.usermail)
        
        print(user_on_db)
        ## user not found
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found'
            )

        ## user found but sent wrong credentials
        if not pwd_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )


        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        payload = {
            'sub': user.usermail,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        ## fin token on database
        

        return JSONResponse(
            content=access_token,
            status_code=status.HTTP_200_OK
        )
    
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Intern Server Error | Login Route'
        )
