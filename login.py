from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials


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

def check_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        return user

@app.get("/login")
def get_login(login: User = Depends(check_user)):
    return {"message": "You have access to the protected resource!", "user_info": login}
