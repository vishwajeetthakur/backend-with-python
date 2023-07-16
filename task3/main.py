from typing import Union, List
from fastapi import FastAPI, Depends, Body, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


class Book(BaseModel):
    name: str
    description: Union[str, None] = None
    author: str
    price: int

class Settings(BaseModel):
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_username: str = "root"
    mongodb_password: str = "root"
    mongodb_db_name: str = "library_management"
    collection_name: str = "books"

app = FastAPI()

settings = Settings()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.mongodb_url, username=settings.mongodb_username, password=settings.mongodb_password)
    app.mongodb = app.mongodb_client[settings.mongodb_db_name]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

async def get_db():
    return app.mongodb

@app.post('/create_book')
async def create_book(book: Book, db = Depends(get_db)):
    try : 
        collection = db[settings.collection_name]
        await collection.insert_one(book.dict())
        return {"Message": 'Book Created Successfully'}
    except Exception as e :
        raise HTTPException(status_code=400, detail="Book Creation Failed")

'''
@app.get('/books', response_model=List[Book])
async def get_books(db = Depends(get_db)):
    collection = db[settings.collection_name]
    books_cursor = collection.find()
    books = [{**book, "_id": str(book["_id"])} for book in await books_cursor.to_list(length=100)]
    return books
'''

@app.get('/books', response_model=List[dict])
async def get_books(db = Depends(get_db)):
    collection = db[settings.collection_name]
    cursor = collection.find()
    # print("### cursor : ", cursor)
    books = []
    async for document in cursor:
        document['_id'] = str(document['_id'])
        books.append(document)
    return books


@app.delete("/delete_books/{book_name}")
async def delete_book(book_name: str, db = Depends(get_db)):
    try: 
        collection = db[settings.collection_name]
        await collection.delete_many({"name": book_name})
        return {"Message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Book Deletion Failed")

@app.put("/update_book/{book_id}")
async def update_book(book_id: str, update_fields: dict = Body(...), db = Depends(get_db)):
    try: 
        collection = db[settings.collection_name]
        await collection.update_one({'_id': ObjectId(book_id)}, {'$set': update_fields})
        return {"Message": 'Books updated Successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Book Update Failed")
