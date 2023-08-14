import redis
from models import Db, Product, User, Basket, Order
from fastapi import Body, HTTPException
from redis_query import *

database = Db()

USERNAME = None
PASSWORD = None
'''

    
basket = [
    basket_id1: {basket_details1},
    basket_id2: {basket_details1},
    basket_id3: {basket_details1},
    ]

orders = [
    user1: [{order_details1}, {order_details2}],
    user2: [bukcet_details],
    user3: [bukcet_details],
    ]
    


'''

def redis_connection():
    client_kwargs = {
        "host": "localhost",
        "port": 6379,
        "decode_responses": True
    }

    if USERNAME:
        client_kwargs["username"] = USERNAME
    if PASSWORD:
        client_kwargs["password"] = PASSWORD

    yield redis.Redis(**client_kwargs)



conn_generator = redis_connection()
conn = next(conn_generator)



def get_basket(user_id):
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
        print(product_object_list)

        
    except Exception as e:
        print( {'message': f'Failed get basket: {str(e)}'} )