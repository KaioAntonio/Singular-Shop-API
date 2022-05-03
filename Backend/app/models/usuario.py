from typing import List, Optional
from fastapi import Request
from pydantic import BaseModel, Field
from sqlalchemy import true
from db.config import *


class Config:
    host = "ec2-3-209-124-113.compute-1.amazonaws.com"
    user = "ojwyfpeihoevxu"
    password = "e632432f03a787d335c96ab0920e7156d808d8cea213ad94f93c95ae838cbec3"
    db = "dd9jdc6nipc3hh"

class Usuario(BaseModel):

    user_id: str = Field(None, alias="user_id")
    username: str = Field(None, alias="username")
    senha: str = Field(None, alias="password")
    email: str = Field(None, alias="email")
    admin: bool = Field(None, alias="admin")
    avatar: str = Field(None, alias= "avatar")

    def set_user(self, user_id, username, senha, email, admin, avatar):
        self.user_id = user_id
        self.username = username
        self.senha = senha
        self.email = email
        self.admin = admin
        self.avatar = avatar

    def insert_user(self, user_id, username, senha, email, admin, avatar):
        self.set_user( user_id, username, senha, email, admin, avatar)
        sql = f"INSERT INTO USUARIO (user_id, username, password,email,admin,avatar)"
        sql += f"VALUES ('{user_id}', '{username}', '{senha}','{email}','{admin}','{avatar}')"
        insert_db(sql)

    def read_user(self):
        sql = f"SELECT * FROM USUARIO;"
        resultado = read_db(sql)
        return resultado

    def put_user(self,  user_id, username, senha, email, admin, avatar):
        self.set_user( user_id, username, senha, email, admin, avatar)
        sql = f"UPDATE USUARIO "
        sql += f"SET username = '{username}',"
        sql += f" password = '{senha}',"
        sql += f" email = '{email}',"
        sql += f" admin = '{admin}',"
        sql += f" avatar = '{avatar}'"
        sql += f"WHERE user_id = '{user_id}'"
        insert_db(sql)

    def delete_user(self, user_id):
        sql = f"DELETE FROM USUARIO"
        sql += f" WHERE user_id = '{user_id}'"
        insert_db(sql)
    
    def find_by_id_user(self, user_id):
        sql = f"SELECT * FROM USUARIO WHERE user_id = '{user_id}'"
        resultado = read_db(sql)
        return resultado