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