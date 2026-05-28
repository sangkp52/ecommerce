from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27018")


def get_db():
    client = AsyncIOMotorClient(MONGO_URI)
    return client["ecommerce"]