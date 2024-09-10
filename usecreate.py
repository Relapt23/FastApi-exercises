from fastapi import FastAPI
import models

app = FastAPI()

@app.post("/create_user")
def create_user(user: models.UseCreate):
    return user