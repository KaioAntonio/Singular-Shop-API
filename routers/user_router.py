from hashlib import new
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from models.user import *
from db.config import *
import jwt

router = APIRouter()


@router.post("/login", tags=["login"], description="Creates new user")
def create_user(new_user: User):
    new_user.insert_user(new_user.username,new_user.password,new_user.email,new_user.admin,new_user.avatar)
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

@router.get("/login/{user_id}", tags=["login"], description="Reads a user")
def get_user_by_id(user_id: str):
    user = User()
    return user.find_by_id_user(user_id)
