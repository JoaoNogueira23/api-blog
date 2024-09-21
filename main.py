from fastapi import FastAPI, APIRouter
from routes.route_posts import router_posts
from routes.user_route import user_router
from fastapi_pagination import add_pagination

app = FastAPI()

api = APIRouter(prefix='/api')


## routes include
api.include_router(router_posts)
api.include_router(user_router)

## incluindo rotas no app
app.include_router(api)

add_pagination(app)