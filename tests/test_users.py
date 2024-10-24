from app import schemas
# from .database import client, session
import pytest
import jwt

from app.config import settings



#Moved to conftest.pyß
# @pytest.fixture(scope="function")
# def test_user(client):
#     user=schemas.UserCreate(email="test2@gmail.com",password="password123")
  
#     response=client.post("/users/",json= user.dict())
#     new_user=response.json()
#     new_user['password']=user.password   
#     print(new_user)
#     assert response.status_code==201
#     return new_user
    
   

# def test_root(client):
#     response=client.get("/")
#     assert response.status_code==200
#     assert response.json()=={"Hello":"production ubuntu -tem"}


def test_create_user(client):
    response=client.post("/users/",json={"email":"test2@gmail.com","password":"password123"})
    new_user=schemas.UserResponse(**response.json())
    assert new_user.email== response.json()["email"]
    assert response.status_code==201

def test_login_user(client, test_user):
    response=client.post("/login/",data={"username":test_user['email'],"password":test_user['password']})
    login_res=schemas.Token(**response.json())
    payload=jwt.decode(login_res.access_token, settings.secret_key , algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id==test_user['id']

    assert login_res.token_type=="bearer"
    print(response.json())

    assert response.status_code==200

@pytest.mark.parametrize(("email", "password", "status_code"), [
    ("wrongemail@gmail.com", "password123", 403),
    ("test2@gmail.com", "password1234", 403),
    (None, "password123", 422),
    ("test2@gmail.com", None, 422)
])
    
def test_incorrect_login(client, email, password, status_code):
    response=client.post("/login/",data={"username":email,"password":password})
    assert response.status_code==status_code
    # assert response.json()=={"detail":detail} 