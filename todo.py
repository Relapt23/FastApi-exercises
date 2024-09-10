from fastapi import FastAPI, HTTPException, status
import sqlite3
from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    description: str
    completed: bool = False

app = FastAPI()

db = sqlite3.connect('todo_list.db', check_same_thread=False)
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS database_todo(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
description TEXT,
completed BOOL)""")
db.commit()

def save_todo(title, description, completed):
    cursor.execute("INSERT INTO database_todo(title,description,completed) VALUES(?, ?, ? );", (title,description,completed))
    cursor.execute("SELECT * FROM database_todo")
    db.commit()


@app.post("/create_todo")
def create(todo: Todo):
    save_todo(todo.title,todo.description,todo.completed)
    return todo

@app.get("/{id}")
def show_todo(id: int):
    cursor.execute("SELECT * FROM database_todo")
    res = cursor.fetchall()
    for items in res:
        if items [0] == id:
            return {"id":items[0],
                    "title": items[1],
                    "description": items[2],
                    "completed": items[3]
                    }
    if id not in res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid id")
    db.commit()

@app.get('/delete/{id}')
def delete_todo(id:int):
    cursor.execute("DELETE FROM database_todo WHERE id = ?", (id,))
    db.commit()
    return {"message": "Успешное удаление"}

@app.post("/update/")
def update_todo(todo:Todo):
    cursor.execute("UPDATE database_todo SET completed = 'True' WHERE title = ?", (todo.title,))
    cursor.execute("SELECT * FROM database_todo")
    values = cursor.fetchall()
    for elem in values:
        if todo.title == elem[1]:
            return elem
    db.commit()

db.close()


