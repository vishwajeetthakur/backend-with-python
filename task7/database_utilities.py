from models import Db, Product, User, Basket, Order
from fastapi import Body, HTTPException

database = Db()


def add_product(product: Product):
    try:
        collection = database.db.products
        collection.insert_one(product.dict())
        return {"Message": 'Product Created Successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


def update_product(product_id: int, update_fields: dict):
    try:
        collection = database.db.products
        print(update_fields, product_id)
        collection.update_one({'product_id': product_id}, {'$set': update_fields})
        return {"Message": 'Product updated Sucesfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_product(product_id: int):
    try:
        collection = database.db.products
        collection.delete_one({"product_id": product_id})
        return {"Message": 'Product deleted Sucesfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
     

def get_all_products():
    try:
        collection = database.db.products
        all_products = collection.find()
        return list(all_products)
        
    except Exception as e:
        return {'message': f'Failed to get products: {str(e)}'}
    

def create_user(user: User):
    try:
        collection = database.db.user
        collection.insert_one(user.dict())
        return {'message': f'user created Sucessfully'}
    except Exception as e:
        return {'message': f'Failed to create user: {str(e)}'} 
    




def add_product_to_basket(details: dict):
    try:
        product_id = details['product_id']
        user_id = details['user_id']
        user = database.db.user.find_one({'user_id': user_id})
        basket_id = user['user_basket_id'] 
        basket = database.db.basket.find_one({'basket_id': basket_id})
        
        if basket:
            basket_obj = Basket(**basket)
            basket_obj.products.append(product_id)
            database.db.basket.update_one({'basket_id': basket_obj.basket_id}, {'$set': basket_obj.dict()})
        else:
            basket_obj = Basket(products=[product_id])
            database.db.basket.insert_one(basket_obj.dict())
        return {'message': 'Product added to basket successfully.'}
    except Exception as e:
        return {'message': f'Failed to add product to basket: {str(e)}'} 
    


def remove_product_from_basket(details: dict):
    try:
        product_id = details['product_id']
        user_id = details['user_id']
        user = database.db.user.find_one({'user_id': user_id})
        basket_id = user['user_basket_id'] # doubtful
        
        # can write logic to validate product
        collection = database.db.basket
        basket = collection.find_one({'basket_id': basket_id})
        if basket:
            basket_obj = Basket(**basket)
            basket_obj.products.remove(product_id)
            collection.update_one({'basket_id': basket_obj.basket_id}, {'$set': basket_obj.dict()})
            return  {'message': 'Product removed from basket successfully.'}
        else:
            return  {'message': 'Product Not in the basket.'}
        
    except Exception as e:
        return {'message': f'Failed to add product to basket: {str(e)}'}
    

def create_order(order: Order):
    try:
        collection = database.db.order
        collection.insert_one(order.dict())
        return {"Message": 'Order Created Successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

def delete_order(order_id: int):
    try:
        collection = database.db.order
        collection.delete_many({"order_id": order_id})
        return {"Message": 'Order Deleted Successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    



def place_order(user_id: int):
    try:
        collection = database.db.user
        user = collection.find_one({'user_id': user_id})
        
        basket = database.db.basket.find_one({'basket_id': user["user_basket_id"]})
        if basket:
            basket_obj = Basket(**basket)
            product_list = []
            for product_id in basket_obj.products:
                product_list.append(product_id)

            order = Order(user_id= user_id, products=product_list)
            create_order(order=order)
            basket_obj.products = []
            basket_obj.previous_order.append(order.order_id)
            database.db.basket.update_one({'basket_id': basket_obj.basket_id}, {'$set': basket_obj.dict()})

        return {'message': 'Order Placed successfully.'}
    
    except Exception as e:
        return {'message': f'Failed to add product to basket: {str(e)}'}


def get_all_orders():
    try:
        orders = database.db.order.find()
        print(orders)
        return list(orders)
    except Exception as e:
        return {'message': f'Failed get Orders: {str(e)}'} 


def get_all_orders_for_user(user_id: int):
    try:
        orders = database.db.order.find({'user_id': user_id})
        return list(orders)
    except Exception as e:
        return {'message': f'Failed get Orders: {str(e)}'}
    

def get_basket_content_for_user(user_id: int):
    try:
        user = database.db.user.find_one({'user_id': user_id})
        
        basket_id = user['user_basket_id']
        print("basket id got = ", basket_id)
        pipeline = [
                    { "$match": { "basket_id": 2 } },
                    { "$unwind": { "path": "$products" } },
                    { "$lookup": { 
                        "from": "products", 
                        "localField": "products", 
                        "foreignField": "product_id", 
                        "as": "product" 
                        } 
                    },
                    { "$unwind": { "path": "$product" } },  
                    { "$project": { 
                        "product_id": "$product.product_id", 
                        "product_name": "$product.product_name", 
                        "product_price": "$product.product_price", 
                        "product_tags": "$product.product_tags", 
                        "product_description": "$product.product_description" 
                        } 
                    }
                ]
        print("testingggggg")
        results = database.db.basket.aggregate(pipeline)
        product_object_list = [Product(**i) for i in results]
        return product_object_list
    except Exception as e:
        return {'message': f'Failed get basket: {str(e)}'}