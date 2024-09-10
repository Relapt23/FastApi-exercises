from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message

class CustomExceptionModel(BaseModel):
    er_message: str
    er_status_code: int
    er_detail: str

class User(BaseModel):
    username: str
    password: str

database = {"username": "Roman", "password": "pass1"}

app = FastAPI()

@app.exception_handler(CustomExceptionA)
async def custom_exception_handler(request: Request, exc: CustomExceptionA):
    error = jsonable_encoder(CustomExceptionModel(
        er_status_code=exc.status_code,
        er_detail=exc.detail, er_message = exc.message
    ))
    return JSONResponse(status_code=exc.status_code, content=error)

@app.exception_handler(CustomExceptionB)
async def custom_exception_handler(request: Request, exc: CustomExceptionB):
    error = jsonable_encoder(CustomExceptionModel(
        er_status_code=exc.status_code,
        er_detail=exc.detail, er_message = exc.message
    ))
    return JSONResponse(status_code=exc.status_code, content=error)

@app.put("/checkA")
def check_errorA(user:User):
    if user.username != database["username"] or user.password != database["password"]:
        raise CustomExceptionA(detail="Item not found", status_code=404, message= ":(")
    return user

@app.post("/checkB")
def check_errorB(user:User):
    if user.username != database["username"] or user.password != database["password"]:
        raise CustomExceptionB(detail="I dont know, that happend", status_code=418, message = "Ooops...")
    return user