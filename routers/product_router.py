from fastapi import APIRouter

from models.product import Product

router = APIRouter()

@router.post("/v1/product", tags=["Product"], description="Creates new product")
def create_product(new_product: Product):
    new_product.insert_product(new_product.name_product,new_product.description,new_product.price,new_product.image)
    return new_product

@router.get("/v1/product", tags=["Product"], description= "Reads all products")
def get_all_products():
    product = Product()
    return product.read_product()


@router.put("/v1/product", tags=["Product"], description= "Update product")
def put_product(new_product: Product):
    new_product.put_product(new_product.productname, new_product.password, new_product.admin, new_product.avatar, new_product.email)
    return new_product

@router.delete("/v1/product/{cod_product}", tags=["Product"], description= "Delete product")
def delete_product(cod_product: str):
    product = Product()
    product.delete_product(cod_product)
    print(product)
    return {"message": "product delete with sucess"}

@router.get("/v1/product/{cod_product}", tags=["Product"], description="Reads a product")
def get_product_by_cod(cod_product: str):
    product = Product()
    return product.find_by_id_product(cod_product)[0]