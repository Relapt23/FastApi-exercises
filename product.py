from fastapi import FastAPI
import models
from typing import Union

app = FastAPI()
sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]
@app.get('/product/{product_id}')
def product_info(product_id: int): 
        for product in sample_products:
            if product['product_id'] == product_id:
                    return product
sort_product =[]
@app.get("/products/search")
def product_search(keyword: str, category: Union[str, None] = None, limit:int = 5):
        for product in sample_products:
            if product not in sort_product:
                if product['category'] == category and keyword.lower() in product['name']:
                    sort_product.append(product)
            return sort_product

