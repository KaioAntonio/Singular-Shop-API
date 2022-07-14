from pydantic import BaseModel, Field
from db.config import *

class Cart(BaseModel):
    products_cart: str = Field(None, alias= "products_cart")
    email: str = Field(None, alias="email")

    def set_cart(self, products_cart, email):
        self.products_cart = products_cart
        self.email = email
    
    def create_cart(email):
        sql = f"INSERT INTO cart (products_cart, email) "
        sql += f"VALUES (ARRAY[]::varchar[], '{email}');"
        insert_db(sql)

    def read_cart(self, email):
        sql = f"SELECT * FROM cart "
        sql += f"WHERE email = '{email}'"
        result = read_db_cart(sql)
        return result
    
    def patch_products_cart(self, products_cart, email):
        sql = f"UPDATE cart "
        sql += f"SET products_cart = ARRAY {products_cart} "
        sql += f"WHERE email = '{email}';"
        result = insert_db(sql)
        return result
    
    def delete_products_cart(self, products_cart, email):
        sql = f"update cart set products_cart = ARRAY {products_cart}"
        sql += f" where email = '{email}';"
        insert_db(sql)

    def delete_one_product_cart(self,products_cart, email):
        sql = f"update cart set products_cart = (select  array_remove(products_cart, '{products_cart}' )  FROM cart "
        sql += f"WHERE email = '{email}') where email = '{email}';"
        insert_db(sql)
