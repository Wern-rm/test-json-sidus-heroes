from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sidus-Heroes test job API"}


def test_get_user_5():
    response = client.get(f"/get/user/{5}")
    assert response.status_code == 200


def test_get_user_100():
    response = client.get(f"/get/user/{100}")
    assert response.status_code == 400


def test_create_user_found_user():
    response = client.post("/create/user", json={'login': 'string1', 'name': 'test', 'password': 'test'})
    assert response.status_code == 400


def test_create_user_success():
    response = client.post("/create/user", json={'login': 'string100', 'name': 'test', 'password': 'test'})
    assert response.status_code == 200


def test_update_user_fail_auth():
    response = client.put(f"/update/user/{5}", json={'new_login': 'User123', 'new_name': 'NewName123'})
    assert response.status_code == 401


def test_update_user_fail_user_id():
    response = client.put(f"/update/user/{5}", json={'new_login': 'User123', 'new_name': 'NewName123'}, auth=('newLogin2', 'string'))
    assert response.status_code == 401


def test_update_user_success():
    response = client.put(f"/update/user/{7}", json={'new_login': 'User123', 'new_name': 'NewName123'}, auth=('newLogin2', 'string'))
    assert response.status_code == 401
