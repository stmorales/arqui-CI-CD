from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    token = "dsnsdsdsd"
    response = client.post("/user/", headers={
            "Authorization": f"Bearer {token}"
        }, json={"username": 'test'})
    assert response.status_code == 200

def test_get_users():
    token = "dsnsdsdsd"
    response = client.get("/users/", headers={
            "Authorization": f"Bearer {token}"
        }, json={"username": 'test'})
    assert list == type(response.json())
    assert response.status_code == 200


test_create_user()
test_get_users()