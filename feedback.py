from fastapi import FastAPI
import models

app = FastAPI()
database = []
@app.post("/feedback")
def print_fb(feedback: models.CheckFid):
    fb = [feedback]
    database.append(fb)
    return {"message": "Feedback received. Thank you," f"{feedback.name}!"}