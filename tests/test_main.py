from fastapi.testclient import TestClient
from main_test2 import app, meta, engine
import pytest


client = TestClient(app)

@pytest.fixture(autouse=True)
def test_clear_bd():
    meta.drop_all(engine)
    meta.create_all(engine)
    yield


def test_login():
    response = client.post("/login", json={"username": "ek35555", "password": "passwd"})
    assert response.status_code == 200
    assert response.json()["message"] == "Successful registration"
    assert response.json()["user"] == "ek35555"

    response = client.post("/login", json={"username": "ek35555", "password": "passwd"})
    assert response.status_code == 418
    assert response.json()["detail"] == "User in database"

def test_get_user():
    client.post("/login", json={"username": "ek35555", "password": "passwd"})

    response = client.get("/login/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["username"] == "ek35555"

def test_get_non_existing_user():
    response = client.get("/login/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid id"

def test_delete_user():
    client.post("/login", json={"username": "ek35555", "password": "passwd"})

    response = client.delete("/delete/ek35555")
    assert response.status_code == 200
    assert response.json()["message"] == "Successful delete"

def test_delete_not_existing_user():
    response = client.delete("/delete/ekl4")
    assert response.status_code == 430
    assert response.json()["detail"] == "User not in database"
