import os
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database("ecommerce")

def get_db() -> AsyncIOMotorDatabase:
    return client.get_database("ecommerce")