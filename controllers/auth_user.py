from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from decouple import config
from models.models import User as UserModel
from models.schemas import UserSchemaOut
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt 
from uuid6 import uuid6

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_TIME = config('ACCESS_TOKEN_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    async def user_register(self, user: UserSchemaOut):
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
        try:
            await self.db_session.add(user_model)
            await self.db_session.commit()
        except IntegrityError:
            ### error of user always register on database
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
        except Exception as err:
            ## generic error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Intern Error'
            )

    def user_login(self, user: UserSchemaOut, expires_in: int = 30):
        ## query for find user on database
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()

        ## user not found
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        ## user found but sent wrong credentials
        if not pwd_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        payload = {
            'sub': user.username,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        
        user_on_db = self.db_session.query(UserModel).filter_by(username=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )