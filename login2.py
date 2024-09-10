from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from pydantic import BaseModel
from typing import Annotated
app = FastAPI()
security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str

USER_DATA = [User(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]

def get_user(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

def authentificate_user(credentials: Annotated[HTTPBasicCredentials,Depends(security)]):
    user = get_user(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return "You got my secret, welcome"

@app.get('/login')
def login_user(user: User=Depends(authentificate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}