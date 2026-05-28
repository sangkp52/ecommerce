import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set")

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("ecommerce")


def get_db():
    return db