from fastapi import FastAPI, APIRouter
from routes.route_posts import router_posts

app = FastAPI()

api = APIRouter(prefix='/api')

print("Rodando API")
## routes include
api.include_router(router_posts)

## incluindo rotas no app
app.include_router(api)