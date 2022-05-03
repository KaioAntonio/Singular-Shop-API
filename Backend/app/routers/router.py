from fastapi import APIRouter
from models.usuario import *
from db.config import *

router = APIRouter()

@router.post("/usuario", tags=["usuario"])
def set_user(user_id: str, username: str, senha: str, email: str, admin: bool, avatar:str):
    user = Usuario()
    user.inserir(user_id, username, senha, email, admin, avatar)
    return user

@router.get("/usuario", tags=["usuario"])
def get_all_users():
    user = Usuario()
    return user.consulta()

@router.put("/usuario/{user_id}", tags=["usuario"])
def put_user(user_id: str, username: str, senha: str, email: str, admin: bool, avatar:str):
    user = Usuario()
    user.alterar(user_id, username, senha, email, admin, avatar)
    return user

@router.delete("/usuario/{user_id}", tags=["usuario"])
def delete_user(user_id: str):
    user = Usuario()
    user.excluir(user_id)
    return "Deletado Com sucesso!"

@router.get("/usuario/{user_id}", tags=["usuario"])
def get_user_by_id(user_id: str):
    user = Usuario()
    return user.consulta_por_id(user_id)



