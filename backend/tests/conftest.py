import pytest
from fastapi.testclient import TestClient
from application import create_app # hoặc create_app

class DB:
    def __init__(self):
        self.users = []

    async def find_one(self, query):
        for u in self.users:
            if u["email"] == query["email"]:
                return u
        return None

    async def insert_one(self, data):
        self.users.append(data)
        return data

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: FakeDB()
    with TestClient(app) as c:
        yield c