from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from fastapi.responses import PlainTextResponse, JSONResponse
import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


users = [{"id":24, "username": "poerr", "password": "p", "email": "romashlapt@mail.ru"}]
class User(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr

class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = 'error', status_code: int = 418):
        super().__init__(detail=detail, status_code=status_code)

app = FastAPI()

@app.exception_handler(UserNotFoundException)
def user_bot_found_handler(request: Request, exc: ErrorResponseModel):
    start = datetime.datetime.now()
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers={'X-ErrorHandleTime': str(datetime.datetime.now() - start)}
    )

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    error = jsonable_encoder(ErrorResponseModel(
        status_code=exc.status_code,
        detail=exc.detail
    ))
    return JSONResponse(status_code=exc.status_code, content=error)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: ErrorResponseModel):
    return PlainTextResponse(str(exc), status_code=418)

@app.post('/login')
def login(user: User):
    for person in users:
        if person["username"] != user.username or person["email"] != user.email:
            users.append({"id": user.id, "username": user.username, "password": user.password, "email": user.email})
            return {"message":"Successful registration", "user": user.username}
        else:
            raise UserNotFoundException("The user is already registered", 404)


@app.get("/check_pass/{user_id}")
async def check_pass(user_id:int):
    print(users)
    for user in users:
        if user_id != users[user]["id"]:
            raise CustomException(detail="Пользователь не найден", status_code=317)
        else:
            return user

