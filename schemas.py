from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "janedoe",
                "email": "janedoe@email.com",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "4435a8d738ff345c703508e84edd9092864a00806f28c62f5c912986c6e9e0b8"
    )


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2, 
                "pizza_size": "SMALL" 
                }
            }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"
    
    class Config:
        orm_mode= True
        schema_extra = {
            "example": {
                "order_status": "PENDING"
			}
		}
