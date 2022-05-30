from fastapi import APIRouter,  HTTPException, Body
from models.user import *
from db.config import *
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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

@router.get("/v1/user", tags=["User"], description= "Reads all users",
     responses={
        200: {
            "description": "User requested",
            "content": {
                "application/json": {
                    "example": { "user_id": "42e8db92-e792-46fd-8344-b3cc4e49a49d",
                                "username": "example",
                                "password": "$2b$12$.32oFz6fGEYNHauOFnrrWuSInKwAoDksKoDWkVQNeDjuiozI8i8pO",
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
        return {"status": 422, "message": "validation error"}

@router.delete("/v1/user/{email}", tags=["User"], description= "Delete user by email", responses= responses_custom)
def delete_user(email: str):
    user_exist = load_user(email)
    if user_exist:
        user = User()
        user.delete_user(email)
        return {"status": 200, "message": "user delete with sucess"}
    else:
        return {"status": 422, "message": "validation error"}

@router.get("/v1/user/{email}", tags=["User"], description="Reads a user", responses= responses_custom)
def get_user_by_email(email: str):
    user_exist = load_user(email)
    if user_exist:
        user = User()
        return user.find_by_id_user(email)[0]
    else:
        return {"status": 422, "message": "validation error"}

manager = LoginManager(SECRET, token_url='/auth/token')

def load_user(email: str):
    user = User()
    return user.find_by_id_user(email)

@router.post('/v1/login/', tags=["Login"], description = "Autenticated Token", responses=responses_custom)
def login(user: User = Body(
        default={
            "email": "test@test.com",
            "password": "@test1234"
        }
    )):
    email = user.email
    password = user.password
    set_user = User.find_password(email)
    admin = User.find_admin(email)
    user = load_user(email)

    if not user:
        raise HTTPException(status_code=404, detail= 'Usuário ou senha inválido')

    elif Hasher.verify_password(password,set_user[0][0]) == False:
        raise HTTPException(status_code=404, detail= 'Usuário ou senha inválido')

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )

    return {'access_token': access_token, 'token_type': 'bearer', 'admin': admin}

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
        return {"status": 401, "message": "validation error"}