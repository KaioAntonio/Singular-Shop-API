from pydantic import BaseModel, Field
from db.config import *

class Section(BaseModel):
    cod_product: str = Field(None, alias="cod_product")
    name_section: str = Field(None, alias= "name_section")

    def set_section(self, cod_product, name_section):
        self.cod_product = cod_product
        self.name_section = name_section
    
    def insert_section(self, cod_product,name_section):
        self.set_section(cod_product, name_section)
        all_sections = Section.read_all_section(self)
        sql = f"INSERT INTO product_section (id_section, cod_product, name_section)"
        sql += f"VALUES ({len(all_sections) + 1}, '{cod_product}', '{name_section}');"
        insert_db(sql)
    
    def read_all_section(self):
        sql = f"SELECT * FROM product_section;"
        result = read_db_section(sql)
        return result
    
    def delete_section(self, name_section):
        sql = f"DELETE FROM product_section"
        sql += f" WHERE name_section = '{name_section}'"
        insert_db(sql)

    def patch_section(self,cod_product,name_section):
        self.set_section(cod_product, name_section)
        sql = f"UPDATE product_section "
        sql += f"SET cod_product = '{cod_product}'"
        sql += f" WHERE name_section = '{name_section}'"
        result = insert_db(sql)
        return result

    def find_section_by_name_section(self, name_section):
        sql = f"SELECT * FROM product_section WHERE name_section = '{name_section}'"
        result = read_db_section(sql)
        return result

