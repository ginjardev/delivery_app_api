from fastapi import APIRouter
from database import engine, SessionLocal
from schemas import SignUpModel
from models import User
from fastapi.exceptions import HTTPException
from fastapi import status
from werkzeug.security import generate_password_hash, check_password_hash


auth_route = APIRouter(
	prefix='/auth',
	tags=['auth']
)

session = SessionLocal(bind=engine)
@auth_route.get('/')
async def authenticate():
	return {"Auth Route": "Authenicate Pls"}


@auth_route.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        return HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail = "User with that email exits"
		)

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that username exits",
        )
    
    new_user = User(
          username = user.username,
          email = user.email,
          password = generate_password_hash(user.password),
          is_staff = user.is_staff,
          is_active = user.is_active
	)
    
    session.add(new_user)
    session.commit()
    
    return new_user

