from urllib import response
from fastapi import APIRouter, Depends,  HTTPException, Body, status
from pydantic import BaseModel
from requests import Session
from models.user import User
from utils.hasher import Hasher
from jose import JWTError, jwt
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import config

SECRET = 'G@LATIKA!MAT' 
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
responses_custom = {
        422: {
            "content": {
                "application/json": {
                    "example": {"status": 422, "message": "validation error"}
                }
            },
        },
        200: {
            "content": {
                "application/json": {
                    "example": {"status": 200, "message": "method sucess"}
                }
            },
        },
    }

class TokenData(BaseModel):
    email: str | None = None

@router.post("/v1/user", tags=["User"], description="Creates new user", responses= responses_custom)
def create_user(new_user: User):
    user_exist = load_user(new_user.email)
    if len(new_user.password) < 8:
        return {'error': 'Senha não pode ter menos que 8 caracteres'}

    if new_user.password.islower():
        return {'error': 'Senha precisa ter letra maiúscula'}

    if new_user.password.isalpha():
        return {'error': 'Senha precisa de um número'}
    
    if new_user.password.isalnum():
        return {'error': 'Senha precisa de um caracter especial'}

    if user_exist:
        return {'status': 422, 'error': 'Este e-mail já está sendo utilizado'}

    elif new_user.email == "":
        return {'status': 422, 'error': 'E-mail inválido'}
        
    else:
        new_user.insert_user(new_user.username,new_user.password,new_user.email,new_user.admin,new_user.avatar)
        return new_user

@router.get("/v1/users", tags=["User"], description= "Reads all users",
     responses={
        200: {
            "description": "User requested",
            "content": {
                "application/json": {
                    "example": { "user_id": "42e8db92-e792-46fd-8344-b3cc4e49a49d",
                                "username": os.getenv("username"),
                                "password": os.getenv("password", "p@ssword!"),
                                "email": "example@example.com",
                                "admin": "true",
                                "avatar": "https://static-wp-tor15-prd.torcedores.com/wp-content/uploads/2016/07/fa.png"
                                }
                }
            },
        },
    },)
def get_all_users():
    user = User()
    return user.read_user()

@router.put("/v1/user", tags=["User"], description= "Update user by email", responses=responses_custom)
def put_user(new_user: User):
    user_exist = load_user(new_user.email)
    if user_exist:
        new_user.put_user(new_user.username, new_user.password, new_user.admin, new_user.avatar, new_user.email)
        return {"status": 200, "message": "update sucess"}
    else:
        return {"status": 422, "message": "validation error on put"}

@router.delete("/v1/user/{email}", tags=["User"], description= "Delete user by email", responses= responses_custom)
def delete_user(email: str):
    user_exist = load_user(email)
    if user_exist:
        user = User()
        user.delete_user(email)
        return {"status": 200, "message": "user delete with sucess"}
    else:
        return {"status": 422, "message": "error on delete"}

@router.get("/v1/user/{email}", tags=["User"], description="Reads a user", responses= responses_custom)
def get_user_by_email(email: str):
    user_exist = load_user(email)
    if user_exist:
        user = User()
        return user.find_by_id_user(email)[0]
    else:
        return {"status": 422, "message": "validation error on get"}

manager = LoginManager(SECRET, token_url='/auth/token')

def load_user(email: str):
    user = User()
    return user.find_by_id_user(email)

@router.post('/v1/login/', tags=["Login"], description = "Autenticated Token", responses=responses_custom)
def login(user: User = Body(
        default={
            "email": "test@test.com",
            "password": os.getenv("password","p@ssword!" )
        }
    )):
    email = user.email
    password = user.password
    set_user = User.find_password(email)
    admin = User.find_admin(email)
    user = load_user(email)
    ERROR = HTTPException(status_code=404, detail= "Usuário ou Senha inválida!")

    if not user:
        raise ERROR

    elif Hasher.verify_password(password,set_user[0][0]) == False:
        raise ERROR

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )

    return {'access_token': access_token, 'token_type': 'bearer', 'admin': admin}

@router.get('/v1/user', tags=["Login"], description="User current", responses=responses_custom)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    
    try: 
        payload = jwt.decode(token, SECRET)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError: 
        raise credentials_exception
    user = User.get_current_user(email)
    if user is None:
        raise credentials_exception
    return user #Return username, email, admin and avatar

@router.patch('/v1/avatar/', tags=["User"], description="Patch a new avatar", responses=responses_custom)
def patch_avatar(user: User = Body(
    default={
            "email": "test@test.com",
            "avatar": "https://thumbs.dreamstime.com/b/imagem-do-avatar-perfil-no-fundo-cinzento-142213585.jpg",
        }
    )):
    user_exist = load_user(user.email)
    if user_exist:
        user.patch_new_avatar(user.email,user.avatar)
        return {"status": 200, "message": "Update avatar with sucess!"}
    else:
        return {"status": 401, "message": "error on patch"}