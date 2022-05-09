from fastapi import APIRouter, Depends
from models.user import *
from db.config import *
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET = 'G@LATIKA!MAT' 

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login", tags=["login"], description="Creates new user")
def create_user(new_user: User):
    dict_user = new_user.insert_user(new_user.username,new_user.password,new_user.email,new_user.admin,new_user.avatar)
    if dict_user == None:
        return {'error': 'Email is already taken'}
    return new_user

@router.get("/login", tags=["login"], description= "Reads all users")
def get_all_users():
    user = User()
    return user.read_user()


@router.put("/login", tags=["login"], description= "Update user")
def put_user(new_user: User):
    new_user.put_user(new_user.username, new_user.password, new_user.admin, new_user.avatar, new_user.email)
    return new_user

@router.delete("/login", tags=["login"], description= "Delete user")
def delete_user(new_user: User):
    new_user.delete_user(new_user.email)
    return new_user

@router.get("/login/{email}", tags=["login"], description="Reads a user")
def get_user_by_id(email: str):
    user = User()
    return user.find_by_id_user(email)

manager = LoginManager(SECRET, token_url='/auth/token')

def load_user(email: str):
    return get_user_by_id(email)

@router.post('/auth/token', tags=["login"], description = "Autenticated Token")
def login(data: OAuth2PasswordRequestForm = Depends()):
    

    email = data.username
    password = data.password
    set_user = User.find_password(email)

    user = load_user(email)

    if not user:
        return {'error': 'User or Password invalid'}

    elif Hasher.verify_password(password,set_user) == False:
        return {'error': 'User or Password invalid'}

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
