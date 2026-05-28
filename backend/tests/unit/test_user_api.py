import pytest
from fastapi.testclient import TestClient
from application import create_app

class Collection:
    def __init__(self):
        self.data = {}

    async def find_one(self, query):
        email = query.get("email")
        return self.data.get(email)

    async def insert_one(self, doc):
        self.data[doc["email"]] = doc

class DB:
    def __init__(self):
        self.users = Collection()

    def __getitem__(self, name):
        if name == "users":
            return self.users

@pytest.fixture
def client():
    app = create_app()

    db = DB()

    # override dependency
    app.dependency_overrides[get_db] = lambda: db

    return TestClient(app)

def test_register_user_success(client):
    """Test API đăng ký user thông qua TestClient và DB giả lập"""
    payload = {
        "email": "test@gmail.com",
        "password": "mysecurepassword"
    }
    # Gọi endpoint đăng ký (bạn thay đổi router của bạn cho đúng, ví dụ /users/ hoặc /signup)
    response = client.post("/users/", json=payload)
    
    assert response.status_code == 200 or response.status_code == 21
    assert response.json()["email"] == "test@gmail.com"


def test_get_user_not_found(client):
    """Test API lấy thông tin user không tồn tại"""
    # Gọi một email chưa từng được insert vào cái DB giả lập ở trên
    response = client.get("/users/unknown@gmail.com")
    
    assert response.status_code == 404