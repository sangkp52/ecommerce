import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from application import create_app
from bson import ObjectId

app = create_app()

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_signup(client):
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "123456",
        "password_confirmation": "123456"
    })
    assert response.status_code == 200
    assert "email" in response.json()

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/auth/login", json={"email": "test@example.com", "password": "123456"})
        assert response.status_code == 200
        
@pytest.mark.asyncio
async def test_crud_product():
    async with AsyncClient(app=app, base_url="http://test") as client:

        # CREATE (TẠO MỚI)
        payload = {
            "name": "Test Product",
            "description": "This is a test product",
            "price": 100.0
        }

        response = await client.post("/products/", json=payload)
        assert response.status_code == 200

        product = response.json()
        
        # Lấy ID linh hoạt từ cả '_id' hoặc 'id' phòng trường hợp Pydantic mapping
        product_id = str(product.get("_id") or product.get("id") or "")
        
        # Kiểm tra xem ID có bị rỗng không, nếu rỗng sẽ in ra toàn bộ response để debug
        assert product_id, f"Backend không trả về ID hợp lệ. Dữ liệu nhận được: {product}"

        # GET ALL (LẤY TẤT CẢ)
        response = await client.get("/products/")
        assert response.status_code == 200

        # GET ONE (LẤY MỘT SẢN PHẨM)
        response = await client.get(f"/products/{product_id}")
        assert response.status_code == 200

        product_data = response.json()
        assert isinstance(product_data, dict), f"Kỳ vọng dict nhưng nhận được {type(product_data)}"
        assert product_data["name"] == "Test Product"

        # UPDATE (CẬP NHẬT)
        update_payload = {
            "price": 150.0
        }

        response = await client.put(
            f"/products/{product_id}",
            json=update_payload
        )

        assert response.status_code == 200
        assert response.json()["price"] == 150.0

        # DELETE (XÓA)
        response = await client.delete(f"/products/{product_id}")
        assert response.status_code == 204

        # VERIFY DELETE (XÁC MINH ĐÃ XÓA)
        response = await client.get(f"/products/{product_id}")
        assert response.status_code == 404