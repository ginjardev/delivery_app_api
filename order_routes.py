from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel
from database import SessionLocal, engine
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

order_route = APIRouter(prefix="/orders", tags=["orders"])

session = SessionLocal(bind=engine)


@order_route.get("/")
async def order_home(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"Order List": "Orders"}


@order_route.post("/order", status_code=status.HTTP_201_CREATED)
async def place_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    new_order = Order(pizza_size=order.pizza_size, quantity=order.quantity)
    new_order.user = user
    session.add(new_order)
    session.commit()

    response = {
        "id": new_order.id,
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "order status": new_order.order_status,
    }

    return jsonable_encoder(response)


@order_route.get("/orders")
async def list_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="You're not a superuser"
    )


@order_route.get('/orders/{id}')
async def get_order_by_id(id:int, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="invalid token"
        )
    current_user = Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.username==current_user).first()
    if user.is_staff:
        order = session.query(Order).filter(Order.id==id).first()
        return jsonable_encoder(order)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detaail="You're not a superuser to fetch this data"
	)


@order_route.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    current_user = Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.username==current_user).first()
    
    return jsonable_encoder(user.orders)


@order_route.get('/user/order/{id}')
async def get_specific_order(id: int, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
		)
    current_user = Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.username==current_user).first()
    
    orders = user.orders
    
    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with that id"
	)


@order_route.put('/order/update/{id}')
async def update_order(id:int, order:OrderModel, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
		)
    
    update_order=session.query(Order).filter(Order.id == id).first()
    
    update_order.quantity = order.quantity
    update_order.pizza_size = order.pizza_size
    
    session.commit()
    
    return jsonable_encoder(update_order)
