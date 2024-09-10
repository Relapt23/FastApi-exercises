from fastapi import FastAPI, Cookie, Response
import models
from random import randint

app = FastAPI()

def getRandStr(lenght):
    return "".join(chr(randint(33, 125)) for _ in range(lenght))

database = [{"username": "user123", "password": "password123"},{"username": "user567", "password": "password567"}] 
tokens ={}
@app.post('/login')
def logon(login: models.Login, response: Response):
    for person in database:
        if login.username == person["username"] and login.password == person["password"]:
            res = getRandStr(4) + chr(randint(65, 90)) + getRandStr(5)
            session_token= res
            tokens[res] = person
            response.set_cookie(key='session_token', value = session_token, httponly=True)
            return {"session_token": session_token}
    
@app.get("/user")
def chek_user(session_token = Cookie()):
    for key in tokens.keys():
        if session_token == key:
            return tokens[key]
        else:
            return {"message": "Unauthorized"}
    

