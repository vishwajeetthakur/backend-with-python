
from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel
import json
from bson import ObjectId

'''
The function parameters will be recognized as follows:

If the parameter is also declared in the path, it will be used as a path parameter.
If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
'''

from pymongo import MongoClient

client = MongoClient("localhost", 27017, username='root', password='root')



class Book(BaseModel):
    name: str
    description: Union[str, None] = None
    author: str
    price: int


app = FastAPI()


@app.post('/create_book')
def create_book(book: Book):
    try : 
        db = client.library_management
        collection = db.books
        print(book, type(book))
        collection.insert_one(book.dict())
        return {"Message": 'Book Created Successfully'}
    except Exception as e :
        print(e)
        return {"Message": 'Failed!!!'}

def get_array_of_json(cursor):
    array = []
    for document in cursor:
        document["_id"] = str(document["_id"])  
        array.append(document)
    return array

@app.get('/books')
def get_books():
    db = client.library_management
    collection = db.books
    result = get_array_of_json(collection.find())

    return result

@app.delete("/delete_books/{book_name}")
def delete_book(book_name: str):
    try: 
        db = client.library_management
        collection = db.books
        collection.delete_many({"name": book_name})
        return {"Message": "Book deelted sucesfully"}
    except Exception as e:
        print(e)
        return {"Message": 'Failed!!!'}

@app.put("/update_book/{book_id}")
def update_book(book_id: str, update_fields: dict = Body(...)):
    try: 
        db = client.library_management
        collection = db.books  

        collection.update_one({'_id': ObjectId(book_id)}, {'$set': update_fields})
        return {"Message": 'Books updated Sucesfully'}
    except Exception as e:
        print(e)
        return {"Message": 'Failed!!!'}

'''
IMPROVE
implement this with asyncio : https://motor.readthedocs.io/en/stable/
Motor for asynio : https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
'''