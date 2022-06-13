from uuid import uuid4
from pydantic import BaseModel, Field
from db.config import insert_db,read_db_product

class Product(BaseModel):

    name_product: str = Field(None, alias="name_product")
    description: str = Field(None, alias="description")
    price: str = Field(None, alias="price")
    image: str = Field(None, alias= "image")

    def set_product(self, name_product, description, price, image):
        self.name_product = name_product
        self.description = description
        self.price = price
        self.image = image

    def insert_product(self, name_product, description, price, image):
        self.set_product(name_product, description, price, image)
        sql = f"INSERT INTO product (cod_product, name_product,description,price,image)"
        sql += f"VALUES ('{str(uuid4())}', '{name_product}','{description}','{price}','{image}')"
        insert_db(sql)

    def read_product(self):
        sql = f"SELECT * FROM product;"
        result = read_db_product(sql)
        return result

    def put_product(self, cod_product, name_product, price, image, description):
        self.set_product(name_product, price, image, description)
        sql = f"UPDATE product "
        sql += f"SET name_product = '{cod_product}',"
        sql += f" description = '{description}',"
        sql += f" price = '{price}',"
        sql += f" image = '{image}'"
        sql += f"WHERE cod_product = '{cod_product}'"
        insert_db(sql)

    def delete_product(self, cod_product):
        sql = f"DELETE FROM product"
        sql += f" WHERE cod_product = '{cod_product}'"
        insert_db(sql)
    
    def find_by_id_product(self, cod_product):
        sql = f"SELECT * FROM product WHERE cod_product = '{cod_product}'"
        result = read_db_product(sql)
        return result