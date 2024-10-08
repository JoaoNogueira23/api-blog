from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from faker import Faker
from controllers.connection import DBConn
from models.models import Post, Base, User, Post
from models.schemas import PostSchemaOut, PostItem
from datetime import datetime
from sqlalchemy import select
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.orm import Session

import json
import base64
from datetime import datetime
from google.cloud import storage
from pathlib import Path
import os
from io import BytesIO
from uuid6 import uuid6
import pytz

# Definindo o timezone (Exemplo: America/Sao_Paulo)
timezone = pytz.timezone('America/Sao_Paulo')


faker = Faker()
db = DBConn()

router_posts = APIRouter(prefix='/posts')

bucket_name = "blog-content-s3"

# Função para fazer upload para o Google Cloud Storage
def upload_to_gcs(file: UploadFile, bucket_name: str, destination_blob_name: str):
    # Cria o cliente de storage
    storage_client = storage.Client()
    
    # Pega o bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Define o blob (o "arquivo" no Google Cloud Storage)
    blob = bucket.blob(destination_blob_name)
    
    # Lê o conteúdo do arquivo e faz upload
    blob.upload_from_file(file.file, content_type=file.content_type)

    # Retorna a URL pública do arquivo (se o bucket estiver público)
    return blob.public_url

@router_posts.get('/get-posts', response_model=LimitOffsetPage[PostSchemaOut])
async def get_posts(db_session: Session = Depends(db.get_session)):
    try:
        posts_query = select(Post)
        result = await db_session.execute(posts_query)
        posts = result.scalars().all()
        print(posts)
        return paginate(posts)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db._engine:
            await db.close()

@router_posts.post('/create-post', status_code=status.HTTP_201_CREATED)
async def create_post(item: PostItem , db_session: Session = Depends(db.get_session)):
    try:    
        #### data process
        new_uuid6 = uuid6()
        paragraphs_list = json.loads(item.paragraphs)

        image_data = base64.b64decode(item.image)

        print(f"imagem decodificada de {len(image_data)} bytes")

        # filename for image
        datenow = datetime.now().strftime("%Y%m%d")
        destination_blob_name = f"posts/{datenow}/{new_uuid6}.webp"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(base_dir, '..', 'variables-key', 'key_google_cloud.json')
        
        # config cloud storage
        storage_client = storage.Client.from_service_account_json(credentials_path)
    
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        image_file = BytesIO(image_data)
        image_file.seek(0)

        blob.upload_from_file(image_file, content_type="image/webp")
        # save post database
        ## config object query
        current_time = datetime.now(timezone)
        post_model = Post(
            postId=str(new_uuid6),
            rawText=';'.join(paragraphs_list),
            publishedDate=current_time,
            acthor=item.acthor,
            title=item.title,
            resume=item.resume,
        )

        ## insert database
        async with db_session as session:
            session.add(post_model)
            await session.commit()

        return JSONResponse(
            content={
                "message": "Post created with sucess!"
            },
            status_code=status.HTTP_201_CREATED
        )
    
    except Exception as err:
        print(err)
        return JSONResponse(
            content={
                "message": "Erro no upload da imagem"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
            
@router_posts.get('/populate-data', status_code=status.HTTP_201_CREATED)
async def populate_data():
    try:
        # Obtenção da sessão de forma assíncrona
        async for session in db.get_session():
            # Manipulação do esquema usando uma conexão síncrona
            async with db._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

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
