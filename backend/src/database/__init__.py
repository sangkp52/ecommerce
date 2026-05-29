from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


def get_db():
    client = AsyncIOMotorClient(MONGO_URI)
    return client["ecommerce"]