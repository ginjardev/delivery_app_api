from fastapi import APIRouter,status, Depends
from database import engine, SessionLocal
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder


auth_route = APIRouter(
	prefix='/auth',
	tags=['auth']
)

session = SessionLocal(bind=engine)

#defaul auth route
@auth_route.get('/')
async def home(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token")
    
    return {"Home": "Hello World!"}


#signup route
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

# login route 
@auth_route.post('/login', status_code=200)
async def login(user: LoginModel, Authorize:AuthJWT=Depends()):
     db_user = session.query(User).filter(User.username == user.username).first()
     if db_user and check_password_hash(db_user.password, user.password):
          access_token = Authorize.create_access_token(subject=db_user.username)
          refresh_token = Authorize.create_refresh_token(subject=db_user.username)

          response = {
               "access": access_token,
               "refresh": refresh_token
          }
          return jsonable_encoder(response)
     raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Invalid username or password"
          )


# refresh token route
@auth_route.get('/refresh')
async def refresh(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access token": access_token})