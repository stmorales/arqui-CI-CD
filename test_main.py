from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    token = "dsnsdsdsd"
    response = client.post("/user/signup", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "userName": 'test',
            "email": "email@email.com",
            "password": "123456"
        })
    assert response.status_code == 200

def test_bad_login():
    token = "dsnsdsdsd"
    response = client.post("/auth/token", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "userName": 'test',
            "email": "email@email.com",
            "password": "112"
        })
    assert response.status_code == 401

def test_unauthorized():
    response = client.get("/messages/")
    assert response.status_code == 401




test_create_user()
test_bad_login()
test_unauthorized()

