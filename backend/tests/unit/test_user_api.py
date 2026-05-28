import pytest
from httpx import AsyncClient
from application import create_app
from bson import ObjectId

# Import hàm get_db gốc từ dự án của bạn
from src.database import get_db 

class MockInsertResult:
    """Giả lập kết quả trả về của MongoDB khi insert thành công"""
    def __init__(self):
        self.inserted_id = ObjectId()

class Collection:
    def __init__(self):
        self.data = {}

    async def find_one(self, query):
        email = query.get("email")
        return self.data.get(email)

    async def insert_one(self, doc):
        self.data[doc["email"]] = doc
        return MockInsertResult()

class DB:
    def __init__(self):
        self.users = Collection()

    def __getitem__(self, name):
        if name == "users":
            return self.users

# Đổi sang Async Fixture để tương thích luồng Async của Router
@pytest.fixture
async def async_client():
    app = create_app()
    db = DB()

    # Override dependency dùng DB giả lập
    app.dependency_overrides[get_db] = lambda: db

    # Khởi tạo AsyncClient thay vì TestClient đồng bộ
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_user_success(async_client):
    """Test API đăng ký user thành công qua endpoint /auth/signup"""
    payload = {
        "email": "test@gmail.com",
        "password": "mysecurepassword",
        "password_confirmation": "mysecurepassword"
    }
    
    # Gọi API bằng await async_client.post
    response = await async_client.post("/auth/signup", json=payload)
    
    assert response.status_code == 200
    assert response.json()["email"] == "test@gmail.com"
    assert "id" in response.json()


@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    """Test API đăng nhập thất bại khi tài khoản chưa tồn tại"""
    payload = {
        "email": "unknown@gmail.com",
        "password": "any_password"
    }
    
    response = await async_client.post("/auth/login", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"error": "user does not exist"}