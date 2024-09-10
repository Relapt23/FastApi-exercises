from fastapi import FastAPI, requests, Body
from fastapi.responses import FileResponse
import models
app = FastAPI()

@app.get('/')
async def home():
    return  FileResponse('templates/index.html')
@app.post("/calculate",)
def calculate(body = Body()):
    res = (body['num1'] + body['num2'])
    return res

@app.post("/users")
def get_users(user: models.User):
    if user.age >= 18:
        return {"name": user.name,
                "age": user.age,
                "is_adult": True}
    else:
        return {"name": user.name,
                "age": user.age,
                "is_adult": False}

