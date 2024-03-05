from fastapi import FastAPI
from auth_routes import auth_route
from order_routes import order_route
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
	return Settings()

app.include_router(auth_route)
app.include_router(order_route)
