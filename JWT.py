from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel


app = FastAPI()

SECRET_KEY = 'qwerty'
ALGORITHM = "HS256"

oauth2 = OAuth2PasswordBearer(tokenUrl='token')

class User(BaseModel):
    username: str
    password: str

database= [{"username": "popa1", "password":"pass1"}, {"username": "popa2", "password":"pass2"}]
def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2)):
    try:
        print("ooo")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token has expired")
    except jwt.PyJWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print("boba")
        print(e)
        raise HTTPException(status_code=401, detail="Dolboeb")
    
    
def get_user(username:str):
    for user in database:
        if user.get("username") == username:
            return user
        return None
    
@app.post("/login")
def enter_user(user: User):
    for person in database:
        if person.get("username") == user.username and person.get("password") == user.password:
            token = create_jwt_token({"sub": person})
            return {"access_token": token}
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",)
    
@app.get('/protected_resource')
def protected_resource(current_user: str = Depends(get_user_from_token)):
    for person in database:
        if current_user.get('username') == person['username'] and current_user.get("password") == person['password']:
            return {"message": "Successful Autharization", "user":current_user.get('username')}
        else:
            return {"error": "User not found"}


