import pytest
from fastapi.testclient import TestClient
from application import create_app
from src.database import get_db

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
    """Test API đăng ký user thành công qua endpoint /auth/signup"""
    payload = {
        "email": "test@gmail.com",
        "password": "mysecurepassword",
        "password_confirmation": "mysecurepassword"  # Cần khớp với UserSignupSchema của bạn
    }
    
    # ĐỔI TẠI ĐÂY: Dùng đúng URL /auth/signup từ file router của bạn
    response = client.post("/auth/signup", json=payload)
    
    assert response.status_code == 200
    assert response.json()["email"] == "test@gmail.com"
    assert "id" in response.json()  # Đảm bảo router trả về trường id


def test_login_user_not_found(client):
    """Test API đăng nhập thất bại khi tài khoản chưa tồn tại"""
    payload = {
        "email": "unknown@gmail.com",
        "password": "any_password"
    }
    
    # Dùng đúng URL /auth/login từ file router của bạn
    response = client.post("/auth/login", json=payload)
    
    assert response.status_code == 200  # Vì router của bạn return dict lỗi trực tiếp thay vì raise HTTPException nên status_code vẫn là 200
    assert response.json() == {"error": "user does not exist"}