from uuid import uuid4
from pydantic import BaseModel, Field
from db.config import read_db,insert_db, read_db_user_necessary,read_password
from models.cart import Cart
from utils.hasher import Hasher

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
        Cart.create_cart(email)
        insert_db(sql)

    def read_user(self):
        sql = f"SELECT * FROM USUARIO;"
        result = read_db(sql)
        return result

    def put_user(self, username, password, admin, avatar, email):
        self.set_user(username, password, admin, avatar, email)
        sql = f"UPDATE USUARIO "
        sql += f"SET username = '{username}',"
        sql += f" password = '{password}',"
        sql += f" admin = '{admin}',"
        sql += f" avatar = '{avatar}'"
        sql += f"WHERE email = '{email}'"
        insert_db(sql)

    def delete_user(self, email):
        sql = f"DELETE FROM USUARIO"
        sql += f" WHERE email = '{email}'"
        insert_db(sql)
    
    def find_by_id_user(self, email):
        sql = f"SELECT * FROM USUARIO WHERE email = '{email}'"
        result = read_db(sql)
        return result
    
    def get_current_user(email):  #get user information necessary for autentication token
        sql = f"SELECT username, email, admin, avatar FROM USUARIO WHERE email = '{email}'"
        result = read_db_user_necessary(sql)
        return result

    def patch_new_avatar(self, email, avatar):
        sql = f"UPDATE USUARIO SET avatar = '{avatar}' WHERE email = '{email}'"
        result = insert_db(sql)
        return result

    def find_password(email):
        sql = f"SELECT password FROM USUARIO WHERE email = '{email}';"
        result = read_password(sql)
        print(result)
        return result

    def find_admin(email):
        sql = f"SELECT admin FROM USUARIO WHERE email = '{email}';"
        result = read_password(sql)
        print(result)
        return result