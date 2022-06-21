from genericpath import exists
from hashlib import new
from fastapi import APIRouter, Body
from models.section import Section
from models.product import Product

router = APIRouter()
responses_custom = {
        422: {
            "content": {
                "application/json": {
                    "example": {"status": 422, "message": "validation error"}
                }
            },
        },
        200: {
            "content": {
                "application/json": {
                    "example": {"status": 200, "message": "method sucess"}
                }
            },
        },
    }

@router.post("/v1/section/", tags=["Section"], description="Create new Section", responses=responses_custom, )
def create_section(new_section: Section = Body(
        default={
        "section_name": "Eletronics",
        "product_id": "84307b01-6d82-4268-9069-d80105c56f42,84307b01-6d82-4268-9069-1231234124"
        }
    )):
    if new_section.find_section_by_section_name(new_section.section_name):
        return {'status': 422, "message": "section name already exists!"}
    if not Product.find_by_id_product(new_section.product_id):
        return {'status': 422, "message": "product id don't exists!"}
    else:
        products =  new_section.product_id.replace(",", " ")
        new_section.insert_section(new_section.section_name, products.split())
        return {'status': 200, "message": "section create with sucess"}

@router.get("/v1/section/", tags=["Section"], description="Reads all section", responses= responses_custom)
def get_all_sections():
    section = Section()
    return section.read_all_section()

@router.get("/v1/section/{section_name}/", tags=["Section"], description="Reads a section name", responses=responses_custom)
def get_section_by_name(section_name: str):
    section = Section()
    return section.find_section_by_section_name(section_name)

@router.delete("/v1/section/{section_name}/", tags=["Section"], description="Deletes a section", responses=responses_custom)
def delete_section(section_name: str):
    section = Section()
    if get_section_by_name(section_name):
        section.delete_section(section_name)
        return {"status": 200, "message": "Section delete with sucess"}
    else:
        return {"status": 422, "message": "validation error on delete"}

@router.patch('/v1/section/products',tags=["Section"], description="Patch products", responses= responses_custom)
def patch_section(section: Section = Body(
        default={
        "section_name": "Eletronics",
        "product_id": "84307b01-6d82-4268-9069-d80105c56f42,84307b01-6d82-4268-9069-1231234124"
        }
    )): #Adds more products a section array in database
    product_list = []
    if section.find_section_by_section_name(section.section_name):
        product_list.append(section.find_section_by_section_name(section.section_name))
        product_list[0][0]['products_id'].append(section.product_id)
        section.patch_products_id(section.section_name,product_list[0][0]['products_id'])
        return {"status": 200, "message": "Update name section with sucess!"}
    else: 
        return {"status": 422, "message": "Section name don't exists"}


