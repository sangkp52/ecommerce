import pytest
from datetime import datetime
from httpx import ASGITransport, AsyncClient
from application import create_app

# Khởi tạo app 
app = create_app()

@pytest.fixture
async def client():
    # Sử dụng ASGITransport để đồng bộ hóa với app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# --- UNIT & INTEGRATION TESTS ---

@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_signup(client):
    random_email = f"test_{datetime.utcnow().timestamp()}@example.com"
    response = await client.post("/auth/signup", json={
        "email": random_email,
        "password": "123456",
        "password_confirmation": "123456"
    })
    data = response.json()
    if response.status_code == 200:
        assert "email" in data
    else:
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_login(client):
    response = await client.post("/auth/login", json={"email": "test@example.com", "password": "123456"})
    assert response.status_code == 200
        
@pytest.mark.asyncio
async def test_crud_product(client):
    payload = {"name": "Test Product", "description": "This is a test product", "price": 100.0}
    response = await client.post("/products/", json=payload)
    assert response.status_code == 200
    
    product = response.json()
    product_id = str(product.get("_id") or product.get("id") or "")
    assert product_id, "Backend không trả về ID"
    
    # Test GET, UPDATE, DELETE
    assert (await client.get("/products/")).status_code == 200
    assert (await client.put(f"/products/{product_id}", json={"price": 150.0})).status_code == 200
    assert (await client.delete(f"/products/{product_id}")).status_code == 204
    assert (await client.get(f"/products/{product_id}")).status_code == 404

# --- METRICS & ROUTE TESTS ---

@pytest.mark.asyncio
async def test_metrics_endpoint_exists(client):
    response = await client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

@pytest.mark.asyncio
async def test_request_generates_metrics(client):
    await client.get("/") 
    metrics = await client.get("/metrics")
    assert metrics.status_code == 200
    assert "http_requests_total" in metrics.text

@pytest.mark.asyncio
async def test_app_routes_work(client):
    response = await client.get("/")
    assert response.status_code in [200, 401, 404]

@pytest.mark.asyncio
async def test_metrics_not_crash(client):
    for _ in range(5):
        await client.get("/")
    res = await client.get("/metrics")
    assert res.status_code == 200