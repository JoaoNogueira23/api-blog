from fastapi import APIRouter
from faker import Faker
from controllers.connection import DBConn
from models.schemas import Post, Base, User
from datetime import datetime

faker = Faker()
db = DBConn()

router_posts = APIRouter(prefix='/posts')

@router_posts.get('/get-posts')
async def get_posts():
    return 'Rota de posts'

@router_posts.get('/populate-data')
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
        if db._engine:
            await db.close()
        print(err)

        return "Error"
