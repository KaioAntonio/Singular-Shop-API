from fastapi import APIRouter,  HTTPException
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
    if len(new_user.password) < 8:
        return {'error': 'password must be longer than 8 characters'}

    if new_user.password.islower():
        return {'error': 'password must have at least one capital letter'}

    if new_user.password.isalpha():
        return {'error': 'password need a number'}
    
    if new_user.password.isalnum():
        return {'error': 'password need a special character'}

    if user_exist:
        return {'error': 'email is already token'}

    elif new_user.email == "":
        return {'error': 'email can not be null'}
        
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
    user = User()
    return user.find_by_id_user(email)

@router.post('/v1/login/', tags=["Login"], description = "Autenticated Token")
def login(user: User):

    email = user.email
    password = user.password
    set_user = User.find_password(email)
    admin = User.find_admin(email)
    user = load_user(email)

    if not user:
        raise HTTPException(status_code=404, detail= 'User or Password invalid')

    elif Hasher.verify_password(password,set_user[0][0]) == False:
        raise HTTPException(status_code=404, detail= 'User or Password invalid')

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )

    return {'access_token': access_token, 'token_type': 'bearer', 'admin': admin}

@router.patch('/v1/avatar/', tags=["User"], description="Patch a new avatar")
def patch_avatar(user: User):
    new_avatar = user.patch_new_avatar(user.email,user.avatar)
    return {"message": "Update avatar with sucess!"}