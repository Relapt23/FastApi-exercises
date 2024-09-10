from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel
from typing import Optional, Annotated, Union
from enum import Enum


app = FastAPI()

SECRET_KEY = 'popa'
ALGORITHM = "HS256"

oauth2 = OAuth2PasswordBearer(tokenUrl='token')
class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'

class Permission(Enum):
    ADMIN = 'create, read, update, delete'
    USER = 'read, update'
    GUEST = 'read'

class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = None


database= {
    "admin": {"username": "popa1", "password":"pass1", "role": "admin"}, 
    "user":{"username": "popa2", "password":"pass2", "role": "user"},
    "guest":{"username":"popa3", "password": "pass3", "role": "guest"}
}
def create_token(data:dict):
    return jwt.encode(data, SECRET_KEY,algorithm=ALGORITHM)

def decode(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload.get("sub")
    except Exception as e:
        raise HTTPException(status_code=401,detail="Error") 

def get_user(username: str):
    if username in database:
        user_data = database[username]
        return User(**user_data)
    return None

def set_permission(user: User):
    if user.role == Role.ADMIN:
        user.permission = Permission.ADMIN
    elif user.role == Role.USER:
        user.permission = Permission.USER
    else:
        user.permission = Permission.GUEST
    return user

@app.post("/token/")
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_data_from_db = get_user(user_data.username)
    print(user_data_from_db)
    # if user_data_from_db is None or user_data.password != user_data_from_db.password:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid credentials",
    #         headers={"WWW-Authenticate": "Bearer"},)
    # return {"access_token": create_token({"sub": user_data.username})}