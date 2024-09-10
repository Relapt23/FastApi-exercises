from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError


app =FastAPI()

class User_data(BaseModel):
    username: str
    password: str = Field(min_length=3, max_length=18)
    age: int = Field(gt=18)
    email: EmailStr

custom_messages = {"username": "Логин не должен содержать цифр",
                  "password": "Длина пароля не должна быть меньше 3 и больше 18",
                  "age": "Пользователь несовершеннолетний",
                  "email": "Некорректная почта"
                  }

@app.exception_handler(RequestValidationError)
def custom_request_validation_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = custom_messages.get(field)
        errors.append({"field": field, "msg": msg, "value": error["input"]})
    print(errors)
    return JSONResponse(status_code=400, content=errors)

@app.post("/check_error")
def check_error(user: User_data):
    return user
