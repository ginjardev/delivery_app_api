from fastapi import APIRouter

auth_route = APIRouter(
	prefix='/auth',
	tags=['auth']
)

@auth_route.get('/')
async def authenticate():
	return {"Auth Route": "Authenicate Pls"}