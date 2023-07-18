from pymongo import MongoClient
from typing import ClassVar, Union, List, Dict, Optional, Any
from pydantic import BaseModel, Field


class Db:
    client = MongoClient("localhost", 27017, username='root', password='root')
    db = client.ecom

class Product(BaseModel):
    product_counter: ClassVar[int] = 1
    product_id: int = Field(default_factory=lambda: Product.get_next_id())
    product_name: str
    product_description: Union[str, None] = None
    product_tags: List[str] = []
    product_price: int

    @staticmethod
    def get_next_id() -> int:
        # global product_counter
        Product.product_counter += 1
        return Product.product_counter
    
class Basket(BaseModel):
    basket_counter: ClassVar[int] = 1
    basket_id: int = Field(default_factory=lambda: Basket.get_next_id())
    products: List[int] = []
    previous_order: List[int] = []

    def save_to_database(self):
        Db.db.basket.insert_one(self.dict())

    @staticmethod
    def get_next_id() -> int:
        # print("counter ran")
        Basket.basket_counter += 1
        return Basket.basket_counter
    
class Order(BaseModel):
    order_counter: ClassVar[int] = 1
    order_id: int = Field(default_factory=lambda: Order.get_next_id())
    products: List[int] = []
    user_id: int

    @staticmethod
    def get_next_id() -> int:
        # print("counter ran")
        Order.order_counter += 1
        return Order.order_counter
    
class User(BaseModel):
    user_counter: ClassVar[int] = 1
    user_id: int = Field(default_factory=lambda: User.get_next_id())
    user_name: str

    # No default_factory for user_basket anymore, it will be initialized in __init__
    user_basket_id: int = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.create_and_save_basket()

    def create_and_save_basket(self):
        basket = Basket()
        self.user_basket_id = basket.basket_id
        basket.save_to_database()

    @staticmethod
    def get_next_id() -> int:
        User.user_counter += 1
        return User.user_counter