from fastapi import FastAPI, Body


app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

@app.get("/users/{user_id}")
def read_users(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    else:
        return {"error":"User not found"}