import pytest
from fastapi.testclient import TestClient
from application import create_app
from httpx import AsyncClient

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

app = create_app()

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/auth/login", json={"email": "test@example.com", "password": "123456"})
        assert response.status_code == 200

# def test_login(client):
#     response = client.post("/auth/login", json={
#         "email": "test@example.com",
#         "password": "123456"
#     })
#     assert response.status_code == 200
#     assert "access_token" in response.json()