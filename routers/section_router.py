from fastapi import APIRouter
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

@router.post("/v1/section/", tags=["Section"], description="Create new Section", responses=responses_custom )
def create_section(new_section: Section):
    cod = Product()
    if cod.find_by_id_product(new_section.cod_product):
        new_section.insert_section(new_section.cod_product, new_section.name_section)
        return {'status': 200, "message": "section create with sucess"}
    else:
        return {'status': 422, "message": 'cod product does not exists'}

@router.get("/v1/section/", tags=["Section"], description="Reads all section", responses= responses_custom)
def get_all_section():
    section = Section()
    return section.read_all_section()

@router.get("/v1/section/{section_name}/", tags=["Section"], description="Reads a section name", responses=responses_custom)
def get_section_by_name(section_name: str):
    section = Section()
    return section.find_section_by_name_section(section_name)

@router.delete("/v1/section/{section_name}/", tags=["Section"], description="Deletes a section", responses=responses_custom)
def delete_section(section_name: str):
    section = Section()
    if get_section_by_name(section_name):
        section.delete_section(section_name)
        return {"status": 200, "message": "user delete with sucess"}
    else:
        return {"status": 422, "message": "validation error"}

@router.patch('/v1/section/',tags=["Section"], description="Patch product in section name", responses= responses_custom)
def patch_section(section: Section):
    section.patch_section(section.cod_product,section.name_section)
    return {"status": 200, "message": "Update name section with sucess!"}

