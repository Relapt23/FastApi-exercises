from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine


meta = MetaData()

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

engine = create_engine("sqlite:///db.db", echo=True)

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String),
    Column('password', String)
)

meta.create_all(engine)
con = engine.connect()

@app.post("/login")
def login_user(user: User):
    s = users.select()
    rows = con.execute(s).fetchall()
    con.commit()
    for elem in rows:
        if elem[1] == user.username:
            raise HTTPException(status_code=418, detail="User in database")
    con.execute(users.insert().values(username=user.username, password=user.password))
    con.commit()
    return {"message":"Successful registration", "user": user.username}

@app.get("/login/{id}")
def get_user(id: int):
    s = users.select()
    res = con.execute(s).fetchall()
    for items in res:
        if items [0] == id:
            return {"id":items[0],
                    "username": items[1]
                }
    if id not in res:
        raise HTTPException(
            status_code=404,
            detail="Invalid id")
    con.commit()

@app.delete("/delete/{username}")
def delete_user(username: str):
    s = users.select()
    res = con.execute(s).fetchall()
    for elem in res:
        if elem[1] == username:
            con.execute(users.delete().where(users.c.username == username))
            con.commit()
            return {"message": "Successful delete"}
    raise HTTPException(status_code=430, detail="User not in database")
    

    
    
