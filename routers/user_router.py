from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.user import *
from db.config import *
import jwt

router = APIRouter()


@router.post("/login", tags=["login"], description="Creates new user")
def create_user(username: str, password: str, email: str, admin: bool, avatar:str):
    user = User()
    user.insert_user(username, password, email, admin, avatar)
    return user

@router.get("/login", tags=["login"], description= "Reads all users")
def get_all_users():
    user = User()
    return user.read_user()

@router.put("/login/{user_id}", tags=["login"], description= "Update user")
def put_user(user_id: str, username: str, password: str, email: str, admin: bool, avatar:str):
    user = User()
    user.put_user(user_id, username, password, email, admin, avatar)
    return user

@router.delete("/login/{user_id}", tags=["login"], description= "Delete user")
def delete_user(user_id: str):
    user = User()
    user.delete_user(user_id)
    return "Deletado Com sucesso!"

@router.get("/login/{user_id}", tags=["login"], description="Reads a user")
def get_user_by_id(user_id: str):
    user = User()
    return user.find_by_id_user(user_id)
