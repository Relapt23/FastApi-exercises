from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Table, Column, String, Integer, create_engine, MetaData

meta = MetaData()

engine = create_engine("sqlite:///tests/database_test.db")

users = Table('users', meta,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('username', String),
              Column('password', String)
)

meta.create_all(engine)

con = engine.connect()

class User(BaseModel):
    username: str
    password: str = Field(min_length=3, max_length=15)

app = FastAPI()

@app.post('/login')
def login_user(user: User):
    s = users.select()
    row = con.execute(s).fetchall()
    for elem in row:
        if elem[1] == user.username:
            raise HTTPException(status_code=404, detail="Users in database")
    insert_user = users.insert().values(username = user.username, password = user.password)
    con.execute(insert_user)
    con.commit()
    return {"message": "Successful registration"}

@app.get('/get/{id}')
def get_user(id: int):
    s = users.select()
    row = con.execute(s).fetchall()
    for elem in row:
        if elem[0] == id:
            return {"id": elem[0],
                    "username": elem[1]
            }
        con.commit()
    raise HTTPException(status_code=420, detail="User not found")

@app.put('/update/{id}')
def updater(id: int, user: User):
    s = users.select()
    row = con.execute(s).fetchall()
    for elem in row:
        if elem[0] == id:
            con.execute(users.update().where(users.c.id == id).values(username = user.username, password = user.password))
            con.commit()
            res = con.execute(users.select().where(users.c.username == user.username)).fetchall()
            print(res)
            return {"message": "Update complete"}
    raise HTTPException(status_code=420, detail="User not found")


