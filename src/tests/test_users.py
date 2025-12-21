from fastapi.testclient import TestClient

from ..schemas import UserOut
from .test_database import client


def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == "SocialMediaAPI"
    assert response.status_code == 200

# As the prefix is /users, the path will be /users/ , so when the request is sent to /users it will respond 
# with 307 Temporary Redirect and then goes to the path /users/
def test_create_user(client):
    response = client.post("/users/", json={"email": "j@gmail.com", "password": "password"})
    print(response.json())
    user_response = UserOut(**response.json())
    # assert user_response.email == "jegadees@gmail.com"
    assert response.status_code == 201

def test_login_user(client):
    response = client.post("/auth/login/", 
        data={"username": "j@gmail.com", "password": "password"}   # use "data" instead of "json" for form data
    )  
    assert response.status_code == 200
