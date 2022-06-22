from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

"""def test_create_user():
    response =  client.post("/v1/user",
     json= {
        "username": "Kaio123decapela",
        "password": "K@123aio123",
        "email": "kaio156312@hotmail.com.br",
        "admin": "1",
        "avatar": "1"
    },)
    assert response.status_code == 200
    assert response.json() == {
        "username": "Kaio123decapela",
        "password": "K@123aio123",
        "email": "kaio156312@hotmail.com.br",
        "admin": "1",
        "avatar": "1"
    }"""

def test_create_existing_user():
    response =  client.post("/v1/user",
     json= {
        "username": "Kaio de capela",
        "password": "K@123aio123",
        "email": "kaioaar@hotmail.com.br",
        "admin": "1",
        "avatar": "1"
    })
    assert response.status_code == 422
    assert response.json() == {
        "status": 422,
        "error": "Este e-mail já está sendo utilizado"
    }

def test_read_users():
    response = client.get("v1/users")
    assert response.status_code == 200

def test_read_user_by_email():
    response = client.get("v1/user/luanzin1167@gmail.com")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "86a4e1be-372f-43ef-b469-e7ee05b5d7ec",
        "username": "Luan Limas",
        "password": "$2b$12$qIfECS.3Gg9BhM577U0CCOet9rQeNsbGLuj5i/wmr2BStagx22RbS",
        "email": "luanzin1167@gmail.com",
        "admin": True,
        "avatar": "https://www.origamid.com/wp-content/uploads/2019/05/igor.jpg"
    }

def test_read_user_by_incorrect_email():
    response = client.get("v1/user/145610@gmail.com")
    assert response.status_code == 422
    assert response.json() == {
        "status": 422,
        "message": "validation error on get"
    }

def test_update_user():
    response = client.put("/v1/user",
    json= {
        "user_id": "86a4e1be-372f-43ef-b469-e7ee05b5d7ec",
        "username": "Luan Limas",
        "password": "$2b$12$qIfECS.3Gg9BhM577U0CCOet9rQeNsbGLuj5i/wmr2BStagx22RbS",
        "email": "waltinho@teste.com",
        "admin": True,
        "avatar": "https://www.origamid.com/wp-content/uploads/2019/05/igor.jpg"
    })
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        'message': 'update sucess'
    }

def test_update_invalid_user():
    response = client.put("/v1/user",
    json= {
        "user_id": "86a4e1be-372f-43ef-b469-e7ee05b5d7ec",
        "username": "Luan Limas",
        "password": "$2b$12$qIfECS.3Gg9BhM577U0CCOet9rQeNsbGLuj5i/wmr2BStagx22RbS",
        "email": "waltinhasdasdo@teste.com",
        "admin": True,
        "avatar": "https://www.origamid.com/wp-content/uploads/2019/05/igor.jpg"
    })
    assert response.status_code == 422
    assert response.json() == {
        "status": 422,
        "message": "validation error on put"
    }

def test_delete_user():
    response = client.delete("/v1/user/waltinho@teste.com")
    assert response.status_code == 200
    assert response.json() == {
        "status": 200, 
        "message": "user delete with sucess"
    }

def test_delete_invalid_user():
    response = client.delete("/v1/user/1234")
    assert response.status_code == 422
    assert response.json() == {
        "status": 422,
        "message": "error on delete"
    }
