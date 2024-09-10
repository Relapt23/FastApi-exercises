from pydantic import BaseModel, conint, EmailStr
from typing import Union

class User(BaseModel):
    name: str
    age: int


class CheckFid(BaseModel):
    name: str
    message: str

class UseCreate(BaseModel):
    name: str
    email: EmailStr
    age: conint(gt=0)
    is_suscribed: Union[bool, None] = None


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


class Login(BaseModel):
    username: str
    password: str
