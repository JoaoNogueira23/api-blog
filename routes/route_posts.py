from fastapi import APIRouter, status, Depends, HTTPException
from faker import Faker
from controllers.connection import DBConn
from models.schemas import Post, Base, User, PostSchemaOut
from datetime import datetime
from sqlalchemy import select
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.ext.asyncio import AsyncSession


faker = Faker()
db = DBConn()

router_posts = APIRouter(prefix='/posts')

@router_posts.get('/get-posts', response_model=LimitOffsetPage[PostSchemaOut])
async def get_posts(db_session: AsyncSession = Depends(db.get_session)):
    try:
        posts_query = select(Post)
        result = await db_session.execute(posts_query)
        posts = result.scalars().all()
        return paginate(posts)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db._engine:
            await db.close()
@router_posts.get('/populate-data', status_code=status.HTTP_201_CREATED)
async def populate_data():
    try:
        # Obtenção da sessão de forma assíncrona
        async with db.get_session() as session:

            # Manipulação do esquema usando uma conexão síncrona
            async with db._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

            # Criando usuários fictícios primeiro
            users = [
                User(
                    userId=faker.uuid4(),
                    name=faker.name(),
                    birthdayDate=faker.date_of_birth(),
                    email=faker.email(),
                    password=faker.password(),
                    userType="standard"
                ) for _ in range(50)  # Criando 50 usuários fictícios
            ]


            # Adicionando usuários ao banco de dados
            session.add_all(users)
            await session.commit()

            # Criando posts após usuários
            posts = [
                Post(
                    postId=faker.uuid4(),
                    rawText=faker.text(),
                    publishedDate=faker.date_time_this_year(tzinfo=None),
                    ingestionDate=datetime.now(),
                    author=faker.name(),
                    userId=users[i].userId,  # Associando posts a usuários existentes
                    title=faker.sentence(),
                    subTitle=faker.sentence(),
                    imgUrlPost=faker.image_url()
                ) for i in range(50)  # Criando 50 posts fictícios
            ]

            session.add_all(posts)
            await session.commit()  # Commit assíncrono

        print("Base populada com sucesso")

        await db.close()  # Fechamento assíncrono da conexão

        return "Success"
    except Exception as err:
        print(err)
        return "Error"
    finally:
        if db._engine:
            await db.close()

