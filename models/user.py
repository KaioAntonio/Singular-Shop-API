from uuid import uuid4
from pydantic import BaseModel, Field
from db.config import *
from passlib.context import CryptContext
from hasher import *

class User(BaseModel):

    username: str = Field(None, alias="username")
    password: str = Field(None, alias="password")
    email: str = Field(None, alias="email")
    admin: str = Field(None, alias="admin")
    avatar: str = Field(None, alias= "avatar")

    def set_user(self, username, password, email, admin, avatar):
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin
        self.avatar = avatar

    def insert_user(self, username, password, email, admin, avatar):
        self.set_user(username, password, email, admin, avatar)
        sql = f"INSERT INTO USUARIO (user_id, username, password,email,admin,avatar)"
        sql += f"VALUES ('{str(uuid4())}', '{username}', '{str(Hasher.get_password_hash(password))}','{email}','{admin}','{avatar}')"
        insert_db(sql)

    def read_user(self):
        sql = f"SELECT * FROM USUARIO;"
        resultado = read_db(sql)
        return resultado

    def put_user(self,  user_id, username, password, email, admin, avatar):
        self.set_user( user_id, username, password, email, admin, avatar)
        sql = f"UPDATE USUARIO "
        sql += f"SET username = '{username}',"
        sql += f" password = '{password}',"
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