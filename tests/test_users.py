import pytest
from jose import jwt
from app import schemas

from app.config import settings

# from starlette.testclient import TestClient
from app.main import app


# client = TestClient(app)
# def test_root():

#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

# when testing users, we use "/users/" instead of "/users", 
# to avoid having a 307 Redirect instead of a 201.

# when you login the user isn't there, since we use client pytest fixture
# and it drops the database at the end of the test.

def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

# okay I think that even if I pass None to one of the fields, 
# OAuth2PasswordRequestForm will still throw a 403 error instead of a 422 error.
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('srinidhi@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    ("None", 'password123', 403),
    ('srinidhi@gmail.com', None, 403)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    assert res.json().get('detail') == 'Invalid Credentials'