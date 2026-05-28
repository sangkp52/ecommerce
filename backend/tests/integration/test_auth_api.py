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
async def test_create_get_update_delete_product():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # CREATE
        payload = {"name": "Test Product", "price": 100}
        response = await client.post("/products/", json=payload)
        assert response.status_code == 200
        product = response.json()
        product_id = product["_id"]

        # GET ALL
        response = await client.get("/products/")
        assert response.status_code == 200
        assert any(p["_id"] == product_id for p in response.json())

        # GET ONE
        response = await client.get(f"/products/{product_id}")
        assert response.status_code == 200
        assert response.json()["_id"] == product_id

        # UPDATE
        update_payload = {"price": 120}
        response = await client.put(f"/products/{product_id}", json=update_payload)
        assert response.status_code == 200
        assert response.json()["price"] == 120

        # DELETE
        response = await client.delete(f"/products/{product_id}")
        assert response.status_code == 204

        # GET AFTER DELETE
        response = await client.get(f"/products/{product_id}")
        assert response.status_code == 404