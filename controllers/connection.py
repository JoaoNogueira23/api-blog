from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = 'postgresql+asyncpg://admin123:admin@localhost:5432/db_agency'
class DBConn:
    def __init__(self):
        self._engine = None
        self._Session = None
    
    def init_db(self):
        self._engine = create_async_engine(DATABASE_URL)
        self._Session = sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self):
       self.init_db()
       async with self._Session() as session:
            try:
                yield session
            except Exception as err:
                # Aqui você pode adicionar qualquer lógica de limpeza ou logging
                print(f"Exception in get_session: {err}")
                raise HTTPException(status_code=500, detail="Database session error")
            finally:
                await self.close()

    async def close(self):
        print("Closing engine")
        if self._engine is None:
            raise ValueError("Database is not initialized")
        await self._engine.dispose()
