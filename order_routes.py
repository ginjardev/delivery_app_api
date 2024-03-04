from fastapi import APIRouter

order_route = APIRouter(
	prefix='/order',
	tags=['order']
)

@order_route.get('/')
async def orders():
	return {'Order List': 'Orders'}