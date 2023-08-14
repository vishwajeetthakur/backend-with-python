from typing import  Union, List, Dict
from fastapi import FastAPI, Body
from models import Db
from database_utilities import add_product as add_prod
from database_utilities import update_product as update_prod
from database_utilities import delete_product as delete_prod
from database_utilities import get_all_products as get_all_prod
from database_utilities import create_user 
from database_utilities import add_product_to_basket 
from database_utilities import remove_product_from_basket 
from database_utilities import place_order 
from database_utilities import get_all_orders 
from database_utilities import get_all_orders_for_user 
from database_utilities import get_basket_content_for_user 

from models import Db, Product, User, Order



database = Db()

    
app = FastAPI()

@app.post("/add_product", status_code=200)
def add_product(product: Product):
    response = add_prod(product)
    return response
    
@app.put("/update_product/{product_id}", status_code=200)
def update_product(product_id: int, update_fields: dict = Body(...)):
    response = update_prod(product_id, update_fields)
    return response

@app.delete("/delete_product/{product_id}", status_code=200)
def delete_product(product_id: int):
    response = delete_prod(product_id)
    return response

    
    

@app.get("/products", response_model=Union[List[Product], Dict[str, str]]) 
def get_all_products():
    response = get_all_prod()
    return response



@app.post('/create_user')
def user_create(user: User):
    response = create_user(user)
    return response



# need to optimize "collection.update_one({'basket_id': basket_obj.basket_id}, {'$set': basket_obj.dict()})"
@app.post("/user/add_product_to_basket", status_code=200)
def add_the_product_to_basket(details: dict = Body(...)): # product_id, user_id
    response = add_product_to_basket(details)
    return response



@app.put("/user/remove_product_from_basket")
def remove_the_product_from_basket(details: dict = Body(...)):
    response = remove_product_from_basket(details) # product_id, user_id
    return response


# # might not require this api
# @app.delete('delete_order/{order_id}', status_code=200)
# def delete_the_order(order_id: int):
#     response = delete_order(order_id)
#     return response

# empty order should not be processed
@app.get('/user/place_order/{user_id}')
def place_the_order(user_id: int):
    response = place_order(user_id)
    return response


@app.get("/orders", response_model=Union[List[Order], Dict[str, str]])
def get_all_the_orders():
    response = get_all_orders()
    return response 

@app.get("/user/orders/{user_id}", response_model=Union[List[Order], Dict[str, str]])
def get_all_the_orders(user_id: int):
    response = get_all_orders_for_user(user_id)
    return response

@app.get("/user/basket_content/{user_id}", response_model= Union[List[Product], Dict[str, str]])
def get_basket_content_for_the_user(user_id: int):
    response = get_basket_content_for_user(user_id)
    return response
