from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import getenv

DATABASE_URL = getenv('DATABASE_URL', 'postgresql+asyncpg://admin:admin123@localhost:5432/db_agency')

class DBConn:
    def __init__(self):
        self._engine = None
        self._Session = None
    
    def init_db(self):
        self._engine = create_async_engine(DATABASE_URL)
        self._Session = sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self):
        try:
            if self._engine is None:
                self.init_db()
                print("Engine initialized")
            else:
                print("Engine already running")
            
            print('Sucess in get session')
            async with self._Session() as session:
                yield session  # Isso mantém a sessão ativa durante o uso da rota.

        except Exception as err:
            print(f"Error creating session: {err}")
        finally:
            self._Session.close_all()
            self._engine.dispose()

    async def close(self):
        print("Closing engine")
        if self._engine is None:
            raise ValueError("Database is not initialized")
        await self._engine.dispose()
