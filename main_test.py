from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

database = [User(username= "ejjejf", password="wejfjewq")]

app = FastAPI()

@app.post("/login")
def login_user(user: User):
    if user not in database:
        database.append(user)
        return {"message":"Successful registration", "user": user.username}
    else:
        raise HTTPException(status_code=418, detail="User in database")

    
@app.get("/login/{username}")
def get_user(username: str):
    for person in database:
        if person.username == username:
            return person        
    raise HTTPException(status_code=418, detail="User not found")

@app.delete("/delete/{username}")
def delete_user(username: str):
    for person in database:
        if username == person.username:
            database.remove(person)
            return {"message": "Successful delete user"}
    raise HTTPException(status_code=418, detail="User not found in DB")
        

    