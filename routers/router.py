from doctest import Example
from fastapi import APIRouter
from models.usuario import *
from db.config import *

router = APIRouter()

@router.post("/login", tags=["login"], description="Creates new user")
def set_user(user_id: str, username: str, senha: str, email: str, admin: bool, avatar:str):
    user = Usuario()
    user.insert_user(user_id, username, senha, email, admin, avatar)
    return user

@router.get("/login", tags=["login"], description= "Reads all users")
def get_all_users():
    user = Usuario()
    return user.read_user()

@router.put("/login/{user_id}", tags=["login"], description= "Update user")
def put_user(user_id: str, username: str, senha: str, email: str, admin: bool, avatar:str):
    user = Usuario()
    user.put_user(user_id, username, senha, email, admin, avatar)
    return user

@router.delete("/login/{user_id}", tags=["login"], description= "Delete user")
def delete_user(user_id: str):
    user = Usuario()
    user.delete_user(user_id)
    return "Deletado Com sucesso!"

@router.get("/login/{user_id}", tags=["login"], description="Reads a user")
def get_user_by_id(user_id: str):
    user = Usuario()
    return user.find_by_id_user(user_id)



