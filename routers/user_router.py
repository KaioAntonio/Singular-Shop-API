from fastapi import APIRouter, Depends
from models.user import *
from db.config import *
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET = 'G@LATIKA!MAT' 

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/v1/user", tags=["User"], description="Creates new user")
def create_user(new_user: User):
    user_exist = load_user(new_user.email)
    if user_exist:
        return {'error': 'email is already token'}
    else:
        new_user.insert_user(new_user.username,new_user.password,new_user.email,new_user.admin,new_user.avatar)
        return new_user

@router.get("/v1/user", tags=["User"], description= "Reads all users")
def get_all_users():
    user = User()
    return user.read_user()


@router.put("/v1/user", tags=["User"], description= "Update user")
def put_user(new_user: User):
    new_user.put_user(new_user.username, new_user.password, new_user.admin, new_user.avatar, new_user.email)
    return new_user

@router.delete("/v1/user/{email}", tags=["User"], description= "Delete user")
def delete_user(email: str):
    user = User()
    user.delete_user(email)
    print(user)
    return {"message": "user delete with sucess"}

@router.get("/v1/user/{email}", tags=["User"], description="Reads a user")
def get_user_by_email(email: str):
    user = User()
    return user.find_by_id_user(email)[0]

manager = LoginManager(SECRET, token_url='/auth/token')

def load_user(email: str):
    return get_user_by_email(email)

@router.post('/v1/login/', tags=["Login"], description = "Autenticated Token")
def login(user: User):

    email = user.username
    password = user.password
    set_user = User.find_password(email)
    admin = User.find_admin(email)
    user = load_user(email)

    if not user:
        return {'error': 'User or Password invalid'}

    elif Hasher.verify_password(password,set_user) == False:
        return {'error': 'User or Password invalid'}

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )

    return {'access_token': access_token, 'token_type': 'bearer', 'admin': admin}
