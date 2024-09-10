from fastapi.testclient import TestClient
from main_test_mock import app, meta, engine
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def test_clear_db():
    meta.drop_all(engine)
    meta.create_all(engine)
    yield


def test_login_true():
    response = client.post("/login", json={"username": "Relapt", "password": "0987"})
    assert response.status_code == 200
    assert response.json()["message"] == "Successful registration"
def test_login_false():
    client.post("/login", json={"username": "Relapt", "password": "0987"})
    response = client.post("/login", json={"username": "Relapt", "password": "0987"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Users in database"

def test_get_true():
    client.post("/login", json={"username": "Relapt", "password": "0987"})
    response = client.get("/get/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["username"] == "Relapt"

def test_get_false():
    client.post("/login", json={"username": "Relapt", "password": "0987"})
    response = client.get("/get/10")
    assert response.status_code == 420
    assert response.json()["detail"] == "User not found"

def test_update_true():
    client.post("/login", json={"username": "Relapt", "password": "0987"})
    response = client.put("update/1", json={"username": "popo4ka", "password": "0987"})
    assert response.status_code == 200
    assert response.json()["message"] == "Update complete"

def test_update_false():
    client.post("/login", json={"username": "Relapt", "password": "0987"})
    response = client.put("update/3", json={"username": "popo4ka", "password": "0987"})
    assert response.status_code == 420
    assert response.json()["detail"] == "User not found"
