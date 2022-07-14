from http.client import responses
from fastapi import APIRouter, Body
from models.cart import Cart
from models.product import Product
from models.section import Section
from routers.user_router import get_current_user


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

@router.post("/v1/cart/", tags=["Cart"], description="Insert products a Cart", responses=responses_custom, )
def insert_cart(new_products: Cart = Body(
        default={
        "products_cart": "84307b01-6d82-4268-9069-d80105c56f42,84307b01-6d82-4268-9069-1231234124",
        "email": "test@test.com"
        }
    )):
    products = new_products.products_cart.replace(",", " ")
    email = new_products.email
    products_split = products.split()
    product_erro = 0
    product_list = []
    for i in range(len(products_split)):
        if not Product.find_by_id_products(products_split[i]):
            product_erro += 1
    if product_erro > 0:
         return {'status': 422, "message": "product id don't exists!"}
    else:
        if new_products.read_cart(new_products.email):
            product_list.append(new_products.read_cart(new_products.email))
            for i in range(len(products_split)):
                product_list[0]['products_cart'].append(products_split[i])
                print(product_list[0]['products_cart'])
                new_products.patch_products_cart(product_list[0]['products_cart'], email)
        return {'status': 200, "message": "Products adds with sucess"} 
        

@router.get("/v1/cart/{email}", tags=["Cart"], description="Read cart by email of current user", responses= responses_custom)
def get_cart(email: str):
    cart = Cart()
    result = cart.read_cart(email)
    list_products = []
    products = Product()
    for i in range(len(result['products_cart'])):
        id_product = result['products_cart'][i]
        list_products.append(products.find_by_id_product(id_product))
    final_json = {"id_cart": result["id_cart"] ,"products_info": list_products}
    return final_json

@router.delete("/v1/cart/", tags=["Cart"], description="Delete cart products by email of current user",
responses= responses_custom)
def delete_product_cart(cart: Cart):
    email = cart.email
    products = cart.products_cart
    pop_product = []
    if cart.read_cart(email):
        read_cart = cart.read_cart(email)
        pop_product = read_cart['products_cart']
        if Product.find_by_id_products(products):
            if products in pop_product:
                if len(pop_product) == 1:
                    cart.delete_one_product_cart(pop_product[0], email)
                    return {"message": "Product(s) delete with success"}
                pop_product.remove(products)
                cart.delete_products_cart(pop_product, email)
                return {"message": "Product(s) delete with success"}
            else:
                return {"message": "Product not in cart"}
        else:
            return {'status': 422, "message": "product id don't exists!"}
    else:
        return {"message": "Error in delete product"}
    
    
