from fastapi.testclient import TestClient
from application import create_app # file chứa FastAPI app

app = create_app()
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_signup():
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "123456",
        "password_confirmation": "123456"
    })
    assert response.status_code == 200
    assert "email" in response.json()


def test_login():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()